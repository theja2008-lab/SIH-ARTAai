# ARTINO API Contracts

## Base URL: `/api/v1`

### 1. Session Management
- `POST /session/start`
  - **Body**: `{ "language": "ta" }`
  - **Response**: `{ "session_id": "SES-1001", "state": "LANGUAGE_SELECTION", "arta_message": "..." }`

- `GET /session/{session_id}`
  - **Response**: Full session object with state and collected profile fields.

- `POST /session/{session_id}/transition`
  - **Body**: `{ "target_state": "NAME_COLLECTION" }`

---

### 2. Onboarding & Profile
- `POST /onboarding/voice-input`
  - **Body**: `{ "session_id": "SES-1001", "transcript": "என் பெயர் குப்புசாமி", "field": "name" }`
  - **Response**: `{ "extracted": { "name": "Kuppuswamy" }, "next_state": "AGE_COLLECTION", "arta_response": "..." }`

- `POST /onboarding/confirm-profile`
  - **Body**: `{ "session_id": "SES-1001" }`
  - **Response**: `{ "artisan_id": "ART-0001", "name": "Kuppuswamy", "status": "CREATED" }`

---

### 3. Identity Demo Verification
- `POST /identity/verify-demo`
  - **Body**: `{ "session_id": "SES-1001", "document_type": "aadhaar_demo", "image_b64": "..." }`
  - **Response**: `{ "verified": true, "extracted_name": "Kuppuswamy", "match_confidence": 0.98, "status": "DEMO_MATCHED" }`

---

### 4. ARTA Dialogue Engine
- `POST /arta/speak`
  - **Body**: `{ "session_id": "SES-1001", "user_text": "...", "context": {} }`
  - **Response**: `{ "arta_text": "...", "audio_hint": "...", "intent": "...", "updated_fields": {} }`

---

### 5. Artwork & Vision Processing
- `POST /artworks/upload`
  - **Body**: Multipart image upload or base64 payload.
  - **Response**: `{ "artwork_id": "ARTW-5001", "image_url": "..." }`

- `POST /artworks/{artwork_id}/analyze-vision`
  - **Response**: `{ "craft_category": "Wood Craft", "detected_material": "Teak Wood", "apparent_complexity": "High", "confidence": 0.92 }`

---

### 6. Catalog Engine
- `POST /catalogs/extract-from-voice`
  - **Body**: `{ "session_id": "SES-1001", "artwork_id": "ARTW-5001", "transcript": "..." }`
  - **Response**: `{ "catalog": { "product_name": "Teak Wood Carving", ... }, "provenance": [...], "missing_fields": [] }`

- `POST /catalogs/{catalog_id}/correct-field`
  - **Body**: `{ "field_name": "price", "new_value": 5000, "source": "ARTISAN" }`
  - **Response**: `{ "updated": true, "catalog": { ... } }`

---

### 7. Fair Price Engine
- `POST /pricing/estimate`
  - **Body**: `{ "craft_category": "Wood Craft", "material": "Teak Wood", "work_hours": 20, "experience_years": 25 }`
  - **Response**: `{ "suggested_min": 4500, "suggested_max": 5500, "suggested_recommended": 5000, "factors": { "labor": 3000, "material": 1200, "skill": 800 } }`
