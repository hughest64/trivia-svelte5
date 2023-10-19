from django.core.management.base import BaseCommand, CommandParser

from codename import codename
from game.models import ChangeLog


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("-t", "--title")
        parser.add_argument("-a", "--appversion", required=True)
        parser.add_argument("-n", "--notes", required=True)

    def handle(self, *args, **options):
        try:
            # use the provided title if present, else auto generate one
            title = options.get("title") or codename()
            notes = options.get("notes")
            app_version = options.get("appversion")
            changelog = ChangeLog.objects.create(
                title=title, notes=notes, version=app_version
            )
            self.stdout.write("created Change Log")
            self.stdout.write(str(changelog.to_json()))
        except Exception as e:
            self.stderr.write(str(e))
