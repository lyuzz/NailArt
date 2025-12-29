from pydantic import BaseModel
from typing import Any, Dict, Optional


class JobOut(BaseModel):
    job_id: str
    kind: str
    status: str
    progress: int
    output: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, str]] = None


class JobCreateResponse(BaseModel):
    job_id: str
    status: str
