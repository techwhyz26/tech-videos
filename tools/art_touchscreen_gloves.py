"""Illustrations for the 'touchscreen-gloves' video. Run:  python tools/art_touchscreen_gloves.py

Objects (phone with a home screen, pointing hand as bare skin / wool glove / touchscreen glove,
a cut-away of the screen with its electrode grid, a sausage) are drawn once in their own
coordinates and placed with translate+rotate+scale, so every scene reuses them.
"""
import random

from artlib import appear, badge, draw, fade, label, phone, pop, save, shadow, waves

SLUG = "touchscreen-gloves"
RED = "#ff4d4d"
GREEN = "#3ddc84"
SKIN, SKIN_LINE = "#f2c6a0", "#c98f66"
WOOL, WOOL_DARK = "#c8414a", "#8f2530"
ICONS = ["#8f7cff", "#ffc93c", "#3ddc84", "#ff6b6b", "#38c6ff", "#ff9f43", "#f368e0", "#c8d6e5"]


def place(x: float, y: float, s: float, inner: str, rot: float = 0) -> str:
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">{inner}</g>'


# ---------------------------------------------------------------------------------------------
# The phone: artlib's phone body with a home screen of app icons.
PW, PH = 380, 760            # phone size used in most scenes
SW, SH = PW - 24, PH - 24    # its screen


def home(sw: float = SW, sh: float = SH, dim: float = 1.0, pressed: int | None = None, begin: float = 1.0) -> str:
    """Home screen in screen coordinates. `pressed` = index of an icon that lights up and opens."""
    size = sw * 0.17
    gap = (sw - 4 * size) / 5
    out = [f'<circle cx="{sw * 0.7}" cy="{sh * 0.3}" r="{sw * 0.6}" class="fa" opacity="{0.16 * dim}" filter="url(#soft)"/>',
           f'<text x="{sw / 2}" y="{sh * 0.13}" font-size="{sw * 0.17:.0f}" text-anchor="middle" opacity="{0.9 * dim}">9:41</text>']
    opening = ""
    corner = (sw + 24) * 0.14 - 8   # same corner radius as artlib's phone screen
    for k in range(16):
        i, j = k % 4, k // 4
        x, y = gap + i * (size + gap), sh * 0.22 + j * (size + gap * 1.3)
        colour = ICONS[(k * 3) % len(ICONS)]
        out.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{size:.0f}" height="{size:.0f}" rx="{size * 0.26:.0f}" '
                   f'fill="{colour}" opacity="{0.9 * dim}"/>')
        if pressed == k:
            out.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{size:.0f}" height="{size:.0f}" rx="{size * 0.26:.0f}" '
                       f'fill="#fff" opacity="0"><animate attributeName="opacity" values="0;0.8;0" begin="{begin}s" dur="0.4s" fill="freeze"/></rect>')
            # the app opens: a window grows out of the icon to fill the screen, then its content fades in
            t = begin + 0.35
            rows = "".join(f'<rect x="{sw * 0.1:.0f}" y="{sh * (0.36 + r * 0.09):.0f}" width="{sw * (0.8 - r % 2 * 0.25):.0f}" '
                           f'height="{sh * 0.035:.0f}" rx="{sh * 0.017:.0f}" fill="#fff" opacity="0.35"/>' for r in range(5))
            opening = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{size:.0f}" height="{size:.0f}" rx="{size * 0.26:.0f}" fill="#16161f" opacity="0">'
                       f'<set attributeName="opacity" to="1" begin="{t}s"/>'
                       f'<animate attributeName="x" to="0" begin="{t}s" dur="0.45s" fill="freeze"/>'
                       f'<animate attributeName="y" to="0" begin="{t}s" dur="0.45s" fill="freeze"/>'
                       f'<animate attributeName="width" to="{sw}" begin="{t}s" dur="0.45s" fill="freeze"/>'
                       f'<animate attributeName="height" to="{sh}" begin="{t}s" dur="0.45s" fill="freeze"/>'
                       f'<animate attributeName="rx" to="{corner}" begin="{t}s" dur="0.45s" fill="freeze"/></rect>'
                       f'<g opacity="0">{fade(t + 0.45, 0.3)}'
                       f'<rect x="0" y="0" width="{sw}" height="{sh * 0.26:.0f}" rx="{corner}" fill="{colour}"/>'
                       f'<rect x="0" y="{corner}" width="{sw}" height="{sh * 0.26 - corner:.0f}" fill="{colour}"/>'
                       f'<circle cx="{sw / 2}" cy="{sh * 0.13:.0f}" r="{sw * 0.11:.0f}" fill="#fff" opacity="0.85"/>{rows}</g>')
    out.append(f'<rect x="{gap * 0.6:.0f}" y="{sh - size - gap * 1.6:.0f}" width="{sw - gap * 1.2:.0f}" height="{size + gap:.0f}" '
               f'rx="{size * 0.35:.0f}" fill="#fff" opacity="{0.1 * dim}"/>')
    return "".join(out) + opening


