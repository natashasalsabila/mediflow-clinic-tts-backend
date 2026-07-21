import argparse
import asyncio
from pathlib import Path

import edge_tts


SAMPLE_TEXT = (
    "Queue number UM zero zero one, patient Sean, "
    "please proceed to General Clinic."
)
DEFAULT_VOICES = (
    "en-GB-SoniaNeural",
    "en-US-JennyNeural",
    "en-US-AvaNeural",
)


async def generate_samples(output_dir: Path, voices: tuple[str, ...]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for voice in voices:
        destination = output_dir / f"{voice}.mp3"
        communicator = edge_tts.Communicate(
            SAMPLE_TEXT,
            voice,
            rate="-8%",
            pitch="+0Hz",
            volume="+0%",
        )
        await communicator.save(str(destination))
        print(f"Generated {destination}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate MediFlow Edge TTS voice samples.")
    parser.add_argument("--output", default="voice_samples")
    parser.add_argument("--voices", nargs="*", default=list(DEFAULT_VOICES))
    args = parser.parse_args()
    asyncio.run(generate_samples(Path(args.output), tuple(args.voices)))


if __name__ == "__main__":
    main()
