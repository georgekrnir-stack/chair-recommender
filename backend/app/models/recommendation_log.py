import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.database import Base


class RecommendationLog(Base):
    __tablename__ = "recommendation_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    form_input = Column(Text)
    parsed_conditions = Column(JSONB)
    recommended_chair_ids = Column(JSONB)
    response_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
