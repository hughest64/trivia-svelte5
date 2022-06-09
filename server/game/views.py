import json

from django.conf import settings
# from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication

from user.authentication import JwtAuthentication
from .models import Team, Location, Game
from .serializers import TeamSerializer, LocationSerializer, GameSerializer
from user.serializers import UserSerializer

# TODO: dev data only, replace once models are in place
with open(settings.BASE_DIR.parent / 'data' / 'teams.json', 'r') as f:
    team_data = json.load(f)
team_classes = [Team(**data) for data in team_data]

with open(settings.BASE_DIR.parent / 'data' / 'event_select_data.json', 'r') as f2:
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


class EventSetupView(APIView):
    authentication_classes = [SessionAuthentication, JwtAuthentication]
    # TODO: is staff permission class

    def get(self, request):
        locationSerializer = LocationSerializer(location_classes, many=True)
        gameSerializer = GameSerializer(game_classes, many=True)

        return Response(
            {
                "location_select_data": locationSerializer.data,
                "game_select_data": gameSerializer.data
            }
        )