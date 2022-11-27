from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from user.authentication import JwtAuthentication
from user.serializers import UserSerializer

from ..models import Game, Location, EventRoundState, EventQuestionState, TriviaEvent, queryset_to_json

channel_layer = get_channel_layer()

# TODO: remove once creating event is implemented
DEMO_EVENT_JOIN_CODE = 1234


def parse_reveal_payload(data):
    """"""
    # TODO: error handling
    key = data.get("key", "")
    round, question = key.split(".")
    revealed = bool(data.get("value", ""))

    return {"key": key, "round": round, "question": question, "revealed": revealed}


class EventHostView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, joincode):
        """fetch a specific event from the joincode parsed from the url"""
        user_serializer = UserSerializer(request.user)

        try:
            event = TriviaEvent.objects.get(join_code=joincode or DEMO_EVENT_JOIN_CODE)
        except TriviaEvent.DoesNotExist:
            return Response(
                {"detail": "an event with that join code does not exist"},
                status=HTTP_404_NOT_FOUND,
            )

        return Response({**event.to_json(), "user_data": user_serializer.data})


class EventSetupView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        """get this weeks games and a list of locations"""
        user = request.user
        locations = queryset_to_json(Location.objects.filter(active=True))
        # TODO: a filter of some sort to limit avialable games (should there be an active pram on the model?)
        games = queryset_to_json(Game.objects.all())
        user_serializer = UserSerializer(user)

        return Response(
            {
                "location_select_data": locations,
                "game_select_data": games,
                "user_data": user_serializer.data,
            }
        )

    @method_decorator(csrf_protect)
    def post(self, request):
        """create a new event or fetch an existing one with a specified game/location combo"""
        user = request.user
        # TODO: get or create
        event = TriviaEvent.objects.get(join_code=DEMO_EVENT_JOIN_CODE)
        user_serializer = UserSerializer(user)

        # TODO: this could just return the join code since the data won't be loaded from this response
        return Response(
            {
                "event_data": event.to_json()["event_data"],
                "user_data": user_serializer.data,
            }
        )


class QuestionRevealView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    # TOOD: csrf protect
    def post(self, request, joincode):
        try:
            data = parse_reveal_payload(request.data)
            async_to_sync(channel_layer.group_send)(
                f"event_{joincode}",
                {
                    "type": "event_update",
                    "msg_type": "question_reveal_popup",
                    "store": "popupData",
                    "message": {
                        "key": data.get("key", "").replace("all", "1"),
                        "value": data.get("revealed"),
                    },
                },
            )
        except Exception as e:
            # TODO: log e
            return Response({"detail": "An Error Occured"}, status=HTTP_400_BAD_REQUEST)

        return Response({"success": True})


class UpdateView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    # TOOD: csrf protect
    def post(self, request, joincode):
        data = parse_reveal_payload(request.data)
        key = data.get("key")
        round_number = data.get("round")
        question_number = data.get("question")
        revealed = data.get("revealed")

        try:

            questionState = EventQuestionState.objects.select_related("event").get(
                event__join_code=joincode,
                round_number=round_number,
                question_number=question_number,
            )
        except EventQuestionState.DoesNotExist:
            return Response(
                data={"detail": f"Question State for Key {key} Does Not Exist"},
                status=HTTP_404_NOT_FOUND,
            )

        # only update current values if the trivia event has been advanced
        updated = False
        event = questionState.event
        if revealed and key > event.current_question_key:
            event.current_round_number = round_number
            event.current_question_number = question_number
            event.save()
            updated = True

        questionState.question_displayed = revealed
        questionState.save()

        async_to_sync(channel_layer.group_send)(
            f"event_{joincode}",
            {
                "type": "event_update",
                "msg_type": "question_update",
                "store": "questionStates",
                "message": {"key": key, "value": revealed},
            },
        )

        if updated:
            async_to_sync(channel_layer.group_send)(
                f"event_{joincode}",
                {
                    "type": "event_update",
                    "msg_type": "current_data_update",
                    "store": "currentEventData",
                    "message": {
                        "question_key": key,
                        "question_number": int(question_number),
                        "round_number": int(round_number),
                    },
                },
            )

        return Response({"success": True})


class UpdateAllView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request, joincode):
        data = parse_reveal_payload(request.data)
        round_number = data.get("round")
        question_number = data.get("question")
        revealed = data.get("revealed")

        if question_number != "all":
            return Response({"detail": "Bad Request"}, status=HTTP_400_BAD_REQUEST)

        event_states = EventQuestionState.objects.filter(
            event__join_code=joincode, round_number=round_number
        )
        event_states.update(question_displayed=revealed)

        updated = False
        event = event_states.first().event
        # TODO: we may not need to calculate these (just use 1)
        min_key = min(*[state.key for state in event_states])
        min_question_number = min(*[state.question_number for state in event_states])
        if revealed and min_key > event.current_question_key:
            event.current_round_number = round_number
            event.current_question_number = min_question_number
            event.save()
            updated = True

        async_to_sync(channel_layer.group_send)(
            f"event_{joincode}",
            {
                "type": "event_update",
                "msg_type": "question_update_all",
                "store": "questionStates",
                "message": {"round_number": round_number, "value": revealed},
            },
        )

        if updated:
            async_to_sync(channel_layer.group_send)(
                f"event_{joincode}",
                {
                    "type": "event_update",
                    "msg_type": "current_data_update",
                    "store": "currentEventData",
                    "message": {
                        "question_key": min_key,
                        "question_number": int(min_question_number),
                        "round_number": int(round_number),
                    },
                },
            )

        return Response({"success": True})


class RoundLockView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request, joincode):
        data = request.data
        round_number = int(data.get("round_number"))
        locked = bool(data.get("value"))

        try:
            round_state = EventRoundState.objects.get(
                event__join_code=joincode, round_number=round_number
            )
        except EventRoundState.DoesNotExist:
            return Response(
                {"detail": f"Round state for round {round_number} does not exist"}
            )

        round_state.locked = locked
        round_state.save()

        async_to_sync(channel_layer.group_send)(
            f"event_{joincode}",
            {
                "type": "event_update",
                "msg_type": "round_update",
                "store": "roundStates",
                "message": {"round_number": round_number, "value": locked},
            },
        )

        return Response({ "success": True })
