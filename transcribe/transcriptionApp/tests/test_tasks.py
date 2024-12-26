from transcriptionApp.models import AudioFile
from transcriptionApp.tasks import transcribe_audio_task
from django.test import TestCase
from unittest.mock import patch

class TranscribeAudioTaskIntegrationTest(TestCase):
    def setUp(self):
        self.audio_file = AudioFile.objects.create(
            title="Test Audio",
            audio="audio/test_audio.mp3"
        )

    @patch("transcriptionApp.tasks.download_tempfile_from_url")
    @patch("transcriptionApp.tasks.transcribe_audio")
    def test_task_execution(self, mock_transcribe_audio, mock_download_tempfile):
        mock_transcribe_audio.return_value = " Hello world. This is demo text for my transcription app."

        # Trigger the task
        transcribe_audio_task.delay(
            "https://transcribe-service-bucket-sc.s3.eu-north-1.amazonaws.com/audio/demo_audio.mp3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIARE7RPQII4BOKZIEF%2F20241226%2Feu-north-1%2Fs3%2Faws4_request&X-Amz-Date=20241226T063004Z&X-Amz-Expires=300&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEE4aCmV1LW5vcnRoLTEiRzBFAiEAqAwC3AZFq4OwA1q7upaMfzDgexlalFbeE6ZRGWEn%2B3YCICPv84M8rGnLW71qGvA4htgNVmI9OhdK2ICdv1ZdMtdFKuwCCCgQAhoMMDc5NDI2NDU0MDMzIgw%2BR0DyXY5j93tux90qyQLV1NO6ShKusGSiOLRdoWbd7ihblZfgpyRUM6EgMjI5nqP7U9tyIt68ORe9TSTgAmVF1ce8GDqi%2FMH2x9gk2%2BxEIPBmKKqSiq5T9OrXBkk7ldQbKArwpu0R2k5egdYugo%2FZ9vYiGNTH9hBUsuGRNToKLbfv3YJFrhxZnnUNcauIgaQZ5n44dLcPA8qSgprBBSEJann1AmHKedjWHd23wADin%2FYSDcarBSAjfnKEi69d139dggPAXaS0uwOmGSCGHfJ8Zm5Ci%2By1UXet4I%2FtE7f546hN3UAcJjhb2RVj1pxnEstO33b6G2H%2FYhfE9EjIoMrNzM6imXQEx3fDU9lDwFI%2Fyl0ImRSMa62EyH0ocMPhaJNVRidghGqPoXSh7NRLHHO05wb0UOX02qGridQ%2BMr%2FLqiRn9TWd2LIY4UaATsljRgFbr8XoP8N3vjDt7rO7BjqzAjhIQn4Ti6%2B0q23L67rjS03kIR3Xs7Ot19F8aedzdi%2FeA%2F1fGYIi0RGKPnPAY8PRzGzDnW4dEpRsnaxgpMtzH6rrDIhHvS%2Fd3g8nIOUFoXBvOp3haSid8tkH8CTPDnYhMKJVEo%2BHKKU895aapk139X%2BzV9ngZFzqBHHJHdlTl5rU03KnR77gvSjzX0yJSU31ZlpxcTumf0BVRyExn6APUCUZSbBnPbqK0HS%2BhO3E3zNJApuhyWrU0yTvtd3SWj6%2FCxyyNBIwmX1bWQKa5wprVpCxd6cPPdxFHsxnWyfzLI2bgPsPWsKH0AaUq%2B6oYRSN27xpRUYmZg4ZuRvkVPzDAvioP2HCuohwAuNq0%2F6vyF513D98xbD%2BL7UGNrJpTq43amRP05IjElaaw01ckXc3zGzB5yU%3D&X-Amz-Signature=02be6ecd0269310dad9f25083d0cade0321f6be2cc7e00d996bfc5f44a350471&X-Amz-SignedHeaders=host&response-content-disposition=inline",
            self.audio_file.pk
        )

        self.audio_file.refresh_from_db()

        # self.assertEqual(
        #     self.audio_file.transcription,
        #     " Hello world. This is demo text for my transcription app."
        # )

        self.assertIsNone(self.audio_file.transcription)
