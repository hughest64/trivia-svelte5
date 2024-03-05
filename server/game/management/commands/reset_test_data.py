import logging
import json

from django.core.management.base import BaseCommand, CommandParser
from django.core.management import call_command
from django.conf import settings

from game.models import *
from game.processors import TriviaEventCreator

from user.models import User

DATA_DIR = settings.BASE_DIR.parent / "tests/data"

logger = logging.getLogger(__name__)

with open(DATA_DIR / "users.json") as f:
    user_data = json.load(f)

with open(DATA_DIR / "trivia_events.json") as f:
    trivia_events = json.load(f)

## games, users, etc from this file will not be deleted on db reset
try:
    with open(DATA_DIR / "exclude.json") as f:
        excludes = json.load(f)
except Exception as e:
    logger.warning(f"could not load exclued test reset data\m{e}")
    excludes = {}


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-a",
            "--all",
            action="store_true",
            help="pass this arg to run all set up commands",
        )
        parser.add_argument(
            "-g", "--games", action="store_true", help="create games but not users"
        )
        parser.add_argument("-t", "--team", action="store_true")

    def handle(self, *args, **options) -> str | None:
        logger.info(f"Using settings file {settings.SETTINGS_FILE_NAME}")
        if settings.SETTINGS_FILE_NAME != "server.settings_tst":
            self.stderr.write(
                "the reset command is only available when using test settings"
            )
            return
        logger.info("Resetting Test Data")
        self.reset()

        if options.get("all"):
            call_command("loaddata", "game/fixtures/gamedata.json")
            self.create_users()
            # self.create_games()
            self.create_trivia_events()

    def reset(self):
        excluded_users = excludes.get("users", [])
        User.objects.exclude(username__in=excluded_users).delete()
        Team.objects.all().delete()
        Game.objects.all().delete()
        Question.objects.all().delete()
        QuestionAnswer.objects.all().delete()

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
            u = User.objects.create_user(
                **u, is_superuser=is_staff, active_team=active_team
            )
            u.teams.set(teams)

    def create_trivia_events(self):
        logger.info(f"creating {len(trivia_events)} trivia events")

        games = Game.objects.all()

        for event in trivia_events.values():
            event_creator = TriviaEventCreator(
                joincode=event.get("joincode"),
                game=games.first(),  # TODO: use a .get with a fallback to .first() (or random)?
                player_limit=event.get("player_limit", False),
            )
