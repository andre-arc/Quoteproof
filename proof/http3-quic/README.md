# Case study: HTTP/3 vs HTTP/2 on lossy mobile networks

Two complete runs of the Quoteproof skill on *"Is HTTP/3 (QUIC) faster than HTTP/2 on lossy mobile networks?"* (2026-11-06). Each run was done by a fresh agent that had only the installed skill to follow: no hints and no knowledge of how it was built. Between the runs we fixed what run 1 exposed. Run 2 is the version that ships.

## Results

| | Run 1 | Run 2 (shipping version) |
| :-- | --: | --: |
| Claims checked | 75 | 83 |
| Claims sourced from PDFs (research papers) | 15 | **35** |
| Verified by the checker | 69 (92%) | **82 (99%)** |
| Misquotes caught | **2** | 0 |
| Source blocked the checker (confirmed by hand) | 4 | 1 |
| Claims in the final report | 70 | 82 |
| Coordinator tokens (searchers on Haiku not included) | 87,977 | 84,678 |
| Wall clock | 5.6 min | 8.1 min |

Run 2's numbers use the current checker. At run time one PDF quote was wrongly rejected because of a footnote number glued to a word ("mobile users1 ."). The checker now strips those footnote markers, and that quote verifies. See [`run2/results-at-run-time.json`](run2/results-at-run-time.json) and [`run2/results-current.json`](run2/results-current.json).

## The two misquotes caught in run 1

Both came from research papers. Both were close enough to the original that a reader, or a model reviewing its own notes, would accept them.

**Yu & Benson, WWW 2021** ([PDF](https://cs.brown.edu/~tab/papers/QUIC_WWW21.pdf))
- Quoted: *"QUIC's removal of HOL blocking has little impact on Page Load Time…"*
- Paper: *"QUIC's removal of HOL **(head-of-line)** blocking has little impact on Page Load Time…"*

**IMDEA / MONROE, 2021** ([PDF](https://dspace.networks.imdea.org/bitstream/20.500.12761/973/1/MedNetCom2021.pdf))
- Quoted: *"QUIC-based operations are advantageous **for** users that move…"*
- Paper: *"QUIC-based operations are advantageous **in case of** users that move…"*

Neither changes the meaning much. That is the point: these are the misquotes that survive human review, and they are why "quoted" should mean quoted. Both were dropped before the report.

## What changed between runs

In run 1 the researchers took quotes from their fetch tool, which returns a model-written summary of the page and cannot read most PDFs. Several primary papers were abandoned, and quotes drifted from the source.

Run 2 added `verify_quotes.py --text URL`, which prints a page's exact text, including from PDFs, in memory. Researchers copied quotes from that. PDF-sourced claims rose from 15 to 35, and checker pass rate from 92% to 99%.

Run 2 cost 4% fewer coordinator tokens than run 1, but took 45% longer because researchers read full page text.

## Files

Each run folder has:
- `claims.json`: every claim submitted for checking, with source and quote
- `results-at-run-time.json`: checker output during the run
- `results-current.json`: output of the current checker on the same claims
- `report.md`: the final report the agent delivered

## Limits

- One topic, one run per version. Search results vary from run to run.
- Token counts cover the coordinating agent only; the five searchers ran on Claude Haiku and are not included.
- The checker proves a quote exists on its page, not that the claim built on it is correct.
