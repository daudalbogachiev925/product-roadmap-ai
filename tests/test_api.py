def test_health(client):
    assert client.get("/health").json()["status"] == "ok"

def test_create_feature(client):
    payload = {"title": "New feature", "reach": 100, "impact": 2.0,
               "confidence": 0.8, "effort": 3.0}
    r = client.post("/api/features", json=payload)
    assert r.status_code == 201
    assert r.json()["title"] == "New feature"

def test_rice_empty(client):
    r = client.get("/api/prioritize/rice")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
