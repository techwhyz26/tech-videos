"""Illustrations for the 'prison-phone-jamming' video. Run:  python tools/art_prison_phone_jamming.py

Objects (prison, jammer, cell tower, house, drone, phone screens) are drawn once in their own
coordinates and placed with translate+scale, so every scene reuses them at any size.
"""
import math
import random

from artlib import appear, badge, bob, draw, fade, label, phone, pop, save, shadow, sine, waves

SLUG = "prison-phone-jamming"
RED = "#ff4d4d"
GREEN = "#3ddc84"


def place(x: float, y: float, s: float, inner: str) -> str:
    return f'<g transform="translate({x} {y}) scale({s})">{inner}</g>'


# --- objects ----------------------------------------------------------------------------------

def fence(x0: float, x1: float, top: float, bottom: float, uid: str, post: float = 6) -> str:
    """Chain-link fence with razor wire on top."""
    step = 62
    posts = "".join(f'<rect x="{x - post / 2}" y="{top}" width="{post}" height="{bottom - top}" fill="#c9c9d2"/>'
                    for x in range(int(x0), int(x1) + 1, step))
    coils = "".join(f'<circle cx="{x}" cy="{top - 12}" r="12" fill="none" stroke="#d8d8e0" stroke-width="3"/>'
                    for x in range(int(x0), int(x1) + 1, 20))
    return (f'<pattern id="{uid}m" width="18" height="18" patternUnits="userSpaceOnUse">'
            f'<path d="M0 0 L18 18 M18 0 L0 18" stroke="#d8d8e0" stroke-width="1.6" opacity="0.55"/></pattern>'
            f'<rect x="{x0}" y="{top}" width="{x1 - x0}" height="{bottom - top}" fill="url(#{uid}m)"/>'
            f'<rect x="{x0}" y="{top}" width="{x1 - x0}" height="5" fill="#c9c9d2"/>'
            f'<rect x="{x0}" y="{bottom - 5}" width="{x1 - x0}" height="5" fill="#c9c9d2"/>{posts}{coils}')


def jammer() -> str:
    """A jammer box at (0,0), 260x170, with antennas reaching up to y=-150."""
    ants = "".join(
        f'<rect x="{26 + i * 42}" y="-14" width="22" height="20" rx="4" fill="#2a2a32"/>'
        f'<line x1="{37 + i * 42}" y1="-10" x2="{37 + i * 42}" y2="{-(105 if i % 2 else 145)}" stroke="#18181d" stroke-width="14" stroke-linecap="round"/>'
        for i in range(6))
    vents = "".join(f'<rect x="22" y="{36 + i * 18}" width="110" height="8" rx="4" fill="#000" opacity="0.5"/>' for i in range(5))
    leds = "".join(
        f'<circle cx="{30 + i * 26}" cy="142" r="8" fill="{RED}"><animate attributeName="opacity" values="1;0.25;1" '
        f'begin="{i * 0.12}s" dur="0.5s" repeatCount="indefinite"/></circle>' for i in range(5))
    blades = "".join(f'<path d="M0 0 L{34 * math.cos(a):.0f} {34 * math.sin(a):.0f} L{34 * math.cos(a + 0.6):.0f} {34 * math.sin(a + 0.6):.0f} z" fill="#55555f"/>'
                     for a in (0, 2.09, 4.19))
    return f"""{shadow(130, 182, 160, 16)}{ants}
<rect x="0" y="0" width="260" height="170" rx="18" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>
<rect x="10" y="8" width="240" height="8" rx="4" fill="#fff" opacity="0.12"/>
{vents}
<circle cx="196" cy="74" r="46" fill="#0c0c10" stroke="#55555f" stroke-width="5"/>
<g transform="translate(196 74)"><g><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="0.4s" repeatCount="indefinite"/>{blades}</g></g>
<circle cx="196" cy="74" r="8" fill="#8d8d99"/>
{leds}
<rect x="160" y="130" width="80" height="24" rx="6" fill="#08080a"/>
<rect x="166" y="136" width="50" height="12" rx="3" class="fa"><animate attributeName="width" values="20;68;34;60;20" dur="0.6s" repeatCount="indefinite"/></rect>"""


