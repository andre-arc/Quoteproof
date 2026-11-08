"""Build the proof visuals in assets/proof/ as theme-aware SVGs (light + dark via prefers-color-scheme).

Run from the repo root:  python3 proof/charts/make_charts.py
Numbers come from the files in proof/ (cited next to each chart below).
"""
import pathlib

OUT = pathlib.Path("assets/proof")
FONT = 'system-ui, -apple-system, "Segoe UI", Helvetica, Arial, sans-serif'

# Reference palette (dataviz skill): accent = categorical slot 1, de-emphasis = neutral gray.
STYLE = """<style>
  svg { --surface:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --muted:#898781; --grid:#e1e0d9; --axis:#c3c2b7;
        --accent:#2a78d6; --accent-wash:rgba(42,120,214,0.14); --gray:#c3c2b7; --on-gray:#0b0b0b;
        --bad:#d03b3b; --bad-wash:rgba(208,59,59,0.12); --border:rgba(11,11,11,0.10); }
  @media (prefers-color-scheme: dark) {
    svg { --surface:#1a1a19; --ink:#f0efec; --ink2:#c3c2b7; --muted:#898781; --grid:#2c2c2a; --axis:#383835;
          --accent:#3987e5; --accent-wash:rgba(57,135,229,0.22); --gray:#5c5b56; --on-gray:#ffffff;
          --bad:#e66767; --bad-wash:rgba(230,103,103,0.18); --border:rgba(255,255,255,0.10); }
  }
  text { font-family: %s; fill: var(--ink); }
  .t { font-size: 17px; font-weight: 600; }
  .s { font-size: 13px; fill: var(--ink2); }
  .l { font-size: 13px; }
  .m { font-size: 12px; fill: var(--muted); font-variant-numeric: tabular-nums; }
  .v { font-size: 13px; font-weight: 600; font-variant-numeric: tabular-nums; }
  .in { font-size: 12px; font-weight: 600; fill: #ffffff; }
  .ingray { font-size: 12px; font-weight: 600; fill: var(--on-gray); }
  .hero { font-size: 44px; font-weight: 600; }
  .q { font-size: 15px; }
</style>""" % FONT


def svg(w, h, body, title, desc):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
            f'aria-labelledby="t d">\n<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n{STYLE}\n'
            f'<rect width="{w}" height="{h}" rx="12" fill="var(--surface)" stroke="var(--border)"/>\n{body}\n</svg>\n')


def bar(x, y, w, h, fill, round_end=True):
    """Horizontal bar: square at the baseline (left), 4px rounded data end (right)."""
    if w <= 0:
        return ""
    r = min(4, w / 2, h / 2) if round_end else 0
    return (f'<path d="M{x} {y} H{x + w - r} Q{x + w} {y} {x + w} {y + r} V{y + h - r} '
            f'Q{x + w} {y + h} {x + w - r} {y + h} H{x} Z" fill="{fill}"/>')


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# 1. Community vs Pro coverage — proof/http3-quic/run2/claims.json, both checkers (see core README).
def coverage():
    W, H, X0, PW = 760, 250, 150, 470
    total, rows = 83, [("Community", 47, 36), ("Pro", 82, 1)]
    sx = PW / total
    b = [f'<text class="t" x="24" y="38">Quotes each edition could check</text>',
         f'<text class="s" x="24" y="60">The same 83 quotes from the HTTP/3 research run (35 from research PDFs)</text>',
         # legend
         f'<rect x="24" y="78" width="12" height="12" rx="3" fill="var(--accent)"/><text class="l" x="42" y="89">Checked word for word</text>',
         f'<rect x="210" y="78" width="12" height="12" rx="3" fill="var(--gray)"/><text class="l" x="228" y="89">Couldn\'t be read (PDFs, blocked sites)</text>']
    for t in range(0, 81, 20):  # gridlines + ticks
        x = X0 + t * sx
        b.append(f'<line x1="{x:.1f}" y1="110" x2="{x:.1f}" y2="196" stroke="var(--grid)"/>')
        b.append(f'<text class="m" x="{x:.1f}" y="214" text-anchor="middle">{t}</text>')
    b.append(f'<line x1="{X0}" y1="108" x2="{X0}" y2="198" stroke="var(--axis)"/>')
    for i, (name, ok, bad) in enumerate(rows):
        y = 124 + i * 40
        b.append(f'<text class="l" x="{X0 - 12}" y="{y + 16}" text-anchor="end">{name}</text>')
        wo, wb = ok * sx, bad * sx
        b.append(bar(X0, y, wo - 1, 24, "var(--accent)", round_end=False))
        b.append(bar(X0 + wo + 1, y, wb - 1, 24, "var(--gray)"))
        b.append(f'<text class="in" x="{X0 + 8}" y="{y + 16}">{ok} checked</text>')
        if wb > 92:
            b.append(f'<text class="ingray" x="{X0 + wo + 9}" y="{y + 16}">{bad} unreadable</text>')
        else:
            b.append(f'<text class="v" x="{X0 + wo + wb + 8}" y="{y + 16}">{bad} unreadable</text>')
    b.append(f'<text class="m" x="{X0 + PW}" y="236" text-anchor="end">quotes</text>')
    return svg(W, H, "\n".join(b), "Quotes each edition could check",
               "Of 83 quotes, Community checked 47 and could not read 36; Pro checked 82 and could not read 1.")


