"""Illustrations for the 'gta6-pc-recompilation' video. Run:  python tools/art_gta6_pc_recompilation.py

Days after GTA VI launched on consoles, a fan project (Leonida) tried to recompile the Xbox build into a
native PC game, until Take-Two's DMCA takedown. The video explains recompilation versus emulation, and
that the code is the easy part: the console's graphics, services and libraries all need stand-ins (shims).

Objects (Xbox-style console tower, controller, PC monitor and tower, code card, recompiler machine, .exe
file, speed gauge, puzzle-piece shim, GPU chip, cloud, books, repo card, chat app) are drawn once in their
own coordinates and placed with place(). No logos.
"""
import math

from artlib import appear, badge, bob, draw, fade, label, pop, save, shadow, waves

SLUG = "gta6-pc-recompilation"
RED = "#ff4d4d"
GREEN = "#3dff8f"

EXTRA = """<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b0b4a"/><stop offset="0.55" stop-color="#ff4f8b"/><stop offset="1" stop-color="#ffb347"/></linearGradient>
<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1f4f8f"/><stop offset="1" stop-color="#0b1a33"/></linearGradient>
<linearGradient id="pcb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#145c3a"/><stop offset="1" stop-color="#0a2e1d"/></linearGradient>
</defs>"""


def out(name: str, svg: str) -> None:
    save(SLUG, name, EXTRA + svg)


def place(x: float, y: float, s: float, inner: str) -> str:
    return f'<g transform="translate({x} {y}) scale({s})">{inner}</g>'


def spin(cx: float, cy: float, inner: str, dur: float = 2.0, rev: bool = False) -> str:
    to = -360 if rev else 360
    return (f'<g><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" '
            f'to="{to} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>{inner}</g>')


def check(r: float = 40) -> str:
    return (f'<circle r="{r}" fill="{GREEN}"/><path d="M{-r * 0.45} 0 l{r * 0.3} {r * 0.35} l{r * 0.6} {-r * 0.7}" '
            f'fill="none" stroke="#0a0a0a" stroke-width="{r * 0.25}" stroke-linecap="round" stroke-linejoin="round"/>')


def cross(r: float = 40) -> str:
    k = r * 0.38
    return (f'<circle r="{r}" fill="{RED}"/><path d="M{-k} {-k} L{k} {k} M{k} {-k} L{-k} {k}" stroke="#fff" '
            f'stroke-width="{r * 0.25}" stroke-linecap="round"/>')


# --- objects ---------------------------------------------------------------------------------------

XB_W, XB_H = 230, 460


def xbox(glow: bool = True) -> str:
    """A tall black console tower at (0,0), 230x460, glowing vent on top, power button, disc slot."""
    vent = "".join(f'<circle cx="{38 + i * 22}" cy="22" r="7" fill="#000"/>' for i in range(8))
    g = ""
    if glow:
        g = (f'<ellipse cx="{XB_W / 2}" cy="20" rx="96" ry="14" class="fa" opacity="0.6" filter="url(#glow)">'
             f'<animate attributeName="opacity" values="0.35;0.85;0.35" dur="1.8s" repeatCount="indefinite"/></ellipse>')
    return f"""{shadow(XB_W / 2, XB_H + 10, XB_W * 0.7, 22)}
<rect x="0" y="0" width="{XB_W}" height="{XB_H}" rx="24" fill="url(#metal)" stroke="#fff" stroke-opacity="0.28" stroke-width="4"/>
<rect x="8" y="0" width="{XB_W - 16}" height="44" rx="18" fill="#0a0a0e"/>
{g}{vent}
<rect x="14" y="54" width="10" height="{XB_H - 80}" rx="5" fill="#fff" opacity="0.1"/>
<circle cx="52" cy="92" r="17" fill="#15151b" stroke="#fff" stroke-opacity="0.4" stroke-width="3"/>
<circle cx="52" cy="92" r="7" fill="#fff"><animate attributeName="opacity" values="1;0.4;1" dur="2.2s" repeatCount="indefinite"/></circle>
<rect x="88" y="86" width="120" height="10" rx="5" fill="#000"/>
<rect x="40" y="{XB_H - 50}" width="30" height="14" rx="4" fill="#000"/>
<circle cx="190" cy="{XB_H - 43}" r="8" fill="#000"/>"""


def controller() -> str:
    """A gamepad centred at (0,0), about 300 wide."""
    body = ("M-130 -20 q0 -50 60 -55 h140 q60 5 60 55 l20 70 q10 45 -30 50 q-30 2 -55 -40 "
            "h-130 q-25 42 -55 40 q-40 -5 -30 -50 z")
    btn = "".join(f'<circle cx="{x}" cy="{y}" r="11" fill="{c}"/>'
                  for x, y, c in ((78, -46, "#3dff8f"), (100, -24, "#ff4d4d"), (56, -24, "#4d8dff"), (78, -2, "#ffd23f")))
    return f"""{shadow(0, 108, 150, 14)}
<path d="{body}" fill="url(#steel)" stroke="#000" stroke-opacity="0.25" stroke-width="3"/>
<circle cx="-72" cy="-22" r="26" fill="#2a2a32"/><circle cx="-72" cy="-22" r="16" fill="#3e3e48"/>
<circle cx="34" cy="26" r="26" fill="#2a2a32"/><circle cx="34" cy="26" r="16" fill="#3e3e48"/>
<path d="M-48 14 h16 v-16 h16 v16 h16 v16 h-16 v16 h-16 v-16 h-16 z" fill="#2a2a32" transform="translate(4 0)"/>
{btn}<circle cx="0" cy="-50" r="13" class="fa"/>"""