def grid_overlay(sw: float = SW, sh: float = SH, step: float = 44, op: float = 0.45) -> str:
    """The invisible electrode grid, made visible: rows in the accent colour, columns in the second."""
    rows = "".join(f'<line x1="0" y1="{y}" x2="{sw}" y2="{y}" class="sa" stroke-width="4" opacity="{op}"/>'
                   for y in range(int(step / 2), int(sh), int(step)))
    cols = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{sh}" class="sa2" stroke-width="4" opacity="{op}"/>'
                   for x in range(int(step / 2), int(sw), int(step)))
    return rows + cols


def scan_bar(sw: float = SW, sh: float = SH, dur: float = 0.9) -> str:
    return (f'<rect x="0" y="0" width="{sw}" height="12" rx="6" class="fa" filter="url(#glow)">'
            f'<animate attributeName="y" from="0" to="{sh - 12}" dur="{dur}s" repeatCount="indefinite"/></rect>')


def handset(screen: str, w: float = PW, h: float = PH) -> str:
    """Phone at (0,0) with its ground shadow."""
    return shadow(w / 2, h + 16, w * 0.5, 20) + phone(0, 0, w, h, screen)


# ---------------------------------------------------------------------------------------------
# The pointing hand. Fingertip at (0,0), finger points up, the fist and wrist hang below (to y=540).
def hand(kind: str = "skin", uid: str = "h") -> str:
    """kind: 'skin' (bare hand + sleeve), 'glove' (wool glove), 'touch' (glove with a silver fingertip)."""
    if kind == "skin":
        base, line = SKIN, SKIN_LINE
        over = ""
        defs = ""
    else:
        base, line = WOOL, WOOL_DARK
        defs = (f'<defs><pattern id="{uid}k" width="18" height="14" patternUnits="userSpaceOnUse">'
                f'<path d="M1 2 l8 9 l8 -9" fill="none" stroke="{WOOL_DARK}" stroke-width="3" opacity="0.65"/></pattern></defs>')
        over = f"url(#{uid}k)"

    def shapes(f: str, stroke: str, sw: float) -> str:
        st = f'stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        return (f'<rect x="-62" y="170" width="208" height="240" rx="62" fill="{f}" {st}/>'
                f'<rect x="-34" y="0" width="68" height="250" rx="34" fill="{f}" {st}/>'
                + "".join(f'<rect x="20" y="{186 + k * 60}" width="130" height="58" rx="29" fill="{f}" {st}/>' for k in range(3)))

    thumb_d = "M-74 372 Q-84 300 -14 270 L36 252"
    if kind == "skin":
        wrist = ('<rect x="-56" y="396" width="196" height="150" rx="22" fill="#3a3f5c"/>'
                 '<rect x="-56" y="396" width="196" height="34" rx="12" fill="#2b2f45"/>'
                 '<rect x="-44" y="384" width="172" height="30" rx="12" fill="#e2b38c"/>')
    else:
        ribs = "".join(f'<line x1="{x}" y1="404" x2="{x}" y2="540" stroke="{WOOL_DARK}" stroke-width="6" opacity="0.8"/>'
                       for x in range(-40, 140, 18))
        wrist = (f'<rect x="-58" y="392" width="200" height="152" rx="24" fill="#b23640"/>{ribs}')

    body = shapes(base, line, 4)
    if over:
        body += shapes(over, "", 0)
    thumb = (f'<path d="{thumb_d}" fill="none" stroke="{line}" stroke-width="64" stroke-linecap="round"/>'
             f'<path d="{thumb_d}" fill="none" stroke="{base}" stroke-width="56" stroke-linecap="round"/>')
    if over:
        thumb += f'<path d="{thumb_d}" fill="none" stroke="{over}" stroke-width="56" stroke-linecap="round"/>'
    shine = '<rect x="-22" y="24" width="14" height="150" rx="7" fill="#fff" opacity="0.25"/>'
    tip = ""
    if kind == "touch":
        threads = "".join(f'<path d="M-30 {y} q10 -6 20 0 t20 0 t20 0" fill="none" stroke="#7d8396" stroke-width="3"/>'
                          for y in (22, 38, 54, 68))
        tip = (f'<path d="M-35 78 V34 A35 35 0 0 1 35 34 V78 Z" fill="url(#steel)" stroke="#8a8f9e" stroke-width="3"/>'
               f'{threads}'
               f'<path d="M-14 6 l4 10 l10 4 l-10 4 l-4 10 l-4 -10 l-10 -4 l10 -4 z" fill="#fff">'
               f'<animate attributeName="opacity" values="0;1;0" dur="1.6s" repeatCount="indefinite"/></path>')
    return f"{defs}{wrist}{body}{thumb}{shine}{tip}"


