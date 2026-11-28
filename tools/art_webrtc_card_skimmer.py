"""Illustrations for the 'webrtc-card-skimmer' video. Run:  python tools/art_webrtc_card_skimmer.py

A Black Friday card skimmer that copied card details at checkout and smuggled them out over a
WebRTC (video call) data channel, through Cloudflare's relay, past the store's server list.

Objects (phone with a checkout page, credit card, skimmer script, thief, server rack, laptop,
checkpoint gate, video call channel, relay cloud, storefront) are drawn once in their own
coordinates and placed with place(), so every scene can reuse them at any size.
"""
from artlib import appear, badge, bob, draw, fade, label, phone, pop, save, shadow, waves

SLUG = "webrtc-card-skimmer"
RED = "#ff3b3b"
GREEN = "#3ddc84"
BLUE = "#3557d6"
SKIN = "#f2c6a0"

PW, PH = 380, 720            # phone size
SW = PW - 24                 # phone screen width


def place(x: float, y: float, s: float, inner: str) -> str:
    return f'<g transform="translate({x} {y}) scale({s})">{inner}</g>'


# ---------------------------------------------------------------------------------------------
# Objects
# ---------------------------------------------------------------------------------------------
def credit_card(w: float = 300, tint: str = BLUE) -> str:
    """A bank card at (0,0), w wide."""
    h = w * 0.63
    k = w / 300
    return (f'<rect x="0" y="0" width="{w}" height="{h}" rx="{18 * k}" fill="{tint}"/>'
            f'<path d="M0 {h * 0.55} Q{w * 0.5} {h * 0.2} {w} {h * 0.45} V{h} H0 Z" fill="#fff" opacity="0.10"/>'
            f'<rect x="0" y="0" width="{w}" height="{h}" rx="{18 * k}" fill="none" stroke="#fff" stroke-opacity="0.35" stroke-width="{3 * k}"/>'
            f'<rect x="{28 * k}" y="{50 * k}" width="{52 * k}" height="{40 * k}" rx="{7 * k}" fill="#e8c15a"/>'
            f'<path d="M{28 * k} {70 * k} h{52 * k} M{54 * k} {50 * k} v{40 * k}" stroke="#a8862c" stroke-width="{3 * k}"/>'
            f'<path d="M{250 * k} {58 * k} q{10 * k} {12 * k} 0 {24 * k} M{262 * k} {50 * k} q{16 * k} {20 * k} 0 {40 * k}" '
            f'fill="none" stroke="#fff" stroke-width="{4 * k}" stroke-linecap="round" opacity="0.8"/>'
            + "".join(f'<rect x="{(28 + i * 64) * k}" y="{118 * k}" width="{52 * k}" height="{14 * k}" rx="{7 * k}" fill="#fff" opacity="0.85"/>'
                      for i in range(4))
            + f'<rect x="{28 * k}" y="{152 * k}" width="{110 * k}" height="{10 * k}" rx="{5 * k}" fill="#fff" opacity="0.5"/>')


def skimmer(eyes: bool = True) -> str:
    """The hidden script: a red code page with sneaky eyes, centred on (0,0), about 180x230."""
    lines = "".join(f'<rect x="{-60 + (i % 2) * 20}" y="{-30 + i * 26}" width="{100 - (i % 3) * 24}" height="12" rx="6" fill="#3a0a10" opacity="0.75"/>'
                    for i in range(4))
    e = ""
    if eyes:
        e = ('<g><animateTransform attributeName="transform" type="scale" values="1 1;1 1;1 0.1;1 1" keyTimes="0;0.9;0.95;1" '
             'dur="2.6s" repeatCount="indefinite" additive="sum"/>'
             '<ellipse cx="-30" cy="-70" rx="20" ry="16" fill="#fff"/><ellipse cx="30" cy="-70" rx="20" ry="16" fill="#fff"/>'
             '<circle cx="-24" cy="-68" r="9" fill="#111"><animate attributeName="cx" values="-36;-22;-36" dur="2s" repeatCount="indefinite"/></circle>'
             '<circle cx="36" cy="-68" r="9" fill="#111"><animate attributeName="cx" values="24;38;24" dur="2s" repeatCount="indefinite"/></circle></g>')
    return (f'{shadow(0, 128, 90, 16)}'
            f'<path d="M-90 -115 H50 L90 -75 V115 H-90 Z" class="fa"/>'
            f'<path d="M50 -115 V-75 H90 Z" fill="#000" opacity="0.3"/>'
            f'<rect x="-80" y="-105" width="20" height="210" rx="10" fill="#fff" opacity="0.18"/>'
            f'{lines}<text x="0" y="98" font-size="44" font-weight="700" text-anchor="middle" style="fill:#3a0a10">&lt;/&gt;</text>{e}')


