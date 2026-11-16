"""Step 2 - turn an idea or news story into a video spec (script + drawings) with Claude.

The standard every video must meet is the 'qr-code-damage' and 'microwave-wifi' videos: every scene
except the closing call to action is a custom animated drawing of the real thing being talked about.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import anthropic

from .common import VIDEOS, config, save_spec, slugify, spec_path, validate

EXAMPLE = (Path(__file__).parent / "example_art.svg").read_text(encoding="utf-8")

SYSTEM = """You write and illustrate 50-75 second vertical videos (Reels / Shorts / TikTok) for a channel about
how technology works and what is new in technology. Each video is a fast sequence of scenes with a
voiceover and word-by-word captions. Almost every scene is a custom animated drawing you make yourself.

Return ONLY a JSON object, no prose and no code fences, with this shape:
{
  "title": "short working title",
  "theme": "violet" | "ember" | "matrix" | "ocean" | "gold" | "crimson"  (pick the mood that suits the topic),
  "caption": "social media caption, 1-3 sentences, then a blank line, then 4-6 hashtags",
  "scenes": [ { "type": "art", "narration": ..., "emphasis": [...], "props": {"svg": "..."} }, ...,
              { "type": "title", "narration": "Follow, and send this to someone who ...", "emphasis": [...],
                "props": {"headline": "Follow for more", "highlight": ["Follow"], "sub": "short line"} } ]
}

THE SCRIPT (this is what keeps people watching)
There are two kinds of video. The user message says which one.

A. HOW IT WORKS (a curious, existing technology):
1. HOOK: one concrete, surprising fact about something the viewer owns or uses. No greeting, no "did
   you know", no "in this video". Example: "You can rip off almost a third of a QR code, and it will still scan."
2. QUESTION, starting with "So": the question the hook raises.
3. ANSWER IN ONE LINE that opens a new gap: "Because every QR code quietly carries a backup of itself."
4. THE STORY: how it works, as things the viewer can picture. Chain lines with "But", "So", "Then",
   "Which is why". Real numbers and names. Around the middle: "But here's the part most people miss."
5. PAYOFF starting with "So" that restates the hook as something the viewer now understands.
6. CALL TO ACTION, the only non-art scene: "Follow, and send this to someone who ...", tied to the topic.

B. TECH UPDATE / NEWS (something just announced or released):
1. HOOK: the news as a concrete, surprising change to something the viewer uses. Name who did it.
2. QUESTION, starting with "So": "So what actually changed?" or the sharper question it raises.
3. WHAT IT IS in one line, in plain words.
4. HOW IT WORKS: the technology behind it, drawn and explained step by step like a type A video. This
   is most of the video. Include the re-hook "But here's the part most people miss."
5. WHAT IT MEANS for the viewer: when they get it, what it costs, what changes, what the catch is
   (only what the source says).
6. PAYOFF starting with "So", then the CALL TO ACTION title scene as above.
For news, only use facts from the source material given. Never invent dates, prices, numbers or quotes.
If the source does not say something, do not say it.

Voice: curious, warm and conversational, like a friend who just found out something fascinating. Short
sentences. Second person ("your phone"). No hype words, no jargon without explaining it.

THE DRAWINGS
Every scene except the last is "type": "art" with "props": {"svg": "..."}. "svg" is the INNER markup
of an <svg viewBox="0 0 1000 1000"> (no outer <svg> tag).

The bar to meet (an approved scene is shown at the end of this prompt):
- Show the REAL THING the sentence is about. A QR code video shows an actual QR code being torn, dirtied,
  scanned at an angle. A microwave video shows a microwave with a window, a turning, steaming bowl, a
  timer and buttons, next to a router with antennas, blinking lights and waves expanding from it. If
  the sentence is about a person, draw the person. If it is about a phone, draw the phone and what is
  on its screen. If it is about a number, draw the objects that number describes. Never a generic
  icon in a circle, never a bullet list, never a bar chart standing in for a thing.
- Draw objects big and solid: they fill most of the canvas (main drawing inside x 20-980, y 100-800).
  Give them depth with the shared gradients and a soft ground shadow (see below), highlights, panels,
  screws, LEDs, screens: the details that make the object recognisable.
- Define each main object once in your head and draw it the same way in every scene it appears in, at
  different sizes and positions (wrap it in <g transform="translate(x y) scale(s)">), so the video
  feels like one world.
- Every scene moves: waves expanding, parts sliding or popping in, things rotating, a signal
  travelling, a line drawing itself, steam rising, LEDs blinking. Stage it: the main object first,
  then the thing that happens (0.3-1.5 s), then a label or badge (1-2 s).
