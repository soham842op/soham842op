"""Generate the SVG artwork used by the profile README.

Run from anywhere:  python scripts/build_assets.py

Every image is written in a dark and a light variant; README.md swaps them
with <picture> + prefers-color-scheme. Edit HEADER and PROJECTS below and
re-run to update the profile.
"""
from pathlib import Path
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parent.parent / "assets"

SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"

# midnight black + cobalt blue, flat colors only
THEMES = {
    "dark": dict(bg="#0a0e17", border="#1e2633", text="#f2f4f8", soft="#c5ccd8",
                 muted="#8792a5", accent="#4b84e8", cobalt="#0047ab"),
    "light": dict(bg="#ffffff", border="#d9dee7", text="#0a0e17", soft="#2b3240",
                  muted="#5b6475", accent="#0047ab", cobalt="#0047ab"),
}


def svg(w, h, body, label):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">\n{body}\n</svg>\n'
    )


def text(x, y, s, size, fill, weight=400, extra=""):
    return (
        f'<text x="{x:g}" y="{y:g}" font-family="{SANS}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" {extra}>{escape(s)}</text>'
    )


def panel(w, h, t):
    return (f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="10" '
            f'fill="{t["bg"]}" stroke="{t["border"]}"/>')


# ---------------------------------------------------------------- header

HEADER = dict(
    hello="Hi, I'm",
    name="Soham Shah",
    line="I build LLM apps, and then I measure them.",
    facts=[("CURRENTLY", "Open to AI/ML, DS and SWE roles"),
           ("STUDIED", "MS CS, Arizona State, 2026"),
           ("FOCUS", "LLM apps, RAG, evals, MLOps")],
)


def header(t):
    W, H = 1200, 360
    facts = []
    for i, (label, value) in enumerate(HEADER["facts"]):
        x = 72 + i * 370
        facts.append(text(x, 300, label, 14, t["muted"], 600, 'letter-spacing="1.5"')
                     + text(x, 330, value, 21, t["text"]))
    body = f"""<clipPath id="frame"><rect width="{W}" height="{H}" rx="10"/></clipPath>
{panel(W, H, t)}
<g clip-path="url(#frame)"><circle cx="1130" cy="30" r="170" fill="{t['cobalt']}"/></g>
{text(72, 94, HEADER['hello'], 26, t['muted'])}
{text(68, 182, HEADER['name'], 92, t['text'], 700, 'letter-spacing="-2"')}
{text(72, 226, HEADER['line'], 26, t['soft'])}
<rect x="72" y="258" width="{W - 144}" height="1" fill="{t['border']}"/>
{''.join(facts)}"""
    return svg(W, H, body, f"{HEADER['name']}. {HEADER['line']}")


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
    desc = "".join(text(36, 138 + 27 * k, line, 19, t["soft"]) for k, line in enumerate(p["desc"]))
    if p["metric"]:
        result = (text(34, 264, p["metric"], 36, t["accent"], 700, 'letter-spacing="-0.5"')
                  + text(36, 292, p["note"], 15, t["muted"]))
    else:
        result = text(36, 264, p["note"], 21, t["text"], 600)
    body = f"""{panel(W, H, t)}
<rect x="36" y="38" width="9" height="9" fill="{t['cobalt']}"/>
{text(54, 47, p['kind'], 15, t['accent'], 600)}
{text(W - 36, 47, "View code ↗", 15, t['muted'], extra='text-anchor="end"')}
{text(34, 96, p['title'], 32, t['text'], 700, 'letter-spacing="-0.5"')}
{desc}
{text(36, 202, p['stack'], 15, t['muted'])}
<rect x="36" y="222" width="{W - 72}" height="1" fill="{t['border']}"/>
{result}"""
    metric = f"{p['metric']} {p['note']}" if p["metric"] else p["note"]
    return svg(W, H, body, f"{p['title']}: {' '.join(p['desc'])} {metric}. Built with {p['stack']}.")


def main():
    for name, t in THEMES.items():
        files = {f"header-{name}.svg": header(t)}
        for p in PROJECTS:
            files[f"projects/{p['slug']}-{name}.svg"] = card(t, p)
        for rel, content in files.items():
            out = ASSETS / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(content, encoding="utf-8", newline="\n")
            print("wrote", out.relative_to(ASSETS.parent))


if __name__ == "__main__":
    main()
