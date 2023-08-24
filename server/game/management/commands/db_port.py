import json
import os

from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction

from game.models import *
from user.models import *


class Xfer:
    fp = None

    def load_locations(self):
        with open(f"{self.fp}/locs.json", "r") as f:
            loc_data = json.load(f)
        locs_created = 0
        try:
            with transaction.atomic():
                for l in loc_data:
                    _, created = Location.objects.update_or_create(
                        name=l.get("name"),
                        defaults={
                            "address": l.get("address"),
                            "active": l.get("active"),
                            "use_sound": l.get("use_sound"),
                        },
                    )
                    locs_created += int(created)
        except Exception as e:
            print("could not create locations", e)

        else:
            print(f"Created {locs_created} new of {len(loc_data)} locations provided")

    def load_teams(self):
        with open(f"{self.fp}/teams.json", "r") as f:
            teams_data = json.load(f)
        teams_created = 0
        try:
            with transaction.atomic():
                for t in teams_data:
                    _, created = Team.objects.update_or_create(
                        name=t.get("team_name"), password=t.get("password")
                    )
                    teams_created += int(created)
        except Exception as e:
            print("could not create teams", e)

        else:
            print(f"Created {teams_created} new of {len(teams_data)} users provided")

    def load_users(self):
        with open(f"{self.fp}/users.json", "r") as f:
            users_data = json.load(f)
        users_created = 0
        missing_teams = set()

        try:
            with transaction.atomic():
                for u in users_data:
                    try:
                        user_home_loc = Location.objects.get(
                            name=u.get("home_location")
                        )

                    except Location.DoesNotExist:
                        user_home_loc = None

                    user, created = User.objects.update_or_create(
                        username=u.get("username"),
                        password=u.get("password"),
                        screen_name=u.get("screen_name"),
                        email=u.get("email"),
                        is_staff=u.get("is_staff"),
                        is_superuser=u.get("is_superuser"),
                        defaults={"home_location": user_home_loc},
                    )
                    users_created += int(created)

                    user_teams = u.get("teams")
                    for t in user_teams:
                        try:
                            db_team = Team.objects.get(
                                name=t.get("team_name"), password=t.get("password")
                            )
                            user.teams.add(db_team)
                        except Team.DoesNotExist:
                            missing_teams.add(t)

        except Exception as e:
            print("could not create users", e)
        else:
            print(f"Created {users_created} new of {len(users_data)} teams provided")
            if len(missing_teams) > 0:
                print(missing_teams)


class Command(Xfer, BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-u", "--users", action="store_true", help="load users into the database"
        )
        parser.add_argument(
            "-t", "--teams", action="store_true", help="load teams into the database"
        )
        parser.add_argument(
            "-l",
            "--locations",
            action="store_true",
            help="load locations into the database",
        )
        parser.add_argument(
            "-p",
            "--path",
            required=True,
            type=str,
            help="file path for fetching source data",
        )

    def handle(self, *args, **options):
        self.fp = options.get("path")

        if not os.path.exists(os.path.dirname(self.fp)):
            self.stderr.write(f"{self.fp} is not a valid file path")
            return

        if options.get("locations"):
            self.load_locations()

        if options.get("teams"):
            self.load_teams()

        if options.get("users"):
            self.load_users()

        print("Finished loading data, Have a nice day!")
