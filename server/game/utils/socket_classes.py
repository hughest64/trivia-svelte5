"""
Helper classes for sending web socket messages outside of the consumer class
"""
from abc import ABC, abstractmethod
from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer


def get_event_group(joincode):
    return f"event_{joincode}"


# combining the team id and joincode ensures messages per team don't pollute other events
def get_team_group(team_id, joincode):
    return f"team_{team_id}_event_{joincode}"


def get_user_group(user_id):
    return f"user_id_{user_id}"


class BaseSocketMessage(ABC):
    """Base class for message handling. It cannot be instantiaed directly."""

    @abstractmethod
    def __init__(self, group: str, message: dict, auto_send=True) -> None:
        self.group = group
        self.message = message
        self._validate()
        self.channel_layer = get_channel_layer()
        if auto_send == True:
            self.send()

    def _validate(self) -> None:
        if not isinstance(self.message, dict):
            raise TypeError("The message property must be a dict.")
        if not "type" in self.message or not "msg_type" in self.message:
            raise ValueError(
                "The message property must contain keys for 'type' and 'msg_type'."
            )

    def send(self) -> None:
        async_to_sync(self.channel_layer.group_send)(self.group, self.message)


class SendEventMessage(BaseSocketMessage):
    def __init__(self, joincode: str | int, message: dict, **kwargs) -> None:
        group = get_event_group(joincode)
        message.update({"type": "event_update"})
        super().__init__(group, message, **kwargs)


class SendTeamMessage(BaseSocketMessage):
    def __init__(self, joincode, team_id: int, message: dict, **kwargs) -> None:
        group = get_team_group(team_id, joincode)
        message.update({"type": "team_update"})
        super().__init__(group, message, **kwargs)
