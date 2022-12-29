from django.test import TestCase

from game.models import *
from game.processors.leaderboard_processor import LeaderboardRank


class LeaderboardTestCase(TestCase):
    def setUp(self) -> None:
        # load fixtures
        # create leaderboards for event 1234
        # create entries for two teams on each lb
        # create responses for both teams (two each?)
        return

    def tearDown(self) -> None:
        # do some things
        return

    def test_something(self):
        # neither lbe entry should have a rank
        # run the lb class w/ the host lb
        # should have ranks
        # hit sync method (does not yet exist)
        # public version should have ranks
        return


class TiebreakerTestCase(TestCase):
    def setUp(self) -> None:
        # set up as above (parent class?)
        # manufacture a tie
        # create tiebraker stuff
        return

    def tearDown(self) -> None:
        # do some things
        return

    def test_tiebreaker_rank(self):
        # process leaderboard w/ tiebreakers
        return
