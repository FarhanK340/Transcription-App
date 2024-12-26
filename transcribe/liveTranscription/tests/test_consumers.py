import json
from channels.testing import WebsocketCommunicator
from django.test import TestCase
from liveTranscription.consumers import AudioConsumer
from liveTranscription.models import Session, Transcription
from channels.layers import get_channel_layer
from asgiref.testing import ApplicationCommunicator
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from asgiref.sync import sync_to_async

class AudioConsumerTest(TestCase):
    async def test_connect(self):
        """Test WebSocket connection."""
        application = ProtocolTypeRouter({
            "websocket": URLRouter([
                path("ws/audio/<str:session_name>/", AudioConsumer.as_asgi()),
            ]),
        })

        communicator = WebsocketCommunicator(application, "ws/audio/test_session/")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    # async def test_receive_audio_data(self):
    #     """Test receiving audio data and processing transcription."""
    #     session = sync_to_async(Session.objects.create)(session_name="test_session")
    #     application = ProtocolTypeRouter({
    #         "websocket": URLRouter([
    #             path("ws/audio/<str:session_name>/", AudioConsumer.as_asgi()),
    #         ]),
    #     })

    #     communicator = WebsocketCommunicator(application, "ws/audio/test_session/")
    #     connected, subprotocol = await communicator.connect()
    #     self.assertTrue(connected)

    #     # Simulate sending audio data
    #     audio_data = b"fake_audio_data"
    #     await communicator.send_to(bytes_data = audio_data)

    #     # Receive the response
    #     response = await communicator.receive_json_from()
    #     self.assertIn("transcription", response)

    #     # Check if transcription is saved in the database
    #     transcription = Transcription.objects.get(session=session)
    #     self.assertEqual(transcription.transcription, response["transcription"])

    #     await communicator.disconnect()

    async def test_disconnect(self):
        """Test WebSocket disconnection."""
        application = ProtocolTypeRouter({
            "websocket": URLRouter([
                path("ws/audio/<str:session_name>/", AudioConsumer.as_asgi()),
            ]),
        })

        communicator = WebsocketCommunicator(application, "ws/audio/test_session/")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()