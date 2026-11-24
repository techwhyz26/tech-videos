"""Illustrations for the 'ladybird-browser-engine' video. Run:  python tools/art_ladybird_browser_engine.py

Ladybird, a browser with its own engine built from scratch, entered alpha this week. The video shows
what a browser engine does (code -> tree -> boxes -> pixels) and that most browsers share Blink,
WebKit or Gecko. Browsers are drawn generically, no logos.

Objects (browser window, rendered page, ladybug, engine block, code sheet, laptop, donation jar) are
drawn once in their own coordinates and placed with place().
"""
import math

from artlib import appear, badge, bob, draw, fade, label, pop, save, shadow, waves

SLUG = "ladybird-browser-engine"
RED = "#e8283c"
BLUE = "#4d8dff"
GREEN = "#3ddc84"
INK = "#1c1c24"
CODE = {"tag": "#ff6b8a", "attr": "#ffd23f", "text": "#e9e9f0", "prop": "#7fd1ff"}


def place(x: float, y: float, s: float, inner: str) -> str:
    return f'<g transform="translate({x} {y}) scale({s})">{inner}</g>'


def spin(cx: float, cy: float, inner: str, dur: float = 2.0, rev: bool = False) -> str:
    to = -360 if rev else 360
    return (f'<g><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" '
            f'to="{to} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>{inner}</g>')


# --- objects ---------------------------------------------------------------------------------------

def gear(cx: float, cy: float, r: float, teeth: int, fill: str) -> str:
    pts = []
    for i in range(teeth * 2):
        a = i * math.pi / teeth
        rr = r if i % 2 == 0 else r * 0.8
        for da in (-0.3, 0.3):
            aa = a + da * math.pi / teeth
            pts.append(f"{cx + rr * math.cos(aa):.1f},{cy + rr * math.sin(aa):.1f}")
    return (f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="#000" stroke-opacity="0.35" stroke-width="3"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.42:.1f}" fill="#2a2a32"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.16:.1f}" fill="#c9c9d4"/>')


ENG_W, ENG_H = 400, 280


def engine(name: str, plate: str = "fa", speed: float = 2.0, bug: bool = False) -> str:
    """An engine block at (0,0), 400x280: cylinder heads on top, gears turning in a window, a nameplate."""
    heads = "".join(
        f'<rect x="{30 + i * 90}" y="-46" width="70" height="60" rx="12" fill="url(#metal)" stroke="#fff" stroke-opacity="0.25" stroke-width="3"/>'
        f'<rect x="{44 + i * 90}" y="-62" width="42" height="22" rx="6" fill="#8d8d99"/>'
        for i in range(4))
    g1 = spin(130, 120, gear(130, 120, 62, 10, "#d8d8e2"), speed)
    g2 = spin(238, 104, gear(238, 104, 44, 8, "#b4b4c0"), speed * 44 / 62, rev=True)
    g3 = spin(300, 160, gear(300, 160, 36, 7, "#d8d8e2"), speed * 36 / 62)
    nameplate = ""
    if name:
        w = len(name) * 30 + 60
        nameplate = (f'<rect x="{ENG_W / 2 - w / 2}" y="214" width="{w}" height="54" rx="10" class="{plate}"/>'
                     f'<text x="{ENG_W / 2}" y="256" font-size="44" font-weight="700" text-anchor="middle" '
                     f'class="display" style="fill:#0a0a0a">{name}</text>')
    stamp = place(342, 236, 0.32, ladybug()) if bug else ""
    return f"""{shadow(ENG_W / 2, ENG_H + 16, ENG_W * 0.55, 22)}
{heads}
<rect x="0" y="0" width="{ENG_W}" height="{ENG_H}" rx="30" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>
<rect x="12" y="10" width="{ENG_W - 24}" height="10" rx="5" fill="#fff" opacity="0.12"/>
<rect x="36" y="34" width="{ENG_W - 72}" height="168" rx="18" fill="#0b0b10"/>
<clipPath id="ew{name or 'x'}{int(speed * 10)}"><rect x="36" y="34" width="{ENG_W - 72}" height="168" rx="18"/></clipPath>
<g clip-path="url(#ew{name or 'x'}{int(speed * 10)})">{g1}{g2}{g3}</g>
<rect x="36" y="34" width="{ENG_W - 72}" height="168" rx="18" fill="none" stroke="#000" stroke-width="5" opacity="0.6"/>
{''.join(f'<circle cx="{x}" cy="{y}" r="7" fill="#9a9aa6"/>' for x in (18, ENG_W - 18) for y in (30, ENG_H - 30))}
{nameplate}{stamp}"""


