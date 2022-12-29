from django.db import models

from fuzzywuzzy import fuzz

from game.models.utils import queryset_to_json

FUZZ_MATCH_RATIO = 85

LEADERBOARD_TYPE_HOST = 0
LEADERBOARD_TYPE_PLAYER = 1
LEADERBOARD_TYPE_OPTIONS = [
    (LEADERBOARD_TYPE_HOST, "Host"),
    (LEADERBOARD_TYPE_PLAYER, "Public"),
]


class QuestionResponse(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    recorded_answer = models.TextField(default="")
    fuzz_ratio = models.IntegerField(default=0)
    points_awarded = models.FloatField(default=0)
    funny = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)
    game_question = models.ForeignKey("GameQuestion", on_delete=models.CASCADE)
    team = models.ForeignKey("Team", related_name="responses", on_delete=models.CASCADE)
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


class Leaderboard(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    leaderboard_type = models.IntegerField(choices=LEADERBOARD_TYPE_OPTIONS)
    event = models.ForeignKey("TriviaEvent", on_delete=models.CASCADE)
    # represents the max round for which player leaderboards should display point totals, rank, etc
    through_round = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.leaderboard_type} leaderboard for event {self.event}"

    # can be used to notify a host that either leaderboard type is not up to date with the max scored round
    def up_to_date(self):
        return (
            self.through_round is not None
            and self.through_round == self.event.max_scored_round()
        )

    def to_json(self):
        return {"leaderboard_entries": queryset_to_json(self.leaderboard_entries.all())}

    class Meta:
        unique_together = ("event", "leaderboard_type")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class LeaderboardEntry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    leaderboard = models.ForeignKey(
        Leaderboard, related_name="leaderboard_entries", on_delete=models.CASCADE
    )
    team = models.ForeignKey("Team", related_name="teams", on_delete=models.CASCADE)
    rank = models.IntegerField(blank=True, null=True)
    tiebreaker_rank = models.IntegerField(blank=True, null=True)
    total_points = models.FloatField(default=0)
    # Other fields:
    # selected_megaround
    # megaround_applied ?
    # points_adjustment
    # points_adjustment_reason
    # trivia_users # ? - this is supposed to rep whom actual played, not all team members

    class Meta:
        ordering = ["-leaderboard__event", "rank", "tiebreaker_rank", "pk"]

    def __str__(self):
        return f"Leaderboard Entry for {self.team} at event {self.event}"

    def to_json(self):
        # TODO:
        return {}


"""
host creates a tiebraker instance and response objects for each team. teams answer
the tiebreaker then the host resolves the tiebreaker. updating the leaderboard is a 
separate action
"""


# class TiebreakerInstance(models.Model):
#     event = models.ForeignKey(
#         "TriviaEvent", related_name="tiebreaker_instances", on_delete=models.CASCADE
#     )
#     round_number = models.IntegerField()
#     resolved = models.BooleanField(default=False)

#     def resolve_tiebreaker(self):
#         resps = self.tiebreaker_responses.all()
#         # set tiebreaker_rank on leaderboard entries based on closeness to the right answer
#         # (assuming all questions are numeric)
#         self.resolved = True
#         self.save()


# class TiebreakerResponse(models.Model):
#     tiebreaker_instance = models.ForeignKey(
#         TiebreakerInstance,
#         related_name="tiebreaker_responses",
#         on_delete=models.CASCADE,
#     )
#     # chosen from the tiebreaker_instance
#     question = models.ForeignKey("Question", on_delete=models.CASCADE)
#     leaderboard_entry = models.ForeignKey(LeaderboardEntry, on_delete=models.CASCADE)
#     recorded_answer = models.TextField(default="")
#     tiebreaker_rank = models.IntegerField(blank=True, null=True)
