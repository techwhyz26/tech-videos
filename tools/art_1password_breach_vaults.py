"""Illustrations for the '1password-breach-vaults' video. Run:  python tools/art_1password_breach_vaults.py

Objects (server rack, safe, hooded attacker, laptop, key, phone) are drawn once in their own
coordinates and placed with translate+scale, so every scene reuses them at any size.
"""
from artlib import appear, badge, bob, draw, fade, label, phone, pop, save, shadow, waves

SLUG = "1password-breach-vaults"
RED = "#ff4d4d"
GREEN = "#3ddc84"
SECRET = "A3-K7QW2M-9XRT4B-LJ8VN-C5HPD-W2YF6-ZQ3MS"   # 34 letters and numbers, made-up example


def place(x: float, y: float, s: float, inner: str) -> str:
    return f'<g transform="translate({x} {y}) scale({s})">{inner}</g>'


def blink(dur: float = 0.8, begin: float = 0, low: float = 0.2, high: float = 1) -> str:
    return (f'<animate attributeName="opacity" values="{high};{low};{high}" begin="{begin}s" dur="{dur}s" '
            f'repeatCount="indefinite"/>')


def red_x(r: float = 60) -> str:
    return (f'<circle r="{r}" fill="{RED}"/><path d="M{-r * .45} {-r * .45} L{r * .45} {r * .45} M{r * .45} {-r * .45} '
            f'L{-r * .45} {r * .45}" stroke="#fff" stroke-width="{r * .22}" stroke-linecap="round"/>')


def tick(r: float = 44) -> str:
    return (f'<circle r="{r}" fill="{GREEN}"/><path d="M{-r * .45} 0 l{r * .3} {r * .35} l{r * .6} {-r * .7}" fill="none" '
            f'stroke="#fff" stroke-width="{r * .25}" stroke-linecap="round" stroke-linejoin="round"/>')


# ---- objects ---------------------------------------------------------------------------------

def server(alert: bool = False) -> str:
    """A server rack at (0,0), 300 wide and 560 tall (plus feet)."""
    units = []
    for i in range(6):
        y = 60 + i * 80
        led = RED if alert else GREEN
        units.append(
            f'<rect x="22" y="{y}" width="256" height="64" rx="10" fill="#15151b"/>'
            f'<rect x="22" y="{y}" width="256" height="8" rx="4" fill="#fff" opacity="0.06"/>'
            + "".join(f'<rect x="{40 + k * 12}" y="{y + 14}" width="6" height="36" rx="3" fill="#3a3a46"/>' for k in range(5))
            + "".join(f'<rect x="{112 + k * 26}" y="{y + 18}" width="20" height="28" rx="4" fill="#2a2a33" stroke="#4a4a56" stroke-width="2"/>' for k in range(4))
            + f'<circle cx="238" cy="{y + 24}" r="7" fill="{led}">{blink(0.5 + i * 0.13, i * 0.1)}</circle>'
            + f'<circle cx="258" cy="{y + 24}" r="7" class="fa">{blink(0.9, i * 0.2 + 0.3)}</circle>'
            + f'<rect x="228" y="{y + 40}" width="38" height="8" rx="4" fill="#3a3a46"/>')
    return (f'{shadow(150, 590, 190, 20)}'
            f'<rect x="20" y="556" width="50" height="22" rx="6" fill="#141418"/><rect x="230" y="556" width="50" height="22" rx="6" fill="#141418"/>'
            f'<rect x="0" y="0" width="300" height="565" rx="22" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>'
            f'<rect x="12" y="10" width="276" height="10" rx="5" fill="#fff" opacity="0.14"/>'
            f'<rect x="22" y="28" width="256" height="20" rx="6" fill="#0c0c10"/>'
            + "".join(units))