def thief() -> str:
    """A hooded figure at a desk, feet of the bust at (0,0), about 300 wide and 320 tall."""
    return (f'{shadow(0, 6, 160, 18)}'
            f'<path d="M-150 0 q0 -150 150 -170 q150 20 150 170 z" fill="#24242c"/>'
            f'<path d="M-104 -150 q-6 -160 104 -170 q110 10 104 170 q-30 30 -104 34 q-74 -4 -104 -34 z" fill="#2e2e38"/>'
            f'<ellipse cx="0" cy="-185" rx="70" ry="84" fill="#0c0c10"/>'
            f'<ellipse cx="-26" cy="-190" rx="13" ry="7" class="fa"><animate attributeName="opacity" values="1;0.4;1" dur="1.6s" repeatCount="indefinite"/></ellipse>'
            f'<ellipse cx="26" cy="-190" rx="13" ry="7" class="fa"><animate attributeName="opacity" values="1;0.4;1" dur="1.6s" repeatCount="indefinite"/></ellipse>'
            f'<path d="M-60 -296 q60 -30 120 0" fill="none" stroke="#fff" stroke-opacity="0.12" stroke-width="10" stroke-linecap="round"/>')


def server(led: str = "fa", n: int = 4) -> str:
    """A rack server at (0,0), 220 wide, 70*n+40 tall, LEDs blinking."""
    h = 70 * n + 40
    units = []
    for j in range(n):
        y = 20 + j * 70
        units.append(f'<rect x="16" y="{y}" width="188" height="58" rx="8" fill="#15151b"/>'
                     + "".join(f'<rect x="{30 + i * 18}" y="{y + 14}" width="8" height="30" rx="3" fill="#3a3a46"/>' for i in range(6))
                     + f'<circle cx="160" cy="{y + 29}" r="8" class="{led}"><animate attributeName="opacity" values="1;0.15;1" begin="{j * 0.21}s" dur="0.8s" repeatCount="indefinite"/></circle>'
                     + f'<circle cx="184" cy="{y + 29}" r="8" fill="{GREEN}"><animate attributeName="opacity" values="0.2;1;0.2" begin="{j * 0.33}s" dur="1.1s" repeatCount="indefinite"/></circle>')
    return (f'{shadow(110, h + 6, 140, 18)}'
            f'<rect x="0" y="0" width="220" height="{h}" rx="18" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>'
            f'<rect x="10" y="6" width="200" height="8" rx="4" fill="#fff" opacity="0.12"/>{"".join(units)}')


def laptop(screen: str = "", uid: str = "l") -> str:
    """A laptop at (0,0): lid 520x330, base below it to y=360. `screen` is drawn in a 490x300 box."""
    return (f'{shadow(260, 372, 330, 20)}'
            f'<rect x="0" y="0" width="520" height="330" rx="22" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>'
            f'<clipPath id="{uid}scr"><rect x="15" y="15" width="490" height="300" rx="10"/></clipPath>'
            f'<rect x="15" y="15" width="490" height="300" rx="10" fill="url(#screen)"/>'
            f'<g clip-path="url(#{uid}scr)"><g transform="translate(15 15)">{screen}</g></g>'
            f'<circle cx="260" cy="8" r="3.5" fill="#000"/>'
            f'<path d="M-40 332 H560 L540 362 H-20 Z" fill="url(#steel)"/>'
            f'<rect x="210" y="332" width="100" height="10" rx="5" fill="#9a9aa6"/>')


def face(cx: float, cy: float, shirt: str, hair: str = "#2a1d18", talk: float = 0) -> str:
    """Head and shoulders for a video call tile, centred on (cx, cy) = face centre."""
    return (f'<path d="M{cx - 120} {cy + 190} q0 -110 120 -116 q120 6 120 116 z" fill="{shirt}"/>'
            f'<rect x="{cx - 20}" y="{cy + 40}" width="40" height="40" rx="10" fill="#e8b48c"/>'
            f'<circle cx="{cx}" cy="{cy}" r="62" fill="{SKIN}"/>'
            f'<path d="M{cx - 62} {cy - 10} q4 -66 66 -64 q56 2 60 60 q-40 -30 -126 4 z" fill="{hair}"/>'
            f'<circle cx="{cx - 22}" cy="{cy + 2}" r="7" fill="#1a1a1a"/><circle cx="{cx + 22}" cy="{cy + 2}" r="7" fill="#1a1a1a"/>'
            f'<ellipse cx="{cx}" cy="{cy + 32}" rx="16" ry="6" fill="#7a3f30">'
            f'<animate attributeName="ry" values="4;10;4" begin="{talk}s" dur="0.5s" repeatCount="indefinite"/></ellipse>')


