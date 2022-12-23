from django.test import TestCase

from game.models import *


class ResponseGradeTestCase(TestCase):
    fixtures = ["dbdump.json"]

    def setUp(self):
        self.event = TriviaEvent.objects.get(join_code=1234)
        self.team = Team.objects.get(name="hello world")

    def tearDown(self) -> None:
        QuestionResponse.objects.all().delete()

    def test_response_auto_grade(self):
        """test auto grader"""
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

    def test_new_qustion(self):
        """new questions should not auto set accepted answers but a response
        to a related game_questions should still score correctly
        """
        answer = QuestionAnswer.objects.last()
        question = Question.objects.create(
            question_text="what is the answer?", display_answer=answer
        )
        game_question = GameQuestion.objects.create(
            question=question, game=self.event.game, round_number=9, question_number=1
        )
        # expect no accepted_answers
        self.assertFalse(game_question.question.accepted_answers.all().exists())

        resp = QuestionResponse.objects.create(
            recorded_answer=answer,
            team=self.team,
            game_question=game_question,
            event=self.event,
        )
        resp.grade()
        resp.save()

        # expect points to be 1.0
        self.assertEqual(resp.points_awarded, 1.0)
        self.assertEqual(resp.fuzz_ratio, 100)
