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
    location_data = None
    user_data = None
    team_data = None

    def create_db_connection(self):
        if self.cur is None:
            conn = psycopg2.connect(
                "dbname=tm_transfer user=triviamafia password=supergoodpassword"
            )
            self.cur = conn.cursor()

    def close_db_connection(self):
        if self.cur is not None:
            self.cur.close()

    def get_locs_from_db(self):
        loc_string = """
            SELECT name, address, active FROM game_location
            WHERE game_location.active = True
        """
        self.cur.execute(loc_string)
        records = self.cur.fetchall()

        print(len(records), "total locations")
        print("location columns", [desc[0] for desc in self.cur.description])
        if len(records) > 0:
            print(records[0])

        self.location_data = records
        return records

    def get_users_from_db(self):
        user_string = """
            SELECT
                u.username,
                u.email,
                u.password,
                u.is_staff,
                u.is_superuser,
                tu.screen_name,
                -- tu.active_team_id,
                l.name
            FROM auth_user u

            LEFT JOIN game_triviauser tu
            ON tu.user_id = u.id

            LEFT JOIN game_triviauser_home_locations hl
            ON hl.triviauser_id = tu.id
            LEFT JOIN game_location l
            ON l.id = hl.location_id

            WHERE tu.is_anonymous_user = False
        """

        self.cur.execute(user_string)
        data = self.cur.fetchall()
        print(len(data), "total users")
        print("user columns", [desc[0] for desc in self.cur.description])
        if len(data) > 0:
            print(data[0])

        self.user_data = data

        return data

    def get_teams_from_db(self):
        team_string = """
            SELECT
                -- team.id,
                team.team_name,
                jc.join_code,
                u.username,
                tu.active_team_id
            FROM game_triviauser_teams tuteam

            INNER JOIN game_triviauser tu
            ON tu.id = tuteam.triviauser_id

            INNER JOIN auth_user u
            ON u.id = tu.user_id

            INNER JOIN game_team team
            ON team.id = tuteam.team_id

            LEFT JOIN game_joincode jc
            ON jc.id = team.join_code_id

            WHERE tu.is_anonymous_user = False
        """
        self.cur.execute(team_string)

        team_dict = {}
        for row in self.cur:
            team_id, team_name, password, username, active_id = row
            team_dict.setdefault(
                team_id,
                {
                    "id": team_id,
                    "team_name": team_name,
                    "password": password,
                    "members": set(),
                },
            )
            is_active_team = team_id == active_id
            team_dict[team_id]["members"].add((username, is_active_team))
        print(len(team_dict.keys()), "total teams")
        print("team columns", [desc[0] for desc in self.cur.description])

        team_dict_values = list(team_dict.values())
        if len(team_dict_values) > 0:
            print(team_dict_values[0])

        self.team_data = team_dict_values
        return team_dict_values

    def load_locations(self):
        if self.location_data is None:
            print("there are no locations to load")
            return

        locs_created = 0
        try:
            with transaction.atomic():
                for row in self.location_data:
                    name, address, active = row
                    _, created = Location.objects.update_or_create(
                        name=name,
                        defaults={
                            "address": address,
                            "active": active,
                            "use_sound": True,
                        },
                    )
                    locs_created += int(created)
        except Exception as e:
            print("could not create locations", e)

        else:
            print(
                f"Created {locs_created} new of {len(self.location_data)} locations provided"
            )

    def load_users(self):
        if self.user_data is None:
            print("there are no users to load")
            return

        users_created = 0
        try:
            with transaction.atomic():
                for row in self.user_data:
                    (
                        username,
                        email,
                        password,
                        is_staff,
                        is_superuser,
                        screen_name,
                        # active_team_id,
                        home_loc_name,
                    ) = row

                    try:
                        user_home_location = Location.objects.get(name=home_loc_name)
                    except Location.DoesNotExist:
                        user_home_location = None

                    _, created = User.objects.update_or_create(
                        username=username,
                        email=email,
                        defaults={
                            "home_location": user_home_location,
                            "password": password,
                            "screen_name": screen_name,
                            "is_staff": is_staff,
                            "is_superuser": is_superuser,
                        },
                    )
                    users_created += int(created)

        except Exception as e:
            print("could not create users", e)
        else:
            print(
                f"Created {users_created} new of {len(self.user_data)} teams provided"
            )

    def load_teams(self):
        if self.team_data_data is None:
            print("there are no locations to load")
            return

        teams_created = 0
        try:
            with transaction.atomic():
                for row in self.team_data:
                    name, joincode, users = row
                    team, created = Team.objects.update_or_create(
                        name=name, password=joincode
                    )
                    teams_created += int(created)

                    # all members of a team
                    members = User.objects.filter(
                        username__in=[tup[0] for tup in users]
                    )
                    team.members.set(members)

                    # get a list of usernames for whom this is the active team
                    active_membernames = [tup[0] for tup in users if tup[1]]
                    active_members = members.filter(username__in=active_membernames)

                    for m in active_members:
                        m.active_team = team
                    User.objects.bulk_update(active_members, fields=["active_team"])

        except Exception as e:
            print("could not create teams", e)

        else:
            print(
                f"Created {teams_created} new of {len(self.team_data)} users provided"
            )


class Command(Xfer, BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-d",
            "--database",
            action="store_true",
            help="pull data directly with sql queries",
        )
        parser.add_argument(
            "-c",
            "--create",
            action="store_true",
            help="create the items in the new database",
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

            print("\nfetching locations")
            self.get_locs_from_db()

            print("\nfetching users")
            self.get_users_from_db()

            # print("\nfecting teams")
            # self.get_teams_from_db()

            self.close_db_connection()

        if options.get("create"):
            print("\nloading locations")
            self.load_locations()

            print("\nloading users")
            self.load_users()

        print("Finished loading data, Have a nice day!")
