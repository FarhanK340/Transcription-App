import json
from django.test import TestCase
from django.urls import reverse
from channels.testing import WebsocketCommunicator
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from liveTranscription.models import Session, Transcription
from liveTranscription.consumers import AudioConsumer
from asgiref.sync import sync_to_async

class LiveTranscriptionIntegrationTests(TestCase):
    def setUp(self):
        self.application = ProtocolTypeRouter({
            "websocket": URLRouter([
                path("ws/<str:session_name>/", AudioConsumer.as_asgi()),
            ]),
        })

    # async def test_create_session_and_transcription(self):
    #     """Test creating a session and transcribing audio."""
    #     # Create a session
    #     session_name = 'test_session'
    #     await sync_to_async(Session.objects.create)(session_name=session_name)

    #     # Connect to the WebSocket
    #     communicator = WebsocketCommunicator(self.application, f"ws/{session_name}/")
    #     connected, subprotocol = await communicator.connect()
    #     self.assertTrue(connected)

    #     # Simulate sending audio data
    #     audio_data = b"fake_audio_data"
    #     await communicator.send_bytes(audio_data)

    #     # Receive the response
    #     response = await communicator.receive_json_from()
    #     self.assertIn("transcription", response)

    #     # Check if the transcription is saved in the database
    #     session = await sync_to_async(Session.objects.get)(session_name=session_name)
    #     transcription = await sync_to_async(Transcription.objects.get)(session=session)
    #     self.assertEqual(transcription.transcription, response["transcription"])

    #     await communicator.disconnect()

    def test_create_session_view(self):
        """Test the CreateSession view."""
        response = self.client.post(reverse('liveTranscription:create-session'), {'session_name': 'Test Session'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Session.objects.filter(session_name='Test_Session').exists())

    def test_transcription_view_existing_session_with_transcription(self):
        """Test TranscriptionView with an existing session and transcription."""
        session = Session.objects.create(session_name='Test_Session')
        Transcription.objects.create(session=session, transcription='Test transcription')
        response = self.client.get(reverse('liveTranscription:session', args=['Test_Session']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'liveTranscription/session.html')
        self.assertIn('transcription', response.context)
        self.assertEqual(response.context['transcription'], 'Test transcription')

    def test_transcription_view_existing_session_no_transcription(self):
        """Test TranscriptionView with an existing session but no transcription."""
        session = Session.objects.create(session_name='Test_Session')
        response = self.client.get(reverse('liveTranscription:session', args=['Test_Session']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'liveTranscription/session.html')
        self.assertIn('transcription', response.context)
        self.assertEqual(response.context['transcription'], '')

