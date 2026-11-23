"""Illustrations for the 'tesla-fsd-reality-view' video. Run:  python tools/art_tesla_fsd_reality_view.py

Tesla FSD v15's "Reality View": a photorealistic chase-camera view of the road that Musk says is
real-time AI video generation, not a game engine. Cars, screens and chips are drawn generically, no logos.

Objects (road view, car from behind, car from the side, centre touchscreen, virtual drone camera, car
computer, road sign, steering wheel) are drawn once in their own coordinates and placed with place().
"""
from artlib import appear, badge, bob, draw, fade, label, pop, save, shadow, waves

SLUG = "tesla-fsd-reality-view"
SUN = "#ffd36b"
PINK = "#ff6b9a"
RED = "#ff3b4a"
GREEN = "#3ddc84"


def place(x: float, y: float, s: float, inner: str) -> str:
    return f'<g transform="translate({x} {y}) scale({s})">{inner}</g>'


def sway(inner: str, deg: float = 3, dur: float = 3.4) -> str:
    return (f'<g><animateTransform attributeName="transform" type="rotate" values="{-deg};{deg};{-deg}" '
            f'dur="{dur}s" repeatCount="indefinite"/>{inner}</g>')


# --- objects ---------------------------------------------------------------------------------------

def palm(s: float = 1) -> str:
    """A palm tree with its foot at (0,0), about 300 tall at s=1."""
    fronds = "".join(
        f'<path d="M0 -290 q{dx * 0.5} {-40 + dy} {dx} {dy}" fill="none" stroke="#1f4a30" stroke-width="22" '
        f'stroke-linecap="round"/>'
        for dx, dy in ((-130, 10), (-100, -60), (-20, -90), (70, -70), (130, 0), (90, 40), (-80, 50)))
    tree = (f'<path d="M0 0 q-24 -150 0 -290" fill="none" stroke="#4a2e1e" stroke-width="20" stroke-linecap="round"/>'
            f'{fronds}<circle cx="0" cy="-290" r="16" fill="#4a2e1e"/>')
    return f'<g transform="scale({s})">{sway(tree, 2.5, 3.1)}</g>'


def car_rear(flat: bool = False) -> str:
    """A car seen from behind. (0,0) = ground centre, 360 wide, about 200 tall."""
    if flat:
        return (f'<rect x="-170" y="-60" width="50" height="60" rx="10" fill="#4a4a54"/>'
                f'<rect x="120" y="-60" width="50" height="60" rx="10" fill="#4a4a54"/>'
                f'<rect x="-180" y="-125" width="360" height="95" rx="30" fill="#8b8b96"/>'
                f'<path d="M-130 -122 L-95 -192 H95 L130 -122 Z" fill="#a2a2ac"/>'
                f'<path d="M-108 -128 L-82 -182 H82 L108 -128 Z" fill="#6a6a76"/>')
    return f"""{shadow(0, 2, 210, 22)}
<rect x="-172" y="-62" width="54" height="62" rx="12" fill="#111"/>
<rect x="118" y="-62" width="54" height="62" rx="12" fill="#111"/>
<ellipse cx="-160" cy="-138" rx="26" ry="14" fill="#c9c9d4"/>
<ellipse cx="160" cy="-138" rx="26" ry="14" fill="#c9c9d4"/>
<rect x="-182" y="-128" width="364" height="100" rx="34" fill="url(#steel)"/>
<path d="M-132 -124 L-96 -196 Q0 -206 96 -196 L132 -124 Z" fill="url(#steel)"/>
<path d="M-110 -130 L-84 -184 Q0 -192 84 -184 L110 -130 Z" fill="url(#screen)"/>
<path d="M-96 -136 L-80 -176 L-40 -178 L-60 -136 Z" fill="#fff" opacity="0.12"/>
<rect x="-168" y="-104" width="336" height="16" rx="8" fill="{RED}">
<animate attributeName="opacity" values="1;0.7;1" dur="1.6s" repeatCount="indefinite"/></rect>
<rect x="-168" y="-104" width="336" height="16" rx="8" fill="{RED}" opacity="0.5" filter="url(#glow)"/>
<rect x="-40" y="-78" width="80" height="26" rx="5" fill="url(#paper)"/>
<rect x="-176" y="-52" width="352" height="26" rx="12" fill="#2a2a32"/>
<rect x="-170" y="-126" width="340" height="6" rx="3" fill="#fff" opacity="0.5"/>"""


