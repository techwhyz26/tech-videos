"""Illustrations for the 'smoke-alarm-radioactive' video. Run:  python tools/art_smoke_alarm_radioactive.py

Objects (smoke alarm seen from the side and from below, the americium button, the ion chamber
cut-away, a 9V battery, a current gauge, a toaster, the light chamber of a photoelectric alarm,
a bed) are drawn once in their own coordinates and placed with translate+rotate+scale.
"""
import math

from artlib import appear, badge, fade, label, pop, save, shadow, waves

SLUG = "smoke-alarm-radioactive"
RED = "#ff3b3b"
GREEN = "#3ddc84"
GOLD = "#ffb02e"
AIR = "#7fb8ff"
SMOKE = "#77707a"
WOOD, WOOD_DARK = "#7a5136", "#553623"
SKIN = "#f2c6a0"


def place(x: float, y: float, s: float, inner: str, rot: float = 0) -> str:
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">{inner}</g>'


def led(cx: float, cy: float, r: float, colour: str, dur: float = 2.0) -> str:
    return (f'<circle cx="{cx}" cy="{cy}" r="{r * 2.6}" fill="{colour}" opacity="0" filter="url(#soft)">'
            f'<animate attributeName="opacity" values="0;0.9;0" dur="{dur}s" repeatCount="indefinite"/></circle>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{colour}" opacity="0.35">'
            f'<animate attributeName="opacity" values="0.35;1;0.35" dur="{dur}s" repeatCount="indefinite"/></circle>')


def ceiling() -> str:
    return ('<rect x="30" y="20" width="940" height="70" rx="18" fill="#2c2328"/>'
            '<rect x="30" y="80" width="940" height="10" rx="5" fill="#fff" opacity="0.10"/>')


# ---------------------------------------------------------------------------------------------
# Smoke alarm, side view. (0,0) = centre of the ceiling plate; 450 wide, about 170 tall.
def alarm_side(led_c: str = GREEN, led_dur: float = 2.0, speck: bool = False) -> str:
    vents = "".join(f'<rect x="{x - 7}" y="62" width="14" height="46" rx="7" fill="#3a3640" opacity="0.55"/>'
                    for x in range(-180, 181, 30))
    sp = ""
    if speck:
        sp = (f'<circle cx="0" cy="92" r="42" class="fa2" opacity="0.3" filter="url(#soft)">'
              f'<animate attributeName="opacity" values="0.2;0.9;0.2" dur="1.2s" repeatCount="indefinite"/></circle>'
              f'<circle cx="0" cy="92" r="13" fill="{GOLD}" stroke="#fff" stroke-width="3"/>')
    return f"""
<rect x="-200" y="-4" width="400" height="36" rx="10" fill="url(#steel)"/>
<path d="M-225 30 H225 Q222 118 165 152 H-165 Q-222 118 -225 30 Z" fill="url(#paper)"/>
<path d="M-225 30 H225 Q224 48 221 58 H-221 Q-224 48 -225 30 Z" fill="#000" opacity="0.08"/>
{vents}
<rect x="-200" y="38" width="400" height="7" rx="4" fill="#fff" opacity="0.7"/>
<ellipse cx="0" cy="152" rx="165" ry="16" fill="#e2ddd2"/>
<ellipse cx="0" cy="157" rx="62" ry="12" fill="url(#steel)" stroke="#9a96a0" stroke-width="2"/>
{led(122, 140, 8, led_c, led_dur)}{sp}"""


# Smoke alarm seen from below. (0,0) = centre, radius r. `inner` shows a cut-away of the middle.
def alarm_face(uid: str, r: float, inner: str = "", led_c: str = GREEN, led_dur: float = 2.0) -> str:
    slots = "".join(
        f'<rect x="{-r * 0.025:.1f}" y="{-r * 0.86:.1f}" width="{r * 0.05:.1f}" height="{r * 0.22:.1f}" rx="{r * 0.025:.1f}" '
        f'fill="#3a3640" opacity="0.5" transform="rotate({a})"/>'
        for a in range(0, 360, 12) if a not in (0, 12, 348))
    if inner:
        mid = (f'<clipPath id="{uid}cut"><circle r="{r * 0.5:.0f}"/></clipPath>'
               f'<circle r="{r * 0.5:.0f}" fill="#0b0b10"/><g clip-path="url(#{uid}cut)">{inner}</g>'
               f'<circle r="{r * 0.5:.0f}" class="nf" stroke="#c9c5bc" stroke-width="{r * 0.03:.0f}"/>')
    else:
        mid = (f'<circle r="{r * 0.22:.0f}" fill="url(#steel)" stroke="#a09ca6" stroke-width="3"/>'
               f'<text y="{r * 0.03:.0f}" font-size="{r * 0.08:.0f}" text-anchor="middle" font-weight="700" style="fill:#6a6670">TEST</text>')
    return f"""<circle cx="14" cy="22" r="{r}" fill="#000" opacity="0.5" filter="url(#soft)"/>
<circle r="{r}" fill="url(#paper)" stroke="#fff" stroke-opacity="0.4" stroke-width="4"/>
<circle r="{r * 0.95:.0f}" class="nf" stroke="#000" stroke-opacity="0.07" stroke-width="{r * 0.04:.0f}"/>
{slots}
<circle r="{r * 0.56:.0f}" fill="#f3f0e8" stroke="#cfcac0" stroke-width="4"/>
{mid}
{led(0, -r * 0.75, r * 0.035, led_c, led_dur)}
<path d="M{-r * 0.8:.0f} {-r * 0.35:.0f} A{r * 0.87:.0f} {r * 0.87:.0f} 0 0 1 {-r * 0.35:.0f} {-r * 0.8:.0f}" class="nf" stroke="#fff" stroke-width="{r * 0.04:.0f}" stroke-linecap="round" opacity="0.7"/>"""


