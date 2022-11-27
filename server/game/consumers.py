from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync

from user.authentication import decode_token, get_user


class SocketConsumer(AsyncJsonWebsocketConsumer):
    unauthorized_msg = {
        "type": "unauthorized",
        "message": "You must be on a team to to play trivia",
    }
    unauthenticated_msg = {"type": "unauthenticated", "message": "You need to log in"}

    user = None
    event_group = ""
    team_group = ""
    user_group = ""

    async def _set_attrs(self):
        """set useful attributes from the scope"""
        kwargs = self.scope.get("url_route", {}).get("kwargs")
        self.joincode = kwargs.get("joincode")
        self.gametype = kwargs.get("gametype")
        self.user = self.scope["user"]
        self.event_group = f"event_{self.joincode}"
        self.team_group = f"team_{self.user.active_team_id}_{self.event_group}"
        self.user_group = f"user_id_{self.user.id}"

    async def _set_connection(self):
        """Called after a user is validated. Will send an unauthenticated message
        (eqivalent to http 401) if user.is_anonymous == True as well as send an
        unauthorized (equvalant to http 403) messasge when accessing a game
        connection without an active team id set.
        """
        user = self.scope.get("user", {})
        kwargs = self.scope.get("url_route", {}).get("kwargs", {})

        if user.is_anonymous:
            await self.send_json(self.unauthenticated_msg)
            return

        # the game socket requires an active team, but on the host socket
        if not user.active_team_id and kwargs.get("gametype") != "host":
            await self.send_json(self.unauthenticated_msg)
            return

        await self._set_attrs()
        await self.join_socket_groups()
        await self.send_json({"type": "connected", "message": "hello Svelte!"})

        print(f"hello {self.user.username} your Join code is {self.joincode} and you are playing on {self.user.active_team_id}")

    async def join_socket_groups(self):
        """Add socket groups for the trivia event, user team, and indiviual user. """
        # trivia event group
        await self.channel_layer.group_add(self.event_group, self.channel_name)
        # team group
        await self.channel_layer.group_add(self.team_group, self.channel_name)
        # individual group (used mostly for host comms with a single player)
        await self.channel_layer.group_add(self.user_group, self.channel_name)

    async def connect(self):
        await self.accept()
        await self._set_connection()

    async def disconnect(self, close_code):
        if self.event_group:
            await self.channel_layer.group_discard(self.event_group, self.channel_name)
            await self.channel_layer.group_discard(self.team_group, self.channel_name)
            await self.channel_layer.group_discard(self.user_group, self.channel_name)

    async def receive_json(self, content):
        # print("content received")
        # print(content)
        if content.get("type") == "authenticate":
           await self.authenticate(content)

    #####################
    ### USER MESSAGES ###
    #####################

    async def authenticate(self, data):
        """Validate a JWT. close the connection with a custom 4010 code if the
        token is not valid. Otherwise set the user in scope and connect.
        """
        msg = data.get("message")
        token = msg.get("token")

        user = await get_user(token)
        if user.is_anonymous:
            await self.close(code=4010)
            return
        else:
            self.scope["user"] = user
            await self._set_connection()

    #####################
    ### TEAM MESSAGES ###
    #####################

    async def team_update(self, data):
        """Pass a single response object back to a team group."""
        # print("updating response", self.team_group)
        msg_type = data.pop("msg_type")
        if msg_type:
            data["type"] = msg_type
        await self.send_json(data)

    ######################
    ### EVENT MESSAGES ###
    ######################

    async def event_update(self, data):
        # print(data)
        msg_type = data.pop("msg_type")
        if msg_type:
            data["type"] = msg_type

        await self.send_json(data)