def prison(uid: str, jam: bool = False) -> str:
    """A prison at (0,0): about 610 wide, ground at y=380. Jammer on the roof at about (311, 40)."""
    wins = "".join(
        f'<rect x="{122 + i * 62}" y="{150 + j * 78}" width="34" height="46" rx="4" fill="#1a1a22"/>'
        f'<path d="M{133 + i * 62} {150 + j * 78} v46 M{145 + i * 62} {150 + j * 78} v46" stroke="#b9b9c6" stroke-width="3"/>'
        for i in range(7) for j in range(2))
    beam = (f'<g opacity="0.16"><animateTransform attributeName="transform" type="rotate" values="-18 35 40;14 35 40;-18 35 40" '
            f'dur="4s" repeatCount="indefinite"/><polygon points="35,40 380,330 250,370" fill="#fff6c4"/></g>')
    roof = place(240, 22, 0.55, jammer()) if jam else ""
    return f"""{shadow(300, 384, 330, 18)}
{beam}
<rect x="80" y="96" width="490" height="22" rx="4" fill="#b3b2bc"/>
<rect x="90" y="112" width="470" height="268" fill="#8f8e98"/>
<rect x="90" y="112" width="470" height="268" fill="url(#metal)" opacity="0.35"/>
<rect x="90" y="112" width="470" height="14" fill="#000" opacity="0.2"/>
{wins}
<rect x="292" y="300" width="66" height="80" rx="4" fill="#3a3a44"/>
<rect x="292" y="300" width="66" height="10" fill="#000" opacity="0.3"/>
{roof}
<rect x="8" y="60" width="54" height="320" fill="#7d7c86"/>
<rect x="8" y="60" width="18" height="320" fill="#fff" opacity="0.08"/>
<rect x="-6" y="10" width="82" height="56" rx="6" fill="url(#metal)"/>
<rect x="4" y="24" width="62" height="22" rx="3" class="fa2" opacity="0.85"/>
<polygon points="-16,12 35,-22 86,12" fill="#5a5a66"/>
{fence(-10, 610, 292, 380, uid)}"""


def tower() -> str:
    """A cell tower at (0,0) = base centre, about 550 tall."""
    levels = [i * 470 / 8 for i in range(9)]
    xl = lambda y: -70 + 54 * y / 470
    braces = "".join(
        f'<line x1="{xl(levels[k]):.0f}" y1="{-levels[k]:.0f}" x2="{-xl(levels[k + 1]):.0f}" y2="{-levels[k + 1]:.0f}" stroke="#9a9aa6" stroke-width="5"/>'
        f'<line x1="{-xl(levels[k]):.0f}" y1="{-levels[k]:.0f}" x2="{xl(levels[k + 1]):.0f}" y2="{-levels[k + 1]:.0f}" stroke="#9a9aa6" stroke-width="5"/>'
        for k in range(8))
    panels = "".join(f'<rect x="{x}" y="-488" width="26" height="92" rx="6" fill="url(#steel)"/>' for x in (-48, -13, 22))
    return f"""{shadow(0, 8, 120, 16)}
<line x1="-70" y1="0" x2="-16" y2="-470" stroke="#c4c4ce" stroke-width="11" stroke-linecap="round"/>
<line x1="70" y1="0" x2="16" y2="-470" stroke="#c4c4ce" stroke-width="11" stroke-linecap="round"/>
{braces}
<rect x="-40" y="-250" width="80" height="12" rx="4" fill="#8d8d99"/>
<circle cx="-30" cy="-300" r="22" fill="url(#steel)"/>
{panels}
<line x1="0" y1="-488" x2="0" y2="-540" stroke="#c4c4ce" stroke-width="8"/>
<circle cx="0" cy="-546" r="11" fill="{RED}"><animate attributeName="opacity" values="1;0.2;1" dur="1.2s" repeatCount="indefinite"/></circle>"""