def vault(spin: float = 6, shake: bool = False) -> str:
    """A steel safe at (0,0), 420 wide and about 445 tall including feet."""
    cx, cy = 210, 175
    ticks_ = "".join(
        f'<line x1="{cx}" y1="{cy - 62}" x2="{cx}" y2="{cy - (50 if k % 3 else 44)}" stroke="#d6d6de" stroke-width="5" '
        f'transform="rotate({k * 30} {cx} {cy})"/>' for k in range(12))
    dial = (f'<circle cx="{cx}" cy="{cy}" r="82" fill="#22222a"/>'
            f'<g><animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};200 {cx} {cy};80 {cx} {cy};320 {cx} {cy};0 {cx} {cy}" '
            f'dur="{spin}s" repeatCount="indefinite"/>'
            f'<circle cx="{cx}" cy="{cy}" r="66" fill="url(#metal)"/>{ticks_}'
            f'<circle cx="{cx}" cy="{cy}" r="26" fill="#55555f"/><rect x="{cx - 6}" y="{cy - 40}" width="12" height="26" rx="5" fill="#d6d6de"/></g>'
            f'<path d="M{cx - 14} {cy - 98} h28 l-14 18 z" class="fa"/>')
    hx, hy = 210, 310
    handle = (f'<g>'
              + "".join(f'<line x1="{hx}" y1="{hy}" x2="{hx}" y2="{hy - 58}" stroke="#4a4a56" stroke-width="16" stroke-linecap="round" '
                        f'transform="rotate({a} {hx} {hy})"/><circle cx="{hx}" cy="{hy - 62}" r="14" fill="#6a6a76" transform="rotate({a} {hx} {hy})"/>'
                        for a in (0, 120, 240))
              + f'<circle cx="{hx}" cy="{hy}" r="22" fill="#6a6a76"/></g>')
    bolts = "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="#8d8d99"/>' for x in (64, 356) for y in (64, 360))
    body = (f'<rect x="38" y="418" width="64" height="26" rx="6" fill="#141418"/><rect x="318" y="418" width="64" height="26" rx="6" fill="#141418"/>'
            f'<rect x="0" y="0" width="420" height="425" rx="34" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>'
            f'<rect x="34" y="34" width="352" height="357" rx="22" fill="url(#steel)"/>'
            f'<rect x="50" y="50" width="320" height="325" rx="16" fill="none" stroke="#000" stroke-opacity="0.15" stroke-width="6"/>'
            f'<rect x="60" y="44" width="220" height="10" rx="5" fill="#fff" opacity="0.6"/>'
            f'<rect x="14" y="90" width="28" height="64" rx="8" fill="#9a9aa6"/><rect x="14" y="270" width="28" height="64" rx="8" fill="#9a9aa6"/>'
            f'{bolts}{dial}{handle}')
    if shake:
        body = (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;-6 0;6 0;-4 0;0 0;0 0" '
                f'keyTimes="0;0.06;0.12;0.18;0.24;1" dur="1.6s" repeatCount="indefinite"/>{body}</g>')
    return shadow(210, 452, 250, 20) + body


def hacker(glow: str = "fa") -> str:
    """A hooded attacker behind a laptop (seen from the back). Origin = middle of the desk edge."""
    return f"""{shadow(0, 26, 260, 18)}
<path d="M-180 0 q0 -200 180 -212 q180 12 180 212 z" fill="#2b2b36"/>
<path d="M-40 -200 l-14 120 M40 -200 l14 120" stroke="#d6d6de" stroke-width="6" stroke-linecap="round"/>
<path d="M-118 -214 q-22 -214 118 -224 q140 10 118 224 q-118 30 -236 0 z" fill="#353542"/>
<ellipse cx="0" cy="-300" rx="70" ry="86" fill="#0b0b10"/>
<ellipse cx="0" cy="-290" rx="70" ry="86" class="{glow}" opacity="0.12">{blink(1.2, 0, 0.06, 0.18)}</ellipse>
<ellipse cx="-26" cy="-306" rx="13" ry="8" class="{glow}">{blink(2.6, 0, 0.1)}</ellipse>
<ellipse cx="26" cy="-306" rx="13" ry="8" class="{glow}">{blink(2.6, 0, 0.1)}</ellipse>
<rect x="-200" y="-176" width="400" height="190" rx="16" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>
<rect x="-186" y="-166" width="200" height="8" rx="4" fill="#fff" opacity="0.15"/>
<rect x="-236" y="8" width="472" height="22" rx="10" fill="url(#steel)"/>"""


