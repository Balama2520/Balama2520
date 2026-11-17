#!/usr/bin/env python3
"""Draws the animated SVG cards used by the profile README.

  python scripts/render_cards.py            -> animated cards (what you commit)
  STATIC=1 python scripts/render_cards.py   -> final frame, no animation (for screenshots)

Edit the text in this file, run it again, and commit the new files in cards/.
"""
import os
from html import escape as esc

STATIC = os.environ.get("STATIC") == "1"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cards")
os.makedirs(OUT, exist_ok=True)

# Palette taken from the ABMVSC banner: deep navy, electric blue, amber.
BG, PANEL, INK, MUTED, LINE = "#0b1220", "#111a2e", "#e8edf7", "#93a4c3", "#1f2c4a"
BLUE, AMBER, GREEN = "#4f8cff", "#ff9f1c", "#2dd4a0"
SERIF = "Georgia, 'Times New Roman', serif"
SANS = "'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', monospace"

CSS_ANIM = """
.a{opacity:0;animation:rise .7s cubic-bezier(.2,.8,.2,1) forwards}
.p{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .6s cubic-bezier(.2,.9,.3,1.3) forwards}
.g{transform-box:fill-box;transform-origin:left center;transform:scaleX(0);animation:grow .9s ease-out forwards}
.s{opacity:0;animation:swing 1s cubic-bezier(.2,.8,.2,1) forwards}
.b{animation:pulse 1.8s ease-in-out infinite}
.n{animation:nudge 1.6s ease-in-out infinite}
@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@keyframes pop{from{opacity:0;transform:scale(.6)}to{opacity:1;transform:scale(1)}}
@keyframes grow{to{transform:scaleX(1)}}
@keyframes swing{0%{opacity:0;transform:translateY(46px) rotate(-3deg)}60%{opacity:1;transform:translateY(-6px) rotate(.8deg)}100%{opacity:1;transform:none}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
@keyframes nudge{0%,100%{transform:translate(0,0)}50%{transform:translate(3px,-3px)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;opacity:1!important;transform:none!important}}
"""


def delay(sec):
    return f' style="animation-delay:{sec:.2f}s"'


def svg(w, h, label, body, defs=""):
    css = "" if STATIC else CSS_ANIM
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">'
        f"<defs>{defs}</defs><style>{css}text{{font-family:{SANS}}}</style>{body}</svg>"
    )


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


# --------------------------------------------------------------------------- hero
def hero():
    W, H = 1000, 300
    shine = "" if STATIC else (
        '<animateTransform attributeName="gradientTransform" type="translate" '
        'from="-1 0" to="1 0" dur="5s" repeatCount="indefinite"/>'
    )
    defs = f"""
<linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="{INK}"/><stop offset=".4" stop-color="{INK}"/>
<stop offset=".5" stop-color="#a8c8ff"/><stop offset=".6" stop-color="{INK}"/>
<stop offset="1" stop-color="{INK}"/>{shine}</linearGradient>
<linearGradient id="bar" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{AMBER}"/></linearGradient>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
<circle cx="2" cy="2" r="1.1" fill="#1b2744"/></pattern>"""

    lines = [
        (122, "✓ saarthi → live", GREEN, 1.2),
        (152, "✓ smart tasks → offline", GREEN, 1.7),
        (182, "✓ portfolio engine → open", GREEN, 2.2),
        (212, "› next: build more", BLUE, 2.7),
    ]
    term = "".join(
        f'<text class="a" x="702" y="{y}" font-size="15" fill="{c}" '
        f'style="font-family:{MONO};animation-delay:{t}s">{esc(txt)}</text>'
        for y, txt, c, t in lines
    )
    cursor = (
        f'<text class="b" x="838" y="212" font-size="15" fill="{BLUE}" '
        f'style="font-family:{MONO}">▌</text>'
    )

    body = f"""
<rect width="{W}" height="{H}" rx="20" fill="{BG}"/>
<rect width="{W}" height="{H}" rx="20" fill="url(#dots)"/>

<text class="a" x="60" y="84" font-size="17" fill="{BLUE}" font-weight="600"{delay(.1)}>Full-stack developer, applied AI</text>
<rect class="g" x="60" y="98" width="120" height="4" rx="2" fill="url(#bar)"{delay(.3)}/>
<text class="a" x="58" y="170" font-size="52" fill="url(#shine)" style="font-family:{SERIF};animation-delay:.35s">Bala Maneesh Ayanala</text>
<text class="a" x="60" y="212" font-size="21" fill="{MUTED}"{delay(.6)}>I build AI products end to end, and ship them live.</text>
<text class="a" x="60" y="242" font-size="15" fill="{MUTED}"{delay(.8)}>Founder of Saarthi AI. IEEE-published researcher.</text>

<g class="a"{delay(1.0)}>
<rect x="60" y="256" width="196" height="30" rx="15" fill="#0f2a22" stroke="{GREEN}" stroke-opacity=".5"/>
<circle class="b" cx="80" cy="271" r="5" fill="{GREEN}"/>
<text x="94" y="276" font-size="13" fill="{GREEN}" font-weight="600">Open to work in India</text>
</g>

<g class="a"{delay(.5)}>
<rect x="680" y="56" width="280" height="200" rx="14" fill="{PANEL}" stroke="{LINE}" stroke-width="2"/>
<circle cx="702" cy="80" r="5" fill="#ff5f57"/><circle cx="720" cy="80" r="5" fill="#febc2e"/><circle cx="738" cy="80" r="5" fill="#28c840"/>
</g>
{term}{cursor}
"""
    save("hero.svg", svg(W, H, "Bala Maneesh Ayanala, full-stack developer and applied AI engineer", body, defs))