def house(lit: bool = True) -> str:
    """A house at (0,0) = ground centre, 240 wide, about 245 tall."""
    glow = "#ffd76a" if lit else "#2a2a32"
    return f"""{shadow(0, 6, 130, 14)}
<rect x="54" y="-232" width="28" height="60" fill="#6b3a2c"/>
<rect x="-100" y="-150" width="200" height="150" fill="#d8c3a5"/>
<rect x="-100" y="-150" width="200" height="16" fill="#000" opacity="0.15"/>
<polygon points="-122,-148 0,-244 122,-148" fill="#a1473a"/>
<polygon points="0,-244 122,-148 100,-148 0,-226" fill="#000" opacity="0.18"/>
<rect x="-80" y="-120" width="50" height="44" rx="4" fill="{glow}"/>
<rect x="30" y="-120" width="50" height="44" rx="4" fill="{glow}"/>
<path d="M-55 -120 v44 M-80 -98 h50 M55 -120 v44 M30 -98 h50" stroke="#8a6a4a" stroke-width="4"/>
<rect x="-20" y="-78" width="40" height="78" rx="4" fill="#5a3a28"/>
<circle cx="12" cy="-38" r="4" fill="#e0c080"/>"""


def drone(cargo: bool = True) -> str:
    """A quadcopter centred on (0,0), about 280 wide; a phone hangs under it."""
    rotors = "".join(
        f'<line x1="{sx * 40}" y1="-6" x2="{sx * 120}" y2="-34" stroke="#2a2a32" stroke-width="12" stroke-linecap="round"/>'
        f'<rect x="{sx * 120 - 6}" y="-46" width="12" height="16" fill="#18181d"/>'
        f'<ellipse cx="{sx * 120}" cy="-48" rx="62" ry="7" fill="#fff" opacity="0.5">'
        f'<animate attributeName="rx" values="62;12;62" dur="0.14s" repeatCount="indefinite"/></ellipse>'
        for sx in (-1, 1))
    pkg = ""
    if cargo:
        pkg = ('<line x1="0" y1="18" x2="0" y2="52" stroke="#d8d8e0" stroke-width="3"/>'
               '<rect x="-26" y="52" width="52" height="92" rx="10" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="2"/>'
               '<rect x="-20" y="60" width="40" height="76" rx="6" class="fa" opacity="0.7"/>')
    return f"""{rotors}
<rect x="-54" y="-22" width="108" height="40" rx="16" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="3"/>
<circle cx="0" cy="22" r="12" fill="#111" stroke="#55555f" stroke-width="3"/>
<circle cx="30" cy="-4" r="5" fill="{GREEN}"><animate attributeName="opacity" values="1;0.2;1" dur="0.5s" repeatCount="indefinite"/></circle>
{pkg}"""


def bars(x: float, y: float, lit: int = 4, drops: tuple = (), s: float = 1) -> str:
    """Signal bars with bottom-left at (x,y). `drops` are times at which lit bars go dark (top bar first)."""
    out = []
    for i in range(4):
        h = (12 + i * 9) * s
        on = i < lit
        anim = ""
        k = lit - 1 - i
        if on and k < len(drops):
            anim = f'<animate attributeName="opacity" from="1" to="0.2" begin="{drops[k]}s" dur="0.15s" fill="freeze"/>'
        out.append(f'<rect x="{x + i * 13 * s}" y="{y - h}" width="{9 * s}" height="{h}" rx="2" fill="#fff" '
                   f'opacity="{1 if on else 0.2}">{anim}</rect>')
    return "".join(out)


def jag(x0: float, x1: float, y: float, amp: float, seed: int, step: float = 16) -> list[str]:
    """Three jagged noise lines with the same number of points, to morph between."""
    out = []
    for k in range(3):
        r = random.Random(seed * 10 + k)
        pts = []
        x = x0
        while x <= x1:
            pts.append(f"{x:.0f} {y + r.uniform(-amp, amp):.0f}")
            x += step
        out.append("M " + " L ".join(pts))
    return out


def noise(x0, x1, y, amp, seed, width=6, cls="sa", begin=0.0, dur=0.3, extra="") -> str:
    a, b, c = jag(x0, x1, y, amp, seed)
    return (f'<path d="{a}" class="nf {cls}" stroke-width="{width}" stroke-linejoin="round" opacity="0" {extra}>{fade(begin, 0.3)}'
            f'<animate attributeName="d" values="{a};{b};{c};{a}" dur="{dur}s" repeatCount="indefinite"/></path>')


def scrolling_sine(y, amp, period, cls, dur, width=8, x0=0, x1=1000, extra="") -> str:
    return (f'<path d="{sine(x0 - 2 * period, x1 + 2 * period, y, amp, period)}" class="nf {cls}" '
            f'stroke-width="{width}" stroke-linecap="round" {extra}>'
            f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{period} 0" '
            f'dur="{dur}s" repeatCount="indefinite"/></path>')


