import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.video import Video
from app.services.youtube import fetch_new_videos

router = APIRouter(prefix="/api/videos", tags=["videos"])


@router.get("")
def list_videos(db: Session = Depends(get_db)):
    videos = db.query(Video).order_by(Video.published_at.desc()).all()
    return videos


@router.get("/{video_id}")
def get_video(video_id: uuid.UUID, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="動画が見つかりません")
    return video


@router.post("/sync")
async def sync_videos(db: Session = Depends(get_db)):
    new_count = await fetch_new_videos(db)
    return {"message": f"{new_count}件の新着動画を取得しました"}
