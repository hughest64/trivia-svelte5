import json
import os

from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from django.utils.crypto import get_random_string

from game.models import *
from user.models import *

import pandas as pd
import psycopg2


class Xfer:
    fp = None
    cur = None

    def create_db_connection(self):
        if self.cur is None:
            conn = psycopg2.connect(
                "dbname=tm_transfer user=triviamafia password=supergoodpassword"
            )
            self.cur = conn.cursor()

    def close_db_connection(self):
        if self.cur is not None:
            self.cur.close()

    def get_locs_from_db(self, close=False):
        loc_string = """
            SELECT name, address, active FROM game_location
            WHERE game_location.active = True
        """
        self.cur.execute(loc_string)
        records = self.cur.fetchall()
        labels = ("name", "address", "active")
        df = pd.DataFrame(records, columns=labels)
        j = df.to_json(orient="records", indent=4)

        with open("game/port_data/game_locs.json", "w") as f:
            f.write(j)

        if close:
            self.cur.close()

    def get_teams_from_db(self):
        team_string = """
            SELECT team.id, team.team_name, u.username, tu.active_team_id FROM game_triviauser_teams tuteam

            INNER JOIN game_triviauser tu
            ON tu.id = tuteam.triviauser_id

            INNER JOIN auth_user u
            ON u.id = tu.user_id

            INNER JOIN game_team team
            ON team.id = tuteam.team_id

            WHERE tu.is_anonymous_user = False
        """

        self.cur.execute(team_string)
        records = self.cur.fetchall()

        print(len(records), "total results")
        print([desc[0] for desc in self.cur.description])
        print(records[:10])

        just_ids = set([t[0] for t in records])
        print(len(just_ids), "unique results")

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
                        email=u.get("email", ""),
                        defaults={
                            "home_location": user_home_loc,
                            "password": u.get("password", get_random_string(12)),
                            "screen_name": u.get("screen_name", ""),
                            "is_staff": u.get("is_staff", False),
                            "is_superuser": u.get("is_superuser", False),
                        },
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
            required=False,
            type=str,
            help="file path for fetching source data",
        )
        parser.add_argument(
            "-d",
            "--database",
            action="store_true",
            help="pull data directly with sql queries",
        )

    def handle(self, *args, **options):
        self.fp = options.get("path")

        if self.fp:
            if not os.path.exists(os.path.dirname(self.fp)):
                self.stderr.write(f"{self.fp} is not a valid file path")
                return

        if options.get("locations"):
            self.load_locations()

        if options.get("teams"):
            self.load_teams()

        if options.get("users"):
            self.load_users()

        if options.get("database"):
            self.create_db_connection()

            # self.get_locs_from_db()
            self.get_teams_from_db()

            self.close_db_connection()

        print("Finished loading data, Have a nice day!")
