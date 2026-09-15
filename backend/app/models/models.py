import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Artisan(Base):
    __tablename__ = "artisans"

    id = Column(String, primary_key=True, index=True) # e.g. ART-0001
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    preferred_language = Column(String, default="ta") # 'ta' or 'en'
    experience_years = Column(Integer, default=0)
    craft_expertise = Column(String, nullable=True)
    profile_photo_url = Column(Text, nullable=True)
    identity_status = Column(String, default="DEMO_UNVERIFIED")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    sessions = relationship("ConversationSession", back_populates="artisan")
    catalogs = relationship("Catalog", back_populates="artisan")

class ConversationSession(Base):
    __tablename__ = "conversation_sessions"

    id = Column(String, primary_key=True, index=True) # e.g. SES-1001
    artisan_id = Column(String, ForeignKey("artisans.id"), nullable=True)
    current_state = Column(String, default="LANGUAGE_SELECTION")
    language = Column(String, default="ta")
    collected_data = Column(JSON, default={})
    user_corrections = Column(JSON, default=[])
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    artisan = relationship("Artisan", back_populates="sessions")
    messages = relationship("ConversationMessage", back_populates="session")
    artworks = relationship("Artwork", back_populates="session")

class ConversationMessage(Base):
    __tablename__ = "conversation_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("conversation_sessions.id"))
    sender = Column(String) # 'USER', 'ARTA', 'SYSTEM'
    message_text = Column(Text)
    language = Column(String, default="ta")
    audio_url = Column(Text, nullable=True)
    metadata_info = Column(JSON, default={})
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("ConversationSession", back_populates="messages")

class Artwork(Base):
    __tablename__ = "artworks"

    id = Column(String, primary_key=True, index=True) # ARTW-5001
    session_id = Column(String, ForeignKey("conversation_sessions.id"))
    image_url = Column(Text) # Local asset URL or b64
    detected_craft = Column(String, nullable=True)
    detected_material = Column(String, nullable=True)
    detected_complexity = Column(String, nullable=True)
    vision_raw_output = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("ConversationSession", back_populates="artworks")
    catalog = relationship("Catalog", back_populates="artwork", uselist=False)

class Catalog(Base):
    __tablename__ = "catalogs"

    id = Column(String, primary_key=True, index=True) # CAT-8001
    artisan_id = Column(String, ForeignKey("artisans.id"))
    artwork_id = Column(String, ForeignKey("artworks.id"))
    product_name = Column(String)
    craft_category = Column(String)
    subcategory = Column(String, nullable=True)
    primary_material = Column(String)
    secondary_materials = Column(String, nullable=True)
    work_hours = Column(Integer)
    production_days = Column(Integer, nullable=True)
    techniques = Column(Text, nullable=True)
    description = Column(Text)
    cultural_significance = Column(Text, nullable=True)
    intended_use = Column(String, nullable=True)
    price_amount = Column(Float)
    price_currency = Column(String, default="INR")
    status = Column(String, default="DRAFT") # DRAFT, APPROVED, READY_FOR_MARKET
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    artisan = relationship("Artisan", back_populates="catalogs")
    artwork = relationship("Artwork", back_populates="catalog")
    fields = relationship("CatalogField", back_populates="catalog")
    price_estimate = relationship("PriceEstimate", back_populates="catalog", uselist=False)

class CatalogField(Base):
    __tablename__ = "catalog_fields"

    id = Column(Integer, primary_key=True, autoincrement=True)
    catalog_id = Column(String, ForeignKey("catalogs.id"))
    field_name = Column(String) # e.g. 'product_name', 'primary_material', 'work_hours'
    field_value = Column(Text)
    source = Column(String) # ARTISAN, AI_VISION, AI_INFERENCE, AI_GENERATED, SYSTEM
    confidence = Column(Float, default=1.0)
    status = Column(String, default="COLLECTED") # COLLECTED, SUGGESTED, CONFIRMED, REJECTED
    confirmed_by_artisan = Column(Boolean, default=False)

    catalog = relationship("Catalog", back_populates="fields")

class PriceEstimate(Base):
    __tablename__ = "price_estimates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    catalog_id = Column(String, ForeignKey("catalogs.id"))
    suggested_min = Column(Float)
    suggested_max = Column(Float)
    recommended_price = Column(Float)
    final_price = Column(Float)
    factor_breakdown = Column(JSON, default={})
    explanation_ta = Column(Text)
    explanation_en = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    catalog = relationship("Catalog", back_populates="price_estimate")
