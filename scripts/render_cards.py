#!/usr/bin/env python3
"""Draws the animated SVG cards used by the profile README.

  python scripts/render_cards.py            -> animated cards (what you commit)
  STATIC=1 python scripts/render_cards.py   -> final frame, no animation (for screenshots)

Edit the data in this file, run it again, and commit the new files in cards/.
Palette mirrors https://abms-portfolio.netlify.app/  (--bg: #0f172a, --accent: #6366f1, etc.)
"""
import os
from html import escape as esc

STATIC = os.environ.get("STATIC") == "1"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cards")
os.makedirs(OUT, exist_ok=True)

# ── Palette (from portfolio CSS variables) ────────────────────────────────────
BG      = "#0f172a"   # --bg        deep navy (body background)
PANEL   = "#1e293b"   # --surface   card surface
BORDER  = "#334155"   # --border    card border
INK     = "#f1f5f9"   # --text      primary text
MUTED   = "#94a3b8"   # --muted     secondary text
ACCENT  = "#6366f1"   # --accent    indigo (links, highlights)
ORANGE  = "#f97316"   # --orange    studio / warm accent
GREEN   = "#10b981"   # --green     live / success
BLUE    = "#38bdf8"   # --sky       code / tech labels

SERIF = "Georgia, 'Times New Roman', serif"
SANS  = "'Inter', 'Segoe UI', Helvetica, Arial, sans-serif"
MONO  = "'SFMono-Regular', Consolas, 'Liberation Mono', monospace"

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


# ─────────────────────────────────────────────────────────────── hero ─────────
def hero():
    W, H = 1000, 320
    shine_anim = "" if STATIC else (
        '<animateTransform attributeName="gradientTransform" type="translate" '
        'from="-1 0" to="1 0" dur="6s" repeatCount="indefinite"/>'
    )
    defs = f"""
<linearGradient id="hero-shine" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="{INK}"/>
<stop offset=".38" stop-color="{INK}"/>
<stop offset=".5" stop-color="#a5b4fc"/>
<stop offset=".62" stop-color="{INK}"/>
<stop offset="1" stop-color="{INK}"/>{shine_anim}</linearGradient>
<linearGradient id="accent-bar" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="{ACCENT}"/>
<stop offset="1" stop-color="{ORANGE}"/></linearGradient>
<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
<path d="M 28 0 L 0 0 0 28" fill="none" stroke="#1e293b" stroke-width="1"/>
</pattern>"""

    # Terminal lines (right panel) — mirrors portfolio "projects I've shipped"
    term_lines = [
        (110, "✦ saarthi-link    →  live", GREEN,  1.3),
        (140, "✦ giakaa-cms      →  live", GREEN,  1.8),
        (170, "✦ smart-tasks     →  live", GREEN,  2.3),
        (200, "✦ avr-shop        →  live", GREEN,  2.8),
        (230, "› next: build more ↗",       ACCENT, 3.3),
    ]
    term = "".join(
        f'<text class="a" x="688" y="{y}" font-size="13.5" fill="{c}" '
        f'style="font-family:{MONO};animation-delay:{t}s">{esc(txt)}</text>'
        for y, txt, c, t in term_lines
    )
    cursor = (
        f'<text class="b" x="852" y="230" font-size="14" fill="{ACCENT}" '
        f'style="font-family:{MONO}">▌</text>'
    )

    body = f"""
<rect width="{W}" height="{H}" rx="20" fill="{BG}"/>
<rect width="{W}" height="{H}" rx="20" fill="url(#grid)" opacity=".35"/>

<!-- eyebrow -->
<text class="a" x="52" y="62" font-size="13" fill="{MUTED}" font-weight="500"{delay(.05)}>Available for work · Bangalore · Hyderabad · Remote</text>

<!-- name -->
<text class="a" x="50" y="130" font-size="54" fill="url(#hero-shine)" style="font-family:{SERIF};animation-delay:.2s">Bala Maneesh Ayanala</text>

<!-- accent bar under name -->
<rect class="g" x="50" y="142" width="260" height="3" rx="1.5" fill="url(#accent-bar)"{delay(.4)}/>

<!-- title -->
<text class="a" x="52" y="180" font-size="22" fill="{ACCENT}" font-weight="700"{delay(.55)}>Full-Stack Developer &amp; AI Engineer</text>

<!-- tagline -->
<text class="a" x="52" y="210" font-size="14.5" fill="{MUTED}"{delay(.7)}>I build production-ready web apps and AI-powered tools —</text>
<text class="a" x="52" y="230" font-size="14.5" fill="{MUTED}"{delay(.8)}>React · Node.js · LangChain · RAG · AWS. Founder of ABMVSC Studio.</text>

<!-- tags row -->
<g class="a"{delay(1.0)}>
  <rect x="52" y="250" width="148" height="26" rx="13" fill="#1e1b4b" stroke="{ACCENT}" stroke-opacity=".5"/>
  <text x="126" y="268" font-size="12" fill="{ACCENT}" font-weight="600" text-anchor="middle">IEEE Published</text>
</g>
<g class="a"{delay(1.1)}>
  <rect x="210" y="250" width="128" height="26" rx="13" fill="#1c1917" stroke="{ORANGE}" stroke-opacity=".5"/>
  <text x="274" y="268" font-size="12" fill="{ORANGE}" font-weight="600" text-anchor="middle">SIH Top 5%</text>
</g>
<g class="a"{delay(1.2)}>
  <rect x="348" y="250" width="136" height="26" rx="13" fill="#052e16" stroke="{GREEN}" stroke-opacity=".5"/>
  <circle class="b" cx="366" cy="263" r="4" fill="{GREEN}"/>
  <text x="414" y="268" font-size="12" fill="{GREEN}" font-weight="600" text-anchor="middle">Open to work</text>
</g>

<!-- right: terminal panel -->
<g class="a"{delay(.5)}>
  <rect x="666" y="52" width="300" height="230" rx="14" fill="{PANEL}" stroke="{BORDER}" stroke-width="1.5"/>
  <circle cx="689" cy="76" r="5" fill="#ff5f57"/>
  <circle cx="707" cy="76" r="5" fill="#febc2e"/>
  <circle cx="725" cy="76" r="5" fill="#28c840"/>
  <text x="744" y="81" font-size="12" fill="{MUTED}" style="font-family:{MONO}">~/abmvsc</text>
</g>
{term}{cursor}
"""
    save("hero.svg", svg(W, H, "Bala Maneesh Ayanala — Full-Stack Developer & AI Engineer. Founder of ABMVSC Studio.", body, defs))


