from django.test import TestCase

from game.models import *
from game.processors import LeaderboardProcessor, ProcedureError


class LeaderboardSetup(TestCase):
    fixtures = ["data-1-19-23.json"]

    def setUp(self) -> None:
        self.event = TriviaEvent.objects.get(joincode=9998)
        self.host_lb = Leaderboard.objects.get(
            event=self.event, leaderboard_type=LEADERBOARD_TYPE_HOST
        )

    def test_leaderboard_update(self):
        entries = LeaderboardEntry.objects.filter(leaderboard=self.host_lb)
        entry_count = len(entries)

        # rank should not be set and total points should be 0 for all entries
        self.assertEqual(entries.filter(total_points=0).count(), entry_count)
        self.assertEqual(entries.filter(rank__isnull=True).count(), entry_count)

        # run the update
        LeaderboardProcessor(
            event=self.event, leaderboard_type=LEADERBOARD_TYPE_HOST, through_round=8
        ).update_leaderboard()
        entries = LeaderboardEntry.objects.filter(leaderboard=self.host_lb)
        # validate pts (summed correct for 1-2 teams?)

        # entries are sorted are ranked properly
        self.assertEqual(entries.filter(rank__isnull=False).count(), entry_count)
        self.assertEqual(entries.first().rank, 1)
        self.assertEqual(entries.last().rank, entry_count)
        # need to assert a <= b <= n... for all entries

    def test_direct_update_public_leaderboard(self):
        with self.assertRaises(ProcedureError):
            LeaderboardProcessor(
                self.event, LEADERBOARD_TYPE_PUBLIC, through_round=8
            ).update_leaderboard()

    # def test_leadboard_sync(self):

    # this is probably worthy of a separate class as there are many scenarios
    # def test_tiebreakers(self):
