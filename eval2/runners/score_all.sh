#!/usr/bin/env bash
# Re-score all PGNs in pgn/ and write results/SUMMARY.md and per-engine cards.
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE"
python3 - <<'PY'
import json, sys
from pathlib import Path
sys.path.insert(0, "lib")
from lib import manifest, score

engs, anchors = manifest.load()
res_dir = Path("results"); per = res_dir / "per_engine"; per.mkdir(parents=True, exist_ok=True)

# Aggregate per engine across pass1 + pass2; pass2 wins on conflicts.
table = []
for e in engs:
    if e.corpus != "main":
        continue
    pgn_dirs = ["pgn/pass2", "pgn/pass1"]
    elo_iv = ci = ngames = None
    for d in pgn_dirs:
        if not Path(d).exists():
            continue
        agg = score.score_one_engine_vs_sf(e.name, Path(d))
        if agg["elo_iv"] is not None:
            elo_iv, ci, ngames = agg["elo_iv"], agg["ci95"], agg["n_games"]
            break
    card = {"engine": e.name, "tier": e.tier, "elo_iv": elo_iv,
            "ci95": ci, "n_games": ngames}
    pf = per / f"{e.name}.preflight.uci.json"
    if pf.exists():
        card["preflight_uci_ok"] = json.loads(pf.read_text()).get("ok")
    perft_pf = per / f"{e.name}.preflight.perft.json"
    if perft_pf.exists():
        card["preflight_perft_ok"] = json.loads(perft_pf.read_text()).get("ok")
    tac_pf = per / f"{e.name}.preflight.tactics.json"
    if tac_pf.exists():
        card["wac_pct"] = json.loads(tac_pf.read_text()).get("pct_solved")
    (per / f"{e.name}.card.json").write_text(json.dumps(card, indent=2))
    table.append(card)

table.sort(key=lambda c: -(c["elo_iv"] or -1))
lines = ["# eval2 — canonical Elo summary", "",
         "| Engine | Tier | Elo | ±95% | Games | UCI | Perft | WAC % |",
         "|---|---|---:|---:|---:|---|---|---:|"]
for c in table:
    lines.append("| {engine} | {tier} | {elo} | {ci} | {n} | {u} | {p} | {w} |".format(
        engine=c["engine"], tier=c["tier"],
        elo=c["elo_iv"] or "—", ci=c["ci95"] or "—", n=c["n_games"] or 0,
        u="✓" if c.get("preflight_uci_ok") else "✗",
        p="✓" if c.get("preflight_perft_ok") else "✗",
        w=c.get("wac_pct") or "—",
    ))
Path("results/SUMMARY.md").write_text("\n".join(lines) + "\n")
print("wrote results/SUMMARY.md and per_engine/*.card.json")
PY
