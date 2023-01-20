from django.test import TestCase

from game.models import *
from game.processors import LeaderboardProcessor


class LeaderboardSetup(TestCase):
    fixtures = ["data-1-19-23.json"]

    def setUp(self) -> None:
        pass
