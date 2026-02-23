import uuid

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.video import Video
from app.routers.auth import require_admin

router = APIRouter(prefix="/api/pipeline", tags=["pipeline"])

# Simple in-memory progress tracking
bulk_build_status = {"running": False, "total": 0, "completed": 0, "current_phase": ""}


@router.post("/bulk-build")
async def start_bulk_build(request: Request, db: Session = Depends(get_db)):
    require_admin(request)
    if bulk_build_status["running"]:
        raise HTTPException(status_code=409, detail="一括構築が既に実行中です")

    # TODO: Implement actual bulk build pipeline
    bulk_build_status["running"] = True
    bulk_build_status["current_phase"] = "準備中"
    return {"message": "一括構築を開始しました"}


@router.get("/bulk-build/status")
def get_bulk_build_status(request: Request):
    require_admin(request)
    return bulk_build_status


@router.post("/extract/{video_id}")
async def extract_video(video_id: uuid.UUID, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="動画が見つかりません")

    # TODO: Implement extraction
    return {"message": f"動画「{video.title}」の抽出を開始しました"}


@router.post("/cluster")
async def cluster_mentions(db: Session = Depends(get_db)):
    # TODO: Implement clustering
    return {"message": "クラスタリング・名寄せを開始しました"}