def status(w: float, lit: int = 4, drops: tuple = (), carrier: str = "LTE") -> str:
    """Phone status bar for a screen `w` wide (narrow screens show only the bars)."""
    if w < 240:
        return bars(w / 2 - 22, 66, lit, drops, 1.2)
    return (f'<text x="26" y="56" font-size="24" opacity="0.8">9:41</text>'
            f'{bars(w - 110, 58, lit, drops, 1.1)}'
            f'<text x="{w - 52}" y="56" font-size="22" opacity="0.8">{carrier}</text>')


def check(begin: float, r: float = 44) -> str:
    return (f'<circle r="{r}" fill="{GREEN}"/><path d="M{-r * .42:.0f} 0 l{r * .28:.0f} {r * .32:.0f} l{r * .56:.0f} {-r * .64:.0f}" '
            f'fill="none" stroke="#fff" stroke-width="{r * .22:.0f}" stroke-linecap="round" stroke-linejoin="round"/>')


def cross(r: float = 50) -> str:
    return (f'<circle r="{r}" fill="{RED}"/><path d="M{-r * .4:.0f} {-r * .4:.0f} L{r * .4:.0f} {r * .4:.0f} M{r * .4:.0f} {-r * .4:.0f} L{-r * .4:.0f} {r * .4:.0f}" '
            f'stroke="#fff" stroke-width="{r * .22:.0f}" stroke-linecap="round"/>')


def prison_top(uid: str) -> str:
    """A prison seen from above, centred on (0,0), fence 340 wide."""
    blocks = "".join(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#8f8e98"/>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h / 2}" rx="6" fill="#fff" opacity="0.12"/>'
        f'<line x1="{x + 8}" y1="{y + h / 2}" x2="{x + w - 8}" y2="{y + h / 2}" stroke="#000" stroke-opacity="0.25" stroke-width="3"/>'
        for x, y, w, h in ((-120, -120, 240, 64), (-120, 56, 240, 64), (-120, -40, 70, 80)))
    towers = "".join(f'<circle cx="{x}" cy="{y}" r="18" fill="#7d7c86" stroke="#c9c9d2" stroke-width="4"/>'
                     for x in (-160, 160) for y in (-160, 160))
    return (f'{shadow(0, 14, 190, 30, 0.5)}'
            f'<rect x="-170" y="-170" width="340" height="340" rx="10" fill="none" stroke="#c9c9d2" stroke-width="5" stroke-dasharray="10 7"/>'
            f'<rect x="-150" y="-150" width="300" height="300" rx="8" fill="#5d6a4f"/>'
            f'<rect x="-150" y="-150" width="300" height="300" rx="8" fill="none" stroke="#b3b2bc" stroke-width="12"/>'
            f'{blocks}<rect x="-30" y="-30" width="140" height="60" rx="30" fill="#c2a878" opacity="0.6"/>{towers}')


# --- scenes -------------------------------------------------------------------------------------

# 1. US prisons just got permission to jam cell phones
hook_screen = (status(126, 4, (1.0, 1.2, 1.4, 1.6))
               + f'<g opacity="0">{fade(1.7, 0.2)}<g transform="translate(68 150)">{cross(44)}</g></g>')
save(SLUG, "hook", f"""
{waves(511, 370, "sa", 3, 40, 520, 2.0, 12, 0.85, 0.6)}
{place(200, 330, 1.0, prison("h", jam=True))}
{bob(phone(20, 30, 160, 290, hook_screen), 6, 2.8)}
{badge(500, 880, "PHONES JAMMED", 1.9)}
""")

# 2. The FCC voted three to zero
lines = "".join(draw(f"M310 {610 + i * 34} h{380 - i * 60}", 0.3 + i * 0.15, 0.4, "nf", 10, 'stroke="#c9c5ba"') for i in range(4))
stamp = (f'<g transform="rotate(-14)"><rect x="-160" y="-56" width="320" height="112" rx="16" fill="#fff" fill-opacity="0.6" stroke="{RED}" stroke-width="10"/>'
         f'<text y="20" font-size="58" font-weight="700" text-anchor="middle" style="fill:{RED}">APPROVED</text></g>')
