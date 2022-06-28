import json
import random

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_401_UNAUTHORIZED

from user.authentication import JwtAuthentication
from user.serializers import UserSerializer
from .models import Team, Location, Game
from .serializers import TeamSerializer, LocationSerializer, GameSerializer

# TODO: dev data only, replace once models are in place
with open(settings.BASE_DIR.parent / 'data' / 'teams.json', 'r') as f:
    team_data = json.load(f)
team_classes = [Team(**data) for data in team_data]

with open(settings.BASE_DIR.parent / 'data' / 'event_setup_data.json', 'r') as f2:
    event_select_data = json.load(f2)
location_classes = [Location(**data) for data in event_select_data.get("locations", [])]
game_classes = [Game(**data) for data in event_select_data.get("games", [])]

with open(settings.BASE_DIR.parent / 'data' / 'game_data_merged.json', 'r') as event_file:
    event_data = json.load(event_file)

# TODO: classes
class UserTeamsView(APIView):
    authentication_classes = [SessionAuthentication, JwtAuthentication]

    def get(self, request):
        # TODO: eventually teams will be a relation on the user model
        # so we'll be able to fetch all of this in a single serializer
        teamSerializer = TeamSerializer(team_classes, many=True)
        userSerializer = UserSerializer(request.user)

        return Response(
            {
                "user_data": userSerializer.data,
                "user_teams": teamSerializer.data,
            }
        )


class TeamSelectView(APIView):
    authentication_classes = [SessionAuthentication, JwtAuthentication]

    # TODO client side needs to send the csrf token for this
    # @method_decorator(csrf_protect)
    def post(self, request):
        team_id = request.data.get("team_id")
        if team_id:
            user = request.user
            # TODO: maybe don't lookup with user? we do allow "guests" on a team
            # (i.e send someone a join code to join the team)
            # requested_team = Team.models.filter(id=team_id, user=request.user)
            # if requested_team.exists():
            user.active_team_id = team_id
            user.save()
            #   set the team on the user and save()

            # else:
                # send a bad response

        return Response({"active_team_id": team_id})


class EventSetupView(APIView):
    # TODO: how to handle jwt and session auth?
    authentication_classes = [JwtAuthentication]
    # authentication_classes = [SessionAuthentication, JwtAuthentication]
    # permission_classes = [IsAdminUser]

    def get(self, request):
        """ get this weeks games and a list of locations """
        # TODO: customer permission class?
        user = request.user
        if (user.is_authenticated and not user.is_staff):
            raise PermissionDenied(code=HTTP_401_UNAUTHORIZED)

        locationSerializer = LocationSerializer(location_classes, many=True)
        gameSerializer = GameSerializer(game_classes, many=True)

        return Response(
            {
                "location_select_data": locationSerializer.data,
                "game_select_data": gameSerializer.data
            }
        )

    def post(self, request):
        """ create a new event or fetch an existing one with a specified game/location combo"""
        user = request.user
        if (user.is_authenticated and not user.is_staff):
            raise PermissionDenied(code=HTTP_401_UNAUTHORIZED)
        # self.check_permissions(request)
        # validate the data
        # get or create
        event_data["join_code"] = random.randint(1000, 9999)
        # serialize
        return Response(event_data)


class EventView(APIView):
    authentication_classes = [SessionAuthentication, JwtAuthentication]

    def get(self, request, joincode=None):
        """fetch a specific event from the joincode parsed from the url"""
        # use the join code to look up event data
        event_data["join_code"] = joincode
        # raise if it's a bad join code

        return Response(event_data)