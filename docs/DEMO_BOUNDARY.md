# ARTINO Feature Classification & Service Boundaries

Every capability in ARTINO is strictly categorized as:
- 🟢 **REAL**: Genuinely implemented and functional in the prototype.
- 🟡 **MOCK**: Believably simulated behind a clean, isolated service interface for demo purposes.
- 🔵 **FUTURE**: Architectural boundary defined for future production implementation.

---

## Service Classifications

| Feature / Service | Classification | Prototype Implementation | Future Replacement |
|---|---|---|---|
| Voice Recognition (STT) | 🟢 REAL | Web Speech API (`ta-IN`, `en-US`) | Whisper / IndicSpeech |
| Voice Synthesis (TTS) | 🟢 REAL | Web Speech API (`SpeechSynthesis`) | Custom Voice / ElevenLabs |
| Vision Understanding | 🟢 REAL | Gemini 2.5 / 1.5 Flash Vision API | Custom Fine-tuned Vision Models |
| AI Extraction Engine | 🟢 REAL | Structured Pydantic LLM Extraction | Dedicated On-Device / Cloud LLMs |
| Fair Price Calculation | 🟢 REAL | Deterministic Labor+Material Engine | ML Market Demand Pricing |
| State Machine & ARTA | 🟢 REAL | Backend Session State Engine | Distributed State Store |
| Camera Stream & Photo | 🟢 REAL | Web MediaDevices Camera Capture | Native Android CameraX |
| Catalog Storage & History | 🟢 REAL | SQLite / SQLAlchemy Database | PostgreSQL Enterprise Cluster |
| Demo Identity Verification | 🟡 MOCK | OCR Name Matching (`DemoIdentityVerificationService`) | Authorized Government Aadhaar API |
| Marketplace Preview Card | 🟡 MOCK | Interactive Product Preview | Live E-Commerce Integrations |
| Payments & Escrow | 🔵 FUTURE | None (Out of Scope for Prototype) | Razorpay / UPI Integration |
| Logistics & Shipping | 🔵 FUTURE | None (Out of Scope for Prototype) | Shiprocket / India Post API |
| Enterprise Fraud Detection | 🔵 FUTURE | None | Risk & Compliance Engine |

---

## Privacy & Security Boundaries
- **No Aadhaar Data Storage**: The prototype uses synthetic demo identity cards and does not store actual Aadhaar numbers.
- **Backend-Only Secrets**: `GEMINI_API_KEY` and backend database paths remain strictly on the Python backend environment and are never exposed to client browsers.
