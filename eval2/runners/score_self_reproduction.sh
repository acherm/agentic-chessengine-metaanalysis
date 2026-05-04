#!/usr/bin/env bash
# Compute self-reported-reproduction Elo and write
# results/self_reproduction_report.md: for each engine, shows the
# Elo we measured under its original setup alongside its anchor-based
# Elo (from run_anchor_gauntlet) and the original public claim.
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE"
python3 - <<'PY'
import json, math, re, sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, "lib")
import manifest

def parse_pgn(path, eng_name, opp_name):
    white = None; scores = []
    for line in open(path):
        line = line.strip()
        m = re.match(r'\[White "([^"]+)"\]', line)
        if m: white = m.group(1)
        m = re.match(r'\[Result "([^"]+)"\]', line)
        if m and white:
            r = m.group(1)
            if r != "*":
                s = {"1-0":1.0,"0-1":0.0,"1/2-1/2":0.5}.get(r)
                if s is not None:
                    if white == eng_name:   scores.append(s)
                    elif white == opp_name: scores.append(1.0 - s)
                white = None
    return scores

engs, _ = manifest.load()
eng_by = manifest.by_name(engs)

# For each engine, aggregate its self-reproduction pairings.
rows = []
for pgn_path in sorted(Path("pgn/self_reproduction").glob("*.pgn")):
    m = re.match(r"(.+)_vs_sf(\d+)_.*\.pgn", pgn_path.name)
    if not m: continue
    eng, rung = m.group(1), int(m.group(2))
    opp_name = f"sf{rung}"
    scores = parse_pgn(pgn_path, eng, opp_name)
    if not scores: continue
    n = len(scores); s = sum(scores); pct = s/n
    pc = max(1e-3, min(1-1e-3, pct))
    diff = -400*math.log10(1/pc-1)
    se = 400/(math.log(10)*pc*(1-pc)) * math.sqrt(pc*(1-pc)/n)
    # "Reproduced self-Elo" = SF_rung nominal + diff
    reproduced = rung + diff
    rows.append({"engine": eng, "opp": opp_name, "rung": rung, "n": n,
                 "pct": pct, "diff": diff, "se": se, "elo": reproduced})

# Group by engine, inverse-variance aggregate within engine
per_engine = defaultdict(list)
for r in rows: per_engine[r["engine"]].append(r)

summary = []
for eng, pairs in per_engine.items():
    meas = [p for p in pairs if 0.02 < p["pct"] < 0.98]
    if not meas: continue
    w = [1/(p["se"]**2) for p in meas]
    total = sum(w)
    elo = sum(p["elo"]*wi for p, wi in zip(meas, w)) / total
    ci95 = 1.96*math.sqrt(1/total)
    summary.append({"engine": eng, "repro_elo": round(elo,0), "ci95": round(ci95,0),
                    "per_rung": [(p["opp"], round(p["pct"],3), round(p["elo"],0), p["n"])
                                 for p in pairs]})

# Load anchor-based Elo from previous step.
anchor_elos = {}
for p in Path("results/anchor").glob("*.anchor.json"):
    d = json.loads(p.read_text())
    anchor_elos[d["engine"]] = d.get("elo")

lines = ["# Self-reproduction vs anchor-based Elo", "",
         "Each engine was re-run against SF under its own original self-eval config",
         "(TC, SF hash, UCI_Elo rungs). The reproduced number shows what we get under",
         "the same setup; the anchor-based number shows what the engine is worth on",
         "the CCRL 40/4 scale (Rustic 1820 + Asymptote 2150).",
         "",
         "| Engine | Reproduced Elo (self-setup) | ±95 | Anchor-based Elo | Δ (repro − anchor) |",
         "|---|---:|---:|---:|---:|"]
for s in sorted(summary, key=lambda x: -x["repro_elo"]):
    anchor = anchor_elos.get(s["engine"])
    delta = round(s["repro_elo"] - anchor, 0) if anchor else "—"
    anchor_s = str(anchor) if anchor else "—"
    lines.append(f"| {s['engine']} | {s['repro_elo']:.0f} | ±{s['ci95']:.0f} | {anchor_s} | {delta} |")
Path("results/self_reproduction_report.md").write_text("\n".join(lines) + "\n")
print("wrote results/self_reproduction_report.md ({} engines)".format(len(summary)))
PY
