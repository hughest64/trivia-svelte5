import json

from django.test import TestCase

from rest_framework.test import APIClient

from game.models import *
from user.models import User


class TeamViewsTestCase(TestCase):
    fixtures = ["dbdump.json"]

    def setUp(self) -> None:
        self.client = APIClient()
        self.client.force_authenticate(user=User.objects.get(username="player"))

    def tearDown(self) -> None:
        Team.objects.all().delete()

    def test_create_user(self):
        # fails
        # post w/ a username that already exists
        # post w/ a username that is not acceptable (spaces for example)
        # post w/ mis-matched passwords

        # sucess
        # post w/ proper information
        # expect user data in response
        # expect a token in the cookies (?)
        return

    def test_login(self):
        # post to /user/login w/ p2 credentials
        # expect user data in the reponse
        # expect a token in the cookie header(?)

        # post w/ bad username
        # expect 400 response

        # post w/ bad password
        # expect 400 response
        return

    def test_create_team(self):
        post_data = {"name": "My Team"}
        response = self.client.post("/team/create", data=post_data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("user_data" in response.data)

        team = Team.objects.get(name="My Team")
        user = User.objects.get(username="player")
        # team should have an auto-generated password
        self.assertTrue(team.password is not None)
        # user should be a member of the team
        self.assertTrue(user in team.members.all())
        # user's active team should my "My Team"
        self.assertTrue(user.active_team == team)

    def test_join_team(self):
        # post a bad password
        bad_resp = self.client.post(
            "/team/join", data={"team_password": "this is a bad passwiord"}
        )
        self.assertEqual(bad_resp.status_code, 400)

        # post a good password
        # silent-pros-earnest - password for "for all The marbles"
        team = Team.objects.get(password="silent-pros-earnest")
        user = User.objects.get(username="player")
        self.assertFalse(user in team.members.all())

        good_resp = self.client.post(
            "/team/join", data={"team_password": "silent-pros-earnest"}
        )
        self.assertEqual(good_resp.status_code, 200)
        self.assertTrue("user_data" in good_resp.data)
        team = Team.objects.get(password="silent-pros-earnest")
        user = User.objects.get(username="player")
        self.assertTrue(user in team.members.all())
        self.assertEqual(user.active_team, team)

    def test_select_team(self):
        # post the id of a team a player doesn't belong to
        bad_resp = self.client.post("/team/select", data={"team_id": 8000})
        # should get a 400 response
        self.assertEqual(bad_resp.status_code, 400)
        # players active team should not be updated
        user = User.objects.get(username="player")
        # current active team is not the same as the requested team
        self.assertNotEqual(user.active_team.id, 5)
        # post the id if a team a player belongs to
        good_resp = self.client.post("/team/select", data={"team_id": 5})
        self.assertEqual(good_resp.status_code, 200)
        self.assertEqual(good_resp.data.get("active_team_id"), 5)
        user = User.objects.get(username="player")
        self.assertEqual(user.active_team.id, 5)