def laptop(screen: str = "", w: int = 520, h: int = 330) -> str:
    """A laptop seen from the front at (0,0). `screen` is drawn in screen coordinates (0,0 top-left)."""
    return (f'{shadow(w / 2, h + 40, w * 0.6, 18)}'
            f'<rect x="0" y="0" width="{w}" height="{h}" rx="18" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>'
            f'<rect x="16" y="16" width="{w - 32}" height="{h - 32}" rx="8" fill="url(#screen)"/>'
            f'<g transform="translate(16 16)">{screen}</g>'
            f'<path d="M-40 {h} h{w + 80} l-20 26 h-{w + 40} z" fill="url(#steel)"/>'
            f'<rect x="{w / 2 - 50}" y="{h}" width="100" height="8" rx="4" fill="#8f8f9a"/>')


def key(length: int = 420, teeth=(60, 40, 70), cls: str = "fa") -> str:
    """A key with its round bow centred on (0,0), pointing right."""
    n = len(teeth)
    step = (length - 120) / max(n, 1)
    tt = "".join(f'<rect x="{110 + length - 120 - (k + 1) * step + 6:.0f}" y="10" width="{step - 12:.0f}" height="{t}" rx="6" class="{cls}"/>'
                 for k, t in enumerate(teeth))
    return (f'<rect x="60" y="-26" width="{length}" height="52" rx="12" class="{cls}"/>{tt}'
            f'<rect x="70" y="-22" width="{length - 20}" height="12" rx="6" fill="#fff" opacity="0.3"/>'
            f'<circle r="96" class="{cls}"/><circle r="38" class="fb"/>'
            f'<path d="M-70 -40 a80 80 0 0 1 60 -44" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" opacity="0.4"/>')


def paper(w: float, h: float, inner: str = "", rot: float = 0) -> str:
    return (f'<g transform="rotate({rot})"><rect x="{-w / 2 + 8}" y="{-h / 2 + 10}" width="{w}" height="{h}" rx="16" fill="#000" opacity="0.35"/>'
            f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="16" fill="url(#paper)"/>{inner}</g>')


def ink(x: float, y: float, text: str, size: int = 40, color: str = "#111", anchor: str = "middle", weight: int = 700,
        mono: bool = False) -> str:
    fam = ' font-family="monospace"' if mono else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}"{fam} '
            f'style="fill:{color}">{text}</text>')


def fly(inner: str, frm: tuple, to: tuple, begin: float, dur: float = 0.8, repeat: bool = False) -> str:
    """Moves `inner` (drawn around the origin) from one point to another."""
    rep = 'repeatCount="indefinite"' if repeat else 'fill="freeze"'
    op = (f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.15;0.8;1" begin="{begin}s" dur="{dur}s" {rep}/>'
          if repeat else fade(begin, 0.15))
    return (f'<g transform="translate({frm[0]} {frm[1]})" opacity="0">{op}'
            f'<animateTransform attributeName="transform" type="translate" from="{frm[0]} {frm[1]}" to="{to[0]} {to[1]}" '
            f'begin="{begin}s" dur="{dur}s" {rep}/>{inner}</g>')


