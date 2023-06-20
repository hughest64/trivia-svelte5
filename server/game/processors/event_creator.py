from datetime import date

from game.models import *


class TriviaEventCreator:
    def __init__(
        self,
        game: Game,
        location: Location = None,
        joincode: int = None,
        auto_create=True,
        **kwargs
    ) -> None:
        self.game = game
        self.location = location
        self.joincode = joincode
        self.create_joincode = joincode is None
        self.event = None
        # for now, True = 1, False = None
        self.player_limit = 1 if kwargs.get("player_limit") else None

        if auto_create:
            self.get_or_create_event()

    def get_or_create_event(self):
        try:
            if self.joincode is not None:
                self.event = TriviaEvent.objects.get(joincode=self.joincode)
            else:
                self.event = TriviaEvent.objects.get(
                    game=self.game, location=self.location, date=date.today()
                )

        except TriviaEvent.DoesNotExist:
            self.event = TriviaEvent.objects.create(
                game=self.game,
                location=self.location if self.location else None,
                joincode=self.joincode,
                # TODO: hard coding a one player limit for now, could be expaned
                # if we want to allow more player per team, but still limit
                player_limit=self.player_limit,
                # date=date.today(),
                create_joincode=self.joincode is None,
            )
        self.game = self.event.game
        self.create_event_states()

    def create_event_states(self):
        """Create round states for the event"""
        # TODO: error handling?
        for round in self.game.game_rounds.exclude(round_number=0):
            EventRoundState.objects.get_or_create(
                event=self.event, round_number=round.round_number
            )