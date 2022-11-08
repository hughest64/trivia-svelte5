from django.db import models
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


# a question that belongs to a specific game, but is immutable
class GameQuestion(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    round_number = models.IntegerField()
    question_number = models.IntegerField()
    key = models.CharField(max_len=3)

    def __str__(self):
        return self.key # ?

# basic round information, immutable
class GameRound(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    round_number = models.IntegerField()
    title = models.CharField(max_len=128)
    description: models.CharField(max_len=128)

    def __str__(self):
        return f"Round {self.round_number}: {self.title}"


class Game(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    block_code = models.CharField(max_length=150, default="")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date_used = models.DateField(default=timezone.now)


# TODO: different file
# a question on a trivia event, extend a game question and is mutible (q and a displayed)
class EventQuestion(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(GameQuestion, on_delete=models.CASCADE)
    question_displayed = models.BooleanField()
    answer_displayed = models.BooleanField()


# round for an event extends a game round with mutable boolean fields (locked and scored)
class EventRound(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    round = models.ForeignKey(GameRound, on_delete=models.CASCADE)
    locked = models.BooleanField()
    scored = models.BooleanField()


class TriviaEvent(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    join_code = models.CharField(max_len=64)
