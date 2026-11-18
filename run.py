"""Video pipeline command line.

  python run.py topics                 find fresh tech stories
  python run.py make --topic 3         script + voice + render story number 3
  python run.py make --idea "..."      script + voice + render your own idea
  python run.py build <slug>           voice + render an existing spec (after editing it)
  python run.py demo                   build the bundled sample video
  python run.py status                 list videos and where each one is
  python run.py voices                 write the same lines in six voices to compare by ear
  python run.py approve <slug>         mark a rendered video as OK to post
  python run.py publish <slug>         post an approved video

  Automation (see AUTOMATION.md):
  python run.py auto                   pick a topic, make the video, send it to Telegram for review
  python run.py review                 post the videos you tapped Approve on in Telegram
  python run.py telegram-setup         print your Telegram chat id
"""
from __future__ import annotations

import argparse
import datetime
import json
import subprocess
import sys
from pathlib import Path

from pipeline import common, notify, publish as publisher, render, script, topics, voice

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def build(spec: dict) -> None:
    errors = common.validate(spec)
    if errors:
        raise SystemExit("Spec problems:\n  " + "\n  ".join(errors))
    print(f"Voicing '{spec['title']}' ...")
    voice.add_voice(spec)
    print(f"  {voice.total_seconds(spec):.1f} seconds of narration")
    print("Rendering (first run downloads a headless browser, later runs are faster) ...")
    out = render.render(spec)
    print(f"\nDone: {out}\nWatch it, then run:  python run.py approve {spec['slug']}")


def cmd_topics(_: argparse.Namespace) -> None:
    found = topics.find_topics()
    if not found:
        print("No fresh stories found.")
    for i, t in enumerate(found, 1):
        print(f"{i:>2}. {t['title']}  [{t['source']}]")
    print("\nPick one with:  python run.py make --topic <number>")


def cmd_make(args: argparse.Namespace) -> None:
    source = None
    idea = args.idea
    if args.topic:
        found = topics.load_topics()
        if not 1 <= args.topic <= len(found):
            raise SystemExit(f"Topic must be between 1 and {len(found)}.")
        source = found[args.topic - 1]
        idea = idea or f"Explain this update, how the technology behind it works, and what it means: {source['title']}"
    if not idea:
        raise SystemExit('Give --topic <number> or --idea "your idea".')
    print("Writing script ...")
    spec = script.write_spec(idea, source, args.kind)
    print(f"  {len(spec['scenes'])} scenes -> {common.spec_path(spec['slug'])}")
    if source:
        topics.mark_used(source["link"])
    if not args.script_only:
        build(spec)


def cmd_build(args: argparse.Namespace) -> None:
    spec = common.load_spec(args.slug)
    spec.setdefault("brand", common.config()["brand"])
    build(spec)


def cmd_demo(_: argparse.Namespace) -> None:
    if common.spec_path("fast-charging").exists():
        spec = common.load_spec("fast-charging")  # resume an earlier attempt
    else:
        spec = json.loads((common.ROOT / "samples" / "fast-charging.json").read_text(encoding="utf-8"))
    spec["brand"] = common.config()["brand"]
    common.save_spec(spec)
    build(spec)


def cmd_voices(_: argparse.Namespace) -> None:
    folder = common.OUTPUT / "voice-samples"
    made = voice.audition(folder)
    print(f"Wrote {len(made)} samples to {folder}:")
    for name in made:
        print(f"  {name}")
    print('Listen, then put the one you like in config.json under "voice" -> "name".')


def cmd_status(_: argparse.Namespace) -> None:
    specs = common.all_specs()
    if not specs:
        print("No videos yet. Try:  python run.py demo")
    for spec in specs:
        print(f"{spec.get('status', 'scripted'):>10}  {spec['slug']}  -  {spec['title']}")


def cmd_approve(args: argparse.Namespace) -> None:
    spec = common.load_spec(args.slug)
    if spec.get("status") != "rendered":
        raise SystemExit(f"'{args.slug}' is '{spec.get('status')}', it must be rendered first.")
    spec["status"] = "approved"
    common.save_spec(spec)
    print(f"Approved. Post it with:  python run.py publish {args.slug}")


