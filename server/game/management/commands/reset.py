from django.core.management.base import BaseCommand

from game.models import *


class Command(BaseCommand):
    help = "reset event related data for the demo app"

    def handle(self, *args, **kwargs):
        """reset all mutable event related data for an event with the joincode 1234"""
        self.stdout.write("reseting event data")
        TriviaEvent.objects.filter(join_code=1234).update(
            current_question_number=1, current_round_number=1
        )
        EventQuestionState.objects.filter(event__join_code=1234).update(
            question_displayed=False, answer_displayed=False
        )
        EventRoundState.objects.filter(event__join_code=1234).update(
            scored=False, locked=False
        )
        QuestionResponse.objects.all().delete()
        self.stdout.write("finished resetting event data")
