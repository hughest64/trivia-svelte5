from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework.response import Response
from rest_framework.views import APIView

from user.authentication import JwtAuthentication

from game.models import QuestionResponse
from game.models.utils import queryset_to_json
from game.views.validation.data_cleaner import (
    DataCleaner,
    DataValidationError,
    TeamRequired,
    get_event_or_404,
)
from user.models import User

channel_layer = get_channel_layer()


class EventView(APIView):
    authentication_classes = [JwtAuthentication]

    def get(self, request, joincode):
        """fetch a specific event from the joincode parsed from the url"""
        user: User = request.user
        if not user.active_team:
            raise TeamRequired

        event = get_event_or_404(join_code=joincode)
        question_responses = QuestionResponse.objects.filter(
            event__join_code=joincode, team=user.active_team
        )

        return Response(
            {
                **event.to_json(),
                "user_data": user.to_json(),
                "response_data": queryset_to_json(question_responses),
            }
        )


class EventJoinView(APIView):
    authentication_classes = [JwtAuthentication]

    def get(self, request):
        user_data = request.user.to_json()

        return Response({"user_data": user_data})


class ResponseView(APIView):
    authentication_classes = [JwtAuthentication]

    @method_decorator(csrf_protect)
    def post(self, request, joincode):
        try:
            data = DataCleaner(request.data)
            team_id = data.as_int("team_id")
            question_id = data.as_int("question_id")
            response_text = data.as_string("response_text")
        except DataValidationError as e:
            return Response(e.response)

        if not request.user.active_team:
            raise TeamRequired

        event = get_event_or_404(join_code=joincode)
        question_response, _ = QuestionResponse.objects.get_or_create(
            team_id=team_id,
            event=event,
            game_question_id=question_id,
        )
        if not question_response.locked:
            question_response.recorded_answer = response_text
            question_response.grade()
            question_response.save()

        async_to_sync(channel_layer.group_send)(
            f"team_{team_id}_event_{joincode}",
            {
                "type": "team_update",
                "msg_type": "team_response_update",
                "message": question_response.to_json(),
            },
        )

        return Response({"success": True})
