from django.test import TestCase
from liveTranscription.forms import SessionForm

class TestSessionForm(TestCase):
    def test_valid_form(self):
        """Test that the form is valid with a proper session name."""
        form_data = {'session_name': 'Valid Session Name'}
        form = SessionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_session_name(self):
        """Test that the form is invalid with an empty session name."""
        form_data = {'session_name': ''}
        form = SessionForm(data=form_data)
        with self.assertRaises(ValueError):
            self.assertFalse(form.is_valid())
        self.assertIn('session_name', form.errors)

    def test_session_name_too_long(self):
        """Test that the form is invalid with a session name longer than 255 characters."""
        form_data = {'session_name': 'a' * 256}
        form = SessionForm(data=form_data)
        with self.assertRaises(ValueError):
            self.assertFalse(form.is_valid())
        self.assertIn('session_name', form.errors)