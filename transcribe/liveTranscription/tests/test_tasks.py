import os
from unittest.mock import patch, mock_open
from django.test import TestCase
from liveTranscription.tasks import transcribe_audio_chunk

# class TranscribeAudioChunkTaskTest(TestCase):
#     @patch('liveTranscription.tasks.load_model')
#     @patch('builtins.open', new_callable=mock_open)
#     @patch('os.path.join', return_value='/mocked/path/to/Desktop/test_session.wav')
#     def test_transcribe_audio_chunk_success(self, mock_path_join, mock_open_file, mock_load_model):
#         """Test successful transcription of audio chunk."""
#         mock_model = mock_load_model.return_value
#         mock_model.transcribe.return_value = {'text': 'Transcribed text'}

#         bytes_data = b'fake_audio_data'
#         session_name = 'test_session'
#         result = transcribe_audio_chunk(bytes_data, session_name)

#         mock_path_join.assert_called_once_with(os.path.expanduser("~"), "Desktop", f"{session_name}.wav")
#         mock_open_file.assert_called_once_with('/mocked/path/to/Desktop/test_session.wav', 'ab')
#         mock_model.transcribe.assert_called_once_with('/mocked/path/to/Desktop/test_session.wav', language='en')
#         self.assertEqual(result, 'Transcribed text')

#     @patch('liveTranscription.tasks.load_model')
#     @patch('builtins.open', new_callable=mock_open)
#     @patch('os.path.join', return_value='/mocked/path/to/Desktop/test_session.wav')
#     def test_transcribe_audio_chunk_failure(self, mock_path_join, mock_open_file, mock_load_model):
#         """Test failure during transcription of audio chunk."""
#         mock_model = mock_load_model.return_value
#         mock_model.transcribe.side_effect = Exception('Transcription error')

#         bytes_data = b'fake_audio_data'
#         session_name = 'test_session'

#         with self.assertRaises(Exception) as context:
#             transcribe_audio_chunk(bytes_data, session_name)

#         self.assertIn('Failed to transcribe audio file', str(context.exception))
#         mock_path_join.assert_called_once_with(os.path.expanduser("~"), "Desktop", f"{session_name}.wav")
#         mock_open_file.assert_called_once_with('/mocked/path/to/Desktop/test_session.wav', 'ab')
#         mock_model.transcribe.assert_called_once_with('/mocked/path/to/Desktop/test_session.wav', language='en')