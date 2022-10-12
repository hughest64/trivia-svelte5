from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync


class SocketConsumer(JsonWebsocketConsumer):
    def connect(self):
        kwargs = self.scope.get("url_route", {}).get("kwargs")
        joincode = kwargs.get("joincode")
        self.event_group = f"event_{joincode}" if joincode else ""
        print(f"hello {self.scope['user']}, {joincode}, is your Join code")

        if self.event_group:
            async_to_sync(self.channel_layer.group_add)(
                self.event_group, self.channel_name
            )
        # reject the connection, you've no business here.
        else:
            self.close()

        # TODO: handle setting a team group from the user's active_team_id
        # how to handle changing it or when it's not set?

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
        print(data)
        # do some business logic

        self.send_json(
            {
                "type": "set_store",
                # TODO: I really want a snake_case to camelCase converter and vice versa
                "store": "responseData",
                "message": data.get("message"),
            }
        )

    ######################
    ### EVENT MESSAGES ###
    ######################
