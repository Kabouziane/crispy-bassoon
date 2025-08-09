import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Note, NoteVersion

class NoteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.note_id = self.scope['url_route']['kwargs']['note_id']
        self.room_group_name = f'note_{self.note_id}'
        
        # Accept connection without auth check for now
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        # Send confirmation
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'note_id': self.note_id
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'note_update':
                content = data.get('content', '')
                user_id = data.get('user_id', 1)  # Default user for testing
                
                # Save to database
                await self.save_note_content(content, user_id)
                
                # Broadcast to all clients in the room
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'note_update_broadcast',
                        'content': content,
                        'user_id': user_id,
                        'sender_channel': self.channel_name
                    }
                )
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': str(e)
            }))

    async def note_update_broadcast(self, event):
        # Don't send back to sender
        if event.get('sender_channel') != self.channel_name:
            await self.send(text_data=json.dumps({
                'type': 'note_update',
                'content': event['content'],
                'user_id': event['user_id']
            }))

    @database_sync_to_async
    def save_note_content(self, content, user_id):
        try:
            note = Note.objects.get(id=self.note_id)
            note.content = content
            note.save()
            
            # Save version
            user = User.objects.get(id=user_id)
            NoteVersion.objects.create(
                note=note,
                content=content,
                user=user
            )
        except (Note.DoesNotExist, User.DoesNotExist):
            pass