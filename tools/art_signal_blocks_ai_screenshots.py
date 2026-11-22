"""Illustrations for the 'signal-blocks-ai-screenshots' video. Run:  python tools/art_signal_blocks_ai_screenshots.py

Objects (phone with a Signal chat, the phone's AI assistant orb, a black screenshot, a server rack,
a laptop, a TV, a person) are drawn once in their own coordinates and placed with place(), so every
scene reuses the same things at different sizes.
"""
from artlib import appear, badge, bob, fade, label, pop, save, shadow, waves

SLUG = "signal-blocks-ai-screenshots"
BLUE = "#3a76f0"     # Signal's own blue for sent messages
GREY = "#3b3b48"     # received messages
RED = "#ff4d4d"

PW, PH = 340, 680            # phone body size
SW, SH = PW - 24, PH - 24    # screen size inside the phone (316 x 656)


def place(x: float, y: float, s: float, inner: str) -> str:
    return f'<g transform="translate({x} {y}) scale({s})">{inner}</g>'


# --- the phone and the Signal chat on its screen ----------------------------------------------
def chat(begin: float | None = None) -> str:
    """A Signal conversation in screen coordinates (316 x 656). Bubbles pop in if `begin` is set."""
    rows = [(0, 150, 200, 2), (1, 250, 170, 1), (0, 330, 230, 2), (1, 432, 190, 2), (0, 534, 150, 1)]
    bubbles = []
    for k, (mine, y, w, lines) in enumerate(rows):
        h = 30 + lines * 26
        x = SW - 18 - w if mine else 18
        fill = BLUE if mine else GREY
        txt = "".join(f'<rect x="{x + 18}" y="{y + 20 + i * 26}" width="{w - 36 - i * 40}" height="12" rx="6" '
                      f'fill="#fff" opacity="0.75"/>' for i in range(lines))
        b = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="24" fill="{fill}"/>{txt}'
        if begin is not None:
            b = appear(b, begin + k * 0.18, 0.2)
        bubbles.append(b)
    return f"""<rect x="0" y="0" width="{SW}" height="{SH}" rx="34" fill="#0e0e14"/>
<rect x="0" y="40" width="{SW}" height="80" fill="#17171f"/>
<path d="M34 80 l-14 -12 m0 0 l14 -12" class="nf" stroke="#fff" stroke-width="5" stroke-linecap="round"/>
<circle cx="76" cy="80" r="25" fill="#c27dff"/><text x="76" y="92" font-size="30" text-anchor="middle">A</text>
<rect x="114" y="66" width="110" height="14" rx="7" fill="#fff" opacity="0.9"/>
<rect x="114" y="88" width="70" height="10" rx="5" fill="#fff" opacity="0.4"/>
<circle cx="282" cy="80" r="10" fill="#fff" opacity="0.5"/>
{''.join(bubbles)}
<rect x="16" y="{SH - 74}" width="{SW - 92}" height="54" rx="27" fill="#24242e"/>
<circle cx="{SW - 44}" cy="{SH - 47}" r="27" fill="{BLUE}"/>
<path d="M{SW - 56} {SH - 47} h22 m-9 -9 l9 9 l-9 9" class="nf" stroke="#fff" stroke-width="5" stroke-linecap="round"/>"""


def handset(screen: str, uid: str, glow: str = "") -> str:
    """A phone body at (0,0), 340 x 680. `screen` is clipped to the screen area."""
    return f"""{shadow(PW / 2, PH + 18, PW * 0.62, 22)}{glow}
<rect x="0" y="0" width="{PW}" height="{PH}" rx="48" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>
<rect x="{PW}" y="150" width="7" height="80" rx="3" fill="#5a5a66"/>
<rect x="-7" y="130" width="7" height="50" rx="3" fill="#5a5a66"/><rect x="-7" y="196" width="7" height="50" rx="3" fill="#5a5a66"/>
<clipPath id="{uid}sc"><rect x="12" y="12" width="{SW}" height="{SH}" rx="36"/></clipPath>
<g clip-path="url(#{uid}sc)"><g transform="translate(12 12)">{screen}</g></g>
<rect x="{PW / 2 - 48}" y="26" width="96" height="26" rx="13" fill="#000"/>
<path d="M30 40 q-10 120 -4 300" class="nf" stroke="#fff" stroke-opacity="0.08" stroke-width="14" stroke-linecap="round"/>"""


