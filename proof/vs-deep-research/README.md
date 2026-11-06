# Quoteproof vs Claude deep research

Same topic, same day (2026-11-06): *"SQLite WAL vs rollback journal for concurrent writes"*. Quoteproof ran with its default settings. Deep research ran as the `deep-research` skill in Claude Code: 4 parallel researchers and 1 report writer, all on the session model.

## Cost and time

| | Quoteproof | Deep research |
| :-- | :-- | :-- |
| Research agents | 5 × Haiku | 4 × session model |
| Research tokens | **78,517** | **278,826** |
| Report tokens | session model, not separately measured | 84,027 |
| Quote check | script: 0 tokens, 18 s for 78 claims | none |
| Wall clock, research phase | about 1 min | about 3.2 min |
| Wall clock, total | not timed | about 5.3 min |

Quoteproof's research phase used about 28% of deep research's tokens, on a cheaper model. Its verify and report step ran in the main session and was not metered separately, so the full-run comparison is incomplete.

## Citation accuracy

Deep research quotes sources directly 21 times (quotes shortened with "…" were split into their pieces). We ran every quote through Quoteproof's checker, then checked each miss by hand.

| | Quoteproof report | Deep research report |
| :-- | :-- | :-- |
| Claims carrying a checkable verbatim quote | 78 of 78 (required) | 21 quotes; most claims are paraphrase + link |
| Checker: verified | 77 | 20 |
| Checker: not found | 0 | 1 |
| Of those, real errors after manual check | — | **1** |
| Of those, false alarms | — | 0 |
| Wrong page cited | 1, caught and corrected before the report | 0 detected |
| Errors that reached the final report | **0** | **1** |

**The error that reached deep research's report:** it attributes *"a VM has its own memory space"* to the [SQLite forum thread](https://sqlite.org/forum/forumpost/292a68c5e4?t=c) as a direct quote. The thread never says it. The closest sentence is *"QEMU provides a private virtual memory space for its VM"*. The substance is right, but a paraphrase is presented as a quotation.

**History: three false alarms, since fixed.** The first version of the checker read HTML only. It flagged *"produces the highest throughput by a wide margin"*, *"slightly less than half as fast"* and *"mostly similar"*, which are all verbatim in the [VLDB 2022 paper](https://par.nsf.gov/servlets/purl/10390276) (PDF). The current checker reads PDFs, rejoins words split across lines, and verifies all three. The table above reflects the current checker; it also still handles quotes shortened with "…" and requires their pieces in the original order.

## Coverage

Deep research was more thorough. Its report includes findings Quoteproof's run did not surface:

- A WAL-reset race that can corrupt databases, present in SQLite 3.7.0–3.51.2 and fixed in 3.51.3 (2026-03-13).
- WAL corruption across VM boundaries (Docker Desktop, VirtioFS bind mounts).
- Multi-worker benchmarks (WordPress PR #483) and the VLDB 2022 paper by SQLite's authors.
- `SQLITE_BUSY_SNAPSHOT` from read-then-write upgrades in `BEGIN DEFERRED`.

## Verdict

- **Quoteproof:** about a quarter of the research tokens on a cheaper model, every claim carries a checkable quote, and no quote error reached the report.
- **Deep research:** broader and deeper findings, at roughly 3.5× the research tokens on the main model. 1 of its 21 direct quotes was a paraphrase in quotation marks, and nothing in its process checks for that.

Use Quoteproof when citations must hold up. Use deep research when coverage matters more than quote accuracy.

## Limits of this comparison

- One topic, one run each. Both pipelines vary run to run.
- Deep research chose its own number of researchers (4); Quoteproof uses 5 angles.
- Token counts come from the subagent usage Claude Code reports. Quoteproof's verify/report step is not included.

## Files

- [`deep-research-report.md`](deep-research-report.md): deep research's full report
- [`deep-research-quotes.json`](deep-research-quotes.json): the 21 quotes extracted from it, each paired with the link that follows it
- [`checker-results.json`](checker-results.json): Quoteproof checker output for those quotes