save(SLUG, "vote", f"""
{shadow(500, 770, 280, 22)}
<g transform="rotate(-3 500 430)">
  <rect x="250" y="100" width="500" height="660" rx="18" fill="url(#paper)"/>
  <text x="500" y="190" font-size="64" font-weight="700" text-anchor="middle" style="fill:#111">FCC</text>
  <text x="500" y="236" font-size="30" text-anchor="middle" style="fill:#555">ORDER</text>
  <rect x="300" y="262" width="400" height="6" rx="3" fill="#c9c5ba"/>
  <rect x="300" y="290" width="400" height="290" rx="12" fill="#2a2f3a"/>
  {place(330, 330, 0.56, prison("v"))}
  {lines}
</g>
{pop(610, 660, stamp, 1.3)}
{appear('<text x="500" y="935" font-size="150" text-anchor="middle" class="display fa">3 - 0</text>', 0.8)}
""")

# 3. Over 25,000 smuggled phones found in the prisons of twenty states
ground_phones = "".join(
    f'<g opacity="0">{fade(0.8 + i * 0.25, 0.15)}<g transform="translate({x} {y}) rotate({rot})">'
    f'<rect x="-22" y="-38" width="44" height="76" rx="8" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="2"/>'
    f'<rect x="-16" y="-31" width="32" height="62" rx="5" class="fa" opacity="0.6"/></g></g>'
    for i, (x, y, rot) in enumerate(((300, 640, -20), (380, 655, 15), (470, 645, 70), (560, 660, -40), (640, 640, 25), (720, 655, -10), (430, 615, 40))))
flight = (f'<g><animateTransform attributeName="transform" type="translate" values="-200 190;640 170" '
          f'dur="1.1s" fill="freeze"/>{bob(drone(), 12, 1.6)}</g>')
save(SLUG, "smuggle", f"""
{place(260, 250, 0.8, prison("sm"))}
{ground_phones}
{fence(20, 980, 600, 790, "sf", 10)}
{shadow(500, 800, 500, 18, 0.4)}
{flight}
{appear('<text x="500" y="930" font-size="120" text-anchor="middle" class="display fa">25,000+ PHONES</text>', 1.4)}
""")

# 4. So how do you switch off a phone nobody can find?
def hidden_phone(x, y, rot, b):
    return (f'<g transform="translate({x} {y}) rotate({rot})">'
            f'<circle r="70" class="fa" opacity="0.5" filter="url(#soft)"><animate attributeName="opacity" values="0.2;0.7;0.2" begin="{b}s" dur="1.4s" repeatCount="indefinite"/></circle>'
            f'<rect x="-22" y="-38" width="44" height="76" rx="8" fill="url(#metal)"/>'
            f'<rect x="-16" y="-31" width="32" height="62" rx="5" class="fa"/></g>')


cells = []
for k in range(3):
    x = 60 + k * 293
    cells.append(
        f'<rect x="{x}" y="200" width="293" height="560" fill="#5d5c66"/>'
        f'<rect x="{x}" y="690" width="293" height="70" fill="#45444c"/>'
        f'<rect x="{x + 30}" y="560" width="200" height="22" rx="4" fill="url(#steel)"/>'
        f'<rect x="{x + 34}" y="540" width="192" height="24" rx="10" fill="#3c5a8a"/>'
        f'<rect x="{x + 40}" y="582" width="10" height="108" fill="#9a9aa6"/><rect x="{x + 210}" y="582" width="10" height="108" fill="#9a9aa6"/>'
        f'<rect x="{x + 90}" y="250" width="110" height="80" rx="6" fill="#2a2a32"/>'
        f'<path d="M{x + 117} 250 v80 M{x + 145} 250 v80 M{x + 173} 250 v80" stroke="#9a9aa6" stroke-width="5"/>')