# ──────────────────────────────────────────────────────────── stat bar ─────────
def proof():
    """4-column stat bar — mirrors the hero stat-row on the portfolio."""
    W, H = 1000, 160
    items = [
        ("3+",      "Live Products",        "shipped & running",           ACCENT),
        ("Top 5%",  "SIH 2024 Finalist",    "10,000+ teams nationally",    ORANGE),
        ("92%",     "mAP on SAR Detection", "IEEE-published · YOLOv8+DAE", GREEN),
        ("5,000+",  "SAR Images Processed", "PSNR 29.95 · SSIM 0.99",     BLUE),
    ]
    cols = ""
    for i, (num, l1, l2, c) in enumerate(items):
        cx = 125 + i * 250
        t  = 0.2 + i * 0.22
        cols += f"""
<text class="p" x="{cx}" y="76" font-size="40" fill="{c}" text-anchor="middle" style="font-family:{SERIF};animation-delay:{t}s">{esc(num)}</text>
<text class="a" x="{cx}" y="106" font-size="13" fill="{INK}" text-anchor="middle" font-weight="600" style="animation-delay:{t+.2}s">{esc(l1)}</text>
<text class="a" x="{cx}" y="124" font-size="11.5" fill="{MUTED}" text-anchor="middle" style="animation-delay:{t+.25}s">{esc(l2)}</text>"""
        if i:
            cols += f'<rect x="{i*250}" y="28" width="1" height="104" fill="{BORDER}"/>'
    body = f'<rect width="{W}" height="{H}" rx="18" fill="{PANEL}" stroke="{BORDER}" stroke-width="1.5"/>{cols}'
    save("proof.svg", svg(W, H, "Highlights: 3+ live products, SIH top 5%, 92% mAP IEEE paper, 5000+ SAR images", body))


