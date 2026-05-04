#!/usr/bin/env bash
# Phase 3b: focused calibrated pass at 120+1. For each engine, plays
# only the rungs within ±N of its Pass-1 estimate.
#
# Read Pass-1 results per engine, find the SF rung whose score is closest
# to 50%, and play the 4 rungs around it (±2) at full 120+1 with 20
# games per rung and SPRT.
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE"
mkdir -p pgn/pass2 logs/pass2

TARGETS=("$@")
if [ ${#TARGETS[@]} -eq 0 ]; then
  mapfile -t TARGETS < <(python3 - <<'PY'
import json, sys
from pathlib import Path
sys.path.insert(0, "lib")
import manifest
engs, _ = manifest.load()
for e in engs:
    if e.corpus != "main":
        continue
    if list(Path("pgn/pass1").glob(f"{e.name}_sf*.pgn")):
        print(e.name)
PY
)
fi

read TC GAMES <<<"$(python3 -c 'import json
d=json.load(open("ladder.json"))["phases"]["3b_pass2_focused"]
print(d["tc"], d["games_per_rung"])')"
SPAN=$(python3 -c 'import json; print(json.load(open("ladder.json"))["phases"]["3b_pass2_focused"]["rungs_around_pass1"])')
mapfile -t ALL_RUNGS < <(python3 -c 'import json; [print(r) for r in json.load(open("ladder.json"))["stockfish"]["rungs_uci_elo"]]')

for engine in "${TARGETS[@]}"; do
  # Find best central rung from pass1: rung whose score is closest to 0.5.
  central=$(python3 - <<PY
import sys; sys.path.insert(0,"lib")
from pathlib import Path
from lib import score
agg = score.score_one_engine_vs_sf("$engine", Path("pgn/pass1"))
if not agg["per_rung"]:
    print(800); raise SystemExit
best = min(agg["per_rung"], key=lambda r: abs(r["score"]-0.5))
print(best["rung"])
PY
)
  echo "=== $engine (central=$central) ==="
  image=$(python3 -c "
import sys; sys.path.insert(0,'lib')
import manifest
e=manifest.by_name(manifest.load()[0])['$engine']
print(e.image)")
  for rung in "${ALL_RUNGS[@]}"; do
    diff=$((rung - central))
    abs=${diff#-}
    step=$((abs / 200))
    if [ "$step" -gt "$SPAN" ]; then continue; fi
    pgn="pgn/pass2/${engine}_sf${rung}.pgn"
    log="logs/pass2/${engine}_sf${rung}.log"
    if [ -s "$pgn" ]; then echo "skip $engine vs sf${rung}"; continue; fi
    echo "  pass2: $engine vs sf${rung} at $TC ($GAMES games)"
    cutechess-cli \
      -engine name="$engine" cmd=wrappers/docker_engine.sh arg="$image" proto=uci \
      -engine name="sf${rung}" cmd=wrappers/docker_engine.sh arg=eval2/stockfish:16.1 proto=uci \
        option.UCI_LimitStrength=true option.UCI_Elo="$rung" option.Threads=1 option.Hash=128 \
      -each tc="$TC" \
      -openings file=fixtures/openings.epd format=epd order=random \
      -games 2 -rounds $((GAMES/2)) -repeat -concurrency 1 \
      -sprt elo0=-25 elo1=25 alpha=0.05 beta=0.05 \
      -resign movecount=5 score=900 \
      -draw movenumber=40 movecount=6 score=10 \
      -pgnout "$pgn" min \
      > "$log" 2>&1 || true
  done
done
echo "pass2 done."