def car_side(roll: bool = True, paint: str = "url(#steel)") -> str:
    """A sedan seen from the side, facing right. (0,0) = ground centre, 580 long, about 215 tall."""
    def wheel(x: float) -> str:
        spokes = "".join(f'<line x1="0" y1="0" x2="0" y2="-30" stroke="#d6d6de" stroke-width="9" '
                         f'transform="rotate({a})"/>' for a in range(0, 360, 72))
        spin = ('<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="0.6s" '
                'repeatCount="indefinite"/>') if roll else ""
        return (f'<g transform="translate({x} -52)"><circle r="54" fill="#111"/><circle r="36" fill="#55555f"/>'
                f'<g>{spin}{spokes}</g><circle r="10" fill="#d6d6de"/></g>')
    return f"""{shadow(0, 4, 300, 20)}
<path d="M-290 -52 L-290 -104 Q-282 -134 -214 -140 L-128 -146 Q-66 -214 22 -216 Q120 -214 196 -150
L262 -136 Q292 -126 292 -86 L292 -52 Z" fill="{paint}"/>
<path d="M-112 -146 Q-60 -200 18 -202 Q102 -200 168 -150 Z" fill="url(#screen)"/>
<line x1="30" y1="-202" x2="30" y2="-146" stroke="#c9c9d4" stroke-width="10"/>
<path d="M-96 -152 Q-60 -186 -10 -192 L-30 -152 Z" fill="#fff" opacity="0.13"/>
<path d="M-40 -140 V-60 M120 -142 V-60" stroke="#000" stroke-opacity="0.18" stroke-width="4"/>
<rect x="-20" y="-118" width="34" height="8" rx="4" fill="#8a8a96"/>
<rect x="140" y="-118" width="34" height="8" rx="4" fill="#8a8a96"/>
<path d="M262 -122 L292 -112 L290 -96 L258 -102 Z" fill="#fff9d6"/>
<rect x="-292" y="-122" width="16" height="22" rx="5" fill="{RED}"/>
<path d="M-290 -76 H292" stroke="#000" stroke-opacity="0.15" stroke-width="10"/>
{wheel(-180)}{wheel(180)}"""


