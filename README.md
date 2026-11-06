<p align="center"><img src="assets/logo-128.png" width="96" height="96" alt="Quoteproof logo"></p>

<h1 align="center">Quoteproof</h1>
<p align="center"><b>Research where every quote is checked against its source.</b></p>

---

AI research reports cite sources with confidence. The quotes are often paraphrased, misremembered or pinned to the wrong page, and asking the model to double-check means trusting the same model that made the mistake.

Quoteproof is an agent skill that checks with code instead. After researching, it fetches every cited page and matches each quote word for word.

## How it works

1. **Decompose.** Splits your topic into 5 angles chosen for that topic.
2. **Search.** Researches the angles in parallel. Every claim is recorded as *claim → source URL → verbatim quote*.
3. **Verify.** Drops contradictions and marketing, then runs the bundled checker on every quote:
   | Result | Meaning | Action |
   | :-- | :-- | :-- |
   | `verified` | Quote is on the cited page | kept |
   | `misattributed` | Quote is real but on a different cited page | kept, source corrected |
   | `not_found` | Quote is on no fetched page | dropped |
   | `fetch_failed` | Page could not be loaded | kept only if confirmed manually |
4. **Report.** A cited report: findings, recommendations, trade-offs and open questions, ending with an audit line of claims checked, verified, corrected and dropped.

## Proof

| Test | Result |
| :-- | :-- |
| Real research run (78 claims, 14 pages) | 77 verified, **1 wrong-page citation caught and corrected** |
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

## Limitations

- Checks that a quote **exists** on its page, not that it **supports** the claim.
- HTML pages only; PDF quote matching is not supported yet.
- Needs Python 3.10+ for the checker; without it, the agent checks quotes itself.
- Fetches the cited source URLs, so it needs network access.

## Get it

Available on [Agensi](https://www.agensi.io) *(listing link coming soon)*. Works with Claude Code and other agents that support `SKILL.md` skills.

---

<sub>© 2026 andre-arc. Logo and brand assets: all rights reserved. Proof data in `proof/` may be reused with attribution.</sub>