def code_lines(w: float, n: int, begin: float, red_from: int = 99) -> str:
    out = []
    widths = [0.7, 0.45, 0.6, 0.8, 0.35, 0.55, 0.65]
    for i in range(n):
        y = 70 + i * 34
        indent = 20 + (i % 3) * 26
        lw = (w - 60) * widths[i % len(widths)]
        cls = f'fill="{RED}"' if i >= red_from else 'fill="#fff" opacity="0.35"'
        b = begin + max(0, i - red_from) * 0.35 if i >= red_from else 0
        bar = f'<rect x="{indent}" y="{y}" width="{lw:.0f}" height="16" rx="8" {cls}/>'
        out.append(appear(bar, b, 0.2) if i >= red_from else bar)
    return "".join(out)


# 0. Hackers broke into 1Password's servers ----------------------------------------------------
packet = f'<rect x="-14" y="-14" width="28" height="28" rx="6" fill="{RED}"/>'
save(SLUG, "breach", f"""
{waves(270, 450, "sa2", 3, 60, 260, 2.0, 8, 0.5)}
{place(120, 160, 1.0, server(alert=True))}
<text x="270" y="138" font-size="40" font-weight="700" text-anchor="middle" class="fa">1Password</text>
{''.join(fly(packet, (560, 560), (420, 450), 0.6 + k * 0.35, 1.05, True) for k in range(3))}
{place(700, 740, 0.95, hacker("fa2"))}
{badge(500, 880, "HACKED", 1.2, "fa2")}
""")

# 1. So why are the passwords still safe? -------------------------------------------------------
qm = lambda x, y, rot, b: pop(x, y, f'<text y="60" font-size="190" text-anchor="middle" class="display fa2" transform="rotate({rot})">?</text>', b)
save(SLUG, "question", f"""
{place(250, 200, 1.2, vault(shake=True))}
<rect x="230" y="160" width="540" height="600" rx="40" class="nf sa" stroke-width="8" stroke-dasharray="28 18" opacity="0">{fade(1.0)}
<animate attributeName="stroke-dashoffset" from="0" to="-92" dur="1.4s" repeatCount="indefinite"/></rect>
{qm(150, 300, -14, 0.4)}{qm(860, 260, 12, 0.7)}{qm(880, 620, -8, 1.0)}
{badge(500, 880, "PASSWORDS STILL SAFE", 1.4)}
""")

# 2. 1Password never had the keys --------------------------------------------------------------
hooks = []
for k in range(3):
    hx = 620 + k * 120
    hooks.append(
        f'<path d="M{hx} 300 v40 q0 24 -24 24" fill="none" stroke="#d6d6de" stroke-width="10" stroke-linecap="round"/>'
        f'<g opacity="0.5">{blink(1.4, k * 0.3, 0.1)}'
        f'<g transform="translate({hx - 10} 420) rotate(90) scale(0.42)"><circle r="96" fill="none" stroke="#fff" stroke-width="10" stroke-dasharray="20 14"/>'
        f'<rect x="60" y="-26" width="300" height="52" rx="12" fill="none" stroke="#fff" stroke-width="10" stroke-dasharray="20 14"/></g></g>')
save(SLUG, "nokeys", f"""
{place(80, 190, 1.0, server())}
<text x="230" y="168" font-size="40" font-weight="700" text-anchor="middle" class="fa">1Password</text>
{shadow(740, 760, 240, 18, 0.4)}
<rect x="520" y="230" width="440" height="520" rx="26" fill="#6b4a32"/>
<rect x="540" y="250" width="400" height="480" rx="16" fill="#4a3324"/>
<rect x="560" y="262" width="360" height="8" rx="4" fill="#fff" opacity="0.15"/>
{''.join(hooks)}
{pop(740, 650, red_x(62), 1.0)}
{appear(label(500, 880, "No copy of your keys", 50), 1.4)}
""")

# 3. An employee's GitHub account pushes malicious code to the servers ----------------------------
gh_screen = (f'<rect x="0" y="0" width="488" height="44" fill="#fff" opacity="0.08"/>'
             f'<text x="20" y="32" font-size="28" font-weight="700" style="fill:#fff">GitHub</text>'
             f'<circle cx="440" cy="22" r="14" class="fa"/>'
             f'{code_lines(488, 7, 0.6, 4)}')
