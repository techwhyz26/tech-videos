"""Illustrations for the 'gta6-ray-tracing' video. Run:  python tools/art_gta6_ray_tracing.py

How a console draws Grand Theft Auto VI's sunset city: ray-traced light, 1440p stretched to 4K, 30 frames
a second because of the city simulation. Everything is generic (a console, a TV, a coastal city at sunset,
a car, people); no game logos or characters.

Objects are drawn once in their own coordinates and placed with place(), like tools/art_microwave.py.
"""
import math

from artlib import appear, badge, bob, draw, fade, label, phone, pop, save, shadow, waves

SLUG = "gta6-ray-tracing"
SUN = "#ffd36b"
PINK = "#ff6b9a"
CYAN = "#38c6ff"


def place(x: float, y: float, s: float, inner: str) -> str:
    return f'<g transform="translate({x} {y}) scale({s})">{inner}</g>'


def sway(inner: str, cx: float, cy: float, deg: float = 3, dur: float = 3.4) -> str:
    return (f'<g><animateTransform attributeName="transform" type="rotate" values="{-deg} {cx} {cy};{deg} {cx} {cy};'
            f'{-deg} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>{inner}</g>')


# --- objects ---------------------------------------------------------------------------------------

def palm(x: float, y: float, s: float = 1) -> str:
    """A palm tree with its foot at (x, y), about 300 tall at s=1."""
    fronds = "".join(
        f'<path d="M0 -290 q{dx * 0.5} {-40 + dy} {dx} {dy}" fill="none" stroke="#1d3b2a" stroke-width="22" '
        f'stroke-linecap="round"/>'
        for dx, dy in ((-130, 10), (-100, -60), (-20, -90), (70, -70), (130, 0), (90, 40), (-80, 50)))
    tree = (f'<path d="M0 0 q-24 -150 0 -290" fill="none" stroke="#3a2418" stroke-width="20" stroke-linecap="round"/>'
            f'{fronds}<circle cx="0" cy="-290" r="16" fill="#3a2418"/>')
    return place(x, y, s, sway(tree, 0, 0, 2.5, 3 + (x % 7) / 5))


