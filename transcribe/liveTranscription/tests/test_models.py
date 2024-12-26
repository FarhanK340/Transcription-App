from django.test import TestCase
from liveTranscription.models import Session

from django.test import TestCase
from liveTranscription.models import Session, Transcription

class TestSessionModel(TestCase):
    def test_session_creation(self):
        """Test creating a Session instance."""
        session = Session.objects.create(session_name="Test Session")
        self.assertEqual(session.session_name, "Test Session")
        self.assertIsNotNone(session.created_at)

    def test_session_str_method(self):
        """Test the string representation of a Session."""
        session = Session.objects.create(session_name="Test Session")
        self.assertEqual(str(session), "Test Session")

    # check that session is created with a name of length 1
    def test_session_name_length_1(self):
        """Test the creation of a Session with a name of length 1."""
        session = Session.objects.create(session_name="a")
        self.assertEqual(session.session_name, "a")


    # check that session is created with a name of length 10
    def test_session_name_length_10(self):
        """Test the creation of a Session with a name of length 10."""
        session = Session.objects.create(session_name="a" * 10)
        self.assertEqual(session.session_name, "a" * 10)

    
    # check that session is created with a name of length 255
    def test_session_name_length_255(self):
        """Test the creation of a Session with a name of length 255."""
        session = Session.objects.create(session_name="a" * 255)
        self.assertEqual(session.session_name, "a" * 255)


    # check that session is not created with a name of length 256
    def test_session_name_length_256(self):
        """Test that a session is not created with a name of length 256."""
        with self.assertRaises(ValueError):
            Session.objects.create(session_name="a" * 256)


    # check that session is not created with an empty name
    def test_session_empty_name(self):
        """Test that a session is not created with an empty name"""
        with self.assertRaises(ValueError):
            Session.objects.create(session_name="")


class TestTranscriptionModel(TestCase):
    def setUp(self):
        """Set up a session for testing Transcription model."""
        self.session = Session.objects.create(session_name="Test Session")

    def test_transcription_creation(self):
        """Test creating a Transcription instance."""
        transcription = Transcription.objects.create(
            session=self.session,
            transcription="This is a test transcription."
        )
        self.assertEqual(transcription.transcription, "This is a test transcription.")
        self.assertEqual(transcription.session, self.session)

    def test_transcription_null_and_blank(self):
        """Test handling of null and blank transcription fields."""
        transcription = Transcription.objects.create(
            session=self.session,
            transcription=None  # This should be allowed since null=True, blank=True
        )
        self.assertIsNone(transcription.transcription)

    def test_transcription_str_method(self):
        """Test the string representation of a Transcription."""
        transcription = Transcription.objects.create(
            session=self.session,
            transcription="Test Transcription"
        )
        self.assertEqual(str(transcription), "Test Transcription")
