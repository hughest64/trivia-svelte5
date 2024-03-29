from datetime import timedelta
import random

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.forms.models import model_to_dict
from django.utils import timezone

from .utils import queryset_to_json

from game.views.validation.exceptions import JoincodeError

GAME_DAYS_TO_ROLL = settings.GAME_DAYS_TO_ROLL

QUESTION_TYPE_GENERAL_KNOWLEDGE = 0
QUESTION_TYPE_THEMED_ROUND = 1
QUESTION_TYPE_WORD_PLAY = 2
QUESTION_TYPE_IMAGE_ROUND = 3
QUESTION_TYPE_LIGHTNING_ROUND = 4
QUESTION_TYPE_SOUND_ROUND = 5
QUESTION_TYPE_TIE_BREAKER = 6

QUESTION_TYPES = [
    (QUESTION_TYPE_GENERAL_KNOWLEDGE, "General Knowledge"),
    (QUESTION_TYPE_THEMED_ROUND, "Themed Round"),
    (QUESTION_TYPE_WORD_PLAY, "Word Play"),
    (QUESTION_TYPE_IMAGE_ROUND, "Image Round"),
    (QUESTION_TYPE_LIGHTNING_ROUND, "Lightning Round"),
    (QUESTION_TYPE_SOUND_ROUND, "Sound Round"),
    (QUESTION_TYPE_TIE_BREAKER, "Tiebreaker"),
]

QUESTION_TYPE_DICT = dict(QUESTION_TYPES)

# higher numbers are currently reserved for testing, but this may change in the future
MAX_JOINCODE_VALUE = 9999
MAX_CREATE_JOINCODE_ATTEMPTS = 30


class Question(models.Model):
    """Question data. Not tied to a game or round number or question number."""

    created_at = models.DateTimeField(auto_now_add=True)
    question_type = models.IntegerField(choices=QUESTION_TYPES, default=0)
    question_text = models.TextField()
    question_url = models.CharField(max_length=255, blank=True, null=True)
    display_answer = models.ForeignKey(
        "QuestionAnswer", related_name="display_answer", on_delete=models.PROTECT
    )
    accepted_answers = models.ManyToManyField(
        "QuestionAnswer", related_name="accepted_answers", blank=True
    )
    answer_notes = models.CharField(max_length=255, blank=True, null=True)
    question_notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        qt = self.question_text
        return qt if len(qt) < 20 else qt[:20] + "..."

    def to_json(self):
        data = model_to_dict(self)
        data.update(
            {
                "display_answer": self.display_answer.text,
                "question_type": QUESTION_TYPE_DICT[self.question_type],
                "accepted_answers": [
                    answer.text for answer in self.accepted_answers.all()
                ],
            }
        )
        return data

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class QuestionAnswer(models.Model):
    """An answer to a question."""

    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.text

    def to_json(self):
        return {"id": self.id, "text": self.text}


