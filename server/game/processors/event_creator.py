from game.models import *


class TriviaEventCreator:
    def __init__(self, game: Game, joincode: int = None, **kwargs) -> None:
        self.game = game
        self.joincode = joincode
        self.create_joincode = joincode is None
        self.event = None
        self.create_event(**kwargs)

    def create_event(self, **kwargs):
        """Create an event"""
        try:
            self.event = TriviaEvent.objects.create(
                game=self.game,
                joincode=self.joincode,
                create_joincode=self.create_joincode,
                **kwargs,
            )

        # TODO: what exceptions can arise here and how do we handle them?
        # maybe a custom exception like EventNotCreated?
        except ValidationError as e:
            raise ValidationError(e)

        else:
            self.create_event_states()

    def create_event_states(self):
        """Create round states for the event"""
        # TODO: error handling?
        for round in self.game.game_rounds.all():
            if round.round_number == 0:
                continue
            EventRoundState.objects.get_or_create(
                event=self.event, round_number=round.round_number
            )