# ---------------------------------------------------------------------------------------------
# The americium button: a steel disc with a gold foil centre, (0,0) = centre of the top face.
def button(rx: float) -> str:
    ry, t = rx * 0.36, rx * 0.13
    return (f'<ellipse cx="0" cy="{t:.0f}" rx="{rx}" ry="{ry:.0f}" fill="#5d5d68"/>'
            f'<rect x="{-rx}" y="0" width="{2 * rx}" height="{t:.0f}" fill="#5d5d68"/>'
            f'<ellipse cx="0" cy="0" rx="{rx}" ry="{ry:.0f}" fill="url(#steel)"/>'
            f'<ellipse cx="0" cy="0" rx="{rx * 0.8:.0f}" ry="{ry * 0.8:.0f}" class="nf" stroke="#9a9aa6" stroke-width="{rx * 0.02:.1f}"/>'
            f'<ellipse cx="0" cy="0" rx="{rx * 0.6:.0f}" ry="{ry * 0.6:.0f}" class="fa2" opacity="0.3" filter="url(#soft)">'
            f'<animate attributeName="opacity" values="0.2;0.7;0.2" dur="1.3s" repeatCount="indefinite"/></ellipse>'
            f'<ellipse cx="0" cy="0" rx="{rx * 0.38:.0f}" ry="{ry * 0.38:.0f}" fill="{GOLD}"/>'
            f'<ellipse cx="{-rx * 0.08:.0f}" cy="{-ry * 0.1:.0f}" rx="{rx * 0.22:.0f}" ry="{ry * 0.16:.0f}" fill="#ffe7a8" opacity="0.8"/>')


def sparks(length: float, size: float, n: int = 7, spread=(-160, -20), dur: float = 1.1) -> str:
    """Alpha particles shooting out of the foil at (0,0)."""
    out = []
    for k in range(n):
        a = math.radians(spread[0] + (spread[1] - spread[0]) * k / (n - 1))
        dx, dy = math.cos(a) * length, math.sin(a) * length
        b = (k * 0.37) % dur
        out.append(f'<g opacity="0"><animate attributeName="opacity" values="0;1;0" dur="{dur}s" begin="{b:.2f}s" repeatCount="indefinite"/>'
                   f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{dx:.0f} {dy:.0f}" dur="{dur}s" begin="{b:.2f}s" repeatCount="indefinite"/>'
                   f'<circle r="{size}" class="fa2" filter="url(#glow)"/></g>')
    return "".join(out)


# ---------------------------------------------------------------------------------------------
def ion(sign: str, s: float = 1) -> str:
    if sign == "+":
        return (f'<circle r="{17 * s}" class="fa"/><text y="{11 * s:.0f}" font-size="{34 * s:.0f}" font-weight="700" '
                f'text-anchor="middle" style="fill:#fff">+</text>')
    return (f'<circle r="{11 * s}" class="fa2"/><text y="{8 * s:.0f}" font-size="{26 * s:.0f}" font-weight="700" '
            f'text-anchor="middle" style="fill:#111">−</text>')


def drift(inner: str, x: float, y0: float, y1: float, dur: float, begin: float) -> str:
    return (f'<g opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.88;1" dur="{dur}s" begin="{begin:.2f}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" from="{x} {y0}" to="{x} {y1}" dur="{dur}s" begin="{begin:.2f}s" repeatCount="indefinite"/>'
            f'{inner}</g>')


def puff(r: float, colour: str = SMOKE) -> str:
    blobs = ((0, 0, 1), (0.75, -0.3, 0.65), (-0.7, 0.25, 0.6), (0.2, 0.6, 0.55), (-0.2, -0.55, 0.5))
    return ("".join(f'<circle cx="{a * r:.0f}" cy="{b * r:.0f}" r="{c * r:.0f}" fill="{colour}"/>' for a, b, c in blobs)
            + f'<circle cx="{-0.3 * r:.0f}" cy="{-0.35 * r:.0f}" r="{0.25 * r:.0f}" fill="#fff" opacity="0.18"/>')