# ───────────────────────────────────────────────────────── project tiles ───────
def tile(fname, color, tag, title, desc, tech, stat, stat_label, t):
    W, H = 330, 270
    d = "".join(
        f'<text x="24" y="{118 + i * 22}" font-size="13.5" fill="{MUTED}">{esc(x)}</text>'
        for i, x in enumerate(desc)
    )
    body = f"""
<g class="s" style="animation-delay:{t}s;transform-origin:165px 270px">
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="{PANEL}" stroke="{color}" stroke-opacity=".45" stroke-width="1.5"/>
<rect x="24" y="26" width="32" height="3" rx="1.5" fill="{color}"/>
<text x="24" y="54" font-size="12.5" fill="{color}" font-weight="600">{esc(tag)}</text>
<text class="n" x="{W-24}" y="54" font-size="18" fill="{color}" text-anchor="end">↗</text>
<text x="24" y="92" font-size="26" fill="{INK}" style="font-family:{SERIF}">{esc(title)}</text>
{d}
<text x="24" y="178" font-size="11.5" fill="{BLUE}" style="font-family:{MONO}">{esc(tech)}</text>
<rect x="24" y="192" width="282" height="1" fill="{BORDER}"/>
<text class="p" x="24" y="230" font-size="26" fill="{INK}" font-weight="700" style="animation-delay:{t+.5}s">{esc(stat)}</text>
<text class="a" x="24" y="250" font-size="11.5" fill="{MUTED}" style="animation-delay:{t+.7}s">{esc(stat_label)}</text>
</g>"""
    save(fname, svg(W, H, f"{title}: {' '.join(desc)}", body))


def tiles():
    tile("saarthi.svg",    ACCENT, "AI Career Platform",   "Saarthi Link",
         ["ATS scoring, 30/90-day", "roadmaps & interview prep."],
         "React · FastAPI · ChromaDB · PostgreSQL",
         "Solo-built", "founder & full-stack developer", 1.4)

    tile("giakaa.svg",     ORANGE, "CMS Platform",          "Giakaa CMS",
         ["Dual-DB CMS with SEO,", "OpenGraph & XSS guard."],
         "React · Node.js · PostgreSQL · MongoDB · Docker",
         "−40%", "API latency via query optimisation", 1.7)

    tile("smarttasks.svg", GREEN,  "Offline PWA",           "Smart Tasks",
         ["No sign-up. Voice input,", "Pomodoro & localStorage."],
         "HTML5 · CSS3 · Vanilla JS · Service Worker",
         "95+", "Lighthouse — fully offline", 2.0)

    tile("avrshop.svg",    BLUE,   "AgriTech E-Commerce",   "AVR Shop",
         ["Digital marketplace for", "farmers + AI advisor."],
         "React · Node.js · Express · MongoDB",
         "MERN", "stack with integrated AI", 2.3)


# ─────────────────────────────────────────────────────────── tech stack ────────
def stack():
    W, H = 1000, 220
    rows = [
        ("Frontend",  "React · TypeScript · JavaScript · Tailwind CSS · Redux · HTML5 · CSS3"),
        ("Backend",   "Node.js · Express · FastAPI · REST APIs · WebSockets · JWT"),
        ("Data",      "PostgreSQL · MongoDB · ChromaDB · NumPy · Pandas"),
        ("AI & ML",   "LangChain · RAG Pipelines · LLM Integration · PyTorch · YOLOv8 · OpenCV"),
        ("Delivery",  "Docker · AWS EC2 · GitHub Actions · Vercel · Netlify · Render"),
    ]
    out = ""
    for i, (k, v) in enumerate(rows):
        y = 46 + i * 34
        t = 0.12 + i * 0.16
        out += (
            f'<text class="a" x="38" y="{y}" font-size="13" fill="{ACCENT}" font-weight="700" style="animation-delay:{t}s">{esc(k)}</text>'
            f'<text class="a" x="158" y="{y}" font-size="14" fill="{INK}" style="animation-delay:{t+.05}s">{esc(v)}</text>'
        )
    body = f'<rect width="{W}" height="{H}" rx="18" fill="{PANEL}" stroke="{BORDER}" stroke-width="1.5"/>{out}'
    save("stack.svg", svg(W, H, "Tech stack: Frontend, Backend, Data, AI & ML, Delivery", body))