def call_screen(shirt: str, hair: str, talk: float) -> str:
    """Video call UI inside a laptop screen box (490x300)."""
    return (f'<rect width="490" height="300" fill="#1d2a3a"/>{face(245, 130, shirt, hair, talk)}'
            f'<rect x="150" y="248" width="190" height="40" rx="20" fill="#000" opacity="0.55"/>'
            f'<circle cx="190" cy="268" r="13" fill="#fff"/><circle cx="245" cy="268" r="13" fill="#fff"/>'
            f'<circle cx="300" cy="268" r="13" fill="{RED}"/>'
            f'<circle cx="460" cy="26" r="9" fill="{RED}"><animate attributeName="opacity" values="1;0.2;1" dur="1s" repeatCount="indefinite"/></circle>')


def camera(cx: float, cy: float, s: float = 1, cls: str = "fw") -> str:
    """A video camera symbol: the sign of a video call channel."""
    return (f'<g transform="translate({cx} {cy}) scale({s})"><rect x="-46" y="-30" width="64" height="60" rx="12" class="{cls}"/>'
            f'<path d="M22 -6 L50 -26 V26 L22 6 Z" class="{cls}"/><circle cx="-14" cy="0" r="12" fill="#111" opacity="0.6"/></g>')


def channel(d: str, uid: str, cards: int = 3, dur: float = 2.4, begin: float = 0, cam: tuple | None = None,
            width: float = 74) -> str:
    """The video call data channel: a glowing tube along path `d`, with stolen cards riding through it."""
    tube = (f'<path d="{d}" fill="none" stroke="#fff" stroke-opacity="0.10" stroke-width="{width}" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" class="sa2" stroke-width="5" stroke-dasharray="18 16" stroke-linecap="round" opacity="0.8">'
            f'<animate attributeName="stroke-dashoffset" from="34" to="0" dur="0.5s" repeatCount="indefinite"/></path>')
    riders = "".join(
        f'<g opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.85;1" begin="{begin + i * dur / cards}s" '
        f'dur="{dur}s" repeatCount="indefinite"/><animateMotion path="{d}" begin="{begin + i * dur / cards}s" dur="{dur}s" '
        f'repeatCount="indefinite"/><g transform="translate(-36 -23)">{credit_card(72)}</g></g>'
        for i in range(cards))
    c = camera(*cam, 0.85, "fa2") if cam else ""
    return f'<g opacity="0">{fade(begin, 0.4)}{tube}{riders}{c}</g>'


def checkout(begin: float = 0.3, step: float = 0.18, cursor: bool = True) -> str:
    """A shop checkout page in phone-screen coordinates (356 wide). Card details type in from `begin`."""
    groups = ["4921", "7730", "5512", "0846"]
    out = [f'<rect width="{SW}" height="{PH - 24}" fill="#f4f2ee"/>',
           f'<rect width="{SW}" height="110" fill="#e6e1d8"/>',
           f'<path d="M30 70 h40 l-5 -32 h-30 z" class="fa2"/><path d="M38 40 q12 -22 24 0" fill="none" stroke="#111" stroke-width="4"/>',
           '<text x="88" y="70" font-size="36" font-weight="700" style="fill:#111">Checkout</text>',
           '<text x="24" y="166" font-size="24" style="fill:#666">Card number</text>',
           f'<rect x="20" y="180" width="{SW - 40}" height="66" rx="12" fill="#fff" stroke="#c9c3b8" stroke-width="3"/>',
           '<text x="24" y="296" font-size="24" style="fill:#666">Expiry</text>',
           '<text x="188" y="296" font-size="24" style="fill:#666">Security code</text>',
           '<rect x="20" y="310" width="150" height="66" rx="12" fill="#fff" stroke="#c9c3b8" stroke-width="3"/>',
           '<rect x="186" y="310" width="150" height="66" rx="12" fill="#fff" stroke="#c9c3b8" stroke-width="3"/>',
           f'<rect x="20" y="430" width="{SW - 40}" height="84" rx="20" fill="#16161c"/>',
           f'<text x="{SW / 2}" y="484" font-size="34" font-weight="700" text-anchor="middle">Pay now</text>',
           f'<rect x="60" y="560" width="{SW - 120}" height="14" rx="7" fill="#d6d0c4"/>',
           f'<rect x="90" y="592" width="{SW - 180}" height="14" rx="7" fill="#d6d0c4"/>']
    t = begin
    for i, g in enumerate(groups):
        out.append(f'<text x="{32 + i * 70}" y="224" font-size="28"font-weight="700" style="fill:#111" opacity="0">{fade(t, 0.08)}{g}</text>')
        t += step
    for x, txt in ((44, "08/29"), (232, "731")):
        out.append(f'<text x="{x}" y="355" font-size="31" font-weight="700" style="fill:#111" opacity="0">{fade(t, 0.08)}{txt}</text>')
        t += step
    if cursor:
        out.append(f'<rect x="30" y="195" width="4" height="36" fill="#111"><animate attributeName="opacity" values="1;0;1" dur="0.8s" repeatCount="indefinite"/>'
                   f'<animate attributeName="x" values="30;98;168;238;320" begin="{begin}s" dur="{step * 4}s" fill="freeze" calcMode="discrete"/></rect>')
    return "".join(out)


