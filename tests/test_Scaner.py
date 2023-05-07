import unittest
import mock
from ..src.Scaner import get_video_metadata
from pymediainfo import MediaInfo
import os
import tempfile

class TestGetVideoMetadata(unittest.TestCase):

	def setUp(self):
		self.test_video_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
		self.test_video_file.write(b"Dummy video content")
		self.test_video_file.close()

	def tearDown(self):
		os.remove(self.test_video_file.name)

	def test_get_video_metadata_type_error(self):
		with self.assertRaises(TypeError):
			get_video_metadata(123)

	def test_get_video_metadata(self):
		mock_track = mock.MagicMock(
			to_data=mock.MagicMock(return_value={
				"@type": "General", "codecs_video": "AVC",
				"complete_name": self.test_video_file.name,
				"audio_codecs": "AAC", "duration": 1000,
				"file_last_modification_date": "UTC 2023-05-06 00:00:00",
				"file_size": 1024, "unique_id": "123456789"
			})
		)

		with mock.patch('pymediainfo.MediaInfo.parse', return_value=mock.Mock(tracks=[mock_track])):
			result = get_video_metadata(self.test_video_file.name)

		expected_result = {
			"codecs_video": "AVC",
			"complete_name": self.test_video_file.name,
			"audio_codecs": "AAC",
			"duration": 1000,
			"file_last_modification_date": "UTC 2023-05-06 00:00:00",
			"file_size": 1024,
			"unique_id": "123456789"
		}

		self.assertEqual(result, expected_result)

if __name__ == '__main__':
	unittest.main()
