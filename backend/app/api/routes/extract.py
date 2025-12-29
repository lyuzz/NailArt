from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models import Job
from app.schemas.job import JobCreateResponse
from app.utils.ids import make_id
from app.workers.tasks import get_queue
from app.services.storage import save_upload

router = APIRouter()


@router.post("/extract", response_model=JobCreateResponse)
def create_extract(
    file: UploadFile = File(...),
    owner_type: str = Form("user"),
    title: str = Form(""),
    db: Session = Depends(get_db),
):
    local_path, _ = save_upload(file)
    job_id = make_id("job")
    job = Job(
        id=job_id,
        kind="extract",
        status="queued",
        progress=0,
        input_json={
            "local_path": local_path,
            "owner_type": owner_type,
            "title": title or file.filename or "Untitled",
        },
    )
    db.add(job)
    db.commit()
    queue = get_queue()
    queue.enqueue("app.workers.tasks.run_extract", job_id)
    return JobCreateResponse(job_id=job_id, status="queued")
