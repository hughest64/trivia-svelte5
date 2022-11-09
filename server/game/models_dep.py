from django.db import models

# TODO: deprecate this file! (keep the to_json method on Team though)


class Team(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200, unique=True)
    # TODO: change model ref to get_user_model()?
    members = models.ManyToManyField( "user.User", related_name="teams" )

    def to_json(self):
        return {
            "name": self.name,
            "password": self.password,
            "members": [member.username for member in self.members.all()]
        }

    def __str__(self):
        return self.name


class Game:
    def __init__(self, game_id, game_title):
        self.game_id = game_id
        self.game_title = game_title


class Location:
    def __init__(self, location_id, location_name):
        self.location_id = location_id
        self.location_name = location_name


class Response:
    def __init__(self, recorded_answer, round_number, question_number ):
        self.recorded_answer = recorded_answer
        self.round_number = round_number
        self.question_number = question_number
        self.previous_answers = list

"""
class Response(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    round = models.ForeignKey(Round, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    previous_answers = models.JSONField(default=list, blank=True)
    recorded_answer = models.TextField(default="", blank=True)
    # set by host only
    is_funny = models.BooleanField(default=False)
    points_awarded = models.FloatField(default=0)
    megaround_value = models.FloatField(default=1)
    leaderboard_entry = models.ForeignKey(
        "LeaderboardEntry",
        on_delete=models.CASCADE,
        related_name="responses",
        # TODO: phase 1b should these be removed after exisitng data is updated?
        # (I.E. require a leaderboard for a response?)
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "responses"
        constraints = [
            models.constraints.UniqueConstraint(
                fields=["leaderboard_entry", "team", "question"],
                name="unique responses for a leaderbaord entry",
            )
        ]

    def __str__(self):
        return (
            f"Round {self.round.round_number}, Question {self.question.question_number}"
        )

    @property
    def response_key(self):
        try:
            return f"{self.round.round_number}{self.question.question_number}"
        except:
            return 0

    def serialize(self):

        model_dict = {
            "leaderboard_entry_id": self.leaderboard_entry_id,
            "recorded_answer": self.recorded_answer,
            "round_id": self.round.id,
            "round_number": self.round.round_number,
            "question_id": self.question.id,
            "question_number": self.question.question_number,
            "display_answer": self.question.display_answer,
            "text": self.question.question_text,
            "event_id": self.event.id if self.event else None,
            "team_id": self.team.id,
            "is_funny": self.is_funny,
            "points_awarded": self.points_awarded,
            "id": self.id,
            "megaround_value": self.megaround_value,
        }

        return model_dict

    def get_team_data(self):
        return {
            "leaderboard_entry_id": self.leaderboard_entry_id,
            "previous_answers": self.previous_answers,
            "recorded_answer": self.recorded_answer,
            "event_id": self.event.id if self.event else None,
            "team_id": self.team.id,
            "round_id": self.round.id,
            "question_id": self.question.id,
            "question_number": self.question.question_number,
            "round_number": self.round.round_number,
            "megaround_value": self.megaround_value,
            "is_funny": self.is_funny,
            "points_awarded": self.points_awarded,
        }

    def save(self, *args, **kwargs):
        self.full_clean()

        super().save(*args, **kwargs)
"""
