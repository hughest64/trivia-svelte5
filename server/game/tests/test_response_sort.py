import json
import timeit

from django.conf import settings
from django.test import TestCase

from rest_framework.test import APIClient

from game.models import *
from user.models import User

from .utils import QuestionResponseGenerator

from game.views.validation.data_cleaner import DataCleaner


class HostResponseGrading(TestCase):
    fixtures = ["dbdump.json"]

    def setUp(self) -> None:
        self.client = APIClient()
        self.client.force_authenticate(user=User.objects.get(username="sample_admin"))
        self.event = TriviaEvent.objects.get(joincode=1234)
        self.resp_generator = QuestionResponseGenerator(
            self.event,
            round_numbers=list(range(1, 9)),
            question_numbers=list(range(1, 11)),
        )
        self.resp_generator.parse_response_json(
            settings.BASE_DIR / "game/fixtures/twitch_resps.json"
        )
        self.resp_generator.generate()

    def tearDown(self) -> None:
        self.resp_generator.clean_up()

    def test_sort_round_reponses(self):
        """test fetching responses for single round."""
        resp = self.client.get("/host/1234/score/1")
        data = resp.data.get("response_data", [])
        self.assertTrue(all([r.get("round_number") == 1 for r in data]))

    def test_get_sorted_responses(self):
        """
        fetch, group, and sort all responses for an event with > 80 teams (~3600 reponses)
        and log how long it takes
        """
        timed = timeit.timeit(lambda: self.client.get("/host/1234/score"), number=1)
        # TODO: make this a log
        print(timed)

    def test_update_funny_values(self) -> None:
        responses_to_update = QuestionResponse.objects.filter(
            event__joincode=1234, funny=False, points_awarded=1
        )[:5]
        resp_ids = [resp.id for resp in responses_to_update]
        self.client.post(
            "/host/1234/score",
            data={
                "points_awarded": 1,
                "funny": "true",
                "response_ids": json.dumps(resp_ids),
            },
        )
        updated_reponses = QuestionResponse.objects.filter(id__in=resp_ids)
        self.assertTrue(all([r.funny for r in updated_reponses]))

    def test_update_points_values(self) -> None:
        responses_to_update = QuestionResponse.objects.filter(
            event__joincode=1234, funny=False, points_awarded=0
        )[:5]
        resp_ids = [resp.id for resp in responses_to_update]
        self.client.post(
            "/host/1234/score",
            data={
                "points_awarded": 0.5,
                "funny": "false",
                "response_ids": json.dumps(resp_ids),
            },
        )
        updated_reponses = QuestionResponse.objects.filter(id__in=resp_ids)
        self.assertTrue(
            all(
                [r.funny == False and r.points_awarded == 0.5 for r in updated_reponses]
            )
        )
