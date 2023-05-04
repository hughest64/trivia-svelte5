import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from game.models import *
from game.utils.game_play import GameActions, TeamActions, HostActions

"""
TODO: it would be nice to use an existing event and start/stop and an rd. that way we could
progress the game and check status at any point, i.e. --start=1 --stop=4 then --start=5 --end=8
an option to run tests at any point would be awsome-sauce as well

run the cmd:
python manage.py play_game -g --game 4567 # looks up a game and creates an event from it
-D --delete (capital) would delete all data from the event down, BUT NOT THE GAME DATA!
-r --rounds the number of rounds to play

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
        parser.add_argument(
            "-c",
            "--config",
            help="The name of a json file used for game play. This option takes precedence over all others. Config files must be located run_game_configs dir",
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
            "-u",
            "--reuse",
            action="store_true",
            help="use in conjuction with -j to reuse an existing event instead of creating a new one",
        )
        parser.add_argument(
            "-D",
            "--delete",
            action="store_true",
            help="Delete all data associated with a game but not the actual game data.",
        )
        parser.add_argument(
            "-t",
            "--teams",
            default=0,
            type=int,
            help="the number of teams added to the event",
        )
        # TODO: possibly add start and stop r0und args and/or remove this one
        parser.add_argument(
            "-r",
            "--rounds",
            default=0,
            type=int,
            help="The number of trivia event rounds to play",
        )

    def handle(self, *args, **options):
        config = options.get("config")
        team_configs = None
        host_config = None
        if config:
            config_path = (
                settings.BASE_DIR / f"game/management/run_game_configs/{config}"
            )
            if not config_path.exists():
                self.stderr.write(f"no config file exists at {config_path}")
                return
            else:
                with open(config_path, "r") as f:
                    data = json.load(f)
                game_id = data.get("game_id")
                joincode = data.get("joincode")
                teams = data.get("teams")
                rounds_to_play = data.get("rounds_to_play")
                reuse = data.get("reuse")
                team_configs = data.get("team_configs")
                host_config = data.get("host_config")
        else:
            game_id = options.get("game")
            joincode = options.get("joincode")
            teams = options.get("teams")
            rounds_to_play = options.get("rounds")
            reuse = options.get("reuse")

        if reuse and joincode is None:
            raise ValueError("-r cannot be used without -j")

        if game_id is not None or reuse:
            self.play_game(
                game_id,
                reuse,
                joincode,
                teams,
                rounds_to_play,
                team_configs,
                host_config,
            )

        elif joincode is not None and options.get("delete"):
            self.delete_data(joincode=joincode)
            print("deleted")

        else:
            print("unrecognized command")

    def play_game(
        self,
        game_id: int | None,
        reuse: bool,
        joincode: int = None,
        teams=0,
        rounds_to_play=0,
        team_configs=None,
        host_config=None,
    ):
        if team_configs is None:
            team_configs = {}
        if host_config is None:
            host_config = {}

        with transaction.atomic():
            game = None
            if game_id is not None:
                game = Game.objects.get(id=game_id)
            g = GameActions(
                game=game, joincode=joincode, team_count=teams, auto_create=not reuse
            )
            self.stdout.write(f"playing: {g.event}")

            teams_dict = {team.name: TeamActions(g.event, team) for team in g.teams}
            host = HostActions(g.event)

            for r in range(1, rounds_to_play + 1):
                for i, team in enumerate(teams_dict.values(), start=1):
                    team_rd = (
                        team_configs.get(str(i), {}).get("rounds", {}).get(str(r), [])
                    )
                    if len(team_rd) > 0:
                        team.answer_questions_from_config(r, team_rd)
                    else:
                        team.answer_questions(rd_num=r, points_awarded=2.5)

                # host.lock(r)
                # host.score(r)
                # host.reveal_answers(r)
                # host.update_leaderboard()

    def delete_data(game_id=None, event_id=None, joincode=None):
        """Delete all downstream data associated with game_id"""
        if joincode is not None:
            # due models.CASCADE, this will delete associated leaderboard entries and round states
            # but NOT teams or users
            TriviaEvent.objects.filter(joincode=joincode).delete()

        # look up events associated w/ game id
        # delete all of the following:
        # users
        # teams
        # leaderboard(entries)
        # resps
        # question/round states
