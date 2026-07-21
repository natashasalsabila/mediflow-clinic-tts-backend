import logging

import edge_tts
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, Field

from .config import settings


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("mediflow-tts")

app = FastAPI(title="MediFlow TTS", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


class TTSRequest(BaseModel):
    text: str = Field(min_length=1, max_length=settings.max_text_length)


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "mediflow-tts",
        "provider": "edge-tts",
    }


@app.post("/tts", response_class=Response)
async def synthesize_speech(request: TTSRequest) -> Response:
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=422, detail="Text cannot be empty.")
    if settings.provider != "edge-tts":
        raise HTTPException(status_code=503, detail="Configured TTS provider is unavailable.")

    logger.info(
        "Generating queue announcement voice=%s rate=%s pitch=%s volume=%s chars=%d",
        settings.voice,
        settings.rate,
        settings.pitch,
        settings.volume,
        len(text),
    )

    try:
        communicator = edge_tts.Communicate(
            text=text,
            voice=settings.voice,
            rate=settings.rate,
            pitch=settings.pitch,
            volume=settings.volume,
        )
        audio_chunks: list[bytes] = []
        async for chunk in communicator.stream():
            if chunk["type"] == "audio":
                audio_chunks.append(chunk["data"])
        audio = b"".join(audio_chunks)
        if not audio:
            raise RuntimeError("Edge TTS returned no audio bytes.")
    except Exception as error:
        logger.exception("Edge TTS generation failed")
        raise HTTPException(
            status_code=503,
            detail="TTS service is currently unavailable.",
        ) from error

    logger.info("Generated %d MP3 bytes", len(audio))
    return Response(
        content=audio,
        media_type="audio/mpeg",
        headers={"Cache-Control": "no-store"},
    )
