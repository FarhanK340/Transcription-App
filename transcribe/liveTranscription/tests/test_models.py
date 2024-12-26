from django.test import TestCase
from liveTranscription.models import Session

class TestLiveTranscriptionAppModels(TestCase):
    # test that session is created
    def test_session_is_created(self):
        session = Session.objects.create(session_name = "new_session")
        self.assertEqual(session.session_name, "new_session")