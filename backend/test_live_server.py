import urllib.request
import json

BASE_URL = "http://127.0.0.1:8000"

def test_live_server_endpoints():
    # 1. Health check
    req = urllib.request.urlopen(f"{BASE_URL}/health")
    assert req.status == 200
    health_data = json.loads(req.read().decode())
    assert health_data["status"] == "healthy"
    print("[Live Test] /health endpoint OK")

    # 2. Frontend index.html serving
    req_index = urllib.request.urlopen(f"{BASE_URL}/")
    assert req_index.status == 200
    html_content = req_index.read().decode()
    assert "ARTINO" in html_content
    print("[Live Test] Frontend index.html served OK")

    # 3. Static asset serving (sample_teak_carving.jpg)
    req_img = urllib.request.urlopen(f"{BASE_URL}/assets/images/sample_teak_carving.jpg")
    assert req_img.status == 200
    assert len(req_img.read()) > 1000
    print("[Live Test] Sample artwork image asset served OK")

    # 4. API Session Start
    session_req = urllib.request.Request(
        f"{BASE_URL}/api/v1/session/start",
        data=json.dumps({"language": "ta"}).encode(),
        headers={"Content-Type": "application/json"}
    )
    res_session = urllib.request.urlopen(session_req)
    assert res_session.status == 200
    s_data = json.loads(res_session.read().decode())
    session_id = s_data["session_id"]
    print(f"[Live Test] Session created OK: {session_id}")

    # 5. Onboarding Name
    name_req = urllib.request.Request(
        f"{BASE_URL}/api/v1/onboarding/voice-input",
        data=json.dumps({"session_id": session_id, "transcript": "என் பெயர் அருண்", "field_target": "name"}).encode(),
        headers={"Content-Type": "application/json"}
    )
    res_name = urllib.request.urlopen(name_req)
    assert res_name.status == 200
    n_data = json.loads(res_name.read().decode())
    assert "extracted_data" in n_data
    print("[Live Test] Voice Name extraction OK")

    # 6. Identity Demo Verification
    id_req = urllib.request.Request(
        f"{BASE_URL}/api/v1/identity/verify-demo",
        data=json.dumps({"session_id": session_id, "document_type": "artisan_id_card"}).encode(),
        headers={"Content-Type": "application/json"}
    )
    res_id = urllib.request.urlopen(id_req)
    assert res_id.status == 200
    id_data = json.loads(res_id.read().decode())
    assert id_data["status"] == "DOCUMENT_ATTACHED"
    print("[Live Test] Identity Document Processing OK: DOCUMENT_ATTACHED")

    # 7. Extract Catalog from Voice
    cat_req = urllib.request.Request(
        f"{BASE_URL}/api/v1/catalogs/extract-from-voice",
        data=json.dumps({
            "session_id": session_id,
            "artwork_id": "ARTW-5001",
            "transcript": "இது தேக்கு மரத்தில் செய்த மரச்சிலை. 20 மணி நேரம் ஆனது."
        }).encode(),
        headers={"Content-Type": "application/json"}
    )
    res_cat = urllib.request.urlopen(cat_req)
    assert res_cat.status == 200
    cat_data = json.loads(res_cat.read().decode())
    catalog_id = cat_data["catalog_id"]
    assert cat_data["price_estimate"]["recommended_price"] >= 4000
    print(f"[Live Test] Catalog extracted OK: {catalog_id}, Price: INR {cat_data['price_estimate']['recommended_price']}")

    # 8. Approve Catalog
    app_req = urllib.request.Request(
        f"{BASE_URL}/api/v1/catalogs/{catalog_id}/approve",
        data=b"",
        headers={"Content-Type": "application/json"}
    )
    res_app = urllib.request.urlopen(app_req)
    assert res_app.status == 200
    print("[Live Test] Catalog approval OK: READY_FOR_MARKET")

    print("ALL LIVE INTEGRATION TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_live_server_endpoints()
