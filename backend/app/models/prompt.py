import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(Text, unique=True, nullable=False)
    name = Column(Text, nullable=False)
    description = Column(Text)
    content = Column(Text, nullable=False)
    version = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    versions = relationship("PromptVersion", back_populates="prompt", cascade="all, delete-orphan")


class PromptVersion(Base):
    __tablename__ = "prompt_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prompt_id = Column(UUID(as_uuid=True), ForeignKey("prompts.id"), nullable=False)
    version = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    prompt = relationship("Prompt", back_populates="versions")
