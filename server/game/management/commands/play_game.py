from django.core.management.base import BaseCommand

from game.models import *

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


class GameActions:
    def __init__(self, game_id: int, joincode: int = None, **kwargs) -> None:
        self.game_id = game_id
        self.joincode = joincode  # or create_joincode()
        self.event = self.create_event(**kwargs)

    # TODO: this is likley very useable for actual host event creation
    def create_event(self, **kwargs):
        try:
            return TriviaEvent.objects.create(
                game_id=self.game_id, joincode=self.joincode, **kwargs
            )

        # TODO: what exceptions can arise here and how do we handle them?
        except:
            return None

    def create_users(self):
        """Create the necessary users based on number of teams and players per team"""
        # create the user and set an active team? then we base all team things off
        # of user_active_team, just like in api endpoints

    def add_teams(self, users):
        """Add teams to the event"""
        # create leaderboard entries for each team (based off of user active team)
        # add teams to the event
        # add players to the event


# provide various getters/setters to update the db to simulate game play
class TeamActions:
    def __init__(self, game: GameActions) -> None:
        self.game = game
        self.event = game.event

    def join_game(self):
        if self.event is None:
            raise AttributeError("There is no event to join")


class HostActions:
    def __init__(self, game: GameActions) -> None:
        self.game = game

    def create_event(self):
        pass


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
            "-D",
            "--delete",
            help="Delete all data associated with a game but not the actual game data.",
        )
        parser.add_argument(
            "-t", "--teams", default=1, help="the number of teams added to the event"
        )

    def handle(self, *args, **options):
        pass

    def delete_data(game_id):
        """Delete all downstream data associated with game_id"""
        # look up events associated w/ game id
        # delete all of the following:
        # users
        # teams
        # leaderboard(entries)
        # resps
        # question/round states
