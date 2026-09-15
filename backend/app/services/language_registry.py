from typing import Dict, Any, List

class LanguageRegistry:
    """
    Centralized Multilingual Language Registry for ARTINO Platform.
    Defines 10 Indic and global languages, native script names, BCP 47 locales,
    and capability classifications (REAL, PARTIAL, FUTURE).
    """

    LANGUAGES = {
        "ta": {
            "id": "ta",
            "name": "தமிழ்",
            "english_name": "Tamil",
            "locale": "ta-IN",
            "stt_status": "REAL",
            "tts_status": "REAL",
            "ai_status": "REAL"
        },
        "en": {
            "id": "en",
            "name": "English",
            "english_name": "English",
            "locale": "en-IN",
            "stt_status": "REAL",
            "tts_status": "REAL",
            "ai_status": "REAL"
        },
        "te": {
            "id": "te",
            "name": "తెలుగు",
            "english_name": "Telugu",
            "locale": "te-IN",
            "stt_status": "REAL",
            "tts_status": "REAL",
            "ai_status": "REAL"
        },
        "kn": {
            "id": "kn",
            "name": "ಕನ್ನಡ",
            "english_name": "Kannada",
            "locale": "kn-IN",
            "stt_status": "REAL",
            "tts_status": "REAL",
            "ai_status": "REAL"
        },
        "ml": {
            "id": "ml",
            "name": "മലയാളം",
            "english_name": "Malayalam",
            "locale": "ml-IN",
            "stt_status": "REAL",
            "tts_status": "REAL",
            "ai_status": "REAL"
        },
        "hi": {
            "id": "hi",
            "name": "हिन्दी",
            "english_name": "Hindi",
            "locale": "hi-IN",
            "stt_status": "REAL",
            "tts_status": "REAL",
            "ai_status": "REAL"
        },
        "gu": {
            "id": "gu",
            "name": "ગુજરાતી",
            "english_name": "Gujarati",
            "locale": "gu-IN",
            "stt_status": "REAL",
            "tts_status": "REAL",
            "ai_status": "REAL"
        },
        "mr": {
            "id": "mr",
            "name": "मराठी",
            "english_name": "Marathi",
            "locale": "mr-IN",
            "stt_status": "REAL",
            "tts_status": "REAL",
            "ai_status": "REAL"
        },
        "bn": {
            "id": "bn",
            "name": "বাংলা",
            "english_name": "Bengali",
            "locale": "bn-IN",
            "stt_status": "REAL",
            "tts_status": "REAL",
            "ai_status": "REAL"
        },
        "pa": {
            "id": "pa",
            "name": "ਪੰਜਾਬੀ",
            "english_name": "Punjabi",
            "locale": "pa-IN",
            "stt_status": "REAL",
            "tts_status": "REAL",
            "ai_status": "REAL"
        }
    }

    @classmethod
    def get_supported_languages(cls) -> List[Dict[str, Any]]:
        return list(cls.LANGUAGES.values())

    @classmethod
    def get_language(cls, code: str) -> Dict[str, Any]:
        return cls.LANGUAGES.get(code.lower(), cls.LANGUAGES["ta"])

    @classmethod
    def get_locale(cls, code: str) -> str:
        lang = cls.get_language(code)
        return lang["locale"]
