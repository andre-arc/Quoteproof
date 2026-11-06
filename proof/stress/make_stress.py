"""Build a stress set with known errors from the real SQLite claims. Deterministic (seed 7)."""
import json, random
random.seed(7)
real = [c for c in json.load(open("proof/sqlite-wal/results.json")) if c["status"] == "verified"]
sources = sorted({c["source"] for c in real})
picks = random.sample(real, 40)
out = []
for c in picks[:10]:   # untouched -> expect verified
    out.append(dict(c, expect="verified", mutation="none"))
for c in picks[10:20]: # paraphrase: swap two adjacent words -> expect not_found
    w = c["quote"].split(); i = max(1, len(w) // 2); w[i - 1], w[i] = w[i], w[i - 1]
    out.append(dict(c, quote=" ".join(w), expect="not_found", mutation="paraphrased (2 words swapped)"))
for c in picks[20:30]: # number/negation tweak -> expect not_found
    q = c["quote"]
    q2 = q.replace(" not ", " ", 1) if " not " in q else (q.replace("1000", "2000") if "1000" in q else q.replace("one", "two", 1) if " one " in f" {q} " else q + " always")
    out.append(dict(c, quote=q2, expect="not_found", mutation="meaning changed"))
for c in picks[30:40]: # cite the wrong page -> expect misattributed, found_in = true source
    wrong = next(s for s in sources if s != c["source"] and s.split("/")[2] == c["source"].split("/")[2]) if any(s != c["source"] and s.split("/")[2] == c["source"].split("/")[2] for s in sources) else next(s for s in sources if s != c["source"])
    out.append(dict(c, source=wrong, expect="misattributed", true_source=c["source"], mutation="wrong page cited"))
fabricated = [
    ("WAL mode allows multiple simultaneous writers.", "WAL mode allows any number of concurrent writers to commit at the same time."),
    ("synchronous=OFF is safe on power loss.", "With synchronous OFF the database cannot be corrupted by a power failure."),
    ("Checkpoints never block readers.", "Checkpoints of every kind are guaranteed never to block a reader."),
    ("WAL works on NFS.", "WAL mode is fully supported on network filesystems such as NFS."),
    ("Default autocheckpoint is 10000 pages.", "By default SQLite checkpoints when the WAL reaches 10000 pages."),
]
for claim, quote in fabricated:
    out.append(dict(claim=claim, source="https://www.sqlite.org/wal.html", quote=quote, expect="not_found", mutation="fabricated quote"))
for o in out:
    o.pop("status", None); o.pop("found_in", None); o.pop("detail", None)
json.dump(out, open("proof/stress/stress.json", "w"), indent=1)
print(len(out), "stress claims")
