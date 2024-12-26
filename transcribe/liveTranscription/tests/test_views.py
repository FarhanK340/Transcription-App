from django.test import TestCase
from django.urls import reverse
from liveTranscription.models import Session, Transcription

class CreateSessionViewTest(TestCase):
    def test_create_session_get(self):
        """Test GET request to CreateSession view."""
        response = self.client.get(reverse('liveTranscription:create-session'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'liveTranscription/index.html')
        self.assertIn('form', response.context)

    def test_create_session_post_valid(self):
        """Test POST request to CreateSession view with valid data."""
        response = self.client.post(reverse('liveTranscription:create-session'), {'session_name': 'Test Session'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Session.objects.filter(session_name='Test_Session').exists())
        self.assertRedirects(response, reverse('liveTranscription:session', args=['Test_Session']))

    def test_create_session_post_invalid(self):
        """Test POST request to CreateSession view with invalid data."""
        with self.assertRaises(ValueError):
            response = self.client.post(reverse('liveTranscription:create-session'), {'session_name': ''})
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'liveTranscription/index.html')
            self.assertIn('form', response.context)
            self.assertFalse(Session.objects.exists())

    def test_create_session_post_duplicate(self):
        """Test POST request to CreateSession view with duplicate session name."""
        Session.objects.create(session_name='Test_Session')
        response = self.client.post(reverse('liveTranscription:create-session'), {'session_name': 'Test Session'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Session.objects.filter(session_name='Test_Session').count(), 1)
        self.assertRedirects(response, reverse('liveTranscription:session', args=['Test_Session']))

class TranscriptionViewTest(TestCase):
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

    # def test_transcription_view_nonexistent_session(self):
    #     """Test TranscriptionView with a nonexistent session."""
    #     response = self.client.get(reverse('liveTranscription:session', args=['Nonexistent_Session']))
    #     self.assertEqual(response.status_code, 404)

    def test_transcription_view_context(self):
        """Test TranscriptionView context data."""
        session = Session.objects.create(session_name='Test_Session')
        Transcription.objects.create(session=session, transcription='Test transcription')
        response = self.client.get(reverse('liveTranscription:session', args=['Test_Session']))
        self.assertEqual(response.context['session_name'], 'Test_Session')
        self.assertEqual(response.context['transcription'], 'Test transcription')