def black(lock: bool = True) -> str:
    """What a capture of the protected window gets: an empty black box (screen coordinates)."""
    padlock = ""
    if lock:
        padlock = lock_icon(SW / 2, SH / 2, 1.0, "#fff", 0.25)
    return f'<rect x="0" y="0" width="{SW}" height="{SH}" fill="#000"/>{padlock}'


def lock_icon(cx: float, cy: float, s: float, colour: str, opacity: float = 1) -> str:
    return (f'<g transform="translate({cx} {cy}) scale({s})" opacity="{opacity}">'
            f'<path d="M-34 -10 v-26 a34 34 0 0 1 68 0 v26" class="nf" stroke="{colour}" stroke-width="14"/>'
            f'<rect x="-52" y="-12" width="104" height="80" rx="16" fill="{colour}"/>'
            f'<circle cx="0" cy="20" r="11" fill="#000" opacity="0.5"/></g>')


def scan_beam(uid: str, begin: float = 0, dur: float = 2.2, colour: str = "#8ab4ff") -> str:
    """A bright band sweeping down the screen (screen coordinates), the AI reading it."""
    return (f'<linearGradient id="{uid}bm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{colour}" stop-opacity="0"/>'
            f'<stop offset="0.85" stop-color="{colour}" stop-opacity="0.55"/><stop offset="1" stop-color="#fff" stop-opacity="1"/></linearGradient>'
            f'<rect x="0" y="-140" width="{SW}" height="140" fill="url(#{uid}bm)" opacity="0">'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.9;1" begin="{begin}s" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y" from="-140" to="{SH}" begin="{begin}s" dur="{dur}s" repeatCount="indefinite"/></rect>')


# --- the phone's built-in AI assistant ----------------------------------------------------------
def orb(uid: str, r: float = 70) -> str:
    """The AI assistant: a glowing orb with a sparkle, centred on (0,0)."""
    k = r / 70
    star = f"M0 {-44 * k} C{6 * k} {-10 * k} {10 * k} {-6 * k} {44 * k} 0 C{10 * k} {6 * k} {6 * k} {10 * k} 0 {44 * k} " \
           f"C{-6 * k} {10 * k} {-10 * k} {6 * k} {-44 * k} 0 C{-10 * k} {-6 * k} {-6 * k} {-10 * k} 0 {-44 * k} Z"
    return f"""<defs><radialGradient id="{uid}orb" cx="0.35" cy="0.3" r="0.8">
<stop offset="0" stop-color="#ffffff"/><stop offset="0.35" stop-color="#8ab4ff"/><stop offset="0.75" stop-color="#9b5cff"/><stop offset="1" stop-color="#ff5ca8"/></radialGradient></defs>
<circle r="{r * 1.5}" fill="#9b5cff" opacity="0.45" filter="url(#soft)"><animate attributeName="opacity" values="0.25;0.6;0.25" dur="1.6s" repeatCount="indefinite"/></circle>
<circle r="{r}" fill="url(#{uid}orb)"/>
<path d="{star}" fill="#fff"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="6s" repeatCount="indefinite"/></path>
<ellipse cx="{-r * 0.35}" cy="{-r * 0.45}" rx="{r * 0.28}" ry="{r * 0.16}" fill="#fff" opacity="0.5"/>"""


def screenshot_card(w: float, h: float, inner: str) -> str:
    """A captured screenshot thumbnail at (0,0): white frame with the captured image inside."""
    return (f'{shadow(w / 2, h + 14, w * 0.55, 16)}'
            f'<rect x="-10" y="-10" width="{w + 20}" height="{h + 20}" rx="22" fill="#f4f4f8"/>'
            f'<rect x="0" y="0" width="{w}" height="{h}" rx="14" fill="#000"/>{inner}')


def flash(x: float, y: float, w: float, h: float, begin: float) -> str:
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="40" fill="#fff" opacity="0">'
            f'<animate attributeName="opacity" values="0;0.95;0" keyTimes="0;0.2;1" begin="{begin}s" dur="0.5s" fill="freeze"/></rect>')


