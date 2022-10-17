from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from user.authentication import JwtAuthentication

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