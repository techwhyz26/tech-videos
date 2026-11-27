"""Post Reels straight to Instagram through Meta's own API.

Free, no monthly limit (Instagram allows up to 100 API posts a day). Needs:
  INSTAGRAM_TOKEN    either
                       - a system-user token from the app's "API setup with Unified login" (starts with
                         "EAA", never expires; uses graph.facebook.com), or
                       - an Instagram-login token (starts with "IG", valid 60 days, refreshed weekly by the
                         "Refresh Instagram token" workflow; uses graph.instagram.com)
  INSTAGRAM_USER_ID  optional: the Instagram account id to post as. Found from the token when not set.

Instagram downloads the video itself from a public link, so the video must be at a public URL: the
GitHub release asset of this (public) repository. The API has no scheduling, so the posting job calls
`publish_reel` when a video's time slot comes round.
"""
from __future__ import annotations

import os
import time

import httpx

VERSION = "v27.0"


class InstagramError(RuntimeError):
    pass


def token() -> str:
    tok = os.environ.get("INSTAGRAM_TOKEN", "").strip().lstrip("﻿")
    if not tok:
        raise InstagramError("INSTAGRAM_TOKEN is not set.")
    return tok


_HOST: dict[str, str] = {}


def _instagram_login() -> bool:
    """True when the token works with graph.instagram.com (Instagram login), False when it is a
    Facebook-style token for graph.facebook.com. Tried once, then remembered."""
    if "host" not in _HOST:
        try:
            r = httpx.get(f"https://graph.instagram.com/{VERSION}/me",
                          params={"fields": "user_id,username", "access_token": token()}, timeout=60)
            ok = r.status_code == 200 and "user_id" in r.json()
        except (httpx.HTTPError, ValueError):
            ok = token().startswith("IG")
        _HOST["host"] = "graph.instagram.com" if ok else "graph.facebook.com"
    return _HOST["host"] == "graph.instagram.com"


def _api() -> str:
    host = "graph.instagram.com" if _instagram_login() else "graph.facebook.com"
    return f"https://{host}/{VERSION}"


def _call(method: str, path: str, **params) -> dict:
    params["access_token"] = token()
    for attempt in range(4):
        try:
            r = httpx.request(method, f"{_api()}/{path}", params=params if method == "GET" else None,
                              data=params if method != "GET" else None, timeout=120)
            break
        except httpx.TransportError:
            if attempt == 3:
                raise
            time.sleep(5 * (attempt + 1))
    try:
        body = r.json()
    except ValueError:
        raise InstagramError(f"Instagram {path}: HTTP {r.status_code} {r.text[:300]}")
    if r.status_code >= 400 or "error" in body:
        err = body.get("error", {})
        raise InstagramError(f"Instagram {path}: {err.get('message') or r.text[:300]}")
    return body


def _user_id() -> str:
    """Id of the Instagram account to post as."""
    if os.environ.get("INSTAGRAM_USER_ID", "").strip():
        return os.environ["INSTAGRAM_USER_ID"].strip()
    try:
        from .common import config
        configured = str(config().get("automation", {}).get("instagram_user_id", "")).strip()
    except Exception:
        configured = ""
    if _instagram_login():
        body = _call("GET", "me", fields="user_id")
        return str((body["data"][0] if "data" in body else body)["user_id"])
    # System-user token: the Instagram account it was given is listed in its granular scopes.
    if configured:
        return configured
    try:
        info = _call("GET", "debug_token", input_token=token()).get("data", {})
    except InstagramError:
        info = {}
    for scope in info.get("granular_scopes", []):
        if scope.get("scope") == "instagram_content_publish" and scope.get("target_ids"):
            return str(scope["target_ids"][0])
    for scope in info.get("granular_scopes", []):
        if scope.get("scope") == "instagram_basic" and scope.get("target_ids"):
            return str(scope["target_ids"][0])
    raise InstagramError("Could not find the Instagram account for this token. "
                         "Set the INSTAGRAM_USER_ID secret.")


def me() -> dict:
    """{'user_id': ..., 'username': ...} of the account the token posts as."""
    uid = _user_id()
    body = _call("GET", uid, fields="username")
    return {"user_id": uid, "username": body.get("username", "")}


def publish_reel(video_url: str, caption: str, wait_minutes: int = 15) -> str:
    """Post a Reel (also shown in the feed) and return its link."""
    user = _user_id()
    # GitHub release links redirect to a temporary storage address (valid about an hour); give Instagram
    # that final address so it does not have to follow the redirect itself.
    try:
        with httpx.stream("GET", video_url, follow_redirects=True, timeout=60) as r:
            if r.status_code == 200:
                video_url = str(r.url)
    except httpx.HTTPError:
        pass
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


def needs_refresh() -> bool:
    """Only Instagram-login tokens expire; system-user tokens never do."""
    return _instagram_login() and token().startswith("IG")


def refresh() -> str:
    """A fresh 60-day Instagram-login token. The token must be at least a day old."""
    r = httpx.get("https://graph.instagram.com/refresh_access_token",
                  params={"grant_type": "ig_refresh_token", "access_token": token()}, timeout=60)
    body = r.json()
    if "access_token" not in body:
        raise InstagramError(f"Token refresh failed: {body.get('error', {}).get('message') or r.text[:300]}")
    return body["access_token"]
