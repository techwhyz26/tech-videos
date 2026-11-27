"""Step 5 - publish an approved video.

Instagram can go straight through Meta's API (pipeline/instagram.py, automation.instagram_direct).
Everything else goes through Upload-Post (https://www.upload-post.com), one API that posts to Instagram,
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

from . import instagram, youtube
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


class LimitReached(RuntimeError):
    """This Upload-Post account has used up its uploads for the month."""


def _keys() -> list[str]:
    """Every Upload-Post API key that is set: UPLOAD_POST_API_KEY, then UPLOAD_POST_API_KEY_2 ... _9.
    Each key is a separate Upload-Post account with Instagram and YouTube connected."""
    names = ["UPLOAD_POST_API_KEY"] + [f"UPLOAD_POST_API_KEY_{i}" for i in range(2, 10)]
    return [k for k in (os.environ.get(n, "").strip().lstrip("﻿") for n in names) if k]


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
    message = str(body.get("message") or body.get("error") or "")
    if r.status_code == 429 and "limit" in message.lower():
        raise LimitReached(message)
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


def video_url(slug: str) -> str:
    """Public link to the rendered video: the GitHub release asset (the repository must be public)."""
    repo = os.environ.get("GITHUB_REPOSITORY") or config().get("automation", {}).get("repo", "techwhyz26/tech-videos")
    return f"https://github.com/{repo}/releases/download/video-{slug}/{slug}.mp4"


def _direct_instagram() -> bool:
    return bool(config().get("automation", {}).get("instagram_direct")) and bool(os.environ.get("INSTAGRAM_TOKEN"))


def _direct_youtube() -> bool:
    """Upload to YouTube through Google's API first. Only once the Google project has passed YouTube's
    API audit (automation.youtube_audited); before that its uploads are locked private, so Upload-Post
    goes first and Google's API is only the fallback when Upload-Post is used up."""
    auto = config().get("automation", {})
    return bool(auto.get("youtube_direct")) and bool(auto.get("youtube_audited")) and youtube.configured()


def _youtube_fallback() -> bool:
    return bool(config().get("automation", {}).get("youtube_direct")) and youtube.configured()


def _youtube_upload(video: Path, spec: dict, when: dt.datetime | None) -> str:
    caption = spec.get("caption", spec["title"])
    audited = bool(config().get("automation", {}).get("youtube_audited"))
    try:
        link = youtube.upload_short(video, youtube.short_title(spec["title"]), f"{caption}\n\n#Shorts",
                                    _hashtags(caption) + ["shorts"], publish_at=when if audited else None,
                                    private=not audited)
    except (youtube.YouTubeError, httpx.HTTPError) as err:
        return f"FAILED: {err}"
    if not audited:
        return f"private {link}"
    return f"scheduled {link}" if when else link


def publish(spec: dict, video: Path | None = None, now: bool = False,
            only: list[str] | None = None) -> dict[str, str]:
    """Post an approved video. It goes into the next free slot of the posting schedule unless `now`.
    `only` limits it to some platforms, e.g. to retry one that failed; earlier results are kept.

    Instagram goes straight through Meta's API when automation.instagram_direct is on: it is queued for
    the slot and `post_due()` publishes it then. Other platforms go through Upload-Post."""
    if spec.get("status") not in ("approved", "published"):
        raise SystemExit(
            f"'{spec['slug']}' is not approved yet. Watch output/{spec['slug']}.mp4, "
            f"then run `python run.py approve {spec['slug']}`."
        )
    video = video or OUTPUT / f"{spec['slug']}.mp4"
    if not video.exists():
        raise SystemExit(f"{video} does not exist. Render it first with `python run.py build {spec['slug']}`.")

    platforms = only or config().get("automation", {}).get("platforms") or []
    direct = [p for p in platforms if p == "instagram" and _direct_instagram()]
    direct_yt = [p for p in platforms if p == "youtube" and _direct_youtube()]
    via_upload_post = [p for p in platforms if p not in direct and p not in direct_yt]
    keys = _keys()
    if not keys and not direct and not direct_yt:
        ready = OUTPUT / "ready"
        ready.mkdir(parents=True, exist_ok=True)
        shutil.copy2(video, ready / video.name)
        (ready / f"{spec['slug']}.txt").write_text(spec.get("caption", spec["title"]), encoding="utf-8")
        return {"manual": str(ready / video.name)}

    when = None if now else next_slot()
    results: dict[str, str] = {}
    if direct:
        if when:
            results["instagram"] = "queued"
        else:
            try:
                results["instagram"] = instagram.publish_reel(video_url(spec["slug"]), spec.get("caption", spec["title"]))
            except instagram.InstagramError as err:
                results["instagram"] = f"FAILED: {err}"
    if direct_yt:
        results["youtube"] = _youtube_upload(video, spec, when)
    if via_upload_post:
        for number, key in enumerate(keys, 1):  # use the accounts in turn; move on when one is used up
            try:
                results.update(_upload_post(video, spec, key, when, via_upload_post))
                spec["account"] = number
                break
            except LimitReached as err:
                print(f"  Upload-Post account {number} is used up for this month: {err}")
        else:
            reason = "Upload-Post's monthly uploads are used up" if keys else "no Upload-Post key"
            results.update({p: f"FAILED: {reason}" for p in via_upload_post})
            if "youtube" in via_upload_post and _youtube_fallback():
                results["youtube"] = _youtube_upload(video, spec, when)
    if results and all(str(v).startswith("FAILED") for v in results.values()):
        raise RuntimeError("Every platform failed: " + "; ".join(f"{p}: {v}" for p, v in results.items()))
    spec["status"] = "published"
    spec["posts"] = {**(spec.get("posts") or {}), **results} if only else results
    if when:
        spec["scheduled_for"] = when.isoformat()
    save_spec(spec)
    return results


def post_due(now: dt.datetime | None = None) -> list[tuple[dict, str]]:
    """Publish queued Instagram posts whose time has come. Returns [(spec, result)]."""
    now = now or dt.datetime.now(dt.timezone.utc)
    done = []
    for spec in all_specs():
        posts = spec.get("posts") or {}
        if posts.get("instagram") != "queued" or not spec.get("scheduled_for"):
            continue
        if dt.datetime.fromisoformat(spec["scheduled_for"]) > now:
            continue
        try:
            result = instagram.publish_reel(video_url(spec["slug"]), spec.get("caption", spec["title"]))
        except instagram.InstagramError as err:
            result = f"FAILED: {err}"
        posts["instagram"] = result
        spec["posts"] = posts
        save_spec(spec)
        done.append((spec, result))
    return done
