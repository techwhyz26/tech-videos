"""Illustrations for the 'iphone-duo-folding-glass' video. Run:  python tools/art_iphone_duo_folding_glass.py

Main objects, each drawn once in its own coordinates and placed with place():
  duo()    - the folding phone, front view; its right half unfolds around the hinge
  stack()  - a side cut through the folding screen: cover, glass, display, titanium plate
  slab()   - one screen layer as a solid 3D slab (exploded view)
  hinge()  - the hinge bar and its many small parts
"""
import math

from artlib import appear, badge, bob, draw, fade, label, pop, save, shadow

SLUG = "iphone-duo-folding-glass"
RED = "#ff4d4d"
GREEN = "#3ddc84"
GLASS = "#d9f2ff"
TI = "#b4b4c2"
SPLINE = 'calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"'

OW, OH = 620, 440   # open phone size in its own coordinates
HW = OW / 2          # hinge x


def place(x: float, y: float, s: float, inner: str) -> str:
    return f'<g transform="translate({x} {y}) scale({s})">{inner}</g>'


# ---------------------------------------------------------------------------------------------
# The phone
# ---------------------------------------------------------------------------------------------
ICON_COLS = ["fa", "fa2", "#ffd34d", "#4cd964", "#7aa7ff", "#ff9f43", "fw"]


def icons(x0: float, y0: float, seed: int) -> str:
    out = []
    for r in range(5):
        for c in range(4):
            col = ICON_COLS[(r * 4 + c + seed) % len(ICON_COLS)]
            fill = f'class="{col}"' if not col.startswith("#") else f'fill="{col}"'
            op = 0.55 if col == "fw" else 0.92
            out.append(f'<rect x="{x0 + 26 + c * 66}" y="{y0 + 40 + r * 70}" width="50" height="50" rx="13" {fill} opacity="{op}"/>')
    return "".join(out)


def inner_half(side: str) -> str:
    """Left or right half of the open phone (clipped from the full open phone), in open-phone coordinates."""
    x = 0 if side == "l" else HW
    cid = "duoL" if side == "l" else "duoR"
    cam = f'<circle cx="{OW - 60}" cy="40" r="9" fill="#000"/>' if side == "r" else ""
    return (f'<clipPath id="{cid}"><rect x="{x}" y="-10" width="{HW}" height="{OH + 20}"/></clipPath>'
            f'<g clip-path="url(#{cid})"><rect x="0" y="0" width="{OW}" height="{OH}" rx="34" fill="url(#metal)" '
            f'stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>'
            f'<rect x="14" y="14" width="{OW - 28}" height="{OH - 28}" rx="22" fill="url(#screen)"/>'
            f'{icons(x + (8 if side == "l" else -6), 4, 0 if side == "l" else 3)}{cam}'
            f'<rect x="30" y="20" width="{OW - 60}" height="8" rx="4" fill="#fff" opacity="0.1"/></g>')


def outer_face() -> str:
    """The outside screen you see when the phone is shut (covers the left half)."""
    bars = "".join(f'<rect x="{60}" y="{300 + k * 30}" width="{190 - k * 50}" height="14" rx="7" fill="#fff" opacity="0.18"/>' for k in range(3))
    return (f'<rect x="0" y="0" width="{HW}" height="{OH}" rx="34" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>'
            f'<rect x="0" y="0" width="22" height="{OH}" rx="11" fill="#2a2a33"/>'
            f'<rect x="14" y="14" width="{HW - 28}" height="{OH - 28}" rx="22" fill="url(#screen)"/>'
            f'<circle cx="{HW / 2}" cy="40" r="9" fill="#000"/>'
            f'<text x="{HW / 2}" y="170" font-size="92" text-anchor="middle" class="display fw">10:09</text>'
            f'<rect x="44" y="210" width="{HW - 88}" height="64" rx="18" class="fa" opacity="0.8"/>{bars}'
            f'<rect x="20" y="8" width="{HW - 40}" height="8" rx="4" fill="#fff" opacity="0.12"/>')


def crease(op: float = 0.12, extra: str = "") -> str:
    return (f'<line x1="{HW}" y1="16" x2="{HW}" y2="{OH - 16}" stroke="#fff" stroke-width="6" opacity="{op}">{extra}</line>')