def ladybug(walk: bool = True) -> str:
    """A ladybird beetle centred at (0,0), about 200 long, head pointing up."""
    legs = "".join(
        f'<path d="M{sx * 50} {y} l{sx * 52} {dy}" stroke="#111" stroke-width="10" stroke-linecap="round">'
        + (f'<animateTransform attributeName="transform" type="rotate" values="-12 {sx * 50} {y};12 {sx * 50} {y};-12 {sx * 50} {y}" '
           f'begin="{k * 0.1}s" dur="0.5s" repeatCount="indefinite"/>' if walk else "")
        + '</path>'
        for k, (sx, y, dy) in enumerate((s, y, dy) for s in (-1, 1) for y, dy in ((-30, -26), (6, 0), (42, 28))))
    spots = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#111"/>'
                    for x, y, r in ((-34, -18, 15), (34, -18, 15), (-40, 34, 13), (40, 34, 13), (-18, 72, 10), (18, 72, 10)))
    return f"""{legs}
<path d="M-24 -84 q-14 -30 -30 -34 M24 -84 q14 -30 30 -34" fill="none" stroke="#111" stroke-width="7" stroke-linecap="round"/>
<ellipse cx="0" cy="-72" rx="40" ry="30" fill="#111"/>
<circle cx="-18" cy="-78" r="9" fill="#fff"/><circle cx="18" cy="-78" r="9" fill="#fff"/>
<ellipse cx="0" cy="14" rx="74" ry="86" fill="{RED}"/>
<ellipse cx="-26" cy="-26" rx="24" ry="16" fill="#fff" opacity="0.3"/>
<line x1="0" y1="-60" x2="0" y2="100" stroke="#111" stroke-width="7"/>
{spots}"""


def page(w: float, h: float, begin: float | None = None) -> str:
    """A rendered web page in its own coords (0,0)-(w,h): header, headline, photo, text, button."""
    s = w / 600
    parts = [
        f'<rect x="0" y="0" width="{w}" height="{70 * s}" class="fa"/>'
        f'<circle cx="{40 * s}" cy="{35 * s}" r="{18 * s}" fill="#fff"/>'
        + "".join(f'<rect x="{(330 + i * 80) * s}" y="{28 * s}" width="{56 * s}" height="{14 * s}" rx="{7 * s}" fill="#fff" opacity="0.8"/>' for i in range(3)),
        f'<rect x="{40 * s}" y="{110 * s}" width="{420 * s}" height="{36 * s}" rx="{8 * s}" fill="{INK}"/>'
        f'<rect x="{40 * s}" y="{160 * s}" width="{300 * s}" height="{36 * s}" rx="{8 * s}" fill="{INK}"/>',
        f'<rect x="{40 * s}" y="{226 * s}" width="{520 * s}" height="{220 * s}" rx="{16 * s}" fill="#7fc4ff"/>'
        f'<circle cx="{450 * s}" cy="{290 * s}" r="{34 * s}" fill="#ffd23f"/>'
        f'<path d="M{40 * s} {446 * s} L{200 * s} {300 * s} L{300 * s} {380 * s} L{400 * s} {290 * s} L{560 * s} {446 * s} Z" fill="#2f9e5b"/>',
        "".join(f'<rect x="{40 * s}" y="{(480 + i * 34) * s}" width="{(520 - (i % 2) * 120) * s}" height="{16 * s}" rx="{8 * s}" fill="#b9b6ad"/>' for i in range(3)),
        f'<rect x="{40 * s}" y="{590 * s}" width="{200 * s}" height="{64 * s}" rx="{32 * s}" class="fa2"/>'
        f'<rect x="{80 * s}" y="{614 * s}" width="{120 * s}" height="{16 * s}" rx="{8 * s}" fill="#0a0a0a" opacity="0.6"/>',
    ]
    out = f'<rect x="0" y="0" width="{w}" height="{h}" fill="url(#paper)"/>'
    for i, p in enumerate(parts):
        out += appear(p, begin + i * 0.2, 0.25) if begin is not None else p
    return out


