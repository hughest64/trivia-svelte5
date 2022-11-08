from django.db import models


QUESTION_TYPE_GENERAL_KNOWLEDGE = 0
QUESTION_TYPES = [
    (QUESTION_TYPE_GENERAL_KNOWLEDGE, 'GeneralKnowledge')
]

class Game(models.Model):
    pass


class GameRound(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    round_number = models.IntegerField()
    title = models.CharField(max_len=128)
    description: models.CharField(max_len=128)

    def __str__(self):
        return f"Round {self.round_number}: {self.title}"


class Question(models.Model):
    text = models.TextField()
    answer = models.CharField(max_len=255)
    question_type = models.IntegerField(choices=QUESTION_TYPES, default=0)
    question_url = models.CharField(max_len=255)


class GameQuestion(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    round_number = models.ForeignKey(GameRound, on_delete=models.CASCADE)
    question_number = models.IntegerField()
    key = models.CharField(max_len=3)


# TODO: different file
class EventQuestion(models.Model):
    game_question = models.ForeignKey(GameQuestion, on_delete=models.CASCADE)
    question_displayed = models.BooleanField()
    answer_displayed = models.BooleanField()


class EventRound(models.Model):
    round_number = models.ForeignKey(GameRound, on_delete=models.CASCADE)
    locked = models.BooleanField()
    scored = models.BooleanField()
