from game.models import (
    Team,
    Leaderboard,
    LeaderboardEntry,
    TriviaEvent,
    QuestionResponse,
    LEADERBOARD_TYPE_HOST,
    LEADERBOARD_TYPE_PLAYER,
)


def queryset_to_json(qs):
    """Convert a queryset to a list of dictionaires. The model must implement a to_json method."""
    if not qs.exists():
        return []

    if not hasattr(qs.first(), "to_json"):
        raise NotImplementedError(
            "This method requires that a to_json method be implemented on the model class"
        )

    return [instance.to_json() for instance in qs]


class LeaderboardRank:
    def __init__(self, leaderboard: Leaderboard, through_round: int):
        self.leaderbaord = leaderboard
        # round to score through inclusive, if None, all locked and scored rounds are considered
        self.through_round = through_round

    def _set_team_score(self, team: Team):
        if self.Team is None:
            raise ValueError("A team instance is required, add one to the init")
        if self.Event is None:
            raise ValueError("A TriviaEvent instance is required, add one to the init")

        lbe, _ = LeaderboardEntry.objects.get_or_create(
            team=self.team, event=self.event
        )

        rng = range(1, self.through_round + 1)
        resps = QuestionResponse.objects.filter(
            event=self.leaderboard.event, team=team, round_number__in=rng
        )

        points = sum(*[resp.points_awarded for resp in resps])
        lbe.points_through_round = points
        if not self.through_round:
            lbe.total_points = points
        lbe.save()

        return points

    def _set_leaderboard_ranks(self):
        leaderboard_entries = Leaderboard.objects.filter(total_points__gte=0).order_by(
            ["-points", "tiebreaker_rank"]
        )
        pts_vals = [lbe.points for lbe in leaderboard_entries]
        tb_index = 0
        for lbe in leaderboard_entries:
            rank = pts_vals.index(lbe.points)
            if lbe.tiebreaker_rank is not None:
                rank += tb_index
                tb_index += 1
            else:
                tb_index = 0
            lbe.rank = rank
            lbe.save()

    def update_leaderboard(self):
        # use with transaction.atomic() and:
        # - lookup all teams for the event (leaderboard.event.teams.all())
        # - pass each team to self.set_team_score()
        # call self.set_team_ranks()
        return

    def handle_tiebreaker(self):
        return

    def sync_leaderboards(self):
        # map a host leaderboard to a public leaderboard
        return
