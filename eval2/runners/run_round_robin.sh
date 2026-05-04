#!/usr/bin/env bash
# Round-robin tournament across all UCI-capable corpus engines.
# See §16 of reports/EVAL2_FINDINGS.md for design rationale.
#
# - 23 engines, n*(n-1)/2 = 253 pairs.
# - 2 games per pair (1 white + 1 black via -repeat) for the pilot run;
#   re-running the script later with GAMES_PER_PAIR=4 (or higher) appends
#   another 2 games to each pair (since cutechess writes PGN incrementally
#   and we count games via grep before the SPRT-style cap).
# - TC = 120+1 (same as Phase B; required for direct anchor-Elo comparison).
# - Concurrency 2, --cpus=2 --memory=1g per docker engine (same as Phase B).
# - Resumable: skip a pair whose PGN already has >= GAMES_PER_PAIR results.
#
# Usage:
#   ./runners/run_round_robin.sh               # default: 2 games/pair
#   GAMES_PER_PAIR=4 ./runners/run_round_robin.sh  # extend / fresh run with 4
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE"
mkdir -p pgn/rr logs/rr

GAMES_PER_PAIR=${GAMES_PER_PAIR:-2}
TC=${TC:-120+1}
CONC=${CONC:-2}
WRAP=wrappers/docker_engine.sh

# Engine list per §16 (26 entries, ordered by Phase B band).
# v2 adds the three port/dsl engines that were missing in v1:
#   chess-revisit-java-toRust-codex  (Java → Rust port via Codex)
#   chess-revisit-java-toCOBOL-codex (Java → COBOL port via Codex)
#   chess-newlang-codex              (Codex-built mini DSL engine)
ENGINES=(
  chess-java-cc chess-rust-cc-redo chess-rust-codex chess-rust-cc
  cplusplus-chess chess-cplusplus-claude chess-why3-cc chess-ruby-cc
  chess-java chess-py chess-py-cc
  chess-purec chess-purec-codex chess-assembly-codex chess-Rocq chess-ruby-codex
  chess-icon-codex chess-why3 lean-chess COBOL-chess chess-cobol-cc
  chess-apl-codex54 chess-latex-codex-replication
  chess-revisit-java-toRust-codex chess-revisit-java-toCOBOL-codex chess-newlang-codex
)

# Build cutechess engine block from manifest (DOCKER or HOST)
build_engine_args() {
  local name=$1 # populates ENGINE_ARGS
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

n_pairs=$(( ${#ENGINES[@]} * (${#ENGINES[@]} - 1) / 2 ))
echo "Round-robin: ${#ENGINES[@]} engines, $n_pairs pairs, $GAMES_PER_PAIR games/pair = $((n_pairs * GAMES_PER_PAIR)) games at $TC"

ix=0
for ((i = 0; i < ${#ENGINES[@]}; i++)); do
  for ((j = i + 1; j < ${#ENGINES[@]}; j++)); do
    A=${ENGINES[i]}; B=${ENGINES[j]}
    ix=$((ix + 1))
    pgn="pgn/rr/${A}_vs_${B}.pgn"
    log="logs/rr/${A}_vs_${B}.log"
    if [ -s "$pgn" ]; then
      done=$(grep -cE '^\[Result "(1-0|0-1|1/2-1/2)"' "$pgn" 2>/dev/null || true)
      if [ "$done" -ge "$GAMES_PER_PAIR" ]; then
        echo "[$ix/$n_pairs] skip $A vs $B ($done games)"; continue
      fi
    fi
    if ! build_engine_args "$A"; then echo "skip: no inv for $A"; continue; fi
    A_ARGS=("${ENGINE_ARGS[@]}")
    if ! build_engine_args "$B"; then echo "skip: no inv for $B"; continue; fi
    B_ARGS=("${ENGINE_ARGS[@]}")

    echo "[$ix/$n_pairs] rr: $A vs $B at $TC ($GAMES_PER_PAIR games)"
    cutechess-cli \
      -engine name="$A" "${A_ARGS[@]}" \
      -engine name="$B" "${B_ARGS[@]}" \
      -each tc="$TC" \
      -openings file=fixtures/openings.epd format=epd order=random \
      -games 2 -rounds $((GAMES_PER_PAIR / 2)) -repeat \
      -concurrency "$CONC" \
      -resign movecount=5 score=900 \
      -draw movenumber=40 movecount=6 score=10 \
      -pgnout "$pgn" min \
      > "$log" 2>&1 || true
  done
done
echo "round-robin done. PGNs in pgn/rr/, logs in logs/rr/."