walls = "".join(f'<rect x="{x}" y="200" width="16" height="560" fill="#3a3a44"/>' for x in (345, 638))
bars_front = "".join(f'<rect x="{x}" y="200" width="7" height="560" fill="#c9c9d2" opacity="0.9"/>' for x in range(76, 940, 44))
save(SLUG, "question", f"""
{shadow(500, 770, 470, 20)}
{''.join(cells)}{walls}
{hidden_phone(170, 548, -78, 0)}
{hidden_phone(560, 420, 12, 0.4)}
<rect x="520" y="370" width="80" height="100" rx="6" fill="none" stroke="#2a2a32" stroke-width="6"/>
{hidden_phone(830, 660, 80, 0.8)}
{bars_front}
<rect x="60" y="200" width="880" height="16" fill="#c9c9d2"/>
<rect x="60" y="744" width="880" height="16" fill="#c9c9d2"/>
{pop(500, 110, '<circle r="66" class="fa2"/><text y="38" font-size="110" font-weight="700" text-anchor="middle" style="fill:#0a0a0a">?</text>', 0.8)}
""")

# 5. You don't. You just shout louder than the cell tower.
save(SLUG, "answer", f"""
{waves(190, 240, "sa2", 3, 20, 170, 2.2, 4, 0.45)}
{place(190, 780, 1.0, tower())}
{waves(729, 520, "sa", 4, 50, 560, 1.4, 22, 0.9, 0.6)}
{place(560, 560, 1.3, jammer())}
{appear(label(190, 875, "Cell tower", 44, "fa2"), 0.3)}
{appear(label(729, 875, "Jammer", 44, "fa"), 0.9)}
""")

# 6. Your phone listens for a tower miles away: a faint whisper
screen6 = (status(296, 2)
           + '<rect x="24" y="100" width="248" height="160" rx="14" fill="#fff" opacity="0.1"/>'
           + "".join(f'<rect x="24" y="{290 + k * 56}" width="{248 - k * 46}" height="30" rx="10" fill="#fff" opacity="0.14"/>' for k in range(4))
           + '<circle cx="148" cy="180" r="34" fill="none" stroke="#fff" stroke-opacity="0.3" stroke-width="8"/>'
           + '<path d="M148 146 a34 34 0 0 1 34 34" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round">'
           + '<animateTransform attributeName="transform" type="rotate" from="0 148 180" to="360 148 180" dur="1.2s" repeatCount="indefinite"/></path>')
save(SLUG, "whisper", f"""
<defs><clipPath id="s6c"><rect x="200" y="380" width="360" height="160"/></clipPath></defs>
{place(150, 760, 0.72, tower())}
{waves(150, 375, "sa2", 2, 10, 100, 2.4, 3, 0.4)}
<g clip-path="url(#s6c)" opacity="0.55">{scrolling_sine(460, 12, 70, "sa2", 1.0, 4)}</g>
{bob(phone(580, 130, 320, 610, screen6), 6, 3)}
{appear(label(500, 880, "A faint whisper from miles away", 46, "fa2"), 0.8)}
""")

# 7. A jammer sits close and blasts noise on the same frequencies
save(SLUG, "noise", f"""
<defs><clipPath id="s7c"><rect x="80" y="660" width="840" height="160" rx="24"/></clipPath></defs>
{waves(500, 250, "sa", 3, 40, 420, 1.6, 10, 0.55)}
{place(279, 300, 1.7, jammer())}
<rect x="80" y="660" width="840" height="160" rx="24" fill="#fff" fill-opacity="0.06" stroke="#fff" stroke-opacity="0.2" stroke-width="3"/>
<g clip-path="url(#s7c)">
  {scrolling_sine(740, 22, 90, "sa2", 1.0, 5)}
  {noise(80, 920, 740, 62, 7, 7, "sa", 0.9, 0.3)}
</g>
{appear(label(500, 900, "Noise on the exact same frequencies", 44), 1.2)}
""")

# 8. The whisper gets buried, the phone shows no service
screen8 = (status(336, 4, (0.6, 0.9, 1.2, 1.5), "")
           + f'<g opacity="0">{fade(1.6, 0.3)}'
           + '<text x="168" y="300" font-size="50" font-weight="700" text-anchor="middle">No Service</text>'
           + f'<g transform="translate(168 400)">{cross(50)}</g></g>'
           + '<rect x="24" y="500" width="288" height="110" rx="20" fill="#fff" opacity="0.08"/>')
fuzz = "".join(noise(x0, x1, y, 26, s, 5, "sa", 0.2 + s * 0.1, 0.25)
               for s, (x0, x1, y) in enumerate(((40, 290, 220), (60, 290, 420), (40, 290, 620), (710, 960, 260), (710, 940, 470), (710, 960, 660))))
