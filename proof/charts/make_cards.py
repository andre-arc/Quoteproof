"""Build the workflow diagram, the real-run card and the GitHub social preview cards.

Run from the repo root:  python3 proof/charts/make_cards.py
Writes assets/proof/{workflow,run}.svg (theme-aware), light/dark PNGs of every proof chart,
and assets/social/*.png (needs google-chrome).
"""
import json, pathlib, subprocess, sys, tempfile
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from make_charts import svg, esc, FONT  # noqa: E402

OUT = pathlib.Path("assets/proof")
SOCIAL = pathlib.Path("assets/social")
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, 'DejaVu Sans Mono', monospace"


# 1. How it works. Steps from SKILL.md; statuses from verify_quotes.py.
def workflow():
    W, H = 760, 330
    steps = [("1", "Decompose", ["5 angles chosen", "for your topic"]),
             ("2", "Search", ["claim → URL →", "exact quote"]),
             ("3", "Check", ["a script fetches each", "page, matches word", "for word"]),
             ("4", "Report", ["cited findings +", "audit line"])]
    bw, gap, x0, y0, bh = 154, 32, 24, 84, 104
    b = ['<text class="t" x="24" y="38">How Quoteproof works</text>',
         '<text class="s" x="24" y="60">Research runs on a fast model. The quote check is code, not the model checking itself.</text>']
    for i, (n, name, lines) in enumerate(steps):
        x = x0 + i * (bw + gap)
        hot = name == "Check"
        b.append(f'<rect x="{x}" y="{y0}" width="{bw}" height="{bh}" rx="10" '
                 f'fill="{"var(--accent-wash)" if hot else "none"}" stroke="{"var(--accent)" if hot else "var(--axis)"}" stroke-width="{2 if hot else 1}"/>')
        b.append(f'<text class="m" x="{x + 14}" y="{y0 + 24}">{n}</text>')
        b.append(f'<text class="v" x="{x + 30}" y="{y0 + 24}">{name}</text>')
        for k, ln in enumerate(lines):
            b.append(f'<text class="l" x="{x + 14}" y="{y0 + 50 + k * 18}">{esc(ln)}</text>')
        if i < 3:
            ax = x + bw + 6
            b.append(f'<path d="M{ax} {y0 + bh / 2} H{ax + gap - 12} M{ax + gap - 17} {y0 + bh / 2 - 5} '
                     f'L{ax + gap - 12} {y0 + bh / 2} L{ax + gap - 17} {y0 + bh / 2 + 5}" '
                     f'fill="none" stroke="var(--muted)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>')
    # every quote gets one of four results
    cx = x0 + 2 * (bw + gap) + bw / 2
    b.append(f'<path d="M{cx} {y0 + bh} V{y0 + bh + 22}" stroke="var(--accent)" stroke-width="1.5"/>')
    ry = y0 + bh + 22
    b.append(f'<rect x="24" y="{ry}" width="712" height="96" rx="10" fill="none" stroke="var(--border)"/>')
    b.append(f'<text class="m" x="40" y="{ry + 24}">Every quote gets one result</text>')
    ok = "M4 8.5 L7 11.5 L12 5"
    no = "M5 5 L11 11 M11 5 L5 11"
    res = [("verified", "kept", "var(--accent)", ok),
           ("misattributed", "kept, source corrected", "var(--accent)", ok),
           ("not_found", "dropped", "var(--bad)", no),
           ("fetch_failed", "kept only if confirmed", "var(--muted)", "M4 8 H12")]
    for i, (st, act, col, icon) in enumerate(res):
        x = 40 + i * 176
        b.append(f'<g transform="translate({x} {ry + 40})"><circle cx="8" cy="8" r="8" fill="{col}"/>'
                 f'<path d="{icon}" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g>')
        b.append(f'<text class="v" x="{x + 24}" y="{ry + 53}" style="font-family:{MONO}">{st}</text>')
        b.append(f'<text class="m" x="{x + 24}" y="{ry + 74}">{act}</text>')
    return svg(W, H, "\n".join(b), "How Quoteproof works",
               "Decompose into 5 angles, search for claim, URL and exact quote, check each quote with a script, report with an audit line. "
               "Each quote is verified (kept), misattributed (kept, source corrected), not_found (dropped) or fetch_failed (kept only if confirmed).")


