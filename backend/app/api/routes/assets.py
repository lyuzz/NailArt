from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models import Asset
from app.schemas.asset import AssetCreate, AssetOut
from app.utils.ids import make_id

router = APIRouter()


@router.post("/assets", response_model=AssetOut)
def create_asset(payload: AssetCreate, db: Session = Depends(get_db)):
    asset = Asset(
        id=make_id("ast"),
        owner_type=payload.owner_type,
        title=payload.title,
        type=payload.type,
        preview_url=payload.preview_url,
        nails_json=payload.nails_json,
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


@router.get("/assets", response_model=list[AssetOut])
def list_assets(owner_type: str = Query("all"), db: Session = Depends(get_db)):
    query = db.query(Asset)
    if owner_type != "all":
        query = query.filter(Asset.owner_type == owner_type)
    return query.order_by(Asset.created_at.desc()).all()


@router.get("/assets/{asset_id}", response_model=AssetOut)
def get_asset(asset_id: str, db: Session = Depends(get_db)):
    asset = db.get(Asset, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset
