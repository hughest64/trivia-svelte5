from channels.layers import get_channel_layer

from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_400_BAD_REQUEST

from game.models import Team
from game.utils.socket_classes import SendEventMessage
from game.views.validation.exceptions import TeamNotFound
from game.views.validation.data_cleaner import DataCleaner, DataValidationError

from user.authentication import JwtAuthentication
from user.models import User
from user.utils import Mailer

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
        # TODO: make updates to the DataCleaner to allow optional params and check for a password key here
        data = DataCleaner(request.data)
        team_name = data.as_string("team_name")

        try:
            team = Team.objects.create(name=team_name)
            team.members.add(request.user)
        except ValidationError as e:
            if "name" in getattr(e, "error_dict", {}):
                err = "That team name is too long. Please choose a shorter name."
            else:
                err = "An error occured in creating the team, please try again."
            raise DataValidationError(err)

        user.active_team = team
        user.save()

        Mailer(user, team).send_team_welcome()

        return Response({
            "team_data": {
                "team_name": team.name,
                "team_password": team.password,
                "qr": team.generate_qr()
            },
            "user_data": user.to_json()
            })


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
        team_id = data.as_int("team_id", request.user.active_team.id)
        team_name = data.as_string("team_name")
        joincode = data.as_int("joincode")

        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            raise TeamNotFound

        team.name = team_name
        team.save()

        if joincode:
            SendEventMessage(
                joincode=joincode,
                message={"msg_type": "teamname_update", "message": team.to_json()},
            )

        return Response({"detail": "The team name has been updated"})


# TODO: we should return a socket message to the event, need the joincode
class UpdateTeamPasswordView(APIView):
    authentication_classes = [JwtAuthentication]

    @method_decorator(csrf_protect)
    def post(self, request):
        data = DataCleaner(request.data)
        team_password = data.as_string("team_password")
        joincode = data.as_int("joincode")
        user = request.user

        try:
            team = Team.objects.get(id=user.active_team.id)
        except Team.DoesNotExist:
            raise TeamNotFound

        if team_password == team.password:
            return Response(
                {"detail": "The new password is the same as the old password"}
            )

        if Team.objects.exclude(id=team.id).filter(password=team_password).exists():
            return Response(
                {"detail": "You cannot use that password"}, status=HTTP_400_BAD_REQUEST
            )

        team.password = team_password
        team.save()

        if joincode:
            SendEventMessage(
                joincode=joincode,
                message={"msg_type": "teampassword_update", "message": team.to_json()},
            )

        return Response({"detail": "Your password has been updated"})


class RemoveTeamMembersView(APIView):
    authentication_classes = [JwtAuthentication]

    @method_decorator(csrf_protect)
    def post(self, request):
        data = DataCleaner(request.data)
        members = data.as_string_array("usernames")
        team_id = data.as_int("team_id")

        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            raise TeamNotFound

        members_to_keep = [
            m.id for m in team.members.all() if m.username not in members
        ]
        team.members.set(members_to_keep)

        # do we need a socket message?

        return Response({"success": True})