def sunset(w: float, h: float) -> str:
    """A sunset coastline with palm trees and towers, filling (0,0)-(w,h): stands in for the game."""
    s = w / 600
    hor = h * 0.62
    towers = "".join(
        f'<rect x="{x * s}" y="{hor - th * s}" width="{tw * s}" height="{th * s}" fill="#1a0b2e"/>'
        for x, tw, th in ((330, 40, 120), (380, 30, 170), (418, 46, 95), (472, 28, 140), (508, 50, 110)))
    lights = "".join(
        f'<rect x="{(x + 8) * s}" y="{hor - (th - 20 - k * 26) * s}" width="{6 * s}" height="{8 * s}" fill="#ffd23f" opacity="0.8"/>'
        for x, th in ((380, 170), (472, 140)) for k in range(4))

    def palm(px: float, ph: float) -> str:
        tx, ty = px * s, hor - ph * s
        fr = "".join(f'<path d="M{tx} {ty} q{dx * 0.5 * s} {-30 * s} {dx * s} {dy * s}" fill="none" stroke="#12081f" '
                     f'stroke-width="{12 * s}" stroke-linecap="round"/>'
                     for dx, dy in ((-80, 20), (-60, 50), (80, 22), (64, 52), (-20, -40), (30, -36)))
        return (f'<path d="M{(px - 10) * s} {hor} q{-16 * s} {-ph * 0.5 * s} {10 * s} {-ph * s}" fill="none" stroke="#12081f" '
                f'stroke-width="{14 * s}" stroke-linecap="round"/>{fr}')

    return f"""<rect x="0" y="0" width="{w}" height="{h}" fill="url(#sky)"/>
<circle cx="{w * 0.42}" cy="{hor - 10 * s}" r="{90 * s}" fill="#ffd36b"/>
{''.join(f'<rect x="{w * 0.42 - 95 * s}" y="{hor - (60 - k * 18) * s}" width="{190 * s}" height="{5 * s}" fill="#ff7a8a"/>' for k in range(3))}
{towers}{lights}
<rect x="0" y="{hor}" width="{w}" height="{h - hor}" fill="url(#sea)"/>
{''.join(f'<rect x="{w * 0.42 - (70 - k * 12) * s}" y="{hor + (14 + k * 18) * s}" width="{(140 - k * 24) * s}" height="{5 * s}" fill="#ffb347" opacity="0.6"><animate attributeName="opacity" values="0.3;0.8;0.3" begin="{k * 0.3}s" dur="1.6s" repeatCount="indefinite"/></rect>' for k in range(4))}
{palm(90, 230)}{palm(170, 180)}"""


def monitor(w: float, h: float, screen: str = "", uid: str = "m") -> str:
    """A desktop monitor at (0,0) size w x h on a stand; `screen` is drawn in screen coords (0,0 top-left)."""
    return f"""{shadow(w / 2, h + 78, w * 0.4, 18)}
<rect x="{w / 2 - 34}" y="{h - 10}" width="68" height="70" fill="#2a2a32"/>
<rect x="{w / 2 - 130}" y="{h + 56}" width="260" height="20" rx="10" fill="url(#metal)" stroke="#fff" stroke-opacity="0.25" stroke-width="3"/>
<rect x="0" y="0" width="{w}" height="{h}" rx="22" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>
<clipPath id="{uid}s"><rect x="14" y="14" width="{w - 28}" height="{h - 28}" rx="10"/></clipPath>
<rect x="14" y="14" width="{w - 28}" height="{h - 28}" rx="10" fill="url(#screen)"/>
<g clip-path="url(#{uid}s)"><g transform="translate(14 14)">{screen}</g></g>
<circle cx="{w / 2}" cy="{h - 7}" r="3" fill="#fff" opacity="0.5"/>"""


def fan(cx: float, cy: float, r: float, dur: float = 0.8) -> str:
    blades = "".join(f'<path d="M0 0 q{r * 0.55} {-r * 0.3} {r * 0.85} {r * 0.15} q{-r * 0.45} {-r * 0.05} {-r * 0.85} {-r * 0.15} z" '
                     f'fill="#c9ffe0" opacity="0.75" transform="rotate({a})"/>' for a in range(0, 360, 72))
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#07120c" stroke="#fff" stroke-opacity="0.3" stroke-width="3"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" class="nf sa" stroke-width="4" opacity="0.7"/>'
            f'<g transform="translate({cx} {cy})"><g><animateTransform attributeName="transform" type="rotate" from="0" to="360" '
            f'dur="{dur}s" repeatCount="indefinite"/>{blades}</g></g><circle cx="{cx}" cy="{cy}" r="{r * 0.2}" fill="#2a2a32"/>')


