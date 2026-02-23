import httpx
from sqlalchemy.orm import Session

from app.config import settings
from app.models.video import Video

YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"


async def fetch_channel_videos(channel_id: str) -> list[dict]:
    """Fetch video list from a YouTube channel."""
    videos = []
    next_page_token = None

    async with httpx.AsyncClient() as client:
        while True:
            params = {
                "key": settings.youtube_api_key,
                "channelId": channel_id,
                "part": "snippet",
                "order": "date",
                "maxResults": 50,
                "type": "video",
            }
            if next_page_token:
                params["pageToken"] = next_page_token

            resp = await client.get(f"{YOUTUBE_API_BASE}/search", params=params)
            data = resp.json()

            for item in data.get("items", []):
                snippet = item["snippet"]
                videos.append({
                    "youtube_video_id": item["id"]["videoId"],
                    "title": snippet["title"],
                    "published_at": snippet["publishedAt"],
                    "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                })

            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break

    return videos


async def fetch_new_videos(db: Session) -> int:
    """Check for new videos and add them to DB. Returns count of new videos."""
    # TODO: Store channel_id in config/settings
    # For now, return 0 as placeholder
    return 0


async def get_transcript(youtube_video_id: str) -> tuple[str, str]:
    """Get transcript for a video. Returns (transcript, source)."""
    # Try YouTube captions first
    transcript = await _fetch_youtube_captions(youtube_video_id)
    if transcript:
        return transcript, "youtube_caption"

    # TODO: Fallback to Whisper
    return "", "none"


async def _fetch_youtube_captions(youtube_video_id: str) -> str | None:
    """Fetch captions from YouTube API."""
    async with httpx.AsyncClient() as client:
        params = {
            "key": settings.youtube_api_key,
            "videoId": youtube_video_id,
            "part": "snippet",
        }
        resp = await client.get(f"{YOUTUBE_API_BASE}/captions", params=params)
        data = resp.json()

        captions = data.get("items", [])
        if not captions:
            return None

        # Find Japanese caption
        ja_caption = next(
            (c for c in captions if c["snippet"]["language"] == "ja"),
            captions[0] if captions else None,
        )

        if not ja_caption:
            return None

        # Note: Downloading actual caption content requires OAuth.
        # For now, return None to trigger Whisper fallback.
        return None
