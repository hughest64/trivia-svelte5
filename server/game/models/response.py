from django.db import models

from fuzzywuzzy import fuzz

FUZZ_MATCH_RATIO = 85


class QuestionResponse(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    recorded_answer = models.TextField(default="")
    fuzz_ratio = models.IntegerField(default=0)
    points_awarded = models.FloatField(default=0)
    funny = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)
    game_question = models.ForeignKey("GameQuestion", on_delete=models.CASCADE)
    team = models.ForeignKey("Team", related_name="responses", on_delete=models.CASCADE)
    # TODO: add leaderboard
    event = models.ForeignKey(
        "TriviaEvent", related_name="responses", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Response for {self.team} on question {self.game_question.key} at {self.event}"

    def to_json(self):
        return {
            "id": self.pk,
            "points_awarded": self.points_awarded,
            "funny": self.funny,
            "locked": self.locked,
            "round_number": self.game_question.round_number,
            "question_number": self.game_question.question_number,
            "key": self.game_question.key,
            "recorded_answer": self.recorded_answer,
        }

    def grade(self):
        """run fuzzy fuzzy using the recorded answer against all accepted answers for the question"""
        if self.locked:
            return
        question = self.game_question.question
        answers = {a.text for a in question.accepted_answers.all()}
        answers.add(question.display_answer.text)
        for answer in answers:
            self.fuzz_ratio = fuzz.token_set_ratio(answer, self.recorded_answer)
            if self.fuzz_ratio >= FUZZ_MATCH_RATIO:
                self.points_awarded = 1
                break
            else:
                self.points_awarded = 0

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
