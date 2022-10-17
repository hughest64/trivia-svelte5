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
        team_id = request.data.get("team_id")
        response_id = request.data.get("response_id")
        new_id = "".join(request.data.get("key", "").split("."))
        response_text = request.data.get("response_text")

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
            # no need to send anything back, could event use a 201 code
            async_to_sync(channel_layer.group_send)(
                f"team_{team_id}",  # TODO: make this tie to a team an event
                {
                    "type": "team_update_response",
                    "store": "responseData",
                    "message": {
                        "response_id": response_id or new_id,
                        "recorded_answer": response_text,
                        "key": request.data.get("key", ""),
                    },
                },
            )
            return Response()
