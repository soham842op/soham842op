"""Generate the SVG artwork used by the profile README.

Run from anywhere:  python scripts/build_assets.py

Every image is written in a dark and a light variant; README.md swaps them
with <picture> + prefers-color-scheme. Edit HERO, CODE and PROJECTS below and
re-run to update the profile.
"""
from pathlib import Path
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parent.parent / "assets"

SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
CW = 0.6  # monospace advance in em; enforced with textLength so layout is font-independent

# midnight black + cobalt blue, flat colors only
THEMES = {
    "dark": dict(bg="#0a0e17", border="#1e2633", text="#f2f4f8", soft="#c5ccd8",
                 muted="#8792a5", accent="#4b84e8", cobalt="#0047ab", string="#a8c7fa"),
    "light": dict(bg="#ffffff", border="#d9dee7", text="#0a0e17", soft="#2b3240",
                  muted="#5b6475", accent="#0047ab", cobalt="#0047ab", string="#1f5fd1"),
}

RISE = (".rise{animation:rise .8s cubic-bezier(.2,.7,.2,1) both}"
        "@keyframes rise{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}")
BLINK = ".blink{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:0}}"


def svg(w, h, body, label, css="", reduced=""):
    style = css + "@media (prefers-reduced-motion: reduce){*{animation:none!important}" + reduced + "}"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label, {chr(34): "&quot;"})}">\n'
        f"<style>{style}</style>\n{body}\n</svg>\n"
    )


def text(x, y, s, size, fill, weight=400, extra=""):
    return (
        f'<text x="{x:g}" y="{y:g}" font-family="{SANS}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" {extra}>{escape(s)}</text>'
    )


def mono(x, y, s, size, fill, extra=""):
    return (
        f'<text x="{x:g}" y="{y:g}" font-family="{MONO}" font-size="{size}" '
        f'textLength="{len(s) * CW * size:.1f}" lengthAdjust="spacing" xml:space="preserve" '
        f'fill="{fill}" {extra}>{escape(s)}</text>'
    )


def panel(w, h, t):
    return (f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="10" '
            f'fill="{t["bg"]}" stroke="{t["border"]}"/>')


def delay(s):
    return f'style="animation-delay:{s:g}s"'


# ---------------------------------------------------------------- hero

HERO = dict(
    hello="Hi, I'm",
    name="Soham Shah",
    lines=["I build LLM apps, and then I measure them.",
           "Right now: RAG, evals and MLOps.",
           "Open to AI/ML, DS and SWE roles."],
    facts=[("CURRENTLY", "Open to AI/ML, DS and SWE roles"),
           ("STUDIED", "MS CS, Arizona State, 2026"),
           ("FOCUS", "LLM apps, RAG, evals, MLOps")],
)


