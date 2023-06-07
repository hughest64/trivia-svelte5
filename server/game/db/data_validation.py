from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from game.models import (
    EventRoundState,
    LeaderboardEntry,
    LEADERBOARD_TYPE_HOST,
)


class TestFailed(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "The test failed"
    default_code = "test_failed"


class ValidateData:
    @classmethod
    def get(cls, key):
        method_dct = {
            "validate_megaround": cls.validate_megaround,
            "megaround_lock": cls.megaround_lock,
            "player_limit": cls.player_limit,
        }

        return method_dct[key]

    @classmethod
    def validate_megaround(cls, request, event):
        round = int(request.data.get("round", 0))
        team = request.data.get("team")

        try:
            lbe = LeaderboardEntry.objects.get(
                event=event,
                team__name=team,
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

    @classmethod
    def megaround_lock(cls, request, event):
        rd_count = event.game.game_rounds.exclude(round_number=0).count()
        for i in range(1, rd_count + 1):
            EventRoundState.objects.update_or_create(
                event=event, round_number=i, defaults={"locked": True}
            )
        return Response({"sucess": True})

    @classmethod
    def player_limit(cls, request, event):
        limit = request.data.get("limit")

        if limit != event.player_limit:
            raise TestFailed(f"limit {limit} != event limit {event.player_limit}")

        return Response({"sucess": True})
