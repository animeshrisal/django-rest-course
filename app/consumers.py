from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json

class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user'].username
        self.room_group_name = "notification_" + self.user
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from room group
    async def notification_message(self, event):
        message = event["message"]
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))