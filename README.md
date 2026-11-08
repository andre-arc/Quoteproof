<p align="center"><img src="assets/logo-128.png" width="96" height="96" alt="Quoteproof logo"></p>

<h1 align="center">Quoteproof</h1>
<p align="center"><b>Research where every quote is checked against its source.</b></p>

---

AI research reports cite sources with confidence. The quotes are often paraphrased, misremembered or pinned to the wrong page, and asking the model to double-check means trusting the same model that made the mistake.

Quoteproof is an agent skill that checks with code instead. After researching, it fetches every cited page and matches each quote word for word.

## Try it free

**[Quoteproof Community](community/quoteproof-community/)** is MIT licensed: the full 5-angle research pipeline with word-for-word quote checking on web pages. Copy the folder into `~/.claude/skills/` and ask your agent to research something. [Pro](https://www.agensi.io/skills/quoteproof) adds PDFs and research papers, exact-text quoting and wrong-page detection; see the [comparison](community/quoteproof-community/README.md#community-vs-pro).

## How it works

1. **Decompose.** Splits your topic into 5 angles chosen for that topic.
2. **Search.** Researches the angles in parallel. Every claim is recorded as *claim → source URL → verbatim quote*.
3. **Verify.** Drops contradictions and marketing, then runs the bundled checker on every quote:
   | Result | Meaning | Action |
   | :-- | :-- | :-- |
   | `verified` | Quote is on the cited page (web page or PDF) | kept |
   | `misattributed` | Quote is real but on a different cited page | kept, source corrected |
   | `not_found` | Quote is on no fetched page | dropped |
   | `fetch_failed` | Page could not be loaded | kept only if confirmed manually |
4. **Report.** A cited report: findings, recommendations, trade-offs and open questions, ending with an audit line of claims checked, verified, corrected and dropped.

## Proof

| Test | Result |
| :-- | :-- |
| Real research run (78 claims, 14 pages) | 77 verified, **1 wrong-page citation caught and corrected** |
| HTTP/3 case study (83 claims, 35 from research PDFs) | 82 verified; an earlier run **caught 2 real misquotes** from papers |
| Stress test with 35 planted errors + 10 controls | **45/45** classified correctly |
| Same topic vs Claude deep research | **~28% of the research tokens**, on a cheaper model. 0 quote errors in the report vs 1 in deep research's |

Deep research covered the topic more broadly; see the [comparison](proof/vs-deep-research/README.md) for what each found. Full data, method and limits: [proof/](proof/README.md).

## Compared with prompt-only research skills

| | Prompt-only "verify your sources" skills | Quoteproof |
| :-- | :-- | :-- |
| Who checks the quote | The same model that wrote it | A script that fetches the page |
| Wrong page cited | Caught only if the model notices | Detected, with the right page named |
| Web access | Often relies on the host | Searches and fetches itself |
| Audit trail | Prose | Per-claim status in JSON |

## Compatibility

| | Status |
| :-- | :-- |
| **Python** | 3.9 – 3.14, tested on each. 3.8 and older do not work. Standard library only. |
| **Claude Code** | Tested end to end (Linux). The skill loads automatically from `~/.claude/skills/`. |
| **Other SKILL.md agents** (Cursor, Codex CLI, Gemini CLI, Windsurf, OpenCode, etc.) | Should work, not yet tested. The agent must be able to **run shell commands**, **search the web** and **write files**. |
| **Parallel research** | Uses subagents where the agent supports them. Agents without subagents research the 5 angles one after another: same result, slower. |
| **Chat apps with a sandbox** (e.g. claude.ai) | Limited. Sandboxes often block outbound network, so the script cannot fetch sources; the agent then checks quotes itself, which is less reliable. |
| **Operating system** | Linux tested. macOS should work (`brew install poppler` for PDFs). Windows untested; the command may be `python` or `py` instead of `python3`. |
| **PDF sources** | Need `pdftotext` (poppler-utils, recommended) or `pypdf`. Without either, PDF quotes are marked unchecked, never verified. Web pages work regardless. |
| **Sources it cannot check** | Pages that need a login or JavaScript to show their text, and sites that block automated requests (seen: Uber's blog). These come back `fetch_failed`; the agent confirms them by hand or drops them. |
| **Network** | Outbound HTTPS to the cited sites. Private and local addresses are refused. |

## Limitations

- Checks that a quote **exists** on its page, not that it **supports** the claim.
- PDF sources need `pdftotext` (poppler-utils, recommended) or `pypdf` installed; without them, PDF quotes are reported as unchecked, never as verified.
- Needs Python 3.9+ for the checker; without it, the agent checks quotes itself.
- Fetches the cited source URLs, so it needs network access.

## Get it

**[Get Quoteproof on Agensi →](https://www.agensi.io/skills/quoteproof)**

Tested with Claude Code; other agents that support `SKILL.md` skills and can run shell commands should work (see Compatibility above).

---

<sub>© 2026 andre-arc. Logo and brand assets: all rights reserved. Proof data in `proof/` may be reused with attribution. Quoteproof Community (`community/`) is MIT licensed.</sub>
