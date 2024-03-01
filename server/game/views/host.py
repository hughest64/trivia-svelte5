import logging

from django.db.models import QuerySet
from django.utils import timezone
from django.db import transaction

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework.exceptions import NotFound
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
    ChatMessage,
    Location,
    EventRoundState,
    EventQuestionState,
    TriviaEvent,
    TiebreakerResponse,
    QuestionResponse,
    Leaderboard,
    LeaderboardEntry,
    LEADERBOARD_TYPE_PUBLIC,
    LEADERBOARD_TYPE_HOST,
    PTS_ADJUSTMENT_OPTIONS_LIST,
    QUESTION_TYPE_TIE_BREAKER,
)
from game.models.utils import queryset_to_json
from game.processors import LeaderboardProcessor
from game.utils.socket_classes import SendEventMessage, SendHostMessage
from game.utils.number_convertor import NumberConvertor, NumberConversionException
from game.views.validation.exceptions import LeaderboardEntryNotFound

logger = logging.getLogger(__name__)


class EventHostView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, joincode):
        """fetch a specific event from the joincode parsed from the url"""
        user_data = request.user.to_json()
        event = get_event_or_404(joincode=joincode)
        chat_messages = ChatMessage.objects.filter(event=event, is_host_message=True)

        lb_entries = LeaderboardEntry.objects.filter(event=event)
        public_lb_entries = lb_entries.filter(leaderboard_type=LEADERBOARD_TYPE_PUBLIC)
        host_lb_entries = lb_entries.filter(leaderboard_type=LEADERBOARD_TYPE_HOST)
        through_round = None
        synced = True

        try:
            lb = Leaderboard.objects.get(event=event)
            through_round = getattr(lb, "public_through_round")
            synced = lb.synced

        except Leaderboard.DoesNotExist:
            pass

        response_data = QuestionResponse.objects.filter(event=event)  # []
        # for now, send all responses so we can do x/y correct summaries, maybe there is a better way in the future?
        # if passed a team id (i.e. leaderboard summary page), fetch respones for the team in question
        # if team_id is not None:
        #     response_data = queryset_to_json(
        #         QuestionResponse.objects.filter(event=event, team_id=team_id)
        #     )

        return Response(
            {
                **event.to_json(),
                "user_data": user_data,
                "chat_messages": queryset_to_json(chat_messages),
                "points_adjustment_reasons": PTS_ADJUSTMENT_OPTIONS_LIST,
                "response_data": queryset_to_json(response_data),
                "leaderboard_data": {
                    "public_leaderboard_entries": queryset_to_json(public_lb_entries),
                    "host_leaderboard_entries": queryset_to_json(host_lb_entries),
                    "through_round": through_round,
                    "synced": synced,
                },
            }
        )


class RecentEventView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        recent_hosted_events = TriviaEvent.objects.filter(host=request.user)[:5]
        return Response(
            {
                "recent_events": [e.game_json() for e in recent_hosted_events],
                "user_data": request.user.to_json(),
            }
        )


