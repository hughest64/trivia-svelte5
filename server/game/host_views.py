from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from user.authentication import JwtAuthentication

from .models import EventQuestionState, TriviaEvent, get_rq_from_key

channel_layer = get_channel_layer()


def parse_reveal_payload(data):
    """"""
    # TODO: error handling
    key = data.get("key", "")
    round, question = key.split(".")
    revealed = bool(data.get("value", ""))

    return {"key": key, "round": round, "question": question, "revealed": revealed}


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
                    "msg_type": "question_reveal",
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
            # TODO: remove joincode here once we have more than one event!
            joincode = 1234
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
                        "qustion_key": key,
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
        key = data.get("key")
        round_number = data.get("round")
        question_number = data.get("number")
        revealed = data.get("revealed")
        
        # TODO: why does this not work? (always a bad request)
        # cannot reveal a single qustion at this endpoint
        # if question_number != "all":
        #     return Response({"detail": "Bad Request"}, status=HTTP_400_BAD_REQUEST)

        # TODO: remove
        joincode = 1234
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
                        "question_number": min_question_number,
                        "round_number": round_number,
                    },
                },
            )

        return Response({"success": True})

class RoundLockView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request, joincode):
        print(request.user)
        # lookup the event
        # use request.data.get("round_number") and request.data.get("locked")
        # to update the db

        # if something goes wrong, send back a standard response

        # if successfull:
        async_to_sync(channel_layer.group_send)(
            f"event_{joincode}",
            {
                "type": "update_round_locks",
                "store": "eventData",
                "message": {"updated": "rounds"},
            },
        )
