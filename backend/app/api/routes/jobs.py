from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models import Job
from app.schemas.job import JobOut

router = APIRouter()


@router.get("/jobs/{job_id}", response_model=JobOut)
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    error = None
    if job.status == "failed":
        error = {"code": job.error_code or "PROCESSING_ERROR", "message": job.error_message or ""}
    return JobOut(
        job_id=job.id,
        kind=job.kind,
        status=job.status,
        progress=job.progress,
        output=job.output_json,
        error=error,
    )
