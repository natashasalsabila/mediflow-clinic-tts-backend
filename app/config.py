from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


def _cors_origins() -> tuple[str, ...]:
    raw_value = os.getenv("TTS_CORS_ORIGINS", "")
    return tuple(origin.strip() for origin in raw_value.split(",") if origin.strip())


@dataclass(frozen=True)
class Settings:
    provider: str = os.getenv("TTS_PROVIDER", "edge-tts")
    voice: str = os.getenv("EDGE_TTS_VOICE", "en-GB-SoniaNeural")
    rate: str = os.getenv("EDGE_TTS_RATE", "-8%")
    pitch: str = os.getenv("EDGE_TTS_PITCH", "+0Hz")
    volume: str = os.getenv("EDGE_TTS_VOLUME", "+0%")
    port: int = int(os.getenv("PORT", "8000"))
    cors_origins: tuple[str, ...] = _cors_origins()
    max_text_length: int = int(os.getenv("TTS_MAX_TEXT_LENGTH", "500"))


settings = Settings()
