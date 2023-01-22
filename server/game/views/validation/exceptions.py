from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_403_FORBIDDEN


def event_exception_handler(exc, context):
    # TODO: handle DataValidationError w/o subclassing APIException
    response = exception_handler(exc, context)
    reason = None
    if response is not None:
        reason = exc.get_codes()
        response.data["detail"] = str(exc.detail)
    if reason is not None:
        response.data["reason"] = reason

    return response


class TeamRequired(APIException):
    status_code = HTTP_403_FORBIDDEN
    default_detail = "You must be on a team to view this page"
    default_code = "team_required"


# TODO: better detail, perhaps reference the actual limit?
class PlayerLimitExceeded(APIException):
    status_code = HTTP_403_FORBIDDEN
    default_detail = "Player limit exceeded for this event"
    default_code = "player_limit_exceeded"


class LeaderboardEntryRequired(APIException):
    status_code = HTTP_403_FORBIDDEN
    default_detail = "A leaderboard entry is required to view this page"
    default_code = "join_required"
