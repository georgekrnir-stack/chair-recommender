import json

from sqlalchemy.orm import Session

from app.models.extraction_log import ExtractionLog
from app.models.prompt import Prompt
from app.models.video import Video
from app.services.llm import call_llm_json


async def extract_chair_mentions(video: Video, db: Session) -> list[dict]:
    """Extract chair mentions from a video's transcript using LLM."""
    if not video.transcript:
        return []

    prompt = db.query(Prompt).filter(Prompt.key == "extract_mentions", Prompt.is_active.is_(True)).first()
    if not prompt:
        return []

    result = await call_llm_json(prompt.content, video.transcript)

    try:
        mentions = json.loads(result)
    except json.JSONDecodeError:
        return []

    logs = []
    for mention in mentions if isinstance(mentions, list) else mentions.get("mentions", []):
        log = ExtractionLog(
            video_id=video.id,
            raw_mention=mention.get("mention", ""),
            context=mention.get("context", ""),
            timestamp_hint=mention.get("timestamp", ""),
            confidence=mention.get("confidence", "medium"),
            status="unresolved",
        )
        db.add(log)
        logs.append(mention)

    db.commit()
    return logs