# The ion chamber cut open: a metal can 600x520, two plates, the button on the bottom plate.
# Gap between plates: x 80-520, y 96-424.
def chamber(uid: str, mode: str = "ions") -> str:
    out = [shadow(300, 540, 320, 22),
           '<rect x="0" y="0" width="600" height="520" rx="34" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>',
           '<rect x="14" y="8" width="572" height="10" rx="5" fill="#fff" opacity="0.12"/>',
           '<rect x="30" y="30" width="540" height="460" rx="16" fill="#0b0b10"/>']
    for vy in (130, 250, 370):
        out.append(f'<rect x="-3" y="{vy}" width="40" height="44" fill="#0b0b10"/><rect x="563" y="{vy}" width="40" height="44" fill="#0b0b10"/>')
    body = []
    if mode == "glow":
        body.append('<rect x="80" y="96" width="440" height="328" class="fa" opacity="0.1">'
                    '<animate attributeName="opacity" values="0.06;0.3;0.06" dur="1.4s" repeatCount="indefinite"/></rect>')
        for i, x in enumerate(range(120, 500, 60)):
            body.append(f'<line x1="{x}" y1="104" x2="{x}" y2="416" class="sa" stroke-width="6" stroke-linecap="round" '
                        f'stroke-dasharray="18 26" opacity="0">{fade(0.5 + i * 0.1)}'
                        f'<animate attributeName="stroke-dashoffset" from="0" to="-44" dur="0.5s" repeatCount="indefinite"/></line>')
        body.append(f'<g transform="translate(300 418)">{sparks(240, 9, 9, (-150, -30), 1.0)}</g>')
    elif mode in ("ions", "smoke"):
        free = []
        for i, x in enumerate(range(120, 500, 54)):
            free.append(drift(ion("+"), x, 112, 404, 2.2, (i * 0.31) % 2.2))
            free.append(drift(ion("-"), x + 27, 404, 112, 1.6, (i * 0.23) % 1.6))
        if mode == "ions":
            body += free
        else:
            body.append(f'<g>{"".join(free)}<animate attributeName="opacity" from="1" to="0" begin="1.3s" dur="0.5s" fill="freeze"/></g>')
            spots = [(170, 190, 70), (380, 170, 62), (260, 330, 78), (440, 330, 60)]
            for k, (bx, by, r) in enumerate(spots):
                b = 0.2 + k * 0.22
                stuck = "".join(pop(math.cos(a) * r * 0.95, math.sin(a) * r * 0.95, ion(sg, 0.85), 1.4 + k * 0.15 + j * 0.12)
                                for j, (a, sg) in enumerate(((-0.6, "+"), (2.0, "-"), (3.6, "+"), (5.0, "-"))))
                body.append(f'<g transform="translate({bx} {by})"><g>'
                            f'<animateTransform attributeName="transform" type="translate" from="-520 30" to="0 0" begin="{b}s" dur="1.1s" fill="freeze"/>'
                            f'{puff(r)}{stuck}</g></g>')
    out.append(f'<clipPath id="{uid}cav"><rect x="0" y="30" width="570" height="460"/></clipPath>'
               f'<g clip-path="url(#{uid}cav)">{"".join(body)}</g>')
    out.append('<rect x="80" y="70" width="440" height="26" rx="6" fill="url(#steel)"/>'
               '<rect x="80" y="424" width="440" height="26" rx="6" fill="url(#steel)"/>'
               '<text x="55" y="96" font-size="44" font-weight="700" text-anchor="middle" class="fa">+</text>'
               '<text x="55" y="452" font-size="44" font-weight="700" text-anchor="middle" class="fa2">−</text>')
    out.append(place(300, 418, 1, button(70)))
    return "".join(out)


def battery() -> str:
    """A 9V battery, body 120x200 at (0,0), terminals on top."""
    return (f'{shadow(60, 210, 80, 14)}'
            '<circle cx="34" cy="-8" r="15" fill="url(#steel)"/>'
            '<rect x="70" y="-20" width="32" height="24" rx="4" fill="url(#steel)"/>'
            '<rect x="0" y="0" width="120" height="200" rx="14" fill="#1d1d22" stroke="#fff" stroke-opacity="0.25" stroke-width="3"/>'
            '<rect x="0" y="0" width="120" height="70" rx="14" class="fa2"/><rect x="0" y="50" width="120" height="20" class="fa2"/>'
            '<rect x="8" y="8" width="14" height="184" rx="7" fill="#fff" opacity="0.14"/>'
            '<text x="60" y="152" font-size="60" text-anchor="middle" class="display fw">9V</text>')


def gauge(a0: float, a1: float, begin: float, red_zone: bool = False) -> str:
    """A needle meter, body 280x190 at (0,0); needle turns from angle a0 to a1 (0 = straight up)."""
    ticks = "".join(f'<line x1="140" y1="56" x2="140" y2="72" stroke="#333" stroke-width="5" transform="rotate({a} 140 150)"/>'
                    for a in range(-80, 81, 20))
    zone = ""
    if red_zone:
        zone = f'<path d="M{140 - 88 * math.cos(math.radians(10)):.0f} {150 - 88 * math.sin(math.radians(10)):.0f} A88 88 0 0 1 {140 - 88 * math.cos(math.radians(45)):.0f} {150 - 88 * math.sin(math.radians(45)):.0f}" class="nf" stroke="{RED}" stroke-width="14"/>'
    return f"""{shadow(140, 200, 150, 14)}
<rect x="0" y="0" width="280" height="190" rx="26" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>
<path d="M30 150 A110 110 0 0 1 250 150 Z" fill="url(#paper)"/>
{zone}{ticks}
<g transform="rotate({a0} 140 150)">
  <animateTransform attributeName="transform" type="rotate" from="{a0} 140 150" to="{a1} 140 150" begin="{begin}s" dur="0.6s" fill="freeze"/>
  <g><animateTransform attributeName="transform" type="rotate" values="-3 140 150;3 140 150;-3 140 150" dur="0.5s" repeatCount="indefinite"/>
  <line x1="140" y1="150" x2="140" y2="58" stroke="{RED}" stroke-width="7" stroke-linecap="round"/></g>
</g>
<circle cx="140" cy="150" r="14" fill="#222"/>
<rect x="30" y="150" width="220" height="10" fill="#000" opacity="0.2"/>"""


