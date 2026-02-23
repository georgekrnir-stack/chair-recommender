import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.chair import Chair

router = APIRouter(prefix="/api/chairs", tags=["chairs"])


class ChairCreate(BaseModel):
    canonical_name: str
    maker: str | None = None
    model_number: str | None = None
    price_range: str | None = None
    features: list | None = []
    target_users: list | None = []
    pros: list | None = []
    cons: list | None = []
    comparison_notes: str | None = None
    is_recommendable: bool = False
    source_video_ids: list | None = []


class ChairUpdate(ChairCreate):
    pass


class RecommendableUpdate(BaseModel):
    is_recommendable: bool


@router.get("")
def list_chairs(db: Session = Depends(get_db)):
    chairs = db.query(Chair).order_by(Chair.canonical_name).all()
    return chairs


@router.get("/{chair_id}")
def get_chair(chair_id: uuid.UUID, db: Session = Depends(get_db)):
    chair = db.query(Chair).filter(Chair.id == chair_id).first()
    if not chair:
        raise HTTPException(status_code=404, detail="椅子が見つかりません")
    return chair


@router.post("")
def create_chair(body: ChairCreate, db: Session = Depends(get_db)):
    chair = Chair(**body.model_dump())
    db.add(chair)
    db.commit()
    db.refresh(chair)
    return chair


@router.put("/{chair_id}")
def update_chair(chair_id: uuid.UUID, body: ChairUpdate, db: Session = Depends(get_db)):
    chair = db.query(Chair).filter(Chair.id == chair_id).first()
    if not chair:
        raise HTTPException(status_code=404, detail="椅子が見つかりません")
    for key, value in body.model_dump().items():
        setattr(chair, key, value)
    db.commit()
    db.refresh(chair)
    return chair


@router.delete("/{chair_id}")
def delete_chair(chair_id: uuid.UUID, db: Session = Depends(get_db)):
    chair = db.query(Chair).filter(Chair.id == chair_id).first()
    if not chair:
        raise HTTPException(status_code=404, detail="椅子が見つかりません")
    db.delete(chair)
    db.commit()
    return {"message": "削除しました"}


@router.patch("/{chair_id}/recommendable")
def toggle_recommendable(chair_id: uuid.UUID, body: RecommendableUpdate, db: Session = Depends(get_db)):
    chair = db.query(Chair).filter(Chair.id == chair_id).first()
    if not chair:
        raise HTTPException(status_code=404, detail="椅子が見つかりません")
    chair.is_recommendable = body.is_recommendable
    db.commit()
    db.refresh(chair)
    return chair
