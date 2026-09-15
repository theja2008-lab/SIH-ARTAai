import pytest
from app.services.pricing_service import PricingService
from app.services.extraction_service import ExtractionService
from app.services.identity_service import IdentityVerificationService

def test_pricing_calculation():
    result = PricingService.calculate_fair_price(
        craft_category="Traditional Wood Craft",
        material="Teak Wood",
        work_hours=20,
        experience_years=25,
        complexity="high"
    )
    assert result["suggested_min"] > 0
    assert result["suggested_max"] > result["suggested_min"]
    assert result["recommended_price"] >= 4000
    assert "20 மணி நேர" in result["explanation_ta"]

def test_extraction_onboarding():
    name_extracted = ExtractionService.extract_onboarding_info("என் பெயர் அருண்", field_target="name")
    assert "name" in name_extracted

    age_extracted = ExtractionService.extract_onboarding_info("எனக்கு 40 வயது", field_target="age")
    assert age_extracted.get("age") == 40

    exp_extracted = ExtractionService.extract_onboarding_info("15 ஆண்டுகள் கைவினை அனுபவம்", field_target="experience_years")
    assert exp_extracted.get("experience_years") == 15

def test_identity_verification():
    result = IdentityVerificationService.process_identity_document("Arun")
    assert result["status"] == "DOCUMENT_ATTACHED"
    assert result["extracted_name"] == "Arun"
