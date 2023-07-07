import logging
import json
import timeit

from django.test import TestCase

from rest_framework.test import APIClient

from game.models import *
from user.models import User

logger = logging.getLogger(__name__)


class ResponseGradeTestCase(TestCase):
    fixtures = ["initial.json"]

    def setUp(self):
        self.event = TriviaEvent.objects.get(joincode=1234)
        self.team = Team.objects.get(name="hello world")

    def tearDown(self) -> None:
        QuestionResponse.objects.all().delete()

    def test_response_auto_grade(self):
        """responses auto grade when created/updated as long as they are not locked"""
        # create a correct response to q 1.1
        q1 = self.event.game.game_questions.all().get(round_number=1, question_number=1)
        resp = QuestionResponse.objects.create(
            recorded_answer="The Ramones",
            team=self.team,
            game_question=q1,
            event=self.event,
        )
        resp.grade()
        resp.save()

        # expect points to be 1.0
        self.assertEqual(resp.points_awarded, 1.0)
        self.assertEqual(resp.fuzz_ratio, 100)

        # update with incorrect answer
        resp.recorded_answer = "not even close"
        resp.grade()
        resp.save()
        self.assertEqual(resp.points_awarded, 0.0)
        self.assertTrue(resp.fuzz_ratio < FUZZ_MATCH_RATIO)

        # cannot grade a locked response
        resp.locked = True
        resp.recorded_answer = "The Ramones"
        resp.save()
        self.assertEqual(resp.points_awarded, 0.0)


class HostResponseGrading(TestCase):
    # fixtures = ["data-2-13-23.json"]
    fixtures = ["initial.json"]

    def setUp(self) -> None:
        self.client = APIClient()
        self.client.force_authenticate(user=User.objects.get(username="sample_admin"))

    def test_sort_round_reponses(self):
        """test fetching responses for single round."""
        resp = self.client.get("/host/9998/score/1")
        data = resp.data.get("response_data", [])
        self.assertTrue(all([r.get("round_number") == 1 for r in data]))

    def test_get_sorted_responses(self):
        """
        fetch, group, and sort all responses for an event with > 80 teams (~3600 reponses)
        and log how long it takes
        """
        timed = timeit.timeit(lambda: self.client.get("/host/9998/score"), number=1)
        logger.info(timed)

    def test_update_funny_values(self) -> None:
        responses_to_update = QuestionResponse.objects.filter(
            event__joincode=9998, funny=False, points_awarded=1
        )[:5]
        resp_ids = [resp.id for resp in responses_to_update]
        self.client.post(
            "/host/9998/score",
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
            event__joincode=9998, funny=False, points_awarded=0
        )[:5]
        resp_ids = [resp.id for resp in responses_to_update]
        self.client.post(
            "/host/9998/score",
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
