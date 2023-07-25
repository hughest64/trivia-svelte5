from typing import List

from django.db.models import QuerySet
from django.utils import timezone

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from game.processors import TriviaEventCreator
from game.views.validation.data_cleaner import (
    DataCleaner,
    DataValidationError,
    get_event_or_404,
    get_game_or_404,
    get_location_or_404,
)
from user.authentication import JwtAuthentication

from game.models import (
    Game,
    GameQuestion,
    Location,
    EventRoundState,
    EventQuestionState,
    TriviaEvent,
    QuestionResponse,
    Leaderboard,
    LeaderboardEntry,
    LEADERBOARD_TYPE_PUBLIC,
    LEADERBOARD_TYPE_HOST,
    PTS_ADJUSTMENT_OPTIONS_LIST,
)
from game.models.utils import queryset_to_json
from game.processors import LeaderboardProcessor
from game.utils.socket_classes import SendEventMessage, SendHostMessage
from game.views.validation.exceptions import LeaderboardEntryNotFound


class EventHostView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, joincode):
        """fetch a specific event from the joincode parsed from the url"""
        user_data = request.user.to_json()
        event = get_event_or_404(joincode=joincode)
        lb_entries = LeaderboardEntry.objects.filter(event=event)
        public_lb_entries = lb_entries.filter(leaderboard_type=LEADERBOARD_TYPE_PUBLIC)
        host_lb_entries = lb_entries.filter(leaderboard_type=LEADERBOARD_TYPE_HOST)
        host_megaround_list = [
            {"team_id": lbe.team.id, "has_megaround": bool(lbe.selected_megaround)}
            for lbe in public_lb_entries
        ]
        through_round = None
        synced = True

        try:
            lb = Leaderboard.objects.get(event=event)
            through_round = getattr(lb, "public_through_round")
            synced = lb.synced

        except Leaderboard.DoesNotExist:
            pass

        return Response(
            {
                **event.to_json(),
                "user_data": user_data,
                "points_adjustment_reasons": PTS_ADJUSTMENT_OPTIONS_LIST,
                "leaderboard_data": {
                    "public_leaderboard_entries": queryset_to_json(public_lb_entries),
                    "host_leaderboard_entries": queryset_to_json(host_lb_entries),
                    "host_megaround_list": host_megaround_list,
                    "through_round": through_round,
                    "synced": synced,
                },
            }
        )


class EventTeamResponsesView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, joincode, team_id):
        event = get_event_or_404(joincode=joincode)
        resps = QuestionResponse.objects.filter(event=event, team_id=team_id)

        return Response({"responses": queryset_to_json(resps)})


class EventSetupView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        """get this weeks games and a list of locations"""
        games = Game.objects.filter(active_through__gte=timezone.localdate())
        blocks = set([game.block for game in games])
        user_data = request.user

        # if the host has a home location set, put it at the front
        try:
            locations = [user_data.home_location.to_json()] + queryset_to_json(
                Location.objects.filter(active=True).exclude(
                    name=user_data.home_location.name
                )
            )
        except AttributeError:
            locations = queryset_to_json(Location.objects.filter(active=True))

        return Response(
            {
                "location_select_data": locations,
                "game_select_data": queryset_to_json(games),
                "game_block_data": blocks,
                "user_data": user_data.to_json(),
            }
        )

    @method_decorator(csrf_protect)
    def post(self, request):
        """create a new event or fetch an existing one with a specified game/location combo"""
        data = DataCleaner(request.data)
        player_limit = data.as_bool("player_limit")
        game_id = data.as_int("game_select")
        location_id = data.as_int("location_select")

        game = get_game_or_404(game_id)
        location = get_location_or_404(location_id)
        event = TriviaEventCreator(
            game=game, location=location, player_limit=player_limit
        ).event

        user_data = request.user.to_json()

        return Response(
            {
                "event_data": event.to_json()["event_data"],
                "user_data": user_data,
            }
        )


class QuestionRevealView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    @staticmethod
    def update_event_data(
        round_number: int, question_numbers: List[int], event: TriviaEvent
    ):
        """update the current attributes of a trivia event when the game play advances"""
        event_data = {"event_updated": False}
        if (round_number > event.current_round_number) or (
            round_number == event.current_round_number
            and max(question_numbers) > event.current_question_number
        ):
            event.current_round_number = round_number
            event.current_question_number = min(question_numbers)
            event.save()
            event_data = {
                "event_updated": True,
                "question_number": event.current_question_number,
                "round_number": event.current_round_number,
            }
        return event_data

    @method_decorator(csrf_protect)
    def post(self, request, joincode):
        # TODO: we don't need this try except
        try:
            data = DataCleaner(request.data)
            round_number = data.as_int("round_number")
            question_numbers = data.as_int_array("question_numbers", deserialize=True)
            reveal = data.as_bool("reveal")
            update = data.as_bool("update")
        except DataValidationError as e:
            return Response(e.response)

        # notify the event group but don't update the db
        if not update:
            SendEventMessage(
                joincode,
                {
                    "msg_type": "question_reveal_popup",
                    "message": {
                        "reveal": reveal,
                        "question_number": min(question_numbers),
                        "round_number": round_number,
                    },
                },
            )
        else:
            event = get_event_or_404(joincode)
            updated_states = []
            for num in question_numbers:
                question_state, _ = EventQuestionState.objects.update_or_create(
                    event=event,
                    round_number=round_number,
                    question_number=num,
                    defaults={"question_displayed": reveal},
                )
                updated_states.append(question_state.to_json())

            current_event_data = self.update_event_data(
                round_number, question_numbers, event
            )

            SendEventMessage(
                joincode,
                {
                    "msg_type": "question_state_update",
                    "message": {
                        "question_states": updated_states,
                        **current_event_data,
                    },
                },
            )

        return Response({"success": True})