def hero(t):
    W, H = 1200, 360
    fs, x0, ty = 24, 72, 228
    period = 15
    slot = period / len(HERO["lines"])
    css = [
        RISE, BLINK,
        ".wave{transform-box:fill-box;transform-origin:70% 80%;animation:wave 3s ease-in-out infinite}"
        "@keyframes wave{0%,60%,100%{transform:rotate(0)}10%,30%{transform:rotate(16deg)}20%{transform:rotate(-8deg)}40%{transform:rotate(-4deg)}50%{transform:rotate(10deg)}}"
        ".orbit{transform-box:view-box;transform-origin:1130px 30px;animation:spin 60s linear infinite}"
        ".moon{transform-box:view-box;transform-origin:1130px 30px;animation:spin 14s linear infinite reverse}"
        "@keyframes spin{to{transform:rotate(360deg)}}"
        ".ping{transform-box:fill-box;transform-origin:center;animation:ping 2.2s cubic-bezier(0,0,.2,1) infinite}"
        "@keyframes ping{0%{transform:scale(1);opacity:.8}100%{transform:scale(3);opacity:0}}"
        "@keyframes caret{0%,31%{opacity:1}31.5%,100%{opacity:0}}"
    ]
    clips, lines = [], []
    for i, s in enumerate(HERO["lines"]):
        n = len(s)
        L = n * CW * fs + 6
        d = 0 if i == 0 else -(period - i * slot)
        css.append(
            f"@keyframes t{i}{{0%{{transform:translateX(0);animation-timing-function:steps({n},end)}}"
            f"11%{{transform:translateX({L:.1f}px);animation-timing-function:linear}}"
            f"27%{{transform:translateX({L:.1f}px);animation-timing-function:steps({n},end)}}"
            f"31%,100%{{transform:translateX(0)}}}}"
            f".w{i}{{animation:t{i} {period}s infinite {d:g}s}}"
            f".c{i}{{animation:caret {period}s infinite {d:g}s}}"
        )
        clips.append(f'<clipPath id="cl{i}"><rect class="w{i}" x="{x0 - L:.1f}" y="{ty - fs}" '
                     f'width="{L:.1f}" height="{fs * 1.5:g}"/></clipPath>')
        lines.append(
            f'<g clip-path="url(#cl{i})">{mono(x0, ty, s, fs, t["soft"])}</g>'
            f'<g class="c{i}"><g class="w{i}"><rect class="blink" x="{x0 - 1}" y="{ty - fs * 0.8:.1f}" '
            f'width="2.5" height="{fs:g}" fill="{t["accent"]}"/></g></g>'
        )
    L0 = len(HERO["lines"][0]) * CW * fs + 6
    reduced = f".w0{{transform:translateX({L0:.1f}px)}}" + "".join(
        f".c{i}{{opacity:0}}" for i in range(1, len(HERO["lines"])))

    facts = []
    for i, (label, value) in enumerate(HERO["facts"]):
        x = 72 + i * 370
        lx = x + 16 if i == 0 else x
        dot = (f'<circle class="ping" cx="{x + 4}" cy="295" r="4" fill="{t["accent"]}"/>'
               f'<circle cx="{x + 4}" cy="295" r="4" fill="{t["accent"]}"/>') if i == 0 else ""
        facts.append(f'<g class="rise" {delay(0.5 + 0.1 * i)}>{dot}'
                     + text(lx, 300, label, 14, t["muted"], 600, 'letter-spacing="1.5"')
                     + text(x, 330, value, 21, t["text"]) + "</g>")

    body = f"""<defs><clipPath id="frame"><rect width="{W}" height="{H}" rx="10"/></clipPath>{''.join(clips)}</defs>
{panel(W, H, t)}
<g clip-path="url(#frame)">
<circle cx="1130" cy="30" r="170" fill="{t['cobalt']}"/>
<circle class="orbit" cx="1130" cy="30" r="205" fill="none" stroke="{t['accent']}" stroke-opacity="0.45" stroke-dasharray="2 10" stroke-linecap="round"/>
<g class="moon"><circle cx="1130" cy="235" r="7" fill="{t['accent']}"/></g>
</g>
<g class="rise">{text(72, 94, HERO['hello'], 26, t['muted'])}<text class="wave" x="158" y="94" font-size="26">👋</text></g>
<g class="rise" {delay(0.15)}>{text(68, 180, HERO['name'], 92, t['text'], 700, 'letter-spacing="-2"')}</g>
{''.join(lines)}
<rect class="rise" {delay(0.4)} x="72" y="258" width="{W - 144}" height="1" fill="{t['border']}"/>
{''.join(facts)}"""
    return svg(W, H, body, f"{HERO['name']}. {HERO['lines'][0]}", "".join(css), reduced)


# ---------------------------------------------------------------- about_me.py

