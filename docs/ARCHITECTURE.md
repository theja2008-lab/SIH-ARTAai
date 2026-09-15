# ARTINO Architecture Specification

## Overview
ARTINO is an AI-powered, voice-first digital platform designed for low-literacy, rural, and traditional artisans. The system uses **ARTA (The Artisan's AI Companion)** to bridge the gap between human artisan stories and digital e-commerce catalogs.

---

## 1. Core Architectural Principle

```
                 ARTINO PLATFORM
                        │
       ┌────────────────┴────────────────┐
       │                                 │
APPLICATION STATE                   ARTA AI ENGINE
(Explicit State Machine)          (Understand, Extract, Explain)
       │                                 │
       └────────────────┬────────────────┘
                        ↓
                 DOMAIN SERVICES
   (Catalog, Pricing, Identity, Vision, Media)
                        ↓
             DATABASE & EXTERNAL APIS
```

- **Application State Machine**: Determines where the user is and what transitions are allowed.
- **ARTA Intelligence**: Determines what is said or extracted based on structured context.
- **Domain Services**: Executes core business logic (pricing formulas, field provenance, catalog generation).
- **Persistence Layer**: SQLAlchemy + SQLite (`artino.db`).

---

## 2. State Machine

```
[LANGUAGE_SELECTION]
         ↓
[NAME_COLLECTION]
         ↓
[AGE_COLLECTION]
         ↓
[DOCUMENT_CAPTURE] → [DOCUMENT_VERIFICATION]
         ↓
[PROFILE_PHOTO]
         ↓
[EXPERIENCE_COLLECTION]
         ↓
[EXPERTISE_COLLECTION]
         ↓
[PROFILE_CONFIRMATION] → [ACCOUNT_CREATION] → [HOME]
                                                ↓
                                        [ARTWORK_CAPTURE]
                                                ↓
                                        [ARTWORK_PREVIEW]
                                                ↓
                                        [ARTWORK_ANALYSIS]
                                                ↓
                                        [VOICE_DESCRIPTION]
                                                ↓
                                    [INFORMATION_EXTRACTION]
                                                ↓
                                    [MISSING_INFORMATION]
                                                ↓
                                       [CATALOG_GENERATION]
                                                ↓
                                       [PRICE_ESTIMATION]
                                                ↓
                                       [ARTISAN_REVIEW]
                                                ↓
                                        [CONFIRMATION]
                                                ↓
                                      [READY_FOR_MARKET]
```

---

## 3. ARTA Context Model

Every interaction with ARTA passes a structured context object:

```json
{
  "language": "ta",
  "current_state": "EXPERIENCE_COLLECTION",
  "current_task": "collect_experience",
  "collected_fields": {
    "name": "Kuppuswamy",
    "age": 45
  },
  "required_fields": ["name", "age", "experience_years", "craft_expertise"],
  "missing_fields": ["experience_years", "craft_expertise"],
  "conversation_context": [],
  "user_corrections": []
}
```

---

## 4. Service Boundaries

| Service Interface | Prototype Implementation | Production Path (Future) |
|---|---|---|
| `ArtaService` | Gemini API / Fallback Prompt Engine | Fine-tuned Local & Cloud AI |
| `SpeechService` | Web Speech API (`ta-IN`, `en-US`) | Whisper / IndicSpeech Models |
| `VisionService` | Gemini Vision / Feature Extraction | Specialized Craft Vision Models |
| `IdentityVerificationService` | `DemoIdentityVerificationService` (OCR Match) | Government Authorized Aadhaar API |
| `PricingService` | `DemoPricingEngine` (Labor+Material+Skill) | Market Demand ML Intelligence |
| `MarketplaceService` | `DemoMarketplaceService` (Preview Card) | Live E-Commerce Integrations |
