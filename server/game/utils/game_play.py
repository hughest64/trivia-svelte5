from game.models import *
from game.processors import TriviaEventCreator


class GameActions(TriviaEventCreator):
    def __init__(self, game: Game, joincode: int = None, **kwargs) -> None:
        super().__init__(game, joincode, **kwargs)

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
