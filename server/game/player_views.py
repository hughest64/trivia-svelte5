from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from user.authentication import JwtAuthentication

from game.models import Response as QuestionResponse, TriviaEvent

channel_layer = get_channel_layer()


class ResponseView(APIView):
    authentication_classes = [JwtAuthentication]

    def post(self, request, joincode):
        team_id = request.data.get("team_id")
        question_id = request.data.get("question_id")
        response_text = request.data.get("response_text")

        # TODO: permission class for this?
        # if request.user.active_team_id != request.data.get("team_id"):
        #     return Response(code=400, data={ "detail": "you are not on the right team"})

        try:
            question_response = QuestionResponse.objects.get(
                team_id=team_id,
                event__join_code=joincode,
                game_question_id=question_id,
            )
            question_response.recorded_answer = response_text
            question_response.save()

        except QuestionResponse.DoesNotExist:
            # TODO: can we look this up more efficiently?
            event = TriviaEvent.objects.filter(join_code=1234).first()
            question_response = QuestionResponse.objects.create(
                team_id=team_id,
                event=event,
                game_question_id=question_id,
                recorded_answer=response_text 
            )

        async_to_sync(channel_layer.group_send)(
            f"team_{team_id}_event_{joincode}",
            {
                "type": "team_update",
                "msg_type": "team_response_update",
                "store": "responseData",
                "message": question_response.to_json(),
            },
        )

        return Response({"success": True})