def browser(w: float, h: float, content: str = "", title: str = "Ladybird", url: str = "example.com",
            tab_cls: str = "fa") -> str:
    """A browser window at (0,0) size w x h. `content` is drawn in the page area (0,0 = its top-left)."""
    top = 112
    return f"""{shadow(w / 2, h + 18, w * 0.52, 24)}
<rect x="0" y="0" width="{w}" height="{h}" rx="26" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>
{''.join(f'<circle cx="{34 + i * 34}" cy="30" r="11" fill="{c}"/>' for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")))}
<path d="M140 52 v-22 q0 -14 14 -14 h{min(260, w - 200) - 28} q14 0 14 14 v22 z" fill="#3a3a46"/>
<circle cx="168" cy="34" r="9" class="{tab_cls}"/>
<text x="188" y="45" font-size="28" class="fw">{title}</text>
<rect x="20" y="62" width="{w - 40}" height="38" rx="19" fill="#0e0e14"/>
<text x="46" y="90" font-size="26" fill="#a9a9b8" style="fill:#a9a9b8">{url}</text>
<clipPath id="pg{int(w)}{int(h)}{title[:3]}"><rect x="12" y="{top}" width="{w - 24}" height="{h - top - 12}" rx="14"/></clipPath>
<g clip-path="url(#pg{int(w)}{int(h)}{title[:3]})"><g transform="translate(12 {top})">{content}</g></g>"""


def code_sheet(lines: list[list[tuple[str, str]]], begin: float = 0, title: str = "") -> str:
    """A sheet of paper-white code on a dark editor card at (0,0), 420 wide. Each line types in."""
    h = 90 + len(lines) * 52
    out = (f'{shadow(210, h + 14, 240, 20)}<rect x="0" y="0" width="420" height="{h}" rx="22" fill="url(#screen)" '
           f'stroke="#fff" stroke-opacity="0.25" stroke-width="4"/>'
           f'<rect x="0" y="0" width="420" height="58" rx="22" fill="#2a2a34"/><rect x="0" y="36" width="420" height="22" fill="#2a2a34"/>'
           f'<text x="30" y="42" font-size="30" font-weight="700" class="fa2">{title}</text>')
    for i, ln in enumerate(lines):
        x = 30
        segs = ""
        for kind, txt in ln:
            segs += f'<tspan style="fill:{CODE[kind]}">{txt}</tspan>'
        out += appear(f'<text x="{x}" y="{112 + i * 52}" font-size="32" font-family="monospace" xml:space="preserve">{segs}</text>',
                      begin + i * 0.25, 0.15)
    return out


HTML = [[("tag", "&lt;h1&gt;"), ("text", "News"), ("tag", "&lt;/h1&gt;")],
        [("tag", "&lt;img "), ("attr", "src"), ("text", "=pic"), ("tag", "&gt;")],
        [("tag", "&lt;p&gt;"), ("text", "Hello..."), ("tag", "&lt;/p&gt;")],
        [("tag", "&lt;button&gt;"), ("text", "Go"), ("tag", "&gt;")]]
CSS = [[("prop", "h1 "), ("text", "{")],
       [("prop", "  font"), ("text", ": 40px;")],
       [("prop", "  color"), ("text", ": navy;")],
       [("text", "}")]]


def laptop(screen: str) -> str:
    """A laptop at (0,0): screen 620x400, base below. `screen` drawn in screen coords."""
    return f"""{shadow(360, 470, 400, 26)}
<rect x="40" y="0" width="640" height="420" rx="24" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>
<rect x="58" y="18" width="604" height="384" rx="10" fill="url(#screen)"/>
<g transform="translate(58 18)">{screen}</g>
<path d="M0 430 h720 l-30 36 h-660 z" fill="url(#steel)"/>
<rect x="300" y="430" width="120" height="12" rx="6" fill="#8d8d99"/>"""