save(SLUG, "noservice", f"""
{fuzz}
{shadow(500, 785, 200, 20)}
{phone(320, 90, 360, 680, screen8)}
{badge(500, 890, "SIGNAL BURIED", 1.8)}
""")

# 9. But here's the part most people miss: radio waves don't stop at a prison wall
save(SLUG, "walls", f"""
{waves(253, 410, "sa", 3, 40, 820, 2.6, 12, 0.75, 0.3)}
<rect x="0" y="660" width="1000" height="10" rx="5" fill="#fff" opacity="0.12"/>
{place(20, 380, 0.75, prison("w", jam=True))}
{place(660, 665, 0.8, house())}
{place(870, 665, 0.7, house())}
{pop(660, 400, f'<circle r="42" fill="{RED}"/><text y="26" font-size="70" font-weight="700" text-anchor="middle">!</text>', 1.4)}
{pop(870, 440, f'<circle r="38" fill="{RED}"/><text y="24" font-size="64" font-weight="700" text-anchor="middle">!</text>', 1.8)}
{appear(label(500, 880, "Radio does not stop at the wall", 46), 1.0)}
""")

# 10. In a South Carolina test, a few small jammers blocked 911 calls
screen10 = ('<text x="153" y="80" font-size="28" text-anchor="middle" opacity="0.8">Emergency call</text>'
            '<text x="153" y="230" font-size="130" text-anchor="middle" class="display">911</text>'
            '<text x="153" y="300" font-size="30" text-anchor="middle" opacity="0.7">Calling...'
            '<animate attributeName="opacity" from="0.7" to="0" begin="1.3s" dur="0.2s" fill="freeze"/></text>'
            f'<text x="153" y="300" font-size="36" font-weight="700" text-anchor="middle" style="fill:{RED}" opacity="0">Call failed{fade(1.4, 0.2)}</text>'
            f'<g transform="translate(153 500)"><circle r="54" fill="{RED}"/>'
            '<path d="M-30 4 q30 -26 60 0 l-8 14 l-14 -6 v-8 q-8 -4 -16 0 v8 l-14 6 z" fill="#fff"/></g>')
save(SLUG, "test911", f"""
{waves(703, 470, "sa", 3, 40, 460, 1.5, 12, 0.7, 0.4)}
{shadow(275, 760, 190, 18)}
{phone(110, 110, 330, 640, screen10)}
{place(560, 520, 1.1, jammer())}
{badge(500, 890, "911 CALLS BLOCKED", 1.6)}
""")

# 11. Affected cell networks up to two and a half miles away
rnd = random.Random(3)
homes = []
for i in range(26):
    a = rnd.uniform(0, 2 * math.pi)
    d = rnd.uniform(170, 300)
    hx, hy = 500 + d * math.cos(a), 450 + d * math.sin(a)
    homes.append(f'<g transform="translate({hx:.0f} {hy:.0f}) rotate({rnd.choice((0, 90))})">'
                 f'<rect x="-17" y="-13" width="34" height="26" rx="3" fill="#a1473a"/>'
                 f'<line x1="-17" y1="0" x2="17" y2="0" stroke="#000" stroke-opacity="0.35" stroke-width="3"/></g>')
roads = "".join(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#fff" stroke-opacity="0.1" stroke-width="20" stroke-linecap="round"/>'
                for x1, y1, x2, y2 in ((90, 450, 910, 450), (500, 120, 500, 780), (180, 160, 820, 740), (820, 170, 200, 760)))
towers11 = "".join(
    place(500 + 320 * math.cos(a) - 0, 450 + 320 * math.sin(a) + 40, 0.18, tower())
    + f'<g opacity="0">{fade(1.8 + k * 0.2, 0.2)}<circle cx="{500 + 320 * math.cos(a):.0f}" cy="{450 + 320 * math.sin(a) - 20:.0f}" r="56" fill="none" stroke="{RED}" stroke-width="8">'
      f'<animate attributeName="opacity" values="1;0.3;1" dur="0.6s" repeatCount="indefinite"/></circle></g>'
    for k, a in enumerate((-2.4, -0.5, 1.1, 2.6)))
