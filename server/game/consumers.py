from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync


class SocketConsumer(JsonWebsocketConsumer):
    def connect(self):
        user = self.scope["user"]
        active_team_id = user.active_team_id
        kwargs = self.scope.get("url_route", {}).get("kwargs")
        joincode = kwargs.get("joincode")

        # TODO: helper functions for this would be great so we keep changes consistent
        self.event_group = f"event_{joincode}" if joincode else ""
        # TODO: make this tie to a team an event
        self.team_group = f"team_{active_team_id}" if active_team_id else ""

        print(f"hello {user}, {joincode}, is your Join code and Your active team is {user.active_team_id}")

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

        self.accept()
        async_to_sync(self.channel_layer.send)(
            self.channel_name, {"type": "connected", "message": {"hello": "Svelte!"}}
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.event_group, self.channel_name
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
