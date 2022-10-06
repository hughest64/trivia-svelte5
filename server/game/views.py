import json
import random

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from user.authentication import JwtAuthentication
from user.serializers import UserSerializer

from .models import Team, Location, Game
from .serializers import LocationSerializer, GameSerializer

# TODO: dev data only, replace once models are in place
with open(settings.BASE_DIR.parent / "data" / "event_setup_data.json", "r") as f2:
    event_select_data = json.load(f2)
location_classes = [Location(**data) for data in event_select_data.get("locations", [])]
game_classes = [Game(**data) for data in event_select_data.get("games", [])]

with open(
    settings.BASE_DIR.parent / "data" / "game_data_merged.json", "r"
) as event_file:
    event_data = json.load(event_file)

# TODO: classes
class TeamView(APIView):
    authentication_classes = [SessionAuthentication, JwtAuthentication]

    def get(self, request):
        serializer = UserSerializer(request.user)

        return Response({"user_data": serializer.data})

    @method_decorator(csrf_protect)
    def post(self, request):
        team_id = request.data.get("team_id")
        status = HTTP_200_OK
        if team_id:
            user = request.user
            requested_team = Team.objects.filter(id=team_id)
            if requested_team.exists():
                user.active_team_id = requested_team.first().id
                user.save()

            else:
                status = HTTP_404_NOT_FOUND

        return Response({"active_team_id": team_id}, status=status)


class EventSetupView(APIView):
    # authentication_classes = [SessionAuthentication, JwtAuthentication]
    # permission_classes = [IsAdminUser]

    def get(self, request):
        """get this weeks games and a list of locations"""
        user = request.user
        if user.is_authenticated and not user.is_staff:
            raise PermissionDenied(code=HTTP_401_UNAUTHORIZED)

        locationSerializer = LocationSerializer(location_classes, many=True)
        gameSerializer = GameSerializer(game_classes, many=True)
        userSerializer = UserSerializer(user)

        return Response(
            {
                "location_select_data": locationSerializer.data,
                "game_select_data": gameSerializer.data,
                "user_data": userSerializer.data
            }
        )

    @method_decorator(csrf_protect)
    def post(self, request):
        """create a new event or fetch an existing one with a specified game/location combo"""
        user = request.user
        if user.is_authenticated and not user.is_staff:
            raise PermissionDenied(code=HTTP_401_UNAUTHORIZED)
        # self.check_permissions(request)
        # validate the data
        # get or create
        event_data["join_code"] = random.randint(1000, 9999)
        # serialize
        userSerializer = UserSerializer(request.user)

        return Response({"event_data": event_data , "user_data": userSerializer.data})


class EventView(APIView):
    authentication_classes = [SessionAuthentication, JwtAuthentication]

    def get(self, request, joincode=None):
        """fetch a specific event from the joincode parsed from the url"""
        # use the join code to look up event data
        event_data["join_code"] = joincode
        # raise if it's a bad join code
        userSerializer = UserSerializer(request.user)

        return Response({"event_data": event_data, "user_data": userSerializer.data })


class EventJoinView(APIView):
    authentication_classes = [SessionAuthentication, JwtAuthentication]

    def get(self, request):
        """return user data to /game/join"""
        serializer = UserSerializer(request.user)

        return Response({"user_data": serializer.data})


class EventHostView(APIView):
    authentication_classes = [SessionAuthentication, JwtAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, joincode=None):
        """fetch a specific event from the joincode parsed from the url"""
        user = request.user
        if user.is_authenticated and not user.is_staff:
            raise PermissionDenied(code=HTTP_401_UNAUTHORIZED)

        # use the join code to look up event data
        event_data["join_code"] = joincode
        # raise if it's a bad join code
        userSerializer = UserSerializer(request.user)

        return Response({"event_data": event_data, "user_data": userSerializer.data })
