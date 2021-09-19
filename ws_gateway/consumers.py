import uuid
import threading


from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from ws_gateway.services import WebSocket, thread_is_running, stop_thread
from api_gateway.models import Account


class BitmexConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.group_name = str(uuid.uuid4())
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, event):
        print('disconnect')
        if self.groups:
            self.client.close_connection()
            is_active_thread = thread_is_running(self.group_name)
            if is_active_thread:
                stop_thread(self.group_name)

            # leave the group
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def subscribe_action(self, content_data):
        is_active_thread = thread_is_running(self.group_name)
        if self.account and not is_active_thread and content_data['action'] == 'subscribe':
            self.client = WebSocket(
                self.account.api_key,
                self.account.api_secret,
                content_data['symbol'],
                self.group_name,
                self.account.name
            )
            thread = threading.Thread(target=self.client.get_data)
            thread.name = self.group_name
            thread.start()
        elif self.account and is_active_thread and content_data['action'] == 'subscribe':
            await self.send_json({
                'already': 'running'
            })

    async def unsubscribe_action(self, content_data):
        is_active_thread = thread_is_running(self.group_name)
        if self.account and is_active_thread and content_data['action'] == 'unsubscribe':
            self.client.close_connection()
            stop_thread(self.group_name)
            await self.send_json({
                'success': True
            })

        elif self.account and not is_active_thread and content_data['action'] == 'unsubscribe':
            await self.send_json({
                'nothing': 'to stop'
            })

    async def receive_json(self, content, **kwargs):

        content_data = {
            'account': content.get('account'),
            'action': content.get('action'),
            'symbol': content.get('symbol'),
        }
        missing_content_data = None in content_data.values()
        if missing_content_data:
            missing_values = []
            for k, v in content_data.items():
                if not v:
                    missing_values.append(k)
            await self.send_json({
                'missing': missing_values
            })

        try:
            self.account = await sync_to_async(Account.objects.get)(name=content_data['account'])
        except ObjectDoesNotExist:
            self.account = None
        if not missing_content_data and content_data['action'] == 'subscribe':
            await self.subscribe_action(content_data)
        elif not missing_content_data and content_data['action'] == 'unsubscribe':
            await self.unsubscribe_action(content_data)

    async def auto_update(self, event):
        print('sending df')
        data = event['data']

        await self.send_json({
            'text': data
        })

    async def websocket_ingest(self, event):
        await self.send_json(event)