# -------------------------------------------------------------------------- tiles
def tile(fname, color, tag, title, desc, tech, stat, stat_label, t):
    W, H = 330, 260
    d = "".join(
        f'<text x="24" y="{122 + i * 22}" font-size="14" fill="{MUTED}">{esc(x)}</text>'
        for i, x in enumerate(desc)
    )
    body = f"""
<g class="s" style="animation-delay:{t}s;transform-origin:165px 260px">
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="{PANEL}" stroke="{color}" stroke-opacity=".5" stroke-width="2"/>
<rect x="24" y="28" width="36" height="4" rx="2" fill="{color}"/>
<text x="24" y="56" font-size="13" fill="{color}" font-weight="600">{esc(tag)}</text>
<text class="n" x="306" y="56" font-size="20" fill="{color}" text-anchor="end">↗</text>
<text x="24" y="94" font-size="28" fill="{INK}" style="font-family:{SERIF}">{esc(title)}</text>
{d}
<text x="24" y="178" font-size="12" fill="{color}" style="font-family:{MONO}">{esc(tech)}</text>
<rect x="24" y="192" width="282" height="1" fill="{LINE}"/>
<text class="p" x="24" y="226" font-size="24" fill="{INK}" font-weight="700" style="animation-delay:{t + .5}s">{esc(stat)}</text>
<text class="a" x="24" y="246" font-size="12" fill="{MUTED}" style="animation-delay:{t + .7}s">{esc(stat_label)}</text>
</g>"""
    save(fname, svg(W, H, f"{title}: {' '.join(desc)}", body))


def tiles():
    tile("saarthi.svg", BLUE, "Live product", "Saarthi AI",
         ["Resume analysis, job matching,", "roadmaps and interview prep."],
         "React · FastAPI · PostgreSQL", "Solo-built", "founder and developer", 1.4)
    tile("smarttasks.svg", AMBER, "Live app", "Smart Tasks",
         ["No sign-up, works offline,", "voice input and a Pomodoro timer."],
         "PWA · JavaScript · Service Worker", "Offline-first", "installs like a real app", 1.7)
    tile("portfolio.svg", GREEN, "Open source tool", "Portfolio Engine",
         ["Fill a form, download a website.", "Free, with no account."],
         "HTML · CSS · JavaScript", "0 uploads", "everything runs in your browser", 2.0)


# -------------------------------------------------------------------------- proof
def proof():
    W, H = 1000, 150
    items = [
        ("92%", "mAP in IEEE-published", "SAR target detection", BLUE),
        ("Top 5%", "Smart India Hackathon 2024", "national finalist", AMBER),
        ("95+", "Lighthouse scores on the", "IBM internship app", GREEN),
        ("5,000+", "SAR images processed in", "the denoising pipeline", BLUE),
    ]
    cols = ""
    for i, (num, l1, l2, c) in enumerate(items):
        cx = 125 + i * 250
        t = 0.2 + i * 0.25
        cols += f"""
<text class="p" x="{cx}" y="72" font-size="42" fill="{c}" text-anchor="middle" style="font-family:{SERIF};animation-delay:{t}s">{esc(num)}</text>
<text class="a" x="{cx}" y="100" font-size="13" fill="{MUTED}" text-anchor="middle" style="animation-delay:{t + .2}s">{esc(l1)}</text>
<text class="a" x="{cx}" y="118" font-size="13" fill="{MUTED}" text-anchor="middle" style="animation-delay:{t + .25}s">{esc(l2)}</text>"""
        if i:
            cols += f'<rect x="{i * 250}" y="32" width="1" height="86" fill="{LINE}"/>'
    body = f'<rect width="{W}" height="{H}" rx="18" fill="{PANEL}" stroke="{LINE}" stroke-width="2"/>{cols}'
    save("proof.svg", svg(W, H, "Highlights: 92 percent mAP, Smart India Hackathon national finalist, 95+ Lighthouse, 5,000+ images", body))


# --------------------------------------------------------------------------- stack
def stack():
    W, H = 1000, 200
    rows = [
        ("Frontend", "React · TypeScript · JavaScript · Tailwind CSS · Redux"),
        ("Backend", "Node.js · Express · FastAPI · REST · WebSockets · JWT"),
        ("Data", "PostgreSQL · MongoDB · ChromaDB"),
        ("AI and ML", "RAG pipelines · LangChain · LLM integration · PyTorch · OpenCV"),
        ("Delivery", "Docker · AWS EC2 · GitHub Actions · Vercel · Netlify · Render"),
    ]
    out = ""
    for i, (k, v) in enumerate(rows):
        y = 44 + i * 30
        t = 0.15 + i * 0.18
        out += (
            f'<text class="a" x="40" y="{y}" font-size="15" fill="{BLUE}" font-weight="600" style="animation-delay:{t}s">{esc(k)}</text>'
            f'<text class="a" x="160" y="{y}" font-size="16" fill="{INK}" style="animation-delay:{t + .05}s">{esc(v)}</text>'
        )
    body = f'<rect width="{W}" height="{H}" rx="18" fill="{PANEL}" stroke="{LINE}" stroke-width="2"/>{out}'
    save("stack.svg", svg(W, H, "Tech stack", body))


if __name__ == "__main__":
    hero()
    tiles()
    proof()
    stack()
    print("cards written to", os.path.abspath(OUT), "(static)" if STATIC else "(animated)")