def wire(d: str, begin: float = 0.3) -> str:
    return (f'<path d="{d}" class="nf" stroke="#c9c9d2" stroke-width="9" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<path d="{d}" class="nf sa2" stroke-width="9" stroke-linecap="round" stroke-dasharray="14 30" opacity="0">{fade(begin)}'
            f'<animate attributeName="stroke-dashoffset" from="0" to="-44" dur="0.6s" repeatCount="indefinite"/></path>')


def toaster() -> str:
    """A toaster, body 380x240 at (0,0); slots on top at y=0."""
    return f"""{shadow(190, 250, 220, 18)}
<rect x="30" y="236" width="50" height="16" rx="5" fill="#222"/><rect x="300" y="236" width="50" height="16" rx="5" fill="#222"/>
<rect x="0" y="0" width="380" height="244" rx="70" fill="url(#steel)" stroke="#fff" stroke-opacity="0.5" stroke-width="3"/>
<rect x="30" y="20" width="18" height="190" rx="9" fill="#fff" opacity="0.6"/>
<rect x="70" y="-6" width="240" height="22" rx="11" fill="#2a2a30"/>
<rect x="70" y="30" width="240" height="22" rx="11" fill="#2a2a30" opacity="0"/>
<rect x="380" y="70" width="28" height="60" rx="8" fill="#55555f"/>
<circle cx="300" cy="170" r="24" fill="#55555f"/><line x1="300" y1="170" x2="300" y2="150" stroke="#ddd" stroke-width="5" stroke-linecap="round"/>"""


def toast_slice(x: float) -> str:
    return (f'<path d="M{x} 30 V-110 q0 -40 40 -40 q20 -26 50 -16 q40 0 40 40 V30 Z" fill="#2a170d"/>'
            f'<path d="M{x + 12} 30 V-104 q0 -30 30 -30 q16 -20 40 -12 q30 0 30 30 V30 Z" fill="#4a2a17"/>'
            f'<circle cx="{x + 55}" cy="-80" r="16" fill="#140a05"/><circle cx="{x + 95}" cy="-40" r="12" fill="#140a05"/>')


# The light chamber of a photoelectric alarm, seen from above. (0,0) = centre, radius 300.
def photo_chamber(scatter: bool = False) -> str:
    vanes = "".join(f'<path d="M-16 -292 L16 -292 L30 -244 L-2 -236 Z" fill="#34343e" transform="rotate({a})"/>'
                    for a in range(0, 360, 22))
    beam = ('<rect x="-200" y="-16" width="440" height="32" class="fa2" opacity="0.25" filter="url(#glow)">'
            '<animate attributeName="opacity" values="0.18;0.4;0.18" dur="1.2s" repeatCount="indefinite"/></rect>'
            '<line x1="-200" y1="0" x2="240" y2="0" class="sa2" stroke-width="6" stroke-dasharray="26 18">'
            '<animate attributeName="stroke-dashoffset" from="0" to="-44" dur="0.4s" repeatCount="indefinite"/></line>')
    extra = ""
    if scatter:
        puffs = "".join(
            f'<g transform="translate({px} {py})"><g opacity="0">{fade(0.3 + k * 0.25, 0.4)}'
            f'<animateTransform attributeName="transform" type="translate" from="0 -220" to="0 0" begin="{0.3 + k * 0.25}s" dur="1.1s" fill="freeze"/>'
            f'{puff(r)}</g></g>'
            for k, (px, py, r) in enumerate(((-60, -6, 34), (40, 4, 40), (130, -8, 30))))
        rays = "".join(
            f'<line x1="{px}" y1="0" x2="{ex}" y2="{ey}" class="sa2" stroke-width="6" stroke-dasharray="14 14" opacity="0">{fade(1.5 + k * 0.1)}'
            f'<animate attributeName="stroke-dashoffset" from="0" to="-28" dur="0.4s" repeatCount="indefinite"/></line>'
            for k, (px, ex, ey) in enumerate(((-60, -14, 180), (40, 0, 180), (130, 14, 180), (40, 120, -150), (-60, -150, -130))))
        hit = (f'<circle cx="0" cy="205" r="70" class="fa" opacity="0" filter="url(#soft)">'
               f'<animate attributeName="opacity" values="0;1;0.5;1" begin="1.7s" dur="0.8s" fill="freeze"/></circle>')
        extra = rays + puffs + hit
    return f"""<circle r="300" fill="#121216" stroke="#2a2a33" stroke-width="10"/>
{vanes}
<circle r="236" class="nf" stroke="#000" stroke-opacity="0.5" stroke-width="6"/>
{beam}
<path d="M226 -44 L262 -24 L262 24 L226 44 Z" fill="#050507"/>
<rect x="-110" y="70" width="70" height="40" rx="8" fill="#26262e"/>
{extra}
<rect x="-262" y="-28" width="40" height="56" rx="8" fill="#3a3a44"/>
<path d="M-222 -22 h20 a22 22 0 0 1 0 44 h-20 z" fill="#fff" opacity="0.9"/>
<circle cx="-205" cy="0" r="30" class="fa2" opacity="0.6" filter="url(#soft)"/>
<rect x="-36" y="190" width="72" height="56" rx="8" fill="#26262e" stroke="#4a4a56" stroke-width="3"/>
<ellipse cx="0" cy="192" rx="30" ry="12" fill="#5a6a8a"/>
<ellipse cx="-8" cy="189" rx="12" ry="4" fill="#fff" opacity="0.5"/>"""