def keys(states: list, times: list) -> tuple[str, str, str]:
    """Fold states (+1 open, -1 shut) -> scale values for the right half and the outer face."""
    e = 0.002
    right = ";".join(f"{max(s, e):.3f} 1" for s in states)
    outer = ";".join(f"{max(-s, e):.3f} 1" for s in states)
    return right, outer, ";".join(f"{t:.3f}" for t in times)


def duo(states=(1,), times=(0,), dur: float = 1, begin: float = 0, repeat: bool = False,
        crease_svg: str | None = None, over: str = "", shadow_on: bool = True) -> str:
    """The folding phone at (0,0), open size 620x440. `states`/`times` animate the fold."""
    rep = 'repeatCount="indefinite"' if repeat else 'fill="freeze"'
    r, o, kt = keys(list(states), list(times))
    r0, o0 = r.split(";")[0], o.split(";")[0]
    anim = len(states) > 1
    ra = f'<animateTransform attributeName="transform" type="scale" values="{r}" keyTimes="{kt}" begin="{begin}s" dur="{dur}s" {rep}/>' if anim else ""
    oa = f'<animateTransform attributeName="transform" type="scale" values="{o}" keyTimes="{kt}" begin="{begin}s" dur="{dur}s" {rep}/>' if anim else ""
    cr = crease() if crease_svg is None else crease_svg
    sh = shadow(OW / 2, OH + 24, OW * 0.5, 22) if shadow_on else ""
    return f"""{sh}
{inner_half("l")}
<g transform="translate({HW} 0)"><g transform="scale({r0.replace(' ', ' ')})">{ra}<g transform="translate({-HW} 0)">{inner_half("r")}</g></g></g>
<rect x="{HW - 3}" y="0" width="6" height="{OH}" fill="#000" opacity="0.5"/>
{cr}{over}
<g transform="translate({HW} 0)"><g transform="scale({o0})">{oa}<g transform="translate({-HW} 0)">{outer_face()}</g></g></g>"""


# open/shut loop used by several scenes
LOOP_S = (1, 1, -1, -1, 1)
LOOP_T = (0, 0.15, 0.45, 0.65, 1)


# ---------------------------------------------------------------------------------------------
# The cut through the screen
# ---------------------------------------------------------------------------------------------
DUO_LAYERS = [  # (thickness, stroke style, bent-state slide)
    (24, 'class="sa" opacity="0.95"', -26),
    (30, f'stroke="{GLASS}" opacity="0.9"', -9),
    (34, 'stroke="#15151d"', 9),
    (28, f'stroke="{TI}"', 26),
]


def arc(cx: float, y: float, L: float, lift: float, slide: float) -> str:
    x0, x1 = cx - L / 2 + slide, cx + L / 2 - slide
    return f"M{x0:.1f} {y - lift:.1f} Q{cx:.1f} {y + lift:.1f} {x1:.1f} {y - lift:.1f}"


