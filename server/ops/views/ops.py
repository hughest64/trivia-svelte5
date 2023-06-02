from django.conf import settings
from django.core import management

from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from game.db import HostActions, ValidateData
from game.views.validation.data_cleaner import get_event_or_404

from user.authentication import JwtAuthentication


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
        print(msg)

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
