from datetime import timedelta

from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from django.utils import timezone

from game.models import *
from user.models import User


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("-j", "--job")
        parser.add_argument("-d", "--days", default=7)

    def handle(self, *args, **options):
        days = options.get("days")
        job_type = options.get("job")

        if job_type == "leaderboard":
            self.purge_empty_leaderboard_entries(days=days)
        elif job_type == "joincodes":
            self.anonymize_join_codes(days=days)
        elif job_type == "users":
            self.purge_anonymous_users(days=days)
        else:
            print("nothing to do")

    def anonymize_join_codes(self, days=30):
        start_date = timezone.now() - timedelta(days=days)
        # TODO: maybe select_for_update() is a good idea here?
        events = TriviaEvent.objects.filter(date__lte=start_date, archived=False)
        if len(events) < 1:
            return {
                "results": f"no events to update found on or before {start_date:%Y-%m-%d}"
            }
        errors = []
        for event in events:
            try:
                with transaction.atomic():
                    event.archived = True
                    event.joincode += f"{event.date:%Y%m%d}"
                    event.save()

            except Exception as e:
                errors.append({"joincode": event.joincode, "error": e})

        error_string = ""
        if len(errors) > 0:
            error_string = (
                f" {len(errors)} event(s) had errors and was/were not updated: {errors}"
            )

        return {
            "results": f"updated join code for {len(events) - len(errors)} event(s) on or before {start_date:%Y-%m-%d}.{error_string}"
        }

    def purge_anonymous_users(days=7):
        start_date = timezone.now() - timedelta(days=days)
        anonymous_users = User.objects.filter(created_at__lte=start_date, is_guest=True)
        user_count = anonymous_users.count()

        if user_count < 1:
            return {
                "results": f"No active anonymous users found created before {start_date:%Y-%m-%d}"
            }
        anonymous_users.delete()

        return {
            "results": f"deleted {user_count} anonymous user(s) created before {start_date:%Y-%m-%d}"
        }

    def purge_empty_leaderboard_entries(self, days=7):
        start_date = timezone.now() - timedelta(days=days)
        entry_count = 0
        events = TriviaEvent.objects.filter(date__lte=start_date, archived=False)

        for event in events:
            # all teams
            all_teams = set(event.event_teams.all())
            # set of teams with actual responses
            teams_with_resps = {r.team for r in event.responses.all()}
            teams_with_no_resps = all_teams - teams_with_resps

            entries_to_delete = LeaderboardEntry.objects.filter(
                event=event, team__in=teams_with_no_resps
            )
            entry_count += entries_to_delete.count()
            entries_to_delete.delete()

        if entry_count < 1:
            return {
                "results": "No empty Leaderboard Entires found created before {start_date:%Y-%m-%d}"
            }

        noun = "entry" if entry_count == 1 else "entries"
        return {
            "results": f"Deleted {entry_count} {noun} created before {start_date:%Y-%m-%d}"
        }
