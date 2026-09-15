import re
from typing import Dict, Any, List, Optional
from app.services.multilingual_extractor import MultilingualExtractor, MultilingualNumberParser

class ExtractionService:
    """
    Structured Voice & Text Information Extraction Engine.
    Leverages language-independent semantic intent extraction for profile data,
    catalog attributes, missing field detection, and user corrections across Indic & English languages.
    """

    REQUIRED_CATALOG_FIELDS = [
        "product_name",
        "craft_category",
        "primary_material",
        "work_hours"
    ]

    @classmethod
    def extract_onboarding_info(cls, transcript: str, field_target: str = None) -> Dict[str, Any]:
        """
        Extracts onboarding fields (name, age, experience, expertise) from voice transcripts across languages.
        """
        text = transcript.strip()
        extracted = {}

        if field_target == "name":
            name_val = MultilingualExtractor.extract_name(text)
            if name_val:
                extracted["name"] = name_val
            return extracted

        if field_target == "age":
            age_val = MultilingualExtractor.extract_age(text)
            if age_val:
                extracted["age"] = age_val
            return extracted

        if field_target == "experience_years":
            exp_val = MultilingualExtractor.extract_experience(text)
            if exp_val:
                extracted["experience_years"] = exp_val
            return extracted

        # Fallback multi-field extraction
        name_val = MultilingualExtractor.extract_name(text)
        if name_val:
            extracted["name"] = name_val

        age_val = MultilingualExtractor.extract_age(text)
        if age_val:
            extracted["age"] = age_val

        exp_val = MultilingualExtractor.extract_experience(text)
        if exp_val:
            extracted["experience_years"] = exp_val

        mat = MultilingualExtractor.extract_material(text)
        if mat:
            extracted["craft_expertise"] = f"Traditional {mat} Craft"
            extracted["primary_material"] = mat

        return extracted

    @classmethod
    def extract_catalog_info(cls, transcript: str, vision_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Extracts product attributes (work hours, material, craft name, description) from artisan voice story.
        """
        text = transcript.strip()
        extracted = {}

        hours_val = MultilingualExtractor.extract_work_hours(text)
        extracted["work_hours"] = hours_val if hours_val else 20

        extracted["primary_material"] = MultilingualExtractor.extract_material(text)
        extracted["craft_category"] = "Traditional Wood Craft"
        extracted["subcategory"] = "Wood Sculpture"
        extracted["product_name"] = f"Handcarved {extracted['primary_material']} Sculpture"

        extracted["description"] = (
            f"Hand-crafted traditional product made from premium {extracted['primary_material']}. "
            f"Requires {extracted['work_hours']} hours of intricate hand work by master artisan."
        )

        extracted["cultural_significance"] = (
            "Reflects heritage woodworking traditions passed down over generations."
        )

        return extracted

    @classmethod
    def detect_missing_fields(cls, catalog_data: Dict[str, Any]) -> List[str]:
        missing = []
        for field in cls.REQUIRED_CATALOG_FIELDS:
            val = catalog_data.get(field)
            if val is None or val == "":
                missing.append(field)
        return missing

    @classmethod
    def parse_correction(cls, transcript: str) -> Dict[str, Any]:
        """
        Parses natural voice correction commands across supported languages.
        """
        return MultilingualExtractor.parse_correction(transcript)