def tapping(inner: str, dist: float = 40, dur: float = 1.1, begin: float = 0) -> str:
    """Moves the hand toward the screen and back, over and over (a tap)."""
    return (f'<g><animateTransform attributeName="transform" type="translate" values="0 {dist};0 0;0 0;0 {dist}" '
            f'keyTimes="0;0.3;0.6;1" begin="{begin}s" dur="{dur}s" repeatCount="indefinite"/>{inner}</g>')


def snow(n: int = 22, seed: int = 3, x0: float = 20, x1: float = 980) -> str:
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x = rnd.uniform(x0, x1)
        r = rnd.uniform(5, 11)
        d = rnd.uniform(3.5, 6)
        b = -rnd.uniform(0, d)
        out.append(f'<circle cx="{x:.0f}" cy="-20" r="{r:.1f}" fill="#fff" opacity="0.75">'
                   f'<animate attributeName="cy" from="-20" to="1000" begin="{b:.2f}s" dur="{d:.2f}s" repeatCount="indefinite"/>'
                   f'<animateTransform attributeName="transform" type="translate" values="0 0;24 0;0 0" begin="{b:.2f}s" '
                   f'dur="{d / 2:.2f}s" repeatCount="indefinite"/></circle>')
    return "".join(out)


def cross_mark(r: float = 46) -> str:
    return (f'<circle r="{r}" fill="{RED}"/><path d="M-{r * .4} -{r * .4} L{r * .4} {r * .4} M{r * .4} -{r * .4} L-{r * .4} {r * .4}" '
            f'stroke="#fff" stroke-width="{r * .22}" stroke-linecap="round"/>')


def check_mark(r: float = 46) -> str:
    return (f'<circle r="{r}" fill="{GREEN}"/><path d="M-{r * .42} 0 l{r * .3} {r * .32} l{r * .56} -{r * .62}" fill="none" '
            f'stroke="#fff" stroke-width="{r * .22}" stroke-linecap="round" stroke-linejoin="round"/>')


# ---------------------------------------------------------------------------------------------
# Cut-away of the screen, seen from the side: glass, the electrode grid, the display underneath.
PX, PY, PWID, PHGT = 40, 70, 920, 740
GLASS_T, GLASS_B = 500, 575
ELEC_Y = 596
ELECS = [130 + i * 92.5 for i in range(9)]


def arc(x1: float, x2: float) -> str:
    return f"M{x1} {ELEC_Y} C{x1} 410 {x2} 410 {x2} {ELEC_Y}"


