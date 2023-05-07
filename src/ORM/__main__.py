from datetime import date
from sqlalchemy import Column, func, ForeignKey, and_, or_
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.declarative import declared_attr

Base = declarative_base()

class BaseColumns:
  id     = Column(Integer, primary_key=True, autoincrement=True)
  added_time = Column(DateTime, default=func.current_timestamp())
  @declared_attr
  def name(cls):
    return Column(String(length=cls.name_length), unique=True)

class VideoCodec(BaseColumns, Base):
  __tablename__ = 'video_codecs'
  name_length = 8


class AudioCodec(BaseColumns, Base):
  __tablename__ = 'audio_codecs'
  name_length = 16

class FileModificationDate(BaseColumns, Base):
  __tablename__ = 'file_modification_dates'
  name_length = None  # No name column needed

class MediaManager(Base):
  __tablename__ = "media_manager"

  name_length = None  # No name column needed
  
  id = Column(Integer, primary_key=True, autoincrement=True)
  complete_name = Column(String(1024))
  duration = Column(Integer)
  file_size = Column(Integer)
  unique_id = Column(String(40))
  added_time = Column(DateTime, default=func.now())
  updated_time     = Column(DateTime, default=func.now(), onupdate=func.now())

  audio_codecs_id = Column(Integer, ForeignKey("audio_codecs.id"))
  audio_codec = relationship("AudioCodec", backref="media_manager")
  
  codecs_video_id = Column(Integer, ForeignKey("video_codecs.id"))
  video_codec = relationship("VideoCodec", backref="media_manager")

  file_last_modification_date_id = Column(Integer, ForeignKey("file_modification_dates.id"))
  file_modification_date = relationship("FileModificationDate", backref="media_manager")
  

def safe_add_relationship(DBSession, model, **kwargs):
  instance = DBSession.query(model).filter_by(**kwargs).first()
  if not instance:
    instance = model(**kwargs)
    DBSession.add(instance)
  return instance

def safe_add_media(
    audio_codec_name: str,
    complete_name: str,
    duration: int,
    file_modification_date: date,
    file_size: int,
    unique_id: str,
    video_codec_name: str,
    DBSession
  ):
  
  audio_codec       = safe_add_relationship(DBSession=DBSession, model=AudioCodec, name=audio_codec_name)
  video_codec       = safe_add_relationship(DBSession=DBSession, model=VideoCodec, name=video_codec_name)
  file_modification = safe_add_relationship(DBSession=DBSession, model=FileModificationDate, name=file_modification_date)

  media_manager = MediaManager(
    audio_codec=audio_codec,
    video_codec=video_codec,
    complete_name=complete_name,
    duration=duration,
    file_size=file_size,
    unique_id=unique_id,
    file_modification_date=file_modification
  )

  DBSession.add(media_manager)
  DBSession.commit()

def create_dynamic_filter(filters: dict, DBSession):
    conditions = []
    
    cls_mapping = {
        'audio_codec': (AudioCodec, MediaManager.audio_codecs_id),
        'video_codec': (VideoCodec, MediaManager.codecs_video_id),
        'file_modification_date': (FileModificationDate, MediaManager.file_last_modification_date_id)
    }    
    for key, values in filters.items():
        if type(values) in (str, int, date):
            values = (values,)
        
        relationship_cls, user_id_mapping = cls_mapping.get(key, (None, None))
        relationship_ids = [
            relationship.id for relationship in
            DBSession.query(relationship_cls.id).filter(relationship_cls.name.in_(set(values)))
        ]
        
        conditions.append(user_id_mapping.in_(relationship_ids))
    
    return and_(*conditions)



# dynamic_filter = create_dynamic_filter(filters)
# result = DBSession.query(User).filter(dynamic_filter).all()
# for user in result:
#   print(user.id, user.name.name, user.age.age)