def gate(raise_at: float | None = None, bounce: bool = False) -> str:
    """A checkpoint: guard booth with the allowed-servers list and a striped barrier arm.
    Booth at (0,0)-(200,330); barrier pivot at (250,240); arm reaches to x=700."""
    stripes = "".join(f'<rect x="{30 + i * 84}" y="-14" width="42" height="28" fill="{RED}"/>' for i in range(5))
    arm = (f'<rect x="0" y="-14" width="450" height="28" rx="14" fill="#f4f4f8"/>{stripes}'
           f'<rect x="0" y="-14" width="450" height="28" rx="14" fill="none" stroke="#000" stroke-opacity="0.25" stroke-width="3"/>')
    anim = ""
    if raise_at is not None:
        anim = f'<animateTransform attributeName="transform" type="rotate" values="0;-70;-70;0" keyTimes="0;0.2;0.75;1" begin="{raise_at}s" dur="2.4s" fill="freeze"/>'
    return f"""{shadow(360, 340, 400, 22)}
<rect x="0" y="40" width="200" height="290" rx="12" fill="url(#steel)"/>
<path d="M-20 40 L100 -10 L220 40 Z" class="fa"/>
<rect x="24" y="80" width="152" height="96" rx="10" fill="url(#screen)"/>
<rect x="34" y="88" width="40" height="80" rx="6" fill="#fff" opacity="0.10"/>
<rect x="30" y="196" width="140" height="120" rx="8" fill="url(#paper)"/>
<text x="100" y="228" font-size="24" font-weight="700" text-anchor="middle" style="fill:#111">ALLOWED</text>
<text x="44" y="262" font-size="22" style="fill:#333">shop.com</text><path d="M146 254 l8 8 l14 -16" fill="none" stroke="{GREEN}" stroke-width="5"/>
<text x="44" y="296" font-size="22" style="fill:#333">pay.com</text><path d="M146 288 l8 8 l14 -16" fill="none" stroke="{GREEN}" stroke-width="5"/>
<rect x="232" y="200" width="36" height="140" rx="10" fill="url(#metal)"/>
<rect x="680" y="250" width="22" height="90" rx="8" fill="url(#metal)"/>
<g transform="translate(250 240)"><g>{anim}{arm}</g></g>
<circle cx="250" cy="240" r="24" fill="#2a2a33" stroke="#fff" stroke-opacity="0.4" stroke-width="4"/>"""


def envelope(cls: str = "fw") -> str:
    """A web request: a small letter centred on (0,0), 90x60."""
    return (f'<rect x="-45" y="-30" width="90" height="60" rx="8" class="{cls}"/>'
            f'<path d="M-45 -26 L0 6 L45 -26" fill="none" stroke="#111" stroke-opacity="0.5" stroke-width="5" stroke-linejoin="round"/>')


def relay_cloud(uid: str) -> str:
    """Cloudflare's relay: a cloud at (0,0) with a relay server inside, about 420x260."""
    return (f'{shadow(210, 270, 220, 18, 0.4)}'
            f'<path d="M60 250 a70 70 0 0 1 0 -140 a90 90 0 0 1 150 -60 a90 90 0 0 1 160 70 a65 65 0 0 1 -10 130 z" '
            f'fill="#fff" fill-opacity="0.13" stroke="#fff" stroke-opacity="0.5" stroke-width="5"/>'
            + place(150, 92, 0.55, server("fa2", 2)))


def browser(w: float, h: float, url: str, inner: str = "") -> str:
    """A browser window at (0,0), size w x h. `inner` is drawn below the address bar (y >= 70)."""
    return (f'{shadow(w / 2, h + 10, w * 0.5, 20)}'
            f'<rect x="0" y="0" width="{w}" height="{h}" rx="22" fill="#f4f2ee"/>'
            f'<path d="M0 22 a22 22 0 0 1 22 -22 h{w - 44} a22 22 0 0 1 22 22 v48 h-{w} z" fill="#2a2a33"/>'
            + "".join(f'<circle cx="{30 + i * 28}" cy="35" r="9" fill="{c}"/>' for i, c in enumerate((RED, "#ffbd2e", GREEN)))
            + f'<rect x="120" y="16" width="{w - 150}" height="38" rx="19" fill="#15151b"/>'
            f'<text x="146" y="45" font-size="26" style="fill:#ddd">{url}</text>{inner}')


