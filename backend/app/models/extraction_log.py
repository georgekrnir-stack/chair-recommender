import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class ExtractionLog(Base):
    __tablename__ = "extraction_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    video_id = Column(UUID(as_uuid=True), ForeignKey("videos.id"), nullable=False)
    chair_id = Column(UUID(as_uuid=True), ForeignKey("chairs.id"), nullable=True)
    raw_mention = Column(Text)
    context = Column(Text)
    timestamp_hint = Column(Text)
    confidence = Column(Text)  # high / medium / low
    status = Column(Text, default="unresolved")  # auto_matched / manually_matched / unresolved
    created_at = Column(DateTime, default=datetime.utcnow)