save(SLUG, "range", f"""
<defs><clipPath id="s11c"><circle cx="500" cy="450" r="350"/></clipPath></defs>
<circle cx="500" cy="450" r="350" fill="#1f2a22"/>
<g clip-path="url(#s11c)">{roads}{''.join(homes)}</g>
<circle cx="500" cy="450" r="350" fill="none" stroke="#fff" stroke-opacity="0.2" stroke-width="4"/>
<circle cx="500" cy="450" r="30" class="fa" opacity="0.15"><animate attributeName="r" from="30" to="330" begin="0.4s" dur="1.6s" fill="freeze"/></circle>
<circle cx="500" cy="450" r="30" class="nf sa" stroke-width="8" stroke-dasharray="22 14"><animate attributeName="r" from="30" to="330" begin="0.4s" dur="1.6s" fill="freeze"/></circle>
{waves(500, 450, "sa", 3, 30, 330, 1.6, 6, 0.6, 2.0)}
{place(500, 450, 0.42, prison_top("r"))}
{towers11}
{appear('<text x="500" y="930" font-size="130" text-anchor="middle" class="display fa">2.5 MILES</text>', 1.6)}
""")

# 12. Jamming is only allowed inside an approved zone where phones are already banned
save(SLUG, "zone", f"""
<defs><clipPath id="s12c"><rect x="265" y="195" width="470" height="470" rx="20"/></clipPath></defs>
<rect x="265" y="195" width="470" height="470" rx="20" class="fa" opacity="0.08"/>
<g clip-path="url(#s12c)">{waves(500, 430, "sa", 3, 30, 340, 1.6, 12, 0.85)}</g>
{place(500, 430, 1.25, prison_top("z"))}
<rect x="265" y="195" width="470" height="470" rx="20" class="nf sa" stroke-width="8" stroke-dasharray="26 16">
  <animate attributeName="stroke-dashoffset" from="0" to="-84" dur="1.2s" repeatCount="indefinite"/></rect>
{place(130, 640, 0.6, house())}
{place(870, 640, 0.6, house())}
{pop(130, 430, check(0), 1.4)}
{pop(870, 430, check(0), 1.6)}
{appear(label(500, 790, "Approved jamming zone", 44, "fa"), 0.6)}
""")

# 13. Prisons must test it twice and warn their neighbours
screen13 = (status(176, 4) + '<text x="88" y="160" font-size="30" font-weight="700" text-anchor="middle">Signal OK</text>'
            + "".join(f'<rect x="24" y="{200 + k * 40}" width="{128 - k * 30}" height="20" rx="7" fill="#fff" opacity="0.15"/>' for k in range(2)))
letter = ('<rect x="-48" y="-32" width="96" height="64" rx="6" fill="url(#paper)"/>'
          '<path d="M-48 -32 L0 6 L48 -32" fill="none" stroke="#b9b5aa" stroke-width="4"/>')
save(SLUG, "rules", f"""
{place(500, 380, 0.8, prison("t", jam=True))}
{place(220, 684, 1.1, house())}
{bob(phone(90, 70, 200, 330, screen13), 6, 2.6)}
<g opacity="0">{fade(0.5, 0.2)}<g><animateTransform attributeName="transform" type="translate" values="640 520;420 380;250 560" keyTimes="0;0.5;1" begin="0.5s" dur="1.2s" fill="freeze"/>{letter}</g></g>
{pop(400, 170, check(0, 46), 1.5)}
{pop(400, 290, check(0, 46), 1.9)}
{badge(500, 890, "TESTED TWICE", 2.2)}
""")

# 14. So a jammer doesn't break a phone. It just shouts over the tower.
screen14 = (status(196, 4, (0.8, 1.0, 1.2, 1.4), "")
            + f'<text x="98" y="210" font-size="30" font-weight="700" text-anchor="middle" opacity="0">No Service{fade(1.5, 0.2)}</text>'
            + '<rect x="20" y="250" width="156" height="110" rx="14" fill="#fff" opacity="0.1"/>')
save(SLUG, "payoff", f"""
{waves(160, 220, "sa2", 3, 20, 220, 2.2, 4, 0.4)}
{place(160, 760, 0.95, tower())}
{waves(790, 540, "sa", 4, 50, 600, 1.4, 20, 0.85, 0.4)}
{shadow(490, 680, 130, 16)}
{phone(380, 250, 220, 420, screen14)}
{place(660, 580, 1.0, jammer())}
{badge(500, 890, "LOUDER, NOT BROKEN", 1.8)}
""")