def jar() -> str:
    """A glass donation jar at (0,0) = bottom centre, 300 wide, 380 tall."""
    return f"""{shadow(0, 8, 190, 20)}
<rect x="-150" y="-380" width="300" height="380" rx="50" fill="#bfe3ff" fill-opacity="0.16" stroke="#fff" stroke-opacity="0.55" stroke-width="6"/>
<rect x="-120" y="-410" width="240" height="46" rx="14" fill="url(#steel)"/>
<rect x="-50" y="-398" width="100" height="14" rx="7" fill="#333"/>
<rect x="-120" y="-350" width="26" height="300" rx="13" fill="#fff" opacity="0.18"/>"""


def coin(cx: float, cy: float) -> str:
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="44" ry="18" fill="#c99a1e"/>'
            f'<ellipse cx="{cx}" cy="{cy - 8}" rx="44" ry="18" fill="#ffd23f"/>'
            f'<ellipse cx="{cx}" cy="{cy - 8}" rx="28" ry="10" fill="none" stroke="#c99a1e" stroke-width="4"/>')


def arrow(x1: float, y1: float, x2: float, y2: float, begin: float, cls: str = "sa") -> str:
    ang = math.atan2(y2 - y1, x2 - x1)
    hx1 = x2 - 34 * math.cos(ang - 0.5)
    hy1 = y2 - 34 * math.sin(ang - 0.5)
    hx2 = x2 - 34 * math.cos(ang + 0.5)
    hy2 = y2 - 34 * math.sin(ang + 0.5)
    return (draw(f"M{x1} {y1} L{x2} {y2}", begin, 0.4, f"nf {cls}", 12)
            + appear(f'<path d="M{hx1:.0f} {hy1:.0f} L{x2} {y2} L{hx2:.0f} {hy2:.0f}" class="nf {cls}" stroke-width="12" '
                     f'stroke-linecap="round" stroke-linejoin="round"/>', begin + 0.35, 0.1))


def belt(x1: float, y1: float, x2: float, y2: float, cls: str = "sa", begin: float = 0) -> str:
    """A cable carrying pulses from an engine up to a browser."""
    return (f'<path d="M{x1} {y1} C{x1} {(y1 + y2) / 2} {x2} {(y1 + y2) / 2} {x2} {y2}" fill="none" stroke="#3a3a46" stroke-width="16" stroke-linecap="round"/>'
            f'<path d="M{x1} {y1} C{x1} {(y1 + y2) / 2} {x2} {(y1 + y2) / 2} {x2} {y2}" fill="none" class="{cls}" stroke-width="8" '
            f'stroke-linecap="round" stroke-dasharray="18 26" opacity="0">{fade(begin)}'
            f'<animate attributeName="stroke-dashoffset" from="0" to="44" dur="0.5s" repeatCount="indefinite"/></path>')


# --- scenes ----------------------------------------------------------------------------------------

# 1. A new browser with its own engine underneath --------------------------------------------------
save(SLUG, "hook", f"""
{belt(500, 640, 500, 560, "sa", 0.6)}
{bob(place(130, 70, 1.0, browser(740, 500, page(716, 376, 0.2))), 8, 3.2)}
{place(300, 640, 1.0, engine("", speed=1.6, bug=True))}
{pop(830, 120, place(0, 0, 0.75, ladybug()), 0.9)}
{badge(500, 975, "ITS OWN ENGINE", 1.6)}
""")

# 2. What is a browser engine? The window lifts like a car bonnet -----------------------------------
save(SLUG, "question", f"""
{place(300, 600, 1.0, engine("", speed=1.4))}
<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -60" keyTimes="0;1" begin="0.3s" dur="0.8s" fill="freeze"/>
{place(170, 150, 0.9, browser(740, 480, page(716, 356)))}</g>
{pop(500, 520, '<circle r="78" class="fa2"/><text y="50" font-size="150" font-weight="700" text-anchor="middle" style="fill:#0a0a0a">?</text>', 1.1)}
""")

# 3. Code in, pixels out ---------------------------------------------------------------------------
pixels = "".join(
    f'<rect x="440" y="{330 + (i % 5) * 40}" width="28" height="28" rx="4" class="{"fa" if i % 3 else "fa2"}" opacity="0">'
    f'<animate attributeName="opacity" values="0;1;0" begin="{0.8 + i * 0.12:.2f}s" dur="1.0s" repeatCount="indefinite"/>'
    f'<animateTransform attributeName="transform" type="translate" from="0 0" to="90 0" begin="{0.8 + i * 0.12:.2f}s" dur="1.0s" repeatCount="indefinite"/></rect>'
    for i in range(10))
