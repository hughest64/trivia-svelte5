import json

from django.conf import settings
# from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication

from user.authentication import JwtAuthentication
from .models import Team
from .serializers import TeamSerializer

# TODO: dev data only, replace once models are in place
with open(settings.BASE_DIR.parent / 'data' / 'teams.json', 'r') as f:
    team_data = json.load(f)
team_classes = [Team(**data) for data in team_data]


class TeamsView(APIView):
    authentication_classes = [SessionAuthentication, JwtAuthentication]

    def get(self, request):
        serializer = TeamSerializer(team_classes, many=True)

        return Response(serializer.data)