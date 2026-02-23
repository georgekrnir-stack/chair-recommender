import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class MakerProduct(Base):
    __tablename__ = "maker_products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    maker = Column(Text, nullable=False)
    product_name = Column(Text, nullable=False)
    model_number = Column(Text)
    source_url = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class MakerScrapeConfig(Base):
    __tablename__ = "maker_scrape_configs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    maker = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    scrape_method = Column(Text)
    last_scraped_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