def section(uid: str, finger: str, inner_extra: str = "") -> str:
    """finger: 'bare' (finger on the glass), 'glove' (wool keeps it 60 px away), 'touch' (silver threads)."""
    cx = 500
    under = {3, 4} if finger in ("bare", "touch") else set()   # field arcs the finger steals
    arcs = []
    for i in range(len(ELECS) - 1):
        a = (f'<path d="{arc(ELECS[i], ELECS[i + 1])}" class="nf sa" stroke-width="6" stroke-dasharray="14 12" opacity="0.8">'
             f'<animate attributeName="stroke-dashoffset" from="0" to="-52" dur="0.8s" repeatCount="indefinite"/>')
        if i in under:
            a += '<animate attributeName="opacity" from="0.8" to="0" begin="1.1s" dur="0.4s" fill="freeze"/>'
        arcs.append(a + "</path>")
    elecs = "".join(f'<rect x="{x - 26}" y="{ELEC_Y - 6}" width="52" height="24" rx="6" class="{"fa" if i % 2 else "fa2"}"/>'
                    for i, x in enumerate(ELECS))
    pixels = "".join(f'<rect x="{x}" y="640" width="26" height="40" rx="4" fill="{ICONS[(x // 34) % len(ICONS)]}" opacity="0.55"/>'
                     for x in range(70, 930, 34))
    stack = (f'<rect x="{PX}" y="{GLASS_T}" width="{PWID}" height="{GLASS_B - GLASS_T}" fill="#bfe6ff" opacity="0.22"/>'
             f'<rect x="{PX}" y="{GLASS_T}" width="{PWID}" height="6" fill="#fff" opacity="0.55"/>'
             f'<rect x="{PX}" y="625" width="{PWID}" height="70" fill="#0b0b10"/>{pixels}'
             f'<rect x="{PX}" y="700" width="{PWID}" height="{PY + PHGT - 700}" fill="url(#metal)"/>')

    # the finger, seen from the side, pointing down
    if finger == "bare":
        tip_y = GLASS_T - 2
        drop = f'<animateTransform attributeName="transform" type="translate" values="0 -170;0 0" begin="0.2s" dur="0.8s" fill="freeze"/>'
        fing = (f'<rect x="{cx - 90}" y="{PY - 40}" width="180" height="{tip_y - PY + 40}" rx="90" fill="{SKIN}" stroke="{SKIN_LINE}" stroke-width="4"/>'
                f'<path d="M{cx + 60} {tip_y - 150} q24 40 10 110 q-30 -10 -34 -60 z" fill="#f7dcc4" stroke="{SKIN_LINE}" stroke-width="3"/>'
                f'<rect x="{cx - 66}" y="{PY}" width="16" height="{tip_y - PY - 90}" rx="8" fill="#fff" opacity="0.22"/>')
        fing = f'<g>{drop}{fing}</g>'
    else:
        tip_y = GLASS_T - 62
        knit = (f'<defs><pattern id="{uid}k" width="22" height="16" patternUnits="userSpaceOnUse">'
                f'<path d="M1 2 l10 11 l10 -11" fill="none" stroke="{WOOL_DARK}" stroke-width="4" opacity="0.7"/></pattern></defs>')
        glove = (f'{knit}<rect x="{cx - 152}" y="{PY - 40}" width="304" height="{GLASS_T - 2 - PY + 40}" rx="152" fill="{WOOL}"/>'
                 f'<rect x="{cx - 152}" y="{PY - 40}" width="304" height="{GLASS_T - 2 - PY + 40}" rx="152" fill="url(#{uid}k)"/>'
                 f'<rect x="{cx - 90}" y="{PY - 40}" width="180" height="{tip_y - PY + 40}" rx="90" fill="{SKIN}" stroke="{SKIN_LINE}" stroke-width="4"/>'
                 f'<rect x="{cx - 66}" y="{PY}" width="16" height="{tip_y - PY - 90}" rx="8" fill="#fff" opacity="0.22"/>')
        fing = glove
    return f"""
<defs><clipPath id="{uid}c"><rect x="{PX}" y="{PY}" width="{PWID}" height="{PHGT}" rx="36"/></clipPath></defs>
<rect x="{PX}" y="{PY}" width="{PWID}" height="{PHGT}" rx="36" fill="#fff" fill-opacity="0.05"/>
<g clip-path="url(#{uid}c)">{stack}{''.join(arcs)}{elecs}{fing}{inner_extra}</g>
<rect x="{PX}" y="{PY}" width="{PWID}" height="{PHGT}" rx="36" fill="none" stroke="#fff" stroke-opacity="0.2" stroke-width="3"/>"""


def charge_flow(paths: list[str], begin: float, cls: str = "fa2", dur: float = 0.9) -> str:
    """Little charge dots running along each path, over and over."""
    out = []
    for p in paths:
        for k in range(3):
            b = begin + k * dur / 3
            out.append(f'<circle r="10" class="{cls}" opacity="0" filter="url(#glow)">'
                       f'<set attributeName="opacity" to="1" begin="{b:.2f}s"/>'
                       f'<animateMotion path="{p}" begin="{b:.2f}s" dur="{dur}s" repeatCount="indefinite"/></circle>')
    return "".join(out)