def cmd_publish(args: argparse.Namespace) -> None:
    results = publisher.publish(common.load_spec(args.slug))
    if "manual" in results:
        print(f"No platforms are connected yet. Copied video and caption to {results['manual']} for manual upload.")
    else:
        for platform, url in results.items():
            print(f"{platform}: {url}")


def cmd_auto(args: argparse.Namespace) -> None:
    """One unattended run: choose a topic, make the video, send it to Telegram for review."""
    kind = args.kind
    if kind == "alternate":  # news one day, a how-it-works explainer the next
        kind = "news" if datetime.date.today().toordinal() % 2 == 0 else "explainer"
    source, idea = None, args.idea
    if not idea and kind == "news":
        found = topics.find_topics()
        if found:
            source = found[script.pick_topic(found)]
            idea = f"Explain this update, how the technology behind it works, and what it means: {source['title']}"
        else:
            print("No fresh news today, making an explainer instead.")
            kind = "explainer"
    if not idea:
        idea = script.suggest_idea([s["title"] for s in common.all_specs()])
    print(f"Kind: {kind}\nIdea: {idea}\nWriting script ...")
    spec = script.write_spec(idea, source, kind)
    if source:
        topics.mark_used(source["link"])
    build(spec)
    (common.OUTPUT / "last.json").write_text(json.dumps({"slug": spec["slug"], "title": spec["title"]}),
                                             encoding="utf-8")
    if not args.no_review:
        notify.send_for_review(common.load_spec(spec["slug"]), common.OUTPUT / f"{spec['slug']}.mp4")
        print("Sent to Telegram for review.")


def _fetch_video(slug: str) -> Path:
    """In the cloud the rendered video lives on a GitHub release called video-<slug>."""
    video = common.OUTPUT / f"{slug}.mp4"
    if not video.exists():
        common.OUTPUT.mkdir(exist_ok=True)
        subprocess.run(["gh", "release", "download", f"video-{slug}", "--pattern", f"{slug}.mp4",
                        "--dir", str(common.OUTPUT), "--clobber"], check=True)
    return video


def cmd_review(_: argparse.Namespace) -> None:
    """Act on Telegram taps: post approved videos, set rejected ones aside."""
    taps = notify.poll()
    if not taps:
        print("No new taps.")
    for tap in taps:
        slug = tap["slug"]
        print(f"{tap['action']}: {slug}")
        try:
            spec = common.load_spec(slug)
            if spec.get("status") == "published":
                notify.acknowledge(tap, "Already posted.")
                continue
            if tap["action"] == "reject":
                spec["status"] = "rejected"
                common.save_spec(spec)
                notify.acknowledge(tap, "Rejected. It won't be posted.")
                continue
            spec["status"] = "approved"
            common.save_spec(spec)
            results = publisher.publish(spec, _fetch_video(slug))
            if "manual" in results:
                notify.acknowledge(tap, "Approved, but no posting service is connected (UPLOAD_POST_API_KEY "
                                        "is missing), so nothing was posted.")
            else:
                notify.acknowledge(tap, "Posted ✅\n" + "\n".join(f"{p}: {u}" for p, u in results.items()))
        except (Exception, SystemExit) as err:  # keep the buttons so you can tap again
            print(f"  failed: {err}")
            notify.send_message(f"Could not post {slug}: {err}\nTap ✅ again to retry.",
                                reply_to=tap["message_id"])


def cmd_send_review(args: argparse.Namespace) -> None:
    notify.send_for_review(common.load_spec(args.slug), _fetch_video(args.slug))
    print("Sent to Telegram for review.")


