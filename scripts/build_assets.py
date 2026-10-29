"""Generate the SVG artwork used by the profile README.

Run from anywhere:  python scripts/build_assets.py

Every image is written in a dark and a light variant; README.md swaps them
with <picture> + prefers-color-scheme. Edit the content blocks near the
bottom (WORDS, STATS, SECTIONS, PROJECTS) and re-run to update the profile.
"""
from pathlib import Path
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parent.parent / "assets"

SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
CW = 0.6  # monospace advance in em; enforced with textLength so layout is font-independent

THEMES = {
    "dark": dict(
        bg0="#070a1a", bg1="#0e1236", bg2="#1d1660",
        text="#f8fafc", sub="#c7d2fe", muted="#94a3b8",
        a1="#818cf8", a2="#c084fc", a3="#f472b6",
        line="#a5b4fc", panel="#0b0f2b", node="#0b0f2b", ok="#34d399",
        edge="#ffffff", edge_op=0.09, tint="#ffffff", tint_op=0.04,
        blob_op=0.42, dot="#ffffff", dot_op=0.10, shine="#ffffff",
        wave0="#151a3d", wave1="#26206b",
    ),
    "light": dict(
        bg0="#ffffff", bg1="#f5f3ff", bg2="#e4e0ff",
        text="#1e1b4b", sub="#4338ca", muted="#64748b",
        a1="#4f46e5", a2="#7c3aed", a3="#db2777",
        line="#6366f1", panel="#ffffff", node="#ffffff", ok="#059669",
        edge="#4f46e5", edge_op=0.18, tint="#4f46e5", tint_op=0.05,
        blob_op=0.22, dot="#312e81", dot_op=0.10, shine="#ffffff",
        wave0="#eef0ff", wave1="#dcdcfe",
    ),
}

REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def svg(w, h, body, label, style="", extra_reduced=""):
    css = style + REDUCED.replace("}}", "}" + extra_reduced + "}")
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">\n'
        f"<style>{css}</style>\n{body}\n</svg>\n"
    )


def mono(x, y, s, size, fill, anchor="start", extra=""):
    length = len(s) * CW * size
    return (
        f'<text x="{x:g}" y="{y:g}" font-family="{MONO}" font-size="{size}" '
        f'textLength="{length:.1f}" lengthAdjust="spacing" text-anchor="{anchor}" '
        f'fill="{fill}" {extra}>{escape(s)}</text>'
    )


def sans(x, y, s, size, fill, weight=400, extra=""):
    return (
        f'<text x="{x:g}" y="{y:g}" font-family="{SANS}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" {extra}>{escape(s)}</text>'
    )


def accent_grad(t, gid="acc", **attrs):
    a = " ".join(f'{k}="{v}"' for k, v in attrs.items())
    return (
        f'<linearGradient id="{gid}" {a}>'
        f'<stop offset="0" stop-color="{t["a1"]}"/>'
        f'<stop offset="0.55" stop-color="{t["a2"]}"/>'
        f'<stop offset="1" stop-color="{t["a3"]}"/></linearGradient>'
    )


def pill(x, y, s, t, size=13, h=30):
    w = len(s) * CW * size + 26
    out = (
        f'<rect x="{x:g}" y="{y:g}" width="{w:.1f}" height="{h}" rx="{h / 2:g}" '
        f'fill="{t["tint"]}" fill-opacity="{t["tint_op"] * 1.5:g}" '
        f'stroke="{t["edge"]}" stroke-opacity="{t["edge_op"] * 1.4:g}"/>'
        + mono(x + 13, y + h / 2 + size * 0.36, s, size, t["sub"])
    )
    return out, w


# ---------------------------------------------------------------- hero

WORDS = ["LLM apps", "RAG systems", "eval harnesses", "MLOps pipelines"]


