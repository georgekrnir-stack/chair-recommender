from app.services.youtube import get_transcript


async def transcribe_video(youtube_video_id: str) -> tuple[str, str]:
    """Get transcript for a video using available methods.

    Returns (transcript_text, source) where source is 'youtube_caption' or 'whisper'.
    """
    transcript, source = await get_transcript(youtube_video_id)

    if transcript:
        return transcript, source

    # TODO: Implement Whisper fallback
    # This would download the audio and use OpenAI Whisper API
    return "", "none"
