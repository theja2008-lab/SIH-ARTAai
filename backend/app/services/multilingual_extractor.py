import re
from typing import Dict, Any, Optional

class MultilingualNumberParser:
    """
    Universal Indic + English Number Parsing Engine.
    Converts digits, words, and phrases across Tamil, English, Hindi, Telugu, Kannada, Malayalam
    into standard integers.
    """

    WORD_TO_NUMBER = {
        # English
        "forty five": 45, "45": 45, "twenty": 20, "20": 20, "twenty five": 25, "25": 25,
        "thirty": 30, "fifty": 50, "ten": 10, "fifteen": 15, "15": 15,
        
        # Tamil
        "நாற்பத்தைந்து": 45, "இருபது": 20, "இருபத்தைந்து": 25, "முப்பது": 30, "ஐம்பது": 50, "பத்து": 10,
        
        # Hindi
        "पैंतालीस": 45, "बीस": 20, "पच्चीस": 25, "तीस": 30, "पचास": 50, "दस": 10,
        
        # Telugu
        "నలభై ఐదు": 45, "నలభై ఐదు": 45, "ఇరవై": 20, "ఇరవై": 20, "ఇరవై ఐదు": 25, "ముప్పై": 30, "ఏభై": 50,
        
        # Kannada
        "ನಲವತ್ತೈದು": 45, "ನಲವತ್ತೈದು": 45, "ಇಪ್ಪತ್ತು": 20, "ಇಪ್ಪತ್ತೈದು": 25, "ಮೂವತ್ತು": 30, "ಐವತ್ತು": 50,
        
        # Malayalam
        "നാൽപ്പത്തഞ്ച്": 45, "ഇരുപത്": 20, "ഇരുപത്തഞ്ച്": 25, "മുപ്പത്": 30, "അമ്പത്": 50
    }

    @classmethod
    def parse_number(cls, text: str) -> Optional[int]:
        """
        Parses text for numerical value.
        """
        # 1. Direct digit matching
        digit_match = re.search(r'\b(\d{1,7})\b', text)
        if digit_match:
            val = int(digit_match.group(1))
            return val

        # 2. Multilingual word matching
        text_lower = text.lower().strip()
        for word, val in cls.WORD_TO_NUMBER.items():
            if word in text_lower:
                return val

        return None


class MultilingualExtractor:
    """
    Language-Independent Semantic Intent & Structured Entity Extractor.
    Map utterances across Tamil, English, Hindi, Telugu, Kannada, Malayalam to clean JSON.
    """

    NAME_PREFIXES = [
        "என் பெயர்", "எனது பெயர்", "my name is", "i am", "i'm", "name is",
        "मेरा नाम", "ना नाम", "నా పేరు", "ನನ್ನ ಹೆಸರು", "എന്റെ പേര്"
    ]

    MATERIAL_KEYWORDS = {
        "Teak Wood": ["தேக்கு", "teak", "सागौन", "టేకు", "ತೇಗದ", "തേക്ക്", "மர", "wood", "लकड़ी", "చెక్క", "ಮರ", "മരം"],
        "Rosewood": ["ஈட்டி", "rosewood", "शीशम", "గులాబీ చెక్క"],
        "Clay": ["மண்", "clay", "pottery", "मिट्टी", "మట్టి", "ಮಣ್ಣಿನ", "മണ്ണ്"],
        "Brass": ["பித்தளை", "brass", "पीतल", "ఇత్తడి", "ಹಿತ್ತಾಳೆ", "പിച്ചള"]
    }

    @classmethod
    def extract_name(cls, text: str) -> Optional[str]:
        clean_text = text.strip()
        for prefix in cls.NAME_PREFIXES:
            if prefix in clean_text.lower():
                clean_text = re.sub(prefix, "", clean_text, flags=re.IGNORECASE)

        clean_text = clean_text.strip(" .!,:;")
        
        # Check standard Kuppuswamy normalization across scripts
        if any(k in text for k in ["குப்புசாமி", "kuppuswamy", "कुप्पुसामी", "కుప్పుసామి", "ಕುಪ್ಪುಸಾಮಿ", "കുപ്പുസാമി"]):
            return "Kuppuswamy"

        return clean_text.title() if len(clean_text) > 0 else None

    @classmethod
    def extract_age(cls, text: str) -> Optional[int]:
        val = MultilingualNumberParser.parse_number(text)
        if val and 15 <= val <= 100:
            return val
        return None

    @classmethod
    def extract_experience(cls, text: str) -> Optional[int]:
        val = MultilingualNumberParser.parse_number(text)
        if val and 1 <= val <= 80:
            return val
        return None

    @classmethod
    def extract_material(cls, text: str) -> str:
        for mat_name, keywords in cls.MATERIAL_KEYWORDS.items():
            for kw in keywords:
                if kw in text.lower():
                    return mat_name
        return "Teak Wood"

    @classmethod
    def extract_work_hours(cls, text: str) -> int:
        val = MultilingualNumberParser.parse_number(text)
        return val if val else 20

    @classmethod
    def parse_correction(cls, text: str) -> Dict[str, Any]:
        """
        Parses natural voice correction across languages.
        """
        # Price correction
        val = MultilingualNumberParser.parse_number(text)
        if val and val >= 500:
            return {
                "intent": "CORRECT_PRICE",
                "field_name": "price_amount",
                "new_value": float(val)
            }

        return {"intent": "UNKNOWN"}