class GameQuestion(models.Model):
    """Ties a question to a game with round number and question number."""

    created_at = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(
        "Game", related_name="game_questions", on_delete=models.CASCADE
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    round_number = models.IntegerField()
    question_number = models.IntegerField()

    class Meta:
        ordering = ["game", "round_number", "question_number"]

    @property
    def key(self):
        return f"{self.round_number}.{self.question_number}"

    def __str__(self):
        return f"Question {self.key} for game {self.game}"

    def to_json(self):
        question_data = self.question.to_json()
        # remove the question id
        question_data.pop("id")
        return {
            "id": self.pk,
            **question_data,
            "round_number": self.round_number,
            "question_number": self.question_number,
            "key": self.key,
        }

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class GameRound(models.Model):
    """Meta data about a round for a game"""

    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    round_description = models.TextField(blank=True, default="")
    round_number = models.IntegerField()
    game = models.ForeignKey(
        "Game", related_name="game_rounds", on_delete=models.CASCADE
    )

    @property
    def question_count(self):
        return self.game.game_questions.filter(round_number=self.round_number).count()

    class Meta:
        ordering = ["game", "round_number"]

    def __str__(self):
        return f"Round {self.round_number}: {self.title} for game {self.game}"

    def to_json(self):
        return {
            "id": self.pk,
            "title": self.title,
            "round_description": self.round_description,
            "round_number": self.round_number,
            "question_count": self.question_count,
        }

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


def get_end_of_week(dt=None, roll=None):
    """return the end of the week from dt or the current local date"""
    if roll is None:
        roll = GAME_DAYS_TO_ROLL
    reference_date = (dt or timezone.localdate()) - timedelta(days=roll)
    return reference_date + timedelta(days=6 + roll - reference_date.weekday())


class Game(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    block_code = models.CharField(max_length=150, default="")
    title = models.CharField(max_length=200)

    date_used = models.DateField(default=timezone.now)
    active_through = models.DateField(default=get_end_of_week, null=True, blank=True)
    use_sound = models.BooleanField(default=True)

    @property
    def block(self):
        return self.block_code.split(" ")[0].capitalize()

    class Meta:
        ordering = ["-date_used", "title"]

    def __str__(self):
        return self.title

    def to_json(self):
        return {
            "game_id": self.pk,
            "game_title": self.title,
            "block": self.block_code,
            "use_sound": self.use_sound,
        }

    def clean(self, *args, **kwargs):
        # TODO: this may not be required since we are now setting it in the airtable importer
        # add active through date to new instances which do not already have on set
        if not self.pk and self.active_through is None:
            self.active_through = get_end_of_week(dt=self.date_used)

        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class TriviaEvent(models.Model):
    def __init__(self, *args, create_joincode=False, **kwargs):
        # shall we auto-generate a joincode?
        self.create_joincode = create_joincode
        super().__init__(*args, **kwargs)

    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(default=timezone.now)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    location = models.ForeignKey(
        "Location", blank=True, null=True, on_delete=models.SET_NULL
    )
    joincode = models.CharField(max_length=64, unique=True, db_index=True)
    current_round_number = models.IntegerField(default=1)
    current_question_number = models.IntegerField(default=1)

    host = models.ForeignKey(
        "user.User",
        related_name="event_host",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    # used to limit qty of players from a team that can join an event
    player_limit = models.IntegerField(blank=True, null=True)
    players = models.ManyToManyField("user.User", related_name="players", blank=True)
    event_teams = models.ManyToManyField("team", related_name="event_teams", blank=True)
    event_complete = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    @property
    def current_question_key(self):
        return f"{self.current_round_number}.{self.current_question_number}"

    @property
    def round_count(self):
        return self.game.game_rounds.count()

    def all_rounds_are_locked(self):
        """Compare the number on non-tiebreaker rounds against the number of locked round states"""
        num_rounds = self.game.game_rounds.exclude(round_number=0).count()
        num_locked_rounds = len([rd for rd in self.round_states.all() if rd.locked])

        return num_rounds > 0 and num_rounds == num_locked_rounds

    def max_scored_round(self):
        round_states = self.round_states.filter(scored=True).order_by("round_number")
        num_states = len(round_states)
        if num_states == 0:
            return None
        return round_states[num_states - 1].round_number

    def max_locked_round(self):
        round_states = self.round_states.filter(locked=True).order_by("round_number")
        num_states = len(round_states)
        if num_states == 0:
            return None
        return round_states[num_states - 1].round_number

    def __str__(self):
        return f"{self.game.title} on {self.date} - {self.joincode}"

    def game_json(self):
        return {
            "id": self.pk,
            # "game_id": self.pk,
            "game_title": self.game.title,
            "joincode": self.joincode,
            "location": self.location.name if self.location else "",
            "block_code": self.game.block_code,
        }

    def to_json(self):
        return {
            "event_data": self.game_json(),
            "current_event_data": {
                "round_number": self.current_round_number,
                "question_number": self.current_question_number,
                "question_key": self.current_question_key,
            },
            "rounds": queryset_to_json(self.game.game_rounds.exclude(round_number=0)),
            "questions": queryset_to_json(
                self.game.game_questions.exclude(round_number=0).order_by(
                    "round_number", "question_number"
                )
            ),
            "round_states": queryset_to_json(self.round_states.all()),
            "question_states": queryset_to_json(self.question_states.all()),
        }

    def generate_joincode(self, attempts, *args, **kwargs):
        if attempts > MAX_CREATE_JOINCODE_ATTEMPTS:
            raise JoincodeError(
                detail="cannot create a joincode for this event, too many attempts"
            )
        try:
            self.joincode = random.randint(1000, MAX_JOINCODE_VALUE)
            self.full_clean()

        # if the error is joincode related, try to create a new one else reraise
        except ValidationError as e:
            if "joincode" in e.error_dict:
                self.generate_joincode(attempts + 1, *args, **kwargs)
            raise ValidationError(e)

    def save(self, *args, **kwargs):
        if self.pk is not None and self.create_joincode:
            raise JoincodeError(
                detail="cannot auto generate a joincode for an existing Trivia Event"
            )

        if self.create_joincode:
            self.generate_joincode(0, *args, **kwargs)
        else:
            self.full_clean()

        super().save(*args, **kwargs)


class EventQuestionState(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(
        TriviaEvent, related_name="question_states", on_delete=models.CASCADE
    )
    question_number = models.IntegerField()
    round_number = models.IntegerField()
    question_displayed = models.BooleanField(default=False)
    answer_displayed = models.BooleanField(default=False)

    class Meta:
        ordering = ["event", "round_number", "question_number"]

    @property
    def key(self):
        return f"{self.round_number}.{self.question_number}"

    def __str__(self):
        return f"Question {self.key} - {self.event}"

    def to_json(self):
        return {
            "question_number": self.question_number,
            "round_number": self.round_number,
            "key": self.key,
            "question_displayed": self.question_displayed,
            "answer_displayed": self.answer_displayed,
        }

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class TeamNote(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    event = models.ForeignKey(
        TriviaEvent, related_name="question_note", on_delete=models.CASCADE
    )
    team = models.ForeignKey(
        "Team", related_name="question_note", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "user.User", related_name="question_note", on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        GameQuestion, related_name="question_note", on_delete=models.CASCADE
    )
    text = models.TextField(max_length=120)

    def local_created_at(self, as_string=True):
        """return the created_at field in local time"""
        local_time = timezone.localtime(self.created_at)

        if as_string:
            return f"{local_time:%I:%M:%S %p}"
        return local_time

    def __str__(self):
        return f"{self.user} - {self.team} - {self.event}"

    def to_json(self):
        return {
            "id": self.id,
            "event_id": self.event.id,
            "team_id": self.team.id,
            "user": self.user.username,
            "question_id": self.question.id,
            "text": self.text,
            "time": self.local_created_at(),
        }


# round for an event extends a game round with mutable boolean fields (locked and scored)
class EventRoundState(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(
        TriviaEvent, related_name="round_states", on_delete=models.CASCADE
    )
    round_number = models.IntegerField()
    locked = models.BooleanField(default=False)
    revealed = models.BooleanField(default=False)
    scored = models.BooleanField(default=False)

    class Meta:
        ordering = ["-event", "round_number"]

    def __str__(self):
        return f"Round {self.round_number} - {self.event}"

    def to_json(self):
        return {
            "round_number": self.round_number,
            "locked": self.locked,
            "scored": self.scored,
            "revealed": self.revealed,
        }

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
