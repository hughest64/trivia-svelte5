from django.test import TestCase

from rest_framework.test import APIClient

from game.models import *
from user.models import User


class QuestionResponseViewTestCase(TestCase):
    fixtures = ["dbdump.json"]

    def setUp(self) -> None:
        self.client = APIClient()
        # force login
        # set up users
        return

    def test_submit_bad_payload(self):
        pass

    def test_submit_no_active_team(self):
        pass

    def test_submit_bad_joincde(self):
        pass

    def test_submit_not_joined_to_event(self):
        pass

    def test_submit_response_locked(self):
        pass

    def test_submit_bad_question_id(self):
        pass

    def test_grade_respose(self):
        pass
