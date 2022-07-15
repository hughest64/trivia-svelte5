from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

# TODO: reconfigure
class SocketConsumer(JsonWebsocketConsumer):
    def connect(self):
        print(self.scope.get("user", "no user found"))
        print(self.scope.get("url_route", {}).get("kwargs"))
        self.accept()

        async_to_sync(self.channel_layer.send)(self.channel_name, {
            "type": "connected",
            "message": { }
        })
        # self.close(code=69)
    
    def receive_json(self, content):
        # print(content)
        pass

    def connected(self, data):
        self.send_json(data)