def lit(xs: list[float], begin: float) -> str:
    """Electrodes that light up because their charge changed."""
    return "".join(f'<rect x="{x - 34}" y="{ELEC_Y - 14}" width="68" height="40" rx="10" fill="#fff" opacity="0" filter="url(#glow)">'
                   f'<animate attributeName="opacity" values="0;0.9;0.4;0.9" begin="{begin}s" dur="1s" fill="freeze"/></rect>'
                   for x in xs)


def sausage(uid: str) -> str:
    """A sausage lying along +x, its rounded tip at (0,0), about 440 long."""
    marks = "".join(f'<path d="M{x} -34 l26 68" stroke="#5a2414" stroke-width="9" stroke-linecap="round" opacity="0.55"/>'
                    for x in (120, 210, 300))
    return (f'<defs><linearGradient id="{uid}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e0734a"/>'
            f'<stop offset="1" stop-color="#8e3519"/></linearGradient></defs>'
            f'<rect x="0" y="-48" width="420" height="96" rx="48" fill="url(#{uid}g)"/>'
            f'{marks}<rect x="40" y="-34" width="320" height="14" rx="7" fill="#fff" opacity="0.28"/>'
            f'<path d="M414 -10 l34 -14 l4 22 l-4 22 l-34 -14 z" fill="#a8441f"/>')


# =============================================================================================
# 1. Winter gloves on, and the phone acts like you're not there ----------------------------------
ring = (f'<circle cx="0" cy="0" r="30" fill="none" stroke="{RED}" stroke-width="7" stroke-dasharray="12 10" opacity="0">'
        f'<animate attributeName="opacity" values="0;0;1;0" keyTimes="0;0.3;0.45;1" dur="1.1s" repeatCount="indefinite"/></circle>')
save(SLUG, "ignored", f"""
{snow(18, 1)}
{place(110, 50, 1, handset(home()))}
{place(300, 450, 0.95, tapping(hand("glove", "s1") + ring), -22)}
{badge(770, 300, "NO TOUCH", 1.4, "fa2")}
""")

# 2. So why does it ignore a hard press? -------------------------------------------------------------
strain = "".join(
    f'<path d="M{dx:.0f} {dy:.0f} l{ex:.0f} {ey:.0f}" class="sa2" stroke-width="9" stroke-linecap="round" opacity="0">'
    f'<animate attributeName="opacity" values="0;1;0" begin="{0.6 + k * 0.12:.2f}s" dur="0.6s" repeatCount="indefinite"/></path>'
    for k, (dx, dy, ex, ey) in enumerate([(-70, -20, -40, -14), (-62, 30, -40, 10), (70, -20, 40, -14), (62, 30, 40, 10)]))
press = (f'<g><animateTransform attributeName="transform" type="translate" values="0 60;0 0;-4 2;4 0;-4 2;4 0;0 0" '
         f'keyTimes="0;0.25;0.4;0.55;0.7;0.85;1" begin="0.2s" dur="1.4s" fill="freeze"/>{hand("glove", "s2")}</g>{strain}')
save(SLUG, "press", f"""
{place(300, 40, 1, handset(home(), 400, 800))}
{place(500, 420, 1.0, press)}
{pop(840, 180, '<circle r="80" class="fa2"/><text y="50" font-size="150" font-weight="700" text-anchor="middle" style="fill:#0a0a0a">?</text>', 1.2)}
""")

# 3. It isn't feeling your touch. It's sensing the electricity in your body ------------------------
charge = "".join(
    f'<circle r="9" class="fa2" filter="url(#glow)"><animateMotion path="M{40 + dx} 520 L{40 + dx} 300 L0 200 L0 10" '
    f'begin="{k * 0.25:.2f}s" dur="1.1s" repeatCount="indefinite"/></circle>'
    for k, dx in enumerate((-30, 0, 30, -15)))
aura = ('<rect x="-90" y="-40" width="260" height="600" rx="120" class="fa" opacity="0.25" filter="url(#soft)">'
        '<animate attributeName="opacity" values="0.15;0.4;0.15" dur="1.2s" repeatCount="indefinite"/></rect>')
save(SLUG, "body", f"""
{place(80, 70, 0.85, handset(home() + waves(196, 400, "sa2", 3, 10, 150, 1.4, 6)))}
{place(257, 420, 1.0, aura + hand("skin", "s3") + charge, -20)}
{appear(label(780, 260, "Your body", 44), 0.6)}
{appear(label(780, 320, "carries charge", 44, "fa2"), 0.9)}
""")