def road_view(uid: str, w: float, h: float, real: bool = True, trees: bool = True, lead: float = 0.06) -> str:
    """The chase-camera view of the road filling a w x h box at (0,0). `real` = new photoreal look,
    otherwise the old, mostly colourless sketch."""
    hz = h * 0.42
    vx = w / 2
    k = w / 1000
    road = f"{vx - w * 0.03},{hz} {vx + w * 0.03},{hz} {w * 1.25},{h} {-w * 0.25},{h}"
    lanes = "".join(
        f'<line x1="{vx + dx * w * 0.01}" y1="{hz}" x2="{w * fx}" y2="{h}" stroke="{"#fff" if real else "#7a7a88"}" '
        f'stroke-width="{7 * k}" stroke-dasharray="{40 * k} {50 * k}" opacity="0.85">'
        f'<animate attributeName="stroke-dashoffset" from="0" to="{-90 * k}" dur="0.35s" repeatCount="indefinite"/></line>'
        for dx, fx in ((-1, 0.2), (1, 0.8)))
    edges = (f'<line x1="{vx - w * 0.03}" y1="{hz}" x2="{-w * 0.25}" y2="{h}" stroke="{"#f4f4f8" if real else "#6a6a78"}" stroke-width="{9 * k}"/>'
             f'<line x1="{vx + w * 0.03}" y1="{hz}" x2="{w * 1.25}" y2="{h}" stroke="{"#f4f4f8" if real else "#6a6a78"}" stroke-width="{9 * k}"/>')
    path = (f'<polygon points="{vx - w * 0.012},{hz + h * 0.1} {vx + w * 0.012},{hz + h * 0.1} {vx + w * 0.17},{h * 0.86} '
            f'{vx - w * 0.17},{h * 0.86}" class="fa" opacity="0.35">'
            f'<animate attributeName="opacity" values="0.2;0.5;0.2" dur="1.4s" repeatCount="indefinite"/></polygon>')
    lead_car = (f'<g transform="translate({vx + w * lead} {hz + h * 0.2}) scale({0.2 * k})">'
                f'<g><animateTransform attributeName="transform" type="translate" values="0 0;-30 0;0 0" dur="4s" '
                f'repeatCount="indefinite"/>{car_rear(not real)}</g></g>')
    ego = place(vx, h * 0.985, 0.95 * k, car_rear(not real))
    if not real:
        return f"""<clipPath id="{uid}c"><rect width="{w}" height="{h}" rx="{12 * k}"/></clipPath>
<g clip-path="url(#{uid}c)">
<rect width="{w}" height="{h}" fill="#14141b"/>
<polygon points="{road}" fill="#24242d"/>{edges}{lanes}
<polygon points="{vx - w * 0.012},{hz + h * 0.1} {vx + w * 0.012},{hz + h * 0.1} {vx + w * 0.17},{h * 0.86} {vx - w * 0.17},{h * 0.86}" fill="#5c6a96" opacity="0.4"/>
{lead_car}{ego}</g>"""
    towers = []
    xs = [0.02, 0.1, 0.17, 0.26, 0.6, 0.68, 0.77, 0.86, 0.93]
    hs = [0.12, 0.2, 0.14, 0.24, 0.18, 0.27, 0.15, 0.22, 0.13]
    for i, (fx, fh) in enumerate(zip(xs, hs)):
        tw, th = w * 0.07, h * fh
        tx, ty = w * fx, hz - th
        lights = "".join(
            f'<rect x="{tx + tw * (0.15 + c * 0.3):.1f}" y="{ty + th * (0.12 + r * 0.2):.1f}" width="{tw * 0.14:.1f}" '
            f'height="{th * 0.07:.1f}" fill="{SUN}" opacity="{0.3 + ((i + r + c) % 3) * 0.25}"/>'
            for r in range(4) for c in range(3) if (i + r * c) % 2 == 0)
        towers.append(f'<rect x="{tx:.1f}" y="{ty:.1f}" width="{tw:.1f}" height="{th:.1f}" fill="#2a1840"/>{lights}')
    tree_svg = ""
    if trees:
        dur = 2.4
        for side in (-1, 1):
            for n in range(3):
                b = -n * dur / 3
                tree_svg += (
                    f'<g><animateTransform attributeName="transform" type="translate" '
                    f'values="{vx + side * w * 0.07} {hz + 4};{vx + side * w * 0.8} {h * 1.25}" keySplines="0.7 0 1 1" '
                    f'calcMode="spline" keyTimes="0;1" begin="{b}s" dur="{dur}s" repeatCount="indefinite"/>'
                    f'<g><animateTransform attributeName="transform" type="scale" values="0.03;{1.9 * k * h / w}" '
                    f'keySplines="0.7 0 1 1" calcMode="spline" keyTimes="0;1" begin="{b}s" dur="{dur}s" '
                    f'repeatCount="indefinite"/>{palm()}</g></g>')
    return f"""<linearGradient id="{uid}sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a1a6e"/>
<stop offset="0.7" stop-color="{PINK}"/><stop offset="1" stop-color="#ffb057"/></linearGradient>
<linearGradient id="{uid}gr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2f6b3a"/><stop offset="1" stop-color="#143020"/></linearGradient>
<linearGradient id="{uid}rd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#55556a"/><stop offset="1" stop-color="#26262e"/></linearGradient>
<clipPath id="{uid}c"><rect width="{w}" height="{h}" rx="{12 * k}"/></clipPath>
<g clip-path="url(#{uid}c)">
<rect width="{w}" height="{hz}" fill="url(#{uid}sk)"/>
<circle cx="{vx}" cy="{hz - h * 0.05}" r="{h * 0.1}" fill="{SUN}" filter="url(#glow)"/>
{''.join(towers)}
<rect y="{hz}" width="{w}" height="{h - hz}" fill="url(#{uid}gr)"/>
<polygon points="{road}" fill="url(#{uid}rd)"/>{edges}{lanes}{path}
{lead_car}{tree_svg}{ego}</g>"""


def screen(inner: str, w: float, h: float, ui: str = "") -> str:
    """The car's centre touchscreen; `inner` is drawn in screen coordinates (0,0 = top-left)."""
    return f"""{shadow(w / 2, h + 90, w * 0.32, 18)}
<path d="M{w / 2 - 50} {h + 10} L{w / 2 + 50} {h + 10} L{w / 2 + 80} {h + 80} L{w / 2 - 80} {h + 80} Z" fill="url(#metal)"/>
<rect x="-16" y="-16" width="{w + 32}" height="{h + 32}" rx="24" fill="#0c0c10" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>
{inner}{ui}
<path d="M0 0 h{w * 0.28} l{-w * 0.16} {h} h{-w * 0.12} z" fill="#fff" opacity="0.05"/>"""


def screen_ui(w: float, speed: str = "42", live: bool = False) -> str:
    """Speed readout (and an optional LIVE tag) drawn on the touchscreen."""
    out = (f'<rect x="18" y="18" width="128" height="86" rx="16" fill="#000" opacity="0.45"/>'
           f'<text x="82" y="70" font-size="48" font-weight="700" text-anchor="middle">{speed}</text>'
           f'<text x="82" y="96" font-size="20" text-anchor="middle" opacity="0.8">MPH</text>')
    if live:
        out += (f'<rect x="{w - 150}" y="18" width="132" height="54" rx="14" fill="#000" opacity="0.5"/>'
                f'<circle cx="{w - 124}" cy="45" r="11" fill="{RED}"><animate attributeName="opacity" values="1;0.2;1" '
                f'dur="0.9s" repeatCount="indefinite"/></circle>'
                f'<text x="{w - 104}" y="57" font-size="32" font-weight="700">LIVE</text>')
    return out


