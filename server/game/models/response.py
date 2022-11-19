from django.db import models
from django.forms.models import model_to_dict


class Response(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    recorded_answer = models.TextField(default="")
    game_question = models.ForeignKey("GameQuestion", on_delete=models.CASCADE)
    team = models.ForeignKey("Team", related_name="responses", on_delete=models.CASCADE)
    # TODO: this will need to change to leaderboard, or at least have leaderboard added, maybe?
    event = models.ForeignKey("TriviaEvent", related_name="responses", on_delete=models.CASCADE)

    def __str__(self):
        return f"Response for {self.team} on question {self.game_question.key} at {self.event}"

    def to_json(self):
        return {
            "id": self.pk,
            "round_number": self.game_question.round_number,
            "question_number": self.game_question.question_number,
            "key": self.game_question.key,
            "recorded_answer": self.recorded_answer
        }

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
