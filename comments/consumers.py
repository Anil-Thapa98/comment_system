from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
    
    async def notify(self, event):
        await self.send(text_data=json.dumps(event))
