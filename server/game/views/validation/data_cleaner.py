import json

from rest_framework.exceptions import NotFound

from game.models import Leaderboard, TriviaEvent, LEADERBOARD_TYPE_PUBLIC
from user.models import User

from game.views.validation.exceptions import (
    DataValidationError,
    PlayerLimitExceeded,
    EventJoinRequired,
)


def check_player_limit(event: TriviaEvent, user: User):
    team_players = event.players.filter(active_team=user.active_team)
    player_limit = event.player_limit or 0
    player_count = team_players.count()
    player_joined = user in team_players
    limit_exceeded = False
    if (
        player_count == event.player_limit and not player_joined
    ) or player_count > player_limit > 0:
        limit_exceeded = True

    if limit_exceeded:
        raise PlayerLimitExceeded

    if not limit_exceeded and player_joined:
        return True

    return False


# TODO: now not being used, can we deprecate?
def get_public_leaderboard(
    event: TriviaEvent, user: User, raise_for_entry=True
) -> Leaderboard:
    """
    Lookup the public leaderboard for an event. If raise_for_entry is True, disallow access to an event
    if a player's active team does not have a leaderboard entery for the event.
    """
    # TODO:
    # an alternative here is to make them an "observer", i.e. cannot submit responses, but can view the game
    # a user persmission to allow it would also be good (debugging, etc)
    try:
        public_lb = Leaderboard.objects.get(
            event=event,
            leaderboard_type=LEADERBOARD_TYPE_PUBLIC,
        )
        if raise_for_entry:
            if not public_lb.leaderboard_entries.filter(team=user.active_team).exists():
                raise EventJoinRequired

    except Leaderboard.DoesNotExist:
        raise NotFound(detail=f"A leaderboard for {event} does not exist")

    return public_lb


def get_event_or_404(joincode) -> TriviaEvent:
    try:
        return TriviaEvent.objects.get(joincode=joincode)
    except TriviaEvent.DoesNotExist:
        raise NotFound(detail=f"Event with join code {joincode} does not exist")


class DataCleaner:
    def __init__(self, data=None, deserialize=False):
        self.data = data
        self.deserialize = deserialize
        self._validate_init()

    def _validate_init(self):
        if self.deserialize and self.data is not None:
            self.data = self._parse_json(self.data)
        elif self.data is None:
            self.data = {}
        if not isinstance(self.data, dict):
            raise DataValidationError("the data property must be a dict", "test")

    def _is_iterable_collection(self, value):
        if not isinstance(value, str) and hasattr(value, "__iter__"):
            return True
        return False

    def _parse_json(value):
        try:
            return json.loads(value)
        except json.decoder.JSONDecodeError:
            raise DataValidationError(f"{value} is not valid serialized json")

    def _get_value_from_key(self, key, data=None):
        value = self.data.get(key, data)
        if key is None and data is None:
            raise ValueError("the data param is required when key is None")
        return value

    def as_bool(self, key=None, data=None):
        value = self._get_value_from_key(key, data)
        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            if value.lower() == "false":
                return False
            # any string other than "false", "False", or "" will return True
            return bool(value)

        raise DataValidationError(f"cannot cast {value} to boolean")

    def as_int(self, key=None, data=None):
        value = self._get_value_from_key(key, data)
        try:
            return int(value)
        except ValueError:
            raise DataValidationError(f"cannot cast {value} to int", key)

    def as_float(self, key=None, data=None):
        value = self._get_value_from_key(key, data)
        try:
            return float(value)
        except ValueError:
            raise DataValidationError(f"cannot cast {value} to float", key)

    def as_string(self, key=None, data=None):
        value = self._get_value_from_key(key, data)
        try:
            return str(value)
        except ValueError:
            raise DataValidationError(f"cannot cast {value} to string", key)

    def as_int_array(self, key=None, data=None, deserialize=False):
        value = self._get_value_from_key(key, data)
        if deserialize:
            value = json.loads(value)
        if self._is_iterable_collection(value):
            return [self.as_int(data=v) for v in value]

        raise DataValidationError(f"{type(value)} is not an iterable collection", key)

    def as_float_array(self, key=None, data=None, deserialize=False):
        value = self._get_value_from_key(key, data)
        if deserialize:
            value = json.loads(value)
        if self._is_iterable_collection(value):
            return [self.as_float(data=v) for v in value]

        raise DataValidationError(f"{type(value)} is not an iterable collection", key)

    def as_string_array(self, key=None, data=None, deserialize=False):
        value = self._get_value_from_key(key, data)
        if deserialize:
            value = json.loads(value)
        if self._is_iterable_collection(value):
            return [self.as_string(data=v) for v in value]

        raise DataValidationError(f"{type(value)} is not an iterable collection", key)
