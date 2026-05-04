#!/usr/bin/env bash
# Phase 1: preflight gate. Runs UCI handshake + perft/legal-move audit
# + tactical suite for each engine. Engines that fail UCI or perft are
# marked PREFLIGHT_FAIL and excluded from Phase 3.
#
# Usage:
#   ./runners/run_preflight.sh                     # all engines
#   ./runners/run_preflight.sh chess-rust-cc       # one engine
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE"

ENGINES=("$@")
if [ ${#ENGINES[@]} -eq 0 ]; then
  ARG="--all"
else
  ARG="${ENGINES[*]}"
fi

mkdir -p logs/preflight

echo "=== UCI handshake ==="
python3 preflight/uci_handshake.py $ARG 2>&1 | tee logs/preflight/uci.log

echo "=== Perft + legal-move audit ==="
python3 preflight/perft_audit.py $ARG 2>&1 | tee logs/preflight/perft.log

echo "=== Tactics: WAC-100 ==="
python3 preflight/tactics.py --epd fixtures/wac100.epd --movetime-ms 5000 $ARG \
  2>&1 | tee logs/preflight/wac.log

echo "=== Tactics: mate-in-2 ==="
python3 preflight/tactics.py --epd fixtures/mate_in_2.epd --movetime-ms 5000 $ARG \
  2>&1 | tee logs/preflight/m2.log

echo "preflight done. results under results/per_engine/*.preflight.*.json"