- At most one or two short labels per scene, on parts or below the drawing at y 840-920, font-size
  40-50, text-anchor="middle". One pill-shaped badge (rect rx about 20, accent fill, dark bold text) is
  fine for the key takeaway. Big display numbers (font-size 100-180, class "display") are fine when
  the sentence is about a number.
- Consecutive scenes must look different: change the camera (whole object, close-up, cut-away, side by
  side, before and after) rather than repeating a layout.

Technical rules for drawings:
- Animate with SMIL only: <animate>, <animateTransform>, <animateMotion>. No CSS animation, no script,
  no external images or fonts. One-off animations need fill="freeze" and a begin time in seconds;
  looping ones use repeatCount="indefinite". Things that appear later start with opacity="0" and
  animate to 1.
- Theme colour classes: fa / sa (accent fill / stroke), fa2 / sa2 (second colour), fw / sw (white),
  fb (background), nf (no fill), "display" on <text> for the headline font. Plain hex colours are right
  for real-world materials (metal, plastic, wood, skin, food, paper, screens).
- Shared definitions you can use without defining them: gradients url(#metal) (dark device body),
  url(#steel) (light grey plastic or metal), url(#screen) (dark glass), url(#paper) (white card);
  filters url(#soft) (heavy blur, for ground shadows and glows) and url(#glow).
  A ground shadow: <ellipse cx=".." cy=".." rx=".." ry="22" fill="#000" opacity="0.55" filter="url(#soft)"/>
- Any ids you define yourself (clipPath, gradients) must be unique and prefixed with the scene number,
  for example id="s4win".
- Expanding waves: a <circle> whose r animates from small to large while opacity goes 0 -> 0.9 -> 0,
  three copies offset in begin time, repeatCount="indefinite".
- Keep each drawing under about 25 KB: draw repeated dots or modules with as few elements as is
  reasonable.

Other rules:
- 12 to 18 scenes, 150 to 210 spoken words in total. One or two short sentences (at most 18 words) per
  scene, so the picture changes every two to five seconds.
- "emphasis" lists 1-2 single words copied exactly from that scene's narration to highlight in captions.
- The narration is read by a text-to-speech voice: spell out numbers and symbols ("eighty percent"),
  avoid abbreviations it would mispronounce, and use plain everyday language.
- Be accurate. Only state facts you are confident about; when source material is given, do not go
  beyond it. Prefer explaining how something works over hype.
- Draw company products generically (a phone, a laptop, a car). Do not draw logos; write company or
  product names as plain text labels only.

An approved scene from a finished video, for the sentence "Your microwave and your Wi-Fi are using almost
exactly the same radio waves." Match this level of detail and motion:
<example>
""" + EXAMPLE + """
</example>
"""


def _extract_json(text: str) -> dict:
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("the model did not return JSON")
    return json.loads(text[start : end + 1])


def _standard_problems(spec: dict) -> list[str]:
    """Checks that the spec meets the house standard: drawings everywhere except the closing CTA."""
    scenes = spec.get("scenes", [])
    problems = []
    for i, sc in enumerate(scenes[:-1]):
        if sc.get("type") != "art" or not str(sc.get("props", {}).get("svg", "")).strip():
            problems.append(f"scene {i + 1} is '{sc.get('type')}' - every scene except the last must be an art drawing")
    if scenes and scenes[-1].get("type") != "title":
        problems.append("the last scene must be the 'title' call to action")
    return problems


def _ask(client: anthropic.Anthropic, model: str, request: str, feedback: str | None = None) -> dict:
    messages = [{"role": "user", "content": request}]
    if feedback:
        messages[0]["content"] += "\n\nA previous attempt had these problems, avoid them:\n" + feedback
    # Server-side fallback: if the main model declines, the API retries on a fallback model.
    # Drawings make the reply long, so stream it to avoid HTTP timeouts. The long system prompt is cached.
    with client.beta.messages.stream(
        model=model,
        max_tokens=64000,
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        system=[{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
        messages=messages,
    ) as stream:
        response = stream.get_final_message()
    if response.stop_reason == "refusal":
        raise SystemExit("Claude declined to write this script. Try a different topic.")
    if response.stop_reason == "max_tokens":
        raise ValueError("the reply was cut off before it finished")
    return _extract_json("".join(block.text for block in response.content if block.type == "text"))


def _store_drawings(spec: dict) -> None:
    """Move each inline drawing into art/scene-NN.svg so it can be edited and previewed on its own."""
    folder = VIDEOS / spec["slug"] / "art"
    folder.mkdir(parents=True, exist_ok=True)
    for i, sc in enumerate(spec["scenes"]):
        svg = sc.get("props", {}).pop("svg", None)
        if sc.get("type") == "art" and svg:
            name = f"scene-{i + 1:02d}"
            (folder / f"{name}.svg").write_text(svg, encoding="utf-8")
            sc["props"]["art"] = name


def pick_topic(found: list[dict]) -> int:
    """Ask Claude which news story makes the best video. Returns an index into `found`."""
    cfg = config()
    listing = "\n".join(f"{i + 1}. {t['title']} ({t['source']}): {t['summary'][:200]}" for i, t in enumerate(found))
    try:
        response = anthropic.Anthropic().messages.create(
            model=cfg["script_model"],
            max_tokens=20,
            messages=[{"role": "user", "content": (
                f"Channel niche: {cfg['niche']}\n\nToday's technology stories:\n{listing}\n\n"
                "Which ONE story makes the best short video for a general audience: a new technology or "
                "product update people will care about, where the technology behind it can be explained "
                "and drawn (devices, parts, how it works)? Avoid funding rounds, lawsuits, politics, "
                "layoffs and opinion pieces. Reply with only the number.")}],
        )
    except TypeError as err:
        raise SystemExit(f"Claude credentials not found ({err}). See README: 'Script writing'.")
    digits = re.findall(r"\d+", "".join(b.text for b in response.content if b.type == "text"))
    n = int(digits[0]) if digits else 1
    return n - 1 if 1 <= n <= len(found) else 0


def suggest_idea(done_titles: list[str]) -> str:
    """Ask Claude for one fresh 'how does it work' idea that the channel has not covered yet."""
    cfg = config()
    done = "\n".join(f"- {t}" for t in done_titles) or "- (none yet)"
    try:
        response = anthropic.Anthropic().messages.create(
            model=cfg["script_model"],
            max_tokens=300,
            messages=[{"role": "user", "content": (
                f"Channel niche: {cfg['niche']}\n\nVideos already made:\n{done}\n\n"
                "Suggest ONE new video about how a piece of everyday technology works, with a surprising "
                "fact a general audience would not expect and that can be shown with drawings of real "
                "objects (devices, parts, people). Different from every video above. Reply with only the "
                "idea as one line, for example: How a QR code still scans when a third of it is torn off")}],
        )
    except TypeError as err:
        raise SystemExit(f"Claude credentials not found ({err}). See README: 'Script writing'.")
    idea = "".join(b.text for b in response.content if b.type == "text").strip().strip('"')
    if not idea:
        raise SystemExit("Claude did not suggest an idea.")
    return idea.splitlines()[0]


def write_spec(idea: str, source: dict | None = None, kind: str | None = None) -> dict:
    """Ask Claude for a spec. `source` is an optional topic dict from topics.py.
    `kind` is "explainer" or "news"; a source defaults to news, an idea to explainer."""
    cfg = config()
    kind = kind or ("news" if source else "explainer")
    request = (f"Niche of the channel: {cfg['niche']}\n\n"
               f"Kind of video: {'B. TECH UPDATE / NEWS' if kind == 'news' else 'A. HOW IT WORKS'}\n\n"
               f"Video idea: {idea}")
    if source:
        request += (
            f"\n\nSource material ({source['source']}):\n"
            f"Headline: {source['title']}\nSummary: {source['summary']}"
        )

    client = anthropic.Anthropic()
    feedback = None
    try:
        for attempt in range(3):
            try:
                spec = _ask(client, cfg["script_model"], request, feedback)
            except (ValueError, json.JSONDecodeError) as err:
                feedback = f"- {err}"
                continue
            problems = _standard_problems(spec)
            if not problems:
                break
            feedback = "\n".join(f"- {p}" for p in problems)
        else:
            raise SystemExit("Claude could not produce a script that meets the standard:\n" + (feedback or ""))
    except TypeError as err:
        # Raised before any network call when no API key / login is configured.
        raise SystemExit(f"Claude credentials not found ({err}). See README: 'Script writing'.")
    except anthropic.AuthenticationError:
        raise SystemExit("Claude rejected the API key. Check ANTHROPIC_API_KEY.")
    except anthropic.RateLimitError:
        raise SystemExit("Claude rate limit hit. Wait a minute and run the command again.")
    except anthropic.APIStatusError as err:
        raise SystemExit(f"Claude API error {err.status_code}: {err.message}")
    except anthropic.APIConnectionError:
        raise SystemExit("Could not reach the Claude API. Check your internet connection.")

    spec["slug"] = slugify(spec.get("title") or idea)
    if spec_path(spec["slug"]).exists():
        spec["slug"] += "-2"
    spec["brand"] = cfg["brand"]
    spec["status"] = "scripted"
    spec["kind"] = kind
    if source:
        spec["source"] = {"title": source["title"], "link": source["link"]}

    _store_drawings(spec)
    errors = validate(spec)
    if errors:
        raise SystemExit("The generated script has problems:\n  " + "\n  ".join(errors))
    save_spec(spec)
    return spec
