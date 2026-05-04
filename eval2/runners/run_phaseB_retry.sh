#!/usr/bin/env bash
# Full Phase B (5-anchor SPRT-capped gauntlet at TC=120+1) for the
# post-retry chess-purec binary. Direct invocation to bypass the
# manifest registration step. Use this for one-off certification of
# experimental engine builds.
#
# Usage:
#   ./runners/run_phaseB_retry.sh <engine_binary_path> [<engine_label>]
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE"

BIN=${1:?"engine binary path required"}
LABEL=${2:-chess-purec-retry}

mkdir -p "pgn/anchor.${LABEL}" "logs/anchor.${LABEL}"

WRAP=wrappers/docker_engine.sh
SF_IMG=eval2/stockfish:18

REFERENCES=(rustic asymptote sf_skill5 sf_skill10 sf_skill15)

ENG_ARGS=(cmd="$BIN" proto=uci)

build_ref_args() {
  local ref=$1
  REF_ARGS=()
  case "$ref" in
    rustic)    REF_ARGS=(cmd="$WRAP" arg=eval2/anchor-rustic:latest arg=--cpus=2 arg=--memory=1g proto=uci) ;;
    asymptote) REF_ARGS=(cmd="$WRAP" arg=eval2/anchor-asymptote:latest arg=--cpus=2 arg=--memory=1g proto=uci) ;;
    sf_skill*)
      local skill="${ref#sf_skill}"
      REF_ARGS=(cmd="$WRAP" arg="$SF_IMG" arg=--cpus=2 arg=--memory=1g proto=uci
                "option.Skill Level=$skill" option.Threads=1 option.Hash=128) ;;
  esac
}

for ref in "${REFERENCES[@]}"; do
  pgn="pgn/anchor.${LABEL}/${LABEL}_vs_${ref}.pgn"
  log="logs/anchor.${LABEL}/${LABEL}_vs_${ref}.log"
  if [ -s "$pgn" ]; then
    done=$(grep -cE '^\[Result "(1-0|0-1|1/2-1/2)"' "$pgn" 2>/dev/null || true)
    if [ "$done" -ge 8 ]; then echo "skip $ref ($done games)"; continue; fi
  fi
  build_ref_args "$ref"
  echo "[$(date +%H:%M:%S)] $LABEL vs $ref at TC=120+1"
  cutechess-cli \
    -engine name="$LABEL" "${ENG_ARGS[@]}" \
    -engine name="$ref" "${REF_ARGS[@]}" \
    -each tc=120+1 \
    -openings file=fixtures/openings.epd format=epd order=random \
    -games 2 -rounds 15 -repeat -concurrency 2 \
    -sprt elo0=-50 elo1=+50 alpha=0.05 beta=0.05 \
    -resign movecount=5 score=900 \
    -draw movenumber=40 movecount=6 score=10 \
    -pgnout "$pgn" min \
    > "$log" 2>&1 || true
done
echo "post-retry Phase B complete. Output dir: pgn/anchor.${LABEL}/"
