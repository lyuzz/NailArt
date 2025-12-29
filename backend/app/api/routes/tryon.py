from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models import Job
from app.schemas.job import JobCreateResponse
from app.utils.ids import make_id
from app.workers.tasks import get_queue
from app.services.storage import save_upload

router = APIRouter()


@router.post("/tryon", response_model=JobCreateResponse)
def create_tryon(
    file: UploadFile = File(...),
    asset_id: str = Form(...),
    db: Session = Depends(get_db),
):
    local_path, _ = save_upload(file)
    job_id = make_id("job")
    job = Job(
        id=job_id,
        kind="tryon",
        status="queued",
        progress=0,
        input_json={
            "local_path": local_path,
            "asset_id": asset_id,
        },
    )
    db.add(job)
    db.commit()
    queue = get_queue()
    queue.enqueue("app.workers.tasks.run_tryon", job_id)
    return JobCreateResponse(job_id=job_id, status="queued")
