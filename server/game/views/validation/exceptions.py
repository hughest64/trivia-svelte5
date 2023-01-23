import json

from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST
from rest_framework.views import exception_handler


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


class TeamRequired(APIException):
    status_code = HTTP_403_FORBIDDEN
    default_detail = "You must be on a team to view this page"
    default_code = "team_required"


class PlayerLimitExceeded(APIException):
    status_code = HTTP_403_FORBIDDEN
    default_detail = "Players per team limit exceeded for this event"
    default_code = "player_limit_exceeded"


class LeaderboardEntryRequired(APIException):
    status_code = HTTP_403_FORBIDDEN
    default_detail = "A leaderboard entry is required to view this page"
    default_code = "join_required"


def event_exception_handler(exc, context):
    if isinstance(exc, APIException):
        response = exception_handler(exc, context)
        reason = None
        if response is not None:
            reason = exc.get_codes()
            response.data["detail"] = str(exc.detail)
        if reason is not None:
            response.data["reason"] = reason

        return response

    if isinstance(exc, DataValidationError):
        return Response(data=exc.response, status=exc.status)

    return None
