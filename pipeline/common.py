"""Shared paths, config and spec helpers for the video pipeline."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VIDEOS = ROOT / "public" / "videos"
OUTPUT = ROOT / "output"
DATA = ROOT / "data"

SCENE_TYPES = {
    "title", "crowd", "pills", "hub", "steps", "stat", "compare", "icon",
    "words", "chart", "phone", "card", "grid", "image", "art",
}
THEMES = {"violet", "ember", "matrix", "ocean", "gold", "crimson"}
STATUSES = ["scripted", "voiced", "rendered", "approved", "published", "rejected"]


def refresh_path() -> None:
    """Pick up tools (node, ffmpeg) installed after this shell was opened."""
    if sys.platform != "win32":
        return
    import winreg

    parts = []
    for hive, key in (
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"),
        (winreg.HKEY_CURRENT_USER, "Environment"),
    ):
        try:
            with winreg.OpenKey(hive, key) as k:
                parts.append(os.path.expandvars(winreg.QueryValueEx(k, "Path")[0]))
        except OSError:
            pass
    os.environ["PATH"] = ";".join(parts + [os.environ.get("PATH", "")])


def config() -> dict:
    return json.loads((ROOT / "config.json").read_text(encoding="utf-8"))


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60] or "video"


def spec_path(slug: str) -> Path:
    return VIDEOS / slug / "spec.json"


def load_spec(slug: str) -> dict:
    path = spec_path(slug)
    if not path.exists():
        raise SystemExit(f"No video called '{slug}'. Run `python run.py status` to list videos.")
    return json.loads(path.read_text(encoding="utf-8"))


def save_spec(spec: dict) -> Path:
    path = spec_path(spec["slug"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(spec, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def all_specs() -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(VIDEOS.glob("*/spec.json"))]


def validate(spec: dict) -> list[str]:
    """Return a list of problems that would break or spoil the render."""
    errors: list[str] = []
    for field in ("slug", "title", "scenes"):
        if not spec.get(field):
            errors.append(f"missing '{field}'")
    for i, scene in enumerate(spec.get("scenes") or []):
        where = f"scene {i + 1}"
        if scene.get("type") not in SCENE_TYPES:
            errors.append(f"{where}: unknown type {scene.get('type')!r}")
        if not str(scene.get("narration", "")).strip():
            errors.append(f"{where}: empty narration")
        props = scene.get("props") or {}
        kind = scene.get("type")
        if kind == "title" and not props.get("headline"):
            errors.append(f"{where}: title needs props.headline")
        if kind in ("pills", "hub") and not props.get("items"):
            errors.append(f"{where}: {kind} needs props.items")
        if kind == "hub" and not (props.get("hub") or {}).get("label"):
            errors.append(f"{where}: hub needs props.hub.label")
        if kind == "steps" and not props.get("steps"):
            errors.append(f"{where}: steps needs props.steps")
        if kind == "stat" and not isinstance(props.get("value"), (int, float)):
            errors.append(f"{where}: stat needs a numeric props.value")
        if kind == "compare" and not (props.get("left") and props.get("right")):
            errors.append(f"{where}: compare needs props.left and props.right")
        if kind == "words" and not props.get("lines"):
            errors.append(f"{where}: words needs props.lines")
        if kind == "chart" and len(props.get("points") or []) < 2:
            errors.append(f"{where}: chart needs at least two props.points")
        if kind == "card" and not props.get("headline"):
            errors.append(f"{where}: card needs props.headline")
        if kind == "art" and not props.get("svg"):
            name = props.get("art")
            if not name:
                errors.append(f"{where}: art needs props.art (a file in art/) or props.svg")
            elif not (VIDEOS / str(spec.get("slug")) / "art" / f"{name}.svg").exists():
                errors.append(f"{where}: art file art/{name}.svg does not exist")
        if kind == "image":
            src = str(props.get("src", ""))
            if not src:
                errors.append(f"{where}: image needs props.src")
            elif not src.startswith("http") and not (ROOT / "public" / src).exists():
                errors.append(f"{where}: image file public/{src} does not exist")
    if spec.get("theme") and spec["theme"] not in THEMES:
        errors.append(f"unknown theme {spec['theme']!r} (choose from {', '.join(sorted(THEMES))})")
    return errors
