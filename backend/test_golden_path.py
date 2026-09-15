import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_full_golden_path():
    # 1. Start Session
    res = client.post("/api/v1/session/start", json={"language": "ta"})
    assert res.status_code == 200
    session_data = res.json()
    session_id = session_data["session_id"]
    assert session_data["current_state"] == "LANGUAGE_SELECTION"
    assert "வணக்கம்" in session_data["arta_message"]

    # 2. Voice Name Input (Dynamic Name: Kuppuswamy)
    res = client.post("/api/v1/onboarding/voice-input", json={
        "session_id": session_id,
        "transcript": "என் பெயர் குப்புசாமி",
        "field_target": "name"
    })
    assert res.status_code == 200
    assert res.json()["extracted_data"].get("name") == "Kuppuswamy"

    # 3. Voice Age Input (Dynamic Age: 45)
    res = client.post("/api/v1/onboarding/voice-input", json={
        "session_id": session_id,
        "transcript": "எனக்கு 45 வயது",
        "field_target": "age"
    })
    assert res.status_code == 200
    assert res.json()["extracted_data"].get("age") == 45

    # 4. Identity Document Processing
    res = client.post("/api/v1/identity/verify-demo", json={
        "session_id": session_id,
        "document_type": "artisan_id_card"
    })
    assert res.status_code == 200
    id_res = res.json()
    assert id_res["status"] == "DOCUMENT_ATTACHED"

    # 5. Confirm Profile & Auto Login with Dynamic Session Data
    res = client.post(f"/api/v1/onboarding/confirm-profile?session_id={session_id}")
    assert res.status_code == 200
    prof_res = res.json()
    assert prof_res["name"] == "Kuppuswamy"
    assert prof_res["current_state"] == "HOME"

    # 6. Upload Artwork
    res = client.post("/api/v1/artworks/upload", data={"session_id": session_id})
    assert res.status_code == 200
    art_res = res.json()
    artwork_id = art_res["artwork_id"]

    # 7. Extract Catalog from Voice Description
    res = client.post("/api/v1/catalogs/extract-from-voice", json={
        "session_id": session_id,
        "artwork_id": artwork_id,
        "transcript": "இது தேக்கு மரத்தில் செய்த பாரம்பரிய மரச்சிலை. இதை செய்ய எனக்கு 20 மணி நேரம் ஆனது."
    })
    assert res.status_code == 200
    cat_res = res.json()
    catalog_id = cat_res["catalog_id"]
    assert cat_res["work_hours"] == 20
    assert cat_res["primary_material"] == "Teak Wood"
    assert cat_res["price_estimate"]["suggested_min"] > 0
    assert cat_res["price_estimate"]["suggested_max"] > cat_res["price_estimate"]["suggested_min"]

    # 8. Natural Voice Correction
    res = client.post(f"/api/v1/catalogs/{catalog_id}/correct", json={
        "catalog_id": catalog_id,
        "field_name": "price_amount",
        "new_value": "5000",
        "source": "ARTISAN"
    })
    assert res.status_code == 200

    # 9. Approve Catalog for Marketplace
    res = client.post(f"/api/v1/catalogs/{catalog_id}/approve")
    assert res.status_code == 200
    app_res = res.json()
    assert app_res["status"] == "READY_FOR_MARKET"
