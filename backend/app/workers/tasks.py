from typing import Any, Dict
import traceback

from redis import Redis
from rq import Queue

from app.core.config import REDIS_URL, QUEUE_NAME
from app.db.session import SessionLocal
from app.db.models import Job, Asset
from app.services.extraction_pipeline import extract_nails
from app.services.tryon_pipeline import tryon
from app.utils.errors import NailArtError, AssetNotFoundError


def get_queue() -> Queue:
    redis_conn = Redis.from_url(REDIS_URL)
    return Queue(QUEUE_NAME, connection=redis_conn)


def _update_job(db, job: Job, **fields: Any) -> None:
    for key, value in fields.items():
        setattr(job, key, value)
    db.add(job)
    db.commit()
    db.refresh(job)


def run_extract(job_id: str) -> None:
    db = SessionLocal()
    try:
        job = db.get(Job, job_id)
        if not job:
            return
        _update_job(db, job, status="running", progress=10)
        local_path = job.input_json["local_path"]
        result = extract_nails(local_path, job_id)
        _update_job(db, job, progress=60)
        output = {
            "preview_url": result["preview_url"],
            "nails": result["nails"],
            "suggested_asset": result["suggested_asset"],
        }
        _update_job(db, job, status="done", progress=100, output_json=output)
    except NailArtError as exc:
        _update_job(
            db,
            job,
            status="failed",
            progress=100,
            error_code=exc.code,
            error_message=exc.message,
        )
    except Exception as exc:
        _update_job(
            db,
            job,
            status="failed",
            progress=100,
            error_code="PROCESSING_ERROR",
            error_message=f"{exc}\n{traceback.format_exc()}",
        )
    finally:
        db.close()


def run_tryon(job_id: str) -> None:
    db = SessionLocal()
    try:
        job = db.get(Job, job_id)
        if not job:
            return
        _update_job(db, job, status="running", progress=10)
        local_path = job.input_json["local_path"]
        asset_id = job.input_json["asset_id"]
        asset = db.get(Asset, asset_id)
        if not asset:
            raise AssetNotFoundError(f"Asset not found: {asset_id}")
        _update_job(db, job, progress=60)
        output = tryon(
            local_path,
            {
                "id": asset.id,
                "nails_json": asset.nails_json,
            },
            job_id,
        )
        _update_job(db, job, status="done", progress=100, output_json=output)
    except NailArtError as exc:
        _update_job(
            db,
            job,
            status="failed",
            progress=100,
            error_code=exc.code,
            error_message=exc.message,
        )
    except Exception as exc:
        _update_job(
            db,
            job,
            status="failed",
            progress=100,
            error_code="PROCESSING_ERROR",
            error_message=f"{exc}\n{traceback.format_exc()}",
        )
    finally:
        db.close()
