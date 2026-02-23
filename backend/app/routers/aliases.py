import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.alias import ChairAlias
from app.models.chair import Chair

router = APIRouter(tags=["aliases"])


class AliasCreate(BaseModel):
    alias: str
    source_video_id: uuid.UUID | None = None


@router.get("/api/chairs/{chair_id}/aliases")
def list_aliases(chair_id: uuid.UUID, db: Session = Depends(get_db)):
    chair = db.query(Chair).filter(Chair.id == chair_id).first()
    if not chair:
        raise HTTPException(status_code=404, detail="椅子が見つかりません")
    return db.query(ChairAlias).filter(ChairAlias.chair_id == chair_id).all()


@router.post("/api/chairs/{chair_id}/aliases")
def create_alias(chair_id: uuid.UUID, body: AliasCreate, db: Session = Depends(get_db)):
    chair = db.query(Chair).filter(Chair.id == chair_id).first()
    if not chair:
        raise HTTPException(status_code=404, detail="椅子が見つかりません")
    alias = ChairAlias(chair_id=chair_id, **body.model_dump())
    db.add(alias)
    db.commit()
    db.refresh(alias)
    return alias


@router.delete("/api/aliases/{alias_id}")
def delete_alias(alias_id: uuid.UUID, db: Session = Depends(get_db)):
    alias = db.query(ChairAlias).filter(ChairAlias.id == alias_id).first()
    if not alias:
        raise HTTPException(status_code=404, detail="エイリアスが見つかりません")
    db.delete(alias)
    db.commit()
    return {"message": "削除しました"}
