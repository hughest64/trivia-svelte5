import json

from django.conf import settings
from django.core import management

from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from game.views.validation.data_cleaner import (
    DataCleaner,
    get_event_or_404,
)
from user.authentication import JwtAuthentication

from game.models import (
    EventRoundState,
    TriviaEvent,
    LeaderboardEntry,
    LEADERBOARD_TYPE_HOST,
)

from game.db import HostActions


class OpsAuthentication(JwtAuthentication):
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
            raise NotFound


class RunGameView(APIView):
    """A view class for using the run_game management command"""

    authentication_classes = [OpsAuthentication]

    def post(self, request):
        # data = DataCleaner(request.data)
        # create_only = data.as_bool("create_only")
        # TODO: this all terrible, I think we need another option in run_game to handle create_only
        data = DataCleaner(request.data)
        create_only = data.as_bool("create_only")
        config_file = request.data.get("config_name")
        game_data = request.data.get("game_data")
        if create_only:
            game_data = json.loads(game_data)
            _, created = TriviaEvent.objects.get_or_create(
                joincode=game_data["joincode"],
                defaults={"game_id": game_data["game_id"]},
            )
            created_msg = "was created" if created else "already exists"
            print(f"event with joincode {game_data['joincode']} {created_msg}")

        else:
            # for now we only care about the config, but other features should be added;
            if config_file is not None:
                msg = management.call_command("run_game", config=config_file)
            elif game_data is not None:
                print(game_data)
                msg = management.call_command("run_game", data=game_data)
            else:
                return Response(
                    {"detail": "config_name or game_data is required"},
                    status=HTTP_400_BAD_REQUEST,
                )
            print(msg)
        # look up data as needed to return - or should the mgmt cmd do this?
        return Response({"sucesss": True})


class ValidateDataView(APIView):
    authentication_classes = [OpsAuthentication]

    def post(self, request):
        # TODO: data cleaner
        secret = request.data.get("secret")
        if secret != "todd is great" or not settings.DEBUG:
            return Response(
                {"detail": "ah ah ah, you didn't say the magic word"},
                status=HTTP_400_BAD_REQUEST,
            )
        joincode = request.data.get("joincode")
        event = get_event_or_404(joincode)
        validation_type = request.data.get("type")

        if validation_type == "megaround":
            return self.validate_megaround(request, event)

        if validation_type == "megaround_lock":
            return self.megaround_lock(event)

        return Response(
            {"detail": f"unrecognized validation type - {validation_type}"},
            status=HTTP_400_BAD_REQUEST,
        )

    def validate_megaround(self, request, event):
        round = int(request.data.get("round", 0))
        team = request.data.get("team")

        try:
            lbe = LeaderboardEntry.objects.get(
                event=event,
                team__name=f"run_game_team_{team}",
                leaderboard_type=LEADERBOARD_TYPE_HOST,
            )
        except LeaderboardEntry.DoesNotExist:
            return Response(
                {"detail": f"no leaderboard entry for team {team}"},
                status=HTTP_400_BAD_REQUEST,
            )
        else:
            if lbe.selected_megaround != round:
                return Response(
                    {
                        "detail": f"selected megaround {lbe.selected_megaround} does not equal {round}"
                    },
                    status=HTTP_400_BAD_REQUEST,
                )

        return Response({"success": True})

    def megaround_lock(self, event: TriviaEvent):
        rd_count = event.game.game_rounds.exclude(round_number=0).count()
        for i in range(1, rd_count + 1):
            EventRoundState.objects.update_or_create(
                event=event, round_number=i, defaults={"locked": True}
            )
        return Response({"sucess": True})
