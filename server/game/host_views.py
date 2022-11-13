from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from user.authentication import JwtAuthentication

from .models import EventQuestionState, TriviaEvent, get_rq_from_key

channel_layer = get_channel_layer()


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


class QuestionRevealView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    # TOOD: csrf protect
    def post(self, request, joincode):
        try:
            data = request.data
            async_to_sync(channel_layer.group_send)(
                f"event_{joincode}",
                {
                    "type": "event_update",
                    "msg_type": "question_reveal",
                    "store": "popupData",
                    "message": {
                        "key": data.get("key"),
                        "value": bool(data.get("value")),
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
        data = request.data
        key = data.get("key")
        round_number, question_number = get_rq_from_key(key)
        revealed = bool(data.get("value"))

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
                        "question_number": question_number,
                        "round_number": round_number,
                    },
                },
            )

        return Response({"message": "database updated"})