# 2. Research tokens vs Claude deep research — proof/vs-deep-research/README.md.
def tokens():
    W, H, X0, PW = 760, 238, 270, 400
    rows = [("Quoteproof", "5 searchers on Haiku", 78517, "var(--accent)"),
            ("Claude deep research", "4 researchers on the main model", 278826, "var(--gray)")]
    mx = 300000
    sx = PW / mx
    b = [f'<text class="t" x="24" y="38">Research tokens, same topic</text>',
         f'<text class="s" x="24" y="60">"SQLite WAL vs rollback journal for concurrent writes" — research phase only</text>']
    for t in range(0, mx + 1, 100000):
        x = X0 + t * sx
        b.append(f'<line x1="{x:.1f}" y1="80" x2="{x:.1f}" y2="170" stroke="var(--grid)"/>')
        b.append(f'<text class="m" x="{x:.1f}" y="188" text-anchor="middle">{"0" if t == 0 else f"{t // 1000}K"}</text>')
    b.append(f'<line x1="{X0}" y1="78" x2="{X0}" y2="172" stroke="var(--axis)"/>')
    for i, (name, sub, v, fill) in enumerate(rows):
        y = 92 + i * 42
        b.append(f'<text class="l" x="{X0 - 12}" y="{y + 10}" text-anchor="end" font-weight="600">{name}</text>')
        b.append(f'<text class="m" x="{X0 - 12}" y="{y + 25}" text-anchor="end">{sub}</text>')
        b.append(bar(X0, y, v * sx, 24, fill))
        b.append(f'<text class="v" x="{X0 + v * sx + 8}" y="{y + 17}">{v / 1000:.1f}K</text>')
    b.append(f'<text class="s" x="24" y="216">Quoteproof used about 28% of the tokens, on a cheaper model. Report-writing tokens are not included.</text>')
    return svg(W, H, "\n".join(b), "Research tokens, same topic",
               "Quoteproof's research phase used 78,517 tokens on Haiku; Claude deep research used 278,826 on the main model.")


# 3. Stress test — proof/stress/stress.json + results.json, scored by proof/stress/score.py.
def stress():
    groups = [("Untouched (control)", 10), ("Paraphrased", 10), ("Meaning changed", 10),
              ("Wrong page cited", 10), ("Fabricated quote", 5)]
    W, H, X0, S, G = 760, 330, 210, 22, 6
    b = [f'<text class="hero" x="24" y="66">45/45</text>',
         f'<text class="t" x="168" y="46">Stress test: every planted error caught</text>',
         f'<text class="s" x="168" y="68">35 quotes damaged on purpose, 10 left intact. Each square is one quote, classified correctly.</text>']
    check = "M5.5 11.5 L9.5 15.5 L16.5 7.5"
    for i, (name, n) in enumerate(groups):
        y = 100 + i * 42
        b.append(f'<text class="l" x="{X0 - 14}" y="{y + 15}" text-anchor="end">{name}</text>')
        for k in range(n):
            x = X0 + k * (S + G)
            b.append(f'<g transform="translate({x} {y})"><rect width="{S}" height="{S}" rx="4" fill="var(--accent)"/>'
                     f'<path d="{check}" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g>')
        b.append(f'<text class="v" x="{X0 + 10 * (S + G) + 8}" y="{y + 15}">{n}/{n}</text>')
    return svg(W, H, "\n".join(b), "Stress test: 45 of 45 correct",
               "Controls 10/10, paraphrased 10/10, meaning changed 10/10, wrong page cited 10/10, fabricated 5/5.")


# 4. The two misquotes caught in run 1 — proof/http3-quic/README.md.
def misquotes():
    W, H = 760, 318
    ex = [("IMDEA / MONROE paper, 2021",
           ["QUIC-based operations are advantageous ", ("in case of", "keep"), " users that move"],
           ["QUIC-based operations are advantageous ", ("for", "bad"), " users that move"]),
          ("Yu &amp; Benson, WWW 2021",
           ["QUIC’s removal of HOL ", ("(head-of-line)", "keep"), " blocking has little impact…"],
           ["QUIC’s removal of HOL ", ("[missing]", "bad"), " blocking has little impact…"])]
    b = [f'<text class="t" x="24" y="38">Two misquotes caught before the report</text>',
         f'<text class="s" x="24" y="60">Close enough that a reader, or the model checking its own notes, accepts them. The checker didn\'t.</text>']
    y = 98
    for src, paper, quoted in ex:
        b.append(f'<text class="m" x="24" y="{y}">{src}</text>')
        for row, (lab, parts) in enumerate((("Paper", paper), ("Agent quoted", quoted))):
            yy = y + 26 + row * 28
            b.append(f'<text class="m" x="24" y="{yy}">{lab}</text>')
            spans = []
            for part in parts:
                if isinstance(part, tuple):
                    txt, kind = part
                    style = "fill:var(--accent)" if kind == "keep" else "fill:var(--bad)"
                    spans.append(f'<tspan font-weight="700" text-decoration="underline" style="{style}">{txt}</tspan>')
                else:
                    spans.append(f"<tspan>{part}</tspan>")
            b.append(f'<text class="q" x="124" y="{yy}">“{"".join(spans)}”</text>')
        yy = y + 26 + 2 * 28 - 2
        b.append(f'<g transform="translate(124 {yy - 14})"><rect width="172" height="22" rx="11" fill="var(--bad-wash)"/>'
                 f'<path d="M11 7 L17 13 M17 7 L11 13" stroke="var(--bad)" stroke-width="2" stroke-linecap="round" transform="translate(0 1)"/>'
                 f'<text class="v" x="26" y="15.5">not_found · dropped</text></g>')
        y += 116
    return svg(W, H, "\n".join(b), "Two misquotes caught before the report",
               "An agent quoted 'advantageous for users that move' where the paper says 'in case of'; another quote dropped '(head-of-line)'. Both were not found on the page and dropped.")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in [("coverage", coverage), ("tokens", tokens), ("stress", stress), ("misquotes", misquotes)]:
        (OUT / f"{name}.svg").write_text(fn())
        print("wrote", OUT / f"{name}.svg")