save(SLUG, "answer", f"""
{place(10, 250, 1.0, code_sheet(HTML, 0.2, "page.html"))}
{pixels}
{place(560, 150, 0.58, browser(740, 960, page(716, 836, 1.0)))}
{appear(label(220, 800, "Code", 64, "display fa2"), 0.3)}
{appear(label(775, 800, "Pixels", 64, "display fa"), 1.3)}
""")

# 4. Ladybird, out to test on Mac and Linux after about four years -----------------------------------
lb_screen = place(0, 0, 604 / 740, browser(740, 470, page(716, 346, 0.4)))
save(SLUG, "ladybird", f"""
{place(140, 200, 1.0, laptop(lb_screen))}
<g><animateTransform attributeName="transform" type="translate" values="0 0;-300 0;-300 0;0 0" keyTimes="0;0.45;0.55;1" dur="6s" repeatCount="indefinite"/>
<g transform="translate(760 140) rotate(-90) scale(0.55)">{ladybug()}</g></g>
{badge(500, 800, "ALPHA · MAC + LINUX", 0.8)}
{appear(label(500, 930, "About four years of work", 52), 1.4)}
""")

# 5. Every website arrives as plain text: HTML and CSS -----------------------------------------------
save(SLUG, "text", f"""
{bob(place(15, 220, 1.1, code_sheet(HTML, 0.3, "HTML")), 8, 3.4)}
{bob(place(530, 300, 1.08, code_sheet(CSS, 1.4, "CSS")), 8, 3.4, 0.6)}
{appear(label(246, 820, "the content", 56, "fa2"), 0.6)}
{appear(label(757, 900, "the look", 56, "fa"), 1.6)}
""")

# 6. The engine builds a tree of every heading, picture and button -----------------------------------
def node(x: float, y: float, text: str, cls: str, begin: float, w: float = 200) -> str:
    inner = (f'<rect x="{-w / 2}" y="-40" width="{w}" height="80" rx="20" class="{cls}"/>'
             f'<text y="14" font-size="38" font-weight="700" text-anchor="middle" font-family="monospace" style="fill:#0a0a0a">{text}</text>')
    return pop(x, y, inner, begin)


tree = [
    (500, 180, "html", "fw", 0.2, None),
    (290, 380, "head", "fw", 0.6, (500, 180)),
    (710, 380, "body", "fw", 0.6, (500, 180)),
    (150, 600, "h1", "fa", 1.0, (710, 380)),
    (390, 600, "img", "fa2", 1.2, (710, 380)),
    (620, 600, "p", "fa", 1.4, (710, 380)),
    (860, 600, "button", "fa2", 1.6, (710, 380)),
]
lines = "".join(draw(f"M{px} {py + 40} L{x} {y - 40}", b - 0.3, 0.3, "nf sw", 6) for x, y, _, _, b, p in tree if p for px, py in [p])
nodes = "".join(node(x, y, t, c, b, 210 if len(t) > 4 else 160) for x, y, t, c, b, _ in tree)
save(SLUG, "tree", f"""
{lines}{nodes}
{appear(label(500, 820, "A tree of every part", 56), 1.9)}
""")

# 7. Layout: the size and position of every box ----------------------------------------------------
def box(x, y, w, h, b, cls="sa"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" class="nf {cls}" stroke-width="6" stroke-dasharray="14 10" opacity="0">'
            f'{fade(b, 0.2)}<animate attributeName="stroke-dashoffset" from="0" to="-48" dur="1s" repeatCount="indefinite"/></rect>')


s = 716 / 600
wire = (f'<rect x="0" y="0" width="716" height="700" fill="#14141c"/>'
        + box(8, 8, 700, 70 * s - 8, 0.2)
        + box(40 * s, 105 * s, 430 * s, 96 * s, 0.5, "sa2")
        + box(40 * s, 222 * s, 520 * s, 228 * s, 0.8)
        + box(40 * s, 472 * s, 520 * s, 92 * s, 1.1, "sa2")
        + box(40 * s, 586 * s, 210 * s, 72 * s, 1.4))
measure = (draw(f"M{150 + 12 + 40 * s * 0.92} 655 L{150 + 12 + 560 * s * 0.92} 655", 1.7, 0.4, "nf sa2", 6)
           + appear(f'<text x="{150 + 12 + 300 * s * 0.92:.0f}" y="640" font-size="34" text-anchor="middle" class="fa2">574 px</text>', 2.0))
