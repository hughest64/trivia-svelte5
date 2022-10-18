from attr import has
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

# TODO: if we end up adding lots of custom methods, it may be nice
# to create a separate class for them and either inherit, or use a mix-in
class SocketConsumer(JsonWebsocketConsumer):
    team_group = "none"
    event_group = "none"

    def _set_attrs(self, data=None):
        """ set useful attributes for use throughout the clss"""
        # self.user
        # self.event_group
        # self.team_group
        # self.user_group

    def authenticate(self, data=None):
        """secondary attempt at authentication if the orignal connection was placed as an anonymous user"""
        # db lookup and if exits, self._set_attrs(data=user) ?
        # self.send_json
        # if still no good self.close(code=4xxx)

    def connect(self):
        # TODO: self.user = UserSerializer(self.scope["user"]) if user.is_authenticated
        user = self.scope["user"]
        kwargs = self.scope.get("url_route", {}).get("kwargs")
        joincode = kwargs.get("joincode")

        self.accept()

        if user.is_anonymous or not user.active_team_id:
            # TODO: instead of closing send a message either asking for credentials (helps in case we have header issues)
            # or have the client redirect to /team (helps if user is_authenticated, but doesn't have an active_team_id)
            self.close(code=4008)
            # - send a message asking for credentials
            # - update if validated
            # - close if not
            return

        active_team_id = user.active_team_id
        # TODO: helper functions for this would be great so we keep changes consistent
        self.event_group = f"event_{joincode}"
        # TODO: make this tie to a team an event
        self.team_group = f"team_{active_team_id}"

        print(
            f"hello {user}, {joincode}, is your Join code and Your active team is {active_team_id}"
        )

        if self.event_group and self.team_group:
            # trivia event group
            async_to_sync(self.channel_layer.group_add)(
                self.event_group, self.channel_name
            )
            # team group
            async_to_sync(self.channel_layer.group_add)(
                self.team_group, self.channel_name
            )
            # individual group (used mostly for host comms with a single player)
            async_to_sync(self.channel_layer.group_add)(
                f"user_{user.id}", self.channel_name
            )

        # reject the connection, you've no business here.
        else:
            self.close()

        async_to_sync(self.channel_layer.send)(
            self.channel_name, {"type": "connected", "message": {"hello": "Svelte!"}}
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.event_group, self.channel_name
        )
        async_to_sync(self.channel_layer.group_discard)(
            self.team_group, self.channel_name
        )
        async_to_sync(self.channel_layer.group_discard)(
            f"user_{self.scope['user'].id}", self.channel_name
        )

    def receive_json(self, content):
        # print(content)
        # TODO: response updates need to route through a team group, not the event!
        async_to_sync(self.channel_layer.group_send)(self.event_group, content)

    def connected(self, data):
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

    # if we do the db work in a view function and use the socket to update all clients:
    def update_round_locks(self, data):
        data.update({"type": "update_store"})
        self.send_json(data)

    #####################
    ### TEAM MESSAGES ###
    #####################

    def team_update_response(self, data):
        self.send_json(data)

    ######################
    ### EVENT MESSAGES ###
    ######################
