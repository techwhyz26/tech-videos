"""Illustrations for the 'microwave-wifi' video. Run:  python tools/art_microwave.py

Objects (microwave, router, person) are drawn once at a fixed size in their own coordinates and
placed with translate+scale, so every scene can reuse them at any size.
"""
import math

from artlib import appear, badge, bob, fade, label, phone, pop, save, shadow, sine, waves

SLUG = "microwave-wifi"
LIGHT = "#ffe45c"
RED = "#ff4d4d"

MW_W, MW_H = 480, 310          # microwave size in its own coordinates
WIN = (28, 36, 300, 238)        # window x, y, w, h inside the microwave


def place(x: float, y: float, s: float, inner: str) -> str:
    return f'<g transform="translate({x} {y}) scale({s})">{inner}</g>'


def bowl(cx: float, cy: float, steam: bool = True) -> str:
    st = ""
    if steam:
        st = "".join(
            f'<path d="M{cx + dx} {cy - 50} q16 -22 0 -44 q-16 -22 0 -44" fill="none" stroke="#fff" stroke-width="7" '
            f'stroke-linecap="round" opacity="0"><animate attributeName="opacity" values="0;0.8;0" begin="{i * 0.4}s" '
            f'dur="1.6s" repeatCount="indefinite"/><animateTransform attributeName="transform" type="translate" '
            f'values="0 10;0 -26" begin="{i * 0.4}s" dur="1.6s" repeatCount="indefinite"/></path>'
            for i, dx in enumerate((-30, 0, 30)))
    return (f'{st}<path d="M{cx - 70} {cy - 40} h140 q-6 52 -70 52 q-64 0 -70 -52 z" fill="#f2f2f5"/>'
            f'<ellipse cx="{cx}" cy="{cy - 40}" rx="70" ry="13" fill="#ff8a3d"/>'
            f'<ellipse cx="{cx}" cy="{cy - 42}" rx="40" ry="6" fill="#ffc06b"/>')


