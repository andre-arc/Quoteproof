# Proof

Two tests, all data included. Both ran Quoteproof's quote checker exactly as it ships in the skill.

A third comparison, against Claude's deep research on the same topic (cost, time, citation accuracy and coverage), is in [vs-deep-research/](vs-deep-research/README.md).

## 1. Real research run: SQLite WAL vs rollback journal

Quoteproof researched *"SQLite WAL vs rollback journal for concurrent writes"* from 5 angles. The research agents (Claude Haiku) collected **78 claims from 14 source pages**. Then the checker fetched each page once and matched every quote.

| Result | Claims |
| :-- | --: |
| verified (quote is on the cited page) | 77 |
| **misattributed (real quote, wrong page cited)** | **1** |
| not found | 0 |
| fetch failed | 0 |

The catch: a research agent attributed *"The synchronous=NORMAL setting provides the best balance between performance and safety for most applications running in WAL mode"* to `sqlite.org/wal.html`. It is on [`sqlite.org/pragma.html`](https://sqlite.org/pragma.html). The quote is real, so a model reviewing its own notes accepts it. The checker found it on the other page and corrected the source.

Files: [`sqlite-wal/claims.json`](sqlite-wal/claims.json) (input) · [`sqlite-wal/results.json`](sqlite-wal/results.json) (checker output) · [`sqlite-wal/report.md`](sqlite-wal/report.md) (final report).

## 2. Stress test: 45 claims with known errors

Real research produces few errors, so this test plants them. [`stress/make_stress.py`](stress/make_stress.py) takes 40 verified claims from run 1 (random, seed 7), damages 30 of them in known ways, and adds 5 invented quotes.

| Planted error | Claims | Caught |
| :-- | --: | --: |
| none (control, must pass) | 10 | 10/10 |
| paraphrased: two adjacent words swapped | 10 | 10/10 |
| meaning changed: "not" removed, number changed, word added | 10 | 10/10 |
| wrong page cited (must name the right page) | 10 | 10/10 |
| fabricated quote | 5 | 5/5 |
| **total** | **45** | **45/45** |

Runtime: 18 s for 45 claims across 14 pages on a home connection. Fetching dominates; each page is fetched once per run.

Scoring note: one wrong-page claim was found on `www.sqlite.org/wal.html` while the scorer expected `sqlite.org/wal.html`. They are the same page, so [`stress/score.py`](stress/score.py) treats `www.` and the bare host as equal.

## Reproduce

Data and scorer are here. The checker itself ships with the Quoteproof skill. From the repo root:

```bash
python3 proof/stress/make_stress.py                    # rebuilds proof/stress/stress.json
python3 <skill>/scripts/verify_quotes.py proof/stress/stress.json > proof/stress/results.json
python3 proof/stress/score.py
```

Source pages change over time, so a rerun months later may differ where sqlite.org has edited its docs.

## What this does not show

- **Support, not just presence.** The checker proves a quote exists on the page. Whether it supports the claim is still the model's judgment.
- **Breadth.** One topic, 14 pages, all HTML documentation. PDF checking was added later and is exercised in [vs-deep-research/](vs-deep-research/README.md), not here.
- **Search quality.** These tests measure the checker, not how good the sources the agents find are.
