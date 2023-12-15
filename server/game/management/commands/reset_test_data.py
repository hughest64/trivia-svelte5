import logging
import json

from django.core.management.base import BaseCommand, CommandParser
from django.core.management import call_command
from django.conf import settings

from game.models import *

from user.models import User

DATA_DIR = settings.BASE_DIR.parent / "tests/data"

logger = logging.getLogger(__name__)

with open(DATA_DIR / "users.json") as f:
    user_data = json.load(f)

with open(DATA_DIR / "games.json") as f:
    game_data = json.load(f)

## games, users, etc from this file will not be deleted on db reset
with open(DATA_DIR / "exclude.json") as f:
    excludes = json.load(f)


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
            self.create_users()
            self.create_games()

        if options.get("games"):
            self.create_games()

    def reset(self):
        excluded_users = excludes.get("users", [])
        User.objects.exclude(username__in=excluded_users).delete()

    def create_users(self):
        logger.info(f"crating {len(user_data)} user(s)")
        for u in user_data.values():
            is_staff = u.get("is_staff", False)
            # TOOD: get_or_create team (maybe we can reuse code here)
            team_name = u.pop("team_name", None)
            # throw the auth storage path away
            u.pop("auth_storage_path", None)
            User.objects.create_user(**u, is_superuser=is_staff)

    def create_games(self):
        logger.info("create games is not implemented")
        return
