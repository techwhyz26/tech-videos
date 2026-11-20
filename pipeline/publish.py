"""Step 5 - publish an approved video.

Posting goes through Upload-Post (https://www.upload-post.com), one API that posts to Instagram,
TikTok, YouTube, Facebook and more from the accounts you connect on their website. It needs:
  UPLOAD_POST_API_KEY            environment variable (GitHub secret in the cloud)
  config.json -> automation.upload_post_user   the profile name you created on Upload-Post
  config.json -> automation.platforms          which of the connected accounts to post to

Without an API key, `publish` only copies the video and caption to output/ready/ for manual upload.
"""
from __future__ import annotations

import datetime as dt
import os
import re
import shutil
import time
from pathlib import Path
from zoneinfo import ZoneInfo

import httpx

from .common import OUTPUT, all_specs, config, save_spec

UPLOAD_URL = "https://api.upload-post.com/api/upload"
STATUS_URL = "https://api.upload-post.com/api/uploadposts/status"
HISTORY_URL = "https://api.upload-post.com/api/uploadposts/history"
DONE = {"completed", "failed"}


def next_slot(now: dt.datetime | None = None) -> dt.datetime | None:
    """The next posting time from config.json -> automation.schedule, at least `days_between` days after
    the last scheduled post, so approved videos go out one at a time at the time of day that reaches
    the most people. None means post straight away."""
    sched = config().get("automation", {}).get("schedule")
    if not sched:
        return None
    tz = ZoneInfo(sched.get("timezone", "UTC"))
    now = (now or dt.datetime.now(dt.timezone.utc)).astimezone(tz)
    earliest = now + dt.timedelta(minutes=30)
    taken = [dt.datetime.fromisoformat(s["scheduled_for"]).astimezone(tz)
             for s in all_specs() if s.get("scheduled_for")]
    if taken:
        earliest = max(earliest, max(taken) + dt.timedelta(days=sched.get("days_between", 1)) - dt.timedelta(hours=1))
    times = sorted(dt.time.fromisoformat(t) for t in sched.get("times", ["18:00"]))
    day = earliest.date()
    while True:
        for t in times:
            slot = dt.datetime.combine(day, t, tz)
            if slot >= earliest:
                return slot
        day += dt.timedelta(days=1)


def _hashtags(text: str) -> list[str]:
    return re.findall(r"#(\w+)", text)


def _upload_post(video: Path, spec: dict, key: str, when: dt.datetime | None = None,
                 only: list[str] | None = None) -> dict[str, str]:
    auto = config().get("automation", {})
    user, platforms = auto.get("upload_post_user"), only or auto.get("platforms") or []
    if not user or not platforms:
        raise SystemExit("Set automation.upload_post_user and automation.platforms in config.json.")
    caption = spec.get("caption", spec["title"])
    headers = {"Authorization": f"Apikey {key}", "Idempotency-Key": f"video-{spec['slug']}-{'-'.join(platforms)}"}
    # On Instagram and TikTok the post text is "title"; YouTube gets a short title and the caption
    # as its description.
    data = [("user", user), ("title", caption), ("description", caption),
            ("youtube_title", spec["title"][:95]), ("youtube_description", f"{caption} #Shorts"),
            ("privacyStatus", "public"), ("media_type", "REELS"), ("facebook_media_type", "REELS"),
            ("async_upload", "true"), ("external_id", spec["slug"])]
    data += [("platform[]", p) for p in platforms]
    data += [("tags[]", t) for t in _hashtags(caption) + ["shorts"]]  # YouTube search tags
    if when:
        data.append(("scheduled_date", when.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
    with video.open("rb") as f:
        form: dict[str, list[str]] = {}  # httpx wants repeated fields (platform[], tags[]) as lists
        for k, v in data:
            form.setdefault(k, []).append(v)
        r = httpx.post(UPLOAD_URL, headers=headers, data=form,
                       files={"video": (video.name, f, "video/mp4")}, timeout=600)
    body = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
    if r.status_code >= 400 or not (body.get("success") or body.get("job_id")):
        raise RuntimeError(f"Upload-Post refused the upload ({r.status_code}): "
                           f"{body.get('message') or body.get('error') or r.text[:300]}")
    if when:  # Upload-Post holds it and posts it at that time
        return {p: "scheduled" for p in platforms}
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
            else f"FAILED: {item.get('message') or item.get('error_message') or ''}"
    if any(v == "FAILED: " for v in results.values()):  # the status call leaves out the reason; history has it
        history = httpx.get(HISTORY_URL, headers={"Authorization": f"Apikey {key}"},
                            params={"request_id": request_id, "limit": 10}, timeout=60).json()
        for item in history.get("history", []):
            if results.get(item.get("platform")) == "FAILED: ":
                results[item["platform"]] = f"FAILED: {item.get('error_message') or 'no reason given'}"
    if status.get("status") not in DONE:
        results["note"] = f"still processing on Upload-Post (request {request_id})"
    return results


def publish(spec: dict, video: Path | None = None, now: bool = False,
            only: list[str] | None = None) -> dict[str, str]:
    """Post an approved video. It goes into the next free slot of the posting schedule unless `now`.
    `only` limits it to some platforms, e.g. to retry one that failed; earlier results are kept."""
    if spec.get("status") not in ("approved", "published"):
        raise SystemExit(
            f"'{spec['slug']}' is not approved yet. Watch output/{spec['slug']}.mp4, "
            f"then run `python run.py approve {spec['slug']}`."
        )
    video = video or OUTPUT / f"{spec['slug']}.mp4"
    if not video.exists():
        raise SystemExit(f"{video} does not exist. Render it first with `python run.py build {spec['slug']}`.")

    key = os.environ.get("UPLOAD_POST_API_KEY", "").strip().lstrip("﻿")
    if not key:
        ready = OUTPUT / "ready"
        ready.mkdir(parents=True, exist_ok=True)
        shutil.copy2(video, ready / video.name)
        (ready / f"{spec['slug']}.txt").write_text(spec.get("caption", spec["title"]), encoding="utf-8")
        return {"manual": str(ready / video.name)}

    when = None if now else next_slot()
    results = _upload_post(video, spec, key, when, only)
    if results and all(str(v).startswith("FAILED") for v in results.values()):
        raise RuntimeError("Every platform failed: " + "; ".join(f"{p}: {v}" for p, v in results.items()))
    spec["status"] = "published"
    spec["posts"] = {**(spec.get("posts") or {}), **results} if only else results
    if when:
        spec["scheduled_for"] = when.isoformat()
    save_spec(spec)
    return results
