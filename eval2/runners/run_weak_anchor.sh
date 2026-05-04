#!/usr/bin/env bash
# Weak-anchor sweep: add SF Skill 0 to Phase B for the saturated cluster
# + give chess-newlang-codex its missing Phase B coverage.
#
# Phase A bounded SF Skill 0 at <1229 Elo on this hardware; we treat its
# anchor Elo as 900 ± 300 (conservative midpoint) for the inverse-variance
# combination. The saved JSONs and the score_anchor library both pick this
# up via SF_SKILL_ELOS_DEFAULT.
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE"
mkdir -p pgn/anchor logs/anchor

WRAP=wrappers/docker_engine.sh
SF_IMG=eval2/stockfish:18

# Engines that saturated sf_skill5 (need a weaker anchor)
SATURATED=(
  chess-apl-codex54
  chess-icon-codex
  chess-latex-codex-replication
  chess-why3
)
# chess-sql + latex-chess-engine excluded — too slow at TC=120+1 to play
# meaningful games (>30s/move; would dominate wall time without changing
# the qualitative answer "they are sub-1500").

# Engines with no Phase B coverage at all
NEW=(chess-newlang-codex)

# Resolve binary/host config from manifest
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

run_one_pair() {
  local engine=$1 ref=$2 games=$3
  local pgn="pgn/anchor/${engine}_vs_${ref}.pgn"
  local log="logs/anchor/${engine}_vs_${ref}.log"
  if [ -s "$pgn" ]; then
    local done=$(grep -cE '^\[Result "(1-0|0-1|1/2-1/2)"' "$pgn" 2>/dev/null || true)
    if [ "$done" -ge 8 ]; then
      echo "skip $engine vs $ref ($done games already)"; return 0
    fi
  fi
  if ! build_engine_args "$engine"; then echo "skip $engine: no inv"; return 0; fi
  local ENG_ARGS=("${ENGINE_ARGS[@]}")

  local REF_ARGS=()
  case "$ref" in
    rustic)    REF_ARGS=(cmd="$WRAP" arg=eval2/anchor-rustic:latest arg=--cpus=2 arg=--memory=1g proto=uci) ;;
    asymptote) REF_ARGS=(cmd="$WRAP" arg=eval2/anchor-asymptote:latest arg=--cpus=2 arg=--memory=1g proto=uci) ;;
    sf_skill*)
      local skill="${ref#sf_skill}"
      REF_ARGS=(cmd="$WRAP" arg="$SF_IMG" arg=--cpus=2 arg=--memory=1g proto=uci
                "option.Skill Level=$skill" option.Threads=1 option.Hash=128) ;;
    *) echo "unknown ref $ref"; return 1 ;;
  esac

  echo "weak-anchor: $engine vs $ref ($games games at TC=120+1)"
  cutechess-cli \
    -engine name="$engine" "${ENG_ARGS[@]}" \
    -engine name="$ref" "${REF_ARGS[@]}" \
    -each tc=120+1 \
    -openings file=fixtures/openings.epd format=epd order=random \
    -games 2 -rounds $((games/2)) -repeat -concurrency 2 \
    -resign movecount=5 score=900 \
    -draw movenumber=40 movecount=6 score=10 \
    -pgnout "$pgn" min \
    > "$log" 2>&1 || true
}

# Saturated engines: only need sf_skill0 to break out of the floor.
for e in "${SATURATED[@]}"; do
  run_one_pair "$e" sf_skill0 10
done

# chess-newlang-codex: full 6-anchor coverage (5 standard + sf_skill0).
for e in "${NEW[@]}"; do
  for ref in rustic asymptote sf_skill0 sf_skill5 sf_skill10 sf_skill15; do
    run_one_pair "$e" "$ref" 10
  done
done

echo "weak-anchor sweep done. PGNs in pgn/anchor/, logs in logs/anchor/."
