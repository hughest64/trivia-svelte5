import json

from rest_framework.exceptions import APIException, NotFound
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from game.models import TriviaEvent


def get_event_or_404(join_code) -> TriviaEvent:
    try:
        return TriviaEvent.objects.get(join_code=join_code)
    except TriviaEvent.DoesNotExist:
        raise NotFound(detail=f"Event with join code {join_code} does not exist")


class TeamRequired(APIException):
    status_code = HTTP_403_FORBIDDEN
    default_detail = "You must be on a team to view this page"


class DataValidationError(Exception):
    def __init__(self, message=None, field=None, status=None):
        self.message = message or "Invalid Data"
        self.field = field
        self.status = status or HTTP_400_BAD_REQUEST

    def __str__(self):
        return json.dumps(self.response())

    @property
    def response(self):
        parts = [self.message]
        if self.field:
            parts.append(self.field)

        return {"detail": " - ".join(parts), "status": self.status}


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
