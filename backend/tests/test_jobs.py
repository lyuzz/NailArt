from fastapi.testclient import TestClient

from app.main import app
from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.db.models import Job


def test_job_fetch():
    init_db()
    db = SessionLocal()
    job = Job(
        id="job_test",
        kind="extract",
        status="queued",
        progress=0,
        input_json={"local_path": "dummy"},
    )
    db.add(job)
    db.commit()
    db.close()

    client = TestClient(app)
    resp = client.get("/v1/jobs/job_test")
    assert resp.status_code == 200
    assert resp.json()["job_id"] == "job_test"
