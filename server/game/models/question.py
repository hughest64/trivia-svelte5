from django.db import models
from django.forms.models import model_to_dict
from django.utils import timezone


QUESTION_TYPE_GENERAL_KNOWLEDGE = 0
QUESTION_TYPES = [
    (QUESTION_TYPE_GENERAL_KNOWLEDGE, 'GeneralKnowledge')
]

# Basic immutable question, has no round or question number
class Question(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    answer = models.CharField(max_len=255)
    question_type = models.IntegerField(choices=QUESTION_TYPES, default=0)
    question_url = models.CharField(max_len=255)
    question_notes = models.CharField(max_len=255)

    def __str__(self):
        return self.text

    def to_json(self):
        return model_to_dict(self)


# a question that belongs to a specific game, but is immutable
class GameQuestion(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey("Game", relate_name="questions", on_delete=models.CASCADE)
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
            "question": model_to_dict(self.question),
            "round_number": self.round_number,
            "question_number": self.question_number,
            "key": self.key
        }


# basic round information, immutable
class GameRound(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey("Game", related_name="rounds", on_delete=models.CASCADE)
    round_number = models.IntegerField()
    title = models.CharField(max_len=128)
    description: models.CharField(max_len=128)

    class Meta:
        order_by = ("-round_number",) # TODO: verify the sort here

    def __str__(self):
        return f"Round {self.round_number}: {self.title}"

    def to_json(self):
        return {
            "round_number": self.round_number,
            "title": self.title,
            "description": self.description
        }


class Game(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    block_code = models.CharField(max_length=150, default="")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date_used = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title # TODO: block code?

    def to_json(self):
        rounds = self.rounds.all()
        questions = self.questions.all()

        return {
            "block_code": self.block_code,
            "title": self.title,
            "description": self.description,
            "date_used": self.date_used,
            "rounds": [round.to_json() for round in rounds],
            "questions": [question.to_json() for question in questions]
        }


# TODO: different file
class TriviaEvent(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    join_code = models.CharField(max_len=64)

    


# a question on a trivia event, extend a game question and is mutible (q and a displayed)
class EventQuestion(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(TriviaEvent, related_name="questions", on_delete=models.CASCADE)
    question = models.ForeignKey(GameQuestion, on_delete=models.CASCADE)
    question_displayed = models.BooleanField()
    answer_displayed = models.BooleanField()


# round for an event extends a game round with mutable boolean fields (locked and scored)
class EventRound(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(TriviaEvent, related_name="rounds", on_delete=models.CASCADE)
    round = models.ForeignKey(GameRound, on_delete=models.CASCADE)
    locked = models.BooleanField()
    scored = models.BooleanField()
