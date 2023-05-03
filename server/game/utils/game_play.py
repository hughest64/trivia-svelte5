from game.models import *
from game.processors import TriviaEventCreator

from user.models import User


class GameActions(TriviaEventCreator):
    def __init__(
        self, game: Game, joincode: int = None, team_count: int = None, **kwargs
    ) -> None:
        super().__init__(game, joincode, **kwargs)
        # number of teams to create and add to the event
        self.team_count = team_count
        print(self.team_count)
        self.players = []
        self.teams = []
        if self.team_count > 0:
            self.create_teams()
            self.add_teams_to_event()

    def create_teams(self):
        """Create the desired number of teams and player user per teams"""
        for i in range(1, self.team_count + 1):
            team, _ = Team.objects.get_or_create(name=f"run_game_team_{i}")
            user, _ = User.objects.get_or_create(
                username=f"run_game_user_{i}",
                defaults={"active_team": team, "password": 12345},
            )
            self.players.append(user)
            self.teams.append(team)

    def add_teams_to_event(self):
        """Add teams to the event"""
        # create leaderboard entries for each team (based off of user active team)
        for team in self.teams:
            LeaderboardEntry.objects.get_or_create(
                event=self.event, team=team, leaderboard_type=LEADERBOARD_TYPE_HOST
            )
        self.event.event_teams.set(self.teams)
        self.event.players.set(self.players)


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