save(SLUG, "github", f"""
{place(60, 260, 0.95, laptop(gh_screen))}
{place(680, 180, 0.95, server(alert=True))}
{''.join(fly(packet, (585, 420), (720, 420), 1.4 + k * 0.3, 0.9, True) for k in range(3))}
{draw("M585 420 L700 420", 1.2, 0.4, "nf sa2", 6, 'stroke-dasharray="1" opacity="0.6"')}
{pop(290, 170, '<rect x="-150" y="-44" width="300" height="88" rx="44" fill="#fff" fill-opacity="0.12" stroke="#fff" stroke-opacity="0.3" stroke-width="2"/><circle cx="-104" cy="0" r="26" fill="#f2c6a0"/><text x="20" y="14" font-size="38" text-anchor="middle">Employee</text>', 0.3)}
{appear(label(500, 880, "Malicious code, pushed to servers", 46, "fa2"), 1.8)}
""")

# 4. Names, emails and sign-in times are taken ---------------------------------------------------
cards = [("Name", "Alex Rivera"), ("Email", "alex@mail.com"), ("Last sign-in", "Nov 18, 9:42")]
card_svg = ""
for k, (head, val) in enumerate(cards):
    inner = (ink(-140, -18, head, 30, "#777", "start", 600) + ink(-140, 30, val, 34, "#111", "start"))
    c = paper(320, 120, inner, (-4, 3, -2)[k])
    card_svg += fly(c, (240, 420), (600 + k * 20, 150 + k * 140), 0.4 + k * 0.5, 0.8)
save(SLUG, "stolen", f"""
{place(80, 200, 0.95, server(alert=True))}
{place(800, 900, 0.7, hacker("fa2"))}
{card_svg}
""")

# 5. Every vault is locked with a key that stays on your device ------------------------------------
minis = f'<defs><g id="mv">{vault(spin=4)}</g></defs>' + "".join(
    place(139 + c * 132, 210 + r * 132, 0.28, '<use href="#mv"/>')
    for r in range(4) for c in range(3))
phone_key = (f'<rect x="0" y="0" width="276" height="536" fill="#fff" opacity="0.04"/>'
             f'<circle cx="138" cy="250" r="110" class="fa" opacity="0.18">{blink(1.3, 0, 0.08, 0.25)}</circle>'
             f'<g transform="translate(70 250) scale(0.38)">{key(330, (50, 30, 60))}</g>')
save(SLUG, "vaults", f"""
{shadow(330, 800, 300, 20)}
<rect x="80" y="150" width="500" height="640" rx="26" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>
<rect x="100" y="170" width="460" height="600" rx="14" fill="#0c0c10"/>
{minis}
{bob(phone(660, 220, 300, 560, phone_key), 8, 3)}
{waves(810, 500, "sa", 2, 40, 160, 2.2, 5, 0.5)}
{pop(560, 170, tick(40), 1.2)}
{appear(label(810, 870, "Key stays with you", 46, "fa"), 1.0)}
""")

# 6. The key is built from two pieces ------------------------------------------------------------
KEY = key(560, (70, 40, 80, 50, 64))
save(SLUG, "twopieces", f"""
<defs><clipPath id="kl"><rect x="-200" y="-200" width="330" height="400"/></clipPath>
<clipPath id="kr"><rect x="130" y="-200" width="600" height="400"/></clipPath></defs>
<g transform="translate(180 420)">
  <g><animateTransform attributeName="transform" type="translate" values="-140 0;-140 0;0 0" keyTimes="0;0.3;1" dur="1.4s" fill="freeze"/>
    <g clip-path="url(#kl)">{KEY}</g></g>
  <g><animateTransform attributeName="transform" type="translate" values="160 0;160 0;0 0" keyTimes="0;0.3;1" dur="1.4s" fill="freeze"/>
    <g clip-path="url(#kr)">{KEY.replace('class="fa"', 'class="fa2"')}</g></g>
</g>
<circle cx="310" cy="420" r="30" fill="#fff" opacity="0" filter="url(#glow)"><animate attributeName="opacity" values="0;1;0" begin="1.4s" dur="0.6s" fill="freeze"/></circle>
{appear(label(200, 640, "Account password", 46, "fa"), 0.3)}
{appear(label(620, 640, "Secret Key", 46, "fa2"), 0.6)}
{badge(500, 860, "1 + 1 = YOUR KEY", 1.8)}
""")

