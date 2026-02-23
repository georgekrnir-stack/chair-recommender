import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    youtube_video_id = Column(Text, unique=True, nullable=False)
    title = Column(Text)
    published_at = Column(DateTime)
    url = Column(Text)
    status = Column(Text, default="pending")  # pending / transcribed / extracted / reviewed
    transcript = Column(Text)
    transcript_source = Column(Text)  # youtube_caption / whisper
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
