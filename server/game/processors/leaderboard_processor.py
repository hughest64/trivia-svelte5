from django.db import transaction

from game.models import (
    Team,
    Leaderboard,
    LeaderboardEntry,
    TriviaEvent,
    QuestionResponse,
    LEADERBOARD_TYPE_HOST,
    LEADERBOARD_TYPE_PUBLIC,
)


class ProcedureError(Exception):
    def __init__(self, message) -> None:
        self.message = message or "This method should not be called indepentently"

    def __str__(self):
        return self.message


class LeaderboardProcessor:
    def __init__(self, event: TriviaEvent, leaderboard_type: int, through_round: int):
        self.event = event
        self.leaderboard_type = leaderboard_type
        # round to score through inclusive
        self.through_round = through_round
        self.processing = False

    def _check_order(self):
        """ensure that the update process is only run from update_leaderboard."""
        if self.processing == False:
            raise ProcedureError("This method cannot be called indepentently")

    def _set_team_score(self, lbe: LeaderboardEntry):
        self._check_order()
        resps = QuestionResponse.objects.filter(
            event=self.event,
            team=lbe.team,
            game_question__round_number__lte=self.through_round,
        )

        points = sum([resp.points_awarded for resp in resps])
        lbe.total_points = points

    # TODO: the tiebreaker bit needs work (do we reset it for example?)
    def _set_leaderboard_rank(self, leaderboard_entries):
        self._check_order()
        pts_vals = sorted(
            [lbe.total_points for lbe in leaderboard_entries],
            reverse=True,
        )
        tb_index = 0
        for lbe in leaderboard_entries:
            rank = pts_vals.index(lbe.total_points) + 1
            if lbe.tiebreaker_rank is not None:
                rank += tb_index
                tb_index += 1
            else:
                tb_index = 0
            lbe.rank = rank

    def handle_tiebreaker(self):
        return

    def update_leaderboard(self):
        if self.leaderboard_type == LEADERBOARD_TYPE_PUBLIC:
            raise ValueError("cannot call update_leaderboard on a public leaderboard")
        self.processing = True
        try:
            with transaction.atomic():
                leaderboard = Leaderboard.objects.get(
                    event=self.event, leaderboard_type=self.leaderboard_type
                )

                entries = leaderboard.leaderboard_entries.all()
                for entry in entries:
                    self._set_team_score(entry)

                self._set_leaderboard_rank(entries)
                LeaderboardEntry.objects.bulk_update(entries, ["total_points", "rank"])
                leaderboard.through_round = self.through_round
                leaderboard.save()
            # TODO: log?
            # better stats to be passed to the front end?
            return {"sucess": True}

        except Exception as e:
            self.processing = False
            # TODO: proper log
            print(f"Could not update leaderboard. Reason: {e}")

    def sync_leaderboards(self):
        # map a host leaderboard to a public leaderboard
        return
