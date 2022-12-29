from django.test import TestCase

from game.models import *
from game.processors.leaderboard_processor import LeaderboardRank


class LeaderboardSetup(TestCase):
    fixtures = ["dbdump.json"]

    def setUp(self) -> None:
        self.event = TriviaEvent.objects.get(join_code=1234)
        self.team_a = Team.objects.get(name="The Best Team")
        self.team_b = Team.objects.get(name="Grambon Weekly")
        # host
        self.host_leaderboard = Leaderboard.objects.create(
            event=self.event, leaderboard_type=LEADERBOARD_TYPE_HOST
        )
        self.team_a_host_entry = LeaderboardEntry.objects.create(
            leaderboard=self.host_leaderboard, team=self.team_a
        )
        self.team_b_host_entry = LeaderboardEntry.objects.create(
            leaderboard=self.host_leaderboard, team=self.team_b
        )
        # public
        self.public_leaderboard = Leaderboard.objects.create(
            event=self.event, leaderboard_type=LEADERBOARD_TYPE_PUBLIC
        )
        self.team_a_public_entry = LeaderboardEntry.objects.create(
            leaderboard=self.public_leaderboard, team=self.team_a
        )
        self.team_b_public_entry = LeaderboardEntry.objects.create(
            leaderboard=self.public_leaderboard, team=self.team_b
        )
        # create responses for both teams (two each?)
        # lock a round (responses for same round)

    def tearDown(self) -> None:
        TriviaEvent.objects.all().delete()


class LeaderboardTestCase(LeaderboardSetup):
    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_something(self):
        # neither lbe entry should have a rank
        # run the lb class w/ the host lb
        # should have ranks
        # hit sync method (does not yet exist)
        # public version should have ranks
        return


class TiebreakerTestCase(LeaderboardSetup):
    def setUp(self) -> None:
        super().setUp()
        # manufacture a tie
        # create tiebraker stuff
        return

    def tearDown(self) -> None:
        super().tearDown()

    def test_tiebreaker_rank(self):
        # process leaderboard w/ tiebreakers
        return