def store_page(w: float) -> str:
    """Shop product grid inside a browser (y from 70)."""
    out = []
    for i in range(3):
        x = 30 + i * (w - 60) / 3
        cw = (w - 60) / 3 - 20
        out.append(f'<rect x="{x}" y="96" width="{cw}" height="{cw * 0.9}" rx="14" fill="#e3ddd2"/>'
                   f'<rect x="{x + cw * 0.2}" y="{96 + cw * 0.18}" width="{cw * 0.6}" height="{cw * 0.6}" rx="18" fill="{["#2f6b8f", "#9b4d3a", "#4a6b3a"][i]}"/>'
                   f'<rect x="{x}" y="{110 + cw * 0.9}" width="{cw * 0.8}" height="14" rx="7" fill="#c9c3b8"/>'
                   f'<rect x="{x}" y="{134 + cw * 0.9}" width="{cw * 0.4}" height="14" rx="7" fill="#e0a43a"/>')
    return "".join(out)


def monitor(screen: str, uid: str) -> str:
    """A desktop monitor at (0,0): 560x360 screen, stand below to y=470."""
    return (f'{shadow(280, 480, 200, 18)}'
            f'<path d="M230 360 L210 450 H350 L330 360 Z" fill="url(#steel)"/>'
            f'<rect x="170" y="450" width="220" height="22" rx="10" fill="url(#steel)"/>'
            f'<rect x="0" y="0" width="560" height="360" rx="20" fill="url(#metal)" stroke="#fff" stroke-opacity="0.3" stroke-width="4"/>'
            f'<clipPath id="{uid}m"><rect x="16" y="16" width="528" height="328" rx="8"/></clipPath>'
            f'<g clip-path="url(#{uid}m)"><g transform="translate(16 16)">{screen}</g></g>')


def storefront(uid: str) -> str:
    """A shop building at (0,0), 460 wide x 500 tall, with a locked front door."""
    awning = "".join(f'<path d="M{i * 46} 110 h46 v40 a23 23 0 0 1 -46 0 z" fill="{RED if i % 2 == 0 else "#f4f4f8"}"/>' for i in range(10))
    return f"""{shadow(230, 505, 280, 22)}
<rect x="0" y="40" width="460" height="460" rx="10" fill="#7a5a48"/>
<rect x="0" y="40" width="460" height="70" rx="10" fill="#5a3f32"/>
<text x="230" y="90" font-size="44" text-anchor="middle" class="display">SHOP</text>
{awning}
<rect x="30" y="200" width="200" height="190" rx="8" fill="url(#screen)" stroke="#d6d6de" stroke-width="8"/>
<path d="M50 220 l70 0 l-70 70 z" fill="#fff" opacity="0.10"/>
<rect x="270" y="200" width="160" height="300" rx="6" fill="#3a2a22" stroke="#d6d6de" stroke-width="8"/>
<rect x="290" y="222" width="120" height="110" rx="6" fill="url(#screen)"/>
<circle cx="400" cy="380" r="9" fill="#e8c15a"/>
<g transform="translate(350 420)"><path d="M-26 -10 v-22 a26 26 0 0 1 52 0 v22" fill="none" stroke="#d6d6de" stroke-width="10"/>
<rect x="-40" y="-12" width="80" height="64" rx="12" fill="#e8c15a"/><circle cx="0" cy="16" r="9" fill="#5a4210"/>
<rect x="-4" y="16" width="8" height="20" fill="#5a4210"/></g>"""


def phone_shadow(x: float, y: float, s: float) -> str:
    return shadow(x + PW * s / 2, y + PH * s + 16, PW * s * 0.6, 20)


# ---------------------------------------------------------------------------------------------
# Scenes
# ---------------------------------------------------------------------------------------------

# 1. Hidden code on five shopping sites copies your card as you type -----------------------------
PX, PY, PS = 90, 80, 0.98
flyers = "".join(
    f'<g opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.8;1" begin="{1.0 + i * 0.7}s" dur="1.4s" repeatCount="indefinite"/>'
    f'<animateMotion path="M276 300 Q 560 150 740 420" begin="{1.0 + i * 0.7}s" dur="1.4s" repeatCount="indefinite"/>'
    f'<g transform="translate(-45 -28)">{credit_card(90, RED)}</g></g>' for i in range(2))
save(SLUG, "hook", f"""
{phone_shadow(PX, PY, PS)}
{place(PX, PY, PS, phone(0, 0, PW, PH, checkout(0.3)))}
<rect x="114" y="262" width="324" height="78"rx="14" class="nf sa" stroke-width="6" opacity="0">
  <animate attributeName="opacity" values="0;1;0.3;1" begin="1.0s" dur="1s" fill="freeze"/></rect>
{flyers}
{pop(770, 470, place(0, 0, 1.3, skimmer()), 0.6)}
{badge(500, 905, "HIDDEN ON 5 SHOPPING SITES", 1.6)}
""")

