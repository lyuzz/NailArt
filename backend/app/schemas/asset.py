from pydantic import BaseModel
from typing import Any, Dict, Optional


class AssetCreate(BaseModel):
    owner_type: str
    title: str
    type: str
    preview_url: str
    nails_json: Dict[str, Any]


class AssetOut(AssetCreate):
    id: str


class AssetFilter(BaseModel):
    owner_type: Optional[str] = None
