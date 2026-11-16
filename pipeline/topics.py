"""Step 1 - find fresh technology stories from RSS feeds."""
from __future__ import annotations

import html
import json
import re
import time

import feedparser

from .common import DATA, config

MAX_AGE_DAYS = 3


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", text or ""))).strip()


def _used() -> set[str]:
    path = DATA / "used.json"
    return set(json.loads(path.read_text(encoding="utf-8"))) if path.exists() else set()


def mark_used(link: str) -> None:
    used = _used() | {link}
    DATA.mkdir(exist_ok=True)
    (DATA / "used.json").write_text(json.dumps(sorted(used), indent=2), encoding="utf-8")


def find_topics(limit: int = 25) -> list[dict]:
    """Fetch every feed in config.json and return recent, not-yet-used stories, newest first."""
    used = _used()
    seen: set[str] = set()
    topics: list[dict] = []
    now = time.time()
    for url in config()["feeds"]:
        feed = feedparser.parse(url, agent="Mozilla/5.0 (compatible; video-pipeline)")
        if not feed.entries:
            print(f"  (no entries from {url})")
            continue
        source = _clean(feed.feed.get("title", url))
        for entry in feed.entries[:30]:
            title = _clean(entry.get("title", ""))
            link = entry.get("link", "")
            stamp = entry.get("published_parsed") or entry.get("updated_parsed")
            published = time.mktime(stamp) if stamp else now
            key = title.lower()
            if not title or link in used or key in seen:
                continue
            if now - published > MAX_AGE_DAYS * 86400:
                continue
            seen.add(key)
            topics.append(
                {
                    "title": title,
                    "link": link,
                    "source": source,
                    "summary": _clean(entry.get("summary", ""))[:1200],
                    "published": published,
                }
            )
    topics.sort(key=lambda t: t["published"], reverse=True)
    topics = topics[:limit]
    DATA.mkdir(exist_ok=True)
    (DATA / "topics.json").write_text(json.dumps(topics, indent=2, ensure_ascii=False), encoding="utf-8")
    return topics


def load_topics() -> list[dict]:
    path = DATA / "topics.json"
    if not path.exists():
        raise SystemExit("No topic list yet. Run `python run.py topics` first.")
    return json.loads(path.read_text(encoding="utf-8"))