def drone() -> str:
    """The virtual camera: a little drone with a camera, outlined dashed. (0,0) = body centre."""
    props = "".join(
        f'<line x1="{x * 0.45}" y1="-30" x2="{x}" y2="-52" stroke="#55555f" stroke-width="12" stroke-linecap="round"/>'
        f'<rect x="{x - 6}" y="-70" width="12" height="20" rx="4" fill="#33333b"/>'
        f'<ellipse cx="{x}" cy="-72" rx="66" ry="8" fill="#d6d6de" opacity="0.7">'
        f'<animate attributeName="rx" values="66;14;66" dur="0.16s" repeatCount="indefinite"/></ellipse>'
        for x in (-120, 120))
    return f"""{props}
<rect x="-80" y="-44" width="160" height="76" rx="26" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="3"/>
<rect x="-60" y="-36" width="120" height="10" rx="5" fill="#fff" opacity="0.15"/>
<circle cx="-50" cy="-6" r="7" fill="{RED}"><animate attributeName="opacity" values="1;0.2;1" dur="0.8s" repeatCount="indefinite"/></circle>
<rect x="-24" y="28" width="48" height="18" fill="#33333b"/>
<circle cx="0" cy="66" r="40" fill="url(#metal)"/>
<circle cx="16" cy="70" r="26" fill="url(#screen)" stroke="#8f7cff" stroke-width="6"/>
<circle cx="8" cy="62" r="8" fill="#fff" opacity="0.6"/>
<rect x="-140" y="-96" width="280" height="216" rx="30" class="nf sa" stroke-width="5" stroke-dasharray="18 14">
<animate attributeName="stroke-dashoffset" from="0" to="-64" dur="1s" repeatCount="indefinite"/></rect>"""


def computer(uid: str, half: bool = True) -> str:
    """The car's computer board, 760x460 at (0,0), with two big accelerator chips. With `half`, only the
    left half of the first chip lights up."""
    traces = "".join(
        f'<path d="M{x0} {y0} H{x1} V{y1} H{x2}" fill="none" stroke="#d8a640" stroke-width="5" opacity="0.55"/>'
        for x0, y0, x1, y1, x2 in ((40, 70, 120, 140, 140), (40, 330, 100, 260, 140), (330, 60, 360, 140, 430),
                                    (330, 400, 370, 300, 430), (720, 90, 680, 160, 630), (720, 380, 690, 290, 630)))
    pins = "".join(f'<rect x="0" y="{60 + i * 34}" width="26" height="18" rx="3" fill="#d8a640"/>' for i in range(11))
    caps = "".join(f'<rect x="{150 + i * 46}" y="380" width="26" height="40" rx="5" fill="#2b2b33"/>' for i in range(10))

    def chip(x: float, y: float, lit: bool) -> str:
        legs = "".join(f'<rect x="{x + 18 + i * 22}" y="{y - 12}" width="10" height="224" fill="#b9b9c6"/>' for i in range(8))
        glow = ""
        if lit:
            glow = (f'<rect x="{x + 30}" y="{y + 30}" width="70" height="140" rx="6" class="fa" filter="url(#glow)">'
                    f'<animate attributeName="opacity" values="0.55;1;0.55" dur="0.8s" repeatCount="indefinite"/></rect>'
                    + "".join(f'<rect x="{x + 38 + c * 20}" y="{y + 40 + r * 20}" width="12" height="12" fill="#fff" opacity="0">'
                              f'<animate attributeName="opacity" values="0;0.9;0" begin="{(r * 3 + c) * 0.11:.2f}s" dur="0.9s" '
                              f'repeatCount="indefinite"/></rect>' for r in range(6) for c in range(3)))
        return (f'{legs}<rect x="{x}" y="{y}" width="200" height="200" rx="16" fill="url(#metal)" stroke="#fff" '
                f'stroke-opacity="0.25" stroke-width="3"/>'
                f'<rect x="{x + 30}" y="{y + 30}" width="140" height="140" rx="8" fill="url(#screen)"/>{glow}'
                f'<line x1="{x + 100}" y1="{y + 22}" x2="{x + 100}" y2="{y + 178}" stroke="#fff" stroke-opacity="0.35" '
                f'stroke-width="3" stroke-dasharray="8 8"/>')
    return f"""<linearGradient id="{uid}pcb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1d4a35"/>
<stop offset="1" stop-color="#0c2418"/></linearGradient>
{shadow(380, 480, 360, 24)}
<rect x="10" y="0" width="760" height="460" rx="28" fill="url(#{uid}pcb)" stroke="#fff" stroke-opacity="0.25" stroke-width="4"/>
{pins}{traces}{caps}
{chip(140, 120, half)}{chip(430, 120, False)}
<text x="60" y="440" font-size="26" opacity="0.7">AI4</text>"""


