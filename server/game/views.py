import json
import random

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from user.authentication import JwtAuthentication
from user.serializers import UserSerializer

from game.models import Location, Team, TriviaEvent, Game, queryset_to_json

# TODO: fix all the broken things
event_data = {}


class TeamView(APIView):
    authentication_classes = [JwtAuthentication]

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
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        """get this weeks games and a list of locations"""
        user = request.user
        locations = queryset_to_json(Location.objects.filter(active=True))
        # TODO: a filter of some sort to limit avialable games (should there be an active pram on the model?)
        games = queryset_to_json(Game.objects.all())
        user_serializer = UserSerializer(user)

        return Response(
            {
                "location_select_data": locations,
                "game_select_data": games,
                "user_data": user_serializer.data,
            }
        )

    @method_decorator(csrf_protect)
    def post(self, request):
        """create a new event or fetch an existing one with a specified game/location combo"""
        user = request.user
        # validate the data
        # get or create
        event_data["join_code"] = random.randint(1000, 9999)
        # serialize
        user_serializer = UserSerializer(user)

        # TODO: this could just return the join code since the data won't be loaded from this response
        return Response({"event_data": event_data, "user_data": user_serializer.data})


class EventView(APIView):
    authentication_classes = [JwtAuthentication]

    def get(self, request, joincode=None):
        """fetch a specific event from the joincode parsed from the url"""
        user_serializer = UserSerializer(request.user)
        
        try:
            event = TriviaEvent.objects.get(join_code=1234)
        except TriviaEvent.DoesNotExist:
            return Response({"detail": "an event with that join code does not exist"}, status=HTTP_404_NOT_FOUND)

        # event_data, game_questions, game_rounds, question_states, round_states
        data = event.to_json()
        # TODO: temporary!
        data["event_data"]["join_code"] = joincode

        # TODO: get responses for this event via the user's active team
        # if they do not have an active team respond with a 400 and a message
        # kit will need to handle the response accordingly

        return Response({**data, "user_data": user_serializer.data, "response_data": []})


class EventJoinView(APIView):
    authentication_classes = [JwtAuthentication]

    def get(self, request):
        """return user data to /game/join"""
        serializer = UserSerializer(request.user)

        return Response({"user_data": serializer.data})


# TODO: do we need this? The data isn't any different from the player view
class EventHostView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, joincode=None):
        """fetch a specific event from the joincode parsed from the url"""
        user_serializer = UserSerializer(request.user)
        
        try:
            event = TriviaEvent.objects.get(join_code=1234)
        except TriviaEvent.DoesNotExist:
            return Response({"detail": "an event with that join code does not exist"}, status=HTTP_404_NOT_FOUND)

        # event_data, game_questions, game_rounds, question_states, round_states
        data = event.to_json()
        # TODO: temporary!
        data["event_data"]["join_code"] = joincode

        return Response({**data, "user_data": user_serializer.data})
