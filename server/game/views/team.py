from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from user.authentication import JwtAuthentication

from game.models import Team, Response as QuestionResponse, TriviaEvent

channel_layer = get_channel_layer()


class TeamView(APIView):
    authentication_classes = [JwtAuthentication]

    def get(self, request):
        user_data = request.user.to_json()

        return Response({"user_data": user_data})


class TeamCreateView(APIView):
    """Create a team and set active"""
    pass


class TeamSelectView(APIView):
    """Select an existing team add to a players teams and set active"""
    pass


class TeamJoinView(APIView):
    """Set an existing player's team active"""
    authentication_classes = [JwtAuthentication]

    @method_decorator(csrf_protect)
    def post(self, request):
        team_id = request.data.get("team_id")

        user = request.user
        requested_team = user.teams.filter(id=team_id)
        if not requested_team.exists():
            return Response({ "detail": "Team Not Found"}, status=HTTP_404_NOT_FOUND)

        user.active_team = requested_team.first()
        user.save()

        return Response({"active_team_id": team_id})
