"""Illustrations for the 'qr-code-damage' video. Run:  python tools/art_qr.py"""
import random

import qrcode

from artlib import appear, badge, bob, chip, fade, label, pop, save, shadow

SLUG = "qr-code-damage"

_q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, border=0, box_size=1)
_q.add_data("Torn, and it still works.")
_q.make(fit=True)
M = _q.get_matrix()
N = len(M)

X, Y, S = 140, 70, 720  # the big white card
PAD = S * 0.05
CELL = (S - 2 * PAD) / N
P = lambda fx, fy: (X + fx * S, Y + fy * S)  # fraction of the card -> canvas point
pts = lambda p: " ".join(f"{a:.0f},{b:.0f}" for a, b in p)


def is_finder(r: int, c: int) -> bool:
    return (r < 7 and c < 7) or (r < 7 and c >= N - 7) or (r >= N - 7 and c < 7)


def modules(pred=lambda r, c: True, x=X, y=Y, size=S) -> str:
    """SVG path data for the dark modules that satisfy `pred`."""
    pad = size * 0.05
    cell = (size - 2 * pad) / N
    d = []
    for r in range(N):
        for c in range(N):
            if M[r][c] and pred(r, c):
                d.append(f"M{x + pad + c * cell:.1f} {y + pad + r * cell:.1f}h{cell + .4:.1f}v{cell + .4:.1f}h-{cell + .4:.1f}z")
    return "".join(d)