def microwave(uid: str, on: bool = True, inside: str | None = None, timer: str = "2:00",
              door_glow: str = "fa2") -> str:
    """A microwave oven at (0,0) size 480x310. `inside` replaces the turning bowl in the window."""
    wx, wy, ww, wh = WIN
    dots = "".join(
        f'<circle cx="{wx + 10 + i * 14}" cy="{wy + 10 + j * 14}" r="2.8" fill="#000" opacity="0.6"/>'
        for i in range(ww // 14) for j in range(wh // 14))
    if inside is None:
        inside = (f'<ellipse cx="{wx + ww / 2}" cy="{wy + wh - 26}" rx="112" ry="15" fill="#9a9aa6"/>'
                  f'<g><animateTransform attributeName="transform" type="translate" values="-34 0;34 0;-34 0" '
                  f'dur="3.6s" repeatCount="indefinite"/>{bowl(wx + ww / 2, wy + wh - 30, on)}</g>')
    glow = ""
    if on:
        glow = (f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="14" class="{door_glow}" opacity="0.35">'
                f'<animate attributeName="opacity" values="0.22;0.5;0.22" dur="1.3s" repeatCount="indefinite"/></rect>')
    px = 360
    buttons = "".join(
        f'<rect x="{px + 4 + i * 30}" y="{128 + j * 34}" width="24" height="22" rx="6" fill="#55555f"/>'
        for i in range(3) for j in range(3))
    return f"""
{shadow(MW_W / 2, MW_H + 14, MW_W * 0.55, 22)}
<rect x="40" y="{MW_H - 6}" width="54" height="20" rx="6" fill="#141418"/>
<rect x="{MW_W - 94}" y="{MW_H - 6}" width="54" height="20" rx="6" fill="#141418"/>
<rect x="0" y="0" width="{MW_W}" height="{MW_H}" rx="28" fill="url(#metal)" stroke="#fff" stroke-opacity="0.32" stroke-width="4"/>
<rect x="10" y="8" width="{MW_W - 20}" height="10" rx="5" fill="#fff" opacity="0.12"/>
<clipPath id="{uid}w"><rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="14"/></clipPath>
<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="14" fill="#0a0a0d"/>
<g clip-path="url(#{uid}w)">{glow}{inside}{dots}</g>
<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="14" fill="none" stroke="#000" stroke-width="6" opacity="0.6"/>
<rect x="{wx + ww + 10}" y="70" width="12" height="170" rx="6" fill="#8d8d99"/>
<rect x="{px - 4}" y="40" width="104" height="60" rx="10" fill="#08080a"/>
<text x="{px + 48}" y="84" font-size="38" text-anchor="middle" class="fa">{timer}</text>
{buttons}
<rect x="{px + 4}" y="236" width="84" height="34" rx="10" class="fa"/>"""


def router(lights: str = "fa") -> str:
    """A Wi-Fi router at (0,0), body 340 wide; antennas reach up to y=-170."""
    ants = "".join(
        f'<line x1="{x}" y1="10" x2="{x + lean}" y2="-160" stroke="#d6d6de" stroke-width="16" stroke-linecap="round"/>'
        f'<circle cx="{x + lean}" cy="-162" r="11" fill="#f0f0f4"/>'
        for x, lean in ((50, -26), (170, 0), (290, 26)))
    leds = "".join(
        f'<circle cx="{58 + i * 38}" cy="40" r="9" class="{lights}"><animate attributeName="opacity" values="1;0.2;1" '
        f'begin="{i * 0.17}s" dur="0.7s" repeatCount="indefinite"/></circle>' for i in range(5))
    return f"""{shadow(170, 98, 200, 18)}{ants}
<rect x="0" y="0" width="340" height="78" rx="20" fill="url(#steel)"/>
<rect x="0" y="52" width="340" height="26" rx="13" fill="#000" opacity="0.12"/>
<rect x="26" y="76" width="34" height="14" rx="4" fill="#8f8f9a"/>
<rect x="280" y="76" width="34" height="14" rx="4" fill="#8f8f9a"/>
{leds}"""


def person(look: str = "right") -> str:
    """A simple standing person at (0,0) = feet centre, about 520 tall."""
    flip = "" if look == "right" else ' transform="scale(-1 1)"'
    return f"""<g{flip}>{shadow(0, 8, 120, 16)}
<rect x="-52" y="-230" width="42" height="236" rx="20" fill="#2b3550"/>
<rect x="10" y="-230" width="42" height="236" rx="20" fill="#2b3550"/>
<path d="M-82 -230 q0 -150 82 -158 q82 8 82 158 z" class="fa2"/>
<path d="M60 -350 q60 40 64 120" fill="none" stroke="#f2c6a0" stroke-width="30" stroke-linecap="round"/>
<path d="M-60 -350 q-40 60 -40 130" fill="none" stroke="#f2c6a0" stroke-width="30" stroke-linecap="round"/>
<rect x="-16" y="-410" width="32" height="34" rx="10" fill="#e8b48c"/>
<circle cx="0" cy="-458" r="64" fill="#f2c6a0"/>
<path d="M-64 -470 q4 -66 70 -64 q56 2 62 56 q-38 -26 -132 8 z" fill="#2a1d18"/>
<circle cx="34" cy="-458" r="8" fill="#1a1a1a"/>
<path d="M30 -424 q14 6 24 -2" fill="none" stroke="#7a3f30" stroke-width="5" stroke-linecap="round"/></g>"""


def scrolling_sine(y: float, amp: float, period: float, cls: str, dur: float, direction: int = 1,
                   width: float = 12, extra: str = "", x0: float = 0, x1: float = 1000) -> str:
    shift = period * direction
    return (f'<path d="{sine(x0 - 2 * period, x1 + 2 * period, y, amp, period)}" class="nf {cls}" '
            f'stroke-width="{width}" stroke-linecap="round" {extra}>'
            f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{shift} 0" '
            f'dur="{dur}s" repeatCount="indefinite"/></path>')


def meter(x: float, y: float, lit: int, cls: str, begin: float, n: int = 10) -> str:
    """A volume meter: n bars growing taller, `lit` of them light up one by one."""
    out = []
    for i in range(n):
        h = 24 + i * 11
        on = i < lit
        bar = f'<rect x="{x + i * 30}" y="{y - h}" width="20" height="{h}" rx="5" fill="#fff" opacity="0.14"/>'
        if on:
            bar += (f'<rect x="{x + i * 30}" y="{y - h}" width="20" height="{h}" rx="5" class="{cls}" opacity="0">'
                    f'{fade(begin + i * 0.08, 0.1)}</rect>')
        out.append(bar)
    return "".join(out)


# 0. A microwave and a router, sending out the same waves ---------------------------------------
save(SLUG, "pair", f"""
{waves(224, 360, "sa2", 3, 60, 360, 2.1, 8)}
{waves(780, 470, "sa", 3, 40, 330, 2.1, 8, start=0.35)}
{place(20, 230, 0.85, microwave("p"))}
{place(620, 560, 0.95, router())}
<text x="530" y="470" font-size="150" text-anchor="middle" class="display fw" opacity="0">{fade(0.6)}=</text>
{appear(label(224, 585, "Microwave", 44), 0.3)}
{appear(label(780, 720, "Wi-Fi router", 44), 0.5)}
{badge(500, 880, "SAME RADIO WAVES", 1.3)}
""")

# 1. One heats dinner, the other loads videos. Why? -------------------------------------------------
video = (f'<rect x="20" y="120" width="216" height="150" rx="14" class="fa" opacity="0.85"/>'
         f'<path d="M108 165 l45 30 l-45 30 z" fill="#fff"/>'
         f'<rect x="20" y="300" width="216" height="12" rx="6" fill="#fff" opacity="0.2"/>'
         f'<rect x="20" y="300" width="20" height="12" rx="6" class="fa"><animate attributeName="width" from="20" to="200" dur="4s" fill="freeze"/></rect>'
         + "".join(f'<rect x="20" y="{340 + k * 46}" width="{216 - k * 50}" height="26" rx="8" fill="#fff" opacity="0.15"/>' for k in range(3)))
save(SLUG, "puzzle", f"""
{place(10, 300, 0.8, microwave("q"))}
{bob(phone(660, 180, 280, 520, video), 8, 3)}
{appear(label(200, 600, "Heats dinner", 44, "fa2"), 0.4)}
{appear(label(800, 760, "Loads videos", 44, "fa"), 0.7)}
{pop(500, 200, '<circle r="90" class="fa2"/><text y="56" font-size="170" font-weight="700" text-anchor="middle" style="fill:#0a0a0a">?</text>', 1.0)}
""")

# 2. Both waves have the same frequency ----------------------------------------------------------
save(SLUG, "frequency", f"""
<defs><clipPath id="fq"><rect x="60" y="120" width="880" height="620" rx="30"/></clipPath></defs>
<rect x="60" y="120" width="880" height="620" rx="30" fill="#fff" fill-opacity="0.05" stroke="#fff" stroke-opacity="0.15" stroke-width="3"/>
<g clip-path="url(#fq)">
  {scrolling_sine(310, 80, 170, "sa2", 0.8, width=14)}
  {scrolling_sine(580, 80, 170, "sa", 0.8, width=14)}
  {''.join(f'<line x1="{x}" y1="140" x2="{x}" y2="720" stroke="#fff" stroke-opacity="0.22" stroke-width="3" stroke-dasharray="10 12"/>' for x in (245, 415, 585, 755))}
</g>
{place(80, 140, 0.22, microwave("f", on=False))}
<text x="200" y="190" font-size="40" class="fa2">MICROWAVE</text>
{place(90, 470, 0.22, router())}
<text x="200" y="480" font-size="40" class="fa">WI-FI</text>
{appear('<text x="500" y="930" font-size="180" text-anchor="middle" class="display fa">2.4 GHz</text>', 0.5)}
""")

# 3. Same waves, very different power: a whisper versus a shout ----------------------------------
save(SLUG, "power", f"""
{waves(170, 400, "sa", 2, 20, 110, 2.0, 4, 0.5)}
{place(40, 470, 0.75, router())}
{waves(650, 380, "sa2", 4, 60, 480, 1.4, 22, 0.95)}
{place(420, 260, 0.95, microwave("w"))}
{appear(label(170, 640, "Wi-Fi router", 40), 0.2)}
{appear(label(650, 640, "Microwave", 40), 0.2)}
{meter(40, 780, 1, "fa", 0.5)}
{meter(500, 780, 10, "fa2", 1.6)}
{appear('<text x="170" y="880" font-size="96" text-anchor="middle" class="display fa">&lt;1 W</text>', 0.6)}
{appear('<text x="650" y="880" font-size="96" text-anchor="middle" class="display fa2">1000 W</text>', 2.4)}
""")

# 4. Water molecules twist back and forth and heat up -------------------------------------------
def molecule(x: float, y: float, b: float, s: float = 1) -> str:
    return (f'<g transform="translate({x} {y}) scale({s})"><g>'
            f'<animateTransform attributeName="transform" type="rotate" values="-40;40;-40" begin="{b}s" dur="0.42s" repeatCount="indefinite"/>'
            f'<line x1="0" y1="0" x2="-58" y2="42" stroke="#fff" stroke-width="12"/><line x1="0" y1="0" x2="58" y2="42" stroke="#fff" stroke-width="12"/>'
            f'<circle cx="-58" cy="42" r="32" fill="#f4f4f8"/><circle cx="58" cy="42" r="32" fill="#f4f4f8"/>'
            f'<circle r="56" fill="#ff5a4d"/><circle cx="-16" cy="-18" r="16" fill="#fff" opacity="0.35"/>'
            f'<text y="18" font-size="50" font-weight="700" text-anchor="middle">O</text>'
            f'<text x="-58" y="55" font-size="34" font-weight="700" text-anchor="middle" style="fill:#111">H</text>'
            f'<text x="58" y="55" font-size="34" font-weight="700" text-anchor="middle" style="fill:#111">H</text></g></g>')


heat = "".join(
    f'<path d="M{x} 300 q26 -34 0 -68 q-26 -34 0 -68 q26 -34 0 -68" class="nf sa2" stroke-width="11" stroke-linecap="round" opacity="0">'
    f'<animate attributeName="opacity" values="0;0.9;0" begin="{1 + i * 0.3}s" dur="1.5s" repeatCount="indefinite"/>'
    f'<animateTransform attributeName="transform" type="translate" from="0 40" to="0 -50" begin="{1 + i * 0.3}s" dur="1.5s" repeatCount="indefinite"/></path>'
    for i, x in enumerate((230, 500, 770)))
save(SLUG, "molecules", f"""
<circle cx="500" cy="560" r="420" class="fa2" opacity="0"><animate attributeName="opacity" values="0;0.18" begin="0.5s" dur="3s" fill="freeze"/></circle>
<g opacity="0.5">{scrolling_sine(430, 46, 150, "sa", 0.7, width=8)}{scrolling_sine(680, 46, 150, "sa", 0.7, width=8)}</g>
{heat}
{molecule(250, 460, 0)}{molecule(520, 420, 0.1, 1.15)}{molecule(780, 480, 0.2)}
{molecule(380, 690, 0.15, 0.9)}{molecule(660, 700, 0.05, 0.9)}
{appear(label(500, 920, "Twisting water molecules = heat", 46), 0.6)}
""")

# 5. Someone stands right in front of it, watching. Why aren't they cooked? -----------------------
inside = (f'<ellipse cx="{WIN[0] + WIN[2] / 2}" cy="{WIN[1] + WIN[3] - 26}" rx="112" ry="15" fill="#9a9aa6"/>'
          + bowl(WIN[0] + WIN[2] / 2, WIN[1] + WIN[3] - 30)
          + waves(WIN[0] + WIN[2] / 2, WIN[1] + WIN[3] / 2, "sa2", 3, 10, 190, 1.2, 8, 0.9))
save(SLUG, "watching", f"""
<rect x="380" y="645" width="620" height="40" rx="8" fill="#6b4a32"/>
<rect x="400" y="685" width="580" height="225" fill="#4a3324"/>
{place(440, 300, 1.08, microwave("s", inside=inside))}
{place(200, 905, 1.0, person())}
{pop(200, 300, '<circle r="62" fill="#fff"/><text y="38" font-size="110" font-weight="700" text-anchor="middle" style="fill:#0a0a0a">?</text>', 0.8)}
""")

# 6. Close-up of the door: a metal mesh full of holes --------------------------------------------
holes = []
for j in range(18):
    for i in range(20):
        hx = 170 + i * 35 + (17 if j % 2 else 0)
        hy = 180 + j * 31
        op = max(0.1, 1 - math.hypot(hx - 500, hy - 445) / 400)
        holes.append(f'<circle cx="{hx}" cy="{hy}" r="9" class="fa2" opacity="{op:.2f}"/>')
save(SLUG, "mesh", f"""
<g><animateTransform attributeName="transform" type="scale" values="1;1.06" dur="4s" fill="freeze" additive="sum"/>
<rect x="100" y="110" width="800" height="670" rx="44" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>
<rect x="130" y="140" width="740" height="610" rx="24" fill="#0b0b0f"/>
<g>{''.join(holes)}<animate attributeName="opacity" values="0.6;1;0.6" dur="1.4s" repeatCount="indefinite"/></g>
<rect x="840" y="250" width="28" height="390" rx="14" fill="#9a9aa6"/>
</g>
{pop(760, 230, '<circle r="80" fill="none" stroke="#fff" stroke-width="10"/><line x1="56" y1="56" x2="110" y2="110" stroke="#fff" stroke-width="16" stroke-linecap="round"/>', 0.6)}
{appear(label(500, 880, "A metal mesh full of tiny holes", 48), 0.5)}
""")

# 7. Microwaves are too big to get through the holes, light is not ------------------------------
wall = "".join(f'<rect x="528" y="{y}" width="24" height="34" rx="6" fill="#a4a4b0"/>' for y in range(140, 810, 46))
gaps = [140 + 46 * k + 40 for k in (3, 5, 7, 9, 11)]
rays = "".join(
    f'<line x1="552" y1="{g}" x2="820" y2="{475 + (g - 475) * 0.25:.0f}" stroke="{LIGHT}" stroke-width="7" stroke-dasharray="20 14" opacity="0">'
    f'{fade(1.6, 0.3)}<animate attributeName="stroke-dashoffset" from="0" to="-34" dur="0.35s" repeatCount="indefinite"/></line>'
    for g in gaps)
save(SLUG, "blocked", f"""
<defs><clipPath id="inside"><rect x="20" y="130" width="500" height="690"/></clipPath></defs>
<g clip-path="url(#inside)">
  {scrolling_sine(475, 130, 250, "sa", 1.0, 1, 16)}
  {scrolling_sine(475, 130, 250, "sa", 1.0, -1, 16, 'opacity="0.3"')}
</g>
<path d="M130 235 v-22 M130 224 h250 M380 235 v-22" class="nf sw" stroke-width="6" stroke-linecap="round"/>
{label(255, 195, "12 cm", 46)}
{wall}
{pop(540, 475, f'<circle r="70" fill="{RED}" opacity="0.9"/><path d="M-30 -30 L30 30 M30 -30 L-30 30" stroke="#fff" stroke-width="14" stroke-linecap="round"/>', 0.9)}
{rays}
<g opacity="0">{fade(1.8, 0.3)}<path d="M800 475 q65 -78 130 0 q-65 78 -130 0 z" class="nf sw" stroke-width="9" stroke-linejoin="round"/>
<circle cx="865" cy="475" r="22" class="fw"/></g>
{appear(label(270, 900, "Microwaves bounce back", 42, "fa"), 0.5)}
{appear(f'<text x="770" y="900" font-size="42" text-anchor="middle" style="fill:{LIGHT}">Light slips out</text>', 1.8)}
""")

# 8. A little leaks out and drowns out the router ------------------------------------------------
save(SLUG, "leak", f"""
{waves(224, 360, "sa2", 3, 60, 640, 2.4, 9, 0.45)}
{waves(800, 520, "sa", 3, 30, 210, 1.6, 6, 0.8)}
{place(20, 230, 0.85, microwave("l"))}
{place(640, 690, 0.95, router())}
{''.join(f'<circle cx="{695 + i * 36:.0f}" cy="728" r="9" fill="{RED}" opacity="0">{fade(1.5, 0.2)}</circle>' for i in range(5))}
{pop(800, 400, f'<circle r="58" fill="{RED}"/><text y="28" font-size="80" font-weight="700" text-anchor="middle">!</text>', 1.5)}
{appear(label(224, 600, "A tiny leak", 44, "fa2"), 0.4)}
{appear(label(500, 900, "Harmless to you, loud to your router", 44), 1.5)}
""")

# 9. Your video buffers the moment someone heats leftovers -----------------------------------------
spinner = ('<g transform="translate(128 195)"><circle r="44" fill="none" stroke="#fff" stroke-opacity="0.2" stroke-width="12"/>'
           '<path d="M0 -44 a44 44 0 0 1 44 44" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round">'
           '<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="0.9s" repeatCount="indefinite"/></path></g>')
bars = "".join(
    f'<rect x="{150 + i * 22}" y="{60 - i * 14}" width="14" height="{20 + i * 14}" rx="3" fill="#fff">'
    + (f'<animate attributeName="opacity" from="1" to="0.18" begin="{1.0 + (3 - i) * 0.25}s" dur="0.2s" fill="freeze"/>' if i else '')
    + '</rect>' for i in range(4))
screen = (f'{bars}<rect x="20" y="120" width="216" height="150" rx="14" class="fa" opacity="0.5"/>{spinner}'
          f'<rect x="20" y="300" width="216" height="12" rx="6" fill="#fff" opacity="0.2"/>'
          f'<rect x="20" y="300" width="70" height="12" rx="6" class="fa"/>'
          f'<text x="128" y="370" font-size="30" text-anchor="middle">Buffering...</text>')
save(SLUG, "buffer", f"""
{waves(224, 550, "sa2", 3, 60, 560, 2.0, 9, 0.5)}
{place(20, 420, 0.85, microwave("b", timer="0:45"))}
{bob(phone(640, 150, 300, 560, screen), 6, 2.6)}
{appear(label(224, 780, "Leftovers", 44, "fa2"), 0.3)}
{badge(790, 800, "WI-FI DROPS", 1.6, "fa")}
""")

# 10. Newer Wi-Fi moves to 5 and 6 GHz, out of the microwave's way -------------------------------
lanes = [("2.4 GHz", 230, 170, "sa2"), ("5 GHz", 470, 95, "sa"), ("6 GHz", 710, 72, "sa")]
lane_svg = []
for k, (name, y, period, cls) in enumerate(lanes):
    lane_svg.append(
        f'<clipPath id="ln{k}"><rect x="250" y="{y - 90}" width="700" height="180" rx="24"/></clipPath>'
        f'<rect x="250" y="{y - 90}" width="700" height="180" rx="24" fill="#fff" fill-opacity="0.06" stroke="#fff" stroke-opacity="0.18" stroke-width="3"/>'
        f'<g clip-path="url(#ln{k})" opacity="0">{fade(0.3 + k * 0.4)}'
        f'{scrolling_sine(y, 50, period, cls, 0.9, width=10, x0=250, x1=950)}</g>'
        f'<text x="40" y="{y + 18}" font-size="54" class="display {"fa2" if k == 0 else "fw"}">{name}</text>')
noise = scrolling_sine(230, 70, 60, "sa2", 0.4, -1, 5, 'opacity="0.6"', 250, 950)
save(SLUG, "bands", f"""
{''.join(lane_svg)}
<g clip-path="url(#ln0)">{noise}</g>
{place(810, 175, 0.24, microwave("bd", on=False))}
{pop(900, 470, '<circle r="40" fill="#3ddc84"/><path d="M-18 0 l12 14 l24 -28" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>', 1.4)}
{pop(900, 710, '<circle r="40" fill="#3ddc84"/><path d="M-18 0 l12 14 l24 -28" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>', 1.7)}
{appear(label(500, 900, "Newer Wi-Fi moves out of the way", 46), 1.9)}
""")

# 11. A microwave is a router turned up 1000x, inside a metal box ---------------------------------
rx0, ry0 = WIN[0] + 40, WIN[1] + WIN[3] - 70
trapped = (place(rx0, ry0, 0.65, router("fa2"))
           + waves(rx0 + 110, ry0 - 40, "sa2", 4, 20, 260, 1.0, 10, 0.95))
save(SLUG, "box", f"""
{place(60, 200, 1.35, microwave("x", inside=trapped, timer="x1000"))}
{appear(label(450, 840, "A Wi-Fi router, turned up 1000x", 48), 0.5)}
{appear(label(450, 905, "inside a metal box", 48, "fa"), 1.1)}
""")
