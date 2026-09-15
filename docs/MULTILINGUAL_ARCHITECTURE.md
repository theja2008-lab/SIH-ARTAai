# ARTINO Multilingual Architecture Specification

## Overview
ARTINO & ARTA are architected as a **language-independent conversation engine**. The application decouples communication language from internal application state, database schemas, and domain business rules.

---

## 1. Decoupled Multilingual Architecture

```
ARTISAN SPEAKS (Tamil / English / Hindi / Telugu / Kannada / Malayalam)
                          ↓
              SPEECH-TO-TEXT (Locale-aware)
                          ↓
             MULTILINGUAL SEMANTIC EXTRACTOR
    (Maps Indic phrases & words to language-neutral JSON)
                          ↓
              LANGUAGE-NEUTRAL DATA MODEL
    (name: "Kuppuswamy", age: 45, work_hours: 20)
                          ↓
              APPLICATION STATE MACHINE
                          ↓
               ARTA DIALOGUE GENERATION
             (Generates text in selected language)
                          ↓
              TEXT-TO-SPEECH SYNTHESIS (Locale-aware)
                          ↓
              ARTISAN HEARS SPOKEN RESPONSE
```

---

## 2. Language Registry & Status Matrix

| Language | Code | Locale | STT Status | TTS Status | AI Extraction Status |
|---|---|---|---|---|---|
| Tamil | `ta` | `ta-IN` | 🟢 REAL | 🟢 REAL | 🟢 REAL |
| English | `en` | `en-IN` | 🟢 REAL | 🟢 REAL | 🟢 REAL |
| Hindi | `hi` | `hi-IN` | 🟢 REAL | 🟢 REAL | 🟢 REAL |
| Telugu | `te` | `te-IN` | 🟢 REAL | 🟢 REAL | 🟢 REAL |
| Kannada | `kn` | `kn-IN` | 🟢 REAL | 🟢 REAL | 🟢 REAL |
| Malayalam | `ml` | `ml-IN` | 🟢 REAL | 🟢 REAL | 🟢 REAL |

---

## 3. Multilingual Number & Name Parsing Examples

All of the following natural expressions map to identical language-independent structured facts:

### Name Normalization (`provide_name`)
- Tamil: `"என் பெயர் குப்புசாமி"` -> `name = "Kuppuswamy"`
- English: `"My name is Kuppuswamy"` -> `name = "Kuppuswamy"`
- Hindi: `"मेरा नाम कुप्पुसामी है"` -> `name = "Kuppuswamy"`
- Telugu: `"నా పేరు కుప్పుసామి"` -> `name = "Kuppuswamy"`
- Kannada: `"ನನ್ನ ಹೆಸರು ಕುಪ್ಪುಸಾಮಿ"` -> `name = "Kuppuswamy"`
- Malayalam: `"എന്റെ പേര് കുപ്പുസാമി"` -> `name = "Kuppuswamy"`

### Number Extraction (`provide_age` / `provide_work_hours`)
- Digits: `"45"`, `"20"` -> `45`, `20`
- Tamil Words: `"நாற்பத்தைந்து"`, `"இருபது"` -> `45`, `20`
- Hindi Words: `"पैंतालीस"`, `"बीस"` -> `45`, `20`
- Telugu Words: `"నలభై ఐదు"`, `"ఇరవై"` -> `45`, `20`
- Kannada Words: `"ನಲವತ್ತೈದು"`, `"ಇಪ್ಪತ್ತು"` -> `45`, `20`
- Malayalam Words: `"നാൽപ്പത്തഞ്ച്"`, `"ഇരുപത്"` -> `45`, `20`

---

## 4. How to Add a New Indic Language

To register a new language (e.g. Bengali `bn-IN`, Marathi `mr-IN`, Gujarati `gu-IN`):

1. **Register Language in `LanguageRegistry`**:
   Add entry in `artino/backend/app/services/language_registry.py` with code, name, locale (`bn-IN`), and capability flags.
2. **Add Spoken Prompts in `ArtaService`**:
   Add state messages in `STATE_MESSAGES` dictionary for state nodes.
3. **Add Indic Number Words in `MultilingualNumberParser`**:
   Add word-to-integer mappings in `WORD_TO_NUMBER`.
4. **Add Script Name Variants in `MultilingualExtractor`**:
   Add name prefix and material keyword variants.
