from datetime import timedelta
import json
from typing import List

from django.db.models import QuerySet, Q
from django.utils import timezone

from django.conf import settings
from django.core import management
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from game.processors import TriviaEventCreator
from game.views.validation.data_cleaner import (
    DataCleaner,
    DataValidationError,
    get_event_or_404,
    get_game_or_404,
    get_location_or_404,
)
from user.authentication import OpsAuthentication

from game.models import (
    Game,
    GameQuestion,
    Location,
    EventRoundState,
    EventQuestionState,
    TriviaEvent,
    QuestionResponse,
    Leaderboard,
    LeaderboardEntry,
    LEADERBOARD_TYPE_PUBLIC,
    LEADERBOARD_TYPE_HOST,
)
from game.models.utils import queryset_to_json
from game.processors import LeaderboardProcessor
from game.utils.socket_classes import SendEventMessage, SendHostMessage

# TODO:
# - maybe convert to regular view functions as there will be a lot of stuffz here
# - extrapolate common processing and share w/ the actual view func


class HostControlsView(APIView):
    authentication_classes = [OpsAuthentication]

    def post(self, request):
        data = DataCleaner(request.data)
        round_number = data.as_int("round_number")
        locked = data.as_bool("locked")
        joincode = data.as_int("joincode")

        event = get_event_or_404(joincode)

        round_state, _ = EventRoundState.objects.update_or_create(
            event=event,
            round_number=round_number,
            defaults={"locked": locked},
        )
        # TODO: bind these so we can send the updated values back in the socket
        # lock or unlock responses for the round
        resps = QuestionResponse.objects.filter(
            event=event, game_question__round_number=round_number
        )
        resps.update(locked=locked)

        resp_summary = None
        if locked:
            resp_summary = QuestionResponse.summarize(event=event)
            # update the host leaderboard
            lb_processor = LeaderboardProcessor(event)
            leaderboard_data = lb_processor.update_host_leaderboard(
                through_round=event.max_locked_round() or round_state.round_number
            )

            # TODO: perhaps we don't need to send this as a separate host message
            # maybe we just ignore the piece of data if the broswer is on a /game route
            # send host message
            SendHostMessage(
                joincode,
                {
                    "msg_type": "leaderboard_update",
                    "message": leaderboard_data,
                },
            )

        SendEventMessage(
            joincode,
            {
                "msg_type": "round_update",
                "message": {
                    "round_state": round_state.to_json(),
                    "responses": queryset_to_json(resps),
                    "response_summary": resp_summary,
                },
            },
        )

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