# --- other objects --------------------------------------------------------------------------------
def server() -> str:
    """A server rack at (0,0), 260 x 440."""
    units = []
    for i in range(6):
        y = 30 + i * 66
        leds = "".join(
            f'<circle cx="{40 + j * 24}" cy="{y + 28}" r="7" fill="{"#3dff8f" if (i + j) % 3 else "#ffb03d"}">'
            f'<animate attributeName="opacity" values="1;0.2;1" begin="{(i * 3 + j) * 0.11:.2f}s" dur="{0.6 + j * 0.2:.1f}s" repeatCount="indefinite"/></circle>'
            for j in range(3))
        slots = "".join(f'<rect x="{126 + j * 26}" y="{y + 14}" width="16" height="28" rx="4" fill="#0a0a0e"/>' for j in range(4))
        units.append(f'<rect x="16" y="{y}" width="228" height="56" rx="8" fill="url(#metal)" stroke="#fff" stroke-opacity="0.18" stroke-width="2"/>{leds}{slots}')
    return f"""{shadow(130, 456, 170, 18)}
<rect x="0" y="0" width="260" height="440" rx="18" fill="#26262f" stroke="#fff" stroke-opacity="0.25" stroke-width="4"/>
<rect x="6" y="6" width="248" height="10" rx="5" fill="#fff" opacity="0.1"/>
{''.join(units)}"""


def laptop(uid: str, screen: str) -> str:
    """A laptop at (0,0): lid 640 x 410, base below. `screen` is in 600 x 370 coordinates."""
    return f"""{shadow(330, 470, 420, 24)}
<rect x="0" y="0" width="640" height="410" rx="26" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>
<clipPath id="{uid}ls"><rect x="20" y="20" width="600" height="370" rx="10"/></clipPath>
<g clip-path="url(#{uid}ls)"><g transform="translate(20 20)">{screen}</g></g>
<circle cx="320" cy="11" r="4" fill="#000"/>
<path d="M-50 412 h740 l-30 44 q-6 8 -20 8 h-640 q-14 0 -20 -8 z" fill="url(#steel)"/>
<rect x="260" y="412" width="120" height="12" rx="6" fill="#9a9aa6"/>"""


def desktop_chat() -> str:
    """Signal on a laptop screen (600 x 370)."""
    rows = [(0, 70, 220), (1, 140, 180), (0, 210, 260), (1, 280, 150)]
    bub = "".join(
        f'<rect x="{600 - 30 - w if m else 200}" y="{y}" width="{w}" height="50" rx="22" fill="{BLUE if m else GREY}"/>'
        f'<rect x="{600 - 30 - w + 18 if m else 218}" y="{y + 19}" width="{w - 50}" height="12" rx="6" fill="#fff" opacity="0.7"/>'
        for m, y, w in rows)
    side = "".join(
        f'<circle cx="40" cy="{60 + i * 70}" r="20" fill="{c}"/><rect x="70" y="{52 + i * 70}" width="90" height="12" rx="6" fill="#fff" opacity="0.5"/>'
        for i, c in enumerate(("#c27dff", "#ff9f5c", "#5cd6ff", "#7dffb0")))
    return (f'<rect x="0" y="0" width="600" height="370" fill="#0e0e14"/>'
            f'<rect x="0" y="0" width="180" height="370" fill="#17171f"/>{side}{bub}')


def tv(uid: str, screen: str) -> str:
    """A TV at (0,0): 600 x 360 panel on a stand. `screen` is in 572 x 332 coordinates."""
    return f"""{shadow(300, 440, 260, 18)}
<path d="M250 360 l-30 72 h160 l-30 -72 z" fill="url(#metal)"/>
<rect x="0" y="0" width="600" height="360" rx="18" fill="#111116" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>
<clipPath id="{uid}tv"><rect x="14" y="14" width="572" height="332" rx="8"/></clipPath>
<g clip-path="url(#{uid}tv)"><g transform="translate(14 14)">{screen}</g></g>
<circle cx="300" cy="352" r="3" fill="#ff4d4d"/>"""


def movie(uid: str) -> str:
    """A film playing: sunset over mountains with a car driving across (572 x 332)."""
    return f"""<linearGradient id="{uid}sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a1a5e"/><stop offset="0.6" stop-color="#ff7a59"/><stop offset="1" stop-color="#ffd27a"/></linearGradient>
<rect x="0" y="0" width="572" height="332" fill="url(#{uid}sky)"/>
<circle cx="380" cy="200" r="60" fill="#fff2b0"/>
<path d="M0 240 l120 -110 l90 70 l110 -120 l140 140 l112 -70 v182 h-572 z" fill="#3a1f4a"/>
<rect x="0" y="282" width="572" height="50" fill="#1a1022"/>
<g><animateTransform attributeName="transform" type="translate" from="-120 0" to="620 0" dur="4s" repeatCount="indefinite"/>
<rect x="0" y="262" width="90" height="26" rx="8" fill="#ff4d6d"/><rect x="18" y="248" width="50" height="20" rx="6" fill="#ff4d6d"/>
<circle cx="20" cy="290" r="10" fill="#111"/><circle cx="70" cy="290" r="10" fill="#111"/></g>"""


