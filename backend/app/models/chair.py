import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Chair(Base):
    __tablename__ = "chairs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    canonical_name = Column(Text, nullable=False)
    maker = Column(Text)
    model_number = Column(Text)
    price_range = Column(Text)
    features = Column(JSONB, default=list)
    target_users = Column(JSONB, default=list)
    pros = Column(JSONB, default=list)
    cons = Column(JSONB, default=list)
    comparison_notes = Column(Text)
    is_recommendable = Column(Boolean, default=False)
    source_video_ids = Column(JSONB, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    aliases = relationship("ChairAlias", back_populates="chair", cascade="all, delete-orphan")
