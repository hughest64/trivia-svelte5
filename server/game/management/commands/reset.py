from django.core.management.base import BaseCommand

from game.models import *


class Command(BaseCommand):
    help = "reset event related data for the demo app"

    def handle(self, *args, **kwargs):
        """reset all mutable event related data for an event with the joincode 1234"""
        self.stdout.write("reseting event data")
        events = TriviaEvent.objects.filter(joincode__in=[1234, 9998, 9999])
        events.update(current_question_number=1, current_round_number=1)
        for event in events:
            event.players.clear()
            event.event_teams.clear()
        EventQuestionState.objects.filter(event__joincode=1234).update(
            question_displayed=False, answer_displayed=False
        )
        EventRoundState.objects.filter(event__joincode=1234).update(
            scored=False, locked=False
        )
        LeaderboardEntry.objects.filter(leaderboard__event__joincode=1234).delete()
        QuestionResponse.objects.exclude(event__joincode=9998).delete()
        self.stdout.write("finished resetting event data")