CODE = [
    [("class", "kw"), (" ", ""), ("Soham", "cls"), (":", "")],
    [("    role      = ", ""), ('"AI/ML Engineer"', "str")],
    [("    studied   = ", ""), ('"MS CS, Arizona State \'26"', "str")],
    [("    gpa       = ", ""), ("3.84", "num")],
    [("    builds    = [", ""), ('"LLM apps"', "str"), (", ", ""), ('"RAG"', "str"), (", ", ""),
     ('"evals"', "str"), (", ", ""), ('"MLOps"', "str"), ("]", "")],
    [("    shipped   = ", ""), ('"FastAPI inference on AWS EKS"', "str")],
    [("    published = ", ""), ('"Springer: RL for trading"', "str")],
    [],
    [("    ", ""), ("def", "kw"), (" ", ""), ("how_i_work", "fn"), ("(self):", "")],
    [("        ", ""), ("return", "kw"), (" ", ""), ('"ship it, then measure it"', "str")],
]

REPL = [
    ("$ python -i about_me.py", "muted"),
    (">>> Soham().how_i_work()", "soft"),
    ("'ship it, then measure it'", "string"),
]


def code_card(t):
    W, H, fs, lh = 1200, 430, 20, 32
    top, gx, cx = 48, 52, 84
    colors = {"": t["soft"], "kw": t["accent"], "cls": t["text"], "fn": t["text"],
              "str": t["string"], "num": t["accent"]}
    weights = {"kw": 700, "cls": 700, "fn": 600}
    rows = []
    for i, toks in enumerate(CODE):
        y = top + 44 + i * lh
        line = "".join(s for s, _ in toks)
        spans = "".join(
            f'<tspan fill="{colors[k]}"{f" font-weight=\"{weights[k]}\"" if k in weights else ""}>{escape(s)}</tspan>'
            for s, k in toks)
        num = mono(gx, y, f"{i + 1:>2}", fs - 2, t["muted"], 'text-anchor="end"')
        src = (f'<text x="{cx}" y="{y}" font-family="{MONO}" font-size="{fs}" xml:space="preserve" '
               f'textLength="{len(line) * CW * fs:.1f}" lengthAdjust="spacing">{spans}</text>') if line else ""
        rows.append(f'<g class="rise" {delay(0.2 + 0.09 * i)}>{num}{src}</g>')

    px, pw = 820, W - 820 - 36
    repl = []
    for i, (s, c) in enumerate(REPL):
        repl.append(f'<g class="rise" {delay(1.3 + 0.35 * i)}>{mono(px + 28, top + 76 + i * 34, s, 17, t[c])}</g>')
    last_y = top + 76 + len(REPL) * 34
    repl.append(f'<g class="rise" {delay(1.3 + 0.35 * len(REPL))}>{mono(px + 28, last_y, ">>> ", 17, t["soft"])}'
                f'<rect class="blink" x="{px + 28 + 4 * CW * 17 + 2:.1f}" y="{last_y - 14}" width="9" height="18" fill="{t["accent"]}"/></g>')

    dots = "".join(f'<circle cx="{28 + 20 * k}" cy="24" r="6" fill="{t["border"]}"/>' for k in range(3))
    body = f"""{panel(W, H, t)}
<rect x="0.5" y="{top}" width="{W - 1}" height="1" fill="{t['border']}"/>
{dots}
<rect x="96" y="1" width="160" height="{top - 1}" fill="{t['bg']}"/>
<rect x="96" y="{top - 2}" width="160" height="2" fill="{t['accent']}"/>
{mono(116, 30, "about_me.py", 15, t['text'])}
<rect x="{px}" y="{top}" width="1" height="{H - top}" fill="{t['border']}"/>
<rect x="{px + 1}" y="{top + 1}" width="{W - px - 2}" height="{H - top - 2}" rx="0" fill="{t['cobalt']}" fill-opacity="0.06"/>
{text(px + 28, top + 36, "TERMINAL", 13, t['muted'], 600, 'letter-spacing="1.5"')}
{''.join(rows)}
{''.join(repl)}"""
    label = "about_me.py: " + " ".join("".join(s for s, _ in toks).strip() for toks in CODE if toks)
    return svg(W, H, body, label, RISE + BLINK)


# ---------------------------------------------------------------- project cards