def cmd_frames(args: argparse.Namespace) -> None:
    """Contact sheet with one frame from each scene (75% of the way in) to check a render by eye."""
    common.refresh_path()
    spec = common.load_spec(args.slug)
    video = common.OUTPUT / f"{args.slug}.mp4"
    if not video.exists():
        raise SystemExit(f"{video} does not exist. Run `python run.py build {args.slug}` first.")
    folder = common.OUTPUT / "frames" / args.slug
    folder.mkdir(parents=True, exist_ok=True)
    t, files = 0, []
    for i, sc in enumerate(spec["scenes"]):
        at = (t + sc.get("durationMs", 3000) * 0.75) / 1000
        t += sc.get("durationMs", 3000)
        f = folder / f"scene-{i + 1:02d}.png"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{at:.2f}", "-i", str(video),
                        "-frames:v", "1", "-vf", "scale=360:640", str(f)], check=True)
        files.append(f)
    cols = 5
    inputs = [a for f in files for a in ("-i", str(f))]
    layout = "|".join(f"{(i % cols) * 360}_{(i // cols) * 640}" for i in range(len(files)))
    sheet = common.OUTPUT / "frames" / f"{args.slug}.png"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex",
                    f"xstack=inputs={len(files)}:layout={layout}:fill=black", str(sheet)], check=True)
    print(f"Contact sheet ({len(files)} scenes, left to right, top to bottom): {sheet}")
    print(f"Single frames: {folder}")


def cmd_mark_used(args: argparse.Namespace) -> None:
    found = topics.load_topics()
    if not 1 <= args.number <= len(found):
        raise SystemExit(f"Topic must be between 1 and {len(found)}.")
    topics.mark_used(found[args.number - 1]["link"])
    print(f"Marked as used: {found[args.number - 1]['title']}")


def cmd_notify(args: argparse.Namespace) -> None:
    notify.send_message(args.text)


def cmd_telegram_setup(_: argparse.Namespace) -> None:
    chats = notify.find_chat_id()
    if not chats:
        raise SystemExit("No messages found. Open your bot in Telegram, send it any message, then run this again.")
    for chat_id, name in chats:
        print(f"TELEGRAM_CHAT_ID = {chat_id}   ({name})")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("topics").set_defaults(fn=cmd_topics)
    make = sub.add_parser("make")
    make.add_argument("--topic", type=int)
    make.add_argument("--idea")
    make.add_argument("--kind", choices=["explainer", "news"],
                      help="how-it-works explainer or tech-update video (default: news for --topic, explainer for --idea)")
    make.add_argument("--script-only", action="store_true", help="stop after writing the script")
    make.set_defaults(fn=cmd_make)
    for name, fn in (("build", cmd_build), ("approve", cmd_approve), ("publish", cmd_publish)):
        p = sub.add_parser(name)
        p.add_argument("slug")
        p.set_defaults(fn=fn)
    sub.add_parser("demo").set_defaults(fn=cmd_demo)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    sub.add_parser("voices").set_defaults(fn=cmd_voices)
    auto = sub.add_parser("auto", help="unattended run: pick a topic, make the video, send it for review")
    auto.add_argument("--kind", choices=["alternate", "news", "explainer"], default="alternate")
    auto.add_argument("--idea", help="make this idea instead of choosing one")
    auto.add_argument("--no-review", action="store_true", help="do not send to Telegram")
    auto.set_defaults(fn=cmd_auto)
    sub.add_parser("review", help="act on Approve / Reject taps in Telegram").set_defaults(fn=cmd_review)
    fr = sub.add_parser("frames", help="contact sheet of one frame per scene, to check a render")
    fr.add_argument("slug")
    fr.set_defaults(fn=cmd_frames)
    mu = sub.add_parser("mark-used", help="mark topic number N from `topics` as used")
    mu.add_argument("number", type=int)
    mu.set_defaults(fn=cmd_mark_used)
    send = sub.add_parser("send-review", help="send a rendered video to Telegram for review")
    send.add_argument("slug")
    send.set_defaults(fn=cmd_send_review)
    note = sub.add_parser("notify", help="send yourself a Telegram message")
    note.add_argument("text")
    note.set_defaults(fn=cmd_notify)
    sub.add_parser("telegram-setup", help="print your Telegram chat id").set_defaults(fn=cmd_telegram_setup)
    args = parser.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