def person() -> str:
    """A person in profile facing right, (0,0) = waist centre, about 470 tall; right hand at (178,-238)."""
    return f"""<path d="M-110 0 q-6 -190 70 -220 q60 -22 110 0 q60 30 60 220 z" fill="#2f4a7a"/>
<path d="M60 -190 q70 40 118 -48" class="nf" stroke="#2f4a7a" stroke-width="46" stroke-linecap="round"/>
<circle cx="178" cy="-238" r="26" fill="#f2c6a0"/>
<rect x="-18" y="-262" width="44" height="50" rx="14" fill="#e8b48c"/>
<circle cx="6" cy="-322" r="80" fill="#f2c6a0"/>
<path d="M84 -320 l14 18 l-12 6" fill="#f2c6a0"/>
<path d="M-74 -320 q-12 -96 76 -100 q72 -2 84 64 q-60 -40 -112 -6 q-18 44 -48 42 z" fill="#2a1d18"/>
<circle cx="52" cy="-326" r="9" fill="#1a1a1a"/>
<path d="M58 -278 q14 4 22 -4" class="nf" stroke="#7a3f30" stroke-width="5" stroke-linecap="round"/>"""


def tick(cx: float, cy: float, begin: float, r: float = 44) -> str:
    return pop(cx, cy, f'<circle r="{r}" fill="#3ddc84"/><path d="M{-r * .42} 0 l{r * .3} {r * .32} l{r * .56} {-r * .64}" '
                       f'class="nf" stroke="#fff" stroke-width="{r * .24}" stroke-linecap="round" stroke-linejoin="round"/>', begin)


def cross(cx: float, cy: float, begin: float, r: float = 50) -> str:
    return pop(cx, cy, f'<circle r="{r}" fill="{RED}"/><path d="M{-r * .4} {-r * .4} L{r * .4} {r * .4} M{r * .4} {-r * .4} L{-r * .4} {r * .4}" '
                       f'stroke="#fff" stroke-width="{r * .26}" stroke-linecap="round"/>', begin)


def shield(cx: float, cy: float, s: float, cls: str = "fa", inner: str = "") -> str:
    return (f'<g transform="translate({cx} {cy}) scale({s})">'
            f'<path d="M0 -100 l84 30 v56 q0 74 -84 114 q-84 -40 -84 -114 v-56 z" class="{cls}" stroke="#fff" stroke-width="6" stroke-opacity="0.6"/>'
            f'<path d="M0 -76 l60 22 v40 q0 54 -60 84" class="nf" stroke="#fff" stroke-opacity="0.35" stroke-width="8" stroke-linecap="round"/>'
            f'{inner}</g>')


# 1. Hook: Signal now blocks screenshots on your phone -------------------------------------------
save(SLUG, "hook", f"""
{place(330, 90, 1.0, handset(chat(), "h1"))}
{flash(342, 102, SW, SH, 0.7)}
<g opacity="0">{fade(1.0, 0.2)}
  <g><animateTransform attributeName="transform" type="translate" values="420 300;150 470" begin="1.0s" dur="0.5s" fill="freeze"/>
    <g transform="rotate(-6)">{screenshot_card(170, 350, lock_icon(85, 175, 0.7, "#fff", 0.3))}</g>
  </g>
</g>
{cross(250, 480, 1.6, 46)}
{badge(500, 900, "SCREENSHOT BLOCKED", 1.8)}
""")

# 2. So who is it hiding your chats from? -------------------------------------------------------
eyes = "".join(
    f'<g transform="translate({x} 300)"><ellipse rx="34" ry="24" fill="#fff"/><circle cx="12" r="13" fill="#111">'
    f'<animate attributeName="cx" values="12;-10;12" dur="2.4s" repeatCount="indefinite"/></circle>'
    f'<rect x="-36" y="-26" width="72" height="0" fill="#040a07"><animate attributeName="height" values="0;0;50;0" keyTimes="0;0.85;0.92;1" dur="3s" repeatCount="indefinite"/></rect></g>'
    for x in (640, 730))