# 2. So how did it get stolen cards past the stores' security? ----------------------------------
save(SLUG, "question", f"""
{place(30, 380, 0.9, gate())}
{place(740, 360, 0.95, server(n=4))}
{appear(label(850, 790, "Thief's server", 40, "fa"), 0.5)}
<g><animateMotion path="M110 150 L420 520" dur="1.0s" fill="freeze"/>
  <g transform="translate(-60 -38)">{credit_card(120)}</g></g>
{pop(560, 190, '<circle r="88" class="fa2"/><text y="56" font-size="170" font-weight="700" text-anchor="middle" style="fill:#0a0a0a">?</text>', 1.1)}
{appear(label(250, 790, "Store security", 40), 0.5)}
""")

# 3. It smuggled them out through the tech your browser uses for video calls ---------------------
save(SLUG, "smuggle", f"""
{phone_shadow(40, 170, 0.75)}
{place(40, 170, 0.75, phone(0, 0, PW, PH, checkout(0, 0.01, False)))}
{place(720, 440, 0.55, thief())}
{channel("M300 420 C 440 200, 600 200, 700 470", "s3", 3, 2.2, 0.4, (500, 262))}
{place(680, 420, 0.9, server(n=3))}
{badge(500, 905, "DISGUISED AS A VIDEO CALL", 1.3)}
""")

# 4. That feature lets a web page open a channel to someone else and pass data -------------------
packets = "".join(
    f'<rect x="-14" y="-14" width="28" height="28" rx="6" class="{"fa2" if i % 2 else "fw"}" opacity="0">'
    f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.9;1" begin="{0.8 + i * 0.35}s" dur="1.4s" repeatCount="indefinite"/>'
    f'<animateMotion path="{"M350 300 Q500 200 650 300" if i % 2 == 0 else "M650 360 Q500 470 350 360"}" begin="{0.8 + i * 0.35}s" dur="1.4s" repeatCount="indefinite"/></rect>'
    for i in range(4))
save(SLUG, "video-call", f"""
{place(40, 230, 0.55, laptop(call_screen("#2f6b8f", "#2a1d18", 0.0), "a"))}
{place(660, 230, 0.55, laptop(call_screen("#9b4d3a", "#6b4a2a", 0.25), "b"))}
<path d="M350 300 Q500 200 650 300" class="nf sw" stroke-width="5" stroke-dasharray="12 12" opacity="0.5"/>
<path d="M650 360 Q500 470 350 360" class="nf sw" stroke-width="5" stroke-dasharray="12 12" opacity="0.5"/>
{packets}
{camera(500, 345, 1.0, "fa2")}
{appear('<text x="500" y="640" font-size="120" text-anchor="middle" class="display fa">WebRTC</text>', 0.6)}
{appear(label(500, 880, "A direct channel for video calls", 44), 1.2)}
""")

# 5. It slipped in through a cookie banner, an ad pixel, or the store's own files ---------------
banner = (f'<rect x="0" y="330" width="640" height="150" fill="#16161c"/>'
          f'<text x="30" y="380" font-size="28">We use cookies</text>'
          f'<rect x="30" y="398" width="320" height="12" rx="6" fill="#fff" opacity="0.3"/>'
          f'<rect x="30" y="420" width="250" height="12" rx="6" fill="#fff" opacity="0.3"/>'
          f'<rect x="440" y="370" width="170" height="70" rx="16" class="fa2"/>'
          f'<text x="525" y="416" font-size="30" font-weight="700" text-anchor="middle" style="fill:#111">Accept</text>')
