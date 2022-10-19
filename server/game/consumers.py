from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

from user.authentication import decode_token
from user.serializers import UserSerializer

error_messages = {
    "unauthorized": {
        "type": "unauthorized",
        "message": "You must be on a team to to play trivia",
    },
    "unauthenticated": {"type": "unauthenticated", "message": "You need to log in"},
}

# TODO: if we end up adding lots of custom methods, it may be nice
# to create a separate class for them and either inherit, or use a mix-in
class SocketConsumer(JsonWebsocketConsumer):
    user = {}
    event_group = ""
    team_group = ""
    user_group = ""

    def _set_attrs(self):
        """set useful attributes from the scope"""
        kwargs = self.scope.get("url_route", {}).get("kwargs")
        self.joincode = kwargs.get("joincode")
        self.gametype = kwargs.get("gametype")
        # TODO: consider if this is useful, or if we should just keep the User object
        self.user = UserSerializer(self.scope["user"]).data
        self.event_group = f"event_{self.joincode}"
        self.team_group = f"team_{self.user.get('active_team_id')}"
        self.user_group = f"user_id_{self.user.get('id')}"

    def join_socket_groups(self):
        """add the connection to the three event groups"""
        # trivia event group
        async_to_sync(self.channel_layer.group_add)(self.event_group, self.channel_name)
        # team group
        async_to_sync(self.channel_layer.group_add)(self.team_group, self.channel_name)
        # individual group (used mostly for host comms with a single player)
        async_to_sync(self.channel_layer.group_add)(self.user_group, self.channel_name)

    def connect(self):
        user = self.scope.get("user", {})
        kwargs = self.scope.get("url_route", {}).get("kwargs", {})
        self.accept()

        if user.is_anonymous:
            self.send_json(error_messages["unauthenticated"])
            return

        # the game socket requires an active team, but on the host socket
        if not user.active_team_id and kwargs.get("gametype") != "host":
            self.send_json(error_messages["unauthorized"])
            return

        self._set_attrs()
        self.join_socket_groups()
        self.send_json({"type": "connected", "message": "hello Svelte!"})

        print(f"hello {self.user.get('username')} your Join code is {self.joincode}")

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
        """authenticate the user"""
        msg = data.get("message")
        token = msg.get("token")

        user = decode_token(token)
        if user.is_anonymous:
            self.close(code=4010)
        else:
            self.scope["user"] = user

        
        if not user.active_team_id:
            self.send_json(error_messages["unauthorized"])
            return

        self._set_attrs()
        self.join_socket_groups()

        print(f"hello {self.user.get('username')} your Join code is {self.joincode}")

    #####################
    ### TEAM MESSAGES ###
    #####################

    def team_update_response(self, data):
        print("updating a response")
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
