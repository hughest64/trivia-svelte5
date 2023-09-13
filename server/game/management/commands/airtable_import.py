import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from game.processors.airtable_importer import AirtableData
from game.processors.game_creator import create_games_from_airtable_data

GAME_DAYS_TO_ROLL = settings.GAME_DAYS_TO_ROLL


class Command(BaseCommand):
    help = "Create trivia games and private events from Airtable data."

    def add_arguments(self, parser):
        parser.add_argument(
            "-p",
            "--private",
            action="store_true",
            default=None,
            help="Pass this option to import airtable data from the private events base.\
                The private argument will always take precedence over the notprivate argument.",
        )
        parser.add_argument(
            "-n",
            "--notprivate",
            action="store_false",
            default=None,
            help="Pass this argument to import airtable data from the standard events base.\
                The script defaults to the value of the PRIVATE_EVENT setting if no arguments are provided.",
        )
        parser.add_argument(
            "-N",
            "--nocommit",
            action="store_true",
            help="Run the entire import process but do not commit any data to the database.",
        )
        parser.add_argument(
            "-s",
            "--start",
            help="The starting date for the airtable query in ISO format.",
        )
        parser.add_argument(
            "-e", "--end", help="The end date for the airtable query in ISO format."
        )
        parser.add_argument(
            "-R",
            "--roll",
            default=GAME_DAYS_TO_ROLL,
            type=int,
            help="Number of days to move the requested date range. Can be positive or negative.",
        )
        parser.add_argument(
            "-r",
            "--raw",
            action="store_true",
            help="Run the airtable import and dump the raw data, prints to stdout unless the file path option is provided.\
                Note that no data will be commited to the database when this option is used.",
        )
        parser.add_argument(
            "-i",
            "--indent",
            type=int,
            default=4,
            help="Integer that is passed to json.dump(s) when writing raw airtable data. Defaluts to 4.",
        )
        parser.add_argument(
            "-f",
            "--filepath",
            default=None,
            help="Location to dump raw airtable data, has no effect unless used with the '-r' option.",
        )

    def handle(self, *args, **options):
        is_private = options.get("private") or options.get("notprivate")
        if is_private is None:
            is_private = settings.PRIVATE_EVENT

        self.stdout.write(
            f"Running airtable import{' for private events' if is_private else ''}"
        )

        start = options.get("start")
        end = options.get("end")
        roll = options.get("roll")
        commit = not options.get("nocommit")
        if not commit:
            self.stdout.write(
                "Running the import prcess but not commting to the database"
            )

        if options.get("raw"):
            fp = options.get("filepath")
            if fp is not None and not os.path.exists(os.path.dirname(fp)):
                self.stderr.write(f"{fp} is not a valid file path")
                return
            indent = options.get("indent")
            atd = AirtableData(start=start, end=end, private_event=is_private)
            data = atd.get_airtable_data(raw=True)
            if fp:
                self.stdout.write(f"wrote airtable data to {fp}")
                with open(fp, "w") as f:
                    json.dump(data, f, indent=indent)
                return

            self.stdout.write(json.dumps(data, indent=indent))
            return

        try:
            import_data = create_games_from_airtable_data(
                private_event=is_private,
                commit=commit,
                verbose=True,
                start=start,
                end=end,
                roll=roll,
            )
            return json.dumps(import_data)
        except NotImplementedError as e:
            self.stderr.write(e)
