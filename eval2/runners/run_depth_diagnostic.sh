#!/usr/bin/env bash
# Q3 — depth-utilization diagnostic.
#
# For each strong corpus engine, play 6 games vs Rustic Alpha 3.0.4 at
# 120+1 with FULL PGN annotations (default cutechess format, NOT `min`).
# Cutechess writes `move {eval/depth time}` per move, which lets us
# answer "is the engine depth-limited (search bottleneck) or
# eval-limited (more time doesn't help)?"
#
# concurrency=1 to minimize contention with a co-running Phase B.
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE"
mkdir -p pgn/depth_diag logs/depth_diag

WRAP=wrappers/docker_engine.sh

# Strong-tier engines (claimed >= 1700 in any source) we want to profile.
ENGINES=(
  chess-rust-cc
  chess-rust-cc-redo
  chess-cplusplus-claude
  cplusplus-chess
  chess-java-cc
  chess-rust-codex
  chess-purec
  chess-py
)

# Reference: Rustic 1820 — the most "real" anchor at corpus mid-strength.
REF_ARGS=(cmd="$WRAP" arg=eval2/anchor-rustic:latest arg=--cpus=2 arg=--memory=1g proto=uci)

for engine in "${ENGINES[@]}"; do
  pgn="pgn/depth_diag/${engine}_vs_rustic.pgn"
  log="logs/depth_diag/${engine}_vs_rustic.log"
  if [ -s "$pgn" ]; then
    done=$(grep -cE '^\[Result "(1-0|0-1|1/2-1/2)"' "$pgn")
    [ "$done" -ge 6 ] && { echo "skip $engine ($done games)"; continue; }
  fi
  ENGINE_ARGS=(cmd="$WRAP" arg="eval2/${engine}:latest" arg=--cpus=2 arg=--memory=1g proto=uci)
  echo "depth_diag: $engine vs rustic at 120+1, 6 games"
  cutechess-cli \
    -engine name="$engine" "${ENGINE_ARGS[@]}" \
    -engine name="rustic" "${REF_ARGS[@]}" \
    -each tc=120+1 \
    -openings file=fixtures/openings.epd format=epd order=random \
    -games 2 -rounds 3 -repeat -concurrency 1 \
    -resign movecount=5 score=900 \
    -draw movenumber=40 movecount=6 score=10 \
    -pgnout "$pgn" \
    > "$log" 2>&1 || true
done
echo "depth_diag done. Score with: python3 lib/score_depth_diag.py"
