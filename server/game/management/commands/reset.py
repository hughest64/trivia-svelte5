from django.core.management.base import BaseCommand, CommandParser

from game.models import *
from user.models import User


class Command(BaseCommand):
    help = "reset event related data for the demo app"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "joincodes",
            nargs="*",
            type=int,
            help="the joincode for a specific event to reset",
        )

    def handle(self, *args, **kwargs):
        """reset all mutable event related data for an event with the joincode 1234"""
        self.stdout.write("reseting event data")

        default_join_codes = {1234, 9998, 9999}
        joincodes = set(kwargs.get("joincodes", [])).union(default_join_codes)

        Team.objects.filter(name="My Cool Team TEST").delete()
        User.objects.filter(username="testuser").delete()

        events = TriviaEvent.objects.filter(joincode__in=joincodes)
        events.update(current_question_number=1, current_round_number=1)
        for event in events:
            event.players.clear()
            event.event_teams.clear()

        EventQuestionState.objects.filter(event__joincode__in=joincodes).delete()
        EventRoundState.objects.filter(event__joincode__in=joincodes).delete()

        LeaderboardEntry.objects.filter(event__joincode__in=joincodes).exclude(
            event__joincode=9998
        ).delete()

        Leaderboard.objects.filter(event__joincode__in=joincodes).exclude(
            event__joincode=9998
        ).delete()

        QuestionResponse.objects.exclude(
            event__joincode__in=default_join_codes
        ).delete()

        self.stdout.write("finished resetting event data")