def road_sign(garbled: bool = True) -> str:
    """A green overhead road sign on two posts. (0,0) = ground centre; sign face 600x300."""
    words = ["MAIN ST", "MAlN 5T", "NAIM ŠT", "MΛIИ S7"] if garbled else ["MAIN ST"]
    n = len(words)
    texts = ""
    for i, wd in enumerate(words):
        vals = ";".join("1" if j == i else "0" for j in range(n)) + (";1" if i == 0 else ";0")
        texts += (f'<text x="0" y="-410" font-size="90" font-weight="700" text-anchor="middle" opacity="{1 if i == 0 else 0}">'
                  f'{wd}' + (f'<animate attributeName="opacity" values="{vals}" calcMode="discrete" dur="1.6s" '
                             f'repeatCount="indefinite"/>' if garbled else "") + '</text>')
    return f"""{shadow(0, 6, 340, 22)}
<rect x="-250" y="-560" width="26" height="566" fill="url(#steel)"/>
<rect x="224" y="-560" width="26" height="566" fill="url(#steel)"/>
<rect x="-300" y="-640" width="600" height="300" rx="26" fill="#13703f"/>
<rect x="-284" y="-624" width="568" height="268" rx="18" fill="none" stroke="#fff" stroke-width="8"/>
<path d="M-30 -560 L0 -590 L30 -560 M0 -590 V-536" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
{texts}"""


def wheel() -> str:
    """A steering wheel, centre at (0,0), radius 150."""
    return f"""<circle r="150" fill="none" stroke="#4a4a58" stroke-width="36"/>
<circle r="150" fill="none" stroke="#fff" stroke-opacity="0.35" stroke-width="6" stroke-dasharray="260 682" transform="rotate(200)"/>
<path d="M-140 10 Q-70 30 -40 70 H40 Q70 30 140 10" fill="none" stroke="#4a4a58" stroke-width="34"/>
<ellipse cx="0" cy="40" rx="64" ry="50" fill="url(#metal)" stroke="#fff" stroke-opacity="0.2" stroke-width="3"/>"""


def calendar() -> str:
    """A tear-off calendar page, 300x320 at (0,0)."""
    grid = "".join(f'<rect x="{30 + c * 36}" y="{120 + r * 36}" width="26" height="26" rx="5" fill="#c9c5ba"/>'
                   for r in range(5) for c in range(7) if not (r == 0 and c < 2))
    return f"""{shadow(150, 330, 150, 16)}
<rect width="300" height="320" rx="24" fill="url(#paper)"/>
<rect width="300" height="90" rx="24" class="fa"/><rect y="60" width="300" height="30" class="fa"/>
<text x="150" y="64" font-size="46" font-weight="700" text-anchor="middle" style="fill:#0a0a0a">DECEMBER</text>
<circle cx="90" cy="-4" r="12" fill="#55555f"/><circle cx="210" cy="-4" r="12" fill="#55555f"/>
{grid}"""


def gauge(value: float, begin: float) -> str:
    """A compute meter (semicircle, radius 150), needle swings to `value` 0..1. (0,0) = needle pivot."""
    ang = -90 + 180 * value
    return f"""<path d="M-150 0 A150 150 0 0 1 150 0" fill="none" stroke="#fff" stroke-opacity="0.15" stroke-width="34"/>
<path d="M-150 0 A150 150 0 0 1 150 0" fill="none" class="sa" stroke-width="34" pathLength="1" stroke-dasharray="1"
stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" from="1" to="{1 - value:.2f}" begin="{begin}s" dur="0.8s" fill="freeze"/></path>
<g transform="rotate(-90)"><animateTransform attributeName="transform" type="rotate" from="-90" to="{ang}" begin="{begin}s" dur="0.8s" fill="freeze"/>
<line x1="0" y1="0" x2="0" y2="-125" stroke="#fff" stroke-width="10" stroke-linecap="round"/></g>
<circle r="18" fill="url(#steel)"/>"""


def red_x(r: float = 70) -> str:
    return (f'<circle r="{r}" fill="{RED}" opacity="0.92"/><path d="M{-r * .42} {-r * .42} L{r * .42} {r * .42} '
            f'M{r * .42} {-r * .42} L{-r * .42} {r * .42}" stroke="#fff" stroke-width="{r * 0.2}" stroke-linecap="round"/>')


def ground(y: float, x0: float = 40, x1: float = 960) -> str:
    """A strip of road with dashes rushing left, for side-view scenes."""
    return (f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="70" rx="20" fill="#2a2a32"/>'
            f'<line x1="{x0 + 20}" y1="{y + 35}" x2="{x1 - 20}" y2="{y + 35}" stroke="#fff" stroke-opacity="0.7" stroke-width="7" '
            f'stroke-dasharray="50 50"><animate attributeName="stroke-dashoffset" from="0" to="100" dur="0.35s" '
            f'repeatCount="indefinite"/></line>')


