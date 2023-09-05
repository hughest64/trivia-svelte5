from channels.layers import get_channel_layer

from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework.response import Response
from rest_framework.views import APIView

from game.models import Team
from game.utils.socket_classes import SendEventMessage
from game.views.validation.exceptions import TeamNotFound
from game.views.validation.data_cleaner import DataCleaner, DataValidationError

from user.authentication import JwtAuthentication
from user.models import User

channel_layer = get_channel_layer()


class TeamView(APIView):
    authentication_classes = [JwtAuthentication]

    def get(self, request):
        user_data = request.user.to_json()

        return Response({"user_data": user_data})


class TeamCreateView(APIView):
    """Create a team and set active"""

    authentication_classes = [JwtAuthentication]

    @method_decorator(csrf_protect)
    def post(self, request):
        user: User = request.user
        data = DataCleaner(request.data)
        team_name = data.as_string("team_name")
        try:
            team = Team.objects.create(name=team_name, create_password=True)
            team.members.add(request.user)
        except ValidationError as e:
            if hasattr(e, "error_dict") and "name" in e.error_dict:
                err = "That team name is too long. Please choose a shorter name."
            else:
                err = "An error occured in creating the team, please try again."
            raise DataValidationError(err)

        user.active_team = team
        user.save()

        return Response({"user_data": user.to_json()})


class TeamJoinView(APIView):
    """Add an existing team to a players teams and set active"""

    authentication_classes = [JwtAuthentication]

    @method_decorator(csrf_protect)
    def post(self, request):
        user = request.user
        data = DataCleaner(request.data)
        team_password = data.as_string("team_password")

        try:
            team = Team.objects.get(password=team_password)
            team.members.add(user)
            user.active_team = team
            user.save()
        except Team.DoesNotExist:
            raise TeamNotFound

        return Response({"user_data": user.to_json()})


class TeamSelectView(APIView):
    """Set an existing player's team active"""

    authentication_classes = [JwtAuthentication]

    @method_decorator(csrf_protect)
    def post(self, request):
        data = DataCleaner(request.data)
        team_id = data.as_int("team_id")

        user: User = request.user
        requested_team = user.teams.filter(id=team_id)
        if not requested_team.exists():
            raise TeamNotFound

        user.active_team = requested_team.first()
        user.save()

        return Response({"active_team_id": team_id})


class TeamUpdateName(APIView):
    authentication_classes = [JwtAuthentication]

    @method_decorator(csrf_protect)
    def post(self, request):
        data = DataCleaner(request.data)
        team_id = data.as_int("team_id")
        team_name = data.as_string("team_name")
        joincode = data.as_int("joincode")

        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            raise TeamNotFound

        team.name = team_name
        team.save()

        SendEventMessage(
            joincode=joincode,
            message={"msg_type": "teamname_update", "message": team.to_json()},
        )

        return Response({"success": True})