save(SLUG, "who", f"""
<g opacity="0">{fade(0.2, 0.3)}
  <g><animateTransform attributeName="transform" type="translate" values="-60 0;0 0" begin="0.2s" dur="0.5s" fill="freeze"/>
  <ellipse cx="686" cy="300" rx="130" ry="80" fill="#000" opacity="0.6" filter="url(#soft)"/>{eyes}</g>
</g>
{place(290, 120, 0.95, handset(chat(), "h2"))}
{pop(170, 300, '<circle r="90" class="fa2"/><text y="56" font-size="170" font-weight="700" text-anchor="middle" style="fill:#0a0a0a">?</text>', 0.5)}
""")

# 3. The AI assistant built into your own phone -------------------------------------------------
assist = (chat()
          + f'<rect x="0" y="0" width="{SW}" height="{SH}" fill="#000" opacity="0">{fade(0.5, 0.4, 0.45)}</rect>'
          + f'<rect x="4" y="4" width="{SW - 8}" height="{SH - 8}" rx="32" class="nf" stroke="#9b5cff" stroke-width="10" opacity="0" filter="url(#glow)">'
            f'{fade(0.5, 0.4)}<animate attributeName="stroke" values="#9b5cff;#8ab4ff;#ff5ca8;#9b5cff" dur="2s" repeatCount="indefinite"/></rect>')
save(SLUG, "assistant", f"""
{place(330, 80, 1.0, handset(assist, "h3"))}
<g opacity="0">{fade(0.6, 0.3)}<g><animateTransform attributeName="transform" type="translate" values="500 760;500 520" begin="0.6s" dur="0.6s" fill="freeze"/>
{orb("o3", 80)}</g></g>
{appear(label(500, 900, "Built into your phone", 48, "fa"), 1.3)}
""")

# 4. Gemini on Android and Siri on iPhone scan whatever is on your screen -----------------------
save(SLUG, "scan", f"""
{place(80, 120, 0.85, handset(chat() + scan_beam("b4a", 0.4), "h4a"))}
{place(630, 120, 0.85, handset(chat() + scan_beam("b4b", 0.9), "h4b"))}
{place(225, 690, 1, orb("o4a", 46))}
{place(775, 690, 1, orb("o4b", 46))}
{appear(label(225, 880, "Gemini", 48), 0.5)}
{appear(label(775, 880, "Siri", 48), 0.9)}
""")

# 5. Once captured, your chat can end up on a server Signal can't control -----------------------
copies = "".join(
    f'<g opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.85;1" begin="{0.6 + i * 0.5}s" dur="1.5s" repeatCount="indefinite"/>'
    f'<animateMotion path="M300 360 Q500 140 700 330" begin="{0.6 + i * 0.5}s" dur="1.5s" repeatCount="indefinite"/>'
    f'<rect x="-50" y="-22" width="100" height="44" rx="20" fill="{BLUE if i % 2 else GREY}"/>'
    f'<rect x="-32" y="-6" width="64" height="12" rx="6" fill="#fff" opacity="0.7"/></g>'
    for i in range(3))
save(SLUG, "server", f"""
{place(40, 170, 0.8, handset(chat(), "h5"))}
<path d="M300 360 Q500 140 700 330" class="nf sa" stroke-width="6" stroke-dasharray="14 14" opacity="0.6">
  <animate attributeName="stroke-dashoffset" from="0" to="-56" dur="0.8s" repeatCount="indefinite"/></path>
{copies}
{place(680, 280, 0.95, server())}
{place(400, 250, 1, orb("o5", 36))}
{appear(label(500, 880, "Somebody else's server", 46), 1.0)}
""")

# 6. Signal's president called that an existential threat -------------------------------------
cracks = ('<path d="M470 520 l30 40 l-22 34 l34 46" class="nf" stroke="#0a0a0a" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" '
          'pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" from="1" to="0" begin="1.0s" dur="0.4s" fill="freeze"/></path>'
          '<path d="M540 500 l-16 44 l26 26" class="nf" stroke="#0a0a0a" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" '
          'pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" from="1" to="0" begin="1.2s" dur="0.3s" fill="freeze"/></path>')
