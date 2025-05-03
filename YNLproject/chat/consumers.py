# # consumers.py
# import json
# from datetime import datetime
# from asgiref.sync import sync_to_async
# from channels.generic.websocket import AsyncWebsocketConsumer
# from django.contrib.auth.models import AnonymousUser
# from .models import Group, GroupMembership, GroupMessage

# class GroupChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.group_id = self.scope['url_route']['kwargs']['group_id']
#         self.group_name = f'group_{self.group_id}'
#         self.user = self.scope['user']
        
#         if isinstance(self.user, AnonymousUser):
#             await self.close()
#             return
        
#         try:
#             self.group = await sync_to_async(Group.objects.get)(id=self.group_id)
#             is_member = await sync_to_async(GroupMembership.objects.filter(
#                 group=self.group, 
#                 user=self.user
#             ).exists)()
            
#             if not is_member:
#                 await self.close()
#                 return
                
#         except Group.DoesNotExist:
#             await self.close()
#             return
        
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         if hasattr(self, 'group_name'):
#             await self.channel_layer.group_discard(
#                 self.group_name,
#                 self.channel_name
#             )

#     async def receive(self, text_data):
#         try:
#             text_data_json = json.loads(text_data)
#             message = text_data_json.get('message')
#             sender = self.user.username
            
#             # Create and save the message
#             group_message = await sync_to_async(GroupMessage.objects.create)(
#                 sender=self.user,
#                 group=self.group,
#                 content=message
#             )
            
#             # Prepare message data to send to group
#             message_data = {
#                 'type': 'chat_message',
#                 'message': message,
#                 'sender': sender,
#                 'timestamp': str(datetime.now()),
#                 'image': text_data_json.get('image'),
#                 'video': text_data_json.get('video'),
#                 'voice_note': text_data_json.get('voice_note')
#             }
            
#             await self.channel_layer.group_send(
#                 self.group_name,
#                 message_data
#             )
            
#         except Exception as e:
#             print(f"Error processing message: {e}")

#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps({
#             'message': event['message'],
#             'sender': event['sender'],
#             'timestamp': event['timestamp'],
#             'image': event['image'],
#             'video': event['video'],
#             'voice_note': event['voice_note']
#         }))

import json
from datetime import datetime
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from .models import Group, GroupMessage

class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group_name = f'group_{self.group_id}'
        self.user = self.scope['user']
        
        if isinstance(self.user, AnonymousUser):
            await self.close()
            return
        
        try:
            self.group = await sync_to_async(Group.objects.get)(id=self.group_id)
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        except Group.DoesNotExist:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            sender = self.user
            
            # Save message to database
            group_message = await sync_to_async(GroupMessage.objects.create)(
                sender=sender,
                group=self.group,
                content=message
            )
            
            # Broadcast to group
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender.username,
                    'timestamp': str(group_message.timestamp)
                }
            )
        except Exception as e:
            print(f"Error: {e}")

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))