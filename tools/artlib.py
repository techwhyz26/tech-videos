"""Small helpers for drawing animated SVG illustrations (1000x1000 canvas, SMIL animation).

Theme classes available inside every illustration: fa/sa (accent fill/stroke), fa2/sa2 (second
colour), fb/sb (background), fw/sw (white), nf (no fill), display (headline font).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


# Shared filters and gradients, added to every illustration.
DEFS = """<defs>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="16"/></filter>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="metal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a4a56"/><stop offset="1" stop-color="#1e1e25"/></linearGradient>
<linearGradient id="steel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f4f4f8"/><stop offset="1" stop-color="#b9b9c6"/></linearGradient>
<linearGradient id="screen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1b1b24"/><stop offset="1" stop-color="#050507"/></linearGradient>
<linearGradient id="paper" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e9e5da"/></linearGradient>
</defs>"""


def save(slug: str, name: str, svg: str) -> None:
    folder = ROOT / "public" / "videos" / slug / "art"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{name}.svg").write_text(DEFS + svg.strip(), encoding="utf-8")
    print(f"  art/{name}.svg  ({len(svg) // 1024} KB)")


def shadow(cx: float, cy: float, rx: float, ry: float = 26, opacity: float = 0.55) -> str:
    """Soft contact shadow on the ground under an object."""
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#000" opacity="{opacity}" filter="url(#soft)"/>'


def bob(inner: str, amp: float = 10, dur: float = 3.2, begin: float = 0) -> str:
    """Gentle idle float so a still object never looks frozen."""
    return (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 {-amp};0 0" '
            f'begin="{begin}s" dur="{dur}s" repeatCount="indefinite"/>{inner}</g>')


def draw(d: str, begin: float, dur: float = 0.6, cls: str = "nf sw", width: float = 8, extra: str = "") -> str:
    """A path that draws itself from start to end."""
    return (f'<path d="{d}" class="{cls}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" '
            f'pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" {extra}>'
            f'<animate attributeName="stroke-dashoffset" from="1" to="0" begin="{begin}s" dur="{dur}s" fill="freeze"/></path>')


def phone(x: float, y: float, w: float, h: float, screen: str = "") -> str:
    """A phone body; `screen` is drawn inside it in its own coordinates (0,0 = screen top-left)."""
    r = w * 0.14
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>'
            f'<rect x="{x + 12}" y="{y + 12}" width="{w - 24}" height="{h - 24}" rx="{r - 8}" fill="url(#screen)"/>'
            f'<rect x="{x + w / 2 - w * 0.14}" y="{y + 24}" width="{w * 0.28}" height="{w * 0.07}" rx="{w * 0.035}" fill="#000"/>'
            f'<g transform="translate({x + 12} {y + 12})">{screen}</g>')


def fade(begin: float, dur: float = 0.35, to: float = 1, frm: float = 0) -> str:
    return (f'<animate attributeName="opacity" from="{frm}" to="{to}" begin="{begin}s" '
            f'dur="{dur}s" fill="freeze"/>')


def appear(inner: str, begin: float, dur: float = 0.35) -> str:
    """Group that is invisible until `begin`, then fades in."""
    return f'<g opacity="0">{fade(begin, dur)}{inner}</g>'


def pop(cx: float, cy: float, inner: str, begin: float) -> str:
    """Group drawn around the origin that pops in at (cx, cy) with a little overshoot."""
    return (f'<g transform="translate({cx} {cy})"><g opacity="0">{fade(begin, 0.2)}'
            f'<animateTransform attributeName="transform" type="scale" values="0.3;1.15;1" '
            f'keyTimes="0;0.7;1" begin="{begin}s" dur="0.45s" fill="freeze"/>{inner}</g></g>')


def label(x: float, y: float, text: str, size: int = 46, cls: str = "", anchor: str = "middle") -> str:
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" class="{cls}">{text}</text>'


def chip(cx: float, cy: float, text: str, begin: float, dot: str = "fa") -> str:
    w = len(text) * 23 + 100
    inner = (f'<rect x="{-w / 2}" y="-38" width="{w}" height="76" rx="38" fill="#fff" fill-opacity="0.12" '
             f'stroke="#fff" stroke-opacity="0.3" stroke-width="2"/>'
             f'<circle cx="{-w / 2 + 38}" cy="0" r="11" class="{dot}"/>'
             f'{label(14, 14, text, 38)}')
    return pop(cx, cy, inner, begin)


def badge(cx: float, cy: float, text: str, begin: float, cls: str = "fa") -> str:
    w = len(text) * 27 + 90
    inner = (f'<rect x="{-w / 2}" y="-48" width="{w}" height="96" rx="20" class="{cls}"/>'
             f'<text x="0" y="16" font-size="46" font-weight="700" text-anchor="middle" '
             f'style="fill:#0a0a0a">{text}</text>')
    return pop(cx, cy, inner, begin)


def waves(cx: float, cy: float, cls: str = "sa", n: int = 3, r0: float = 30, r1: float = 300,
          dur: float = 2.0, width: float = 7, peak: float = 0.9, start: float = 0) -> str:
    """Rings that keep expanding outward from a point, like a radio signal."""
    out = []
    for i in range(n):
        b = start + i * dur / n
        out.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r0}" class="nf {cls}" stroke-width="{width}" opacity="0">'
            f'<animate attributeName="r" from="{r0}" to="{r1}" begin="{b}s" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;{peak};0" keyTimes="0;0.15;1" begin="{b}s" '
            f'dur="{dur}s" repeatCount="indefinite"/></circle>')
    return "".join(out)


def sine(x0: float, x1: float, y: float, amp: float, period: float, phase: float = 0) -> str:
    pts = []
    x = x0
    while x <= x1:
        pts.append(f"{x:.0f} {y + amp * math.sin((x - x0) / period * 2 * math.pi + phase):.1f}")
        x += period / 24
    return "M " + " L ".join(pts)


if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
