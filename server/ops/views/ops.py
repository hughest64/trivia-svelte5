import re

from django.conf import settings
from django.core import management
from django.utils import timezone

from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from game.db import HostActions, ValidateData, TestFailed
from game.models import Game, TriviaEvent, Team, get_end_of_week
from game.processors.game_creator import SOUND_SLUG, NO_SOUND_SLUG
from game.views.validation.data_cleaner import get_event_or_404

from user.authentication import JwtAuthentication
from user.models import User


class OpsAuthentication(JwtAuthentication):
    """
    Auth class used for testing only which inherits from JwtAuthentication.
    Parses the jwt from an auth header and is only valid when DEBUG=True
    """

    def authenticate(self, request):
        # only allow this method of auth for develeopment and testing
        if not settings.DEBUG:
            raise AuthenticationFailed("not allowed")

        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if auth_header is None:
            raise AuthenticationFailed("not authorized")

        self.token = auth_header.rsplit()[-1]
        return super().authenticate(request)


class HostControlsView(APIView):
    authentication_classes = [OpsAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request, joincode=None):
        post_type = request.data.pop("type", None)
        try:
            return HostActions.get(post_type)(request, joincode)
        except KeyError:
            raise NotFound(f"type {post_type} does not exist")


class GameSetupView(APIView):
    """Update test block games to this week"""

    authentication_classes = [OpsAuthentication]

    @staticmethod
    def update_through_date(block_code: str, fallback: Game):
        """update the active through date on existing games or create new ones from fallback"""
        for _type in [SOUND_SLUG, NO_SOUND_SLUG]:
            game = Game.objects.filter(
                block_code=block_code, title__iendswith=_type
            ).last()
            created = False
            if game is None:
                game = Game(**fallback)
                game.block_code = block_code
                game.title = f"Test Game {block_code}{_type}"
                game.use_sound = _type == SOUND_SLUG
                created = True

            game.active_through = get_end_of_week()
            game.save()

            if created:
                game.game_rounds.set(fallback.game_rounds.all())
                game.game_questions.set(fallback.game_questions.all())

    def post(self, request):
        fallback = Game.objects.latest("id")
        if fallback is None:
            raise NotFound("no games for testing")

        self.update_through_date("A", fallback)
        self.update_through_date("B", fallback)

        return Response({"success": True})


class DeleteView(APIView):
    authentication_classes = [OpsAuthentication]

    def post(self, request):
        delete_type = request.data.get("type")
        if delete_type is None:
            raise TestFailed("please provide a delete type")

        if delete_type == "game":
            joincodes = request.data.get("joincodes")
            if joincodes is None:
                raise NotFound("no joincodes found in post data")

            TriviaEvent.objects.filter(joincode__in=joincodes).delete()

        elif delete_type == "team":
            team_names = request.data.get("team_names")
            if team_names is None:
                raise NotFound("no team names were provided")

            Team.objects.filter(name__in=team_names).delete()

        elif delete_type == "user":
            usernames = request.data.get("usernames")

            if usernames is None:
                raise NotFound("no users were provided")
            users = User.objects.filter(username__in=usernames)
            users.delete()

        return Response({"success": True})


class RunGameView(APIView):
    """A view class for using the run_game management command"""

    authentication_classes = [OpsAuthentication]

    def post(self, request):
        config_file = request.data.get("config_name")
        game_data = request.data.get("game_data")

        if config_file is None and game_data is None:
            return Response(
                {"detail": "config_name or game_data is required"},
                status=HTTP_400_BAD_REQUEST,
            )

        msg = management.call_command("run_game", config=config_file, data=game_data)

        return Response({"sucesss": True})


class ValidateDataView(APIView):
    authentication_classes = [OpsAuthentication]

    def post(self, request):
        # TODO: data cleaner
        joincode = request.data.get("joincode")
        event = get_event_or_404(joincode)

        validation_type = request.data.get("type")

        try:
            return ValidateData.get(validation_type)(request, event)
        except KeyError:
            raise NotFound(f"validation_type {validation_type} does not exist")