def hero(t):
    W, H = 1200, 400
    fs, x0, ty = 36, 112, 280
    period = 12
    slot = period / len(WORDS)

    css = [
        ".blob{animation:drift 18s ease-in-out infinite alternate}"
        ".b2{animation-duration:23s;animation-delay:-7s}.b3{animation-duration:29s;animation-delay:-13s}"
        "@keyframes drift{0%{transform:translate(0,0)}50%{transform:translate(70px,-35px)}100%{transform:translate(-50px,30px)}}"
        ".ping{transform-box:fill-box;transform-origin:center;animation:ping 2.4s cubic-bezier(0,0,.2,1) infinite}"
        "@keyframes ping{0%{transform:scale(1);opacity:.75}100%{transform:scale(2.8);opacity:0}}"
        ".blink{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
        "@keyframes caret{0%,23.5%{opacity:1}24%,100%{opacity:0}}"
    ]
    clips, words = [], []
    for i, w in enumerate(WORDS):
        n = len(w)
        L = n * CW * fs + 8
        delay = 0 if i == 0 else -(period - i * slot)
        css.append(
            f"@keyframes t{i}{{0%{{transform:translateX(0);animation-timing-function:steps({n},end)}}"
            f"10%{{transform:translateX({L:.1f}px);animation-timing-function:linear}}"
            f"19%{{transform:translateX({L:.1f}px);animation-timing-function:steps({n},end)}}"
            f"23.5%,100%{{transform:translateX(0)}}}}"
            f".w{i}{{animation:t{i} {period}s infinite {delay:g}s}}"
            f".c{i}{{animation:caret {period}s infinite {delay:g}s}}"
        )
        clips.append(
            f'<clipPath id="cl{i}"><rect class="w{i}" x="{x0 - L:.1f}" y="{ty - fs}" '
            f'width="{L:.1f}" height="{fs * 1.5:g}"/></clipPath>'
        )
        words.append(
            f'<g clip-path="url(#cl{i})">{mono(x0, ty, w, fs, t["sub"], extra="font-weight=\"600\"")}</g>'
            f'<g class="c{i}"><g class="w{i}"><rect class="blink" x="{x0 - 2}" y="{ty - fs * 0.78:.1f}" '
            f'width="3.5" height="{fs * 0.95:.1f}" rx="1.5" fill="{t["a2"]}"/></g></g>'
        )
    L0 = len(WORDS[0]) * CW * fs + 8
    reduced = f".w0{{transform:translateX({L0:.1f}px)}}" + "".join(
        f".c{i}{{opacity:0}}" for i in range(1, len(WORDS))
    )

    # neural-net motif
    layers = [(830, [130, 210, 290]), (930, [105, 175, 245, 315]), (1030, [140, 210, 280]), (1120, [210])]
    edges = []
    for (xa, ya), (xb, yb) in zip(layers, layers[1:]):
        for p in ya:
            for q in yb:
                edges.append(f'<line x1="{xa}" y1="{p}" x2="{xb}" y2="{q}"/>')
    routes = [(0, 0, 0), (1, 2, 1), (2, 3, 2), (1, 1, 0), (0, 3, 2), (2, 0, 1)]
    pulses = []
    for k, (a, b, c) in enumerate(routes):
        pts = [(layers[0][0], layers[0][1][a]), (layers[1][0], layers[1][1][b]),
               (layers[2][0], layers[2][1][c]), (layers[3][0], layers[3][1][0])]
        path = "M" + " L".join(f"{x} {y}" for x, y in pts)
        begin = f"{k * 0.6:g}s"
        color = t["a2"] if k % 2 else t["a3"]
        pulses.append(
            f'<circle r="4.5" fill="{color}" opacity="0" filter="url(#glow)">'
            f'<animateMotion dur="3.6s" begin="{begin}" repeatCount="indefinite" path="{path}"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.85;1" '
            f'dur="3.6s" begin="{begin}" repeatCount="indefinite"/></circle>'
        )
    nodes = []
    for x, ys in layers[:-1]:
        for y in ys:
            nodes.append(f'<circle cx="{x}" cy="{y}" r="9"/>')
    ox, oy = layers[-1][0], layers[-1][1][0]

    chip_text = "OPEN TO AI/ML · DATA SCIENCE · SWE ROLES"
    chip_w = 108 - 70 + len(chip_text) * CW * 14 + 20

    body = f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['bg0']}"/><stop offset="0.6" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg2']}"/></linearGradient>