save(SLUG, "threat", f"""
{shadow(500, 790, 260, 26)}
<path d="M380 440 v-90 a120 120 0 0 1 240 0 v90" class="nf" stroke="url(#steel)" stroke-width="46"/>
<rect x="300" y="430" width="400" height="330" rx="44" fill="{BLUE}"/>
<rect x="300" y="430" width="400" height="60" rx="30" fill="#fff" opacity="0.15"/>
<path d="M500 540 a56 56 0 1 1 -40 96 l-30 12 l10 -30 a56 56 0 0 1 60 -78 z" fill="#fff"/>
{cracks}
<g opacity="0">{fade(0.4, 0.3)}<g><animateTransform attributeName="transform" type="translate" values="870 140;780 230;870 140" dur="3s" repeatCount="indefinite"/>{orb("o6", 60)}</g></g>
<g opacity="0">{fade(0.6, 0.3)}<polygon points="780,250 380,450 620,450" fill="#8ab4ff" opacity="0.25">
  <animate attributeName="opacity" values="0.1;0.35;0.1" dur="1s" repeatCount="indefinite"/></polygon></g>
{badge(500, 900, "EXISTENTIAL THREAT", 1.5)}
""")

# 7. So the app marks its window as secure: the screen is a stack of layers --------------------
def iso(f: float, inner: str, s: float = 0.8, e: float = 618) -> str:
    """Lay a screen-sized drawing (316 x 656) flat in isometric view, top corner at (e, f)."""
    a, b = 0.866 * s, 0.5 * s
    return f'<g transform="matrix({a:.3f} {b:.3f} {-a:.3f} {b:.3f} {e} {f})">{inner}</g>'


home = (f'<linearGradient id="s7wp" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1d3b6b"/><stop offset="1" stop-color="#5a2a7a"/></linearGradient>'
        f'<rect x="0" y="0" width="{SW}" height="{SH}" rx="34" fill="url(#s7wp)"/>'
        + "".join(f'<rect x="{30 + i * 70}" y="{90 + j * 90}" width="50" height="50" rx="14" fill="#fff" opacity="0.35"/>' for i in range(4) for j in range(5)))
sysui = (f'<rect x="0" y="0" width="{SW}" height="{SH}" rx="34" fill="#fff" opacity="0.06" stroke="#fff" stroke-opacity="0.5" stroke-width="4"/>'
         f'<rect x="20" y="14" width="60" height="14" rx="7" fill="#fff" opacity="0.8"/><rect x="240" y="14" width="56" height="14" rx="7" fill="#fff" opacity="0.8"/>'
         f'<rect x="108" y="{SH - 24}" width="100" height="10" rx="5" fill="#fff" opacity="0.8"/>')
secure = (f'{chat()}<rect x="0" y="0" width="{SW}" height="{SH}" rx="34" class="nf sa" stroke-width="10" opacity="0">{fade(1.2, 0.3)}'
          f'<animate attributeName="opacity" values="1;0.4;1" begin="1.5s" dur="1s" repeatCount="indefinite"/></rect>')
