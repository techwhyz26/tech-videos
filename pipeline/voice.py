"""Step 3 - voiceover with free Microsoft Edge neural voices, plus word timings for captions."""
from __future__ import annotations

import asyncio

import aiohttp
import edge_tts
import edge_tts.exceptions

from .common import VIDEOS, config, save_spec

TAIL_MS = 260  # breathing room after the last word of each scene

AUDITION_VOICES = [
    "en-US-AndrewMultilingualNeural",
    "en-US-BrianMultilingualNeural",
    "en-US-AvaMultilingualNeural",
    "en-US-EmmaMultilingualNeural",
    "en-US-ChristopherNeural",
    "en-GB-RyanNeural",
]
AUDITION_TEXT = (
    "A thief can switch your phone off, and you can still find it on a map. "
    "So what is still running inside a phone that's off? Here's the part most people miss."
)


async def _audition(folder) -> list[str]:
    cfg = config()["voice"]
    made = []
    for voice in AUDITION_VOICES:
        path = folder / f"{voice}.mp3"
        for attempt in range(1, ATTEMPTS + 1):
            try:
                if await _speak(AUDITION_TEXT, path, voice, cfg["rate"], cfg.get("pitch", "+0Hz")):
                    made.append(path.name)
                    break
            except (edge_tts.exceptions.EdgeTTSException, aiohttp.ClientError):
                pass
            await asyncio.sleep(min(8, 1.5 * attempt))
    return made


def audition(folder) -> list[str]:
    """Write the same lines in several voices so you can pick one by ear."""
    folder.mkdir(parents=True, exist_ok=True)
    return asyncio.run(_audition(folder))
ATTEMPTS = 12


async def _speak(text: str, path, voice: str, rate: str, pitch: str = "+0Hz") -> list[dict]:
    words: list[dict] = []
    stream = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, boundary="WordBoundary").stream()
    with open(path, "wb") as audio:
        async for chunk in stream:
            if chunk["type"] == "audio":
                audio.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                start = chunk["offset"] / 10_000  # 100 ns ticks -> ms
                words.append(
                    {
                        "text": chunk["text"],
                        "startMs": round(start),
                        "endMs": round(start + chunk["duration"] / 10_000),
                    }
                )
    return words


async def _voice_all(spec: dict) -> None:
    cfg = config()["voice"]
    folder = VIDEOS / spec["slug"]
    folder.mkdir(parents=True, exist_ok=True)
    for i, scene in enumerate(spec["scenes"]):
        name = f"scene-{i + 1:02d}.mp3"
        # Resume: keep audio from an earlier run if the narration and voice have not changed.
        pitch = cfg.get("pitch", "+0Hz")
        stamp = f"{cfg['name']}|{cfg['rate']}|{pitch}|{scene['narration']}"
        if scene.get("voiced") == stamp and scene.get("words") and (folder / name).exists():
            continue
        words: list[dict] = []
        # The free service randomly drops requests, so retry with a growing pause.
        for attempt in range(1, ATTEMPTS + 1):
            try:
                words = await _speak(scene["narration"], folder / name, cfg["name"], cfg["rate"], pitch)
            except (edge_tts.exceptions.EdgeTTSException, aiohttp.ClientError) as err:
                if attempt == ATTEMPTS:
                    raise SystemExit(
                        f"Voice service failed for scene {i + 1}: {err}\n"
                        f"Finished scenes are saved. Run `python run.py build {spec['slug']}` to continue."
                    )
            if words:
                break
            await asyncio.sleep(min(8, 1.5 * attempt))
        if not words:
            raise SystemExit(f"No audio came back for scene {i + 1}. Check your internet connection.")
        scene["voiced"] = stamp
        scene["audio"] = f"videos/{spec['slug']}/{name}"
        scene["words"] = words
        scene["durationMs"] = words[-1]["endMs"] + TAIL_MS
        save_spec(spec)  # so a failed run can pick up where it stopped


def add_voice(spec: dict) -> dict:
    asyncio.run(_voice_all(spec))
    spec["status"] = "voiced"
    save_spec(spec)
    return spec


def total_seconds(spec: dict) -> float:
    return sum(s.get("durationMs", 0) for s in spec["scenes"]) / 1000