# ================================================================================================
# 1. A tiny speck of radioactive metal on your ceiling ----------------------------------------------
lens_in = (f'<circle cx="500" cy="560" r="200" fill="#0b0b10"/>'
           f'{place(500, 610, 1, button(120))}'
           f'<g transform="translate(500 610)">{sparks(170, 9, 8)}</g>'
           f'{waves(500, 610, "sa2", 3, 30, 190, 1.6, 5, 0.6)}')
save(SLUG, "ceiling", f"""
{ceiling()}
{place(500, 90, 1.2, alarm_side(speck=True))}
<g opacity="0">{fade(0.5)}
  <path d="M488 210 L330 410 M512 210 L670 410" class="nf sw" stroke-width="4" stroke-dasharray="10 10" opacity="0.6"/>
  <clipPath id="s1lens"><circle cx="500" cy="560" r="200"/></clipPath>
  <g clip-path="url(#s1lens)">{lens_in}</g>
  <line x1="640" y1="705" x2="745" y2="805" stroke="#2a2a30" stroke-width="44" stroke-linecap="round"/>
  <line x1="640" y1="705" x2="745" y2="805" stroke="url(#metal)" stroke-width="36" stroke-linecap="round"/>
  <circle cx="500" cy="560" r="200" class="nf" stroke="url(#steel)" stroke-width="24"/>
  <path d="M370 470 A160 160 0 0 1 450 410" class="nf sw" stroke-width="10" stroke-linecap="round" opacity="0.35"/>
</g>
{badge(500, 900, "RADIOACTIVE", 1.4)}
""")

# 2. So why would a smoke alarm need something radioactive? ------------------------------------------
save(SLUG, "why", f"""
<g><animateTransform attributeName="transform" type="rotate" values="-3 430 450;3 430 450;-3 430 450" dur="4s" repeatCount="indefinite"/>
{place(430, 450, 1, alarm_face("s2", 330))}</g>
{pop(840, 250, '<circle r="88" class="fa"/><text y="56" font-size="170" font-weight="700" text-anchor="middle" style="fill:#0a0a0a">?</text>', 0.6)}
{pop(870, 560, f'<circle r="62" fill="{GOLD}"/><circle r="14" fill="#1a1a1a"/>' + "".join(f'<path d="M0 0 L{50 * math.cos(math.radians(a - 30)):.0f} {50 * math.sin(math.radians(a - 30)):.0f} A50 50 0 0 1 {50 * math.cos(math.radians(a + 30)):.0f} {50 * math.sin(math.radians(a + 30)):.0f} Z" fill="#1a1a1a" transform="scale(0.95)"/>' for a in (-90, 30, 150)) + f'<circle r="20" fill="{GOLD}"/><circle r="12" fill="#1a1a1a"/>', 1.1)}
""")

# 3. That speck makes the air inside carry electricity ----------------------------------------------
save(SLUG, "conduct", f"""
{place(200, 110, 1, chamber("s3", "glow"))}
{appear(label(500, 880, "The air inside carries electricity", 48), 1.0)}
""")

# 4. Americium: about a third of a millionth of a gram ------------------------------------------------
save(SLUG, "speck", f"""
{shadow(500, 590, 330, 26)}
{place(500, 420, 1, button(300))}
<g transform="translate(500 420)">{sparks(230, 12, 9, (-165, -15), 1.3)}</g>
{appear('<text x="500" y="160" font-size="88" text-anchor="middle" class="display fa2">AMERICIUM</text>', 0.4)}
{appear('<text x="500" y="800" font-size="130" text-anchor="middle" class="display fw">0.0000003 g</text>', 1.2)}
""")

# 5. Tiny particles knock electrons off the air molecules -------------------------------------------
def molecule(s: float = 1) -> str:
    return (f'<circle cx="{-24 * s}" cy="0" r="{34 * s}" fill="{AIR}"/><circle cx="{24 * s}" cy="0" r="{34 * s}" fill="{AIR}"/>'
            f'<circle cx="{-34 * s}" cy="{-12 * s}" r="{10 * s}" fill="#fff" opacity="0.5"/><circle cx="{14 * s}" cy="{-12 * s}" r="{10 * s}" fill="#fff" opacity="0.5"/>')


