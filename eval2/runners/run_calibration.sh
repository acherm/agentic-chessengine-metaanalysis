#!/usr/bin/env bash
# Phase 2: calibrate the calibrator.
#
# (a) SF-vs-SF self-pairings to confirm rung gaps land near 200 Elo.
# (b) SF-vs-anchor matches to verify the SF UCI_Elo curve agrees with
#     CCRL 40/4 nominals on this hardware.
#
# SF 16.1 UCI_Elo floor is 1320; rungs below that are invalid.
#
# Output PGNs under pgn/calibration/.
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE"
mkdir -p pgn/calibration logs/calibration

GAMES=$(python3 -c 'import json; print(json.load(open("ladder.json"))["phases"]["2_calibration"]["games_per_pairing"])')
TC=$(python3 -c 'import json; print(json.load(open("ladder.json"))["phases"]["2_calibration"]["tc"])')

SF_IMG="eval2/stockfish:16.1"
WRAP="wrappers/docker_engine.sh"

# (a) SF self-pairings — adjacent rungs, ~200 Elo expected gap.
sf_pair() {
  local rA=$1
  local rB=$2
  local tag="sf${rA}_vs_sf${rB}"
  local pgn="pgn/calibration/${tag}.pgn"
  local log="logs/calibration/${tag}.log"
  if [ -s "$pgn" ]; then echo "skip $tag (pgn exists)"; return; fi
  echo "calibration: SF${rA} vs SF${rB} at $TC ($GAMES games)"
  # --cpus=2 --memory=1g overrides wrapper defaults; concurrency=2 uses
  # 4 engines × 2 cores = 8 of 16 cores; no CPU contention (prior run with
  # concurrency=2 × --cpus=1 = 4 cores oversubscribed caused ~150 Elo
  # compression at mid rungs, now resolved by generous per-container caps).
  cutechess-cli \
    -engine name="sf${rA}" cmd="$WRAP" arg="$SF_IMG" arg=--cpus=2 arg=--memory=1g proto=uci \
      option.UCI_LimitStrength=true option.UCI_Elo="$rA" option.Threads=1 option.Hash=128 \
    -engine name="sf${rB}" cmd="$WRAP" arg="$SF_IMG" arg=--cpus=2 arg=--memory=1g proto=uci \
      option.UCI_LimitStrength=true option.UCI_Elo="$rB" option.Threads=1 option.Hash=128 \
    -each tc="$TC" \
    -openings file=fixtures/openings.epd format=epd order=random \
    -games 2 -rounds $((GAMES/2)) -repeat -concurrency 2 \
    -resign movecount=5 score=900 \
    -draw movenumber=40 movecount=6 score=10 \
    -pgnout "$pgn" min \
    > "$log" 2>&1 || true
}

sf_pair 1320 1500
sf_pair 1700 1900
sf_pair 2300 2500

# (b) Anchor-vs-SF matches.
anchor_pair() {
  local anchor_name=$1
  local anchor_image=$2
  local sf_rung=$3
  local tag=$4
  local pgn="pgn/calibration/${tag}.pgn"
  local log="logs/calibration/${tag}.log"
  if [ -s "$pgn" ]; then echo "skip $tag (pgn exists)"; return; fi
  echo "calibration: $anchor_name vs SF${sf_rung} at $TC ($GAMES games)"
  cutechess-cli \
    -engine name="$anchor_name" cmd="$WRAP" arg="$anchor_image" arg=--cpus=2 arg=--memory=1g proto=uci \
    -engine name="sf${sf_rung}" cmd="$WRAP" arg="$SF_IMG" arg=--cpus=2 arg=--memory=1g proto=uci \
      option.UCI_LimitStrength=true option.UCI_Elo="$sf_rung" option.Threads=1 option.Hash=128 \
    -each tc="$TC" \
    -openings file=fixtures/openings.epd format=epd order=random \
    -games 2 -rounds $((GAMES/2)) -repeat -concurrency 2 \
    -resign movecount=5 score=900 \
    -draw movenumber=40 movecount=6 score=10 \
    -pgnout "$pgn" min \
    > "$log" 2>&1 || true
}

anchor_pair rustic      eval2/anchor-rustic:latest      1700 "rustic_vs_sf1700"
anchor_pair countergo40 eval2/anchor-countergo40:latest 2300 "countergo40_vs_sf2300"

echo "calibration done. PGNs in pgn/calibration/, logs in logs/calibration/."
