from attr import has
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

from user.serializers import UserSerializer

# TODO: if we end up adding lots of custom methods, it may be nice
# to create a separate class for them and either inherit, or use a mix-in
class SocketConsumer(JsonWebsocketConsumer):
    def _set_attrs(self, data=None):
        """set useful attributes for use throughout the clss"""
        user = data or self.scope["user"]
        kwargs = self.scope.get("url_route", {}).get("kwargs")

        self.user = UserSerializer(user).data
        self.joincode = kwargs.get("joincode")
        self.event_group = f"event_{self.joincode}"
        self.team_group = f"team_{user.active_team_id}"
        self.user_group = f"user_id_{user.id}"

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
        self.accept()

        if user.is_anonymous:
            self.send_json(
                {"type": "unauthenticated ", "message": "You need to log in"}
            )
            return

        if not user.active_team_id:
            self.send_json(
                {
                    "type": "unauthorized",
                    "message": "You must be on a team to to play trivia",
                }
            )
            return

        self._set_attrs()
        self.join_socket_groups()
        self.send_json({"type": "connected", "message": "hello Svelte!"})

        print(f"hello {self.user.get('username')} your Join code is {self.joincode}")

    def disconnect(self, close_code):
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
        print('content received')
        # print(content)
        if content.get("type") == "user_authenticate":
            self.user_authenticate(content)

    #####################
    ### USER MESSAGES ###
    #####################

    def user_authenticate(self, data):
        """secondary attempt at authentication if the orignal connection was placed as an anonymous user"""
        print(data)
        # db lookup and if exits, self._set_attrs(data=user) ?
        # TODO: in the case of data being passed, should be try to set it in the scope?
        # self.send_json
        # if still no good self.close(code=4xxx)

    # if we do the db work in a view function and use the socket to update all clients:
    def update_round_locks(self, data):
        data.update({"type": "update_store"})
        self.send_json(data)

    #####################
    ### TEAM MESSAGES ###
    #####################

    def team_update_response(self, data):
        print("updating a response")
        self.send_json(data)

    ######################
    ### EVENT MESSAGES ###
    ######################

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