save(SLUG, "layout", f"""
{place(150, 60, 0.92, browser(740, 830, wire))}
{measure}
{badge(500, 940, "SIZE + POSITION", 2.2)}
""")

# 8. Paint the pixels, then JavaScript makes it move ------------------------------------------------
cols, rows = 14, 13
cw = 716 / cols
paint_cells = "".join(
    f'<rect x="{c * cw:.1f}" y="{r * cw:.1f}" width="{cw + 0.5:.1f}" height="{cw + 0.5:.1f}" fill="#14141c">'
    f'<animate attributeName="opacity" from="1" to="0" begin="{0.2 + (r * cols + c) * 0.008:.3f}s" dur="0.1s" fill="freeze"/></rect>'
    for r in range(rows) for c in range(cols))
moving = (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;300 0;0 0" begin="2s" dur="2s" repeatCount="indefinite"/>'
          f'<rect x="{40 * s}" y="{590 * s}" width="{200 * s}" height="{64 * s}" rx="{32 * s}" class="fa2" opacity="0">{fade(2.0, 0.1)}</rect></g>')
paint_page = page(716, 776) + paint_cells + f'<rect x="{40 * s - 4}" y="{590 * s - 4}" width="{200 * s + 8}" height="{64 * s + 8}" rx="40" fill="url(#paper)" opacity="0">{fade(2.0, 0.1)}</rect>' + moving
save(SLUG, "paint", f"""
{place(150, 40, 0.92, browser(740, 900, paint_page))}
{appear(f'<text x="500" y="960" font-size="64" text-anchor="middle" class="display fa">PAINT, THEN JAVASCRIPT</text>', 2.0)}
""")

# 9. Chrome, Edge, Brave and Vivaldi all share Blink ------------------------------------------------
mini_pg = page(716, 300)
spots = ((255, 140, "Chrome"), (745, 140, "Edge"), (255, 390, "Brave"), (745, 390, "Vivaldi"))
def start_page(name: str, h: float = 300) -> str:
    """A browser's own start page: big name over a search box."""
    return (f'<rect x="0" y="0" width="716" height="{h}" fill="url(#paper)"/>'
            f'<text x="358" y="125" font-size="96" font-weight="700" text-anchor="middle" style="fill:{INK}">{name}</text>'
            f'<rect x="108" y="165" width="500" height="64" rx="32" fill="#fff" stroke="#c9c5ba" stroke-width="5"/>'
            f'<circle cx="150" cy="197" r="14" fill="none" stroke="#9a978f" stroke-width="5"/>')


wins = "".join(
    pop(x, y, place(-207, -106, 0.56, browser(740, 380, start_page(name), name, f"{name.lower()}.app", "fa2")), 0.3 + i * 0.25)
    for i, (x, y, name) in enumerate(spots))
cables = "".join(belt(x, y + 90, 500 + (x - 500) * 0.35, 600, "sa", 1.3) for x, y, _ in spots)
save(SLUG, "blink", f"""
{cables}
{wins}
{place(270, 600, 1.15, engine("BLINK", speed=1.2))}
""")

# 10. Safari on WebKit, Firefox on Gecko ------------------------------------------------------------
save(SLUG, "others", f"""
{belt(255, 420, 255, 540, "sa2", 0.8)}{belt(745, 420, 745, 540, "sa", 1.0)}
{pop(255, 260, place(-222, -150, 0.6, browser(740, 520, start_page("Safari", 396), "Safari", "safari.app", "fa2")), 0.2)}
{pop(745, 260, place(-222, -150, 0.6, browser(740, 520, start_page("Firefox", 396), "Firefox", "firefox.app", "fa")), 0.5)}
{place(55, 560, 1.0, engine("WEBKIT", "fa2", 1.7))}
{place(545, 560, 1.0, engine("GECKO", "fa", 2.3))}
""")

# 11. Ladybird wrote its own engine from scratch -------------------------------------------------
def part_chip(t: str, c: str) -> str:
    w = len(t) * 26 + 60
    return (f'<rect x="{-w / 2}" y="-40" width="{w}" height="80" rx="20" class="{c}"/>'
            f'<text y="14" font-size="40" font-weight="700" text-anchor="middle" style="fill:#0a0a0a">{t}</text>')


