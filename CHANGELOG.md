# Changelog

## 2026-11-09

- Fixed (Pro): a quote shortened with `…` could join two real passages from far apart on a page into something the source never said, and still pass as verified. Pieces of a shortened quote must now be within 60 words of each other, and each piece needs at least 2 words. Reported by u/Elegant_Yam2783 on r/ClaudeAI.