def city(uid: str, w: float, h: float, rays: bool = False) -> str:
    """A coastal city at sunset filling a w x h box at (0,0): sky, sun, towers, palms, sea."""
    horizon = h * 0.66
    towers = []
    xs = [0.04, 0.12, 0.2, 0.3, 0.38, 0.5, 0.6, 0.7, 0.78, 0.88]
    hs = [0.22, 0.34, 0.26, 0.42, 0.3, 0.36, 0.48, 0.28, 0.38, 0.24]
    for i, (fx, fh) in enumerate(zip(xs, hs)):
        tw, th = w * 0.075, h * fh
        tx, ty = w * fx, horizon - th
        lights = "".join(
            f'<rect x="{tx + 6 + c * tw / 3}" y="{ty + 10 + r * 22}" width="{tw / 5}" height="9" fill="{SUN}" '
            f'opacity="{0.25 + ((i + r + c) % 3) * 0.25}"/>'
            for r in range(int(th // 22) - 1) for c in range(3))
        towers.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" fill="#2a1840"/>{lights}'
                      f'<rect x="{tx}" y="{ty}" width="{tw * 0.25}" height="{th}" fill="{PINK}" opacity="0.22"/>')
    shimmer = "".join(
        f'<rect x="{w * (0.15 + 0.12 * k)}" y="{horizon + 18 + k % 3 * 22}" width="{w * 0.14}" height="6" rx="3" '
        f'fill="{SUN}" opacity="0.5"><animate attributeName="opacity" values="0.15;0.7;0.15" begin="{k * 0.3}s" '
        f'dur="1.8s" repeatCount="indefinite"/></rect>' for k in range(6))
    ray = ""
    if rays:
        ray = "".join(
            f'<line x1="{w * 0.5}" y1="{horizon - h * 0.08}" x2="{w * 0.5 + math.cos(a) * w}" '
            f'y2="{horizon - h * 0.08 + math.sin(a) * w}" stroke="{SUN}" stroke-width="10" opacity="0">'
            f'<animate attributeName="opacity" values="0;0.35;0" begin="{k * 0.25}s" dur="2s" repeatCount="indefinite"/></line>'
            for k, a in enumerate(math.radians(d) for d in (200, 225, 250, 290, 315, 340)))
    return f"""
<linearGradient id="{uid}sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b1458"/>
<stop offset="0.55" stop-color="{PINK}"/><stop offset="1" stop-color="#ffb057"/></linearGradient>
<linearGradient id="{uid}sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3b2a6e"/>
<stop offset="1" stop-color="#0d1f3c"/></linearGradient>
<clipPath id="{uid}c"><rect width="{w}" height="{h}"/></clipPath>
<g clip-path="url(#{uid}c)">
<rect width="{w}" height="{horizon}" fill="url(#{uid}sky)"/>
<circle cx="{w * 0.5}" cy="{horizon - h * 0.08}" r="{h * 0.16}" fill="{SUN}" filter="url(#glow)">
<animate attributeName="r" values="{h * 0.155};{h * 0.17};{h * 0.155}" dur="3s" repeatCount="indefinite"/></circle>
{ray}{''.join(towers)}
<rect y="{horizon}" width="{w}" height="{h - horizon}" fill="url(#{uid}sea)"/>{shimmer}
{palm(w * 0.08, h * 1.02, h / 520)}{palm(w * 0.93, h * 1.04, h / 470)}
</g>"""


def tv(uid: str, inner: str, w: float = 700, h: float = 400) -> str:
    """A flat TV at (0,0) with a w x h picture; `inner` is drawn in picture coordinates."""
    return f"""{shadow(w / 2, h + 70, w * 0.4, 18)}
<rect x="{w / 2 - 20}" y="{h + 20}" width="40" height="44" fill="#2a2a32"/>
<rect x="{w / 2 - 130}" y="{h + 58}" width="260" height="16" rx="8" fill="url(#metal)"/>
<rect x="-18" y="-18" width="{w + 36}" height="{h + 36}" rx="18" fill="#0c0c10" stroke="#fff" stroke-opacity="0.28" stroke-width="4"/>
<g transform="translate(0 0)">{inner}</g>
<path d="M0 0 h{w * 0.3} l{-w * 0.18} {h} h{-w * 0.12} z" fill="#fff" opacity="0.05"/>"""


def console(pro: bool = False) -> str:
    """A tall games console standing upright, (0,0) = foot centre, about 430 tall."""
    stripes = ""
    if pro:
        stripes = "".join(f'<rect x="-82" y="{-300 + i * 26}" width="164" height="8" rx="4" fill="#111" opacity="0.45"/>'
                          for i in range(3))
    return f"""{shadow(0, 6, 150, 18)}
<rect x="-110" y="-12" width="220" height="18" rx="9" fill="#1c1c22"/>
<path d="M-70 -430 h140 v418 h-140 z" fill="#15151b"/>
<path d="M-70 -440 q-40 10 -48 60 l-8 360 q30 10 56 8 z" fill="url(#steel)"/>
<path d="M70 -440 q40 10 48 60 l8 360 q-30 10 -56 8 z" fill="url(#steel)"/>
{stripes}
<rect x="-6" y="-420" width="12" height="396" rx="6" fill="{CYAN}" filter="url(#glow)">
<animate attributeName="opacity" values="0.5;1;0.5" dur="2.4s" repeatCount="indefinite"/></rect>
<rect x="-52" y="-120" width="34" height="10" rx="5" fill="#333"/>"""


def car(uid: str, color: str = PINK, reflect: str = "") -> str:
    """A sports car side view, (0,0) = between the wheels on the ground, about 520 wide.
    `reflect` is drawn clipped to the body (for reflections)."""
    body = "M-260 -40 q0 -50 40 -60 l90 -12 q40 -60 120 -64 q90 -2 130 56 l110 18 q30 6 30 50 v20 h-520 z"
    wheel = lambda x: (f'<g transform="translate({x} -10)"><circle r="46" fill="#0d0d10"/><circle r="28" fill="url(#steel)"/>'
                       f'<g><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="0.8s" '
                       f'repeatCount="indefinite"/>' +
                       "".join(f'<rect x="-4" y="-26" width="8" height="24" fill="#666" transform="rotate({a})"/>'
                               for a in (0, 72, 144, 216, 288)) + '</g></g>')
    return f"""{shadow(0, 30, 280, 20, 0.7)}
<clipPath id="{uid}b"><path d="{body}"/></clipPath>
<path d="{body}" fill="{color}"/>
<g clip-path="url(#{uid}b)">
<rect x="-270" y="-60" width="560" height="40" fill="#000" opacity="0.25"/>
{reflect}
<rect x="-300" y="-130" width="60" height="130" fill="#fff" opacity="0.35" transform="skewX(-25)">
<animateTransform attributeName="transform" type="translate" values="0 0;640 0" dur="2.6s" repeatCount="indefinite" additive="sum"/></rect>
</g>
<path d="M-118 -110 q36 -50 108 -54 q70 0 104 46 z" fill="#1d2440"/>
<path d="M-104 -112 q30 -40 90 -44 v44 z" fill="{CYAN}" opacity="0.35"/>
<rect x="232" y="-82" width="26" height="14" rx="5" fill="{SUN}"/>
<rect x="-262" y="-80" width="18" height="14" rx="4" fill="#ff3b3b"/>
{wheel(-160)}{wheel(170)}"""


def npc(color: str, skin: str = "#e8b48c", s: float = 1) -> str:
    """A small walking person, (0,0) = feet, about 200 tall at s=1."""
    legs = (f'<rect x="-18" y="-80" width="14" height="80" rx="7" fill="#26304a">'
            f'<animateTransform attributeName="transform" type="rotate" values="-12 -11 -80;12 -11 -80;-12 -11 -80" '
            f'dur="0.8s" repeatCount="indefinite"/></rect>'
            f'<rect x="4" y="-80" width="14" height="80" rx="7" fill="#26304a">'
            f'<animateTransform attributeName="transform" type="rotate" values="12 11 -80;-12 11 -80;12 11 -80" '
            f'dur="0.8s" repeatCount="indefinite"/></rect>')
    return place(0, 0, s, f"""{shadow(0, 4, 40, 8)}{legs}
<path d="M-30 -76 q0 -70 30 -74 q30 4 30 74 z" fill="{color}"/>
<circle cx="0" cy="-172" r="24" fill="{skin}"/>
<path d="M-25 -178 q2 -26 26 -24 q22 2 24 22 q-20 -10 -50 2 z" fill="#2a1d18"/>""")


def chip(scale: float = 1) -> str:
    """A processor chip centred at (0,0), 260 wide."""
    pins = "".join(
        f'<rect x="{-110 + i * 30}" y="-160" width="12" height="30" rx="4" fill="#c9a24a"/>'
        f'<rect x="{-110 + i * 30}" y="130" width="12" height="30" rx="4" fill="#c9a24a"/>'
        f'<rect x="-160" y="{-110 + i * 30}" width="30" height="12" rx="4" fill="#c9a24a"/>'
        f'<rect x="130" y="{-110 + i * 30}" width="30" height="12" rx="4" fill="#c9a24a"/>' for i in range(8))
    return place(0, 0, scale, f"""{pins}
<rect x="-130" y="-130" width="260" height="260" rx="26" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>
<rect x="-80" y="-80" width="160" height="160" rx="14" fill="url(#steel)"/>
<text x="0" y="16" font-size="46" font-weight="700" text-anchor="middle" fill="#2a2a32">CPU</text>""")


def gamebox(uid: str) -> str:
    """A game case at (0,0), 150 x 190, with sunset cover art."""
    return (f'<rect x="-6" y="-6" width="162" height="202" rx="12" fill="#0d1a3a"/>'
            f'<g transform="translate(8 8)">{city(uid, 134, 174)}</g>'
            f'<rect x="-6" y="-6" width="162" height="202" rx="12" fill="none" stroke="#fff" stroke-opacity="0.35" stroke-width="3"/>')


def ray(points: list[tuple[float, float]], begin: float, color: str = SUN, width: float = 9) -> str:
    """A light ray drawn along points, then a bright dot travelling along it forever."""
    d = "M " + " L ".join(f"{x} {y}" for x, y in points)
    return (draw(d, begin, 0.8, "nf", width, f'stroke="{color}" filter="url(#glow)"') +
            f'<circle r="13" fill="#fff" opacity="0">{fade(begin + 0.8, 0.1)}'
            f'<animateMotion path="{d}" begin="{begin + 0.8}s" dur="1.4s" repeatCount="indefinite"/></circle>')


def sun(cx: float, cy: float, r: float = 70) -> str:
    beams = "".join(f'<rect x="-6" y="{-r - 44}" width="12" height="30" rx="6" fill="{SUN}" transform="rotate({a})"/>'
                    for a in range(0, 360, 45))
    return (f'<g transform="translate({cx} {cy})"><g><animateTransform attributeName="transform" type="rotate" '
            f'from="0" to="360" dur="12s" repeatCount="indefinite"/>{beams}</g>'
            f'<circle r="{r}" fill="{SUN}" filter="url(#glow)"/></g>')


def eye(cx: float, cy: float) -> str:
    """A camera (the player's view) pointing left."""
    return (f'<g transform="translate({cx} {cy})"><rect x="-10" y="-60" width="140" height="120" rx="22" fill="url(#metal)" '
            f'stroke="#fff" stroke-opacity="0.3" stroke-width="4"/><circle cx="-10" cy="0" r="52" fill="#15151b" '
            f'stroke="url(#steel)" stroke-width="12"/><circle cx="-10" cy="0" r="22" fill="{CYAN}">'
            f'<animate attributeName="r" values="18;26;18" dur="1.6s" repeatCount="indefinite"/></circle></g>')


# --- scenes ----------------------------------------------------------------------------------------

# 1. Just launched: a TV showing the sunset city, and a pile of game cases
boxes = "".join(pop(x, 655, f'<g transform="rotate({r}) translate(-75 -95)">{gamebox(f"b{i}")}</g>', 0.5 + i * 0.15)
                for i, (x, r) in enumerate([(230, -12), (365, -5), (500, 0), (635, 5), (770, 12)]))
save(SLUG, "launch", f"""
{place(150, 70, 1, tv("l", city("lc", 700, 380, rays=True), 700, 380))}
{shadow(500, 770, 330, 20)}
{boxes}
{badge(500, 900, "19 MILLION COPIES", 1.6)}
""")

# 2. Critics: 99 out of 100
cards = "".join(
    pop(x, y, f'<rect x="-90" y="-60" width="180" height="120" rx="16" fill="url(#paper)"/>'
              f'<rect x="-66" y="-36" width="132" height="12" rx="6" fill="#bbb"/>'
              f'<rect x="-66" y="-12" width="100" height="12" rx="6" fill="#ccc"/>'
              f'<text x="0" y="40" font-size="34" text-anchor="middle" fill="{PINK}">★★★★★</text>', b)
    for x, y, b in ((170, 260, 0.9), (830, 300, 1.1), (160, 700, 1.3), (840, 720, 1.5)))
score = (f'<rect x="20" y="70" width="276" height="330" rx="24" fill="#120f22"/>'
         f'<text x="158" y="290" font-size="190" font-weight="700" text-anchor="middle" fill="{SUN}">99</text>'
         f'<text x="158" y="370" font-size="48" text-anchor="middle" fill="#fff" opacity="0.8">/ 100</text>')
save(SLUG, "score", f"""
{waves(500, 470, "sa2", 3, 120, 460, 2.4, 6, 0.5)}
{shadow(500, 860, 190, 22)}
{bob(phone(330, 120, 340, 700, appear(score, 0.3)), 8)}
{cards}
""")

# 3. How does a console draw a city this real?
save(SLUG, "question", f"""
{place(330, 120, 0.86, tv("q", city("qc", 700, 400), 700, 400))}
{place(160, 820, 0.95, console())}
{pop(780, 700, '<text x="0" y="60" font-size="260" font-weight="700" text-anchor="middle" class="fa2">?</text>', 1.0)}
""")

# 4. It traces the light: sun -> car -> camera
save(SLUG, "traces", f"""
{sun(170, 190)}
{place(430, 760, 0.9, car("t"))}
{eye(830, 300)}
{ray([(210, 240), (420, 640), (760, 320)], 0.3)}
{ray([(150, 260), (300, 650), (520, 640), (760, 300)], 0.9)}
{ray([(240, 210), (640, 650), (760, 340)], 1.5)}
{badge(500, 925, "RAY TRACING", 1.2)}
""")

# 5. Older games painted the shadows on ahead of time
brush = (f'<g><animateTransform attributeName="transform" type="translate" values="-200 0;200 0;-200 0" '
         f'dur="2.2s" repeatCount="indefinite"/><g transform="translate(500 760) rotate(30)">'
         f'<rect x="-14" y="-260" width="28" height="200" rx="12" fill="#b07a4a"/>'
         f'<rect x="-20" y="-70" width="40" height="40" fill="url(#steel)"/>'
         f'<path d="M-22 -30 h44 l-6 46 q-16 14 -32 0 z" fill="#1a1a1a"/></g></g>')
save(SLUG, "baked", f"""
<g opacity="0">{fade(0.2, 1.4, 0.85)}<ellipse cx="500" cy="770" rx="320" ry="44" fill="#000"/></g>
{place(500, 680, 1.0, car("k", CYAN))}
{brush}
{appear(label(500, 220, "PAINTED ON BY HAND", 64, "display fw"), 0.4)}
{appear(label(500, 290, "before the game ships", 40, "fw"), 0.7)}
""")

# 6. Rays bounce off cars and windows: a glass tower reflected in the car
tower = "".join(f'<rect x="{80 + c * 70}" y="{120 + r * 70}" width="58" height="58" fill="{CYAN}" opacity="{0.25 + (r + c) % 3 * 0.18}"/>'
                for r in range(7) for c in range(4))
moving_reflection = (f'<g opacity="0.55"><animateTransform attributeName="transform" type="translate" '
                     f'values="-120 0;120 0;-120 0" dur="4s" repeatCount="indefinite"/>' +
                     "".join(f'<rect x="{-240 + i * 80}" y="-130" width="40" height="120" fill="{CYAN}"/>' for i in range(7)) +
                     '</g>')
save(SLUG, "reflect", f"""
<rect x="70" y="110" width="290" height="510" rx="8" fill="#1d2440"/>{tower}
{sun(830, 170, 60)}
{place(560, 800, 0.95, car("r", PINK, moving_reflection))}
{ray([(790, 220), (600, 650), (330, 420)], 0.3)}
{ray([(770, 210), (330, 300), (480, 650)], 1.0, CYAN)}
{appear(label(500, 960, "REFLECTIONS", 56, "display fw"), 1.2)}
""")

# 7. Bounced light fills the shade: a street between two walls at sunset
save(SLUG, "bounce", f"""
<rect x="60" y="120" width="300" height="680" fill="#c9773e"/>
<rect x="640" y="120" width="300" height="680" fill="#2a1840"/>
<rect x="640" y="120" width="300" height="680" fill="#ff8a3d" opacity="0">
<animate attributeName="opacity" values="0;0.55" begin="1.4s" dur="1.2s" fill="freeze"/></rect>
{''.join(f'<rect x="{100 + c * 90}" y="{170 + r * 110}" width="50" height="70" rx="4" fill="#3a1c10" opacity="0.6"/>' for r in range(5) for c in range(3))}
{''.join(f'<rect x="{680 + c * 90}" y="{170 + r * 110}" width="50" height="70" rx="4" fill="#0d0820" opacity="0.6"/>' for r in range(5) for c in range(3))}
<rect x="60" y="800" width="880" height="60" fill="#1a1420"/>
{sun(500, 110, 50)}
{ray([(480, 160), (360, 470), (640, 560)], 0.4)}
{ray([(520, 160), (360, 620), (640, 720)], 0.9)}
{place(500, 860, 0.9, npc(CYAN))}
{badge(500, 945, "BOUNCED LIGHT", 1.6)}
""")

# 8. Every person gets hair drawn strand by strand
def strand(i: int) -> str:
    """One hair strand from the crown, curving down the left or right side of the head (never the face)."""
    side = -1 if i % 2 else 1
    k = i // 2
    x0, y0 = 500 + side * (20 + k * 12), 290 + k * 4
    return draw(f"M{x0} {y0} C{500 + side * (150 + k * 6)} {280 + k * 3} {500 + side * (205 + k * 3)} {420 + k * 10} "
                f"{500 + side * (178 + k * 4)} {560 + k * 14}",
                0.2 + i * 0.04, 0.5, "nf", 7, f'stroke="{["#5a3a26", "#3a2418", "#7a5236"][i % 3]}"')


strands = "".join(strand(i) for i in range(26))
save(SLUG, "hair", f"""
{shadow(500, 900, 220, 24)}
<rect x="420" y="640" width="160" height="140" rx="40" fill="#d9a07a"/>
<path d="M300 900 q0 -150 200 -160 q200 10 200 160 z" class="fa"/>
<ellipse cx="500" cy="480" rx="170" ry="200" fill="#e8b48c"/>
<circle cx="560" cy="480" r="13" fill="#1a1a1a"/><circle cx="440" cy="480" r="13" fill="#1a1a1a"/>
<path d="M470 580 q30 18 60 0" fill="none" stroke="#7a3f30" stroke-width="7" stroke-linecap="round"/>
<path d="M330 420 q10 -150 170 -150 q160 0 170 150 q-80 -60 -340 0 z" fill="#3a2418"/>
{strands}
{appear(label(500, 180, "EVERY STRAND", 64, "display fw"), 1.4)}
""")

# 9. The catch: a magnifier over the TV picture shows the pixels
pixels = "".join(f'<rect x="{-90 + c * 30}" y="{-90 + r * 30}" width="28" height="28" '
                 f'fill="{[PINK, SUN, "#2a1840", "#ffb057", CYAN][(r * 3 + c * 2) % 5]}"/>' for r in range(6) for c in range(6))
lens = (f'<g><animateTransform attributeName="transform" type="translate" values="300 330;620 380;300 330" '
        f'dur="4s" repeatCount="indefinite"/><clipPath id="lensc"><circle r="96"/></clipPath>'
        f'<g clip-path="url(#lensc)">{pixels}</g><circle r="100" fill="none" stroke="url(#steel)" stroke-width="22"/>'
        f'<rect x="64" y="64" width="34" height="140" rx="16" fill="#3a2418" transform="rotate(-45 80 80)"/></g>')
save(SLUG, "catch", f"""
{place(150, 150, 1, tv("c", city("cc", 700, 400), 700, 400))}
{appear(lens, 0.5)}
{badge(500, 890, "THE CATCH", 1.0)}
""")

# 10. Drawn at 1440p, stretched to 4K
small_grid = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="180" stroke="#000" stroke-opacity="0.35" stroke-width="2"/>'
                     for x in range(0, 320, 20)) + "".join(
    f'<line x1="0" y1="{y}" x2="320" y2="{y}" stroke="#000" stroke-opacity="0.35" stroke-width="2"/>' for y in range(0, 180, 20))
big = (f'<g opacity="0">{fade(1.2, 0.5)}<animateTransform attributeName="transform" type="scale" values="0.55;1" '
       f'begin="1.2s" dur="0.9s" fill="freeze" additive="sum"/>{city("bg", 560, 315)}'
       f'<rect width="560" height="315" fill="none" stroke="#fff" stroke-width="6"/></g>')
save(SLUG, "upscale", f"""
<g transform="translate(90 180)">{city("sm", 320, 180)}{small_grid}
<rect width="320" height="180" fill="none" stroke="#fff" stroke-width="5"/></g>
{appear(label(250, 430, "1440p", 64, "display fa"), 0.3)}
{draw("M430 270 L560 420", 0.8, 0.4, "nf sw", 10)}{draw("M520 410 L560 420 L555 378", 1.1, 0.2, "nf sw", 10)}
<g transform="translate(380 460)">{big}</g>
{appear(label(660, 860, "4K", 80, "display fa2"), 2.0)}
""")

# 11. Thirty frames a second: a filmstrip ticking under a TV
frames = "".join(
    f'<rect x="{90 + i * 82}" y="700" width="70" height="90" rx="8" fill="#fff" fill-opacity="0.12" stroke="#fff" stroke-opacity="0.3" stroke-width="2"/>'
    f'<rect x="{90 + i * 82}" y="700" width="70" height="90" rx="8" class="fa" opacity="0">'
    f'<animate attributeName="opacity" values="0;1;0.25" keyTimes="0;0.1;1" begin="{i * 0.1}s" dur="1s" repeatCount="indefinite"/></rect>'
    for i in range(10))
stepped = (f'<g><animateTransform attributeName="transform" type="translate" calcMode="discrete" '
           f'values="{";".join(f"{x} 0" for x in range(-300, 720, 34))}" dur="1s" repeatCount="indefinite"/>'
           f'{place(0, 360, 0.5, car("f", PINK))}</g>')
save(SLUG, "thirty", f"""
{place(170, 120, 0.94, tv("f", city("fc", 700, 400) + stepped, 700, 400))}
<rect x="70" y="680" width="860" height="130" rx="16" fill="#0c0c10"/>{frames}
{badge(500, 905, "30 FRAMES A SECOND", 1.0)}
""")

# 12. The consoles can't run the city's simulation any faster
orbiters = "".join(
    f'<g><animateTransform attributeName="transform" type="rotate" from="{a} 500 470" to="{a + 360} 500 470" '
    f'dur="14s" repeatCount="indefinite"/><g transform="translate(500 {470 - 330})">'
    f'<g><animateTransform attributeName="transform" type="rotate" from="{-a}" to="{-a - 360}" dur="14s" repeatCount="indefinite"/>'
    f'{npc(c, s=0.6) if k % 2 == 0 else place(0, 0, 0.26, car(f"o{k}", c))}</g></g></g>'
    for k, (a, c) in enumerate(zip(range(0, 360, 45), [PINK, CYAN, SUN, "#8fe388", PINK, "#ff8a3d", CYAN, SUN])))
links = "".join(f'<line x1="500" y1="470" x2="{500 + 290 * math.cos(math.radians(a))}" y2="{470 + 290 * math.sin(math.radians(a))}" '
                f'stroke="{CYAN}" stroke-width="5" stroke-dasharray="12 14"><animate attributeName="stroke-dashoffset" '
                f'from="0" to="-52" dur="0.8s" repeatCount="indefinite"/></line>' for a in range(0, 360, 30))
save(SLUG, "simulation", f"""
<circle cx="500" cy="470" r="330" fill="none" stroke="#fff" stroke-opacity="0.15" stroke-width="80"/>
{links}
<g transform="translate(500 470)"><g>{chip(0.95)}</g></g>
<circle cx="500" cy="470" r="150" fill="#ff3b3b" opacity="0"><animate attributeName="opacity" values="0;0.35;0" dur="0.9s" repeatCount="indefinite"/></circle>
{orbiters}
{badge(500, 905, "CITY SIMULATION", 1.0)}
""")

# 13. The Pro: sharper picture and ray-traced shadows (blocky vs smooth)
blocky = "".join(f'<rect x="{-220 + i * 44}" y="{10 - (i % 3) * 12}" width="44" height="{44 + (i % 3) * 22}" fill="#000" opacity="0.85"/>'
                 for i in range(10))
save(SLUG, "pro", f"""
{place(170, 850, 1.0, console(pro=True))}
{sun(860, 140, 54)}
<g transform="translate(640 470)"><g transform="translate(0 0)">{blocky}</g>{place(0, 0, 0.62, car("p1", "#8a8a9a"))}</g>
{appear(f'<g transform="translate(640 780)"><ellipse cx="0" cy="22" rx="190" ry="26" fill="#000" opacity="0.75" filter="url(#soft)"/>{place(0, 0, 0.62, car("p2", PINK))}</g>', 1.0)}
{draw("M640 560 L640 680", 0.8, 0.3, "nf sw", 10)}{draw("M610 650 L640 685 L670 650", 1.0, 0.2, "nf sw", 10)}
{appear(label(640, 300, "RAY-TRACED SHADOWS", 50, "display fw"), 1.3)}
""")

# 14. Payoff: real light and real people, not more pixels
crowd = "".join(place(x, 392, 1, npc(c, s=0.55)) for x, c in ((140, PINK), (230, CYAN), (520, SUN), (610, "#8fe388")))
save(SLUG, "payoff", f"""
{place(110, 150, 1.12, tv("y", city("yc", 700, 400, rays=True) + crowd, 700, 400))}
{badge(500, 900, "REAL LIGHT, REAL PEOPLE", 1.0)}
""")