# --- scenes ----------------------------------------------------------------------------------------
SW, SH = 800, 500  # touchscreen size used for close-ups

# 1. Tesla turned its self-driving screen into something that looks like GTA ---------------------
save(SLUG, "hook", f"""
<path d="M0 760 Q500 690 1000 760 V820 H0 Z" fill="#17171d"/>
{place(250, 200, 0.85, screen(road_view("a", 800, 500) + screen_ui(800), 800, 500))}
{place(205, 690, 1.0, '<g><animateTransform attributeName="transform" type="rotate" values="-6;6;-6" dur="3s" repeatCount="indefinite"/>' + wheel() + '</g>')}
{badge(560, 905, "IT'S LIKE GTA", 1.4)}
""")

# 2. So what is actually drawing that picture? ------------------------------------------------------
save(SLUG, "what", f"""
<clipPath id="wrev"><rect x="100" y="140" width="0" height="500">
<animate attributeName="width" values="0;800;800" keyTimes="0;0.7;1" dur="2.6s" repeatCount="indefinite"/></rect></clipPath>
{place(100, 140, 1, screen('<rect width="800" height="500" rx="12" fill="#050507"/>', 800, 500))}
<g clip-path="url(#wrev)">{place(100, 140, 1, road_view("b", 800, 500))}</g>
<rect x="96" y="130" width="10" height="520" rx="5" fill="#fff" filter="url(#glow)">
<animate attributeName="x" values="96;896;896" keyTimes="0;0.7;1" dur="2.6s" repeatCount="indefinite"/></rect>
{pop(170, 110, '<circle r="66" class="fa2"/><text y="40" font-size="116" font-weight="700" text-anchor="middle" style="fill:#0a0a0a">?</text>', 0.8)}
{pop(860, 720, '<circle r="54" class="fa2"/><text y="33" font-size="94" font-weight="700" text-anchor="middle" style="fill:#0a0a0a">?</text>', 1.2)}
""")

# 3. An AI that makes up video of your surroundings, live, as you drive -----------------------------
frames = "".join(
    pop(x, y, f'<g transform="rotate({rot})"><rect x="-118" y="-78" width="236" height="156" rx="10" fill="#0c0c10" '
              f'stroke="#fff" stroke-opacity="0.35" stroke-width="3"/>{place(-110, -70, 1, road_view(f"c{i}", 220, 140, trees=False, lead=0.02 * i))}</g>', b)
    for i, (x, y, rot, b) in enumerate(((180, 200, -8, 0.5), (420, 140, -3, 0.9), (660, 160, 4, 1.3), (860, 260, 9, 1.7))))
beams = "".join(
    f'<line x1="500" y1="520" x2="{x}" y2="{y + 80}" class="sa" stroke-width="5" stroke-dasharray="12 14" opacity="0">'
    f'{fade(b - 0.2, 0.2)}<animate attributeName="stroke-dashoffset" from="0" to="-52" dur="0.5s" repeatCount="indefinite"/></line>'
    for x, y, b in ((180, 200, 0.5), (420, 140, 0.9), (660, 160, 1.3), (860, 260, 1.7)))
save(SLUG, "ai-video", f"""
{beams}
{ground(712)}
{place(500, 720, 1.0, car_side())}
<circle cx="500" cy="520" r="18" class="fa" filter="url(#glow)"><animate attributeName="r" values="14;22;14" dur="0.8s" repeatCount="indefinite"/></circle>
{frames}
{appear(label(500, 900, "Video made up live, by AI", 50), 1.9)}
""")

# 4. Tesla calls it Reality View, part of FSD version fifteen ---------------------------------------
tab = ('<rect x="560" y="18" width="222" height="54" rx="14" fill="#000" opacity="0.5"/>'
       '<text x="671" y="55" font-size="30" font-weight="700" text-anchor="middle" class="fa">Reality View</text>')
save(SLUG, "reality-view", f"""
<g><animateTransform attributeName="transform" type="scale" values="0.94;1" dur="3s" fill="freeze" additive="sum"/>
{place(100, 110, 1, screen(road_view("d", 800, 500) + screen_ui(800, "38") + tab, 800, 500))}
</g>
{badge(500, 890, "FULL SELF-DRIVING V15", 1.0)}
""")

# 5. The old screen was a mostly colourless sketch of the road --------------------------------------
save(SLUG, "old", f"""
{place(100, 110, 1, screen(road_view("e", 800, 500, real=False) + screen_ui(800, "38"), 800, 500))}
{appear(label(500, 860, "Before: mostly colourless", 50), 0.6)}
""")

