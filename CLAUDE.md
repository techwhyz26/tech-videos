# TechWhyz video pipeline

Short vertical (1080x1920) videos for the TechWhyz channel: the surprising technology behind what is trending
right now (launches, new tech, tech news). Remotion renders them, edge-tts voices them, and `run.py` drives everything.
The README covers the commands, scene types and spec format.

## The standard (non-negotiable)

The `qr-code-damage` and `microwave-wifi` videos are the approved look. Every new video must match them:

- **Every scene except the closing "Follow" title card is an `art` scene**: a custom animated SVG that
  draws the real thing the sentence talks about. A QR video shows a real QR code being torn, dirtied and
  scanned at an angle. A microwave video shows a microwave with a turning, steaming bowl next to a router
  with blinking LEDs and expanding waves. People, phones and screens are drawn when the sentence is
  about them.
- No generic icon-in-a-circle, no pills/hub/crowd/bar-chart templates standing in for a thing.
- Objects are big and solid, with gradients (`url(#metal)`, `url(#steel)`, `url(#screen)`, `url(#paper)`),
  soft ground shadows (`shadow()`), highlights and recognisable details. Each main object is drawn once as
  a function and reused across scenes at different sizes and positions with `place()`.
- Every scene moves (SMIL only): waves expanding, parts popping in, rotation, steam, LEDs, lines drawing.
- There are at most one or two short labels or a badge per scene. Labels never overlap the drawing,
  and nothing is cut off at the canvas edge.
- The theme varies from video to video (`violet ember matrix ocean gold crimson`).

`tools/art_qr.py` and `tools/art_microwave.py` are the reference. Read both before drawing anything new.

## Script format

The rules live in the `SYSTEM` prompt in `pipeline/script.py`, sections "THE SCRIPT" and "Other rules":
- hook -> "So..." question -> one-line answer -> story with "But here's the part most people miss" ->
  "So..." payoff -> "Follow, and send this to someone who ..." call to action
- 12-18 scenes, 150-210 spoken words
- numbers spelled out for the voice
- for news, only facts from the source

## Making one video (the daily cloud job follows this)

1. **Choose the subject.** The channel lives on what people are talking about *right now*: big launches
   (games, phones, consoles, AI models, rockets, cars), viral gadgets, and tech in the headlines this
   week. Never make a video about something most people already know (how Wi-Fi, touchscreens or QR
   codes work). The angle is the surprising technology inside the trending thing, e.g. for a new game,
   how the console draws its world.
   - News: `python run.py topics`, then read `data/topics.json`. Also use WebSearch for what is trending
     in tech and gaming this week. Pick the story the most people will be curious about whose inner
     workings can be drawn. Skip funding, lawsuits, politics, layoffs, executives, opinion. If it came
     from topics.json, run `python run.py mark-used <number>`.
   - Explainer: the technology behind something trending this week, found with WebSearch.
   - Check `public/videos/*/spec.json` titles so a subject is never repeated.
   - Facts: read the articles with WebFetch and use only facts stated by at least one source, keeping
     estimates as estimates ("an estimated ..."). Put the main article in `source`.
2. **Pick a slug** (lowercase-hyphenated, at most 40 characters) and a theme different from the latest
   video's.
3. **Write the drawings** as `tools/art_<slug_with_underscores>.py` in the style of `tools/art_microwave.py`.
   Import from `artlib`, set `SLUG`, define reusable object functions, and `save()` one drawing per scene.
   Run it from the project root: `python tools/art_<name>.py`.
4. **Write `public/videos/<slug>/spec.json`**. Copy the structure of
   `public/videos/microwave-wifi/spec.json` but leave out `audio`, `words`, `durationMs` and `posts`. Set
   `"status": "scripted"`, `"brand": {"name": "TechWhyz"}`, a `caption` with 4-6 hashtags, and for news a
   `"source": {"title": ..., "link": ...}`. Scenes use `{"type": "art", "props": {"art": "<name>"}}`.
5. **Build**: `python run.py build <slug>` (voice + render, several minutes).
6. **Check by eye**: `python run.py frames <slug>`, then open the contact sheet PNG it prints. Look at
   every scene for:
   - objects cut off at the edges
   - labels overlapping drawings
   - text too small to read on a phone
   - empty or near-empty scenes
   - a drawing that does not show what its sentence says
   - anything that looks like a template rather than the real thing

   Fix the art script, rerun it, and build again. Do at most two fix rounds.
7. **Finish**: write `output/last.json` as `{"slug": "<slug>", "title": "<title>"}`. The workflow then
   commits, stores the video and sends it to Telegram. Do not commit, push or send anything yourself.

Do not change pipeline code, workflows, config or other videos while making a video.
