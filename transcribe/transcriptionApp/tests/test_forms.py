from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from transcriptionApp.forms import AudioFileForm


class AudioFileFormTest(TestCase):
    def test_valid_form(self):
        """
        Test if the form is valid with correct data.
        """
        form_data = {'title': 'Test Audio'}
        file_data = {
            'audio': SimpleUploadedFile(
                "test_audio.mp3",
                b"file_content",
                content_type="audio/mpeg"
            )
        }
        form = AudioFileForm(data=form_data, files=file_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """
        Test if the form is invalid without required data.
        """
        form = AudioFileForm(data={})
        self.assertFalse(form.is_valid())