def stack(cx: float, cy: float, L: float = 760, lift: float = 90, dur: float = 2.6, begin: float = 0,
          layers=None, gap: float = 10, glue: str = "", bend: bool = True, highlight: int | None = None,
          pixels: bool = True, dent: float = 0, slide_scale: float = 1.0) -> str:
    """Side view of the layered screen bending back and forth. glue: '' (hidden) or a class for the glue lines."""
    layers = layers or DUO_LAYERS
    total = sum(t for t, _, _ in layers) + gap * (len(layers) - 1)
    ys, y = [], cy - total / 2
    for t, _, _ in layers:
        ys.append(y + t / 2)
        y += t + gap

    def anim(y, slide, extra_lift=0):
        flat = arc(cx, y, L, 0.001, 0)
        if not bend:
            return flat, ""
        bent = arc(cx, y, L, lift + extra_lift, slide * slide_scale)
        return flat, (f'<animate attributeName="d" values="{flat};{bent};{flat}" keyTimes="0;0.5;1" {SPLINE} '
                      f'begin="{begin}s" dur="{dur}s" repeatCount="indefinite"/>')

    out = [shadow(cx, cy + total / 2 + 40, L * 0.5, 22, 0.45)]
    for i, ((t, style, slide), y) in enumerate(zip(layers, ys)):
        d, a = anim(y, slide)
        out.append(f'<path d="{d}" fill="none" {style} stroke-width="{t}">{a}</path>')
        if pixels and i == 2 and layers is DUO_LAYERS:
            out.append(f'<path d="{d}" fill="none" class="sa2" stroke-width="{t * 0.4}" stroke-dasharray="8 9" opacity="0.85">{a}</path>')
            out.append(f'<path d="{d}" fill="none" class="sa" stroke-width="{t * 0.4}" stroke-dasharray="8 9" stroke-dashoffset="8" opacity="0.85">{a}</path>')
        if i == 1 and layers is DUO_LAYERS:  # glass shine
            out.append(f'<path d="{d}" fill="none" stroke="#fff" stroke-width="5" opacity="0.7" transform="translate(0 -8)">{a}</path>')
        if highlight == i:
            out.append(f'<path d="{d}" fill="none" class="sa2" stroke-width="{t + 16}" opacity="0.35" filter="url(#glow)">{a}'
                       f'<animate attributeName="opacity" values="0.15;0.6;0.15" dur="1.1s" repeatCount="indefinite"/></path>')
        if glue and i < len(layers) - 1:
            gy = y + t / 2 + gap / 2
            gd, ga = anim(gy, (slide + layers[i + 1][2]) / 2)
            out.append(f'<path d="{gd}" fill="none" class="{glue}" stroke-width="{gap - 2}" stroke-dasharray="14 8" filter="url(#glow)">{ga}</path>')
    return "".join(out)


# ---------------------------------------------------------------------------------------------
# One layer as a solid slab (for the exploded view)
# ---------------------------------------------------------------------------------------------
SKEW = 'transform="matrix(1 0 -0.2857 1 0 0)"'


def slab(top: str, side: str, t: float = 24, face: str = "") -> str:
    """A slab centred at (0,0): top face is a parallelogram, 600 wide and 140 deep."""
    return (f'<polygon points="-300,70 260,70 260,{70 + t} -300,{70 + t}" {side}/>'
            f'<polygon points="260,70 300,-70 300,{-70 + t} 260,{70 + t}" {side} opacity="0.8"/>'
            f'<g {SKEW}><rect x="-280" y="-70" width="560" height="140" {top}/>{face}</g>')


def pixel_face() -> str:
    return "".join(
        f'<rect x="{-262 + i * 26}" y="{-56 + j * 24}" width="18" height="14" rx="3" class="{("fa", "fa2", "fw")[(i + j) % 3]}" opacity="0.75"/>'
        for i in range(21) for j in range(5))


