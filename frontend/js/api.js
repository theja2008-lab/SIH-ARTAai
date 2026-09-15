const API_BASE_URL = '/api/v1';

class ArtinoAPI {
  static async startSession(language = 'ta') {
    const res = await fetch(`${API_BASE_URL}/session/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ language })
    });
    return await res.json();
  }

  static async submitVoiceInput(sessionId, transcript, fieldTarget = null) {
    const res = await fetch(`${API_BASE_URL}/onboarding/voice-input`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId,
        transcript,
        field_target: fieldTarget
      })
    });
    return await res.json();
  }

  static async verifyDemoIdentity(sessionId, documentType = 'aadhaar_demo', imageB64 = null) {
    const res = await fetch(`${API_BASE_URL}/identity/verify-demo`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId,
        document_type: documentType,
        image_b64: imageB64
      })
    });
    return await res.json();
  }

  static async confirmProfile(sessionId) {
    const res = await fetch(`${API_BASE_URL}/onboarding/confirm-profile?session_id=${sessionId}`, {
      method: 'POST'
    });
    return await res.json();
  }

  static async uploadArtwork(sessionId, file = null) {
    const formData = new FormData();
    formData.append('session_id', sessionId);
    if (file) {
      formData.append('file', file);
    }
    const res = await fetch(`${API_BASE_URL}/artworks/upload`, {
      method: 'POST',
      body: formData
    });
    return await res.json();
  }

  static async extractCatalogFromVoice(sessionId, artworkId, transcript) {
    const res = await fetch(`${API_BASE_URL}/catalogs/extract-from-voice`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId,
        artwork_id: artworkId,
        transcript
      })
    });
    return await res.json();
  }

  static async correctCatalogField(catalogId, fieldName, newValue) {
    const res = await fetch(`${API_BASE_URL}/catalogs/${catalogId}/correct`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        catalog_id: catalogId,
        field_name: fieldName,
        new_value: String(newValue),
        source: 'ARTISAN'
      })
    });
    return await res.json();
  }

  static async approveCatalog(catalogId) {
    const res = await fetch(`${API_BASE_URL}/catalogs/${catalogId}/approve`, {
      method: 'POST'
    });
    return await res.json();
  }
}

window.ArtinoAPI = ArtinoAPI;