class RoundLockView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    @method_decorator(csrf_protect)
    def post(self, request, joincode):
        try:
            data = DataCleaner(request.data)
            round_number = data.as_int("round_number")
            locked = data.as_bool("locked")
        except DataValidationError as e:
            return Response(e.response)

        event = get_event_or_404(joincode)

        round_state, _ = EventRoundState.objects.update_or_create(
            event=event,
            round_number=round_number,
            defaults={"locked": locked},
        )
        # lock or unlock responses for the round
        resps = QuestionResponse.objects.filter(
            event=event, game_question__round_number=round_number
        )
        resps.update(locked=locked)

        resp_summary = None
        if locked:
            resp_summary = QuestionResponse.summarize(event=event)
            # update the host leaderboard
            lb_processor = LeaderboardProcessor(event)
            leaderboard_data = lb_processor.update_host_leaderboard(
                through_round=event.max_locked_round() or round_state.round_number
            )

            # TODO: perhaps we don't need to send this as a separate host message
            # maybe we just ignore the piece of data if the broswer is on a /game route
            # send host message
            SendHostMessage(
                joincode,
                {
                    "msg_type": "leaderboard_update",
                    "message": leaderboard_data,
                },
            )

        SendEventMessage(
            joincode,
            {
                "msg_type": "round_update",
                "message": {
                    "round_state": round_state.to_json(),
                    "responses": queryset_to_json(resps),
                    "response_summary": resp_summary,
                },
            },
        )

        return Response({"success": True})


class ScoreRoundView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    @staticmethod
    def get_fuzz_ratio(resp_data):
        return resp_data.get("fuzz_ratio", 0)

    def get(self, request, joincode, round_number=None) -> Response:
        event = get_event_or_404(joincode)
        lb_entries = LeaderboardEntry.objects.filter(event=event)
        public_lb_entries = lb_entries.filter(leaderboard_type=LEADERBOARD_TYPE_PUBLIC)
        host_lb_entries = lb_entries.filter(leaderboard_type=LEADERBOARD_TYPE_HOST)
        through_round = None
        synced = True
        try:
            first = public_lb_entries.first()
            through_round = first.leaderboard.public_through_round
            synced = first.leaderboard.synced
        except AttributeError:
            pass

        if (
            round_number is not None
            and not event.game.game_rounds.filter(round_number=round_number).exists()
        ):
            return Response(
                {"detail": f"Round {round_number} not found for event {joincode}"}
            )

        # fetch all rounds, but filter to a specific round if appropriate
        questions: QuerySet[GameQuestion] = event.game.game_questions.all()
        if round_number is not None:
            questions = questions.filter(round_number=round_number)

        response_data = []
        for question in questions:
            responses = QuestionResponse.objects.filter(
                game_question=question, event=event
            )
            grouped_responses = {}
            for response in responses:
                text = response.recorded_answer.lower().strip()
                # don't process blank responses
                if not text:
                    continue
                grouped_responses.setdefault(
                    text,
                    {
                        "recorded_answer": response.recorded_answer,
                        "round_number": question.round_number,
                        "question_number": question.question_number,
                        "key": question.key,
                        "points_awarded": response.points_awarded,
                        "funny": response.funny,
                        "fuzz_ratio": response.fuzz_ratio,
                        "response_ids": [],
                    },
                )
                grouped_responses[text]["response_ids"].append(response.id)

            response_data.extend(
                sorted(
                    grouped_responses.values(), key=self.get_fuzz_ratio, reverse=True
                )
            )

        return Response(
            {
                "user_data": request.user.to_json(),
                **event.to_json(),
                "leaderboard_data": {
                    "public_leaderboard_entries": queryset_to_json(public_lb_entries),
                    "host_leaderboard_entries": queryset_to_json(host_lb_entries),
                    "through_round": through_round,
                    "synced": synced,
                },
                "host_response_data": response_data,
            }
        )

    @method_decorator(csrf_protect)
    def post(self, request, joincode):
        data = DataCleaner(request.data)
        id_list = data.as_int_array("response_ids", deserialize=True)
        funny = data.as_bool("funny")
        points_awarded = data.as_float("points_awarded")
        update_type = data.as_string("update_type")

        # TODO: should we use transaction.atomic and/or select_for_update here?
        resps = QuestionResponse.objects.filter(id__in=id_list)
        resps.update(points_awarded=points_awarded, funny=funny)

        # update the host leaderboard on point changes
        lb_entries = None
        response_summary = None
        if update_type == "points":
            event = get_event_or_404(joincode=joincode)
            lb_entries = LeaderboardProcessor(event=event).update_host_leaderboard(
                event.max_locked_round()
            )
            # TODO: selective updating would be MUCH preferred here
            # seems pretty easy to do if we add key=None as a kwarg to the method (or an array?)
            response_summary = QuestionResponse.summarize(event=event)

        msg_data = dict(request.data)
        # ensure we are sending back a deserialized list
        msg_data["response_ids"] = id_list

        SendEventMessage(
            joincode,
            {
                "msg_type": "score_update",
                "message": {
                    **msg_data,
                    "leaderboard_data": lb_entries,
                    "response_summary": response_summary,
                },
            },
        )

        return Response({"success": True})