def card(x=X, y=Y, size=S) -> str:
    return f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size * 0.06:.0f}" fill="url(#paper)"/>'


def code(pred=lambda r, c: True, fill="#111", x=X, y=Y, size=S) -> str:
    return f'{card(x, y, size)}<path d="{modules(pred, x, y, size)}" fill="{fill}"/>'


def mini(x: float, y: float, size: float) -> str:
    return code(x=x, y=y, size=size)


GROUND = shadow(500, Y + S + 22, 330)

# The torn-off corner, as fractions of the card
jag = [P(*f) for f in [(1, .3), (.883, .35), (.842, .467), (.717, .5), (.683, .633), (.55, .675), (.525, .8), (.4, .85), (.333, 1)]]
main = [P(0, 0), P(1, 0)] + jag + [P(0, 1)]
piece = jag + [P(1, 1)]
RIP_DEFS = f"""<defs>
  <clipPath id="rip-main"><polygon points="{pts(main)}"/></clipPath>
  <clipPath id="rip-piece"><polygon points="{pts(piece)}"/></clipPath>
</defs>"""
px, py = P(.75, .75)

# 1. A real QR code gets a corner torn off, then still scans -----------------------------------
save(SLUG, "rip", f"""{RIP_DEFS}
{GROUND}
<g clip-path="url(#rip-main)">{code()}</g>
<g>
  <animateTransform attributeName="transform" type="translate" values="0 0;18 12;170 150" keyTimes="0;0.25;1" begin="0.9s" dur="0.8s" fill="freeze"/>
  <animate attributeName="opacity" from="1" to="0.35" begin="1.4s" dur="0.5s" fill="freeze"/>
  <g>
    <animateTransform attributeName="transform" type="rotate" from="0 {px:.0f} {py:.0f}" to="22 {px:.0f} {py:.0f}" begin="0.9s" dur="0.8s" fill="freeze"/>
    <g clip-path="url(#rip-piece)">{code()}</g>
  </g>
</g>
<polyline points="{pts(jag)}" class="nf sa2" stroke-width="9" stroke-linejoin="round" opacity="0" filter="url(#glow)">{fade(0.7, 0.2)}</polyline>
<rect x="{X - 30}" y="{Y}" width="{S + 60}" height="12" rx="6" class="fa" opacity="0" filter="url(#glow)">
  <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.9;1" begin="2s" dur="0.9s" fill="freeze"/>
  <animate attributeName="y" from="{Y}" to="{Y + S - 12}" begin="2s" dur="0.9s" fill="freeze"/>
</rect>
{badge(500, 925, "STILL SCANS", 2.8)}
""")

# 2. How does a damaged code still know what it says? -------------------------------------------
q = lambda x, y, rot, b: pop(x, y, f'<text y="70" font-size="230" text-anchor="middle" class="display fa2" transform="rotate({rot})" filter="url(#glow)">?</text>', b)
br = lambda x, y, dx, dy: f'<path d="M{x} {y + dy * 110} L{x} {y} L{x + dx * 110} {y}" class="nf sa" stroke-width="14" stroke-linecap="round"/>'
save(SLUG, "confused", f"""{RIP_DEFS}
{GROUND}
<g clip-path="url(#rip-main)">{code()}</g>
<polyline points="{pts(jag)}" class="nf sa2" stroke-width="9" stroke-linejoin="round"/>
<g>
  <animate attributeName="opacity" values="1;0.25;1" dur="0.9s" repeatCount="indefinite"/>
  {br(X - 40, Y - 40, 1, 1)}{br(X + S + 40, Y - 40, -1, 1)}{br(X - 40, Y + S + 40, 1, -1)}{br(X + S + 40, Y + S + 40, -1, -1)}
</g>
{q(760, 640, 12, 0.4)}{q(650, 760, -10, 0.7)}{q(840, 800, 22, 1.0)}
""")

# 3. Every code carries a backup of itself ------------------------------------------------------
rnd = random.Random(7)
backup = {(r, c) for r in range(N) for c in range(N) if not is_finder(r, c) and rnd.random() < 0.55}
save(SLUG, "backup", f"""
{GROUND}
{code()}
<path d="{modules(lambda r, c: (r, c) in backup)}" class="fa" opacity="0">
  {fade(0.5, 0.7)}<animate attributeName="opacity" values="1;0.55;1" begin="1.4s" dur="1.2s" repeatCount="indefinite"/>
</path>
{chip(300, 925, "Message", 0.3, "fw")}
{chip(690, 925, "Backup copy", 0.9, "fa")}
""")

# 4. Car parts factory: boxes with QR labels pass under a scanner ------------------------------
boxes = "".join(f"""
<g transform="translate(-400 0)">
  <animateTransform attributeName="transform" type="translate" from="-400 0" to="1100 0" begin="{i * 2.1}s" dur="6.3s" repeatCount="indefinite"/>
  <rect x="0" y="420" width="320" height="280" rx="12" fill="#c79a66"/>
  <rect x="0" y="420" width="320" height="46" fill="#b08552"/>
  <rect x="140" y="420" width="40" height="280" fill="#e6c79a" opacity="0.55"/>
  <rect x="0" y="640" width="320" height="60" rx="12" fill="#000" opacity="0.12"/>
  {mini(85, 500, 150)}
</g>""" for i in range(3))
rollers = "".join(
    f'<g><animateTransform attributeName="transform" type="rotate" from="0 {x} 733" to="360 {x} 733" dur="1.2s" repeatCount="indefinite"/>'
    f'<circle cx="{x}" cy="733" r="22" fill="#6a6a76"/><line x1="{x - 15}" y1="733" x2="{x + 15}" y2="733" stroke="#111" stroke-width="5"/></g>'
    for x in range(10, 1000, 122))
save(SLUG, "factory", f"""
<text x="500" y="110" font-size="130" text-anchor="middle" class="display fa">1994 · JAPAN</text>
{shadow(500, 790, 520, 30)}
<rect x="476" y="150" width="48" height="130" fill="url(#metal)"/>
<rect x="400" y="270" width="200" height="66" rx="14" class="fa2"/>
<polygon points="440,336 560,336 690,430 310,430" class="fa">
  <animate attributeName="opacity" values="0.1;0.6;0.1" dur="0.7s" repeatCount="indefinite"/>
</polygon>
{boxes}
<rect x="-60" y="704" width="1120" height="58" rx="29" fill="url(#metal)"/>
{rollers}
{appear(label(500, 900, "Tracking parts on the factory line", 48), 0.4)}
""")

# 5. Dirt, oil and scratches land on the label ---------------------------------------------------
splat = lambda cx, cy, r, fill, b: pop(cx, cy, (
    f'<circle r="{r}" fill="{fill}"/><circle cx="{r * .8}" cy="{-r * .5}" r="{r * .45}" fill="{fill}"/>'
    f'<circle cx="{-r * .7}" cy="{r * .6}" r="{r * .5}" fill="{fill}"/><circle cx="{r * .2}" cy="{r * .95}" r="{r * .3}" fill="{fill}"/>'
    f'<circle cx="{-r * .3}" cy="{-r * .35}" r="{r * .18}" fill="#fff" opacity="0.18"/>'), b)
scratch = lambda a, b_, t: (f'<path d="M{a[0]:.0f} {a[1]:.0f} L{b_[0]:.0f} {b_[1]:.0f}" class="nf" stroke="#f6f4ef" stroke-width="18" stroke-linecap="round" '
                            f'pathLength="1" stroke-dasharray="1" stroke-dashoffset="1">'
                            f'<animate attributeName="stroke-dashoffset" from="1" to="0" begin="{t}s" dur="0.25s" fill="freeze"/></path>')
save(SLUG, "dirty", f"""
{GROUND}
{code()}
{splat(*P(.27, .68), 74, "#5d4020", 0.4)}
{splat(*P(.73, .25), 58, "#5d4020", 0.6)}
{splat(*P(.66, .75), 84, "#16161a", 0.9)}
{scratch(P(.1, .3), P(.45, .17), 1.4)}
{scratch(P(.17, .45), P(.53, .58), 1.6)}
{scratch(P(.53, .9), P(.9, .68), 1.8)}
{chip(215, 925, "Dirt", 0.4, "fa2")}
{chip(465, 925, "Oil", 0.9, "fa2")}
{chip(760, 925, "Scratches", 1.4, "fa2")}
""")

# 6. Thirty percent of the code disappears -------------------------------------------------------
edge = round(N * 0.46)
gone = lambda r, c: r >= edge and c >= edge
gx, gy = X + PAD + edge * CELL, Y + PAD + edge * CELL
gw = (N - edge) * CELL
outline = lambda cls, extra="": (f'<rect x="{gx - 10:.0f}" y="{gy - 10:.0f}" width="{gw + 20:.0f}" height="{gw + 20:.0f}" rx="12" '
                                 f'class="nf {cls}" stroke-width="9" {extra}>')
save(SLUG, "missing", f"""
{GROUND}
{card()}
<path d="{modules(lambda r, c: not gone(r, c))}" fill="#111"/>
<path d="{modules(gone)}" fill="#111"><animate attributeName="opacity" from="1" to="0.05" begin="0.5s" dur="0.6s" fill="freeze"/></path>
{outline("sa2", 'stroke-dasharray="24 16" opacity="0"')}{fade(0.5)}</rect>
{appear('<text x="500" y="960" font-size="170" text-anchor="middle" class="display fa2">30% GONE</text>', 1.0)}
""")

# 7. The phone rebuilds the missing part ---------------------------------------------------------
bands = "".join(
    f'<path d="{modules(lambda r, c, i=i: gone(r, c) and (c - edge) // 2 == i)}" class="fa" opacity="0">{fade(0.4 + i * 0.14, 0.2)}</path>'
    for i in range((N - edge + 1) // 2))
save(SLUG, "repair", f"""
{GROUND}
{card()}
<path d="{modules(lambda r, c: not gone(r, c))}" fill="#111"/>
<path d="{modules(gone)}" fill="#111" opacity="0.05"/>
{bands}
{outline("sa", 'filter="url(#glow)"')}</rect>
{badge(500, 925, "REBUILT WITH MATH", 1.9)}
""")

# 8. A scratched CD keeps playing ----------------------------------------------------------------
note = lambda x, b: (f'<text x="{x}" y="330" font-size="150" class="fa" opacity="0">♪'
                     f'<animate attributeName="y" from="380" to="90" begin="{b}s" dur="2s" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="0;1;0" begin="{b}s" dur="2s" repeatCount="indefinite"/></text>')
save(SLUG, "cd", f"""
<g>
  <animateTransform attributeName="transform" type="rotate" from="0 500 480" to="360 500 480" dur="3s" repeatCount="indefinite"/>
  <circle cx="500" cy="480" r="390" fill="url(#steel)"/>
  <path d="M500 480 L890 480 A390 390 0 0 0 776 204 Z" class="fa" opacity="0.5"/>
  <path d="M500 480 L110 480 A390 390 0 0 0 224 756 Z" class="fa2" opacity="0.5"/>
  {''.join(f'<circle cx="500" cy="480" r="{r}" class="nf" stroke="#000" stroke-opacity="0.12" stroke-width="3"/>' for r in (355, 305, 255, 205, 155))}
  <path d="M300 250 L350 335 L326 380 L406 510" class="nf" stroke="#2a2a2a" stroke-width="11" stroke-linecap="round"/>
  <circle cx="500" cy="480" r="118" fill="#f1f1f5"/>
  <circle cx="500" cy="480" r="48" class="fb"/>
</g>
{note(860, 0)}{note(60, 0.7)}{note(900, 1.3)}
{appear(label(500, 950, "Scratched, still plays", 52), 0.5)}
""")

# 9. The three corner squares are not data -------------------------------------------------------
fsize = CELL * 7
corners = [(X + PAD, Y + PAD), (X + S - PAD - fsize, Y + PAD), (X + PAD, Y + S - PAD - fsize)]
rings = "".join(
    f'<rect x="{x - 16:.0f}" y="{y - 16:.0f}" width="{fsize + 32:.0f}" height="{fsize + 32:.0f}" rx="14" class="nf sa2" stroke-width="10" filter="url(#glow)">'
    f'<animate attributeName="opacity" values="1;0.15;1" begin="{i * 0.3}s" dur="1s" repeatCount="indefinite"/></rect>'
    for i, (x, y) in enumerate(corners))
save(SLUG, "finder", f"""
{GROUND}
{card()}
<path d="{modules(lambda r, c: not is_finder(r, c))}" fill="#111" opacity="0.14"/>
<path d="{modules(is_finder)}" class="fa"/>
{rings}
{appear(label(500, 925, "They only say which way is up", 50), 0.6)}
""")

# 10. Scans from any angle -----------------------------------------------------------------------
QS = 520
qx = qy = 470 - QS / 2
save(SLUG, "angle", f"""
{br(70, 40, 1, 1)}{br(870, 40, -1, 1)}{br(70, 900, 1, -1)}{br(870, 900, -1, -1)}
<g>
  <animateTransform attributeName="transform" type="rotate"
    values="0 470 470;90 470 470;90 470 470;205 470 470;205 470 470;360 470 470"
    keyTimes="0;0.2;0.35;0.55;0.7;1" dur="5s" repeatCount="indefinite"/>
  <rect x="{qx}" y="{qy}" width="{QS}" height="{QS}" rx="30" fill="url(#paper)"/>
  <path d="{modules(lambda r, c: not is_finder(r, c), qx, qy, QS)}" fill="#111"/>
  <path d="{modules(is_finder, qx, qy, QS)}" class="fa"/>
</g>
{badge(470, 990, "READS IT ANYWAY", 0.9)}
""")

# 11. Four toughness levels, from 7% to 30% ------------------------------------------------------
def level(x: float, y: float, name: str, pct: int, begin: float, best: bool = False) -> str:
    size = 340
    e = N - round(N * (pct / 100) ** 0.5)
    hole = lambda r, c: r >= e and c >= e
    ring = (f'<rect x="{x - 12}" y="{y - 12}" width="{size + 24}" height="{size + 24}" rx="30" class="nf sa" stroke-width="10" filter="url(#glow)"/>'
            if best else "")
    inner = (f'{card(x, y, size)}<path d="{modules(lambda r, c: not hole(r, c), x, y, size)}" fill="#111"/>'
             f'<path d="{modules(hole, x, y, size)}" class="fa2" opacity="0.35"/>{ring}'
             f'<text x="{x + size / 2}" y="{y + size + 68}" font-size="62" text-anchor="middle" class="display {"fa" if best else "fw"}">{name} · {pct}%</text>')
    return appear(inner, begin, 0.3)


save(SLUG, "levels", f"""
{level(110, 20, "LOW", 7, 0.2)}
{level(550, 20, "MEDIUM", 15, 0.7)}
{level(110, 500, "HIGH", 25, 1.2)}
{level(550, 500, "MAX", 30, 1.7, True)}
""")

# 12. Free to use, so it is everywhere -----------------------------------------------------------
menu = (f'<g transform="rotate(-5)"><rect x="-150" y="-200" width="300" height="400" rx="18" fill="url(#paper)"/>'
        f'<text y="-130" font-size="64" text-anchor="middle" class="display" style="fill:#111">MENU</text>'
        f'{"".join(f"<rect x=-110 y={-95 + i * 30} width={220 - i * 40} height=12 rx=6 fill=#c9c5ba />".replace("=", chr(61) + chr(34)).replace(" ", chr(34) + " ", 5) for i in range(0))}'
        f'<rect x="-110" y="-95" width="220" height="12" rx="6" fill="#c9c5ba"/><rect x="-110" y="-65" width="170" height="12" rx="6" fill="#c9c5ba"/>'
        f'{mini(-75, -25, 150)}</g>')
ticket = (f'<g transform="rotate(4)"><rect x="-190" y="-110" width="380" height="220" rx="20" class="fa2"/>'
          f'<circle cx="-190" cy="0" r="30" class="fb"/><circle cx="190" cy="0" r="30" class="fb"/>'
          f'<text x="-70" y="-20" font-size="50" text-anchor="middle" class="display" style="fill:#111">ADMIT</text>'
          f'<text x="-70" y="40" font-size="50" text-anchor="middle" class="display" style="fill:#111">ONE</text>'
          f'{mini(30, -75, 150)}</g>')
terminal = (f'<rect x="-140" y="-190" width="280" height="380" rx="30" fill="url(#metal)" stroke="#fff" stroke-opacity="0.25" stroke-width="4"/>'
            f'<rect x="-110" y="-160" width="220" height="200" rx="14" fill="#fff"/>{mini(-80, -140, 160)}'
            f'{"".join(f"<circle cx={chr(34)}{-66 + i * 66}{chr(34)} cy={chr(34)}{84 + j * 52}{chr(34)} r={chr(34)}18{chr(34)} fill={chr(34)}#6a6a76{chr(34)}/>" for i in range(3) for j in range(2))}')
sign = (f'<rect x="-150" y="-200" width="300" height="400" rx="24" fill="#fff" fill-opacity="0.08" stroke="#fff" stroke-opacity="0.35" stroke-width="5"/>'
        f'<path d="M-70 -110 a100 100 0 0 1 140 0 M-42 -82 a60 60 0 0 1 84 0" class="nf sa" stroke-width="14" stroke-linecap="round"/>'
        f'<circle cx="0" cy="-52" r="12" class="fa"/>'
        f'<text y="5" font-size="46" text-anchor="middle">Free Wi-Fi</text>{mini(-75, 30, 150)}')
save(SLUG, "everywhere", f"""
{pop(250, 240, menu, 0.2)}
{pop(730, 190, ticket, 0.6)}
{pop(260, 690, terminal, 1.0)}
{pop(740, 620, sign, 1.4)}
{badge(500, 960, "FREE TO USE", 2.0)}
""")

# 13. A logo in the middle is just damage --------------------------------------------------------
lx, ly = P(.5, .5)
save(SLUG, "logo", f"""
{GROUND}
{code()}
{pop(lx, ly, '<circle r="135" fill="#f6f4ef"/><circle r="112" class="fa"/><text y="18" font-size="56" font-weight="700" text-anchor="middle" style="fill:#0a0a0a">LOGO</text>', 0.5)}
<circle cx="{lx}" cy="{ly}" r="156" class="nf sa2" stroke-width="10" opacity="0" filter="url(#glow)">
  <animate attributeName="opacity" values="0;1;0.2;1" begin="1.3s" dur="1.2s" fill="freeze"/>
</circle>
{appear(label(500, 925, "Covered squares = damage", 52, "fa2"), 1.3)}
""")
