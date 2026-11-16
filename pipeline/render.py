"""Step 4 - render the spec to an MP4 with Remotion."""
from __future__ import annotations

import copy
import json
import shutil
import subprocess

from .common import OUTPUT, ROOT, VIDEOS, refresh_path, save_spec


def write_render_spec(spec: dict) -> str:
    """Write spec.render.json: the spec with illustrations (art/<name>.svg) inlined for the renderer."""
    slug = spec["slug"]
    resolved = copy.deepcopy(spec)
    for scene in resolved["scenes"]:
        props = scene.get("props") or {}
        if scene.get("type") == "art" and props.get("art") and not props.get("svg"):
            props["svg"] = (VIDEOS / slug / "art" / f"{props['art']}.svg").read_text(encoding="utf-8")
    (VIDEOS / slug / "spec.render.json").write_text(json.dumps(resolved, ensure_ascii=False), encoding="utf-8")
    return f"public/videos/{slug}/spec.render.json"


def render(spec: dict) -> str:
    refresh_path()
    npx = shutil.which("npx")
    if not npx:
        raise SystemExit("Node.js was not found. Install it, then open a new terminal.")
    OUTPUT.mkdir(exist_ok=True)
    slug = spec["slug"]
    out = f"output/{slug}.mp4"
    props_file = write_render_spec(spec)
    result = subprocess.run(
        [npx, "remotion", "render", "src/index.ts", "Main", out,
         f"--props={props_file}", "--log=warn"],
        cwd=ROOT,
    )
    if result.returncode != 0:
        raise SystemExit("Render failed, see the messages above.")
    (OUTPUT / f"{slug}.txt").write_text(spec.get("caption", spec["title"]), encoding="utf-8")
    spec["status"] = "rendered"
    save_spec(spec)
    return out