SRC = (190, 690)
hits = [(430, 250, 0.0, (110, -90)), (650, 430, 0.5, (130, 40)), (820, 230, 1.0, (60, -120)),
        (500, 560, 1.5, (-30, 130)), (800, 640, 0.25, (110, 90))]
CYC, F = 2.4, 0.22
parts = []
for mx, my, b, (ex, ey) in hits:
    dx, dy = mx - SRC[0], my - SRC[1]
    sx, sy = SRC[0] + dx * 0.06, SRC[1] + dy * 0.06 - 10
    parts.append(
        f'<g transform="translate({mx} {my})">{molecule()}'
        f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{F};{F + 0.02};1" dur="{CYC}s" begin="{b}s" repeatCount="indefinite"/>'
        f'<circle r="78" class="nf sa" stroke-width="7"/><g transform="translate(0 -62)">{ion("+", 1.1)}</g></g>'
        f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{F};{F + 0.02};0.85;1" dur="{CYC}s" begin="{b}s" repeatCount="indefinite"/>'
        f'<animateTransform attributeName="transform" type="translate" values="0 0;0 0;{ex} {ey}" keyTimes="0;{F};1" dur="{CYC}s" begin="{b}s" repeatCount="indefinite"/>'
        f'{ion("-", 1.4)}</g></g>'
        f'<g opacity="0"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;{F};{F + 0.01};1" dur="{CYC}s" begin="{b}s" repeatCount="indefinite"/>'
        f'<animateTransform attributeName="transform" type="translate" values="{sx:.0f} {sy:.0f};{mx} {my};{mx} {my}" keyTimes="0;{F};1" dur="{CYC}s" begin="{b}s" repeatCount="indefinite"/>'
        f'<circle r="12" class="fa2" filter="url(#glow)"/></g>'
        f'<circle cx="{mx}" cy="{my}" r="40" class="fa2" opacity="0" filter="url(#soft)">'
        f'<animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;{F};{F + 0.03};{F + 0.15};1" dur="{CYC}s" begin="{b}s" repeatCount="indefinite"/></circle>')
calm = "".join(f'<g transform="translate({x} {y})"><g><animateTransform attributeName="transform" type="translate" values="0 0;0 -10;0 0" dur="{2.4 + i * 0.3}s" repeatCount="indefinite"/>{molecule(0.8)}</g></g>'
               for i, (x, y) in enumerate(((300, 420), (620, 130), (920, 450), (360, 140))))
save(SLUG, "ionize", f"""
{shadow(SRC[0], SRC[1] + 70, 130, 18)}
{place(SRC[0], SRC[1], 1, button(110))}
{calm}
{"".join(parts)}
{appear(label(500, 885, "Electrons knocked loose", 48), 0.8)}
""")

# 6. A battery pulls the charged bits to two plates: a tiny current flows ------------------------------
save(SLUG, "plates", f"""
{wire("M456 216 H675 V160", 0.6)}
{wire("M705 370 V470", 0.6)}
{wire("M600 600 H560 V500 H456", 0.6)}
{place(40, 150, 0.8, chamber("s6", "ions"))}
{place(645, 170, 1, battery())}
{place(600, 470, 1.15, gauge(-70, 40, 0.8))}
{appear(label(500, 880, "A tiny, steady current", 48), 1.2)}
""")

# 7. The alarm never looks for smoke; it watches that current ------------------------------------------
can_slots = "".join(f'<rect x="-8" y="-104" width="16" height="34" rx="8" fill="#3a3a44" transform="rotate({a})"/>' for a in range(0, 360, 30))
can = (f'<circle r="112" fill="url(#steel)" stroke="#8a8a96" stroke-width="4"/>{can_slots}'
       f'<circle r="52" fill="#2a2a33"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#55556a"/>' for x in range(-36, 37, 18) for y in range(-36, 37, 18) if x * x + y * y < 1600)
       + f'<circle r="12" fill="{GOLD}" opacity="0.5"><animate attributeName="opacity" values="0.3;1;0.3" dur="1.2s" repeatCount="indefinite"/></circle>')
legs = "".join(f'<rect x="{578 + i * 24}" y="268" width="10" height="18" fill="#c9c9d2"/><rect x="{578 + i * 24}" y="404" width="10" height="18" fill="#c9c9d2"/>' for i in range(7))
pulses = "".join(f'<circle r="11" class="fa2" filter="url(#glow)" opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.9;1" dur="1.2s" begin="{0.6 + k * 0.4}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="cx" from="462" to="560" dur="1.2s" begin="{0.6 + k * 0.4}s" repeatCount="indefinite"/><animate attributeName="cy" from="345" to="345" dur="1.2s" begin="{0.6 + k * 0.4}s" repeatCount="indefinite"/></circle>' for k in range(3))
traces = "".join(f'<path d="{d}" class="nf" stroke="#d4b25a" stroke-width="6" opacity="0.7"/>' for d in (
    "M230 250 H320 V230", "M760 450 V500", "M450 560 H560", "M230 640 H300 V600", "M740 250 H780 V320"))
