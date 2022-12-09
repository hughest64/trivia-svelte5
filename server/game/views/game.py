from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from user.authentication import JwtAuthentication

from game.models import Team, Response as QuestionResponse, TriviaEvent
from game.models.utils import queryset_to_json

channel_layer = get_channel_layer()


class EventView(APIView):
    authentication_classes = [JwtAuthentication]

    def get(self, request, joincode):
        """fetch a specific event from the joincode parsed from the url"""
        user_data = request.user.to_json()

        active_team_qs = Team.objects.filter(id=request.user.active_team_id)
        if not request.user.active_team_id or not active_team_qs.exists:
            return Response(
                {"detail": "You must be on a team to view this page"},
                status=HTTP_403_FORBIDDEN,
            )

        try:
            event = TriviaEvent.objects.get(join_code=joincode)
        except TriviaEvent.DoesNotExist:
            return Response(
                {"detail": f"An event with join code {joincode} was not found"},
                status=HTTP_404_NOT_FOUND,
            )

        question_responses = QuestionResponse.objects.filter(
            event__join_code=joincode, team_id=request.user.active_team_id
        )

        return Response(
            {
                **event.to_json(),
                "user_data": user_data,
                "response_data": queryset_to_json(question_responses),
            }
        )


class EventJoinView(APIView):
    authentication_classes = [JwtAuthentication]

    def get(self, request):
        """return user data to /game/join"""
        user_data = request.user.to_json()

        return Response({"user_data": user_data})


class ResponseView(APIView):
    authentication_classes = [JwtAuthentication]

    @method_decorator(csrf_protect)
    def post(self, request, joincode):
        team_id = request.data.get("team_id")
        question_id = request.data.get("question_id")
        response_text = request.data.get("response_text")

        active_team_qs = Team.objects.filter(id=request.user.active_team_id)
        if not request.user.active_team_id or not active_team_qs.exists:
            return Response(
                {"detail": "You must be on a team to view this page"},
                status=HTTP_403_FORBIDDEN,
            )

        try:
            event = TriviaEvent.objects.get(join_code=joincode)
        except TriviaEvent.DoesNotExist:
            return Response(
                {"detail": f"event with join code {joincode} not found"},
                status=HTTP_404_NOT_FOUND,
            )

        question_response, created = QuestionResponse.objects.get_or_create(
            team_id=team_id,
            event=event,
            game_question_id=question_id,
            defaults={"recorded_answer": response_text}
        )
        if not created:
            question_response.recorded_answer = response_text
            question_response.save()

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