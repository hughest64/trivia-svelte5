from django.db import transaction

from game.models import (
    Leaderboard,
    LeaderboardEntry,
    TriviaEvent,
    QuestionResponse,
    LEADERBOARD_TYPE_HOST,
    LEADERBOARD_TYPE_PUBLIC,
)


class ProcedureError(Exception):
    def __init__(self, message=None) -> None:
        self.message = message or "This method should not be called indepentently"

    def __str__(self):
        return self.message


class LeaderboardProcessor:
    def __init__(self, event: TriviaEvent):
        self.event = event
        self.processing = False

    def _check_order(self):
        """ensure that the update process is only run from update_host_leaderboard."""
        if self.processing == False:
            raise ProcedureError("This method cannot be called indepentently")

    def _validate_round_number(self, through_round):
        if not self.event.game.game_rounds.filter(round_number=through_round).exists():
            raise ValueError(
                f"event {self.event} does not contain a round {through_round}"
            )

    def _set_team_score(self, lbe: LeaderboardEntry, through_round: int):
        self._check_order()
        resps = QuestionResponse.objects.filter(
            event=self.event,
            team=lbe.team,
            game_question__round_number__lte=through_round,
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

    def update_host_leaderboard(self, through_round):
        self._validate_round_number(through_round)
        self.processing = True
        try:
            with transaction.atomic():
                # an alternative here would be to loop event.teams and get_or_create on each team to ensure that every team has an entry
                entries = LeaderboardEntry.objects.filter(
                    event=self.event, leaderboard_type=LEADERBOARD_TYPE_HOST
                )
                for entry in entries:
                    self._set_team_score(entry, through_round)

                self._set_leaderboard_rank(entries)
                LeaderboardEntry.objects.bulk_update(entries, ["total_points", "rank"])
                Leaderboard.objects.update_or_create(
                    event=self.event, defaults={"host_through_round": through_round}
                )

            # TODO: log?
            return {"status": f"Host leaderboard updated through round {through_round}"}

        except Exception as e:
            # TODO: proper log
            print(f"Could not update leaderboard. Reason: {e}")

        self.processing = False

    def sync_leaderboards(self):
        """use host leaderboard and entry data to update the public leaderboard"""
        with transaction.atomic():
            host_lb_entries = LeaderboardEntry.objects.filter(
                event=self.event, leaderboard_type=LEADERBOARD_TYPE_HOST
            )

            event_lb, _ = Leaderboard.objects.get_or_create(event=self.event)
            event_lb.public_through_round = event_lb.host_through_round
            event_lb.save()

            for e in host_lb_entries:
                LeaderboardEntry.objects.update_or_create(
                    event=self.event,
                    leaderboard_type=LEADERBOARD_TYPE_PUBLIC,
                    team=e.team,
                    defaults={
                        "leaderboard": event_lb,
                        "rank": e.rank,
                        "tiebreaker_rank": e.tiebreaker_rank,
                        "total_points": e.total_points,
                    },
                )
