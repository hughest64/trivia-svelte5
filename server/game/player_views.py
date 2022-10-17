from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from user.authentication import JwtAuthentication

channel_layer = get_channel_layer()


class ResponseView(APIView):
    authentication_classes = [JwtAuthentication]

    def post(self, request, joincode, id):
        print(request.data)

        # TODO: permission class for this?
        # if request.user.active_team_id != request.data.get("team_id"):
        #     return Response(code=400, data={ "detail": "you are not on the right team"})

        # lock the transaction to prevent race conditions?
        try:
            "lookup up the object with id"
        except AttributeError:  # Response.DoesNotExist, not AttributeError
            "create the object"

        except Exception as e:  # if something goes wrong:
            # TODO: probably want better messaging back to the user
            return Response(status=400, data={"error": e})
        else:
            # use request.data["team_id"] to group send back to the team group
            # no need to send anything back, could event use a 201 code
            # async_to_sync(channel_layer.group_send)(
            #     f"event_{joincode}",
            #     {
            #         "type": "team_set_response",
            #         "store": "response",
            #         "message": {"r.q": "serialized response"},
            #     },
            # )
            return Response()