save(SLUG, "watching", f"""
<circle cx="514" cy="452" r="380" fill="#000" opacity="0.5" filter="url(#soft)"/>
<circle cx="500" cy="440" r="380" fill="url(#paper)"/>
<circle cx="500" cy="440" r="356" class="nf" stroke="#cfcac0" stroke-width="6"/>
<rect x="190" y="200" width="620" height="490" rx="30" fill="#1d6b47"/>
<rect x="190" y="450" width="620" height="240" rx="30" fill="#000" opacity="0.12"/>
{traces}
<path d="M462 345 H560" class="nf" stroke="#d4b25a" stroke-width="10"/>
{place(350, 345, 1, can)}
{legs}
<rect x="560" y="284" width="190" height="122" rx="10" fill="#141418"/>
<circle cx="582" cy="304" r="7" fill="#444"/>
<rect x="560" y="284" width="190" height="122" rx="10" class="nf sa2" stroke-width="6" opacity="0">
  <animate attributeName="opacity" values="0;1;0.3;1" begin="1.0s" dur="1s" repeatCount="indefinite"/></rect>
{pulses}
<circle cx="360" cy="580" r="86" fill="#c9a24a"/><circle cx="360" cy="580" r="62" fill="#f1efe8"/><circle cx="360" cy="580" r="20" fill="#c9a24a"/>
{place(610, 500, 0.8, battery())}
{led(700, 230, 10, RED, 1.4)}
{badge(500, 900, "IT WATCHES THE CURRENT", 1.6)}
""")

# 8. Smoke drifts in, its particles grab the charged bits ------------------------------------------
wisps = "".join(
    f'<g opacity="0"><animate attributeName="opacity" values="0;0.8;0" begin="{k * 0.5}s" dur="2s" repeatCount="indefinite"/>'
    f'<animateTransform attributeName="transform" type="translate" from="20 {y}" to="190 {y - 20}" begin="{k * 0.5}s" dur="2s" repeatCount="indefinite"/>'
    f'{puff(34)}</g>' for k, y in enumerate((260, 380, 500, 320)))
save(SLUG, "smoke", f"""
{wisps}
{place(200, 110, 1, chamber("s8", "smoke"))}
{appear(label(500, 880, "Smoke grabs the charged bits", 48), 1.6)}
""")

# 9. The current drops, the chip sounds the alarm ------------------------------------------------------
save(SLUG, "alarm", f"""
{ceiling()}
{waves(300, 270, "sa", 4, 60, 270, 1.2, 12, 0.9, 0.9)}
<g><animateTransform attributeName="transform" type="translate" values="0 0;3 0;-3 0;0 0" begin="0.9s" dur="0.15s" repeatCount="indefinite"/>
{place(300, 90, 1.1, alarm_side(RED, 0.35))}</g>
{place(620, 470, 1.15, gauge(40, -65, 0.3, True))}
{appear(label(781, 790, "Current drops", 44, "fa"), 0.4)}
{badge(300, 880, "BEEEEP!", 0.9)}
""")

# 10. Burnt toast sets it off ----------------------------------------------------------------------
rising = "".join(
    f'<g opacity="0"><animate attributeName="opacity" values="0;0.85;0.6;0" begin="{0.7 + k * 0.45}s" dur="2.6s" repeatCount="indefinite"/>'
    f'<animateTransform attributeName="transform" type="translate" values="{x} 470;{x + 120} 360;{x + 330} 250" begin="{0.7 + k * 0.45}s" dur="2.6s" repeatCount="indefinite"/>'
    f'<animateTransform attributeName="transform" type="scale" from="0.6" to="1.5" begin="{0.7 + k * 0.45}s" dur="2.6s" repeatCount="indefinite" additive="sum"/>'
    f'{puff(38, "#5e5862")}</g>' for k, x in enumerate((220, 300, 250, 330)))
save(SLUG, "toast", f"""
{ceiling()}
<rect x="40" y="780" width="560" height="34" rx="10" fill="{WOOD}"/>
{place(700, 90, 0.85, alarm_side(RED, 0.4))}
<g opacity="0">{fade(1.8, 0.2)}{waves(700, 240, "sa", 3, 50, 190, 1.2, 10, 0.9)}</g>
<g transform="translate(110 530)">
  {toaster()}
  <clipPath id="s10slot"><rect x="0" y="-400" width="400" height="404"/></clipPath>
  <g clip-path="url(#s10slot)"><g><animateTransform attributeName="transform" type="translate" values="0 140;0 -20;0 0" keyTimes="0;0.7;1" begin="0.2s" dur="0.5s" fill="freeze"/>
  {toast_slice(85)}{toast_slice(190)}</g></g>
</g>
{rising}
{appear(label(300, 885, "Burnt toast", 48, "fa"), 0.6)}
""")

# 11. The particles can't get through a sheet of paper ------------------------------------------------
shots = "".join(
    f'<g opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.9;1" dur="0.9s" begin="{k * 0.18:.2f}s" repeatCount="indefinite"/>'
    f'<animateTransform attributeName="transform" type="translate" from="250 {450 + dy * 0.2:.0f}" to="{555 + dy * 0.05:.0f} {450 + dy:.0f}" dur="0.9s" begin="{k * 0.18:.2f}s" repeatCount="indefinite"/>'
    f'<circle r="12" class="fa2" filter="url(#glow)"/></g>'
    for k, dy in enumerate((-200, -110, -30, 50, 130, 210)))
