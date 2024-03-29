import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from game.models import *
from game.utils.game_play import EventSetup, TeamActions, HostActions

"""
TODO: it would be nice to use an existing event and start/stop and an rd. that way we could
progress the game and check status at any point, i.e. --start=1 --stop=4 then --start=5 --end=8
an option to run tests at any point would be awsome-sauce as well

run the cmd:
python manage.py play_game -g --game 4567 # looks up a game and creates an event from it
-D --delete (capital) would delete all data from the event down, BUT NOT THE GAME DATA!
-r --rounds the number of rounds to play

we need options for all of these things
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
        parser.add_argument(
            "-d",
            "--data",
            help="use a dictionary of data for game play instead of loading a file",
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
        parser.add_argument(
            "-r",
            "--rounds",
            default=0,
            type=int,
            help="The number of trivia event rounds to play",
        )

    def handle(self, *args, **options):
        config = options.get("config")
        data = options.get("data")

        if config:
            config_path = (
                settings.BASE_DIR / f"game/management/run_game_configs/{config}"
            )
            if not config_path.exists():
                self.stderr.write(f"no config file exists at {config_path}")
                return
            else:
                with open(config_path, "r") as f:
                    game_data = json.load(f)
        elif data:
            game_data = json.loads(data) if isinstance(data, str) else data
        else:
            game_data = options

        joincode = game_data.get("joincode")
        game_id = game_data.get("game_id")

        if joincode is not None and options.get("delete"):
            self.delete_data(joincode=joincode)
            self.stdout.write("deleted")
            return

        if game_id is None and joincode is None:
            raise ValueError("at least one of joincode or game_id is required")

        self.play_game(**game_data)

    def play_game(
        self,
        game_id: int = None,
        joincode: int = None,
        reset_event=True,
        player_limit=False,
        teams=0,
        rounds_to_play: int = None,
        team_configs=None,
        host_config=None,
        **kwargs,
    ):
        if team_configs is None:
            team_configs = {}
        if host_config is None:
            host_config = {}

        with transaction.atomic():
            game = None
            try:
                game = Game.objects.get(id=game_id)
            except Game.DoesNotExist:
                game = Game.objects.latest("id")
                print(
                    f"Game with id {game_id} does no exist, using latest id, {game.id}"
                )

            g = EventSetup(
                game=game,
                joincode=joincode,
                auto_create=True,
                reset=reset_event,
                player_limit=player_limit,
            )
            self.stdout.write(f"playing: {g.event}")
            host = HostActions(g.event)

            for i in range(1, teams + 1):
                team_config = team_configs[str(i)]
                team = TeamActions(g.event)
                team.get_or_create_team(
                    team_config.get("name"), i, players=team_config.get("players")
                )
                team.add_team_to_event()

                # use the score percentage if provided
                if team_config.get("score_percentage") is not None:
                    team.answer_questions_from_percentage(
                        team_config.get("score_percentage"),
                        through_rd=rounds_to_play,
                        megaround_data=team_config.get("megaround"),
                    )
                elif team_config.get("questions") is not None:
                    team.answer_questions(team_config.get("questions"))

                # else answer questions on a per round played basis
                # else:
                #     team_rds = team_config.get("rounds", {})
                #     for r in range(1, rounds_to_play + 1):
                #         team_rd = team_rds.get(str(r), [])
                #         # we have predetermined answers for this round
                #         if len(team_rd) > 0:
                #             team.answer_questions_from_config(r, team_rd)

                #         else:
                #             team.answer_questions(rd_num=r, points_awarded=2.5)

            if rounds_to_play is not None and host_config.get("lock_rounds"):
                [host.lock(r) for r in range(1, rounds_to_play + 1)]

            # TODO: handle these scenarios
            # host.score(r)
            # host.reveal_answers(r)
            # host.update_leaderboard()

    def delete_data(game_id=None, event_id=None, joincode=None):
        """Delete all downstream data associated with game_id"""
        if joincode is not None:
            # due to models.CASCADE, this will delete associated leaderboard entries and round states
            # but NOT teams or users
            TriviaEvent.objects.filter(joincode=joincode).delete()
