from django.db import models
from django.forms.models import model_to_dict
from django.utils import timezone

QUESTION_TYPE_GENERAL_KNOWLEDGE = 0
QUESTION_TYPE_THEMED_ROUND = 1
QUESTION_TYPE_WORD_PLAY = 2
QUESTION_TYPE_IMAGE_ROUND = 3
QUESTION_TYPE_LIGHTNING_ROUND = 4
QUESTION_TYPE_SOUND_ROUND = 5
QUESTION_TYPE_TIE_BREAKER = 6

# TODO: validate the string values here agaainst airtable
QUESTION_TYPES = [
    (QUESTION_TYPE_GENERAL_KNOWLEDGE, "General Knowledge"),
    (QUESTION_TYPE_THEMED_ROUND, "Themed Round"),
    (QUESTION_TYPE_WORD_PLAY, "Word Play"),
    (QUESTION_TYPE_IMAGE_ROUND, "Image Round"),
    (QUESTION_TYPE_LIGHTNING_ROUND, "Lightning Round"),
    (QUESTION_TYPE_SOUND_ROUND, "Sound Round"),
    (QUESTION_TYPE_TIE_BREAKER, "Tiebreaker"),
]

question_type_dict = dict(QUESTION_TYPES)


def queryset_to_json(qs):
    """Convert a queryset to a list of dictionaires. The model must implement a to_json method."""
    if not qs.exists():
        return []

    # TODO: maybe check has_attr(qs.first(), 'to_json') and raise NotImplemented if False?
    return [instance.to_json() for instance in qs]

class Question(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    question_type = models.IntegerField(choices=QUESTION_TYPES, default=0)
    question_text = models.TextField()
    question_url = models.CharField(max_length=255, blank=True, null=True)
    display_answer = models.CharField(max_length=255)
    # TODO: answers (ArrayField)
    answer_notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.question_text[:30] + "..."

    def to_json(self):
        data = model_to_dict(self)
        # get the text value
        data.update({"question_type": question_type_dict[self.question_type]})
        return data

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class GameQuestion(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(
        "Game", related_name="game_questions", on_delete=models.CASCADE
    )
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

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class GameRound(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    round_description = models.TextField(blank=True, default="")
    round_number = models.IntegerField()
    game = models.ForeignKey(
        "Game", related_name="game_rounds", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Round {self.round_number}: {self.title}"

    def to_json(self):
        return {
            "id": self.pk,
            "title": self.title,
            "round_description": self.round_description,
            "round_number": self.round_number,
        }

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Game(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    block_code = models.CharField(max_length=150, default="")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date_used = models.DateField(default=timezone.now)

    class Meta:
        ordering = ["-date_used", "title"]

    def __str__(self):
        return self.title  # TODO: block code?

    # TODO: this isn't a great representation for to_json as it doesn't contain all the things
    def to_json(self):
        return {
            # "game_id": self.pk,
            "block_code": self.block_code,
            "game_title": self.title,
            # "description": self.description,
        }

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class TriviaEvent(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(default=timezone.now)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    join_code = models.CharField(max_length=64, unique=True, db_index=True)
    current_round_number = models.IntegerField(default=1)
    current_question_number = models.IntegerField(default=1)

    @property
    def current_question_key(self):
        return f"{self.current_round_number}.{self.current_question_number}"

    def __str__(self):
        return f"{self.game.title} on {self.date}"

    def to_json(self):
        return {
            "event_data": {
                "id": self.pk,
                # "game_id": self.pk,
                "game_title": self.game.title,
                "join_code": self.join_code,
                # TODO: add this
                # "location": self.location.name
                "block_code": self.game.block_code,
            },
            "current_event_data": {
                "round_number": self.current_round_number,
                "question_number": self.current_question_number,
                "quesion_key": self.current_question_key,
            },                
            "rounds": queryset_to_json(self.game.game_rounds.all()),
            "questions": queryset_to_json(self.game.game_questions.all()),
            "round_states": queryset_to_json(self.round_states.all()),
            "question_states": queryset_to_json(self.question_states.all()),
        }

    def save(self, *args, **kwargs):
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

    @property
    def key(self):
        return f"{self.round_number}.{self.question_number}"

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


# round for an event extends a game round with mutable boolean fields (locked and scored)
class EventRoundState(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(
        TriviaEvent, related_name="round_states", on_delete=models.CASCADE
    )
    round_number = models.IntegerField()
    locked = models.BooleanField(default=False)
    scored = models.BooleanField(default=False)

    def to_json(self):
        return {
            "round_number": self.round_number,
            "locked": self.locked,
            "scored": self.scored,
        }

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)