def tower() -> str:
    """A gaming PC case at (0,0), 180x360, glass side with two spinning fans and an RGB strip."""
    return f"""{shadow(90, 366, 120, 16)}
<rect x="0" y="0" width="180" height="360" rx="16" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>
<rect x="16" y="40" width="148" height="300" rx="10" fill="#050a07" stroke="#fff" stroke-opacity="0.2" stroke-width="2"/>
{fan(90, 120, 54)}{fan(90, 250, 54, 0.9)}
<rect x="22" y="324" width="136" height="8" rx="4" class="fa"><animate attributeName="opacity" values="1;0.35;1" dur="1.2s" repeatCount="indefinite"/></rect>
<circle cx="150" cy="22" r="8" fill="#fff" opacity="0.8"/>
<rect x="20" y="16" width="60" height="10" rx="5" fill="#000"/>"""


PC_W, PC_H = 740, 404


def pc(screen: str = "", uid: str = "p") -> str:
    """Monitor (520x330) plus tower, at (0,0), about 740x404."""
    return monitor(520, 330, screen, uid) + place(560, 44, 1, tower())


def code_card(lines: list[str], begin: float = 0, w: float = 420, color: str = "#e9e9f0", step: float = 0.18,
              head: str = "") -> str:
    """Hex machine code on a dark card at (0,0), `w` wide. Lines type in one by one."""
    h = 90 + len(lines) * 52
    rows = "".join(
        appear(f'<text x="34" y="{110 + i * 52}" font-size="36" style="font-family:monospace;fill:{color}">{t}</text>',
               begin + i * step, 0.15) for i, t in enumerate(lines))
    return (f'{shadow(w / 2, h + 14, w * 0.55, 18)}<rect x="0" y="0" width="{w}" height="{h}" rx="22" fill="url(#screen)" '
            f'stroke="#fff" stroke-opacity="0.25" stroke-width="4"/>'
            + "".join(f'<circle cx="{30 + i * 28}" cy="34" r="9" fill="{c}"/>' for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")))
            + (f'<text x="{w - 30}" y="46" font-size="30" text-anchor="end" style="fill:#8a8a99">{head}</text>' if head else "")
            + rows)


XB_HEX = ["48 8B 05 3C 1A", "C5 FA 10 44 24", "E8 9F 02 00 00", "0F 28 C1 F3 0F", "48 83 C4 28 C3",
          "4C 8D 0D 11 7E", "FF 15 A2 30 00", "33 C0 48 8B 5C"]
PC_HEX = ["48 8B 0D 7A 2B", "C5 F8 28 4C 24", "E8 31 0F 00 00", "0F 59 C8 F3 0F", "48 81 C4 38 01",
          "4C 8B 05 E9 12", "FF 15 6C 41 00", "31 C0 48 89 5C"]


def gear(cx: float, cy: float, r: float, teeth: int, fill: str) -> str:
    pts = []
    for i in range(teeth * 2):
        a = i * math.pi / teeth
        rr = r if i % 2 == 0 else r * 0.8
        for da in (-0.3, 0.3):
            aa = a + da * math.pi / teeth
            pts.append(f"{cx + rr * math.cos(aa):.1f},{cy + rr * math.sin(aa):.1f}")
    return (f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="#000" stroke-opacity="0.35" stroke-width="3"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.42:.1f}" fill="#2a2a32"/>')


def machine(uid: str = "r") -> str:
    """The recompiler: a metal box at (0,0), 340x260, with an input funnel on top-left and an output chute right."""
    g1 = spin(120, 150, gear(120, 150, 58, 10, "#d8d8e2"), 1.6)
    g2 = spin(222, 136, gear(222, 136, 42, 8, "#b4b4c0"), 1.6 * 42 / 58, rev=True)
    return f"""{shadow(170, 276, 200, 20)}
<path d="M40 -70 h150 l-35 74 h-80 z" fill="url(#steel)" stroke="#000" stroke-opacity="0.3" stroke-width="3"/>
<rect x="320" y="150" width="70" height="60" rx="8" fill="#2a2a32"/>
<rect x="0" y="0" width="340" height="260" rx="28" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>
<rect x="12" y="10" width="316" height="10" rx="5" fill="#fff" opacity="0.12"/>
<clipPath id="{uid}w"><rect x="34" y="56" width="272" height="170" rx="16"/></clipPath>
<rect x="34" y="56" width="272" height="170" rx="16" fill="#060a08"/>
<g clip-path="url(#{uid}w)">{g1}{g2}</g>
<rect x="34" y="56" width="272" height="170" rx="16" fill="none" stroke="#000" stroke-width="5" opacity="0.6"/>
<circle cx="290" cy="34" r="10" class="fa"><animate attributeName="opacity" values="1;0.2;1" dur="0.6s" repeatCount="indefinite"/></circle>
<circle cx="262" cy="34" r="10" class="fa2"><animate attributeName="opacity" values="0.2;1;0.2" dur="0.6s" repeatCount="indefinite"/></circle>"""


def exe(name: str = "GAME.EXE") -> str:
    """A program file at (0,0), 200x250, with a folded corner and a window icon."""
    return f"""{shadow(100, 262, 120, 16)}
<path d="M0 18 q0 -18 18 -18 h124 l58 58 v174 q0 18 -18 18 h-164 q-18 0 -18 -18 z" fill="url(#paper)"/>
<path d="M142 0 v42 q0 16 16 16 h42 z" fill="#c9c5b8"/>
<rect x="44" y="72" width="112" height="84" rx="10" class="fa"/>
<rect x="44" y="72" width="112" height="20" rx="8" fill="#0a0a0a" opacity="0.35"/>
<path d="M86 104 l30 18 l-30 18 z" fill="#0a0a0a"/>
<text x="100" y="212" font-size="32" font-weight="700" text-anchor="middle" style="fill:#0a0a0a">{name}</text>"""


def gauge(r: float, value: float, begin: float, text: str, cls: str = "fa") -> str:
    """A speedometer centred at (0,0) (dial above). The needle swings from 0 to `value` (0..1)."""
    ticks = "".join(
        f'<line x1="{(r - 18) * math.cos(math.pi * (1 - k / 10)):.1f}" y1="{-(r - 18) * math.sin(math.pi * (1 - k / 10)):.1f}" '
        f'x2="{(r - 44) * math.cos(math.pi * (1 - k / 10)):.1f}" y2="{-(r - 44) * math.sin(math.pi * (1 - k / 10)):.1f}" '
        f'stroke="#fff" stroke-width="{6 if k % 5 == 0 else 3}" opacity="0.7"/>' for k in range(11))
    arc = f"M{-r + 18} 0 A{r - 18} {r - 18} 0 0 1 {r - 18} 0"
    ang = -90 + 180 * value
    return f"""<path d="M{-r} 0 A{r} {r} 0 0 1 {r} 0 z" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>
<path d="{arc}" class="nf {cls}" stroke-width="10" opacity="0.35"/>
<path d="{arc}" class="nf {cls}" stroke-width="10" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1">
<animate attributeName="stroke-dashoffset" from="1" to="{1 - value}" begin="{begin}s" dur="0.8s" fill="freeze"/></path>
{ticks}
<g transform="rotate(-90)"><animateTransform attributeName="transform" type="rotate" from="-90" to="{ang}" begin="{begin}s" dur="0.8s" fill="freeze"/>
<path d="M-8 0 L0 {-r + 30} L8 0 z" fill="{RED}"/></g>
<circle r="18" fill="#e9e9f0"/>
<text y="70" font-size="48" font-weight="700" text-anchor="middle" class="display {cls}">{text}</text>"""


def piece_path(s: float = 100) -> str:
    """A jigsaw piece outline centred at (0,0), body s x s, knobs on top and right."""
    a, k = s / 2, s / 5
    return (f"M{-a} {-a} h{a - k} a{k} {k} 0 1 1 {2 * k} 0 h{a - k} v{a - k} a{k} {k} 0 1 1 0 {2 * k} "
            f"v{a - k} h{-s} z")


def piece(s: float = 100, cls: str = "fa", inner: str = "") -> str:
    return (f'<path d="{piece_path(s)}" class="{cls}" stroke="#000" stroke-opacity="0.35" stroke-width="4"/>'
            f'<path d="{piece_path(s * 0.9)}" fill="#fff" opacity="0.18" transform="translate(-6 -6)"/>{inner}')


def socket(s: float = 100) -> str:
    return (f'<path d="{piece_path(s)}" fill="#fff" fill-opacity="0.04" stroke="#fff" stroke-opacity="0.5" '
            f'stroke-width="5" stroke-dasharray="14 10"/>')


def gpu_chip(s: float = 1.0) -> str:
    """A graphics chip centred at (0,0), 160 wide (scaled by s)."""
    pins = "".join(
        f'<rect x="{-62 + i * 18}" y="-92" width="8" height="18" fill="#d4b24a"/>'
        f'<rect x="{-62 + i * 18}" y="74" width="8" height="18" fill="#d4b24a"/>'
        f'<rect x="-92" y="{-62 + i * 18}" width="18" height="8" fill="#d4b24a"/>'
        f'<rect x="74" y="{-62 + i * 18}" width="18" height="8" fill="#d4b24a"/>' for i in range(8))
    return (f'<g transform="scale({s})">{pins}<rect x="-76" y="-76" width="152" height="152" rx="14" fill="url(#pcb)" '
            f'stroke="#fff" stroke-opacity="0.3" stroke-width="3"/>'
            f'<rect x="-48" y="-48" width="96" height="96" rx="8" fill="url(#steel)"/>'
            f'<text y="16" font-size="40" font-weight="700" text-anchor="middle" style="fill:#1a1a22">GPU</text></g>')


def cloud(s: float = 1.0) -> str:
    """An online-services cloud with a small server inside, centred at (0,0), about 220 wide."""
    return (f'<g transform="scale({s})"><path d="M-90 50 q-50 0 -50 -45 q0 -45 50 -45 q10 -60 80 -60 q60 0 80 50 '
            f'q60 -5 70 50 q0 50 -50 50 z" fill="url(#steel)" stroke="#000" stroke-opacity="0.2" stroke-width="3"/>'
            + "".join(f'<rect x="-46" y="{-28 + k * 26}" width="92" height="20" rx="5" fill="#2a2a32"/>'
                      f'<circle cx="30" cy="{-18 + k * 26}" r="5" class="fa"><animate attributeName="opacity" values="1;0.2;1" '
                      f'begin="{k * 0.2}s" dur="0.8s" repeatCount="indefinite"/></circle>' for k in range(3))
            + '</g>')


def books(s: float = 1.0) -> str:
    """A row of library books on a shelf, centred at (0,0), about 220 wide."""
    spec = ((-100, 170, "#4d8dff"), (-62, 190, "#3dff8f"), (-24, 160, "#ffd23f"), (14, 184, "#ff6b8a"), (52, 150, "#b07cff"))
    bk = "".join(f'<rect x="{x}" y="{80 - h}" width="34" height="{h}" rx="4" fill="{c}" stroke="#000" stroke-opacity="0.3" stroke-width="2"/>'
                 f'<rect x="{x + 6}" y="{80 - h + 20}" width="22" height="8" rx="3" fill="#fff" opacity="0.6"/>' for x, h, c in spec)
    lean = ('<g transform="rotate(18 92 80)"><rect x="92" y="-80" width="34" height="160" rx="4" fill="#ff9f43" '
            'stroke="#000" stroke-opacity="0.3" stroke-width="2"/></g>')
    return f'<g transform="scale({s})">{bk}{lean}<rect x="-120" y="80" width="260" height="16" rx="5" fill="#8a6a4a"/></g>'


def repo_card() -> str:
    """A code repository card at (0,0), 160x110: folder icon, name bars and a fork glyph."""
    return ('<rect x="0" y="0" width="160" height="110" rx="14" fill="url(#metal)" stroke="#fff" stroke-opacity="0.25" stroke-width="3"/>'
            '<path d="M18 26 h20 l8 8 h26 v28 h-54 z" class="fa"/>'
            '<rect x="84" y="30" width="58" height="10" rx="5" fill="#fff" opacity="0.6"/>'
            '<rect x="84" y="50" width="40" height="10" rx="5" fill="#fff" opacity="0.3"/>'
            '<circle cx="28" cy="82" r="6" fill="none" stroke="#fff" stroke-width="3"/>'
            '<circle cx="52" cy="82" r="6" fill="none" stroke="#fff" stroke-width="3"/>'
            '<circle cx="40" cy="100" r="6" fill="none" stroke="#fff" stroke-width="3" transform="translate(0 -4)"/>'
            '<rect x="84" y="78" width="58" height="10" rx="5" fill="#fff" opacity="0.3"/>')


# 0. GTA VI launched Nov 19; within days fans tried to run the Xbox version on PC ----------------------
arc = "M240 300 Q430 170 600 420"
out("launch", f"""
{place(70, 320, 1.0, xbox())}
{place(250, 880, 0.62, controller())}
{place(380, 440, 0.8, pc(appear(sunset(492, 302), 1.6, 0.6), "l"))}
<path d="{arc}" class="nf sa" stroke-width="10" stroke-linecap="round" stroke-dasharray="22 18" opacity="0">{fade(0.6)}
<animate attributeName="stroke-dashoffset" from="0" to="-40" dur="0.5s" repeatCount="indefinite"/></path>
{pop(606, 430, '<path d="M-30 -20 L10 30 L30 -26 z" class="fa"/>', 1.2)}
{badge(500, 120, "GTA VI · NOV 19", 0.3)}
""")

# 1. No PC version has even been announced -----------------------------------------------------------
rows = []
for k, (name, ok) in enumerate((("PlayStation 5", True), ("Xbox Series", True), ("PC", False))):
    y = 300 + k * 84
    mark = check(30) if ok else cross(30)
    extra = '' if ok else f'<text x="0" y="14" font-size="40" font-weight="700" text-anchor="end" style="fill:{RED}">Not announced</text>'
    rows.append(appear(f'<rect x="30" y="{y - 36}" width="696" height="72" rx="14" fill="#fff" fill-opacity="0.06"/>'
                       f'<text x="60" y="{y + 15}" font-size="44" font-weight="700">{name}</text>', 0.2 + k * 0.2)
                + pop(680, y, mark, 0.35 + k * 0.2 + (0.15 if not ok else 0))
                + (appear(f'<g transform="translate(620 {y})">{extra}</g>', 0.9) if not ok else ""))
out("no-pc", f"""
{place(110, 150, 1.0, monitor(780, 560, sunset(752, 220) + ''.join(rows), "n"))}
""")

# 2. How do you turn a console game into a PC game without its source code? ------------------------
lock = ('<rect x="-46" y="-10" width="92" height="74" rx="12" fill="#ffd23f"/>'
        '<path d="M-28 -10 v-24 a28 28 0 0 1 56 0 v24" fill="none" stroke="#ffd23f" stroke-width="14"/>'
        '<circle cx="0" cy="22" r="10" fill="#0a0a0a"/><rect x="-4" y="22" width="8" height="24" fill="#0a0a0a"/>')
sheet = ('<rect x="0" y="0" width="220" height="270" rx="16" fill="url(#paper)"/>'
         + "".join(f'<rect x="{24 + (i % 3) * 18}" y="{30 + i * 30}" width="{150 - (i % 4) * 26}" height="12" rx="6" fill="#9a968b"/>' for i in range(8)))
out("question", f"""
{place(60, 360, 0.9, xbox())}
{place(410, 460, 0.75, pc(f'<rect width="492" height="302" fill="#000"/>', "q"))}
{bob(place(330, 70, 1.0, sheet), 8, 3)}
{pop(440, 250, lock, 0.6)}
{pop(790, 230, '<circle r="100" class="fa"/><text y="62" font-size="180" font-weight="700" text-anchor="middle" style="fill:#0a0a0a">?</text>', 1.0)}
""")

# 3. You translate its machine code, the raw instructions the processor runs ------------------------
beam = ('<rect x="40" y="290" width="400" height="10" class="fa" opacity="0" filter="url(#glow)">'
        '<animateTransform attributeName="transform" type="translate" values="0 0;0 400;0 0" dur="2.4s" begin="1.2s" repeatCount="indefinite"/>'
        f'{fade(1.2, 0.2, 0.8)}</rect>')
chev = "".join(
    f'<path d="M{470 + i * 24} 450 l26 30 l-26 30" fill="none" class="sa" stroke-width="10" stroke-linecap="round" opacity="0.2">'
    f'<animate attributeName="opacity" values="0.2;1;0.2" begin="{i * 0.2}s" dur="0.8s" repeatCount="indefinite"/></path>' for i in range(3))
out("translate", f"""
{place(40, 200, 0.95, code_card(XB_HEX, 0.1, 420, "#e9e9f0", 0.12))}
{beam}
{chev}
{place(560, 200, 0.95, code_card(PC_HEX, 1.4, 420, GREEN, 0.18))}
{appear(label(240, 780, "Xbox code", 48), 0.3)}
{appear(label(760, 780, "PC code", 48, "fa"), 1.4)}
""")

# 4. A fan project called Leonida tried exactly that, using leaked files from an Xbox build ----------
def doc(b: float, dx: float) -> str:
    d = ('<rect x="-34" y="-44" width="68" height="88" rx="8" fill="url(#paper)"/>'
         '<rect x="-20" y="-26" width="40" height="8" rx="4" fill="#9a968b"/><rect x="-20" y="-8" width="30" height="8" rx="4" fill="#9a968b"/>')
    return (f'<g opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.85;1" begin="{b}s" dur="1.8s" repeatCount="indefinite"/>'
            f'<animateMotion path="M175 320 Q{400 + dx} 120 640 470" begin="{b}s" dur="1.8s" repeatCount="indefinite" rotate="auto"/>{d}</g>')


editor = ('<rect width="492" height="302" fill="#0b0f0d"/>'
          '<path d="M14 40 v-20 q0 -10 10 -10 h150 q10 0 10 10 v20 z" fill="#1d2a22"/>'
          '<circle cx="34" cy="26" r="7" class="fa"/><text x="50" y="36" font-size="26">Leonida</text>'
          + "".join(appear(f'<rect x="{30 + (k % 3) * 24}" y="{64 + k * 30}" width="{180 + (k * 53) % 200}" height="14" rx="7" '
                           f'fill="{(GREEN, "#7fd1ff", "#ffd23f", "#e9e9f0")[k % 4]}" opacity="0.85"/>', 0.8 + k * 0.25, 0.1) for k in range(8)))
out("leonida", f"""
{place(50, 360, 0.9, xbox())}
{place(400, 440, 0.75, pc(editor, "e"))}
{doc(0.6, 0)}{doc(1.2, 40)}{doc(1.8, -40)}
{badge(500, 140, "LEAKED XBOX FILES", 0.4)}
""")

# 5. Emulation: a program pretends to be the console, live, while you play --------------------------
emu_screen = (sunset(692, 432)
              + '<rect x="18" y="18" width="250" height="396" rx="18" fill="#000" opacity="0.72"/>'
              + place(48, 52, 0.62, xbox())
              + '<rect x="30" y="34" width="226" height="370" rx="20" fill="none" class="sa" stroke-width="6" stroke-dasharray="16 12">'
              + '<animate attributeName="stroke-dashoffset" from="0" to="-56" dur="0.7s" repeatCount="indefinite"/></rect>'
              + f'<g transform="translate(520 52)"><rect x="-12" y="-30" width="150" height="56" rx="12" fill="#000" opacity="0.7"/>'
              + f'<circle cx="16" cy="-2" r="12" fill="{RED}"><animate attributeName="opacity" values="1;0.2;1" dur="0.8s" repeatCount="indefinite"/></circle>'
              + '<text x="40" y="12" font-size="36" font-weight="700">LIVE</text></g>')
out("emulation", f"""
{place(140, 130, 1.0, monitor(720, 460, emu_screen, "em"))}
{place(500, 760, 0.6, controller())}
{badge(500, 905, "EMULATION", 1.0)}
""")

# 6. Recompilation translates once, ahead of time, into a new PC program that runs far faster -------
chunks = "".join(
    f'<rect x="-22" y="-14" width="44" height="28" rx="6" class="fa" opacity="0">'
    f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.8;1" begin="{i * 0.4}s" dur="1.2s" repeatCount="indefinite"/>'
    f'<animateMotion path="M180 300 Q300 120 445 200" begin="{i * 0.4}s" dur="1.2s" repeatCount="indefinite"/></rect>' for i in range(3))
out("recompile", f"""
{place(30, 260, 0.55, code_card(XB_HEX[:6], 0, 420))}
{chunks}
{place(330, 270, 0.95, machine())}
{draw("M700 420 L748 420", 0.7, 0.3, "nf sa", 10)}
{pop(860, 400, place(-100, -125, 0.95, exe()), 0.9)}
{place(500, 800, 1.0, gauge(170, 0.92, 1.2, "FASTER"))}
""")

# 7. But here's the part most people miss: the code is the easy bit --------------------------------
inside = (f'<rect x="20" y="54" width="190" height="384" rx="14" fill="url(#pcb)" stroke="#000" stroke-width="3" opacity="0">{fade(0.4, 0.4)}</rect>'
          + appear('<rect x="34" y="68" width="162" height="70" rx="10" class="fa"/>'
                   '<text x="115" y="116" font-size="36" font-weight="700" text-anchor="middle" style="fill:#0a0a0a;font-family:monospace">CODE</text>', 0.7)
          + appear(place(115, 220, 0.62, gpu_chip()) + fan(115, 370, 50, 0.7)
                   + ''.join(f'<rect x="{40 + k * 52}" y="292" width="38" height="24" rx="4" fill="#1a1a22" stroke="#d4b24a" stroke-width="2"/>' for k in range(3))
                   + ''.join(f'<path d="M{34 + k * 12} 160 v{260 - k * 20}" stroke="#d4b24a" stroke-width="2" opacity="0.6"/>' for k in range(3)), 1.0))
out("easy-bit", f"""
{place(330, 110, 1.5, xbox() + inside)}
{pop(640, 270, check(34), 1.3)}
{draw("M760 270 L690 270", 1.5, 0.3, "nf sw", 6)}
{appear(label(775, 286, "Easy bit", 48, "fa", "start"), 1.5)}
{draw("M760 560 L640 560", 2.2, 0.3, "nf sw", 6)}
{appear(label(775, 576, "The rest", 48, "fa2", "start"), 2.2)}
""")

# 8. A console game leans on graphics, services and libraries. A PC has none of them ----------------
deps = [(180, 640, gpu_chip(0.95)), (500, 650, cloud(0.95)), (820, 640, books(0.95))]
cables = "".join(draw(f"M500 340 C500 460 {x} 460 {x} {y - 110}", 0.4 + k * 0.2, 0.6, "nf sa", 8) for k, (x, y, _) in enumerate(deps))
out("missing", f"""
{place(400, 80, 1.0, exe())}
{cables}
{''.join(pop(x, y, d, 0.8 + k * 0.25) for k, (x, y, d) in enumerate(deps))}
{''.join(pop(x + 90, y - 90, cross(36), 2.0 + k * 0.3) for k, (x, y, _) in enumerate(deps))}
{appear(label(500, 900, "None of these on a PC", 50), 2.0)}
""")


# 9. Every missing piece needs a stand-in, called a shim ------------------------------------------
def fly(x: float, y: float, fx: float, fy: float, b: float, inner: str) -> str:
    return (f'<g transform="translate({x} {y})"><g opacity="0">{fade(b, 0.15)}'
            f'<animateTransform attributeName="transform" type="translate" from="{fx - x} {fy - y}" to="0 0" begin="{b}s" dur="0.5s" fill="freeze"/>'
            f'{inner}</g></g>')


icons = [place(0, 0, 0.42, gpu_chip()), place(0, 6, 0.36, cloud()), place(-4, -8, 0.38, books())]
slots = [(200, 600), (500, 600), (800, 600)]
out("shim", f"""
{place(400, 90, 1.0, exe())}
{''.join(draw(f"M500 340 C500 450 {x} 440 {x} {y - 85}", 0.2, 0.5, "nf sa", 8) for x, y in slots)}
{''.join(f'<g transform="translate({x} {y})">{socket(150)}</g>' for x, y in slots)}
{''.join(fly(x, y, x + (-260, 0, 260)[k], 1060, 0.3 + k * 0.3, piece(150, "fa", icons[k])) for k, (x, y) in enumerate(slots))}
{''.join(pop(x + 70, y + 70, check(30), 0.85 + k * 0.3) for k, (x, y) in enumerate(slots))}
{badge(500, 880, "SHIM = STAND-IN", 1.6)}
""")

# 10. Leonida reached the menus and setup screens, then went black ----------------------------------
menu = (sunset(752, 472) + '<rect width="752" height="472" fill="#000" opacity="0.45"/>'
        + '<rect x="40" y="40" width="330" height="390" rx="16" fill="#000" opacity="0.55"/>'
        + '<rect x="56" y="80" width="298" height="64" rx="10" class="fa" opacity="0.9">'
        + '<animateTransform attributeName="transform" type="translate" values="0 0;0 84;0 168;0 168" keyTimes="0;0.3;0.6;1" dur="2s" fill="freeze"/></rect>'
        + "".join(f'<text x="80" y="{125 + k * 84}" font-size="38" font-weight="700">{t}</text>'
                  for k, t in enumerate(("LANGUAGE", "DISPLAY", "SETTINGS", "CONTINUE")))
        + '<rect width="752" height="472" fill="#000" opacity="0"><animate attributeName="opacity" from="0" to="1" begin="2.2s" dur="0.25s" fill="freeze"/></rect>'
        + '<text x="40" y="440" font-size="48" font-weight="700" opacity="0" style="font-family:monospace">_'
        + '<animate attributeName="opacity" values="0;1;0" begin="2.5s" dur="0.9s" repeatCount="indefinite"/></text>')
out("black-screen", f"""
{place(110, 140, 1.0, monitor(780, 500, menu, "bs"))}
{appear(label(500, 860, "Menus... then black", 52), 2.3)}
""")

# 11. Take-Two filed a copyright takedown; GitHub removed 3,007 copies of the project --------------
cards = []
for j in range(4):
    for i in range(5):
        k = j * 5 + i
        cards.append(f'<g transform="translate({70 + i * 176} {110 + j * 128})">{repo_card()}'
                     f'<rect x="0" y="0" width="160" height="110" rx="14" fill="#000" opacity="0">'
                     f'<animate attributeName="opacity" from="0" to="0.75" begin="{1.3 + k * 0.06:.2f}s" dur="0.2s" fill="freeze"/></rect></g>')
stamp = (f'<g transform="rotate(-12)"><rect x="-250" y="-70" width="500" height="140" rx="16" fill="none" stroke="{RED}" stroke-width="14"/>'
         f'<rect x="-250" y="-70" width="500" height="140" rx="16" fill="{RED}" opacity="0.18"/>'
         f'<text y="34" font-size="96" font-weight="700" text-anchor="middle" class="display" style="fill:{RED}">REMOVED</text></g>')
out("takedown", f"""
{''.join(cards)}
{pop(500, 360, stamp, 1.1)}
{appear('<text x="500" y="850" font-size="170" text-anchor="middle" class="display fa">3,007</text>', 1.8)}
""")

# 12. Its Discord, with almost 180,000 members, went dark too ---------------------------------------
avatars = "".join(
    f'<circle cx="610" cy="{150 + k * 62}" r="22" fill="{("#3dff8f", "#7fd1ff", "#ffd23f", "#ff6b8a", "#b07cff", "#ff9f43", "#4d8dff")[k]}"/>'
    f'<rect x="644" y="{142 + k * 62}" width="{120 - (k * 23) % 60}" height="16" rx="8" fill="#fff" opacity="0.5"/>' for k in range(7))
bubbles = "".join(
    appear(f'<circle cx="140" cy="{130 + k * 96}" r="24" fill="{("#ffd23f", "#7fd1ff", "#ff6b8a", "#3dff8f")[k]}"/>'
           f'<rect x="178" y="{112 + k * 96}" width="{300 - (k * 70) % 160}" height="40" rx="14" fill="#fff" opacity="0.14"/>', 0.2 + k * 0.25)
    for k in range(4))
servers = "".join(f'<circle cx="46" cy="{100 + k * 76}" r="28" fill="{c}"/>'
                  for k, c in enumerate(("#3dff8f", "#4a4a56", "#4a4a56", "#4a4a56")))
chat = f"""{shadow(410, 610, 400, 22)}
<rect x="0" y="0" width="820" height="600" rx="26" fill="#14161a" stroke="#fff" stroke-opacity="0.25" stroke-width="4"/>
<rect x="0" y="0" width="92" height="600" rx="26" fill="#0c0d10"/>{servers}
<rect x="92" y="0" width="728" height="70" fill="#1b1e23"/>
<text x="124" y="48" font-size="36" font-weight="700"># leonida</text>
<rect x="570" y="70" width="250" height="530" fill="#101215"/>
<text x="590" y="110" font-size="28" style="fill:#9a9aa6">MEMBERS</text>
{avatars}{bubbles}
<rect x="120" y="520" width="420" height="52" rx="14" fill="#fff" opacity="0.08"/>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="1.6s" dur="0.6s" fill="freeze"/>
<rect x="0" y="0" width="820" height="600" rx="26" fill="#000" opacity="0.86"/>
<text x="410" y="320" font-size="50" font-weight="700" text-anchor="middle" style="fill:#9a9aa6">Server unavailable</text></g>"""
out("discord-dark", f"""
{place(90, 120, 1.0, chat)}
{appear('<text x="500" y="860" font-size="110" text-anchor="middle" class="display fa">180,000</text>', 0.5)}
""")

# 13. The hard part isn't translating the game. It's rebuilding the whole console around it ----------
grid = [(x, y) for y in (190, 320, 450, 580, 710) for x in (370, 500, 630)
        if not (x == 500 and y in (320, 450, 580))]
pieces = "".join(pop(x, y, piece(118, ("fa", "fa2")[(i * 7) % 3 == 0]), 0.9 + i * 0.13) for i, (x, y) in enumerate(grid))
out("rebuild", f"""
{shadow(500, 790, 260, 24)}
{draw("M314 140 h372 q24 0 24 24 v592 q0 24 -24 24 h-372 q-24 0 -24 -24 v-592 q0 -24 24 -24 z", 0.1, 0.8, "nf sw", 6, 'opacity="0.7"')}
{pieces}
{pop(500, 455, place(-90, -112, 0.9, exe()), 0.4)}
{waves(500, 455, "sa", 3, 120, 420, 2.2, 6, 0.5, start=2.5)}
{appear(label(500, 910, "Rebuild the console around it", 50), 2.6)}
""")
