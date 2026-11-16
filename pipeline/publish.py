"""Step 5 - publish an approved video.

Posting goes through Upload-Post (https://www.upload-post.com), one API that posts to Instagram,
TikTok, YouTube, Facebook and more from the accounts you connect on their website. It needs:
  UPLOAD_POST_API_KEY            environment variable (GitHub secret in the cloud)
  config.json -> automation.upload_post_user   the profile name you created on Upload-Post
  config.json -> automation.platforms          which of the connected accounts to post to

Without an API key, `publish` only copies the video and caption to output/ready/ for manual upload.
"""
from __future__ import annotations

import os
import shutil
import time
from pathlib import Path

import httpx

from .common import OUTPUT, config, save_spec

UPLOAD_URL = "https://api.upload-post.com/api/upload"
STATUS_URL = "https://api.upload-post.com/api/uploadposts/status"
DONE = {"completed", "failed"}


def _upload_post(video: Path, spec: dict, key: str) -> dict[str, str]:
    auto = config().get("automation", {})
    user, platforms = auto.get("upload_post_user"), auto.get("platforms") or []
    if not user or not platforms:
        raise SystemExit("Set automation.upload_post_user and automation.platforms in config.json.")
    caption = spec.get("caption", spec["title"])
    headers = {"Authorization": f"Apikey {key}", "Idempotency-Key": f"video-{spec['slug']}"}
    # On Instagram and TikTok the post text is "title"; YouTube gets a short title and the caption
    # as its description.
    data = [("user", user), ("title", caption), ("description", caption),
            ("youtube_title", spec["title"][:95]), ("youtube_description", caption),
            ("privacyStatus", "public"), ("media_type", "REELS"), ("facebook_media_type", "REELS"),
            ("async_upload", "true"), ("external_id", spec["slug"])]
    data += [("platform[]", p) for p in platforms]
    with video.open("rb") as f:
        r = httpx.post(UPLOAD_URL, headers=headers, data=data,
                       files={"video": (video.name, f, "video/mp4")}, timeout=600)
    body = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
    if r.status_code >= 400 or not body.get("success"):
        raise RuntimeError(f"Upload-Post refused the upload ({r.status_code}): "
                           f"{body.get('message') or body.get('error') or r.text[:300]}")
    if "results" in body:  # finished straight away
        return {p: (v.get("url") or "posted") if v.get("success") else f"FAILED: {v.get('error')}"
                for p, v in body["results"].items() if not v.get("skipped")}

    # Processing in the background: check every 15 s for up to 15 minutes.
    request_id = body["request_id"]
    status = {}
    for _ in range(60):
        time.sleep(15)
        status = httpx.get(STATUS_URL, headers={"Authorization": f"Apikey {key}"},
                           params={"request_id": request_id}, timeout=60).json()
        if status.get("status") in DONE:
            break
    results = {}
    for item in status.get("results") or []:
        ok = item.get("success")
        results[item.get("platform", "?")] = (item.get("post_url") or item.get("url") or "posted") if ok \
            else f"FAILED: {item.get('message', '')}"
    if status.get("status") not in DONE:
        results["note"] = f"still processing on Upload-Post (request {request_id})"
    return results


def publish(spec: dict, video: Path | None = None) -> dict[str, str]:
    if spec.get("status") not in ("approved", "published"):
        raise SystemExit(
            f"'{spec['slug']}' is not approved yet. Watch output/{spec['slug']}.mp4, "
            f"then run `python run.py approve {spec['slug']}`."
        )
    video = video or OUTPUT / f"{spec['slug']}.mp4"
    if not video.exists():
        raise SystemExit(f"{video} does not exist. Render it first with `python run.py build {spec['slug']}`.")

    key = os.environ.get("UPLOAD_POST_API_KEY", "").strip()
    if not key:
        ready = OUTPUT / "ready"
        ready.mkdir(parents=True, exist_ok=True)
        shutil.copy2(video, ready / video.name)
        (ready / f"{spec['slug']}.txt").write_text(spec.get("caption", spec["title"]), encoding="utf-8")
        return {"manual": str(ready / video.name)}

    results = _upload_post(video, spec, key)
    if results and all(str(v).startswith("FAILED") for v in results.values()):
        raise RuntimeError("Every platform failed: " + "; ".join(f"{p}: {v}" for p, v in results.items()))
    spec["status"] = "published"
    spec["posts"] = results
    save_spec(spec)
    return results
