import json
from django.test import TestCase
from django.urls import reverse
from channels.testing import WebsocketCommunicator
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chatApp.models import Room, Message
from chatApp.consumers import ChatConsumer
from asgiref.sync import sync_to_async

class ChatAppIntegrationTests(TestCase):
    def setUp(self):
        self.application = ProtocolTypeRouter({
            "websocket": URLRouter([
                path("ws/notification/<str:room_name>/", ChatConsumer.as_asgi()),
            ]),
        })

    async def test_create_room_and_send_message(self):
        """Test creating a room and sending a message."""
        # Create a room
        room_name = 'test_room'
        username = 'test_user'
        await sync_to_async(Room.objects.create)(room_name=room_name)

        # Connect to the WebSocket
        communicator = WebsocketCommunicator(self.application, f"ws/notification/{room_name}/")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        # Send a message
        message_data = {
            'message': 'Hello, world!',
            'room_name': room_name,
            'sender': username
        }
        await communicator.send_json_to(message_data)

        # Receive the message
        response = await communicator.receive_json_from()
        self.assertEqual(response['message']['sender'], username)
        self.assertEqual(response['message']['message'], 'Hello, world!')

        # Check if the message is saved in the database
        room = await sync_to_async(Room.objects.get)(room_name=room_name)
        message = await sync_to_async(Message.objects.get)(room=room)
        self.assertEqual(message.sender, username)
        self.assertEqual(message.message, 'Hello, world!')

        await communicator.disconnect()

    def test_create_room_view(self):
        """Test the CreateRoom view."""
        response = self.client.post(reverse('chatApp:create-room'), {'username': 'test_user', 'room': 'test_room'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Room.objects.filter(room_name='test_room').exists())

    def test_message_view(self):
        """Test the MessageView view."""
        room = Room.objects.create(room_name='test_room')
        Message.objects.create(room=room, sender='test_user', message='Hello, world!')
        response = self.client.get(reverse('chatApp:room', args=['test_room', 'test_user']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chatApp/message.html')
        self.assertIn('messages', response.context)
        self.assertEqual(response.context['messages'].first().message, 'Hello, world!')