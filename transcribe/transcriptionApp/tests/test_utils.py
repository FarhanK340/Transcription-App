import os, tempfile
from django.test import TestCase
from unittest.mock import patch
from transcriptionApp.utils import download_tempfile_from_url, split_large_audio


class UtilsTest(TestCase):
    @patch("requests.get")
    def test_download_tempfile_from_url(self, mock_get):
        """
        Test the download_tempfile_from_url function.
        """
        mock_response = mock_get.return_value
        mock_response.status_code = 200

        file_path = download_tempfile_from_url("https://transcribe-service-bucket-sc.s3.eu-north-1.amazonaws.com/audio/demo_audio.mp3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIARE7RPQII4BOKZIEF%2F20241226%2Feu-north-1%2Fs3%2Faws4_request&X-Amz-Date=20241226T063004Z&X-Amz-Expires=300&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEE4aCmV1LW5vcnRoLTEiRzBFAiEAqAwC3AZFq4OwA1q7upaMfzDgexlalFbeE6ZRGWEn%2B3YCICPv84M8rGnLW71qGvA4htgNVmI9OhdK2ICdv1ZdMtdFKuwCCCgQAhoMMDc5NDI2NDU0MDMzIgw%2BR0DyXY5j93tux90qyQLV1NO6ShKusGSiOLRdoWbd7ihblZfgpyRUM6EgMjI5nqP7U9tyIt68ORe9TSTgAmVF1ce8GDqi%2FMH2x9gk2%2BxEIPBmKKqSiq5T9OrXBkk7ldQbKArwpu0R2k5egdYugo%2FZ9vYiGNTH9hBUsuGRNToKLbfv3YJFrhxZnnUNcauIgaQZ5n44dLcPA8qSgprBBSEJann1AmHKedjWHd23wADin%2FYSDcarBSAjfnKEi69d139dggPAXaS0uwOmGSCGHfJ8Zm5Ci%2By1UXet4I%2FtE7f546hN3UAcJjhb2RVj1pxnEstO33b6G2H%2FYhfE9EjIoMrNzM6imXQEx3fDU9lDwFI%2Fyl0ImRSMa62EyH0ocMPhaJNVRidghGqPoXSh7NRLHHO05wb0UOX02qGridQ%2BMr%2FLqiRn9TWd2LIY4UaATsljRgFbr8XoP8N3vjDt7rO7BjqzAjhIQn4Ti6%2B0q23L67rjS03kIR3Xs7Ot19F8aedzdi%2FeA%2F1fGYIi0RGKPnPAY8PRzGzDnW4dEpRsnaxgpMtzH6rrDIhHvS%2Fd3g8nIOUFoXBvOp3haSid8tkH8CTPDnYhMKJVEo%2BHKKU895aapk139X%2BzV9ngZFzqBHHJHdlTl5rU03KnR77gvSjzX0yJSU31ZlpxcTumf0BVRyExn6APUCUZSbBnPbqK0HS%2BhO3E3zNJApuhyWrU0yTvtd3SWj6%2FCxyyNBIwmX1bWQKa5wprVpCxd6cPPdxFHsxnWyfzLI2bgPsPWsKH0AaUq%2B6oYRSN27xpRUYmZg4ZuRvkVPzDAvioP2HCuohwAuNq0%2F6vyF513D98xbD%2BL7UGNrJpTq43amRP05IjElaaw01ckXc3zGzB5yU%3D&X-Amz-Signature=02be6ecd0269310dad9f25083d0cade0321f6be2cc7e00d996bfc5f44a350471&X-Amz-SignedHeaders=host&response-content-disposition=inline")
        
        self.assertTrue(os.path.exists(file_path))

        self.assertTrue(file_path.startswith(tempfile.gettempdir()))

        os.remove(file_path)

    @patch("transcriptionApp.utils.AudioSegment.from_file")
    def test_split_large_audio(self, mock_audio_segment):
        """
        Test the split_large_audio function.
        """
        mock_audio = mock_audio_segment.return_value
        mock_audio.frame_rate = 44100
        mock_audio.frame_width = 2
        mock_audio.__len__.return_value = 10000

        chunks = split_large_audio("transcribe/demo audio.mp3", max_size_mb=1)
        self.assertGreater(len(chunks), 0)