parts = [("HTML", 115, 150, "fa"), ("CSS", 300, 150, "fa2"), ("Layout", 510, 150, "fa2"), ("JavaScript", 805, 150, "fa")]
feeds = "".join(belt(x, 190, 500 + (x - 500) * 0.4, 380, "sa2" if i % 2 else "sa", 0.5 + i * 0.3) for i, (_, x, _, _) in enumerate(parts))
chips = "".join(pop(x, y, part_chip(t, c), 0.2 + i * 0.3) for i, (t, x, y, c) in enumerate(parts))
save(SLUG, "scratch", f"""
<g opacity="0">{fade(1.6)}{waves(500, 560, "sa", 3, 160, 420, 1.8, 6, 0.5)}</g>
{feeds}
{place(220, 380, 1.4, engine("", speed=1.5, bug=True))}
{chips}
{badge(500, 940, "BUILT FROM SCRATCH", 2.0)}
""")

# 12. Paid for by donations and sponsors, not search deals ---------------------------------------
drops = "".join(
    f'<g opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.85;1" begin="{i * 0.45}s" dur="1.35s" repeatCount="indefinite"/>'
    f'<animateTransform attributeName="transform" type="translate" from="0 -560" to="0 -170" begin="{i * 0.45}s" dur="1.35s" repeatCount="indefinite"/>'
    f'{coin(dx, 0)}</g>'
    for i, dx in enumerate((-30, 20, -10)))
pile = "".join(coin(dx, -30 - k * 20) for k, dx in enumerate((-60, 40, -20, 50, -40, 10, -10)))
jar_scene = jar() + pile + drops + place(0, -250, 0.6, ladybug(False))
save(SLUG, "donations", f"""
{place(500, 840, 1.35, jar_scene)}
{appear(label(500, 950, "Donations, not search deals", 54), 0.8)}
""")

# 13. Still rough: some sites break, it can crash --------------------------------------------------
broken = (page(716, 600)
          + '<path d="M300 0 L340 160 L270 240 L380 380 L330 600" fill="none" stroke="#111" stroke-width="7"/>'
          + '<path d="M340 160 L520 120 M270 240 L80 300 M380 380 L600 460" fill="none" stroke="#111" stroke-width="5"/>'
          + '<rect x="330" y="0" width="386" height="600" fill="#14141c" opacity="0"><animate attributeName="opacity" values="0;0.85;0;0.85" begin="0.9s" dur="0.6s" fill="freeze"/></rect>')
save(SLUG, "rough", f"""
<g><animateTransform attributeName="transform" type="translate" values="0 0;-8 0;8 0;-4 0;0 0" begin="0.8s" dur="0.4s" repeatCount="2"/>
{place(130, 90, 1.0, browser(740, 720, broken, "Ladybird", "some-site.com"))}</g>
{pop(760, 180, '<circle r="76" fill="#ff3b4a"/><text y="40" font-size="120" font-weight="700" text-anchor="middle" style="fill:#fff">!</text>', 1.2)}
{badge(500, 935, "ALPHA: EXPECT CRASHES", 1.6)}
""")

# 14. Payoff: the app is a frame, the engine does the work, and now there is a new one ---------------
save(SLUG, "payoff", f"""
{place(20, 110, 0.52, engine("BLINK", speed=1.2))}
{place(260, 110, 0.52, engine("WEBKIT", "fa2", speed=1.7))}
{place(500, 110, 0.52, engine("GECKO", speed=2.3))}
<g opacity="0">{fade(1.0)}<animateTransform attributeName="transform" type="translate" values="0 80;0 0" begin="1.0s" dur="0.5s" fill="freeze"/>
{waves(844, 183, "sa", 3, 60, 150, 1.6, 6, 0.7)}
{place(740, 110, 0.52, engine("NEW", "fa2", speed=1.0, bug=True))}</g>
{place(278, 380, 0.6, browser(740, 560, page(716, 436, 0.3), "Ladybird", "ladybird.org"))}
{appear(label(500, 840, "The app is the frame.", 54), 1.6)}
{appear(label(500, 915, "The engine does the work.", 54, "fa"), 2.1)}
""")