# 7. The Secret Key: 34 characters, made on your device, never sent ------------------------------
chars = "".join(
    f'<tspan opacity="0">{fade(0.4 + i * 0.05, 0.05)}{ch}</tspan>' for i, ch in enumerate(SECRET))
kit_inner = (ink(-410, -40, "SECRET KEY", 32, "#777", "start", 700)
             + f'<text x="0" y="40" font-size="29" font-weight="700" text-anchor="middle" font-family="monospace" style="fill:#111">{chars}</text>')
spark = (f'<circle cx="138" cy="230" r="100" class="fa" opacity="0.2">{blink(0.9, 0, 0.08, 0.25)}</circle>'
         f'<g transform="translate(138 230)"><g><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="4s" repeatCount="indefinite"/>'
         + "".join(f'<rect x="-8" y="-80" width="16" height="40" rx="8" class="fa" transform="rotate({a})"/>' for a in range(0, 360, 45))
         + '</g></g>'
         f'<text x="138" y="420" font-size="34" text-anchor="middle" style="fill:#fff">Creating key</text>')
save(SLUG, "secretkey", f"""
{place(90, 120, 1.0, phone(0, 0, 300, 520, spark))}
{place(690, 150, 0.6, server())}
{draw("M400 330 L670 330", 0.6, 0.6, "nf sw", 6, 'stroke-dasharray="14 14" opacity="0.7"')}
{pop(540, 330, red_x(52), 1.4)}
{appear(label(540, 250, "Never sent", 44, "fa2"), 1.6)}
{place(500, 760, 1.0, appear(paper(940, 150, kit_inner), 0.2))}
""")

# 8. Your device mixes them into one key and scrambles everything ----------------------------------
items = [("Bank", "••••••••"), ("Email", "••••••"), ("Wi-Fi", "•••••••••")]
item_svg = "".join(
    fly(paper(250, 116, ink(-105, -10, n, 34, "#777", "start", 600) + ink(-105, 36, v, 36, "#111", "start")),
        (160, 240 + k * 180), (400, 420), 0.3 + k * 0.6, 1.0, True)
    for k, (n, v) in enumerate(items))
scr = ["x7#Qa9!", "Lp$2v&Z", "9@kR!f3"]
scr_svg = "".join(
    fly(f'<rect x="-100" y="-34" width="200" height="68" rx="14" class="fa2" opacity="0.9"/>'
        + ink(0, 12, s, 34, "#0a0a0a", mono=True), (640, 420), (840, 240 + k * 180), 1.0 + k * 0.6, 1.0, True)
    for k, s in enumerate(scr))
ph = (f'<circle cx="118" cy="230" r="90" class="fa" opacity="0.2">{blink(0.8, 0, 0.08, 0.25)}</circle>'
      f'<g transform="translate(118 230)"><g><animateTransform attributeName="transform" type="rotate" values="-20;20;-20" dur="1s" repeatCount="indefinite"/>'
      f'<g transform="translate(-70 0) scale(0.32)">{key(330, (50, 30, 60))}</g></g></g>')
save(SLUG, "encrypt", f"""
{item_svg}
{bob(phone(380, 180, 260, 500, ph), 6, 3)}
{scr_svg}
{appear(label(500, 880, "Scrambled before it leaves", 48, "fa"), 0.8)}
""")