# 4. Under the glass: a grid of invisible wires --------------------------------------------------------
def iso(y: float, inner: str, start: float) -> str:
    return (f'<g><animateTransform attributeName="transform" type="translate" values="0 {430 - y};0 0" '
            f'begin="0.2s" dur="0.9s" fill="freeze"/>'
            f'<g transform="translate(410 {y}) scale(1 0.55) rotate(-40)">{inner}</g></g>')


lay_glass = ('<rect x="-150" y="-280" width="300" height="560" rx="44" fill="#bfe6ff" fill-opacity="0.16" stroke="#fff" stroke-opacity="0.7" stroke-width="5"/>'
             '<path d="M-120 -120 L60 -260 M-120 -40 L120 -230" stroke="#fff" stroke-width="14" stroke-linecap="round" opacity="0.25"/>')
grid_lines = "".join(
    f'<line x1="-150" y1="{y}" x2="150" y2="{y}" class="sa" stroke-width="7"><animate attributeName="opacity" values="0.35;1;0.35" '
    f'begin="{k * 0.1:.1f}s" dur="1.3s" repeatCount="indefinite"/></line>' for k, y in enumerate(range(-250, 260, 40))) + "".join(
    f'<line x1="{x}" y1="-280" x2="{x}" y2="280" class="sa2" stroke-width="7" opacity="0.8"/>' for x in range(-120, 130, 40))
lay_grid = f'<rect x="-150" y="-280" width="300" height="560" rx="44" fill="#000" opacity="0.35"/>{grid_lines}'
lay_screen = (f'<rect x="-150" y="-280" width="300" height="560" rx="44" fill="url(#metal)"/>'
              f'<rect x="-138" y="-268" width="276" height="536" rx="34" fill="url(#screen)"/>'
              f'<g transform="translate(-138 -268)">{home(276, 536)}</g>')
save(SLUG, "layers", f"""
{shadow(410, 830, 300, 26)}
{iso(650, lay_screen, 0)}
{iso(430, lay_grid, 0)}
{iso(210, lay_glass, 0)}
{appear('<line x1="650" y1="215" x2="720" y2="215" class="sw" stroke-width="4" opacity="0.6"/>' + label(850, 230, "Glass", 44), 1.2)}
{appear('<line x1="650" y1="435" x2="720" y2="435" class="sa" stroke-width="4"/>' + label(850, 450, "Wire grid", 44, "fa"), 1.5)}
""")

# 5. Your skin is full of salty water, so it conducts -------------------------------------------------
rnd = random.Random(11)
ions = []
for k in range(14):
    x, y = rnd.uniform(270, 730), rnd.uniform(190, 720)
    plus = k % 2 == 0
    cls = "fa2" if plus else "fa"
    jx, jy = rnd.uniform(-30, 30), rnd.uniform(-30, 30)
    ions.append(f'<g transform="translate({x:.0f} {y:.0f})"><g>'
                f'<animateTransform attributeName="transform" type="translate" values="0 0;{jx:.0f} {jy:.0f};0 0" '
                f'dur="{rnd.uniform(1.2, 2):.2f}s" repeatCount="indefinite"/>'
                f'<circle r="30" class="{cls}" opacity="0.95"/>'
                f'<text y="15" font-size="46" font-weight="700" text-anchor="middle" style="fill:#0a0a0a">{"+" if plus else "−"}</text></g></g>')
drops = "".join(f'<path d="M{x} {y} q-24 34 0 46 q24 -12 0 -46 z" fill="#7fd3ff" opacity="0.8"/>'
                for x, y in ((330, 300), (640, 260), (700, 560), (380, 600)))
ridges = "".join(f'<ellipse cx="500" cy="520" rx="{40 + k * 38}" ry="{60 + k * 46}" fill="none" stroke="#d49c74" stroke-width="7"/>'
                 for k in range(9))
save(SLUG, "skin", f"""
<defs><clipPath id="s5c"><circle cx="500" cy="440" r="350"/></clipPath></defs>
{shadow(500, 820, 300, 22, 0.5)}
<circle cx="500" cy="440" r="350" fill="#16121c"/>
<g clip-path="url(#s5c)">
  <rect x="230" y="150" width="540" height="900" rx="270" fill="{SKIN}"/>
  {ridges}
  <rect x="230" y="150" width="540" height="900" rx="270" class="fa" opacity="0"><animate attributeName="opacity" values="0;0.25;0.1;0.25" begin="0.6s" dur="1.6s" fill="freeze"/></rect>
  <g opacity="0">{fade(0.4, 0.5)}{drops}{''.join(ions)}</g>
</g>
<circle cx="500" cy="440" r="350" fill="none" stroke="url(#steel)" stroke-width="26"/>
<circle cx="500" cy="440" r="336" fill="none" stroke="#fff" stroke-opacity="0.25" stroke-width="4"/>
{appear(label(500, 905, "Salty water conducts", 50), 1.0)}
""")

