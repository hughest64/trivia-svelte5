from django.test import TestCase

from game.models import *
from game.processors import LeaderboardProcessor, ProcedureError


class LeaderboardSetup(TestCase):
    fixtures = ["data-1-19-23.json"]

    def setUp(self) -> None:
        self.host_lb = Leaderboard.objects.get(event__joincode=9998)

    def test_leaderboard_update(self):
        # get all etries for 9998 event
        # get qty
        # validate no entries have total_pts or rank

        # run the update
        # validate pts (summed correct for 1-2 teams?)
        # validate rank (max pts should have 1, min pts should have all().count())
        # valiidate highes pts has rank 1
        # validate ordering
        return

    def test_direct_update_public_leaderboard(self):
        # validate that it raises ProcdureError
        return

    # def test_leadboard_sync(self):

    # this is probably worthy of a separate class as there are many scenarios
    # def test_tiebreakers(self):
