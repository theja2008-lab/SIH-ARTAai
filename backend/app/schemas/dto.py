from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class SessionStartRequest(BaseModel):
    language: str = Field(default="ta", description="Language code: 'ta' or 'en'")

class SessionResponse(BaseModel):
    session_id: str
    current_state: str
    language: str
    collected_data: Dict[str, Any]
    arta_message: str
    audio_hint: Optional[str] = None

class VoiceInputRequest(BaseModel):
    session_id: str
    transcript: str
    field_target: Optional[str] = None

class VoiceInputResponse(BaseModel):
    session_id: str
    extracted_data: Dict[str, Any]
    current_state: str
    arta_response: str
    missing_fields: List[str]
    is_complete: bool

class DemoIdentityRequest(BaseModel):
    session_id: str
    document_type: str = "aadhaar_demo"
    image_b64: Optional[str] = None

class DemoIdentityResponse(BaseModel):
    verified: bool
    extracted_name: str
    match_confidence: float
    status: str
    arta_response: str

class ArtworkUploadResponse(BaseModel):
    artwork_id: str
    image_url: str
    detected_craft: str
    detected_material: str
    detected_complexity: str

class CatalogExtractRequest(BaseModel):
    session_id: str
    artwork_id: str
    transcript: str

class CatalogFieldDTO(BaseModel):
    field_name: str
    field_value: str
    source: str # ARTISAN, AI_VISION, AI_INFERENCE, AI_GENERATED
    status: str # SUGGESTED, CONFIRMED, REJECTED
    confirmed_by_artisan: bool = False

class PriceEstimateDTO(BaseModel):
    suggested_min: float
    suggested_max: float
    recommended_price: float
    factor_breakdown: Dict[str, Any]
    explanation_ta: str
    explanation_en: str

class CatalogResponse(BaseModel):
    catalog_id: str
    product_name: str
    craft_category: str
    subcategory: Optional[str] = None
    primary_material: str
    secondary_materials: Optional[str] = None
    work_hours: int
    experience_years: int
    description: str
    cultural_significance: Optional[str] = None
    fields: List[CatalogFieldDTO]
    price_estimate: PriceEstimateDTO
    status: str

class CorrectFieldRequest(BaseModel):
    catalog_id: str
    field_name: str
    new_value: str
    source: str = "ARTISAN"

class ApproveCatalogRequest(BaseModel):
    catalog_id: str
