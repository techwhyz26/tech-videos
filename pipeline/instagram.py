"""Post Reels straight to Instagram through Meta's own API ("Instagram API with Instagram Login").

Free, no monthly limit (Instagram allows up to 100 API posts a day). Needs:
  INSTAGRAM_TOKEN   long-lived token from the Meta app dashboard (valid 60 days, refreshed weekly by the
                    "Refresh Instagram token" workflow)

Instagram downloads the video itself from a public link, so the video must be at a public URL: the
GitHub release asset of this (public) repository. The API has no scheduling, so the posting job calls
`publish_reel` when a video's time slot comes round.
"""
from __future__ import annotations

import os
import time

import httpx

API = "https://graph.instagram.com/v27.0"


class InstagramError(RuntimeError):
    pass


def token() -> str:
    tok = os.environ.get("INSTAGRAM_TOKEN", "").strip().lstrip("﻿")
    if not tok:
        raise InstagramError("INSTAGRAM_TOKEN is not set.")
    return tok


def _call(method: str, path: str, **params) -> dict:
    params["access_token"] = token()
    for attempt in range(4):
        try:
            r = httpx.request(method, f"{API}/{path}", params=params if method == "GET" else None,
                              data=params if method != "GET" else None, timeout=120)
            break
        except httpx.TransportError:
            if attempt == 3:
                raise
            time.sleep(5 * (attempt + 1))
    body = r.json()
    if r.status_code >= 400 or "error" in body:
        err = body.get("error", {})
        raise InstagramError(f"Instagram {path}: {err.get('message') or r.text[:300]}")
    return body


def me() -> dict:
    """{'user_id': ..., 'username': ...} of the account the token belongs to."""
    body = _call("GET", "me", fields="user_id,username")
    return body["data"][0] if "data" in body else body


def publish_reel(video_url: str, caption: str, wait_minutes: int = 15) -> str:
    """Post a Reel (also shown in the feed) and return its link."""
    user = me()["user_id"]
    container = _call("POST", f"{user}/media", media_type="REELS", video_url=video_url,
                      caption=caption[:2200], share_to_feed="true")["id"]
    status = ""
    for _ in range(wait_minutes * 2):  # Instagram fetches and processes the video first
        time.sleep(30)
        status = _call("GET", container, fields="status_code,status").get("status_code", "")
        if status in ("FINISHED", "ERROR", "EXPIRED"):
            break
    if status != "FINISHED":
        detail = _call("GET", container, fields="status_code,status")
        raise InstagramError(f"Instagram could not process the video ({status or 'timed out'}): "
                             f"{detail.get('status', '')}")
    media = _call("POST", f"{user}/media_publish", creation_id=container)["id"]
    try:
        return _call("GET", media, fields="permalink").get("permalink") or f"posted (id {media})"
    except InstagramError:
        return f"posted (id {media})"


def refresh() -> str:
    """A fresh 60-day token. The token must be at least a day old."""
    r = httpx.get("https://graph.instagram.com/refresh_access_token",
                  params={"grant_type": "ig_refresh_token", "access_token": token()}, timeout=60)
    body = r.json()
    if "access_token" not in body:
        raise InstagramError(f"Token refresh failed: {body.get('error', {}).get('message') or r.text[:300]}")
    return body["access_token"]