# 6. A virtual camera floats above and behind the car, like a drone ---------------------------------
save(SLUG, "drone", f"""
<polygon points="310,330 600,560 880,600 880,740 560,740" class="fa" opacity="0.14">
<animate attributeName="opacity" values="0.08;0.22;0.08" dur="1.6s" repeatCount="indefinite"/></polygon>
<line x1="310" y1="330" x2="560" y2="740" class="sa" stroke-width="4" stroke-dasharray="14 12" opacity="0.7"/>
<line x1="310" y1="330" x2="880" y2="600" class="sa" stroke-width="4" stroke-dasharray="14 12" opacity="0.7"/>
{ground(722)}
{place(650, 730, 0.95, car_side())}
{pop(230, 250, bob(drone(), 14, 2.2), 0.4)}
{appear(label(260, 480, "Virtual camera", 46, "fa"), 1.1)}
""")

# 7. Musk says there's no game engine behind it -------------------------------------------------------
def box3d(x: float, y: float, w: float, h: float, d: float, b: float) -> str:
    p = (f"M{x} {y} h{w} v{h} h{-w} z M{x} {y} l{d} {-d * 0.6} h{w} l{-d} {d * 0.6} "
         f"M{x + w} {y} l{d} {-d * 0.6} v{h} l{-d} {d * 0.6}")
    return draw(p, b, 0.7, "nf sa", 5)


grid = "".join(f'<line x1="{100 + i * 100}" y1="760" x2="{500 + (i - 4) * 30}" y2="560" stroke="#8f7cff" stroke-opacity="0.35" stroke-width="3"/>'
               for i in range(9))
save(SLUG, "no-engine", f"""
<polygon points="100,760 900,760 620,560 380,560" fill="#8f7cff" opacity="0.06"/>
{grid}
{box3d(170, 380, 130, 330, 60, 0.1)}{box3d(330, 260, 150, 450, 70, 0.3)}{box3d(520, 330, 120, 380, 60, 0.5)}
{box3d(680, 440, 140, 270, 60, 0.7)}
{pop(500, 470, red_x(150), 0.9)}
{badge(500, 880, "NO GAME ENGINE", 1.2)}
""")

# 8. It's real-time AI video generation, made fresh as you drive -----------------------------------
counter = "".join(
    f'<text x="500" y="745" font-size="54" text-anchor="middle" class="display fa" opacity="0">FRAME {n:04d}'
    f'<animate attributeName="opacity" values="{";".join("1" if j == i else "0" for j in range(6))}" calcMode="discrete" '
    f'dur="2.4s" repeatCount="indefinite"/></text>' for i, n in enumerate(range(1, 7)))
stack = "".join(f'<rect x="{150 + o}" y="{120 - o}" width="700" height="440" rx="16" fill="#1a1a22" stroke="#fff" '
                f'stroke-opacity="0.25" stroke-width="3"/>' for o in (40, 20))
save(SLUG, "frames", f"""
{stack}
<clipPath id="frev"><rect x="150" y="120" width="0" height="440">
<animate attributeName="width" values="0;700;700" keyTimes="0;0.8;1" dur="0.4s" repeatCount="indefinite"/></rect></clipPath>
<rect x="150" y="120" width="700" height="440" rx="16" fill="#0c0c10"/>
<g clip-path="url(#frev)">{place(150, 120, 1, road_view("f", 700, 440))}</g>
<rect x="150" y="120" width="700" height="440" rx="16" fill="none" stroke="#fff" stroke-opacity="0.35" stroke-width="4"/>
{counter}
{badge(500, 880, "REAL-TIME AI VIDEO", 0.8)}
""")

# 9. It runs on just half of one accelerator chip in the car's computer -----------------------------
save(SLUG, "chip", f"""
{place(100, 170, 1.04, computer("g"))}
{appear(f'<path d="M346 150 V110 H230" class="nf sa" stroke-width="5"/>', 1.0)}
{appear(label(230, 90, "Half of one chip", 46, "fa"), 1.0)}
{badge(500, 860, "THAT'S ALL IT USES", 1.6)}
""")

# 10. Less computing power than Tesla's earliest self-driving visuals ------------------------------
save(SLUG, "compute", f"""
{place(80, 130, 0.48, screen(road_view("h", 800, 500, real=False), 800, 500))}
{place(540, 130, 0.48, screen(road_view("i", 800, 500), 800, 500))}
{place(272, 680, 1, gauge(0.85, 0.5))}
{place(732, 680, 1, gauge(0.4, 1.0))}
{label(272, 790, "Earliest visuals", 44)}
{label(732, 790, "Reality View", 44, "fa")}
""")