lift = lambda dy, inner: (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 {dy}" begin="0.3s" dur="0.7s" fill="freeze"/>{inner}</g>')
save(SLUG, "secure", f"""
{shadow(500, 800, 340, 26)}
{lift(110, iso(300, home))}
{iso(300, secure)}
{lift(-120, iso(300, sysui))}
{pop(250, 300, shield(0, 0, 0.75, "fa", lock_icon(0, 0, 0.6, "#0a0a0a")), 1.2)}
{badge(500, 910, "SECURE WINDOW", 1.5)}
""")

# 8. But here's the part most people miss: your eyes still see every message ------------------
sight = "".join(
    f'<line x1="392" y1="{y0}" x2="560" y2="{y1}" class="sa" stroke-width="5" stroke-dasharray="12 12" opacity="0">{fade(0.5, 0.3, 0.8)}'
    f'<animate attributeName="stroke-dashoffset" from="0" to="-48" dur="0.6s" repeatCount="indefinite"/></line>'
    for y0, y1 in ((464, 300), (466, 520), (468, 740)))
save(SLUG, "eyes", f"""
{place(340, 790, 1.0, person())}
{sight}
{place(560, 170, 0.92, handset(chat(0.2), "h8"))}
{tick(880, 210, 1.3)}
{appear(label(520, 900, "You still see every message", 48), 1.2)}
""")

# 9. Any screenshot or screen grab of that window comes out as an empty black box -------------
save(SLUG, "black", f"""
{place(80, 130, 0.9, handset(chat(), "h9"))}
{flash(91, 141, SW * 0.9, SH * 0.9, 0.6)}
<path d="M430 450 h110 m-30 -30 l30 30 l-30 30" class="nf sw" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" opacity="0">{fade(0.8)}</path>
<g opacity="0">{fade(1.0, 0.3)}{place(600, 150, 0.9, screenshot_card(SW, SH, ""))}</g>
{appear(label(233, 840, "On screen", 44), 0.3)}
{appear(label(742, 840, "Screenshot", 44, "fa"), 1.2)}
""")

# 10. The same kind of protection streaming services use to guard movies ----------------------
save(SLUG, "movies", f"""
{place(40, 230, 0.78, tv("t10", movie("m10")))}
{flash(51, 241, 446, 259, 0.8)}
<g opacity="0">{fade(1.1, 0.3)}<g transform="translate(570 262) rotate(3)">{screenshot_card(360, 210, "")}</g></g>
{appear(label(274, 640, "Movie playing", 42), 0.4)}
{appear(label(750, 640, "Its screenshot", 42, "fa"), 1.3)}
{badge(500, 850, "SAME TRICK", 1.6)}
""")

# 11. On Android it switches on by itself when an assistant tries to read the screen ----------
android_screen = (chat() + scan_beam("b11", 0.3, 1.2)
                  + f'<g opacity="0">{fade(1.4, 0.15)}{black()}</g>')
save(SLUG, "android", f"""
{place(240, 110, 0.95, handset(android_screen, "h11"))}
<g><animateTransform attributeName="transform" type="translate" values="820 160;720 260" dur="1.2s" fill="freeze"/>{orb("o11", 60)}</g>
{pop(660, 450, shield(0, 0, 1.1, "fa", lock_icon(0, 6, 0.75, "#0a0a0a")), 1.4)}
{appear(label(500, 900, "Screen security: on", 48, "fa"), 1.7)}
""")

# 12. On iPhone with iOS 27, Block Siri AI is on by default and hides chats in the app switcher -
def card(x: float, inner: str, uid: str, title_fill: str) -> str:
    return (f'<g transform="translate({x} 330) scale(0.62)">{shadow(SW / 2, SH + 20, SW * 0.6, 22)}'
            f'<clipPath id="{uid}"><rect x="0" y="0" width="{SW}" height="{SH}" rx="36"/></clipPath>'
            f'<g clip-path="url(#{uid})">{inner}</g>'
            f'<circle cx="30" cy="-40" r="22" fill="{title_fill}"/><rect x="64" y="-50" width="120" height="20" rx="10" fill="#fff" opacity="0.6"/></g>')


maps = (f'<rect x="0" y="0" width="{SW}" height="{SH}" fill="#d9e8d2"/>'
        f'<path d="M-20 200 q160 -60 360 40 M60 -20 q40 300 -40 700 M-20 480 q200 40 360 -60" class="nf" stroke="#fff" stroke-width="26"/>'
        f'<circle cx="170" cy="330" r="26" fill="{RED}"/>')
photos = (f'<rect x="0" y="0" width="{SW}" height="{SH}" fill="#14141a"/>'
          + "".join(f'<rect x="{6 + i * 104}" y="{6 + j * 104}" width="98" height="98" fill="{c}"/>'
                    for j in range(6) for i, c in enumerate(("#ff9f5c", "#5cd6ff", "#c27dff") if j % 2 else ("#7dffb0", "#ffd23f", "#ff5ca8"))))
signal_card = (f'<rect x="0" y="0" width="{SW}" height="{SH}" fill="#0e0e14"/>'
               f'<g opacity="1"><animate attributeName="opacity" from="1" to="0" begin="1.1s" dur="0.3s" fill="freeze"/>{chat()}</g>'
               f'<g opacity="0">{fade(1.1, 0.3)}<circle cx="{SW / 2}" cy="{SH / 2}" r="80" fill="{BLUE}"/>'
               f'<path d="M{SW / 2} {SH / 2 - 44} a44 44 0 1 1 -30 76 l-24 10 l8 -24 a44 44 0 0 1 46 -62 z" fill="#fff"/></g>')
toggle = (f'<rect x="-230" y="-50" width="460" height="100" rx="50" fill="#fff" fill-opacity="0.1" stroke="#fff" stroke-opacity="0.3" stroke-width="3"/>'
          f'<text x="-190" y="16" font-size="42">Block Siri AI</text>'
          f'<rect x="90" y="-30" width="110" height="60" rx="30" fill="#55555f"><animate attributeName="fill" from="#55555f" to="#3ddc84" begin="0.7s" dur="0.2s" fill="freeze"/></rect>'
          f'<circle cx="120" cy="0" r="24" fill="#fff"><animate attributeName="cx" from="120" to="170" begin="0.7s" dur="0.2s" fill="freeze"/></circle>')
save(SLUG, "iphone", f"""
{pop(500, 150, toggle, 0.2)}
<g><animateTransform attributeName="transform" type="translate" values="40 0;0 0" dur="1s" fill="freeze"/>
{card(40, maps, "s12a", "#3ddc84")}
{card(764, photos, "s12c", "#ffd23f")}
{card(402, signal_card, "s12b", BLUE)}
</g>
{appear(label(500, 900, "Hidden in the app switcher", 46, "fa"), 1.4)}
""")

# 13. But Signal admits it's incomplete: agents can still dig into files saved on the phone ----
folders = "".join(
    f'<g transform="translate({60 + i * 120} 0)"><path d="M0 10 h36 l10 12 h54 v70 h-100 z" fill="#ffc94d"/>'
    f'<rect x="0" y="30" width="100" height="62" rx="6" fill="#ffd97a"/></g>' for i in range(3))
grabbed = (f'<g opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.85;1" begin="1.0s" dur="1.8s" repeatCount="indefinite"/>'
           f'<animateMotion path="M520 690 Q640 520 780 300" begin="1.0s" dur="1.8s" repeatCount="indefinite"/>'
           f'<path d="M-40 -30 h30 l8 10 h42 v50 h-80 z" fill="#ffc94d"/><rect x="-40" y="-14" width="80" height="44" rx="5" fill="#ffd97a"/></g>')
save(SLUG, "files", f"""
{place(110, 90, 0.75, handset(black(), "h13"))}
{shield(237, 340, 0.9, "fa", lock_icon(0, 6, 0.6, "#0a0a0a"))}
<g opacity="0">{fade(0.3, 0.4)}
  <rect x="80" y="640" width="440" height="160" rx="24" fill="url(#steel)"/>
  <rect x="80" y="640" width="440" height="30" rx="15" fill="#fff" opacity="0.5"/>
  <g transform="translate(70 680)">{folders}</g>
</g>
<path d="M520 690 Q640 520 780 300" class="nf" stroke="#8ab4ff" stroke-width="5" stroke-dasharray="12 12" opacity="0">{fade(0.8, 0.3, 0.7)}</path>
{grabbed}
{place(800, 250, 1, orb("o13", 64))}
{appear(label(300, 870, "Files on the phone", 44), 0.5)}
{badge(760, 880, "INCOMPLETE", 1.6, "fa2")}
""")

# 14. And on a Mac, it can't block them at all ----------------------------------------------
mac_screen = (desktop_chat()
              + f'<rect x="0" y="-90" width="600" height="90" fill="url(#b14g)" opacity="0.9">'
                f'<animate attributeName="y" from="-90" to="370" begin="0.6s" dur="1.6s" repeatCount="indefinite"/></rect>'
              + '<linearGradient id="b14g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8ab4ff" stop-opacity="0"/>'
                '<stop offset="1" stop-color="#ffffff" stop-opacity="0.9"/></linearGradient>')
save(SLUG, "mac", f"""
{place(180, 280, 1.0, laptop("l14", mac_screen))}
{place(820, 170, 1, orb("o14", 60))}
{pop(170, 170, shield(0, 0, 0.8, "fa", lock_icon(0, 6, 0.55, "#0a0a0a")), 0.2)}
{cross(235, 230, 0.7, 46)}
{appear(label(500, 880, "No block on a Mac", 50, "fa2"), 0.6)}
""")

# 15. So that black screenshot isn't a glitch: your chat app is hiding from your own phone -----
hide = (chat()
        + f'<g opacity="0">{fade(1.3, 0.3)}{black(False)}{lock_icon(SW / 2, SH / 2 - 20, 1.1, BLUE)}</g>')
save(SLUG, "payoff", f"""
{place(330, 100, 1.0, handset(hide, "h15"))}
<g><animateTransform attributeName="transform" type="translate" values="880 140;800 220;880 140" dur="3s" repeatCount="indefinite"/>{orb("o15", 56)}</g>
<g opacity="0">{fade(1.6, 0.3)}<text x="830" y="390" font-size="100" font-weight="700" text-anchor="middle" class="fw">?</text></g>
{badge(500, 900, "HIDING FROM YOUR PHONE", 1.8)}
""")
