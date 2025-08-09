import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Note, NoteVersion

class NoteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.note_id = self.scope['url_route']['kwargs']['note_id']
        self.room_group_name = f'note_{self.note_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data['type']

        if message_type == 'note_update':
            await self.save_note_content(data['content'])
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'note_update',
                    'content': data['content'],
                    'user': self.scope['user'].username
                }
            )

    async def note_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'note_update',
            'content': event['content'],
            'user': event['user']
        }))

    @database_sync_to_async
    def save_note_content(self, content):
        try:
            note = Note.objects.get(id=self.note_id)
            note.content = content
            note.save()
            
            # Save version
            NoteVersion.objects.create(
                note=note,
                content=content,
                user=self.scope['user']
            )
        except Note.DoesNotExist:
            pass