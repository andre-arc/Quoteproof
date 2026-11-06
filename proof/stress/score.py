"""Score results.json against the known errors in stress.json."""
import collections, json
same = lambda a, b: a and b and a.replace("://www.", "://") == b.replace("://www.", "://")  # www. and bare host are one page
S = json.load(open("proof/stress/stress.json")); R = json.load(open("proof/stress/results.json"))
rows = collections.defaultdict(lambda: [0, 0])
for s, r in zip(S, R):
    ok = r["status"] == s["expect"] and (s["expect"] != "misattributed" or same(r.get("found_in"), s["true_source"]))
    rows[s["mutation"]][0] += ok; rows[s["mutation"]][1] += 1
for m, (a, b) in rows.items(): print(f"| {m} | {b} | {a}/{b} |")
print(f"| **total** | {len(S)} | **{sum(a for a, _ in rows.values())}/{len(S)}** |")
