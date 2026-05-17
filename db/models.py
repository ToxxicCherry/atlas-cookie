from sqlalchemy import Column, text, String, Text, DateTime, func, Enum as SQLEnum
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum


Base = declarative_base()

class MarketPlace(enum.Enum):
    wildberries = 'wildberries'
    ozon = 'ozon'

class Cookie(Base):
    __tablename__ = "cookies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    source = Column(SQLEnum(MarketPlace, name="market_place"), nullable=False, default=MarketPlace.wildberries)
    x_wbaas_token = Column(Text, nullable=False)
    user_agent = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())



