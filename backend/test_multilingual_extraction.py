import pytest
from app.services.multilingual_extractor import MultilingualExtractor, MultilingualNumberParser
from app.services.extraction_service import ExtractionService
from app.services.language_registry import LanguageRegistry

def test_language_registry():
    languages = LanguageRegistry.get_supported_languages()
    assert len(languages) == 10
    ids = [l["id"] for l in languages]
    for lang_code in ["ta", "en", "te", "kn", "ml", "hi", "gu", "mr", "bn", "pa"]:
        assert lang_code in ids

def test_multilingual_name_extraction():
    test_cases = [
        ("என் பெயர் குப்புசாமி", "Kuppuswamy"),
        ("My name is Kuppuswamy", "Kuppuswamy"),
        ("मेरा नाम कुप्पुसामी है", "Kuppuswamy"),
        ("నా పేరు కుప్పుసామి", "Kuppuswamy"),
        ("ನನ್ನ ಹೆಸರು ಕುಪ್ಪುಸಾಮಿ", "Kuppuswamy"),
        ("എന്റെ പേര് കുപ്പുസാമി", "Kuppuswamy")
    ]
    for transcript, expected_name in test_cases:
        extracted_name = MultilingualExtractor.extract_name(transcript)
        assert extracted_name == expected_name

def test_multilingual_number_parsing():
    # 45 parsing across Indic languages
    assert MultilingualNumberParser.parse_number("45") == 45
    assert MultilingualNumberParser.parse_number("forty five") == 45
    assert MultilingualNumberParser.parse_number("நாற்பத்தைந்து") == 45
    assert MultilingualNumberParser.parse_number("पैंतालीस") == 45
    assert MultilingualNumberParser.parse_number("నలభై ఐదు") == 45
    assert MultilingualNumberParser.parse_number("ನಲವತ್ತೈದು") == 45
    assert MultilingualNumberParser.parse_number("നാൽപ്പത്തഞ്ച്") == 45

    # 20 parsing across Indic languages
    assert MultilingualNumberParser.parse_number("20") == 20
    assert MultilingualNumberParser.parse_number("twenty") == 20
    assert MultilingualNumberParser.parse_number("இருபது") == 20
    assert MultilingualNumberParser.parse_number("बीस") == 20
    assert MultilingualNumberParser.parse_number("ఇరవై") == 20
    assert MultilingualNumberParser.parse_number("ಇಪ್ಪತ್ತು") == 20
    assert MultilingualNumberParser.parse_number("ഇരുപത്") == 20

def test_multilingual_material_extraction():
    assert MultilingualExtractor.extract_material("தேக்கு மரம்") == "Teak Wood"
    assert MultilingualExtractor.extract_material("Teak Wood Sculpture") == "Teak Wood"
    assert MultilingualExtractor.extract_material("सागौन की लकड़ी") == "Teak Wood"
    assert MultilingualExtractor.extract_material("టేకు చెక్క") == "Teak Wood"
    assert MultilingualExtractor.extract_material("ತೇಗದ ಮರ") == "Teak Wood"
    assert MultilingualExtractor.extract_material("തേക്ക് മരം") == "Teak Wood"

def test_multilingual_correction_parsing():
    assert ExtractionService.parse_correction("Change price to 5000")["new_value"] == 5000.0
    assert ExtractionService.parse_correction("விலையை 5000 ஆக மாற்று")["new_value"] == 5000.0
    assert ExtractionService.parse_correction("कीमत बदलकर 5000 कर दो")["new_value"] == 5000.0
    assert ExtractionService.parse_correction("ధరను 5000 కి మార్చండి")["new_value"] == 5000.0