PROJECTS = [
    dict(slug="livedocs", title="LiveDocs", kind="LLM + RAG",
         desc=["Realtime collaborative editor with a Gemini",
               "copilot that answers with citations (pgvector)."],
         stack="Next.js · FastAPI · Postgres + pgvector · AWS S3",
         metric="97.1%", note="hit@1 on a 40-question retrieval benchmark (100% hit@5)"),
    dict(slug="devlens", title="DevLens", kind="Local LLM tooling",
         desc=["CLI that indexes repos and git history and writes",
               "reports with a local Llama 3. No code leaves the box."],
         stack="TypeScript · Node.js · SQLite · Ollama · Vitest",
         metric="96%", note="error-handling precision, up from 31% with ground-truth evals"),
    dict(slug="music-recommender", title="Hybrid Music Recommender", kind="Recommender systems",
         desc=["Item2Vec and audio-feature embeddings over 170K",
               "Spotify tracks with FAISS retrieval. Group project."],
         stack="Python · Gensim · FAISS · LightGBM",
         metric="+22%", note="NDCG@10 over collaborative-only (95% CI 13-33%)"),
    dict(slug="datawhisperer", title="DataWhisperer", kind="Text-to-SQL",
         desc=["Ask a question in plain English, get the SQL and",
               "the answer from a local CodeLlama model."],
         stack="Python · LangChain · llama-cpp · Streamlit",
         metric=None, note="Runs fully offline on a local GPU."),
]


def card(t, p):
    W, H = 600, 320
    css = (RISE
           + ".draw{transform-box:fill-box;transform-origin:left;animation:draw 1.4s .5s cubic-bezier(.6,0,.2,1) both}"
           "@keyframes draw{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
           ".nudge{animation:nudge 2.6s ease-in-out infinite}"
           "@keyframes nudge{0%,100%{transform:translate(0,0)}50%{transform:translate(3px,-3px)}}"
           ".bob{transform-box:fill-box;transform-origin:center;animation:bob 4s ease-in-out infinite}"
           "@keyframes bob{0%,100%{transform:rotate(0)}50%{transform:rotate(90deg)}}")
    desc = "".join(text(36, 138 + 27 * k, line, 19, t["soft"]) for k, line in enumerate(p["desc"]))
    if p["metric"]:
        result = (text(34, 264, p["metric"], 36, t["accent"], 700, 'letter-spacing="-0.5"')
                  + text(36, 292, p["note"], 15, t["muted"]))
    else:
        result = text(36, 264, p["note"], 21, t["text"], 600)
    body = f"""{panel(W, H, t)}
<rect class="bob" x="36" y="38" width="9" height="9" fill="{t['cobalt']}"/>
{text(54, 47, p['kind'], 15, t['accent'], 600)}
{text(W - 52, 47, "View code", 15, t['muted'], extra='text-anchor="end"')}
<path class="nudge" d="M{W - 46} 47 l8 -8 m-6 0 h6 v6" fill="none" stroke="{t['muted']}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
<g class="rise">{text(34, 96, p['title'], 32, t['text'], 700, 'letter-spacing="-0.5"')}
{desc}
{text(36, 202, p['stack'], 15, t['muted'])}</g>
<rect x="36" y="222" width="{W - 72}" height="1" fill="{t['border']}"/>
<rect class="draw" x="36" y="221.5" width="{W - 72}" height="2" fill="{t['accent']}"/>
<g class="rise" {delay(0.6)}>{result}</g>"""
    metric = f"{p['metric']} {p['note']}" if p["metric"] else p["note"]
    return svg(W, H, body, f"{p['title']}: {' '.join(p['desc'])} {metric}. Built with {p['stack']}.", css)


def main():
    for name, t in THEMES.items():
        files = {f"hero-{name}.svg": hero(t), f"about-{name}.svg": code_card(t)}
        for p in PROJECTS:
            files[f"work/{p['slug']}-{name}.svg"] = card(t, p)
        for rel, content in files.items():
            out = ASSETS / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(content, encoding="utf-8", newline="\n")
            print("wrote", out.relative_to(ASSETS.parent))


if __name__ == "__main__":
    main()