# 6. Close up, the finger pulls charge away from the wires underneath ---------------------------------
steal = [f"M{ELECS[3]} {ELEC_Y} Q{ELECS[3]} 520 480 {GLASS_T - 10}",
         f"M{ELECS[4]} {ELEC_Y} L500 {GLASS_T - 10}",
         f"M{ELECS[5]} {ELEC_Y} Q{ELECS[5]} 520 520 {GLASS_T - 10}"]
steal_svg = "".join(f'<path d="{p}" class="nf sa2" stroke-width="7" opacity="0">{fade(1.1, 0.3)}</path>' for p in steal)
save(SLUG, "pull", f"""
{section("s6", "bare", steal_svg + charge_flow(steal, 1.2) + lit(ELECS[3:6], 1.2))}
{appear(label(500, 900, "Charge pulled away", 50, "fa2"), 1.4)}
""")

# 7. The phone scans every crossing, over a hundred times a second ------------------------------------
hit = (f'<g transform="translate(220 420)">{waves(0, 0, "sa2", 3, 16, 90, 1.2, 6)}'
       f'<circle r="20" class="fa2" filter="url(#glow)"/>'
       f'<path d="M-60 0 h36 M24 0 h36 M0 -60 v36 M0 24 v36" class="sw" stroke-width="6" stroke-linecap="round"/></g>')
save(SLUG, "scan", f"""
{place(70, 40, 1, handset(home(SW, SH, 0.35) + grid_overlay() + scan_bar() + appear(hit, 0.9)))}
{appear('<text x="745" y="470" font-size="170" text-anchor="middle" class="display fa">100+</text>', 0.5)}
{appear(label(745, 550, "times a second", 46), 0.8)}
""")

# 8. Pressing harder does nothing ---------------------------------------------------------------------------
light = place(200, 340, 0.62, tapping(hand("skin", "s8a"), 30, 1.2))
hard = place(700, 340, 0.62, f'<g><animateTransform attributeName="transform" type="translate" values="-5 0;5 0;-5 0" dur="0.18s" repeatCount="indefinite"/>{hand("glove", "s8b")}</g>'
             + "".join(f'<path d="M{dx} {dy} l{ex} {ey}" class="sa2" stroke-width="12" stroke-linecap="round"><animate attributeName="opacity" values="0.2;1;0.2" begin="{k * 0.15}s" dur="0.6s" repeatCount="indefinite"/></path>'
                       for k, (dx, dy, ex, ey) in enumerate([(-70, -10, -50, -10), (-64, 40, -50, 10), (70, -10, 50, -10), (64, 40, 50, 10)])))
save(SLUG, "harder", f"""
{place(60, 40, 1, handset(home(256, 536) + waves(128, 300, "sa2", 3, 10, 110, 1.2, 6), 280, 560))}
{place(560, 40, 1, handset(home(256, 536), 280, 560))}
{light}{hard}
{pop(450, 110, check_mark(44), 0.8)}
{pop(920, 110, cross_mark(44), 1.2)}
{badge(500, 905, "PRESSURE DOESN'T COUNT", 1.6)}
""")

# 9. A wool glove doesn't conduct and holds your finger too far away -----------------------------------------
gap = (f'<g opacity="0">{fade(1.0)}'
       f'<path d="M700 {GLASS_T - 62} h60 M700 {GLASS_T - 2} h60 M730 {GLASS_T - 54} v44" stroke="{RED}" stroke-width="7" stroke-linecap="round"/>'
       f'<path d="M718 {GLASS_T - 44} l12 -12 l12 12 M718 {GLASS_T - 20} l12 12 l12 -12" fill="none" stroke="{RED}" stroke-width="6" stroke-linecap="round"/>'
       f'<line x1="410" y1="{GLASS_T - 62}" x2="700" y2="{GLASS_T - 62}" stroke="{RED}" stroke-width="4" stroke-dasharray="10 8"/></g>')