<linearGradient id="name" gradientUnits="userSpaceOnUse" x1="66" y1="0" x2="660" y2="0"><stop offset="0" stop-color="{t['text']}"/><stop offset="0.5" stop-color="{t['a1']}"/><stop offset="1" stop-color="{t['a2']}"/></linearGradient>
<linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="220" y2="0">
<stop offset="0" stop-color="{t['shine']}" stop-opacity="0"/><stop offset="0.5" stop-color="{t['shine']}" stop-opacity="0.55"/><stop offset="1" stop-color="{t['shine']}" stop-opacity="0"/>
<animateTransform attributeName="gradientTransform" type="translate" values="-300 0;1000 0;1000 0" keyTimes="0;0.45;1" dur="7s" repeatCount="indefinite"/></linearGradient>
<radialGradient id="fadeg" cx="0.78" cy="0.45" r="0.6"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>
<mask id="fade"><rect width="{W}" height="{H}" fill="url(#fadeg)"/></mask>
<pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="13" cy="13" r="1.2" fill="{t['dot']}" fill-opacity="{t['dot_op'] * 1.6:g}"/></pattern>
<filter id="blur" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="70"/></filter>
<filter id="glow" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="frame"><rect width="{W}" height="{H}" rx="24"/></clipPath>
{''.join(clips)}
</defs>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<g filter="url(#blur)" opacity="{t['blob_op']}">
<circle class="blob" cx="930" cy="110" r="190" fill="{t['a1']}"/>
<circle class="blob b2" cx="1110" cy="360" r="170" fill="{t['a2']}"/>
<circle class="blob b3" cx="560" cy="430" r="200" fill="{t['a3']}"/>
</g>
<rect width="{W}" height="{H}" fill="url(#dots)" mask="url(#fade)"/>
</g>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="24" fill="none" stroke="{t['edge']}" stroke-opacity="{t['edge_op'] * 1.3:g}"/>

<g stroke="{t['line']}" stroke-opacity="0.22" stroke-width="1.3">{''.join(edges)}</g>
{''.join(pulses)}
<g fill="{t['node']}" stroke="{t['line']}" stroke-width="2.5">{''.join(nodes)}</g>
<circle class="ping" cx="{ox}" cy="{oy}" r="14" fill="none" stroke="{t['a2']}" stroke-width="2"/>
<circle cx="{ox}" cy="{oy}" r="14" fill="{t['a1']}" stroke="{t['a2']}" stroke-width="3" filter="url(#glow)"/>

<rect x="70" y="58" width="{chip_w:.1f}" height="38" rx="19" fill="{t['tint']}" fill-opacity="{t['tint_op'] * 1.5:g}" stroke="{t['edge']}" stroke-opacity="{t['edge_op'] * 1.6:g}"/>
<circle class="ping" cx="91" cy="77" r="5" fill="{t['ok']}"/>
<circle cx="91" cy="77" r="5" fill="{t['ok']}"/>
{mono(108, 82, chip_text, 14, t['sub'])}

<text x="64" y="212" font-family="{SANS}" font-size="104" font-weight="700" letter-spacing="-2" fill="url(#name)">Soham Shah</text>
<text x="64" y="212" font-family="{SANS}" font-size="104" font-weight="700" letter-spacing="-2" fill="url(#shine)">Soham Shah</text>

<path d="M74 {ty - 26} l13 12.5 l-13 12.5" fill="none" stroke="{t['a1']}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
{''.join(words)}

{sans(70, 338, "AI/ML Engineer  ·  MS in Computer Science, Arizona State University", 22, t['muted'])}"""
    return svg(W, H, body, "Soham Shah - AI/ML Engineer building LLM apps, RAG systems and MLOps pipelines",
               "".join(css), reduced)


# ---------------------------------------------------------------- stats strip

STATS = [
    ("3.84", "GPA", "MS CS · ARIZONA STATE"),
    ("97.1%", "HIT@1 RETRIEVAL", "LIVEDOCS RAG BENCHMARK"),
    ("+22%", "NDCG@10 VS CF-ONLY", "HYBRID MUSIC RECSYS"),
    ("31→96%", "ERROR-HANDLING PRECISION", "DEVLENS EVAL HARNESS"),
]


def stats(t):
    W, H, gap = 1200, 164, 20
    tw = (W - gap * (len(STATS) - 1)) / len(STATS)
    css = (
        ".rise{animation:rise .9s cubic-bezier(.2,.7,.2,1) both}"
        "@keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}"
    )
    tiles = []
    for i, (num, l1, l2) in enumerate(STATS):
        x = i * (tw + gap)
        tiles.append(
            f'<g class="rise" style="animation-delay:{0.12 * i:g}s">'
            f'<rect x="{x + 0.5:.1f}" y="0.5" width="{tw - 1:.1f}" height="{H - 1}" rx="20" fill="{t["panel"]}" '
            f'stroke="{t["edge"]}" stroke-opacity="{t["edge_op"] * 1.6:g}"/>'
            f'<rect x="{x + 0.5:.1f}" y="0.5" width="{tw - 1:.1f}" height="{H - 1}" rx="20" fill="url(#corner)"/>'
            f'<rect x="{x + 28:.1f}" y="28" width="30" height="4" rx="2" fill="url(#acc)"/>'
            f'{sans(x + 26, 94, num, 50, "url(#acc)", 700, "letter-spacing=\"-1\"")}'
            f'{mono(x + 28, 122, l1, 14, t["sub"])}'
            f'{mono(x + 28, 143, l2, 14, t["muted"])}</g>'
        )
    body = f"""<defs>{accent_grad(t)}
