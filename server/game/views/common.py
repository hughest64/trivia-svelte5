import json

from django.conf import settings
from django.core import management

from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from game.views.validation.data_cleaner import get_event_or_404, DataCleaner
from user.authentication import JwtAuthentication

from game.models import (
    EventRoundState,
    LeaderboardEntry,
    TriviaEvent,
    LEADERBOARD_TYPE_PUBLIC,
    LEADERBOARD_TYPE_HOST,
    queryset_to_json,
)


class LeaderboardView(APIView):
    authentication_classes = [JwtAuthentication]

    def get(self, request, joincode):
        event = get_event_or_404(joincode)

        public_lb_entries = LeaderboardEntry.objects.filter(
            event=event, leaderboard_type=LEADERBOARD_TYPE_PUBLIC
        )

        return Response(
            {
                "user_data": request.user.to_json(),
                "leaderboard_data": queryset_to_json(public_lb_entries),
            }
        )


class ClearEventDataView(APIView):
    """Endpoint used for resetting event data during tests"""

    def post(self, request):
        # TODO: this kinda get's buried in the test run (we only see the 400 response)
        if not settings.ALLOW_EVENT_RESET:
            return Response(
                {"detail": "that is not allowed"}, status=HTTP_400_BAD_REQUEST
            )

        secret = request.data.get("secret")
        joincodes = request.data.get("joincodes", [])
        if isinstance(joincodes, (str, int)):
            joincodes = [joincodes]

        # TODO: probably better to keep the secret in a .env file and read it into settings
        if secret != "todd is great":
            return Response(
                {"detail": "ah ah ah, you didn't say the magic word"},
                status=HTTP_400_BAD_REQUEST,
            )

        try:
            msg = management.call_command("reset", *joincodes)
            print(msg)
        except Exception as e:
            print(e)
            return Response({"detail": ""}, status=HTTP_400_BAD_REQUEST)

        return Response({"success": True})


class RunGameView(APIView):
    """A view class for using the run_game management command"""

    def post(self, request):
        secret = request.data.get("secret")
        if secret != "todd is great" or not settings.DEBUG:
            return Response(
                {"detail": "ah ah ah, you didn't say the magic word"},
                status=HTTP_400_BAD_REQUEST,
            )
        # data = DataCleaner(request.data)
        # create_only = data.as_bool("create_only")
        # TODO: this all terrible, I think we need another option in run_game to handle create_only
        create_only = True
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
