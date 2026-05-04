#!/usr/bin/env bash
# Phase B — the canonical Elo gauntlet.
#
# Every main-corpus engine plays SPRT-capped 120+1 matches against each
# reference. References are:
#   rustic     (CCRL 40/4 = 1820, external)
#   asymptote  (CCRL 40/4 = 2150, external)
#   sf_skill5  (effective Elo 1658 ± 126 from Phase A)
#   sf_skill10 (effective Elo 2004 ± 112 from Phase A)
#   sf_skill15 (effective Elo 2325 ± 124 from Phase A)
#
# SF is configured with `Skill Level` only — NOT UCI_LimitStrength,
# which Phase 2 showed is compressed 200-450 Elo on our hardware. Each
# Skill level's effective CCRL-scale Elo was measured in Phase A.
#
# Usage:
#   ./runners/run_anchor_gauntlet.sh                          # all in-scope engines
#   ./runners/run_anchor_gauntlet.sh chess-rust-cc            # one engine
#   ./runners/run_anchor_gauntlet.sh --host chess-purec-codex # host-native
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE"
mkdir -p pgn/anchor logs/anchor

MODE=docker
TARGETS=()
for a in "$@"; do
  case "$a" in
    --host) MODE=host ;;
    *) TARGETS+=("$a") ;;
  esac
done

WRAP=wrappers/docker_engine.sh
SF_IMG=eval2/stockfish:18

REFERENCES=(rustic asymptote sf_skill5 sf_skill10 sf_skill15)

SPRT_ELO0=-50
SPRT_ELO1=+50
SPRT_ALPHA=0.05
SPRT_BETA=0.05
GAMES_MAX=30
CONCURRENCY=2
TC=120+1

if [ ${#TARGETS[@]} -eq 0 ]; then
  while IFS= read -r e; do TARGETS+=("$e"); done < <(python3 - <<'PY'
import sys
sys.path.insert(0, "lib")
import manifest
engs, _ = manifest.load()
for e in engs:
    if e.corpus == "main": print(e.name)
PY
)
fi

# Build the engine -engine block as a bash ARRAY (so quoting survives).
build_engine_args() {
  # populates global ENGINE_ARGS from manifest entry $1, mode $MODE
  local name=$1
  ENGINE_ARGS=()
  local manifest_line
  manifest_line=$(python3 - <<PY
import sys, shlex
sys.path.insert(0, "lib")
import manifest
e = manifest.by_name(manifest.load()[0]).get("$name")
if not e:
    sys.exit(1)
if "$MODE" == "host":
    if not e.host_cmd: sys.exit(2)
    inner = f"cd {shlex.quote(e.host_cwd)} && exec {e.host_cmd}"
    print("HOST", inner)
else:
    print("DOCKER", e.image)
PY
  ) || return 1
  read -r kind rest <<<"$manifest_line"
  if [ "$kind" = "HOST" ]; then
    ENGINE_ARGS=(cmd=bash arg=-c "arg=$rest" proto=uci)
  else
    ENGINE_ARGS=(cmd="$WRAP" arg="$rest" arg=--cpus=2 arg=--memory=1g proto=uci)
  fi
  return 0
}

# Build the reference -engine block as a bash ARRAY for the given ref name.
build_ref_args() {
  local ref=$1
  REF_ARGS=()
  case "$ref" in
    rustic)
      REF_ARGS=(cmd="$WRAP" arg=eval2/anchor-rustic:latest arg=--cpus=2 arg=--memory=1g proto=uci)
      ;;
    asymptote)
      REF_ARGS=(cmd="$WRAP" arg=eval2/anchor-asymptote:latest arg=--cpus=2 arg=--memory=1g proto=uci)
      ;;
    sf_skill*)
      local skill="${ref#sf_skill}"
      # The "Skill Level" UCI option name has a space; pass as one token.
      REF_ARGS=(cmd="$WRAP" arg="$SF_IMG" arg=--cpus=2 arg=--memory=1g proto=uci
                "option.Skill Level=$skill" option.Threads=1 option.Hash=128)
      ;;
    *) echo "unknown ref $ref" >&2; return 1 ;;
  esac
  return 0
}

for engine in "${TARGETS[@]}"; do
  if ! build_engine_args "$engine"; then
    echo "SKIP $engine: no invocation available"; continue
  fi
  for ref in "${REFERENCES[@]}"; do
    pgn="pgn/anchor/${engine}_vs_${ref}.pgn"
    log="logs/anchor/${engine}_vs_${ref}.log"
    if [ -s "$pgn" ]; then
      done=$(grep -cE '^\[Result "(1-0|0-1|1/2-1/2)"' "$pgn" 2>/dev/null)
      if [ "$done" -ge 8 ]; then
        echo "skip $engine vs $ref ($done games)"
        continue
      fi
    fi
    build_ref_args "$ref"
    echo "gauntlet: $engine vs $ref at $TC"
    cutechess-cli \
      -engine name="$engine" "${ENGINE_ARGS[@]}" \
      -engine name="$ref" "${REF_ARGS[@]}" \
      -each tc="$TC" \
      -openings file=fixtures/openings.epd format=epd order=random \
      -games 2 -rounds $((GAMES_MAX/2)) -repeat -concurrency "$CONCURRENCY" \
      -sprt elo0=$SPRT_ELO0 elo1=$SPRT_ELO1 alpha=$SPRT_ALPHA beta=$SPRT_BETA \
      -resign movecount=5 score=900 \
      -draw movenumber=40 movecount=6 score=10 \
      -pgnout "$pgn" min \
      > "$log" 2>&1 || true
  done
done
echo "anchor gauntlet done. PGNs in pgn/anchor/, logs in logs/anchor/."