<radialGradient id="corner" cx="1" cy="0" r="0.9"><stop offset="0" stop-color="{t['a2']}" stop-opacity="0.16"/><stop offset="1" stop-color="{t['a2']}" stop-opacity="0"/></radialGradient></defs>
{''.join(tiles)}"""
    label = "Highlights: " + "; ".join(f"{n} {a.lower()}, {b.lower()}" for n, a, b in STATS)
    return svg(W, H, body, label, css)


# ---------------------------------------------------------------- section headers

SECTIONS = [
    ("about", "About", "WHO I AM"),
    ("work", "Selected work", "THINGS I'VE SHIPPED"),
    ("oss", "Open source", "CONTRIBUTIONS"),
    ("publication", "Publication", "RESEARCH"),
    ("toolkit", "Toolkit", "WHAT I BUILD WITH"),
]


def section(t, idx, title, caption):
    W, H = 1200, 100
    css = (
        ".sweep{animation:sweep 6s ease-in-out infinite}"
        "@keyframes sweep{0%{transform:translateX(-220px)}60%,100%{transform:translateX(1300px)}}"
    )
    body = f"""<defs>
<linearGradient id="rule" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t['a1']}"/><stop offset="0.35" stop-color="{t['a2']}" stop-opacity="0.7"/><stop offset="1" stop-color="{t['a3']}" stop-opacity="0"/></linearGradient>
<linearGradient id="spark" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t['a3']}" stop-opacity="0"/><stop offset="0.5" stop-color="{t['a3']}"/><stop offset="1" stop-color="{t['a3']}" stop-opacity="0"/></linearGradient>
</defs>
<rect x="1" y="18" width="54" height="54" rx="15" fill="{t['tint']}" fill-opacity="{t['tint_op'] * 1.5:g}" stroke="{t['a1']}" stroke-opacity="0.55" stroke-width="1.5"/>
{mono(28, 51, f"{idx:02d}", 18, t['a1'], "middle", 'font-weight="700"')}
{sans(76, 61, title, 40, t['text'], 700, 'letter-spacing="-0.5"')}
{mono(1198, 58, caption, 16, t['muted'], "end")}
<rect x="0" y="92" width="{W}" height="2" rx="1" fill="url(#rule)"/>
<rect class="sweep" x="0" y="91" width="200" height="4" rx="2" fill="url(#spark)"/>
<circle cx="3" cy="93" r="3" fill="{t['a1']}"/>"""
    return svg(W, H, body, f"{idx:02d} {title}", css)


# ---------------------------------------------------------------- project cards

PROJECTS = [
    dict(slug="livedocs", title="LiveDocs", tag="LLM · RAG · REALTIME",
         desc=["Realtime collaborative editor with a Gemini",
               "copilot: cited RAG Q&A over pgvector."],
         metric="97.1%", metric_label="HIT@1  ·  100% HIT@5 ON A 40-QUESTION BENCHMARK",
         stack=["Next.js", "FastAPI", "pgvector", "AWS S3"]),
    dict(slug="devlens", title="DevLens", tag="LOCAL LLM · DEV TOOLS",
         desc=["Privacy-first CLI that indexes repos and git",
               "history, then reports with a local Llama 3."],
         metric="31→96%", metric_label="ERROR-HANDLING PRECISION AFTER GROUND-TRUTH EVALS",
         stack=["TypeScript", "SQLite", "Ollama", "Vitest"]),
    dict(slug="music-recommender", title="Hybrid Music Recommender", tag="RECSYS · EMBEDDINGS",
         desc=["Item2Vec + audio embeddings over 170K Spotify",
               "tracks with FAISS retrieval. Group project."],
         metric="+22%", metric_label="NDCG@10 VS CF-ONLY  ·  95% CI 13-33%, p < 0.00001",
         stack=["Python", "Gensim", "FAISS", "LightGBM"]),
    dict(slug="datawhisperer", title="DataWhisperer", tag="AGENTS · TEXT-TO-SQL",
         desc=["Ask questions in plain English; get SQL and",
               "answers from a local CodeLlama on GPU."],
         metric="Offline", metric_label="TEXT-TO-SQL AGENT, RUNS ENTIRELY ON YOUR MACHINE",
         stack=["Python", "LangChain", "llama-cpp", "Streamlit"]),
]


def card(t, i, p):
    W, H = 600, 340
    css = (
        ".rise{animation:rise .9s cubic-bezier(.2,.7,.2,1) both}"
        "@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}"
        ".nudge{animation:nudge 2.8s ease-in-out infinite}"
        "@keyframes nudge{0%,100%{transform:translate(0,0)}50%{transform:translate(3px,-3px)}}"
    )
    pills, x = [], 36
    for s in p["stack"]:
        out, w = pill(x, 286, s, t, size=14)
        pills.append(out)
        x += w + 8
    desc = "".join(sans(36, 146 + 28 * k, line, 19, t["muted"]) for k, line in enumerate(p["desc"]))
    body = f"""<defs>{accent_grad(t)}{accent_grad(t, "border", x1="0", y1="0", x2="1", y2="1")}
