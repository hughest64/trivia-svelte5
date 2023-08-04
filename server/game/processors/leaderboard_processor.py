import logging

from django.db import transaction

from game.models import (
    EventRoundState,
    Leaderboard,
    LeaderboardEntry,
    TriviaEvent,
    QuestionResponse,
    LEADERBOARD_TYPE_HOST,
    LEADERBOARD_TYPE_PUBLIC,
    queryset_to_json,
)

logger = logging.getLogger(__name__)


class ProcedureError(Exception):
    def __init__(self, message=None) -> None:
        self.message = message or "This method should not be called independently"

    def __str__(self):
        return self.message


class LeaderboardProcessor:
    def __init__(self, event: TriviaEvent = None):
        self.event = event
        self.processing = False

    def _check_order(self):
        """ensure that the update process is only run from update_host_leaderboard."""
        if self.processing == False:
            raise ProcedureError("This method cannot be called independently")

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

        if lbe.megaround_applied and lbe.selected_megaround is not None:
            points = 0
            for resp in resps:
                if resp.game_question.round_number == lbe.selected_megaround:
                    points += resp.points_awarded * resp.megaround_value or 1
                else:
                    points += resp.points_awarded
        else:
            points = sum([resp.points_awarded for resp in resps])

        lbe.total_points = points + lbe.points_adjustment

    def _set_leaderboard_rank(self, leaderboard_entries):
        self._check_order()
        pts_vals = sorted(
            [lbe.total_points + lbe.points_adjustment for lbe in leaderboard_entries],
            reverse=True,
        )

        # track the points and rank of ties like - {pts: index}
        ties = {}
        seen = set()
        for i, pts in enumerate(pts_vals):
            if pts in seen and pts not in ties:
                ties[pts] = i
            seen.add(pts)

        for lbe in leaderboard_entries:
            # combine response points and points awarded
            pts_with_adj = lbe.total_points + lbe.points_adjustment

            # don't assign rank for 0 points
            if pts_with_adj <= 0:
                lbe.rank = None
                lbe.tied_for_rank = None
                lbe.tiebreaker_round_number = None
                lbe.tiebreaker_rank = None
                continue

            apply_tiebreaker_rank = (
                lbe.tiebreaker_rank is not None
                and lbe.tiebreaker_round_number is not None
                # this will auto reset tiebreakers when the next round is locked
                and self.event.max_locked_round() <= (lbe.tiebreaker_round_number or 0)
            )

            if apply_tiebreaker_rank:
                lbe.rank = lbe.tiebreaker_rank
                lbe.tied_for_rank = None

            else:
                lbe.rank = pts_vals.index(pts_with_adj) + 1
                lbe.tied_for_rank = ties.get(pts_with_adj)

            if not apply_tiebreaker_rank:
                lbe.tiebreaker_rank = None
                lbe.tiebreaker_round_number = None

    def rank_host_leaderboard(self, entries):
        """Apply new rankings to leaderboard entries"""
        self.processing = True

        # with transaction.atomic():
        self._set_leaderboard_rank(entries)
        LeaderboardEntry.objects.bulk_update(
            entries,
            fields=[
                "rank",
                "tied_for_rank",
                "tiebreaker_round_number",
                "tiebreaker_rank",
            ],
        )

        self.processing = False
        return queryset_to_json(entries.order_by("rank", "pk"))

    def update_host_leaderboard(self, through_round):
        self._validate_round_number(through_round)
        self.processing = True
        try:
            with transaction.atomic():
                apply_megaround = self.event.all_rounds_are_locked()
                lb, _ = Leaderboard.objects.update_or_create(
                    event=self.event,
                    defaults={
                        "host_through_round": through_round,
                        "synced": False,
                    },
                )
                entries = LeaderboardEntry.objects.filter(
                    event=self.event, leaderboard_type=LEADERBOARD_TYPE_HOST
                )
                for entry in entries:
                    entry.leaderboard = lb
                    entry.megaround_applied = apply_megaround
                    self._set_team_score(entry, through_round)

                self._set_leaderboard_rank(entries)
                LeaderboardEntry.objects.bulk_update(
                    entries,
                    [
                        "total_points",
                        "rank",
                        "tied_for_rank",
                        "tiebreaker_round_number",
                        "tiebreaker_rank",
                        "leaderboard",
                        "megaround_applied",
                    ],
                )

            logger.info(
                f"Host leaderboard for event {self.event} updated through round {through_round}"
            )

        except Exception as e:
            logger.exception(f"Could not update leaderboard. Reason: {e}")

        self.processing = False

        return {
            "host_leaderboard_entries": queryset_to_json(
                entries.order_by("rank", "pk")
            ),
            "synced": False,
        }

    def sync_leaderboards(self):
        """use host leaderboard and entry data to update the public leaderboard"""
        with transaction.atomic():
            host_lb_entries = LeaderboardEntry.objects.filter(
                event=self.event, leaderboard_type=LEADERBOARD_TYPE_HOST
            )

            event_lb, _ = Leaderboard.objects.get_or_create(event=self.event)
            event_lb.public_through_round = event_lb.host_through_round
            event_lb.synced = True
            event_lb.save()

            # mark rounds scored through the current round
            round_states = EventRoundState.objects.filter(
                event=self.event, round_number__lte=event_lb.host_through_round
            )
            round_states.update(scored=True)

            public_entries = []
            for e in host_lb_entries:
                lbe, _ = LeaderboardEntry.objects.update_or_create(
                    event=self.event,
                    leaderboard_type=LEADERBOARD_TYPE_PUBLIC,
                    team=e.team,
                    defaults={
                        "leaderboard": event_lb,
                        "rank": e.rank,
                        "tiebreaker_rank": e.tiebreaker_rank,
                        "total_points": e.total_points,
                        "megaround_applied": e.megaround_applied,
                    },
                )
                public_entries.append(lbe)

            return {
                "public_leaderboard_entries": queryset_to_json(public_entries),
                "through_round": event_lb.public_through_round,
                "synced": event_lb.synced,
                "round_states": queryset_to_json(round_states),
            }
