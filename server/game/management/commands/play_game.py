from django.core.management.base import BaseCommand


class GameActions:
    def __init__(self, game_id: int, joincode: int) -> None:
        self.game_id = game_id
        self.joincode = joincode

    def setGame(self):
        # handle game lookup and/or event lookup/creation
        # store the peritnent data as an attr
        pass


# provide various getters/setters to update the db to simulate game play
class TeamActions:
    def __init__(self, game: GameActions) -> None:
        self.game = game

    def join_game(self):
        pass


class HostActions:
    def __init__(self, game: GameActions) -> None:
        self.game = game

    def create_event(self):
        pass


class Command(BaseCommand):
    def add_arguments(self, parser):
        # possible args:
        # - config (a file to read)
        # - reset (remove reponses & lb data, but don't delete the event?)
        # - delete (delete event and all the things (except the actual game data))
        # - start stage
        # - stop stage
        return

    def handle(self, *args, **options):
        pass

    # what is the process? (process can be stopped at any stage, then perhaps resumed)
    # - decide a game to use
    # - create an event
    # - decide how many teams will play
    # - host creates the event
    # - teams join the event
    # - teams answer questions - some alg for %correct vs incorrect, etc?
    # - host locks rounds
    # - host scores rounds (perhaps if we want to ensure ties, etc)
    # - host reveals answers
    # - host updates the leaderboard
    # - handle tiebreakers
    # - complete a game
