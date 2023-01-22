import json

from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN


class EventException(Exception):
    status_code = HTTP_403_FORBIDDEN
    default_detail = "Not Allowed"
    default_reason = "not_allowed"

    def __init__(self, detail=None, status=None, reason=None) -> None:
        self.detail = detail or self.default_detail
        self.status = status or self.status_code
        self.reason = reason or self.default_reason

    def __str__(self):
        return self.detail

    @property
    def response(self):
        return {
            "detail": self.detail,
            "reason": self.reason,
            "status": self.status,
        }


class LeaderboardEntryRequired(EventException):
    default_detail = "A leaderboard entry is required to view this page"
    default_reason = "join_required"


class TeamRequried(EventException):
    default_detail = "You must be on a team to view this page"
    default_reason = "team_required"
