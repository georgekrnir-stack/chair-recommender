import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.extraction_log import ExtractionLog
from app.models.recommendation_log import RecommendationLog

router = APIRouter(prefix="/api", tags=["logs"])


class ResolveRequest(BaseModel):
    chair_id: uuid.UUID


@router.get("/logs/extraction")
def list_extraction_logs(
    status: str | None = None,
    video_id: uuid.UUID | None = None,
    chair_id: uuid.UUID | None = None,
    confidence: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(ExtractionLog)
    if status:
        query = query.filter(ExtractionLog.status == status)
    if video_id:
        query = query.filter(ExtractionLog.video_id == video_id)
    if chair_id:
        query = query.filter(ExtractionLog.chair_id == chair_id)
    if confidence:
        query = query.filter(ExtractionLog.confidence == confidence)
    return query.order_by(ExtractionLog.created_at.desc()).all()


@router.get("/logs/recommendation")
def list_recommendation_logs(db: Session = Depends(get_db)):
    return db.query(RecommendationLog).order_by(RecommendationLog.created_at.desc()).all()


@router.get("/extraction-logs")
def list_extraction_logs_alias(status: str | None = None, db: Session = Depends(get_db)):
    query = db.query(ExtractionLog)
    if status:
        query = query.filter(ExtractionLog.status == status)
    return query.order_by(ExtractionLog.created_at.desc()).all()


@router.patch("/extraction-logs/{log_id}/resolve")
def resolve_log(log_id: uuid.UUID, body: ResolveRequest, db: Session = Depends(get_db)):
    log = db.query(ExtractionLog).filter(ExtractionLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="ログが見つかりません")
    log.chair_id = body.chair_id
    log.status = "manually_matched"
    db.commit()
    db.refresh(log)
    return log


@router.post("/extraction-logs/{log_id}/ignore")
def ignore_log(log_id: uuid.UUID, db: Session = Depends(get_db)):
    log = db.query(ExtractionLog).filter(ExtractionLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="ログが見つかりません")
    log.status = "ignored"
    db.commit()
    db.refresh(log)
    return log
