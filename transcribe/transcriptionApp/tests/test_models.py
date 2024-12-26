from django.test import TestCase
from transcriptionApp.models import AudioFile


class AudioFileModelTest(TestCase):
    def test_audio_file_creation(self):
        """
        Test if AudioFile model creates an object correctly.
        """
        audio = AudioFile.objects.create(
            title="Test Audio",
            audio="audio/test_audio.mp3",
        )
        self.assertEqual(audio.title, "Test Audio")
        self.assertEqual(audio.transcription, None)
