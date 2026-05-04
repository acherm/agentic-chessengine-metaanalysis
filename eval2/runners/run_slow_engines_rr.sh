#!/usr/bin/env bash
# Slow-engine round-robin: 3 engines previously excluded from the
# n=26 RR (chess-brainfuck, chess-sql, latex-chess-engine) plus
# cross-validation against four already-measured opponents that
# bracket their expected Elo range.
#
# Smoke test showed all 3 engines are depth-capped (not time-capped)
# and return moves in <3s at TC=120+1. The original "10-15h, exceeds
# time budget" estimate was wrong.
#
# chess-brainfuck-cc is excluded (manifest skipped:true; bf_uci.py is
# a BF emitter, not a UCI driver — Docker image doesn't respond to UCI).
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE"
mkdir -p pgn/rr logs/rr pgn/anchor logs/anchor

WRAP=wrappers/docker_engine.sh

SLOW=(chess-brainfuck chess-sql latex-chess-engine)
# Cross-validation opponents: bottom 4 of the n=26 RR in known order.
OPPS=(chess-apl-codex54 chess-icon-codex chess-Rocq sf_skill0)

build_engine_args() {
  local name=$1
  ENGINE_ARGS=()
  local block
  block=$(python3 - <<PY
import sys, shlex
sys.path.insert(0, "lib")
import manifest
m = manifest.by_name(manifest.load()[0])
e = m.get("$name")
if not e: sys.exit(1)
if e.host_cmd:
    inner = f"cd {shlex.quote(e.host_cwd)} && exec {e.host_cmd}"
    print("HOST", inner)
else:
    print("DOCKER", e.image)
PY
  ) || return 1
  read -r kind rest <<<"$block"
  if [ "$kind" = "HOST" ]; then
    ENGINE_ARGS=(cmd=bash arg=-c "arg=$rest" proto=uci)
  else
    ENGINE_ARGS=(cmd="$WRAP" arg="$rest" arg=--cpus=2 arg=--memory=1g proto=uci)
  fi
  return 0
}

run_pair() {
  local A=$1 B=$2 dir=$3 games=$4
  local pgn="pgn/${dir}/${A}_vs_${B}.pgn"
  local log="logs/${dir}/${A}_vs_${B}.log"
  if [ -s "$pgn" ]; then
    local done=$(grep -cE '^\[Result "(1-0|0-1|1/2-1/2)"' "$pgn" 2>/dev/null || true)
    if [ "$done" -ge "$((games - 2))" ]; then
      echo "skip $A vs $B ($done games)"; return 0
    fi
  fi

  if ! build_engine_args "$A"; then echo "skip: no inv for $A"; return 0; fi
  local A_ARGS=("${ENGINE_ARGS[@]}")

  local B_ARGS=()
  case "$B" in
    sf_skill0)
      B_ARGS=(cmd="$WRAP" arg=eval2/stockfish:18 arg=--cpus=2 arg=--memory=1g proto=uci
              "option.Skill Level=0" option.Threads=1 option.Hash=128) ;;
    *)
      if ! build_engine_args "$B"; then echo "skip: no inv for $B"; return 0; fi
      B_ARGS=("${ENGINE_ARGS[@]}") ;;
  esac

  echo "[$(date +%H:%M:%S)] $A vs $B ($games games TC=120+1)"
  cutechess-cli \
    -engine name="$A" "${A_ARGS[@]}" \
    -engine name="$B" "${B_ARGS[@]}" \
    -each tc=120+1 \
    -openings file=fixtures/openings.epd format=epd order=random \
    -games 2 -rounds $((games / 2)) -repeat -concurrency 2 \
    -resign movecount=5 score=900 \
    -draw movenumber=40 movecount=6 score=10 \
    -pgnout "$pgn" min \
    > "$log" 2>&1 || true
}

# Inter-slow-engine RR (3 pairs)
for ((i = 0; i < ${#SLOW[@]}; i++)); do
  for ((j = i + 1; j < ${#SLOW[@]}; j++)); do
    run_pair "${SLOW[i]}" "${SLOW[j]}" rr 6
  done
done

# Slow engines vs cross-validation opponents
for s in "${SLOW[@]}"; do
  for o in "${OPPS[@]}"; do
    case "$o" in
      sf_skill0) run_pair "$s" "$o" anchor 10 ;;
      *)         run_pair "$s" "$o" rr 6 ;;
    esac
  done
done

echo "slow-engine RR done."
