from django.test import TestCase

from rest_framework.test import APIClient

from game.models import *
from user.models import User


class EventViewTestCase(TestCase):
    fixtures = ["dbdump.json"]

    def setUp(self):
        self.client = APIClient()
        self.player = User.objects.get(username="player")
        self.client.force_authenticate(user=self.player)
        self.event = TriviaEvent.objects.get(joincode=1234)
        self.host_lb = Leaderboard.objects.create(
            event=self.event, leaderboard_type=LEADERBOARD_TYPE_HOST
        )
        self.public_lb = Leaderboard.objects.create(
            event=self.event, leaderboard_type=LEADERBOARD_TYPE_PUBLIC
        )

    def tearDown(self) -> None:
        Leaderboard.objects.all().delete()

    def test_bad_join_code(self):
        resp = self.client.get("/game/8888")
        self.assertEqual(resp.status_code, 404)

    def test_get_without_leaderboard_entry(self):
        resp = self.client.get("/game/1234")
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.data.get("reason"), "join_required")

    def test_get_over_player_limit(self):
        # make a leaderboard entry for self.user.active_team
        # set the player limit to 1 for self.event
        # add a teammate of player (player_two?) to the event
        # try get request, should be over the limit
        # reset the event and delete the lbe
        return

    # test successful get request

    def test_no_active_team(self):
        self.player.active_team = None
        self.player.save()
        resp = self.client.get("/game/1234")
        self.assertEqual(resp.status_code, 403)

    # test post bad join code (both non-existent and non-integer)
    def test_post_bad_code(self):
        # cannot post a string as the join code
        response = self.client.post("/game/join", data={"joincode": "monkey"})
        self.assertEqual(response.status_code, 400)

        response = self.client.post("/game/join", data={"joincode": 7864})
        self.assertEqual(response.status_code, 404)

    # test post no active team
    # test post over player limit
    # test successful post
