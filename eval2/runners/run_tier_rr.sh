#!/usr/bin/env bash
# Phase 4: round-robin within each tier (A, B, C). Avoids the global
# N²; we only RR engines that landed in similar Pass-2 brackets.
#
# Usage:
#   ./runners/run_tier_rr.sh A     # only Tier A
#   ./runners/run_tier_rr.sh       # all tiers
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE"
mkdir -p pgn/rr logs/rr

TIERS=("$@")
[ ${#TIERS[@]} -eq 0 ] && TIERS=(A B C)

read TC GAMES CONC <<<"$(python3 -c 'import json
d=json.load(open("ladder.json"))["phases"]["4_tier_rr"]
print(d["tc"], d["games_per_pairing"], d["concurrency"])')"

for tier in "${TIERS[@]}"; do
  mapfile -t names < <(python3 - <<PY
import sys; sys.path.insert(0,"lib")
import manifest
engs, _ = manifest.load()
for e in engs:
    if e.tier == "$tier" and e.corpus == "main":
        print(e.name)
PY
)
  echo "=== Tier $tier RR (${#names[@]} engines) ==="
  for A in "${names[@]}"; do
    for B in "${names[@]}"; do
      [ "$A" = "$B" ] && continue
      pgn="pgn/rr/tier${tier}_${A}_vs_${B}.pgn"
      log="logs/rr/tier${tier}_${A}_vs_${B}.log"
      [ -s "$pgn" ] && { echo "skip $A vs $B"; continue; }
      img_pair=$(python3 -c "
import sys; sys.path.insert(0,'lib')
import manifest
m = manifest.by_name(manifest.load()[0])
print(m['$A'].image, m['$B'].image)")
      read imgA imgB <<<"$img_pair"
      echo "  rr: $A vs $B at $TC"
      cutechess-cli \
        -engine name="$A" cmd=wrappers/docker_engine.sh arg="$imgA" proto=uci \
        -engine name="$B" cmd=wrappers/docker_engine.sh arg="$imgB" proto=uci \
        -each tc="$TC" \
        -openings file=fixtures/openings.epd format=epd order=random \
        -games 2 -rounds $((GAMES/2)) -repeat -concurrency "$CONC" \
        -resign movecount=5 score=900 \
        -draw movenumber=40 movecount=6 score=10 \
        -pgnout "$pgn" min \
        > "$log" 2>&1 || true
    done
  done
done
echo "tier rr done."
