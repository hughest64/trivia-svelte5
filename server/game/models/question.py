from django.db import models
from django.forms.models import model_to_dict
from django.utils import timezone

QUESTION_TYPE_GENERAL_KNOWLEDGE = 0
QUESTION_TYPES = [(QUESTION_TYPE_GENERAL_KNOWLEDGE, "General Knowledge")]


def queryset_to_json(qs):
    """Convert a queryset to a list of dictionaires. The model must implement a to_json method."""
    try:
        if not qs.exists():
            return []
        return [instance.to_json() for instance in qs]

    except AttributeError:
        raise NotImplementedError("The model must implement a to_json method")


# Basic immutable question, has no round or question number
class Question(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    answer = models.CharField(max_len=255)
    notes = models.CharField(max_len=255)
    question_type = models.IntegerField(choices=QUESTION_TYPES, default=0)
    question_url = models.CharField(max_len=255)

    def __str__(self):
        return self.text

    def to_json(self):
        return model_to_dict(self)


# a question that belongs to a specific game, but is immutable
class GameQuestion(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey("Game", related_name="game_questions", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    round_number = models.IntegerField()
    question_number = models.IntegerField()

    @property
    def key(self):
        return f"{self.round_number}.{self.question_number}"

    def __str__(self):
        return self.key

    def to_json(self):
        return {
            **self.question.to_json(),
            "round_number": self.round_number,
            "question_number": self.question_number,
            "key": self.key,
        }


# basic round information, immutable
class GameRound(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey("Game", related_name="game_rounds", on_delete=models.CASCADE)
    round_number = models.IntegerField()
    title = models.CharField(max_len=128)
    description: models.CharField(max_len=128)

    def __str__(self):
        return f"Round {self.round_number}: {self.title}"

    def to_json(self):
        return {
            "round_number": self.round_number,
            "title": self.title,
            "description": self.description,
        }


class Game(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    block_code = models.CharField(max_length=150, default="")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date_used = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title  # TODO: block code?

    # reverse lookup
    def rounds(self):
        return self.rounds.all()

    def questions(self):
        return self.questions.all()

    def to_json(self):
        return {
            "block_code": self.block_code,
            "title": self.title,
            "description": self.description,
            "date_used": self.date_used,
        }


class TriviaEvent(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    join_code = models.CharField(max_len=64, unique=True, db_index=True)

    def __str__(self):
        return f"{self.game.title} on {self.date}"

    # reverse lookup
    def round_states(self):
        return self.round_states.all()

    def question_states(self):
        return self.round_states.all()

    def to_json(self):
        return {
            "event_data": {"join_code": self.join_code, **self.game.to_json()},
            "round_states": queryset_to_json(self.round_states()),
            "question_states": queryset_to_json(self.question_states()),
            "game_rounds": queryset_to_json(self.game.game_rounds.all()),
            "game_questions": queryset_to_json(self.game.game_questions.all())
        }


# a question on a trivia event, extend a game question and is mutible (q and a displayed)
class EventQuestionState(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(
        TriviaEvent, related_name="questions", on_delete=models.CASCADE
    )
    question_number = models.IntegerField()
    round_number = models.IntegerField()
    question_displayed = models.BooleanField()
    answer_displayed = models.BooleanField()

    def to_json(self):
        return {
            "question_number": self.question_number,
            "round_number": self.round_number,
            "key": self.question.key,
            "question_displayed": self.question_displayed,
            "answer_displayed": self.answer_displayed,
        }


# round for an event extends a game round with mutable boolean fields (locked and scored)
class EventRoundState(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(
        TriviaEvent, related_name="rounds", on_delete=models.CASCADE
    )
    round_number = models.IntegerField()
    locked = models.BooleanField()
    scored = models.BooleanField()

    def to_json(self):
        return {
            "round_number": self.round_number,
            "locked": self.locked,
            "scored": self.scored,
        }


# I think this is mostly what we are shooting for in an event payload
event_payload = {
    "event_data": {
        # pulled from game
        "title": "abcd",
        # pulled from event
        "location": "abc bar",
        "join_code": 1234,
    },
    # pulled from specific game
    "game_rounds": [
        {"rond_number": 1, "description": "foo", "title": "bar"},
    ],
    "game_questions": [
        {
            "question_number": 1,
            "key": "1.1",
            "text": "qqq",
            "answer": "bbb",
            "notes": "ccc",
            "url": "abc.com",
        },
    ],
    # pulled specific event
    "event_round_states": [
        {"round_number": 1, "locked": False, "scored": False},
    ],
    "event_question_states": [
        {"key": "1.1", "question_displayed": False, "answer_displayed": False}
    ],
}
