"""Telegram review: send each new video to your phone with Approve / Reject buttons, and read the taps.

Needs two environment variables (GitHub secrets when it runs in the cloud):
  TELEGRAM_BOT_TOKEN   from @BotFather
  TELEGRAM_CHAT_ID     your own chat id (`python run.py telegram-setup` prints it)

There is no server listening for taps. A scheduled job calls `poll()` every hour, so a tap is acted on
within about an hour. Telegram keeps unread taps for 24 hours.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

import httpx

API = "https://api.telegram.org/bot{token}/{method}"


def _token() -> str:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip().lstrip("﻿")
    if not token:
        raise SystemExit("TELEGRAM_BOT_TOKEN is not set. See AUTOMATION.md, step 3.")
    return token


def _chat() -> str:
    chat = os.environ.get("TELEGRAM_CHAT_ID", "").strip().lstrip("﻿")
    if not chat:
        raise SystemExit("TELEGRAM_CHAT_ID is not set. Run `python run.py telegram-setup`.")
    return chat


def _call(method: str, timeout: float = 60, files: dict | None = None, **params) -> dict:
    data = {k: (json.dumps(v) if isinstance(v, (dict, list)) else v) for k, v in params.items() if v is not None}
    for attempt in range(4):  # cloud runners sometimes get a connection reset; try again
        try:
            if files:
                for _, f in files.items():
                    f[1].seek(0)
            r = httpx.post(API.format(token=_token(), method=method), data=data, files=files, timeout=timeout)
            break
        except httpx.TransportError:
            if attempt == 3:
                raise
            time.sleep(5 * (attempt + 1))
    body = r.json()
    if not body.get("ok"):
        raise RuntimeError(f"Telegram {method} failed: {body.get('description', r.text)}")
    return body["result"]


def send_message(text: str, reply_to: int | None = None) -> None:
    _call("sendMessage", chat_id=_chat(), text=text[:4000], reply_to_message_id=reply_to,
          link_preview_options={"is_disabled": True})


def send_for_review(spec: dict, video: Path) -> int:
    """Send the video with its caption and two buttons. Returns the Telegram message id."""
    slug = spec["slug"]
    caption = f"{spec['title']}\n\n{spec.get('caption', '')}"
    if spec.get("source"):
        caption += f"\n\nSource: {spec['source']['link']}"
    buttons = {"inline_keyboard": [[
        # Telegram allows 64 bytes of button data; slugs are at most 60 characters.
        {"text": "✅ Post it", "callback_data": f"a:{slug}"},
        {"text": "❌ Reject", "callback_data": f"r:{slug}"},
    ]]}
    if video.stat().st_size > 49 * 1024 * 1024:  # bots can upload at most 50 MB
        raise SystemExit(f"{video.name} is over Telegram's 50 MB limit.")
    with video.open("rb") as f:
        msg = _call("sendVideo", timeout=300, files={"video": (video.name, f, "video/mp4")},
                    chat_id=_chat(), caption=caption[:1024], reply_markup=buttons,
                    supports_streaming=True, width=1080, height=1920)
    return msg["message_id"]


def send_youtube_kit(spec: dict, video: Path, title: str, description: str, tags: list[str],
                     when_text: str, reply_to: int | None = None) -> None:
    """Everything needed to upload a video to YouTube by hand, one message per field so each can be
    copied with a long press: the original video file, the title, the description and the tags."""
    send_message(f"📋 YouTube upload kit for '{spec['title']}'\n\n"
                 "1. Save the video file below and upload it in the YouTube app or studio.youtube.com\n"
                 "2. Copy the title, description and tags from the next messages\n"
                 f"3. Visibility: Schedule it for {when_text}" if when_text else
                 f"📋 YouTube upload kit for '{spec['title']}'\n\n"
                 "1. Save the video file below and upload it in the YouTube app or studio.youtube.com\n"
                 "2. Copy the title, description and tags from the next messages\n"
                 "3. Visibility: Public", reply_to=reply_to)
    with video.open("rb") as f:  # as a file, so Telegram does not shrink the quality
        _call("sendDocument", timeout=300, files={"document": (video.name, f, "video/mp4")},
              chat_id=_chat(), caption="Video file (full quality)")
    send_message(title)
    send_message(description)
    send_message(", ".join(tags))


def poll() -> list[dict]:
    """Return the button taps since the last poll: [{action, slug, message_id}], oldest first.
    Only taps from TELEGRAM_CHAT_ID count; anyone else who finds the bot is ignored."""
    chat = _chat()
    updates = _call("getUpdates", timeout=30, allowed_updates=["callback_query"])
    taps = []
    for u in updates:
        q = u.get("callback_query")
        if not q or str(q.get("message", {}).get("chat", {}).get("id")) != chat:
            continue
        code, _, slug = str(q.get("data", "")).partition(":")
        action = {"a": "approve", "r": "reject"}.get(code)
        if action and slug:
            taps.append({"action": action, "slug": slug, "message_id": q["message"]["message_id"],
                         "callback_id": q["id"]})
    if updates:  # confirm them so Telegram does not send them again
        _call("getUpdates", offset=updates[-1]["update_id"] + 1, timeout=30)
    return taps


def acknowledge(tap: dict, text: str) -> None:
    """Remove the buttons from the review message and reply under it."""
    try:
        _call("answerCallbackQuery", callback_query_id=tap["callback_id"], text=text[:190])
    except RuntimeError:
        pass  # taps older than a few minutes can no longer be answered; that is fine
    try:
        _call("editMessageReplyMarkup", chat_id=_chat(), message_id=tap["message_id"],
              reply_markup={"inline_keyboard": []})
    except RuntimeError:
        pass
    send_message(text, reply_to=tap["message_id"])


def find_chat_id() -> list[tuple[str, str]]:
    """List (chat id, name) of everyone who has messaged the bot recently."""
    seen = {}
    for u in _call("getUpdates", timeout=30, allowed_updates=["message", "callback_query"]):
        msg = u.get("message") or {}
        chat = msg.get("chat") or {}
        if chat.get("id"):
            seen[str(chat["id"])] = chat.get("first_name") or chat.get("title") or chat.get("username", "")
    return list(seen.items())