<radialGradient id="corner" cx="1" cy="0" r="0.75"><stop offset="0" stop-color="{t['a2']}" stop-opacity="0.22"/><stop offset="1" stop-color="{t['a2']}" stop-opacity="0"/></radialGradient></defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="24" fill="{t['panel']}"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="24" fill="url(#corner)"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="24" fill="none" stroke="url(#border)" stroke-opacity="0.5" stroke-width="1.5"/>
<g class="rise">
{mono(36, 56, f"{i:02d} / {p['tag']}", 14, t['a1'], extra='font-weight="600"')}
<circle cx="554" cy="51" r="21" fill="{t['tint']}" fill-opacity="{t['tint_op'] * 1.5:g}" stroke="{t['a1']}" stroke-opacity="0.5" stroke-width="1.5"/>
<path class="nudge" d="M547 58 L561 44 M550 44 H561 V55" fill="none" stroke="{t['text']}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
{sans(34, 106, p['title'], 34, t['text'], 700, 'letter-spacing="-0.5"')}
{desc}
{sans(34, 242, p['metric'], 44, "url(#acc)", 700, 'letter-spacing="-1"')}
{mono(36, 267, p['metric_label'], 13, t['sub'])}
{''.join(pills)}
</g>"""
    label = f"{p['title']}: {' '.join(p['desc'])} {p['metric']} {p['metric_label'].lower()}. Built with {', '.join(p['stack'])}."
    return svg(W, H, body, label, css)


# ---------------------------------------------------------------- footer

def wave(y0, amp, period=300, width=2400, close=True):
    d = f"M0 {y0} Q {period / 2:g} {y0 - amp} {period} {y0}"
    x = period
    while x < width:
        x += period
        d += f" T {x} {y0}"
    return d + (" V160 H0 Z" if close else "")


def footer(t):
    W, H = 1200, 160
    css = (
        ".wa{animation:slide 18s linear infinite}.wb{animation:slide 27s linear infinite reverse}"
        "@keyframes slide{from{transform:translateX(0)}to{transform:translateX(-1200px)}}"
    )
    body = f"""<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t['wave0']}"/><stop offset="1" stop-color="{t['wave1']}"/></linearGradient></defs>
{mono(600, 40, "THANKS FOR STOPPING BY", 16, t['muted'], "middle")}
<circle cx="600" cy="62" r="3" fill="{t['a2']}"/>
<path class="wb" d="{wave(108, 22, 400)}" fill="{t['a1']}" fill-opacity="0.14"/>
<path class="wa" d="{wave(118, 18)}" fill="url(#g)"/>
<path class="wa" d="{wave(126, 18, close=False)}" fill="none" stroke="{t['a1']}" stroke-opacity="0.6" stroke-width="2"/>"""
    return svg(W, H, body, "Thanks for stopping by", css)


def main():
    for name, t in THEMES.items():
        files = {
            f"banner-{name}.svg": hero(t),
            f"stats-{name}.svg": stats(t),
            f"footer-{name}.svg": footer(t),
        }
        for i, (slug, title, caption) in enumerate(SECTIONS, 1):
            files[f"sections/{slug}-{name}.svg"] = section(t, i, title, caption)
        for i, p in enumerate(PROJECTS, 1):
            files[f"cards/{p['slug']}-{name}.svg"] = card(t, i, p)
        for rel, content in files.items():
            out = ASSETS / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(content, encoding="utf-8", newline="\n")
            print("wrote", out.relative_to(ASSETS.parent))


if __name__ == "__main__":
    main()
