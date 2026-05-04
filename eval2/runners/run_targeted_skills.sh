#!/usr/bin/env bash
# Targeted SF Skill-anchor matches: per-engine, run ~20-game matches
# at TC=120+1 against the SF Skill level whose calibrated Elo is
# closest to the engine's current BT MLE estimate.
#
# Goal: tighten per-engine BT CIs by adding new anchor edges where the
# engine scores 30-70% (the highest-information region).
#
# Engines marked "saturated" / "weak" get 2 anchors each; engines with
# already-measurable BT signal get 1. Selection from BT MLE output of
# 2026-05-02; see `eval2/lib/score_combined_bt.py`.
#
# After this runs, re-execute `python3 lib/score_combined_bt.py` to
# refit and write the updated combined Elo card.
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE"
mkdir -p pgn/anchor logs/anchor

WRAP=wrappers/docker_engine.sh
SF_IMG=eval2/stockfish:18

# Per-engine target Skill level(s). Format: "engine target_skill_csv"
PAIRS=(
  # === Measurable engines (1 new anchor each) ===
  "chess-java-cc 11"
  "chess-revisit-java-toRust-codex 9"
  "chess-rust-cc-redo 9"
  "chess-rust-cc 8"
  "chess-rust-codex 7"
  "chess-ruby-cc 7"
  "chess-cplusplus-claude 7"
  "chess-py 6"
  "cplusplus-chess 6"
  "chess-why3-cc 6"
  "chess-newlang-codex 6"
  "chess-py-cc 4"
  "chess-java 4"
  "chess-revisit-java-toCOBOL-codex 4"
  # === Saturated / weak engines (2 new anchors each) ===
  "chess-purec 4,6"
  "chess-assembly-codex 3,4"
  "chess-purec-codex 3,4"
  "chess-ruby-codex 3,4"
  "COBOL-chess 3,4"
  "chess-cobol-cc 3,4"
  "chess-Rocq 2,3"
  "lean-chess 2,3"
  "chess-brainfuck 2,3"
  "chess-why3 2,3"
  "chess-icon-codex 1,2"
)
GAMES_PER_PAIR=20

# Engine launcher (Docker or host)
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
  local engine=$1 skill=$2
  local pgn="pgn/anchor/${engine}_vs_sf_skill${skill}.pgn"
  local log="logs/anchor/${engine}_vs_sf_skill${skill}.log"
  if [ -s "$pgn" ]; then
    local done=$(grep -cE '^\[Result "(1-0|0-1|1/2-1/2)"' "$pgn" 2>/dev/null || true)
    if [ "$done" -ge "$((GAMES_PER_PAIR - 2))" ]; then
      echo "skip $engine vs sf_skill${skill} ($done games)"; return 0
    fi
  fi
  if ! build_engine_args "$engine"; then echo "skip $engine: no inv"; return 0; fi
  local ENG_ARGS=("${ENGINE_ARGS[@]}")
  echo "[$(date +%H:%M:%S)] $engine vs sf_skill${skill} ($GAMES_PER_PAIR games TC=120+1)"
  cutechess-cli \
    -engine name="$engine" "${ENG_ARGS[@]}" \
    -engine name="sf_skill${skill}" cmd="$WRAP" arg="$SF_IMG" arg=--cpus=2 arg=--memory=1g proto=uci \
      "option.Skill Level=${skill}" option.Threads=1 option.Hash=128 \
    -each tc=120+1 \
    -openings file=fixtures/openings.epd format=epd order=random \
    -games 2 -rounds $((GAMES_PER_PAIR / 2)) -repeat -concurrency 2 \
    -resign movecount=5 score=900 \
    -draw movenumber=40 movecount=6 score=10 \
    -pgnout "$pgn" min \
    > "$log" 2>&1 || true
}

n_pairs=0
for spec in "${PAIRS[@]}"; do
  read -r eng skills <<<"$spec"
  IFS=',' read -ra arr <<<"$skills"
  for s in "${arr[@]}"; do n_pairs=$((n_pairs + 1)); done
done
echo "Total new pairs queued: $n_pairs (~$((n_pairs * GAMES_PER_PAIR)) games)"
echo

idx=0
for spec in "${PAIRS[@]}"; do
  read -r eng skills <<<"$spec"
  IFS=',' read -ra arr <<<"$skills"
  for s in "${arr[@]}"; do
    idx=$((idx + 1))
    echo "[$idx/$n_pairs]"
    run_pair "$eng" "$s"
  done
done

echo "targeted-skill run done. Refit BT MLE: python3 lib/score_combined_bt.py"
