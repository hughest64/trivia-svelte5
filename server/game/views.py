import json

from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser

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

    def post(self, request):
        print(request.data)
        serializer = TeamSerializer(data=request.data)
        # TODO: we shouldn't have any invalid data here, but handle it in case
        # what we are really after is to set an active team for the user in the db
        # so maybe it will be a UserSerializer instance?
        serializer.is_valid()
        print(serializer.data)

        return Response({"msg": "ok"})


class EventSetupView(APIView):
    authentication_classes = [SessionAuthentication, JwtAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        """ get this weeks games and a list of locations """
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
        # validate the data
        # get or create
        # serialize
        return Response()


class EventView(APIView):
    authentication_classes = [SessionAuthentication, JwtAuthentication]

    def get(self, request, joincode=None):
        """fetch a specific event from the joincode parsed from the url"""
        # use the join code to look up event data
        # raise if it's a bad join code

        return Response()