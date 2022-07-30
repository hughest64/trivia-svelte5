from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

class SocketConsumer(JsonWebsocketConsumer):
    def connect(self):
        kwargs = self.scope.get("url_route", {}).get("kwargs")
        joincode = kwargs.get("joincode")
        self.event_group = f"event_{joincode}" if joincode else ""

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
        async_to_sync(self.channel_layer.group_send)(
            self.event_group, content
        )

    def connected(self, data):
        self.send_json(data)

    #####################
    ### TEAM MESSAGES ###
    #####################

    def team_update_response(self, data):
        print(data)

    ######################
    ### EVENT MESSAGES ###
    ######################