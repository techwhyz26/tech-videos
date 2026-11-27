"""Upload Shorts straight to YouTube through Google's own YouTube Data API (free).

Needs three values, saved once by `python tools/youtube_auth.py`:
  YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET   the OAuth client of your Google Cloud project
  YOUTUBE_REFRESH_TOKEN                      permission to upload to your channel (does not expire while
                                             the project's OAuth app is "In production")

The free daily quota covers several uploads a day. YouTube schedules natively: a video uploaded as
private with `publishAt` goes public by itself at that time.

Note: Google keeps videos uploaded by a project that has not passed its (free) API audit private.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import time
from pathlib import Path

import httpx

TOKEN_URL = "https://oauth2.googleapis.com/token"
UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/videos"
VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"
CHANNELS_URL = "https://www.googleapis.com/youtube/v3/channels"


class YouTubeError(RuntimeError):
    pass


def _env(name: str) -> str:
    return os.environ.get(name, "").strip().lstrip("﻿")


def configured() -> bool:
    return all(_env(n) for n in ("YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN"))


def access_token() -> str:
    if not configured():
        raise YouTubeError("YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET and YOUTUBE_REFRESH_TOKEN must be set.")
    r = httpx.post(TOKEN_URL, data={"client_id": _env("YOUTUBE_CLIENT_ID"),
                                    "client_secret": _env("YOUTUBE_CLIENT_SECRET"),
                                    "refresh_token": _env("YOUTUBE_REFRESH_TOKEN"),
                                    "grant_type": "refresh_token"}, timeout=60)
    body = r.json()
    if "access_token" not in body:
        raise YouTubeError(f"YouTube sign-in failed: {body.get('error_description') or body.get('error') or r.text[:300]}")
    return body["access_token"]


def channel() -> dict:
    """{'id': ..., 'title': ...} of the channel the token uploads to."""
    r = httpx.get(CHANNELS_URL, params={"part": "snippet", "mine": "true"},
                  headers={"Authorization": f"Bearer {access_token()}"}, timeout=60)
    items = r.json().get("items") or []
    if not items:
        raise YouTubeError(f"No YouTube channel found for this sign-in: {r.text[:300]}")
    return {"id": items[0]["id"], "title": items[0]["snippet"]["title"]}


def upload_short(video: Path, title: str, description: str, tags: list[str],
                 publish_at: dt.datetime | None = None, private: bool = False) -> str:
    """Upload a Short. With `publish_at` it stays private until then and YouTube makes it public by
    itself. Returns the video's link."""
    status: dict = {"selfDeclaredMadeForKids": False, "embeddable": True}
    if publish_at:
        status["privacyStatus"] = "private"
        status["publishAt"] = publish_at.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        status["privacyStatus"] = "private" if private else "public"
    meta = {"snippet": {"title": title[:100], "description": description[:4900],
                        "tags": [t for t in tags if t][:30], "categoryId": "28"},  # Science & Technology
            "status": status}
    size = video.stat().st_size
    token = access_token()
    r = httpx.post(UPLOAD_URL, params={"uploadType": "resumable", "part": "snippet,status"},
                   headers={"Authorization": f"Bearer {token}",
                            "Content-Type": "application/json; charset=UTF-8",
                            "X-Upload-Content-Type": "video/mp4",
                            "X-Upload-Content-Length": str(size)},
                   content=json.dumps(meta), timeout=60)
    if r.status_code >= 400 or "location" not in r.headers:
        raise YouTubeError(f"YouTube refused the upload ({r.status_code}): {_reason(r)}")
    session = r.headers["location"]
    for attempt in range(4):
        try:
            with video.open("rb") as f:
                r = httpx.put(session, content=f.read(), timeout=900,
                              headers={"Authorization": f"Bearer {token}", "Content-Type": "video/mp4"})
            break
        except httpx.TransportError:
            if attempt == 3:
                raise
            time.sleep(10 * (attempt + 1))
    if r.status_code >= 400:
        raise YouTubeError(f"YouTube upload failed ({r.status_code}): {_reason(r)}")
    return f"https://www.youtube.com/shorts/{r.json()['id']}"


def _reason(r: httpx.Response) -> str:
    try:
        err = r.json().get("error", {})
        return err.get("message") or str(err)[:300]
    except ValueError:
        return r.text[:300]


def short_title(title: str) -> str:
    """YouTube titles: at most 100 characters, no angle brackets."""
    return re.sub(r"[<>]", "", title).strip()[:95]