class UpdateAdjustmentPointsView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    @method_decorator(csrf_protect)
    def post(self, request, joincode):
        data = DataCleaner(request.data)
        points = data.as_float("adjustment_points")
        adjustment_reason = data.as_int("adjustment_reason")
        team_id = data.as_int("team_id")

        entries = LeaderboardEntry.objects.filter(
            event__joincode=joincode, leaderboard_type=LEADERBOARD_TYPE_HOST
        )

        try:
            lbe = entries.get(team_id=team_id)

        except LeaderboardEntry.DoesNotExist:
            raise LeaderboardEntryNotFound

        if adjustment_reason is not None:
            lbe.points_adjustment_reason = adjustment_reason
            lbe.save()

        leaderboard_data = None
        if points is not None:
            lbe.points_adjustment += points
            lbe.total_points += points
            lbe.save()
            leaderboard_data = LeaderboardProcessor().rank_host_leaderboard(entries)

        lbe.leaderboard.synced = False
        lbe.leaderboard.save()

        message = {
            "msg_type": "leaderboard_update_host_entry",
            "message": {
                "entry": lbe.to_json(),
                "synced": False,
            },
        }

        if leaderboard_data is not None:
            message = {
                "msg_type": "leaderboard_update",
                "message": {
                    "host_leaderboard_entries": leaderboard_data,
                    "synced": False,
                },
            }

        SendHostMessage(joincode=joincode, message=message)

        return Response({"success": True})


class UpdatePublicLeaderboardView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    @method_decorator(csrf_protect)
    def post(self, request, joincode):
        event = get_event_or_404(joincode=joincode)

        lb_processor = LeaderboardProcessor(event=event)
        # public lb entries, public through round, and updated event round states
        updated_lb_data = lb_processor.sync_leaderboards()

        SendEventMessage(
            joincode,
            {"msg_type": "leaderboard_update", "message": updated_lb_data},
        )

        return Response({"success": True})


class RevealAnswersView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    @method_decorator(csrf_protect)
    def post(self, request, joincode):
        # get round number from payload
        event = get_event_or_404(joincode=joincode)

        # reveal rounds that are locked
        round_states = EventRoundState.objects.filter(event=event)
        for rs in round_states:
            rs.revealed = rs.locked
        EventRoundState.objects.bulk_update(round_states, fields=["revealed"])

        SendEventMessage(
            joincode,
            {
                "msg_type": "round_state_update",
                "message": {"round_states": queryset_to_json(round_states)},
            },
        )

        return Response({"success": True})


class FinishGameview(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    @method_decorator(csrf_protect)
    def post(self, request, joincode):
        # TODO: one option for backfilling responses is to do it here when the host finishes the game
        # another option is to use the completed field in an automated celery task that runs daily
        event = get_event_or_404(joincode=joincode)
        event.event_complete = True
        event.save()

        SendEventMessage(joincode, {"msg_type": "finish_game_popup", "message": ""})

        return Response({"success": True})


class ResolveTiebreakerView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    @method_decorator(csrf_protect)
    def post(self, request, joincode):
        """
        request.data = {
            tied_for_rank: 1,
            question_id: 45467,
            team_data: {
                team_id: 1234,
                answer: 673456
            }
        }
        """
        # get the event
        # get the tb question
        # get the lb entries
        # create (and grade) tb responese for each team
        # - grade is the difference between their answer and the actual answer
        # sort them by (absolute?) grade
        # set lb rank (and rank) on each entry based on index + for_rank
        # host socket message w/ updated lb entries (might need a new msg_type to handle selective updates)
        # send some data back the client

        return Response({"success": True})
