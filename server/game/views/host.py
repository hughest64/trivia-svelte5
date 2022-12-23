from asgiref.sync import async_to_sync
from typing import List

from channels.layers import get_channel_layer

from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from game.views.validation.data_cleaner import (
    DataCleaner,
    DataValidationError,
    get_event_or_404,
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
)
from game.models.utils import queryset_to_json

channel_layer = get_channel_layer()

# TODO: remove once creating event is implemented
DEMO_EVENT_JOIN_CODE = 1234


class EventHostView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, joincode):
        """fetch a specific event from the joincode parsed from the url"""
        user_data = request.user.to_json()

        try:
            event = TriviaEvent.objects.get(join_code=joincode or DEMO_EVENT_JOIN_CODE)
        except TriviaEvent.DoesNotExist:
            return Response(
                {"detail": f"An event with join code {joincode} was not found"},
                status=HTTP_404_NOT_FOUND,
            )

        return Response({**event.to_json(), "user_data": user_data})


class EventSetupView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        """get this weeks games and a list of locations"""
        locations = queryset_to_json(Location.objects.filter(active=True))
        # TODO: add active param to game model, possibly use celery to update the attr
        games = queryset_to_json(Game.objects.all())
        user_data = request.user.to_json()

        return Response(
            {
                "location_select_data": locations,
                "game_select_data": games,
                "user_data": user_data,
            }
        )

    @method_decorator(csrf_protect)
    def post(self, request):
        """create a new event or fetch an existing one with a specified game/location combo"""
        event = TriviaEvent.objects.get(join_code=DEMO_EVENT_JOIN_CODE)
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
    def get_updated_event_data(
        round_number: int, question_numbers: List[int], event: TriviaEvent
    ):
        """update the current attributes of a trivia event when the game play advances"""
        event_data = {"event_updated": False}
        if (round_number > event.current_round_number) or (
            round_number == event.current_round_number
            and max(question_numbers) > event.current_question_number
        ):
            event.current_round_number = round_number
            event.current_question_number = (
                question_numbers[0]
                if len(question_numbers) == 1
                else min(question_numbers)
            )
            event.save()
            event_data = {
                "event_updated": True,
                "question_number": event.current_round_number,
                "round_number": event.current_round_number,
            }
        return event_data

    @method_decorator(csrf_protect)
    def post(self, request, joincode):
        try:
            data = DataCleaner(request.data)
            round_number = data.as_int("round_number")
            question_numbers = data.as_int_array("question_numbers", deserialize=True)
            reveal = data.as_bool("reveal")
            update = data.as_bool("update")
        except DataValidationError as e:
            return Response(e.response())

        # notify the event group but don't update the db
        if not update:
            async_to_sync(channel_layer.group_send)(
                f"event_{joincode}",
                {
                    "type": "event_update",
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

            current_event_data = self.get_updated_event_data(
                round_number, question_numbers, event
            )
            async_to_sync(channel_layer.group_send)(
                f"event_{joincode}",
                {
                    "type": "event_update",
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
            return Response(e.response())

        event = get_event_or_404(joincode)

        round_state, _ = EventRoundState.objects.update_or_create(
            event=event,
            round_number=round_number,
            defaults={"locked": locked},
        )

        async_to_sync(channel_layer.group_send)(
            f"event_{joincode}",
            {
                "type": "event_update",
                "msg_type": "round_update",
                "message": round_state.to_json(),
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
                "host_response_data": response_data,
            }
        )

    @method_decorator(csrf_protect)
    def post(self, request, joincode):
        try:
            data = DataCleaner(request.data)
            id_list = data.as_int_array("response_ids", deserialize=True)
            funny = data.as_bool("funny")
            points_awarded = data.as_float("points_awarded")
        except DataValidationError as e:
            return Response(e.response())

        QuestionResponse.objects.filter(id__in=id_list).update(
            points_awarded=points_awarded, funny=funny
        )

        async_to_sync(channel_layer.group_send)(
            f"event_{joincode}",
            {
                "type": "event_update",
                "msg_type": "score_update",
                "message": request.data,  # NOTE: the id array will be serialized!
            },
        )

        return Response({"success": True})