# 2. Real checker output. proof/sqlite-wal/results.json, the one misattributed quote.
def run():
    rs = json.load(open("proof/sqlite-wal/results.json"))
    m = next(r for r in rs if r["status"] == "misattributed")
    n, v = len(rs), sum(r["status"] == "verified" for r in rs)
    q = m["quote"]
    cut = q.rfind(" ", 0, 74)
    lines = [("$ python3 verify_quotes.py claims.json", "p"), ("…", "d"), ("{", ""),
             (f'  "quote": "{q[:cut]}', ""), (f'            {q[cut + 1:]}",', ""),
             (f'  "source": "{m["source"]}",', ""),
             ('  "status": "misattributed",', "hot"),
             (f'  "found_in": "{m["found_in"]}"', "hot"), ("}", "")]
    W, H = 760, 80 + len(lines) * 21 + 24 + 52
    b = ['<text class="t" x="24" y="38">Real output: a wrong page, caught and corrected</text>',
         f'<text class="s" x="24" y="60">SQLite research run: {n} quotes checked, {v} verified, 1 cited to the wrong page.</text>',
         f'<rect x="24" y="80" width="712" height="{len(lines) * 21 + 24}" rx="8" fill="var(--grid)" fill-opacity="0.45" stroke="var(--border)"/>']
    for i, (ln, kind) in enumerate(lines):
        y = 106 + i * 21
        style = {"p": "fill:var(--ink2)", "d": "fill:var(--muted)", "hot": "fill:var(--accent);font-weight:700"}.get(kind, "")
        b.append(f'<text x="40" y="{y}" style="font-family:{MONO};font-size:13px;{style}" xml:space="preserve">{esc(ln)}</text>')
    b.append(f'<text class="m" x="24" y="{H - 18}">The quote is real, but on pragma.html, not wal.html. The report cites pragma.html. Data: proof/sqlite-wal/results.json</text>')
    return svg(W, H, "\n".join(b), "Real output: a wrong page, caught and corrected",
               f"Checker output from the SQLite run: {n} quotes, {v} verified, one misattributed quote found on pragma.html instead of the cited wal.html.")


# 3. GitHub social preview cards, 1280x640 (GitHub keeps a 40px safe border).
MARK = ('<g transform="translate({x} {y}) scale({s})"><circle cx="180" cy="214" r="60" fill="#ffffff"/>'
        '<path d="M240 214 C 240 300, 198 350, 126 374 L 116 348 C 160 330, 184 302, 186 273 Z" fill="#ffffff"/>'
        '<path d="M278 262 L 328 312 L 412 196" fill="none" stroke="#2ecc8a" stroke-width="50" stroke-linecap="round" stroke-linejoin="round"/></g>')


def social(title, tagline, chips, foot):
    b = [f'<rect width="1280" height="640" fill="#142033"/>', MARK.format(x=72, y=60, s=0.5),
         f'<text x="96" y="368" style="font-size:84px;font-weight:700;fill:#ffffff">{esc(title)}</text>',
         f'<text x="96" y="430" style="font-size:34px;fill:#c9d4e3">{esc(tagline)}</text>']
    x = 96
    for big, small in chips:
        w = 40 + max(len(big) * 22, len(small) * 11.5)
        b.append(f'<rect x="{x}" y="478" width="{w:.0f}" height="92" rx="14" fill="#ffffff" fill-opacity="0.08" stroke="#ffffff" stroke-opacity="0.18"/>')
        b.append(f'<text x="{x + 20}" y="520" style="font-size:36px;font-weight:700;fill:#2ecc8a">{esc(big)}</text>')
        b.append(f'<text x="{x + 20}" y="552" style="font-size:20px;fill:#c9d4e3">{esc(small)}</text>')
        x += w + 20
    b.append(f'<text x="1184" y="96" text-anchor="end" style="font-size:24px;fill:#8ea0b8">{esc(foot)}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 640" width="1280" height="640">'
            f'<style>text{{font-family:{FONT}}}</style>{"".join(b)}</svg>')


def png(svg_text, path, w, h, scale=1, dark=False):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(f'<html><head><meta name="color-scheme" content="{"dark" if dark else "light"}"></head>'
                f'<body style="margin:0;background:transparent">{svg_text}</body></html>')
    flags = ["--force-dark-mode", "--blink-settings=preferredColorScheme=0"] if dark else []
    subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--hide-scrollbars", *flags,
                    f"--force-device-scale-factor={scale}", f"--window-size={w},{h}", "--default-background-color=00000000",
                    f"--screenshot={path}", f"file://{f.name}"], check=True, capture_output=True)
    pathlib.Path(f.name).unlink()


if __name__ == "__main__":
    SOCIAL.mkdir(parents=True, exist_ok=True)
    gen = {"workflow": workflow, "run": run}
    for name in ["workflow", "run", "misquotes", "stress", "coverage", "tokens"]:  # last 4 come from make_charts.py
        if name in gen:
            (OUT / f"{name}.svg").write_text(gen[name]())
        s = (OUT / f"{name}.svg").read_text()
        h = int(s.split('height="')[1].split('"')[0])
        for dark in (False, True):
            png(s, OUT / f"{name}-{'dark' if dark else 'light'}.png", 760, h, scale=2, dark=dark)
        print("wrote", OUT / f"{name}.svg", "+ PNGs")
    cards = {"core": social("Quoteproof", "Research where every quote is checked against its source.",
                            [("45/45", "planted errors caught"), ("2", "real misquotes caught"), ("82/83", "quotes verified, PDFs too")],
                            "github.com/andre-arc/Quoteproof"),
             "community": social("Quoteproof Community", "Free research skill. Every quote checked on its web page.",
                                 [("Free", "MIT licensed"), ("5", "research angles"), ("Word for word", "quote check by code")],
                                 "Claude Code skill")}
    for name, s in cards.items():
        png(s, SOCIAL / f"{name}.png", 1280, 640)
        print("wrote", SOCIAL / f"{name}.png")
