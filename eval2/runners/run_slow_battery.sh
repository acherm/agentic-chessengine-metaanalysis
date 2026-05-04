#!/usr/bin/env bash
# Phase 5: slow-by-design battery (Tier C only).
# Reduced ladder (SF 800/1000), st=30 movetime, 10 games per pairing.
# Plus random-mover baseline + tactical suite at high movetime.
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE"
mkdir -p pgn/slow logs/slow

mapfile -t SLOW < <(python3 - <<'PY'
import sys; sys.path.insert(0,"lib")
import manifest
engs, _ = manifest.load()
for e in engs:
    if e.tier == "C" and e.corpus == "main":
        print(e.name)
PY
)

GAMES=$(python3 -c 'import json; print(json.load(open("ladder.json"))["phases"]["5_slow_battery"]["games_per_pairing"])')
mapfile -t RUNGS < <(python3 -c 'import json; [print(r) for r in json.load(open("ladder.json"))["phases"]["5_slow_battery"]["rungs_uci_elo"]]')
TC="st=30000"

for engine in "${SLOW[@]}"; do
  image=$(python3 -c "
import sys; sys.path.insert(0,'lib')
import manifest
print(manifest.by_name(manifest.load()[0])['$engine'].image)")
  echo "=== slow battery: $engine ==="
  for rung in "${RUNGS[@]}"; do
    pgn="pgn/slow/${engine}_sf${rung}.pgn"
    [ -s "$pgn" ] && continue
    echo "  $engine vs sf${rung} at $TC"
    cutechess-cli \
      -engine name="$engine" cmd=wrappers/docker_engine.sh arg="$image" arg=--memory=1024m proto=uci tc=$TC \
      -engine name="sf${rung}" cmd=wrappers/docker_engine.sh arg=eval2/stockfish:16.1 proto=uci tc=$TC \
        option.UCI_LimitStrength=true option.UCI_Elo="$rung" option.Threads=1 option.Hash=128 \
      -openings file=fixtures/openings.epd format=epd order=random \
      -games 2 -rounds $((GAMES/2)) -repeat -concurrency 1 \
      -resign movecount=5 score=900 \
      -draw movenumber=40 movecount=6 score=10 \
      -pgnout "$pgn" min \
      > "logs/slow/${engine}_sf${rung}.log" 2>&1 || true
  done

  # Random-mover baseline (the random mover is a tiny SF tweak: UCI_Elo=
  # 800 with skill level=0 isn't truly random; we instead use a Python
  # random-legal engine launched directly. See preflight/random_mover.py
  # for the implementation; for now, use the same SF800 image with skill 0.)
  pgn="pgn/slow/${engine}_vs_random.pgn"
  if [ ! -s "$pgn" ]; then
    echo "  $engine vs random-mover at $TC"
    cutechess-cli \
      -engine name="$engine" cmd=wrappers/docker_engine.sh arg="$image" arg=--memory=1024m proto=uci tc=$TC \
      -engine name="random" cmd=python3 arg=lib/random_mover.py proto=uci tc=$TC \
      -openings file=fixtures/openings.epd format=epd order=random \
      -games 2 -rounds $((GAMES/2)) -repeat -concurrency 1 \
      -resign movecount=5 score=900 \
      -draw movenumber=40 movecount=6 score=10 \
      -pgnout "$pgn" min \
      > "logs/slow/${engine}_vs_random.log" 2>&1 || true
  fi
done

# Tactical suite at higher movetime (60s) for Tier C.
echo "=== Tier C tactical suite at 60s/move ==="
for engine in "${SLOW[@]}"; do
  python3 preflight/tactics.py "$engine" \
    --epd fixtures/mate_in_2.epd --movetime-ms 60000 \
    > "logs/slow/${engine}_tactics.log" 2>&1 || true
done

echo "slow battery done."