# ───────────────────────────────────────────────────────── research bar ────────
def research():
    """Full-width IEEE / Research strip."""
    W, H = 1000, 110
    body = f"""
<rect width="{W}" height="{H}" rx="16" fill="{PANEL}" stroke="{BORDER}" stroke-width="1.5"/>

<!-- left: IEEE badge -->
<g class="a"{delay(.1)}>
  <rect x="28" y="22" width="58" height="66" rx="10" fill="#1e1b4b" stroke="{ACCENT}" stroke-opacity=".5"/>
  <text x="57" y="52" font-size="11" fill="{ACCENT}" text-anchor="middle" font-weight="700">IEEE</text>
  <text x="57" y="68" font-size="9.5" fill="{MUTED}" text-anchor="middle">Xplore</text>
  <text x="57" y="80" font-size="9" fill="{MUTED}" text-anchor="middle">2025</text>
</g>

<text class="a" x="104" y="44" font-size="16" fill="{INK}" font-weight="700"{delay(.2)}>SAR Military Target Detection — YOLOv8 + Denoising Autoencoders</text>
<text class="a" x="104" y="66" font-size="13" fill="{MUTED}"{delay(.3)}>Published on IEEE Xplore · 92% mAP accuracy · 5,000+ SAR images processed · PSNR 29.95 · SSIM 0.99</text>
<text class="a" x="104" y="86" font-size="12" fill="{ACCENT}"{delay(.4)}>ieeexplore.ieee.org/document/11042387 · ResearchGate · HuggingFace Demo</text>

<!-- right: ResearchGate chip -->
<g class="a"{delay(.5)}>
  <rect x="860" y="30" width="112" height="52" rx="10" fill="#052e16" stroke="{GREEN}" stroke-opacity=".5"/>
  <text x="916" y="52" font-size="11" fill="{GREEN}" text-anchor="middle" font-weight="700">ResearchGate</text>
  <text x="916" y="69" font-size="10" fill="{MUTED}" text-anchor="middle">+HuggingFace</text>
</g>
"""
    save("research.svg", svg(W, H, "IEEE Publication: SAR Military Target Detection, 92% mAP, YOLOv8", body))


# ─────────────────────────────────────────────────────────── experience ────────
def experience():
    W, H = 1000, 200
    roles = [
        (ACCENT, "Full-Stack Developer Intern",           "IBM Innovation Centre for Education",  "Aug – Oct 2025 · Remote",
         ["MERN dashboard · 15+ metrics · 25% efficiency ↑", "Docker + AWS EC2 + GitHub Actions CI/CD", "95+ Lighthouse · 30% ops effort ↓"]),
        (ORANGE, "Research Assistant — AI & Computer Vision", "SRMIST, Chennai",                 "Jan – Jun 2025",
         ["Published IEEE paper · 92% mAP · YOLOv8+DAE", "5,000+ SAR images · PyTorch + OpenCV", "PSNR 29.95 · SSIM 0.99 · outperformed baselines"]),
    ]
    out = ""
    for col_i, (color, role, company, date, bullets) in enumerate(roles):
        x0 = 28 + col_i * 490
        t  = 0.15 + col_i * 0.3
        btext = "".join(
            f'<text class="a" x="{x0}" y="{132 + bi*22}" font-size="13" fill="{MUTED}" style="animation-delay:{t + .4 + bi*.1}s">· {esc(b)}</text>'
            for bi, b in enumerate(bullets)
        )
        out += f"""
<rect class="a" x="{x0-4}" y="22" width="460" height="{H-40}" rx="12" fill="{PANEL}" stroke="{color}" stroke-opacity=".35" style="animation-delay:{t}s"/>
<rect class="g" x="{x0}" y="30" width="40" height="3" rx="1.5" fill="{color}" style="animation-delay:{t+.1}s"/>
<text class="a" x="{x0}" y="62" font-size="15.5" fill="{INK}" font-weight="700" style="animation-delay:{t+.15}s">{esc(role)}</text>
<text class="a" x="{x0}" y="82" font-size="13" fill="{color}" style="animation-delay:{t+.2}s">{esc(company)}</text>
<text class="a" x="{x0}" y="100" font-size="12" fill="{MUTED}" style="animation-delay:{t+.25}s">{esc(date)}</text>
{btext}"""
    body = f'<rect width="{W}" height="{H}" rx="18" fill="{BG}"/>{out}'
    save("experience.svg", svg(W, H, "Experience: IBM Intern Full-Stack Developer, SRMIST Research Assistant", body))


if __name__ == "__main__":
    hero()
    proof()
    tiles()
    stack()
    research()
    experience()
    print("cards written to", os.path.abspath(OUT), "(static)" if STATIC else "(animated)")