save(SLUG, "gap", f"""
{section("s9", "glove", gap)}
{pop(820, 300, cross_mark(54), 1.4)}
{appear(label(500, 900, "Wool doesn't conduct", 50), 0.8)}
""")

# 10. So the charge never moves, and the screen thinks nobody is there --------------------------------------
save(SLUG, "nobody", f"""
{snow(12, 5, 560, 980)}
{place(100, 40, 1, handset(home(SW, SH, 0.3) + grid_overlay(op=0.35) + scan_bar(dur=1.1)))}
{place(300, 440, 0.95, tapping(hand("glove", "s10"), 30, 1.3), -22)}
{badge(770, 260, "NOBODY HERE", 1.2, "fa2")}
""")

# 11. A sausage works too: salty and wet, like a finger --------------------------------------------------------
save(SLUG, "sausage", f"""
{place(90, 30, 1, handset(home(pressed=5, begin=1.1)))}
<g><animateTransform attributeName="transform" type="translate" values="120 60;0 0" begin="0.2s" dur="0.8s" fill="freeze"/>
{place(240, 325, 1.2, sausage("s11"), 28)}</g>
<g opacity="0">{fade(1.0, 0.1)}{waves(240, 325, "sa2", 3, 20, 140, 1.2, 7)}</g>
{appear(label(500, 900, "Salty and wet, like a finger", 48), 1.4)}
""")

# 12. Touchscreen gloves: silver or copper thread sewn into the fingertips ----------------------------------
stitch = "".join(draw(f"M-30 {y} q10 -7 20 0 t20 0 t20 0", 0.4 + k * 0.25, 0.4, "nf", 5,
                      'stroke="#e8ecf5"') for k, y in enumerate((22, 38, 54, 68)))
save(SLUG, "thread", f"""
{shadow(470, 950, 220, 20)}
<circle cx="400" cy="190" r="120" class="fa" opacity="0.3" filter="url(#soft)"><animate attributeName="opacity" values="0.2;0.55;0.2" dur="1.4s" repeatCount="indefinite"/></circle>
{place(400, 140, 1.45, hand("touch", "s12") + stitch)}
{appear('<path d="M470 190 L600 230" class="sw" stroke-width="5" stroke-linecap="round" opacity="0.7"/>' + label(780, 245, "Silver thread", 46), 1.3)}
{appear(label(780, 305, "in the fingertip", 40, "fa2"), 1.6)}
""")

# 13. The thread carries the charge from your skin through to the glass -------------------------------------
threads = [f"M{x} {GLASS_T - 70} q-14 15 0 30 t0 30" for x in (455, 500, 545)]
thread_svg = "".join(f'<path d="{p}" fill="none" stroke="url(#steel)" stroke-width="12" stroke-linecap="round"/>' for p in threads)
up = [f"M{ELECS[3]} {ELEC_Y} Q{ELECS[3]} 520 455 {GLASS_T}",
      f"M{ELECS[4]} {ELEC_Y} L500 {GLASS_T}",
      f"M{ELECS[5]} {ELEC_Y} Q{ELECS[5]} 520 545 {GLASS_T}"]
flow = up + [f"M{x} {GLASS_T} L{x} {GLASS_T - 80}" for x in (455, 500, 545)]
bridge = (thread_svg + "".join(f'<path d="{p}" class="nf sa2" stroke-width="7" opacity="0">{fade(1.1, 0.3)}</path>' for p in up)
          + charge_flow(flow, 1.2) + lit(ELECS[3:6], 1.2))
save(SLUG, "bridge", f"""
{section("s13", "touch", bridge)}
{pop(820, 300, check_mark(54), 1.6)}
{appear(label(500, 900, "Charge gets through", 50, "fa2"), 1.4)}
""")

# 14. So your screen felt your body, and now the glove lets it through ------------------------------------
save(SLUG, "works", f"""
{snow(18, 9)}
{place(110, 50, 1, handset(home(pressed=10, begin=1.0) + appear(waves(219, 372, "sa2", 3, 10, 140, 1.2, 7), 0.6)))}
{place(341, 434, 0.95, f'<g><animateTransform attributeName="transform" type="translate" values="0 50;0 0" begin="0.2s" dur="0.5s" fill="freeze"/>{hand("touch", "s14")}</g>', -22)}
{badge(770, 300, "IT FEELS YOU", 1.6)}
""")