# 11. But here's the part most people miss: it's not a camera feed ----------------------------------
cam_screen = place(560, 110, 0.44, screen(road_view("j", 800, 500), 800, 500))
save(SLUG, "not-camera", f"""
{place(340, 770, 1.3, car_rear())}
<circle cx="340" cy="532" r="16" fill="#111" stroke="#8a8a96" stroke-width="5"/>
<circle cx="340" cy="532" r="7" class="fa"/>
<path d="M340 516 Q400 300 600 360" class="nf sw" stroke-width="6" stroke-dasharray="16 14" opacity="0.7">
<animate attributeName="stroke-dashoffset" from="0" to="-60" dur="0.6s" repeatCount="indefinite"/></path>
{cam_screen}
{pop(450, 340, red_x(56), 1.0)}
{badge(500, 900, "NOT A CAMERA FEED", 1.6)}
""")

# 12. A road sign gives it away: generated, not stitched from camera angles ------------------------
lens = ('<circle r="110" fill="#fff" fill-opacity="0.08" stroke="url(#steel)" stroke-width="22"/>'
        '<line x1="80" y1="80" x2="170" y2="170" stroke="url(#metal)" stroke-width="34" stroke-linecap="round"/>'
        '<path d="M-60 -50 a80 80 0 0 1 50 -36" fill="none" stroke="#fff" stroke-width="8" opacity="0.5" stroke-linecap="round"/>')
save(SLUG, "sign", f"""
{place(500, 760, 1.0, road_sign())}
<g transform="translate(700 380)"><g opacity="0">{fade(0.6)}
<animateTransform attributeName="transform" type="translate" values="0 0;-160 10;0 0" begin="0.6s" dur="3s" repeatCount="indefinite"/>{lens}</g></g>
{appear(label(500, 880, "The words keep changing", 50, "fa2"), 1.2)}
""")

# 13. The lag is a bit high; Musk plans to cut about 35% of it ---------------------------------------
turn = '<animateTransform attributeName="transform" type="rotate" values="0;-35;-35;0;0" keyTimes="0;0.15;0.5;0.65;1" dur="3s" repeatCount="indefinite"/>'
lagged = ('<animateTransform attributeName="transform" type="rotate" values="0 400 500;0 400 500;-8 400 500;-8 400 500;0 400 500;0 400 500" '
          'keyTimes="0;0.15;0.3;0.65;0.8;1" dur="3s" repeatCount="indefinite"/>')
save(SLUG, "lag", f"""
{place(380, 140, 0.72, screen(f'<clipPath id="lgc"><rect width="800" height="500" rx="12"/></clipPath><g clip-path="url(#lgc)"><g>{lagged}<g transform="translate(-100 -60) scale(1.25)">' + road_view("k", 800, 500) + '</g></g></g>', 800, 500))}
{place(200, 520, 0.95, '<g>' + turn + wheel() + '</g>')}
<rect x="120" y="760" width="760" height="40" rx="20" fill="#fff" opacity="0.12"/>
<rect x="120" y="760" width="760" height="40" rx="20" class="fa2"><animate attributeName="width" from="760" to="494" begin="1.0s" dur="0.9s" fill="freeze"/></rect>
<text x="140" y="740" font-size="44">Screen lag</text>
{appear('<text x="760" y="890" font-size="110" text-anchor="middle" class="display fa2">-35%</text>', 1.6)}
""")

# 14. Early access testers have it now; everyone else in December -----------------------------------
grey = '<g opacity="0.45">' + car_side(False) + '</g>'
save(SLUG, "rollout", f"""
{waves(220, 420, "sa", 3, 30, 190, 1.8, 7)}
{ground(552, 40, 960)}
{place(220, 560, 0.55, car_side())}
{place(565, 560, 0.42, grey)}{place(830, 560, 0.42, grey)}
{appear(label(220, 690, "Testers: now", 44, "fa"), 0.4)}
{pop(690, 290, place(-150, -160, 0.95, calendar()), 1.2)}
{appear(label(697, 690, "Everyone else", 44), 1.4)}
{badge(500, 860, "HOLIDAY UPDATE", 1.9)}
""")

# 15. So that GTA view isn't a recording; it's an AI imagining it, live ----------------------------
save(SLUG, "payoff", f"""
<clipPath id="prev"><rect x="100" y="110" width="0" height="500">
<animate attributeName="width" values="0;800;800" keyTimes="0;0.5;1" dur="3s" repeatCount="indefinite"/></rect></clipPath>
{place(100, 110, 1, screen('<rect width="800" height="500" rx="12" fill="#14141b"/>', 800, 500))}
<g clip-path="url(#prev)">{place(100, 110, 1, road_view("l", 800, 500) + place(0, 0, 1, screen_ui(800, "42", live=True)))}</g>
{badge(500, 880, "IMAGINED, LIVE", 1.0)}
""")
