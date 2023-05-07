import unittest
from ..src.ORM import (
		Base, safe_add_relationship, safe_add_media,
		create_dynamic_filter, AudioCodec, MediaManager
	)

from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestMediaManager(unittest.TestCase):

	def setUp(self):
		engine = create_engine('sqlite://')
		Base.metadata.create_all(engine)

		Session = sessionmaker(bind=engine)
		self.DBSession = Session()

	def tearDown(self):
		self.DBSession.rollback()

	def test_safe_add_relationship(self):
		with self.DBSession.no_autoflush:
			audio_codec = safe_add_relationship(self.DBSession, AudioCodec, name="AC3")
			self.DBSession.flush()

			added_audio_codec = self.DBSession.query(AudioCodec).filter(AudioCodec.name == "AC3").one()
			self.assertEqual(added_audio_codec.name, "AC3")

			existing_audio_codec = safe_add_relationship(self.DBSession, AudioCodec, name="AC3")
			self.assertEqual(existing_audio_codec, added_audio_codec)

			self.DBSession.commit()

	def test_safe_add_media(self):
		safe_add_media(
			audio_codec_name="AC3",
			complete_name="example.mp4",
			duration=3600,
			file_modification_date=date(2023, 1, 1),
			file_size=1024,
			unique_id="unique_id_1",
			video_codec_name="H264",
			DBSession=self.DBSession
		)

		media_entry = self.DBSession.query(MediaManager).filter(MediaManager.unique_id == "unique_id_1").one()
		self.assertEqual(media_entry.complete_name, "example.mp4")

	def test_create_dynamic_filter(self):
		safe_add_media(
			audio_codec_name="AC3",
			complete_name="example.mp4",
			duration=3600,
			file_modification_date=date(2023, 1, 1),
			file_size=1024,
			unique_id="unique_id_1",
			video_codec_name="H264",
			DBSession=self.DBSession
		)
		safe_add_media(
			audio_codec_name="AC3",
			complete_name="example2.mp4",
			duration=3600,
			file_modification_date=date(2023, 1, 1),
			file_size=1024,
			unique_id="unique_id_2",
			video_codec_name="H264",
			DBSession=self.DBSession
		)

		filters = {
			'audio_codec': 'AC3',
			'video_codec': 'H264',
			'file_modification_date': date(2023, 1, 1)
		}

		dynamic_filter = create_dynamic_filter(filters,DBSession=self.DBSession)
		filtered_media = self.DBSession.query(MediaManager).filter(dynamic_filter).all()

		self.assertEqual(len(filtered_media), 2)
		self.assertEqual(set(media_entry.unique_id for media_entry in filtered_media), {"unique_id_1", "unique_id_2"})


if __name__ == '__main__':
	unittest.main()
