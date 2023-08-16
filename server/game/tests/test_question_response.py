from django.test import TestCase

from rest_framework.test import APIClient

from game.models import *
from user.models import User


class QuestionResponseViewTestCase(TestCase):
    fixtures = ["initial.json"]

    def setUp(self) -> None:
        self.client = APIClient()
        self.p1 = User.objects.get(username="player")
        self.p2 = User.objects.get(username="player_two")
        self.team = self.p1.active_team
        self.client.force_authenticate(user=self.p1)
        # self.client.force_authenticate(user=self.p2)

        self.event = TriviaEvent.objects.get(joincode=1234)
        self.first_question = self.event.game.game_questions.first()
        self.last_question = self.event.game.game_questions.last()
        self.event.event_teams.add(self.team)
        self.event.players.set([self.p1, self.p2])

    def test_submit_bad_payload(self):
        payload = {
            "team_id": self.p1.active_team.id,
            # bad question id in the payload
            "question_id": "bob",
            "response_text": "I know the answer",
        }
        response = self.client.post("/game/1234/response", data=payload)
        self.assertEqual(response.status_code, 400)

    def test_submit_bad_joincde(self):
        payload = {
            "team_id": self.team.id,
            "question_id": self.first_question.id,
            "response_text": "I know the answer",
        }
        # post to a non-existent event
        response = self.client.post("/game/0000/response", data=payload)
        self.assertEqual(response.status_code, 404)

    def test_submit_no_active_team(self):
        self.p1.active_team = None
        self.p1.save()
        payload = {
            "team_id": self.team.id,
            "question_id": self.first_question.id,
            "response_text": "I know the answer",
        }
        response = self.client.post("/game/1234/response", data=payload)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data.get("reason"), "team_required")

    def test_submit_not_joined_to_event(self):
        self.p1.active_team = self.team
        self.p1.save()
        self.event.players.remove(self.p1)

        payload = {
            "team_id": self.team.id,
            "question_id": self.first_question.id,
            "response_text": "I know the answer",
        }
        response = self.client.post("/game/1234/response", data=payload)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data.get("reason"), "join_required")

    def test_submit_response_locked(self):
        QuestionResponse.objects.create(
            game_question=self.first_question,
            event=self.event,
            team=self.team,
            recorded_answer="hello tests",
            locked=True,
        )
        self.p1.active_team = self.team
        self.p1.save()
        self.event.event_teams.add(self.team)
        self.event.players.set([self.p1, self.p2])

        payload = {
            "team_id": self.team.id,
            "question_id": self.first_question.id,
            "response_text": "I know the answer",
        }
        response = self.client.post("/game/1234/response", data=payload)
        self.assertEqual(response.status_code, 400)

    def test_grade_response(self):
        # expect points awarded to be set correctly
        self.p1.active_team = self.team
        self.p1.save()
        self.event.event_teams.add(self.team)
        self.event.players.set([self.p1, self.p2])

        payload = {
            "team_id": self.team.id,
            "question_id": self.last_question.id,
            "response_text": self.last_question.question.display_answer.text,
        }
        response = self.client.post("/game/1234/response", data=payload)
        self.assertEqual(response.status_code, 200)
        # excpect 1 point to be awarded
        question_answer = QuestionResponse.objects.get(
            game_question=self.last_question, team=self.team
        )
        self.assertEqual(question_answer.points_awarded, 1)


# TODO: test megaround
