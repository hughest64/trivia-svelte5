import io
import logging
import json
import random

from django.core.management.base import BaseCommand, CommandParser
from django.core.management import call_command
from django.conf import settings
from django.utils import timezone

from game.models import *
from game.processors import TriviaEventCreator

from user.models import User

DATA_DIR = settings.BASE_DIR.parent / "tests/data"

logger = logging.getLogger(__name__)

with open(DATA_DIR / "users.json") as f:
    user_data = json.load(f)

with open(DATA_DIR / "trivia_events.json") as f:
    trivia_events = json.load(f)

with open(DATA_DIR / "locations.json") as f:
    locations = json.load(f)

## games, users, etc from this file will not be deleted on db reset
try:
    with open(DATA_DIR / "exclude.json") as f:
        excludes = json.load(f)
except Exception as e:
    logger.warning(f"could not load exclued test reset data\m{e}")
    excludes = {}


class Command(BaseCommand):
    data_removed = False

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-a",
            "--all",
            action="store_true",
            help="pass this arg to run all set up commands",
        )
        parser.add_argument(
            "-g", "--games", action="store_true", help="load game data only"
        )
        parser.add_argument("-t", "--team", action="store_true"),
        parser.add_argument(
            "-e",
            "--erase",
            action="store_true",
            help="delete exisiting data but do not load new data",
        ),
        parser.add_argument("-r", "--reset_indicies", action="store_true")

    def handle(self, *args, **options) -> str | None:
        logger.info(f"Using settings file {settings.SETTINGS_FILE_NAME}")
        if settings.SETTINGS_FILE_NAME != "server.settings_tst":
            self.stderr.write(
                "the reset command is only available when using test settings"
            )
            return
        logger.info("Resetting Test Data")

        # the all option takes precedence over all other options
        if options.get("all"):
            self.reset_data()
            self.reset_indicies()
            call_command("loaddata", "game/fixtures/gamedata.json")
            self.create_locations()
            self.create_users()
            self.update_game_dates()
            self.create_trivia_events()

        else:
            if options.get("games"):
                print(Game.objects.all())

            if options.get("erase"):
                logger.info("removing existing data")
                self.reset_data()

            if options.get("reset_indicies"):
                self.reset_indicies()

    def reset_data(self):
        excluded_users = excludes.get("users", [])
        User.objects.exclude(username__in=excluded_users).delete()
        Team.objects.all().delete()
        Location.objects.all().delete()
        Game.objects.all().delete()
        Question.objects.all().delete()
        QuestionAnswer.objects.all().delete()

        # reset the id of excluded objects so they come first (could be moved to bulk update if neccessary)
        for i, name in enumerate(excluded_users, start=1):
            try:
                user = User.objects.get(username=name)
                user.id = i
                user.save()
            except User.DoesNotExist:
                pass

        self.data_removed = True

    def reset_indicies(self):
        """
        Ensure we get a fresh set of table ids on each run.
        First use sqlsequencereset to produce the required sql to maniupulate the id index for all tables.
        Then modify the sql so all tables reset to use 1 as the first available id.
        Finally, use the dbshell command to update the test database.
        """
        if not self.data_removed:
            raise Exception("cannot reset db indicies before removing data")

        iodata = io.StringIO()
        call_command("sqlsequencereset", "game", "user", no_color=True, stdout=iodata)
        stringdata = iodata.getvalue().replace('coalesce(max("id"), 1)', "1")
        call_command("dbshell", "--", "-c", stringdata)

    def create_locations(self):
        logger.info(f"creating {len(locations)} locations")

        created_locations = [Location(**loc_data) for loc_data in locations]
        Location.objects.bulk_create(created_locations)

    def create_users(self):
        logger.info(f"creating {len(user_data)} user(s)")
        for u in user_data.values():
            # throw the auth storage path away
            u.pop("auth_storage_path", None)

            team_names = u.pop("team_names", [])
            team_configs = u.pop("team_configs", [])
            teams = []
            # first add generic teams (auto gen the password)
            if len(team_names) > 0:
                for name in team_names:
                    try:
                        team = Team.objects.get(name=name)
                    except Team.DoesNotExist:
                        team = Team.objects.create(name=name)
                    teams.append(team)

            # then more specific team data
            if len(team_configs) > 0:
                for config in team_configs:
                    join = config.pop("join", False)
                    team = Team.objects.create(**config)
                    if join:
                        teams.append(team)

            active_team = teams[0] if len(teams) > 0 else None
            is_staff = u.get("is_staff", False)

            # try to get a home location for the user
            home_loc_index = u.pop("home_location_index", None)
            home_location = None
            if home_loc_index:
                try:
                    home_location = Location.objects.get(
                        name=locations[home_loc_index].get("name")
                    )
                except Location.DoesNotExist:
                    logger.warning(
                        f"could not set home location for user {u.get('username')}"
                    )

            user = User.objects.create_user(
                **u,
                is_superuser=is_staff,
                active_team=active_team,
                home_location=home_location,
            )
            user.teams.set(teams)

    def update_game_dates(self):
        games = Game.objects.all()
        games.update(active_through=timezone.now())

    def create_trivia_events(self):
        logger.info(f"creating {len(trivia_events)} trivia events")

        games = Game.objects.all()

        for event in trivia_events.values():
            event_creator = TriviaEventCreator(
                joincode=event.get("joincode"),
                # NOTE this would need work to use an actual game, (like the id or some other sepcific data)
                # look for a specific game or use a random one,
                game=event.get("game", games[random.randint(0, len(games) - 1)]),
                player_limit=event.get("player_limit", False),
            )
            teams = event.get("teams", [])
            players = event.get("players", [])
            event_creator.event.event_teams.set(Team.objects.filter(name__in=teams))
            event_creator.event.players.set(User.objects.filter(username__in=players))

            leaderboard_entries = []
            fetched_teams = Team.objects.filter(name__in=teams)
            for team in fetched_teams:
                host_lb = LeaderboardEntry(
                    team=team,
                    event=event_creator.event,
                    leaderboard_type=LEADERBOARD_TYPE_HOST,
                )
                public_lb = LeaderboardEntry(
                    team=team,
                    event=event_creator.event,
                    leaderboard_type=LEADERBOARD_TYPE_PUBLIC,
                )
                leaderboard_entries.extend([host_lb, public_lb])

            if leaderboard_entries:
                LeaderboardEntry.objects.bulk_create(leaderboard_entries)