# 9. Password about 40 bits, Secret Key 128 bits -------------------------------------------------
save(SLUG, "bits", f"""
{pop(190, 260, f'<g transform="scale(0.75)">{key(260, (60, 40))}</g>', 0.2)}
{appear('<text x="560" y="300" font-size="130" class="display fw">40</text><text x="700" y="300" font-size="46" style="fill:#fff">bits</text>', 0.5)}
{appear(label(330, 400, "Your password (estimated)", 40), 0.6)}
{pop(130, 540, f'<g transform="scale(0.75)">{key(860, (70, 40, 80, 50, 64, 36, 76, 54, 70, 44))}</g>', 1.8)}
{appear('<text x="560" y="790" font-size="150" class="display fa">128</text><text x="815" y="790" font-size="46" class="fa">bits</text>', 2.2)}
{appear(label(250, 790, "Secret Key", 44, "fa"), 2.2)}
""")

# 10. Guessing your password alone gets nowhere ----------------------------------------------------
guess = "".join(
    f'<text x="24" y="{60 + k * 46}" font-size="32" font-family="monospace" style="fill:#fff" opacity="0.7">{w}</text>'
    for k, w in enumerate(["sunshine1", "Pa$$w0rd", "dragon99", "letmein!"]))
scroll = (f'<g><animateTransform attributeName="transform" type="translate" values="0 40;0 -20" dur="0.8s" repeatCount="indefinite"/>{guess}</g>')
save(SLUG, "brute", f"""
{place(560, 180, 1.0, vault(spin=1.2, shake=True))}
{place(40, 300, 0.8, laptop(f'<clipPath id="gc"><rect x="0" y="0" width="488" height="298"/></clipPath><g clip-path="url(#gc)">{scroll}</g>'))}
{''.join(fly(packet, (470, 450), (600, 400), 0.4 + k * 0.4, 1.2, True) for k in range(3))}
<g transform="translate(770 390)" opacity="0">{fade(0.8, 0.1)}<g>{red_x(70)}<animate attributeName="opacity" values="1;0.3;1" dur="0.6s" repeatCount="indefinite"/></g></g>
{badge(500, 880, "STILL LOCKED", 1.2)}
""")

# 11. The stolen emails make fake 1Password messages -----------------------------------------------
mail = (f'<rect x="0" y="0" width="316" height="596" fill="#f4f4f8"/>'
        f'<rect x="0" y="0" width="316" height="90" class="fa2"/>'
        f'<text x="20" y="58" font-size="30" font-weight="700" style="fill:#0a0a0a">Inbox</text>'
        + ink(20, 150, "1Passw0rd Support", 26, "#555", "start", 700)
        + ink(20, 200, "Urgent: verify", 32, "#111", "start", 700)
        + ink(20, 240, "your account", 32, "#111", "start", 700)
        + "".join(f'<rect x="20" y="{280 + k * 30}" width="{270 - k * 50}" height="14" rx="7" fill="#c9c5ba"/>' for k in range(3))
        + f'<rect x="40" y="400" width="236" height="74" rx="37" fill="{RED}"/>'
        + ink(158, 449, "Sign in", 34, "#fff"))
hook = (f'<g><animateTransform attributeName="transform" type="translate" values="0 -260;0 0;0 -14;0 0" keyTimes="0;0.6;0.8;1" dur="1.4s" fill="freeze"/>'
        f'<line x1="690" y1="110" x2="690" y2="560" stroke="#d6d6de" stroke-width="5"/>'
        f'<path d="M690 560 v50 q0 46 -40 46 q-36 0 -40 -36" fill="none" stroke="#d6d6de" stroke-width="12" stroke-linecap="round"/>'
        f'<path d="M610 620 l-14 -22 l26 4 z" fill="#d6d6de"/></g>')
