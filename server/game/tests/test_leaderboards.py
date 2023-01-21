from django.test import TestCase

from game.models import *
from game.processors import LeaderboardProcessor

# TODO: this should test the update functionality in stages
# i.e. through rd 4 then through rd 8


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
        LeaderboardProcessor(event=self.event).update_host_leaderboard(through_round=8)
        entries = LeaderboardEntry.objects.filter(leaderboard=self.host_lb)

        # point totals are summed correctly
        team_a = entries[0].team
        team_a_resps = QuestionResponse.objects.filter(event=self.event, team=team_a)
        team_a_pt_total = sum([r.points_awarded for r in team_a_resps])
        self.assertEqual(team_a_pt_total, entries[0].total_points)

        team_b = entries[1].team
        team_b_resps = QuestionResponse.objects.filter(event=self.event, team=team_b)
        team_b_pt_total = sum([r.points_awarded for r in team_b_resps])
        self.assertEqual(team_b_pt_total, entries[1].total_points)

        # entries are sorted are ranked properly
        self.assertEqual(entries.filter(rank__isnull=False).count(), entry_count)
        self.assertEqual(entries.first().rank, 1)
        self.assertEqual(entries.last().rank, entry_count)
        # assert a <= b <= n... for all entries
        for i, e in enumerate(entries):
            if i == 0:
                self.assertTrue(e.rank == 1)
                continue
            self.assertTrue(e.rank >= entries[i - 1].rank)

    def test_though_round_out_of_range(self):
        with self.assertRaises(ValueError):
            LeaderboardProcessor(self.event).update_host_leaderboard(through_round=9)

    def test_leadboard_sync(self):
        LeaderboardProcessor(self.event).sync_leaderboards()
        host_entries = self.host_lb.leaderboard_entries.all()
        public_lb = Leaderboard.objects.get(
            event=self.event, leaderboard_type=LEADERBOARD_TYPE_PUBLIC
        )

        self.assertEqual(self.host_lb.through_round, public_lb.through_round)

        for e in host_entries:
            public_entry = LeaderboardEntry.objects.get(
                leaderboard=public_lb, team=e.team
            )
            self.assertEqual(e.total_points, public_entry.total_points)
            self.assertEqual(e.tiebreaker_rank, public_entry.tiebreaker_rank)

    # this is probably worthy of a separate class as there are many scenarios
    # def test_tiebreakers(self):
