import json

from rest_framework.exceptions import NotFound

from game.models import Game, Location, TriviaEvent
from user.models import User

from game.views.validation.exceptions import (
    DataValidationError,
    EventJoinRequired,
    PlayerLimitExceeded,
)


def check_player_limit(event: TriviaEvent, user: User, join_required=False):
    """
    Check the user's active team against the active team of other user's on the event.
    Raise an error if too many players have joined the vent for the user's active team.
    Return a boolean indicating whether or not the user has already joined the event.
    """
    # members of the user's active team already on the event
    team_players = event.players.filter(active_team=user.active_team)
    player_limit = event.player_limit or 0
    player_count = team_players.count()
    # has the user joined the event?
    player_joined = user in team_players
    limit_exceeded = False
    if (
        # limit has been reached but the user has not joined
        player_count == event.player_limit
        and not player_joined
        # already past the player limit
    ) or player_count > player_limit > 0:
        limit_exceeded = True

    if limit_exceeded:
        raise PlayerLimitExceeded

    if not limit_exceeded and player_joined:
        return True

    if join_required:
        raise EventJoinRequired

    return False


def get_event_or_404(joincode) -> TriviaEvent:
    try:
        return TriviaEvent.objects.get(joincode=joincode)
    except TriviaEvent.DoesNotExist:
        raise NotFound(detail=f"Event with join code {joincode} does not exist")


def get_game_or_404(id) -> Game:
    try:
        return Game.objects.get(id=id)
    except Game.DoesNotExist:
        raise NotFound(detail=f"Game with id {id} does not exist")


def get_location_or_404(id) -> Location:
    try:
        return Location.objects.get(id=id)
    except Location.DoesNotExist:
        raise NotFound(detail=f"Location with id {id} does not exist")


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

    def as_dict(self):
        return self.data

    def as_bool(self, key=None, data=None):
        if self.data.get(key) is None and data is None:
            return False
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
        if value is None:
            return None
        try:
            return int(value)
        except ValueError:
            raise DataValidationError(f"cannot cast {value} to int", key)

    def as_float(self, key=None, data=None):
        value = self._get_value_from_key(key, data)
        if value is None:
            return None
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
