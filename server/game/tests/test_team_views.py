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
        post_data = {"team_name": "My Team"}
        response = self.client.post("/team/create", data=post_data)
        # expect a 200 response
        # team My Team should exist
        # team should have an auto-generated password
        # user should be a member of the team
        # user's active team should my "My Team"
