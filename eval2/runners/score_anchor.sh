#!/usr/bin/env bash
# Compute anchor-based Elo for every engine and emit results/anchor_summary.md.
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE"
python3 - <<'PY'
import json, sys
from pathlib import Path
sys.path.insert(0, "lib")
import manifest
from score_anchor import score_engine

engs, anchors = manifest.load()
anchor_refs = [(a.name, a.ccrl_40_4_elo) for a in anchors]
res_dir = Path("results/anchor")
res_dir.mkdir(parents=True, exist_ok=True)

rows = []
for e in engs:
    if e.corpus != "main":
        continue
    if e.raw.get("skipped") and not e.host_cmd:
        continue
    r = score_engine(e.name, anchor_refs)
    (res_dir / f"{e.name}.anchor.json").write_text(json.dumps(r, indent=2))
    rows.append((e.name, e.tier, r))

rows.sort(key=lambda x: -(x[2].get("elo") or -1))
lines = ["# Anchor-based Elo summary", "",
         "Elo anchored to CCRL 40/4 via " + ", ".join(f"{n} ({int(e)})" for n, e in anchor_refs) + ".",
         "", "| Engine | Tier | Elo | ±95% CI | Status | Anchors used |",
         "|---|---|---:|---:|---|---|"]
for name, tier, r in rows:
    status = r.get("status", "?")
    elo = r.get("elo", "—")
    ci = r.get("ci95", "—")
    if elo is None:
        lb = r.get("lower_bound"); ub = r.get("upper_bound")
        if lb is not None and ub is None: elo = f">{lb:.0f}"
        elif ub is not None and lb is None: elo = f"<{ub:.0f}"
        elif ub is not None and lb is not None: elo = f"{lb:.0f}—{ub:.0f}"
        else: elo = "—"
        ci = "—"
    anc_used = ",".join(p["anchor"] for p in r.get("per_anchor", [])) or "—"
    lines.append(f"| {name} | {tier} | {elo} | {ci} | {status} | {anc_used} |")
Path("results/anchor_summary.md").write_text("\n".join(lines) + "\n")
print("wrote results/anchor_summary.md with", len(rows), "engines")
PY