pixel = '<rect x="596" y="84" width="16" height="16" fill="#ff8a3d"/>'
ring = lambda x, y, w, h, b: (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" class="nf sa" stroke-width="7" opacity="0" filter="url(#glow)">'
                              f'<animate attributeName="opacity" values="0;1;0.4;1" begin="{b}s" dur="0.8s" fill="freeze"/></rect>')
save(SLUG, "ways-in", f"""
{place(30, 150, 1.0, browser(640, 480, "shop.com", store_page(640) + banner + pixel))}
{place(740, 250, 1.0, server(n=4))}
{ring(30, 470, 640, 160, 0.4)}
{ring(616, 224, 36, 36, 0.9)}
{ring(732, 242, 236, 336, 1.4)}
{pop(375, 555, place(0, 0, 0.42, skimmer(False)), 0.6)}
{pop(640, 200, place(0, 0, 0.32, skimmer(False)), 1.1)}
{pop(850, 220, place(0, 0, 0.42, skimmer(False)), 1.6)}
{appear(label(500, 760, "Cookie banner · Ad pixel · Store files", 42), 1.9)}
""")

# 6. It only woke up on phones, and on one site, only at checkout --------------------------------
zzz = "".join(f'<text x="{0 + i * 30}" y="{-i * 40}" font-size="{40 + i * 12}" font-weight="700" class="fw" opacity="0">'
              f'<animate attributeName="opacity" values="0;1;0" begin="{i * 0.4}s" dur="1.6s" repeatCount="indefinite"/>Z</text>' for i in range(3))
save(SLUG, "phones-only", f"""
<g opacity="0.55">{place(20, 220, 0.85, monitor(f'<rect width="528" height="328" fill="#f4f2ee"/><g transform="scale(0.8)">{store_page(660)}</g>', "m6"))}</g>
<g transform="translate(250 460)">{place(-38, -48, 0.42, skimmer(False))}<g transform="translate(40 -60)">{zzz}</g></g>
{phone_shadow(620, 140, 0.82)}
{place(620, 140, 0.82, phone(0, 0, PW, PH, checkout(0.9, 0.15, False)))}
{pop(860, 200, place(0, 0, 0.75, skimmer()), 0.5)}
{waves(860, 200, "sa", 3, 50, 120, 1.4, 6, start=0.6)}
{appear(label(260, 800, "Computer: asleep", 42), 0.3)}
{appear(label(775, 800, "Phone: awake", 42, "fa"), 0.8)}
""")

# 7. Card number, expiry, security code: all copied before the payment was even checked ----------
grab = "".join(
    f'<g opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.8;1" begin="{b}s" dur="0.9s" fill="freeze"/>'
    f'<animateMotion path="M{sx} {sy} Q 620 {sy - 120} 780 280" begin="{b}s" dur="0.9s" fill="freeze"/>'
    f'<text x="0" y="12" font-size="40" font-weight="700" text-anchor="middle" class="fa">{t}</text></g>'
    for sx, sy, t, b in ((290, 350, "4921 7730…", 1.2), (157, 545, "08/29", 1.6), (400, 545, "731", 1.9)))
save(SLUG, "copied", f"""
{place(20, 40, 1.45, f'<clipPath id="s7c"><rect x="0" y="0" width="{SW}" height="420"/></clipPath><g clip-path="url(#s7c)">{checkout(0.2, 0.16)}</g>')}
{shadow(278, 668, 280, 18)}
{pop(780, 260, place(0, 0, 1.0, skimmer()), 0.4)}
{grab}
{badge(500, 905, "COPIED BEFORE PAYMENT", 2.2)}
""")

# 8. A store can block every server except the ones it lists ------------------------------------
save(SLUG, "the-list", f"""
{place(20, 200, 1.15, gate(raise_at=0.4))}
<g><animateMotion path="M940 470 L330 470"begin="0.4s" dur="2.0s" fill="freeze"/><animate attributeName="opacity" from="1" to="0" begin="2.2s" dur="0.3s" fill="freeze"/>{envelope("fw")}
  <text x="0" y="-48" font-size="30" text-anchor="middle">pay.com</text></g>
<g opacity="0">{fade(3.0)}<animateMotion path="M910 470 L872 470 L910 470" keyTimes="0;0.5;1" begin="3.0s" dur="1.6s" repeatCount="indefinite"/>
  {envelope("fa")}<text x="0" y="-48" font-size="30" text-anchor="middle" class="fa">unknown.com</text></g>
{appear(label(500, 880, "Only listed servers get through", 46), 1.0)}
""")

# 9. But that list doesn't cover video call channels -------------------------------------------
save(SLUG, "not-covered", f"""
{place(170, 380, 0.9, gate())}
<g><animateMotion path="M920 520 L700 520 L640 520 L900 520" keyTimes="0;0.45;0.55;1" dur="1.8s" repeatCount="indefinite"/>{envelope("fa")}</g>
{channel("M80 300 C 300 100, 700 100, 930 300", "s9", 3, 2.2, 0.8, (505, 152))}
{pop(500, 300, f'<rect x="-120" y="-36" width="240" height="72" rx="20" fill="#fff" fill-opacity="0.12" stroke="#fff" stroke-opacity="0.4" stroke-width="3"/><text y="14" font-size="40" font-weight="700" text-anchor="middle" class="fa2">Not on the list</text>', 1.4)}
{appear(label(500, 890, "Video calls slip past the guard", 46), 1.8)}
""")

# 10. The script needed just two ordinary requests to set up the call ---------------------------
save(SLUG, "two-requests", f"""
{phone_shadow(50, 190, 0.7)}
{place(50, 190, 0.7, phone(0, 0, PW, PH, checkout(0, 0.01, False)))}
{place(730, 280, 0.95, server(n=4))}
{pop(200, 150, place(0, 0, 0.5, skimmer()), 0.2)}
<g opacity="0">{fade(0.5, 0.1)}<animateMotion path="M330 330 L720 330" begin="0.5s" dur="0.7s" fill="freeze"/>{envelope("fw")}</g>
<g opacity="0">{fade(1.1, 0.1)}<animateMotion path="M330 450 L720 450" begin="1.1s" dur="0.7s" fill="freeze"/>{envelope("fw")}</g>
{appear('<text x="525" y="250" font-size="170" text-anchor="middle" class="display fa2">2</text>', 1.4)}
{channel("M330 580 L730 580", "s10", 2, 1.6, 2.0, (525, 650), 60)}
{appear(label(500, 900, "Two requests, then the call opens", 46), 1.8)}
""")

# 11. Then everything flowed through Cloudflare's relay, looking like a normal video call -------
save(SLUG, "relay", f"""
{phone_shadow(20, 300, 0.6)}
{place(20, 300, 0.6, phone(0, 0, PW, PH, checkout(0, 0.01, False)))}
{place(290, 130, 1.0, relay_cloud("r"))}
{place(780, 400, 0.85, server(n=4))}
{appear(label(500, 100, "Cloudflare relay", 44, "fa2"), 0.4)}
{channel("M240 520 C 330 520, 360 420, 450 400", "s11a", 2, 1.4, 0.3)}
{channel("M560 400 C 650 420, 700 520, 790 540", "s11b", 2, 1.4, 1.0)}
{pop(500, 620, camera(0, 0, 1.4, "fw"), 1.5)}
{appear(label(500, 880, "Looks like a normal video call", 46), 1.8)}
""")

# 12. Even the skimmer's own code arrived in chunks over that channel ---------------------------
chunk = lambda i: (f'<rect x="-50" y="-30" width="100" height="60" rx="10" class="fa"/>'
                   f'<rect x="-36" y="-10" width="{50 + (i % 2) * 20}" height="10" rx="5" fill="#3a0a10" opacity="0.75"/>')
chunks = "".join(
    f'<g opacity="0">{fade(0.3 + i * 0.4, 0.1)}<animateMotion path="M880 {260 + i * 10} L{560 if True else 0} {260 + i * 10} L{430} {330 + i * 70}" '
    f'begin="{0.3 + i * 0.4}s" dur="0.8s" fill="freeze"/><animate attributeName="opacity" from="1" to="0" begin="2.1s" dur="0.3s" fill="freeze"/>{chunk(i)}</g>' for i in range(4))
save(SLUG, "chunks", f"""
{place(720, 360, 0.95, server(n=4))}
{channel("M790 300 C 640 220, 480 220, 360 300", "s12", 0, 1.6, 0, None, 60)}
{phone_shadow(260, 230, 0.7)}
{place(260, 230, 0.7, phone(0, 0, PW, PH, ""))}
{chunks}
<g opacity="0">{fade(2.1, 0.3)}{place(430, 440, 0.9, skimmer())}</g>
{pop(560, 580, f'<circle r="44" fill="{GREEN}"/><path d="M-20 0 l14 15 l26 -30" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>', 2.5)}
{appear(label(500, 900, "Sent in pieces, checked, then run", 46), 2.0)}
""")

# 13. Researchers at InfoHawk caught it; all five stores removed it by November 25 ---------------
glass = (f'<circle r="120" fill="#fff" fill-opacity="0.12" stroke="#d6d6de" stroke-width="22"/>'
         f'<line x1="86" y1="86" x2="190" y2="190" stroke="url(#metal)" stroke-width="40" stroke-linecap="round"/>'
         f'<path d="M-70 -50 a90 90 0 0 1 50 -50" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" opacity="0.6"/>')
save(SLUG, "caught", f"""
{place(80, 120, 1.3, browser(640, 470, "shop.com/checkout", store_page(640)))}
<g><animate attributeName="opacity" from="1" to="0" begin="2.0s" dur="0.4s" fill="freeze"/>
  {place(540, 470, 1.0, skimmer())}</g>
<g transform="translate(250 280)"><animateTransform attributeName="transform" type="translate" values="250 280;520 460" dur="1.2s" fill="freeze"/>{glass}</g>
<path d="M430 340 L650 600 M650 340 L430 600" stroke="{RED}" stroke-width="24" stroke-linecap="round" opacity="0">{fade(1.5, 0.2)}
  <animate attributeName="opacity" from="1" to="0" begin="2.0s" dur="0.4s" fill="freeze"/></path>
{badge(500, 905, "REMOVED BY NOV 25", 2.2)}
""")

# 14. Your card didn't leave through the web; it left on a video call nobody was watching -------
save(SLUG, "payoff", f"""
{place(60, 290, 0.95, storefront("p"))}
{channel("M300 330 C 420 110, 700 110, 860 300", "s14", 3, 2.0, 0.6, (580, 172))}
{place(760, 300, 0.75, server(n=4))}
{appear(label(280, 840, "Front door: locked", 42), 0.3)}
{badge(500, 930, "LEFT ON A VIDEO CALL", 1.4)}
""")
