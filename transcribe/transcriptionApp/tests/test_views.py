from django.test import TestCase, Client
from django.urls import reverse
from transcriptionApp.models import AudioFile


class AudioFileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.audio_file = AudioFile.objects.create(
            title="Test Audio",
            audio="audio/test_audio.mp3"
        )

    def test_upload_audio_view_get(self):
        """
        Test the upload_audio view for GET request.
        """
        response = self.client.get(reverse('transcriptionApp:upload_audio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transcriptionApp/upload.html')

    def test_view_transcription_ajax(self):
        """
        Test the view_transcription view for AJAX request.
        """
        response = self.client.get(
            reverse('transcriptionApp:transcription', args=[self.audio_file.pk]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), 'Transcribing the Audio')
