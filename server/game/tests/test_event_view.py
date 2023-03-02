from django.test import TestCase

from rest_framework.test import APIClient

from game.models import *
from user.models import User


class EventViewTestCase(TestCase):
    fixtures = ["initial.json"]

    def setUp(self):
        self.client = APIClient()
        self.player = User.objects.get(username="player")
        self.client.force_authenticate(user=self.player)
        self.event = TriviaEvent.objects.get(joincode=1234)

    # GET requests

    def test_bad_join_code(self):
        resp = self.client.get("/game/8888")
        self.assertEqual(resp.status_code, 404)

    def test_get_without_joining_event(self):
        resp = self.client.get("/game/1234")
        # not_joined
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.get("player_joined"), False)

    def test_get_over_player_limit(self):
        LeaderboardEntry.objects.create(
            event=self.event,
            team=self.player.active_team,
            leaderboard_type=LEADERBOARD_TYPE_PUBLIC,
        )
        self.event.player_limit = 1
        self.event.save()
        p2 = User.objects.get(username="player_two")

        # both players are on the same team
        self.assertEqual(self.player.active_team, p2.active_team)
        # add p2 and team to the event
        self.event.players.add(p2)
        self.event.event_teams.add(p2.active_team)

        # should be over the limit
        response = self.client.get("/game/1234")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data.get("reason"), "player_limit_exceeded")

        # inceasing the limit should succeed
        self.event.player_limit = 2
        self.event.save()
        self.event.players.add(self.player)
        response = self.client.get("/game/1234")
        self.assertEqual(response.status_code, 200)

    def test_no_active_team(self):
        self.player.active_team = None
        self.player.save()
        resp = self.client.get("/game/1234")
        self.assertEqual(resp.status_code, 403)

    # POST requests

    def test_post_bad_code(self):
        # cannot post a string as the join code
        response = self.client.post("/game/join", data={"joincode": "monkey"})
        self.assertEqual(response.status_code, 400)
        # non-existent event
        response = self.client.post("/game/join", data={"joincode": 7864})
        self.assertEqual(response.status_code, 404)

    def test_post_with_no_active_team(self):
        self.player.active_team = None
        self.player.save()
        response = self.client.post("/game/join", data={"joincode": 1234})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data.get("reason"), "team_required")

    def test_post_over_player_limit(self):
        self.event.player_limit = 1
        self.event.save()
        p2 = User.objects.get(username="player_two")

        # both players are on the same team
        self.assertEqual(self.player.active_team, p2.active_team)
        # add p2 and team to the event
        self.event.players.add(p2)
        self.event.event_teams.add(p2.active_team)

        response = self.client.post("/game/join", data={"joincode": 1234})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data.get("reason"), "player_limit_exceeded")

    def test_successful_post(self):
        self.assertFalse(self.player in self.event.players.all())
        response = self.client.post("/game/join", data={"joincode": 1234})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"player_joined": True})

        self.assertTrue(self.player in self.event.players.all())
        self.assertTrue(self.player.active_team in self.event.event_teams.all())