save(SLUG, "phishing", f"""
{bob(phone(330, 150, 340, 620, mail), 6, 3)}
{hook}
{badge(200, 330, "FAKE", 1.4, "fa2")}
{appear(label(500, 880, "Watch for fake emails", 48), 1.8)}
""")

# 12. 1Password will never ask for your password or Secret Key -----------------------------------
call = (f'<rect x="0" y="0" width="276" height="536" fill="#fff" opacity="0.04"/>'
        f'<circle cx="138" cy="150" r="62" fill="#55555f"/><circle cx="138" cy="132" r="24" fill="#d6d6de"/>'
        f'<path d="M98 190 q40 -50 80 0" fill="#d6d6de"/>'
        f'<text x="138" y="270" font-size="30" font-weight="700" text-anchor="middle" style="fill:#fff">"1Password"</text>'
        f'<text x="138" y="310" font-size="26" text-anchor="middle" style="fill:#fff" opacity="0.6">calling...</text>'
        f'<circle cx="68" cy="440" r="40" fill="{RED}">{blink(0.8, 0, 0.5)}</circle>'
        f'<circle cx="208" cy="440" r="40" fill="{GREEN}"/>')
ring = (f'<g><animateTransform attributeName="transform" type="rotate" values="0 220 440;-4 220 440;4 220 440;0 220 440" '
        f'dur="0.4s" repeatCount="indefinite"/>{phone(70, 160, 300, 560, call)}</g>')
bubble = (f'<path d="M-230 -110 h460 a30 30 0 0 1 30 30 v120 a30 30 0 0 1 -30 30 h-380 l-50 50 v-50 h-30 a30 30 0 0 1 -30 -30 v-120 a30 30 0 0 1 30 -30 z" fill="url(#paper)"/>'
          + ink(0, -30, "Read me your", 40, "#111") + ink(0, 30, "Secret Key?", 40, "#111"))
save(SLUG, "neverask", f"""
{waves(220, 440, "sa", 3, 120, 240, 1.8, 6, 0.6)}
{ring}
{pop(690, 300, bubble, 0.5)}
{pop(930, 180, red_x(48), 1.4)}
{appear(label(690, 560, "Never asks", 50, "fa2"), 1.6)}
""")

# 13. Payoff: into the building, but the safe stays locked ------------------------------------------
room = (f'<rect x="30" y="170" width="660" height="620" rx="20" fill="#1c1c24" stroke="#fff" stroke-opacity="0.25" stroke-width="5"/>'
        f'<path d="M10 190 L360 40 L710 190 z" fill="url(#metal)" stroke="#fff" stroke-opacity="0.25" stroke-width="5"/>'
        f'<rect x="30" y="700" width="660" height="90" fill="#000" opacity="0.25"/>'
        f'<rect x="80" y="240" width="140" height="110" rx="10" fill="#0b0b10" stroke="#55555f" stroke-width="6"/>'
        f'<rect x="80" y="240" width="140" height="110" rx="10" class="fa" opacity="0.08"/>'
        f'<text x="360" y="155" font-size="40" font-weight="700" text-anchor="middle" class="fa">1Password</text>')
holder = (f'<rect x="0" y="0" width="216" height="396" fill="#fff" opacity="0.04"/>'
          f'<circle cx="108" cy="190" r="80" class="fa" opacity="0.2">{blink(1.2, 0, 0.08, 0.25)}</circle>'
          f'<g transform="translate(52 190) scale(0.28)">{key(330, (50, 30, 60))}</g>')
save(SLUG, "payoff", f"""
{room}
{place(300, 310, 0.85, vault(spin=8))}
{place(165, 780, 0.6, hacker("fa2"))}
{bob(phone(730, 300, 240, 420, holder), 8, 3)}
{waves(850, 510, "sa", 2, 40, 150, 2.4, 5, 0.5)}
{badge(500, 890, "LOCKED WITH YOUR KEY", 1.2)}
""")
