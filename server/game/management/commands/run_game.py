from django.core.management.base import BaseCommand

from game.models import *
from game.utils.game_play import GameActions

"""
TODO: it would be nice to use an existing event and start/stop and an rd. that way we could
progress the game and check status at any point, i.e. --start=1 --stop=4 then --start=5 --end=8
an option to run tests at any point would be awsome-sauce as well

run the cmd:
python manage.py play_game -g --game 4567 # looks up a game and creates an event from it
-D --delete (capital) would delete all data from the event down, BUT NOT THE GAME DATA!
-r --rounds the number of rounds to play

so the fist step is to create and event from a game id, this can likely be used for actual
host event creation as well

-t --teams number of teams to have on the event
is there a config option to specify teams, or are they "random" - random to start
can we specify a number of players?
- create a number of users for the teams?
- create the number of requested teams
- the teams join the event
- host reveals rd 1
- teams answer (need an answer generator here that randomizes resps - can control %corect per team?)
- continue for all rds
TODO: we need options for all of these things
- host locks
- host socres? (future add on)
- host reveals
- host updates leaderboards
- tiebreakers
- host finishes event
"""


class Command(BaseCommand):
    help = "A utiltiy tool for simulating trivia events."

    def add_arguments(self, parser):
        # possible args:
        # - start stage
        # - stop stage
        parser.add_argument(
            "-c",
            "--conifg",
            required=False,
            help="The path of a config file used for game play. This option takes precedence over all others.",
        )
        parser.add_argument("-g", "--game", help="the id of the game data to use")
        parser.add_argument(
            "-e",
            "--event",
            help="the id of a trivia event, useful for deleting a single event and it's data",
        )
        parser.add_argument(
            "-j",
            "--joincode",
            help="the joincode of a trivia event, useful for deleting a single event and it's data",
        )
        parser.add_argument(
            "-D",
            "--delete",
            action="store_true",
            help="Delete all data associated with a game but not the actual game data.",
        )
        parser.add_argument(
            "-t", "--teams", default=1, help="the number of teams added to the event"
        )

    def handle(self, *args, **options):
        game_id = options.get("game")
        joincode = options.get("joincode")

        if game_id is not None:
            game = Game.objects.get(id=game_id)
            g = GameActions(game=game)
            print(g.event)

        elif joincode is not None and options.get("delete"):
            self.delete_data(joincode=joincode)
            print("deleted")

        else:
            print("unrecognized command")

    def delete_data(game_id=None, event_id=None, joincode=None):
        """Delete all downstream data associated with game_id"""
        if joincode is not None:
            TriviaEvent.objects.filter(joincode=joincode).delete()

        # look up events associated w/ game id
        # delete all of the following:
        # users
        # teams
        # leaderboard(entries)
        # resps
        # question/round states