# ---------------------------------------------------------------------------------------------
# Hinge parts
# ---------------------------------------------------------------------------------------------
def gear(r: float, teeth: int = 10, fill: str = 'fill="url(#steel)"') -> str:
    pts = []
    for k in range(teeth):
        a0 = 2 * math.pi * k / teeth
        for da, rr in ((-0.32, r * 0.8), (-0.18, r), (0.18, r), (0.32, r * 0.8)):
            a = a0 + da * 2 * math.pi / teeth
            pts.append(f"{rr * math.cos(a):.1f},{rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" {fill}/><circle r="{r * 0.3:.1f}" fill="#22222a"/>'


def spin(inner: str, dur: float, rev: bool = False) -> str:
    to = -360 if rev else 360
    return f'<g><animateTransform attributeName="transform" type="rotate" from="0" to="{to}" dur="{dur}s" repeatCount="indefinite"/>{inner}</g>'


SPRING = '<polyline points="-50,0 -40,-16 -28,16 -16,-16 -4,16 8,-16 20,16 32,-16 44,0" fill="none" stroke="#cfcfda" stroke-width="7" stroke-linejoin="round"/>'
PIN = '<rect x="-46" y="-9" width="92" height="18" rx="9" fill="url(#steel)"/><rect x="-46" y="-9" width="14" height="18" rx="6" fill="#8a8a96"/>'
LINK = ('<rect x="-52" y="-22" width="104" height="44" rx="22" fill="#9a9aa8"/>'
        '<circle cx="-30" cy="0" r="9" fill="#22222a"/><circle cx="30" cy="0" r="9" fill="#22222a"/>')
SCREW = ('<circle r="20" fill="url(#steel)"/><path d="M-11 0 h22 M0 -11 v22" stroke="#55555f" stroke-width="5" stroke-linecap="round"/>')


def hinge(w: float = 720) -> str:
    """Hinge bar centred at (0,0)."""
    knuckles = "".join(
        f'<rect x="{-w / 2 + 20 + k * 68}" y="-34" width="40" height="68" rx="10" fill="#7d7d8a"/>'
        for k in range(int((w - 40) / 68) + 1))
    return (f'{shadow(0, 70, w * 0.5, 18)}<rect x="{-w / 2}" y="-38" width="{w}" height="76" rx="38" fill="url(#steel)"/>'
            f'{knuckles}<rect x="{-w / 2 + 20}" y="-28" width="{w - 40}" height="10" rx="5" fill="#fff" opacity="0.6"/>')


# =============================================================================================
# 1. Apple's first folding iPhone bends its screen in half every time you open it.
S = 1.3
save(SLUG, "hook", f"""
<g><animateTransform attributeName="transform" type="translate" values="{HW * S / 2} 0;{HW * S / 2} 0;0 0" keyTimes="0;0.4;1" begin="0.4s" dur="1.6s" fill="freeze"/>
{place(97, 150, S, duo((-1, -1, 1), (0, 0.4, 1), 1.6, 0.4, crease_svg=crease(0.12, '<animate attributeName="opacity" values="0.1;0.9;0.1" begin="2.1s" dur="1.2s" repeatCount="indefinite"/>')))}
</g>
<line x1="500" y1="130" x2="500" y2="740" class="sa" stroke-width="14" opacity="0" filter="url(#glow)">
  <animate attributeName="opacity" values="0;0.8;0" begin="2.1s" dur="1.2s" repeatCount="indefinite"/></line>
{badge(500, 880, "IPHONE DUO", 2.0)}
""")

# 2. So how does glass fold without snapping? -----------------------------------------------------
flat = arc(500, 430, 760, 0.001, 0)
bent = arc(500, 430, 760, 120, 0)
crack = "M500 380 L488 410 L512 432 L494 462 L508 490"
shards = "".join(pop(x, y, f'<polygon points="0,-16 14,8 -12,12" fill="{GLASS}" opacity="0.85" transform="rotate({rot})"/>', 1.3 + k * 0.08)
                 for k, (x, y, rot) in enumerate(((450, 520, 20), (560, 540, -30), (520, 600, 60), (470, 590, -10))))
save(SLUG, "question", f"""
{shadow(500, 560, 380, 22, 0.4)}
<path d="{flat}" fill="none" stroke="{GLASS}" stroke-width="44" opacity="0.85">
  <animate attributeName="d" values="{flat};{bent}" begin="0.2s" dur="1.0s" fill="freeze" calcMode="spline" keySplines="0.4 0 1 1"/></path>
<path d="{flat}" fill="none" stroke="#fff" stroke-width="6" opacity="0.8" transform="translate(0 -12)">
  <animate attributeName="d" values="{flat};{bent}" begin="0.2s" dur="1.0s" fill="freeze" calcMode="spline" keySplines="0.4 0 1 1"/></path>
{draw(crack, 1.15, 0.2, f'nf', 9, f'stroke="{RED}"')}
{shards}
{pop(500, 210, '<circle r="95" class="fa2"/><text y="58" font-size="180" font-weight="700" text-anchor="middle" style="fill:#0a0a0a">?</text>', 1.6)}
{appear(label(500, 800, "Glass, folded in half?", 52), 0.4)}
""")

# 3. Because the screen isn't one sheet. It's a stack of layers that can slide. --------------------
SL = [  # top style, side style, face, final y
    ('class="fa" opacity="0.6"', 'class="fa" opacity="0.95"', "", 190),
    (f'fill="{GLASS}" opacity="0.55"', f'fill="{GLASS}" opacity="0.9"',
     '<rect x="-200" y="-56" width="60" height="112" fill="#fff" opacity="0.35"/>', 340),
    ('fill="#101018"', 'fill="#24242e"', pixel_face(), 490),
    ('fill="url(#steel)"', f'fill="#8f8f9c"', "", 640),
]
slabs = []
for k, (top, side, face, fy) in reversed(list(enumerate(SL))):
    start = 400 + k * 30
    slabs.append(f'<g transform="translate(500 {start})"><animateTransform attributeName="transform" type="translate" '
                 f'values="500 {start};500 {start};500 {fy}" keyTimes="0;0.3;1" begin="0s" dur="1.4s" fill="freeze" {SPLINE.replace(";0.45 0 0.55 1", ";0.3 0 0.2 1")}/>'
                 f'{bob(slab(top, side, 24, face), 6, 2.8, k * 0.3)}</g>')
save(SLUG, "layers", f"""
{shadow(500, 760, 330, 22, 0.45)}
{''.join(slabs)}
{badge(500, 900, "NOT ONE SHEET", 1.5)}
""")

# 4. On top sits a polymer cover, up to forty percent stiffer than others use, Apple says. ---------
finger = ('<path d="M-46 -420 L-46 -40 Q-46 10 0 10 Q46 10 46 -40 L46 -420 Z" fill="#f2c6a0"/>'
          '<path d="M-28 -60 Q-28 -16 0 -16 Q28 -16 28 -60 L28 -86 Q0 -96 -28 -86 Z" fill="#fbe3d0"/>'
          '<rect x="-46" y="-420" width="92" height="40" fill="#e0b08c"/>')
cy4 = 560
top4 = cy4 - (24 + 30 + 34 + 28 + 30) / 2
dent0 = arc(500, top4 + 12, 760, 0.001, 0)
dent1 = f"M120 {top4 + 12} L430 {top4 + 12} Q500 {top4 + 26} 570 {top4 + 12} L880 {top4 + 12}"
dent0b = f"M120 {top4 + 12} L430 {top4 + 12} Q500 {top4 + 12} 570 {top4 + 12} L880 {top4 + 12}"
K = 1.8  # the cut is drawn taller than life so the layers read on a phone


def tall(cy: float, inner: str, k: float = K) -> str:
    return f'<g transform="translate(0 {cy}) scale(1 {k}) translate(0 {-cy})">{inner}</g>'


save(SLUG, "cover", f"""
{tall(cy4, f'''{stack(500, cy4, bend=False, layers=[(24, 'stroke="none"', 0)] + DUO_LAYERS[1:], gap=10)}
<path d="{dent0b}" fill="none" class="sa" stroke-width="24">
  <animate attributeName="d" values="{dent0b};{dent1};{dent0b}" keyTimes="0;0.5;1" begin="0.6s" dur="1.8s" repeatCount="indefinite"/></path>
<path d="{dent0b}" fill="none" class="sa" stroke-width="44" opacity="0.3" filter="url(#glow)">
  <animate attributeName="d" values="{dent0b};{dent1};{dent0b}" keyTimes="0;0.5;1" begin="0.6s" dur="1.8s" repeatCount="indefinite"/></path>''')}
<g transform="translate(500 {cy4 + (top4 - cy4) * K - 4:.0f})"><g>
  <animateTransform attributeName="transform" type="translate" values="0 -60;0 -60;0 12;0 -60" keyTimes="0;0.0001;0.5;1" begin="0.6s" dur="1.8s" repeatCount="indefinite"/>
  {finger}</g></g>
{appear(label(500, 790, "Polymer cover", 50, "fa"), 0.3)}
{badge(500, 900, "UP TO 40% STIFFER", 1.0)}
""")

# 5. Underneath sits a titanium plate. ------------------------------------------------------------
cy5 = 500
tot5 = 24 + 30 + 34 + 28 + 30
ti_y = cy5 + tot5 / 2 - 14
save(SLUG, "titanium", f"""
{tall(cy5, stack(500, cy5, bend=False, layers=DUO_LAYERS[:3] + [(28, 'stroke="none"', 0)], gap=10) + f'''
<g opacity="0">{fade(0.3, 0.3)}<animateTransform attributeName="transform" type="translate" values="900 0;0 0" begin="0.3s" dur="0.8s" fill="freeze" calcMode="spline" keySplines="0.2 0 0.2 1"/>
  <rect x="120" y="{ti_y - 14}" width="760" height="28" fill="url(#steel)"/>
  <rect x="120" y="{ti_y - 14}" width="760" height="6" fill="#fff" opacity="0.7"/>
  <rect x="112" y="{ti_y - 22}" width="776" height="44" rx="8" class="nf sa" stroke-width="6" opacity="0" filter="url(#glow)">
    <animate attributeName="opacity" values="0;1;0.3;1" begin="1.1s" dur="1.2s" fill="freeze"/></rect>
</g>''')}
{pop(500, 800, '<rect x="-70" y="-70" width="140" height="140" rx="20" fill="url(#steel)"/><text y="26" font-size="76" font-weight="700" text-anchor="middle" style="fill:#2a2a33">Ti</text>', 1.2)}
{appear(label(500, 940, "Titanium plate", 52, "fa"), 1.0)}
""")

# 6. But here's the part most people miss. The glue between the layers lets them slide. ------------
arrows = "".join(
    f'<path d="M{x} {y} l{dx} 0 M{x + dx} {y} l{-dx * 0.4:.0f} -12 M{x + dx} {y} l{-dx * 0.4:.0f} 12" class="nf sw" stroke-width="7" stroke-linecap="round" opacity="0">'
    f'<animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;0.3;0.5;0.7;1" dur="2.6s" repeatCount="indefinite"/></path>'
    for x, y, dx in ((150, 200, -40), (850, 200, 40), (200, 420, 40), (800, 420, -40)))
save(SLUG, "glue", f"""
{tall(480, stack(500, 480, glue="sa2", dur=2.6, lift=110), 1.6)}
{arrows}
{appear(label(500, 760, "Glue that lets layers shift", 50, "fa2"), 0.5)}
""")

# 7. Bend a stack of paper and the pages slide. Glue them solid, and it fights back. ---------------
PAPER = [(14, 'stroke="#f6f3ea"', s) for s in (-24, -12, 0, 12, 24)]
GLUED = [(14, 'stroke="#f6f3ea"', 0) for _ in range(5)]
crack7 = "M740 470 L726 500 L752 520 L732 556"
save(SLUG, "paper", f"""
{stack(265, 470, L=380, lift=80, dur=2.4, layers=PAPER, gap=5, pixels=False)}
{stack(740, 470, L=380, lift=22, dur=2.4, layers=GLUED, gap=5, pixels=False, glue="sa2")}
<path d="{crack7}" class="nf" stroke="{RED}" stroke-width="8" stroke-linecap="round" opacity="0">
  <animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;0.35;0.5;0.65;1" dur="2.4s" repeatCount="indefinite"/></path>
{appear(label(265, 680, "Pages slide", 48, "fa"), 0.4)}
{appear(label(740, 680, "Glued: it fights", 48, "fa2"), 0.9)}
{pop(740, 330, f'<circle r="40" fill="{RED}"/><text y="22" font-size="64" font-weight="700" text-anchor="middle">!</text>', 1.3)}
{pop(265, 300, f'<circle r="40" fill="{GREEN}"/><path d="M-18 0 l12 14 l24 -28" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>', 1.0)}
""")

# 8. The hinge under all of that is built from more than one hundred parts. ------------------------
parts = [
    (170, 210, spin(gear(52, 12), 3)), (330, 230, PIN), (500, 200, spin(gear(40, 10), 2.4, True)),
    (660, 230, SPRING), (830, 210, spin(gear(52, 12), 3, True)),
    (200, 330, LINK), (400, 320, SCREW), (600, 320, SCREW), (800, 330, LINK),
    (180, 590, SCREW), (340, 600, SPRING), (500, 610, spin(gear(46, 11), 2.8)), (660, 600, PIN), (820, 590, SCREW),
    (260, 710, PIN), (500, 720, LINK), (740, 710, SPRING),
]
save(SLUG, "hinge", f"""
{''.join(pop(x, y, p, 0.2 + k * 0.07) for k, (x, y, p) in enumerate(parts))}
<g transform="translate(500 460)">{bob(hinge(760), 4, 2.4)}</g>
{badge(500, 880, "100+ PARTS", 1.6)}
""")

# 9. Shut, it has a five point four inch screen. Open, seven point six inches. -------------------
def measure(x0, y0, x1, y1, b):
    return draw(f"M{x0} {y0} L{x1} {y1}", b, 0.6, "nf sa", 8, 'filter="url(#glow)"')


sc = 0.88
save(SLUG, "sizes", f"""
{place(40, 230, sc, duo((-1,), (0,)))}
{place(372, 230, sc, duo((-1, -1, 1), (0, 0.3, 1), 1.2, 0.2))}
{measure(40 + 30, 230 + 30, 40 + (HW - 30) * sc, 230 + (OH - 30) * sc, 0.4)}
{measure(372 + 30, 230 + 30, 372 + (OW - 30) * sc, 230 + (OH - 30) * sc, 1.5)}
{appear('<text x="176" y="720" font-size="96" text-anchor="middle" class="display fw">5.4"</text>', 0.5)}
{appear('<text x="645" y="720" font-size="96" text-anchor="middle" class="display fa">7.6"</text>', 1.6)}
{appear(label(176, 800, "Shut", 46), 0.5)}
{appear(label(645, 800, "Open", 46, "fa"), 1.6)}
""")

# 10. The crease is still there. A nano-texture finish cuts reflections, so it's harder to see. -----
tex = "".join(f'<circle cx="{18 + i * 16}" cy="{18 + j * 16}" r="2.4" fill="#fff" opacity="0.16"/>'
              for i in range(37) for j in range(26))
glare = (f'<defs><linearGradient id="glr" x1="0" y1="0" x2="1" y2="0">'
         f'<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="1"/>'
         f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>'
         f'<rect x="{HW - 70}" y="16" width="140" height="{OH - 32}" fill="url(#glr)" opacity="0.85">'
         f'<animate attributeName="opacity" values="0.85;0.2" begin="1.6s" dur="0.8s" fill="freeze"/></rect>'
         f'<g opacity="0">{fade(1.5, 0.6)}<clipPath id="txc"><rect x="14" y="14" width="{OW - 28}" height="{OH - 28}" rx="22"/></clipPath>'
         f'<g clip-path="url(#txc)">{tex}</g></g>')
lamp = ('<path d="M-60 0 L60 0 L36 -70 L-36 -70 Z" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="3"/>'
        '<rect x="-6" y="-200" width="12" height="130" fill="#55555f"/>'
        '<ellipse cx="0" cy="4" rx="40" ry="12" fill="#fff6c8" filter="url(#glow)"/>')
rays = "".join(
    f'<line x1="{140 + dx}" y1="200" x2="{x2}" y2="{y2}" stroke="#fff6c8" stroke-width="5" stroke-dasharray="18 14" opacity="0.6">'
    f'<animate attributeName="stroke-dashoffset" from="0" to="-32" dur="0.5s" repeatCount="indefinite"/>'
    f'<animate attributeName="opacity" values="0.6;0.15" begin="1.6s" dur="0.8s" fill="freeze"/></line>'
    for dx, x2, y2 in ((-20, 470, 420), (0, 500, 520), (20, 530, 620)))
save(SLUG, "crease", f"""
{place(140, 210, 1, lamp)}
{rays}
{place(220, 300, 0.95, duo(crease_svg=crease(0.35), over=glare))}
{appear(label(500, 800, "Nano-texture finish", 50, "fa"), 1.6)}
""")

# 11. One tester folded it eleven thousand five hundred times, and the crease got more noticeable. --
counts = ["500", "5,000", "10,000", "11,500"]
counter = "".join(
    f'<text x="500" y="205" font-size="110" text-anchor="middle" class="display fa" opacity="0">'
    f'<set attributeName="opacity" to="1" begin="{k * 0.9}s"/>'
    + (f'<set attributeName="opacity" to="0" begin="{(k + 1) * 0.9}s"/>' if k < 3 else "")
    + f'{c}</text>' for k, c in enumerate(counts))
save(SLUG, "foldtest", f"""
<rect x="290" y="90" width="420" height="150" rx="24" fill="#08080c" stroke="#fff" stroke-opacity="0.25" stroke-width="4"/>
{counter}
<rect x="150" y="740" width="700" height="44" rx="14" fill="url(#metal)" stroke="#fff" stroke-opacity="0.2" stroke-width="3"/>
<rect x="180" y="784" width="40" height="40" rx="6" fill="#141418"/><rect x="780" y="784" width="40" height="40" rx="6" fill="#141418"/>
<rect x="180" y="430" width="40" height="320" rx="10" fill="#6a6a76"/><rect x="164" y="450" width="56" height="70" rx="10" class="fa2"/>
{place(210, 300, 0.94, duo(LOOP_S, LOOP_T, 0.9, 0, True, shadow_on=False,
       crease_svg=crease(0.05, '<animate attributeName="opacity" values="0.05;0.9" dur="3.4s" fill="freeze"/>')))}
{badge(500, 900, "CREASE SHOWS MORE", 3.0, "fa2")}
""")

# 12. But the hinge stayed smooth, and opened just like day one. -------------------------------------
ring = (f'<path d="M-140 0 A140 140 0 1 1 0 140" class="nf sa" stroke-width="10" stroke-linecap="round"/>'
        f'<path d="M0 140 l26 -22 M0 140 l26 22" class="nf sa" stroke-width="10" stroke-linecap="round"/>')
save(SLUG, "smooth", f"""
{place(190, 250, 1.0, duo(LOOP_S, LOOP_T, 2.6, 0, True))}
<g transform="translate({190 + HW} 470)" opacity="0.55">{spin(ring, 2.6)}</g>
{pop(800, 220, f'<circle r="56" fill="{GREEN}"/><path d="M-24 0 l16 18 l32 -36" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>', 0.8)}
{badge(500, 880, "STILL SMOOTH", 1.2)}
""")

# 13. Apple hasn't said how many folds the screen is rated for. ----------------------------------
rows = "".join(f'<rect x="40" y="{110 + k * 56}" width="{260 - k * 40}" height="18" rx="9" fill="#c9c5ba"/>'
               f'<circle cx="330" cy="{119 + k * 56}" r="14" fill="{GREEN}"/>' for k in range(3))
sheet = (f'<rect x="0" y="0" width="380" height="460" rx="24" fill="url(#paper)"/>'
         f'<rect x="40" y="40" width="200" height="30" rx="10" fill="#9b968a"/>{rows}'
         f'<line x1="40" y1="300" x2="340" y2="300" stroke="#c9c5ba" stroke-width="4"/>'
         f'<text x="40" y="380" font-size="54" style="fill:#222" font-weight="700">FOLDS:</text>'
         f'<text x="300" y="392" font-size="110" text-anchor="middle" font-weight="700" class="fa2">?'
         f'<animate attributeName="opacity" values="1;0.25;1" dur="1s" repeatCount="indefinite"/></text>')
save(SLUG, "rating", f"""
{place(40, 300, 0.7, duo((-1, -1, 1), (0, 0.3, 1), 1.0, 0.2))}
{shadow(760, 790, 200, 20)}
{pop(760, 530, f'<g transform="translate(-190 -230) rotate(3 190 230)">{sheet}</g>', 0.6)}
{appear(label(500, 900, "Apple hasn't said", 50, "fa2"), 1.2)}
""")

# 14. It starts at one thousand nine hundred ninety nine dollars. ---------------------------------
tag = (f'<circle r="12" fill="#ddd"/><line x1="0" y1="0" x2="0" y2="160" stroke="#ddd" stroke-width="5"/>'
       f'<g transform="translate(0 160)"><path d="M-40 0 L40 0 L140 30 L140 200 L-140 200 L-140 30 Z" class="fa"/>'
       f'<circle cx="0" cy="22" r="12" class="fb"/>'
       f'<text x="0" y="150" font-size="100" text-anchor="middle" class="display" style="fill:#0a0a0a">$1,999</text></g>')
save(SLUG, "price", f"""
{place(30, 190, 0.95, duo((-1, -1, 1), (0, 0.3, 1), 1.0, 0.2))}
<g transform="translate(810 300)"><g><animateTransform attributeName="transform" type="rotate" values="-6;6;-6" dur="2s" repeatCount="indefinite"/>
  {appear(tag, 0.8)}</g></g>
{appear(label(500, 900, "Starting price", 50), 1.0)}
""")

# 15. So the glass doesn't fight the fold. Its layers slide, every time you open it. ----------------
save(SLUG, "payoff", f"""
{place(190, 40, 1.0, duo(LOOP_S, LOOP_T, 3.0, 0, True))}
{tall(720, stack(500, 720, L=720, lift=70, dur=3.0, glue="sa2"), 1.3)}
{badge(500, 930, "LAYERS THAT SHIFT", 1.0)}
""")
