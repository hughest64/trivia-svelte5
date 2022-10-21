from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

from user.authentication import decode_token


# TODO: possibly create a separate class for the extra methods as a mix-in
class SocketConsumer(JsonWebsocketConsumer):
    unauthorized_msg = {
        "type": "unauthorized",
        "message": "You must be on a team to to play trivia",
    }
    unauthenticated_msg = {"type": "unauthenticated", "message": "You need to log in"}

    user = None
    event_group = ""
    team_group = ""
    user_group = ""

    def _set_attrs(self):
        """set useful attributes from the scope"""
        kwargs = self.scope.get("url_route", {}).get("kwargs")
        self.joincode = kwargs.get("joincode")
        self.gametype = kwargs.get("gametype")
        self.user = self.scope["user"]
        self.event_group = f"event_{self.joincode}"
        self.team_group = f"team_{self.user.active_team_id}"
        self.user_group = f"user_id_{self.user.id}"

    def _set_connection(self):
        """Called after a user is validated. Will send an unauthenticated message
        (eqivalent to http 401) if user.is_anonymous == True as well as send an
        unauthorized (equvalant to http 403) messasge when accessing a game
        connection without an active team id set.
        """
        user = self.scope.get("user", {})
        kwargs = self.scope.get("url_route", {}).get("kwargs", {})

        if user.is_anonymous:
            self.send_json(self.unauthenticated_msg)
            return

        # the game socket requires an active team, but on the host socket
        if not user.active_team_id and kwargs.get("gametype") != "host":
            self.send_json(self.unauthenticated_msg)
            return

        self._set_attrs()
        self.join_socket_groups()
        self.send_json({"type": "connected", "message": "hello Svelte!"})

        print(f"hello {self.user.username} your Join code is {self.joincode}")

    def join_socket_groups(self):
        """Add socket groups for the trivia event, user team, and indiviual user. """
        # trivia event group
        async_to_sync(self.channel_layer.group_add)(self.event_group, self.channel_name)
        # team group
        async_to_sync(self.channel_layer.group_add)(self.team_group, self.channel_name)
        # individual group (used mostly for host comms with a single player)
        async_to_sync(self.channel_layer.group_add)(self.user_group, self.channel_name)

    def connect(self):
        self.accept()
        self._set_connection()

    def disconnect(self, close_code):
        if self.event_group:
            async_to_sync(self.channel_layer.group_discard)(
                self.event_group, self.channel_name
            )
            async_to_sync(self.channel_layer.group_discard)(
                self.team_group, self.channel_name
            )
            async_to_sync(self.channel_layer.group_discard)(
                self.user_group, self.channel_name
            )

    def receive_json(self, content):
        # print("content received")
        # print(content)
        if content.get("type") == "authenticate":
            self.authenticate(content)

    #####################
    ### USER MESSAGES ###
    #####################

    def authenticate(self, data):
        """Validate a JWT. close the connection with a custom 4010 code if the
        token is not valid. Otherwise set the user in scope and connect.
        """
        msg = data.get("message")
        token = msg.get("token")

        user = decode_token(token)
        if user.is_anonymous:
            self.close(code=4010)
            return
        else:
            self.scope["user"] = user
            self._set_connection()

    #####################
    ### TEAM MESSAGES ###
    #####################

    def team_update_response(self, data):
        """Pass a single response object back to a team group."""
        print("updating response", self.team_group)
        self.send_json(data)

    ######################
    ### EVENT MESSAGES ###
    ######################

    # if we do the db work in a view function and use the socket to update all clients:
    def update_round_locks(self, data):
        data.update({"type": "update_store"})
        self.send_json(data)

    def lock_round(self, data):
        print(data)
        # load the event from datq["message"]["event_id"]
        # set the round lock
        # send all rounds back via:
        self.send_json(
            {
                # "type": "update_store",
                "type": "log_me",
                "store": "eventData",
                "message": {"rounds": ["updated Rounds"]},
            }
        )
