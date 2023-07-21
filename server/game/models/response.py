from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from fuzzywuzzy import fuzz

from game.models.utils import queryset_to_json

FUZZ_MATCH_RATIO = 85

LEADERBOARD_TYPE_HOST = 0
LEADERBOARD_TYPE_PUBLIC = 1
LEADERBOARD_TYPE_OPTIONS = [
    (LEADERBOARD_TYPE_HOST, "Host"),
    (LEADERBOARD_TYPE_PUBLIC, "Public"),
]
LEADERBOARD_TYPE_DICT = dict(LEADERBOARD_TYPE_OPTIONS)

PTS_ADJUSTMENT_BLANK = 0
PTS_ADJUSTMENT_TEAM_LIMIT = 1
PTS_ADJUSTMENT_TEAM_NAME = 2
PTS_ADJUSTMENT_FUNNY_ANSWER = 3
PTS_ADJUSTMENT_TEAM_SPIRIT = 4
PTS_ADJUSTMENT_DISCRETIONARY = 5

PTS_ADJUSTMENT_OPTIONS = [
    (PTS_ADJUSTMENT_BLANK, "-----"),
    (PTS_ADJUSTMENT_TEAM_LIMIT, "Team Limit Exceeded"),
    (PTS_ADJUSTMENT_TEAM_NAME, "Best Team Name"),
    (PTS_ADJUSTMENT_FUNNY_ANSWER, "Funny Answer"),
    (PTS_ADJUSTMENT_TEAM_SPIRIT, "Team Spirit"),
    (PTS_ADJUSTMENT_DISCRETIONARY, "Host Discretion"),
]

PTS_ADJUSTMENT_OPTIONS_LIST = [{"id": k, "text": v} for k, v in PTS_ADJUSTMENT_OPTIONS]


class QuestionResponse(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    recorded_answer = models.TextField(default="", blank=True)
    fuzz_ratio = models.IntegerField(default=0)
    points_awarded = models.FloatField(default=0)
    # TODO: we should use min/max validators here, i.e 1-5 AND they should be unique
    megaround_value = models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
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
            "megaround_value": self.megaround_value,
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

    # TODO: add a key=None kwarg, use it to filter specific keys and selectively update on the frontend
    @staticmethod
    def summarize(event):
        all_resps = QuestionResponse.objects.filter(event=event)
        summarized = {}
        for resp in all_resps:
            key = resp.game_question.key
            summarized.setdefault(key, {"correct": 0, "half": 0, "total": 0})
            values = summarized[key]
            if resp.points_awarded == 1:
                values["correct"] += 1
            elif resp.points_awarded == 0.5:
                values["half"] += 1

            values["total"] += 1

        return summarized

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


# for now, this only contains references to the round through which leaderboard entries
# of a given type are scored, but it could also contain aggregated data about an event
class Leaderboard(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.OneToOneField(
        "TriviaEvent", related_name="leaderboards", on_delete=models.CASCADE
    )
    public_through_round = models.IntegerField(blank=True, null=True)
    host_through_round = models.IntegerField(blank=True, null=True)
    # do the two sets of entires match? note that this is not toally dependent upon through rounds matching
    synced = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.event} @ {self.event.location}"


class LeaderboardEntry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    leaderboard_type = models.IntegerField(choices=LEADERBOARD_TYPE_OPTIONS)
    event = models.ForeignKey(
        "TriviaEvent",
        related_name="leaderboard_entries",
        related_query_name="leaderboard_entry",
        on_delete=models.CASCADE,
    )
    leaderboard = models.ForeignKey(
        Leaderboard,
        related_name="entries",
        related_query_name="leaderboard_entry",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    team = models.ForeignKey("Team", related_name="teams", on_delete=models.CASCADE)
    rank = models.IntegerField(blank=True, null=True)
    tiebreaker_rank = models.IntegerField(blank=True, null=True)
    total_points = models.FloatField(default=0)
    selected_megaround = models.IntegerField(blank=True, null=True)
    megaround_applied = models.BooleanField(default=False)
    points_adjustment = models.FloatField(default=0)
    points_adjustment_reason = models.IntegerField(
        default=0,
        choices=PTS_ADJUSTMENT_OPTIONS,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )

    class Meta:
        unique_together = ("team", "event", "leaderboard_type")
        ordering = [
            "-event",
            "rank",
            "tiebreaker_rank",
            "pk",
            "-leaderboard_type",
        ]
        verbose_name_plural = "Leaderboard Entries"

    def _get_through_rounds(self):
        round_data = {"public": None, "host": None}
        if self.leaderboard:
            round_data = {
                "public": self.leaderboard.public_through_round,
                "host": self.leaderboard.host_through_round,
            }

        return round_data

    def get_through_round(self, type):
        if type not in ["public", "host"]:
            raise ValueError("The type argument must be one of 'public' or 'host'")
        through_rounds = self._get_through_rounds()

        return through_rounds[type]

    def __str__(self):
        return f"{LEADERBOARD_TYPE_DICT[self.leaderboard_type]} @ {self.event} - {self.team}"

    def to_json(self):
        return {
            "team_id": self.team.id,
            "team_name": self.team.name,
            "team_password": self.team.password,
            "rank": self.rank or "-",
            "total_points": self.total_points,
            "megaround": self.selected_megaround,
            "points_adjustment_value": self.points_adjustment,
            "points_adjustment_reason_id": self.points_adjustment_reason,
        }


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