flashes = "".join(f'<circle cx="{560 + dy * 0.05:.0f}" cy="{450 + dy}" r="26" class="fa2" opacity="0" filter="url(#soft)">'
                  f'<animate attributeName="opacity" values="0;0;1;0" keyTimes="0;0.85;0.92;1" dur="0.9s" begin="{k * 0.18:.2f}s" repeatCount="indefinite"/></circle>'
                  for k, dy in enumerate((-200, -110, -30, 50, 130, 210)))
save(SLUG, "paper", f"""
{shadow(180, 640, 110, 18)}
{place(190, 450, 0.6, button(300), rot=90)}
{shots}
{shadow(600, 780, 120, 18)}
<polygon points="560,190 660,140 660,710 560,770" fill="url(#paper)"/>
<polygon points="560,190 660,140 660,170 560,220" fill="#fff" opacity="0.5"/>
{flashes}
{pop(840, 450, f'<circle r="64" fill="{GREEN}"/><path d="M-28 0 l18 20 l36 -40" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>', 1.4)}
{badge(500, 890, "STOPPED BY PAPER", 1.0)}
""")

# 12. Newer alarms use light instead ----------------------------------------------------------------
save(SLUG, "light", f"""
{place(500, 440, 1, alarm_face("s12", 340, place(0, 0, 0.6, photo_chamber())))}
{appear(label(500, 880, "Light instead of a speck", 48, "fa2"), 0.8)}
""")

# 13. LED beam misses the hidden sensor until smoke bounces light onto it ---------------------------
save(SLUG, "scatter", f"""
{place(500, 420, 1.2, photo_chamber(scatter=True))}
{appear(label(500, 890, "Smoke bounces light onto the sensor", 46), 1.8)}
""")

# 14. The little disc above your bed, watching all night --------------------------------------------
stars = "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#fff"><animate attributeName="opacity" values="1;0.2;1" begin="{k * 0.4}s" dur="1.6s" repeatCount="indefinite"/></circle>'
                for k, (x, y) in enumerate(((95, 230), (205, 270), (120, 360), (225, 395))))
zzz = "".join(f'<text x="420" y="520" font-size="{40 + k * 12}" font-weight="700" class="fa2" opacity="0">Z'
              f'<animate attributeName="opacity" values="0;1;0" begin="{k * 0.6}s" dur="1.8s" repeatCount="indefinite"/>'
              f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{40 + k * 20} -110" begin="{k * 0.6}s" dur="1.8s" repeatCount="indefinite"/></text>'
              for k in range(3))
save(SLUG, "bedroom", f"""
{ceiling()}
<rect x="60" y="180" width="200" height="260" rx="14" fill="url(#metal)"/>
<rect x="74" y="194" width="172" height="232" rx="8" fill="#14203f"/>
<circle cx="200" cy="245" r="30" fill="#ffe9a8"/><circle cx="214" cy="236" r="26" fill="#14203f"/>
{stars}
<rect x="157" y="194" width="6" height="232" fill="#3a3a44"/>
{waves(620, 240, "sa2", 2, 40, 200, 3.0, 4, 0.35)}
{place(620, 90, 0.75, alarm_side(GREEN, 1.6))}
{shadow(580, 815, 360, 18)}
<rect x="250" y="520" width="44" height="290" rx="12" fill="{WOOD_DARK}"/>
<rect x="290" y="700" width="640" height="56" rx="10" fill="{WOOD}"/>
<rect x="300" y="756" width="26" height="50" fill="{WOOD_DARK}"/><rect x="890" y="756" width="26" height="50" fill="{WOOD_DARK}"/>
<rect x="290" y="640" width="640" height="70" rx="18" fill="#ecebf2"/>
<ellipse cx="370" cy="628" rx="78" ry="32" fill="#fff"/>
<circle cx="390" cy="596" r="46" fill="{SKIN}"/>
<path d="M346 588 q6 -50 54 -42 q34 8 36 36 q-40 -14 -90 6 z" fill="#2a1d18"/>
<path d="M392 604 q10 6 20 0" class="nf" stroke="#7a3f30" stroke-width="4" stroke-linecap="round"/>
<path d="M430 650 Q450 590 540 596 Q720 584 880 618 Q930 628 930 670 L930 712 L430 712 Z" fill="#3b4a8a">
  <animate attributeName="d" values="M430 650 Q450 590 540 596 Q720 584 880 618 Q930 628 930 670 L930 712 L430 712 Z;M430 650 Q450 580 540 588 Q720 578 880 614 Q930 626 930 670 L930 712 L430 712 Z;M430 650 Q450 590 540 596 Q720 584 880 618 Q930 628 930 670 L930 712 L430 712 Z" dur="3s" repeatCount="indefinite"/></path>
<path d="M470 640 Q600 610 760 625" class="nf" stroke="#fff" stroke-opacity="0.15" stroke-width="8" stroke-linecap="round"/>
{zzz}
{badge(500, 900, "WATCHING ALL NIGHT", 1.0)}
""")
