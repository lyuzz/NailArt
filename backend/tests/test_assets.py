from fastapi.testclient import TestClient

from app.main import app
from app.db.init_db import init_db


def test_assets_crud():
    init_db()
    client = TestClient(app)
    payload = {
        "owner_type": "user",
        "title": "Sample",
        "type": "set5",
        "preview_url": "/static/sample.jpg",
        "nails_json": {"nails": []},
    }
    resp = client.post("/v1/assets", json=payload)
    assert resp.status_code == 200
    asset = resp.json()
    assert asset["id"].startswith("ast_")

    resp_list = client.get("/v1/assets?owner_type=all")
    assert resp_list.status_code == 200
    data = resp_list.json()
    assert any(item["id"] == asset["id"] for item in data)
