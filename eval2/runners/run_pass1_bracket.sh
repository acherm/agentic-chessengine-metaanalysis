#!/usr/bin/env bash
# Phase 3a: fast bracketing pass. Plays every engine vs the full SF
# ladder at tc=30+0.3, ~10 games/rung, with SPRT early-stop. Produces
# a rough Elo bracket per engine that Pass-2 then refines at 120+1.
#
# Usage:
#   ./runners/run_pass1_bracket.sh                  # all engines that passed preflight
#   ./runners/run_pass1_bracket.sh chess-rust-cc    # one engine
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE"
mkdir -p pgn/pass1 logs/pass1

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
    pf = Path("results/per_engine") / f"{e.name}.preflight.uci.json"
    if pf.exists() and json.loads(pf.read_text()).get("ok"):
        print(e.name)
PY
)
fi

read TC GAMES CONC <<<"$(python3 -c 'import json
d=json.load(open("ladder.json"))["phases"]["3a_pass1_bracket"]
print(d["tc"], d["games_per_rung"], d["concurrency"])')"
mapfile -t RUNGS < <(python3 -c 'import json; [print(r) for r in json.load(open("ladder.json"))["stockfish"]["rungs_uci_elo"]]')

for engine in "${TARGETS[@]}"; do
  echo "=== $engine ==="
  image=$(python3 -c "
import sys; sys.path.insert(0,'lib')
import manifest
e=manifest.by_name(manifest.load()[0])['$engine']
print(e.image, e.tier)")
  read engine_image engine_tier <<<"$image"
  for rung in "${RUNGS[@]}"; do
    pgn="pgn/pass1/${engine}_sf${rung}.pgn"
    log="logs/pass1/${engine}_sf${rung}.log"
    if [ -s "$pgn" ]; then echo "skip $engine vs sf${rung} (pgn exists)"; continue; fi
    echo "  pass1: $engine vs sf${rung} at $TC ($GAMES games, conc=$CONC)"
    cutechess-cli \
      -engine name="$engine" cmd=wrappers/docker_engine.sh arg="$engine_image" proto=uci \
      -engine name="sf${rung}" cmd=wrappers/docker_engine.sh arg=eval2/stockfish:16.1 proto=uci \
        option.UCI_LimitStrength=true option.UCI_Elo="$rung" option.Threads=1 option.Hash=128 \
      -each tc="$TC" \
      -openings file=fixtures/openings.epd format=epd order=random \
      -games 2 -rounds $((GAMES/2)) -repeat -concurrency "$CONC" \
      -sprt elo0=-50 elo1=50 alpha=0.05 beta=0.05 \
      -resign movecount=5 score=900 \
      -draw movenumber=40 movecount=6 score=10 \
      -pgnout "$pgn" min \
      > "$log" 2>&1 || true
  done
done
echo "pass1 done."