class EventSetupView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        """get this weeks games and a list of locations"""
        games = Game.objects.filter(active_through__gte=timezone.localdate())
        blocks = set([game.block_code for game in games])
        user_data = request.user

        todays_events = TriviaEvent.objects.filter(date=timezone.localdate())

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
                "todays_events": [
                    {
                        "game_id": e.game.id,
                        "location_id": (
                            e.location.id if e.location is not None else None
                        ),
                    }
                    for e in todays_events
                ],
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
            game=game, host=request.user, location=location, player_limit=player_limit
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
    def set_current_question(event: TriviaEvent, updated_state: EventQuestionState):
        """
        Determine whether on not to update the current round and question in a Trivia Event based on
        the index of the updated question state object compared to it's index in all event questions.
        Only update the current question if the indicies match; i.e. all states before the updated state
        must be revealed.
        Note that progress of a game never moves backwards. Unrevealing a question does NOT reset the current
        round or question.
        """
        # look up all revealed question states and sort the keys
        displayed_states = event.question_states.filter(question_displayed=True)
        displayed_state_keys = [s.key for s in displayed_states]

        # look up all questions keys (excluding tiebreakers) and sort
        all_question_keys = [
            q.key for q in event.game.game_questions.exclude(round_number=0)
        ]

        # check for matching indicies and update the event if appropriate
        question_key_index = all_question_keys.index(updated_state.key)
        displayed_state_index = displayed_state_keys.index(updated_state.key)
        should_update = question_key_index == displayed_state_index

        if should_update:
            event.current_question_number = updated_state.question_number
            event.current_round_number = updated_state.round_number
            event.save()

        return {
            "event_updated": should_update,
            "question_number": event.current_question_number,
            "round_number": event.current_round_number,
        }

    @method_decorator(csrf_protect)
    def post(self, request, joincode):
        data = DataCleaner(request.data)
        round_number = data.as_int("round_number")
        question_numbers = data.as_int_array("question_numbers", deserialize=True)
        reveal = data.as_bool("reveal")
        update = data.as_bool("update")

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
                updated_states.append(question_state)

            current_event_data = {
                "event_updated": False,
                "question_number": event.current_question_number,
                "round_number": event.current_round_number,
            }

            # update the current question of the game if questions were revealed
            # use the first question state in the case of multiple state updates
            if reveal:
                current_event_data.update(
                    self.set_current_question(event, updated_states[-1])
                )

            SendEventMessage(
                joincode,
                {
                    "msg_type": "question_state_update",
                    "message": {
                        "question_states": queryset_to_json(updated_states),
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

        # update the host leaderboard
        lb_processor = LeaderboardProcessor(event)
        leaderboard_data = lb_processor.update_host_leaderboard(
            through_round=event.max_locked_round()
        )

        resp_summary = None
        if locked:
            resp_summary = QuestionResponse.summarize(event=event)

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
        if hasattr(event, "leaderboard"):
            synced = event.leaderboard.synced
        else:
            synced = False
            # NOTE: this is unlikely to occur, be it is possible.
            logger.error(
                f"No leaderboard was found for event with joincode {joincode}, cannot determine leaderboard sync status"
            )

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

        all_responses = QuestionResponse.objects.filter(event=event)
        host_response_data = []
        for question in questions:
            responses = all_responses.filter(game_question=question)
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

            host_response_data.extend(
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
                "response_data": queryset_to_json(all_responses),
                "host_response_data": host_response_data,
            }
        )

    @method_decorator(csrf_protect)
    def post(self, request, joincode):
        data = DataCleaner(request.data)
        id_list = data.as_int_array("response_ids", deserialize=True)
        funny = data.as_bool("funny")
        points_awarded = data.as_float("points_awarded")
        update_type = data.as_string("update_type")

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

        event = get_event_or_404(joincode=joincode)
        entries = LeaderboardEntry.objects.filter(
            event=event, leaderboard_type=LEADERBOARD_TYPE_HOST
        )

        try:
            lbe = entries.get(team_id=team_id)

        except LeaderboardEntry.DoesNotExist:
            raise LeaderboardEntryNotFound

        if adjustment_reason is not None:
            lbe.points_adjustment_reason = adjustment_reason
            lbe.save()

        leaderboard_data = None
        synced = False
        if points is not None:
            lbe.points_adjustment += points
            lbe.total_points += points
            lbe.save()

            lb_processor = LeaderboardProcessor(event=event)
            leaderboard_data, synced = lb_processor.rank_host_leaderboard(
                entries, event.max_locked_round()
            )

        message = {
            "msg_type": "leaderboard_update_host_entry",
            "message": {
                "entry": lbe.to_json(),
                "synced": synced,
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
        event = get_event_or_404(joincode=joincode)
        event.event_complete = True
        event.save()

        SendEventMessage(joincode, {"msg_type": "finish_game_popup", "message": ""})

        return Response({"success": True})


class TiebreakerView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, joincode):
        event = get_event_or_404(joincode=joincode)
        questions = GameQuestion.objects.filter(
            game=event.game, question__question_type=QUESTION_TYPE_TIE_BREAKER
        )
        responses = TiebreakerResponse.objects.filter(event=event)
        return Response(
            {
                "tiebreaker_questions": queryset_to_json(questions),
                "tiebreaker_responses": queryset_to_json(responses),
            }
        )

    @method_decorator(csrf_protect)
    def post(self, request, joincode):
        data = DataCleaner(request.data)
        tied_for_rank = data.as_int("tied_for_rank")
        question_id = data.as_int("question_id")
        team_data = request.data.get("team_data", [])

        try:
            question = GameQuestion.objects.get(id=question_id)
        except GameQuestion.DoesNotExist:
            raise NotFound(f"could not find Game Question with id {question_id}")

        event = get_event_or_404(joincode=joincode)
        leaderboard_entries = LeaderboardEntry.objects.filter(
            event=event,
            leaderboard_type=LEADERBOARD_TYPE_HOST,
        )

        through_round = event.max_locked_round()
        question_responses = []
        nan_respones = []
        with transaction.atomic():
            for entry in team_data:
                team_id = entry.get("team_id")
                answer = entry.get("answer")

                try:
                    NumberConvertor.convert_to_number(answer)
                except NumberConversionException as e:
                    return Response({"detail": str(e)}, status=400)

                question_response, _ = TiebreakerResponse.objects.update_or_create(
                    game_question=question,
                    event=event,
                    team_id=team_id,
                    defaults={"recorded_answer": answer, "round_number": through_round},
                )
                # if there is an error calculating the grade, we get the string "NaN"
                # we keep those separate to make sorting easier
                if question_response.grade == "NaN":
                    nan_respones.append(question_response)
                else:
                    question_responses.append(question_response)

        # grade is abs(actual_answer - resp.answer)
        sorted_resps = (
            sorted(question_responses, key=lambda resp: resp.grade) + nan_respones
        )

        resp_teams = [resp.team.id for resp in sorted_resps]
        # set lb rank (and rank) on each entry based on index + for_rank
        entries_to_update = leaderboard_entries.filter(team_id__in=resp_teams)
        for lb_entry in entries_to_update:
            lb_entry.tiebreaker_rank = tied_for_rank + resp_teams.index(
                lb_entry.team.id
            )
            lb_entry.tiebreaker_round_number = through_round
        LeaderboardEntry.objects.bulk_update(
            entries_to_update, fields=["tiebreaker_rank", "tiebreaker_round_number"]
        )
        ranked_entries, synced = LeaderboardProcessor(
            event=event
        ).rank_host_leaderboard(leaderboard_entries, through_round)

        message = {
            "msg_type": "leaderboard_update",
            "message": {
                "host_leaderboard_entries": ranked_entries,
                "tiebreaker_responses": queryset_to_json(sorted_resps),
                "synced": synced,
            },
        }

        SendHostMessage(joincode=joincode, message=message)

        return Response({"success": True})


class ReminderView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, joincode, reminder_type):
        event = get_event_or_404(joincode=joincode)
        team_ids = []
        if reminder_type == "megaround":
            entries = LeaderboardEntry.objects.filter(
                event=event,
                leaderboard_type=LEADERBOARD_TYPE_HOST,
                selected_megaround__isnull=True,
            )
            team_ids = [e.team.id for e in entries]
        elif reminder_type == "imageround":
            # get team_ids of all teams
            # event_team_ids = [t.id for t in event.event_teams.all()]
            # look up all rd 4 responses
            for team in event.event_teams:
                resps = QuestionResponse.objects.filter(event=event, team=team)
            # get the number of questions in rd 4
            # count rd 4 resps per team, if < total questions, add to team _ids

            pass

        SendEventMessage(
            joincode=joincode,
            message={
                "msg_type": "host_reminder",
                "message": {"type": reminder_type, "team_ids": team_ids},
            },
        )
        return Response({"success": True})
