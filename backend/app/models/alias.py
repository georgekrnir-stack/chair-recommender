import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class ChairAlias(Base):
    __tablename__ = "chair_aliases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chair_id = Column(UUID(as_uuid=True), ForeignKey("chairs.id"), nullable=False)
    alias = Column(Text, nullable=False)
    source_video_id = Column(UUID(as_uuid=True), ForeignKey("videos.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    chair = relationship("Chair", back_populates="aliases")
