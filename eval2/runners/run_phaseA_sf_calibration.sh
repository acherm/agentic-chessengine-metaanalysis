#!/usr/bin/env bash
# Phase A — empirically calibrate SF 18 Skill Levels against the
# external anchors (Rustic Alpha 3.0.4 @ 1820, Asymptote 0.7 @ 2150).
#
# Output: pgn/phaseA/sf_skill_<N>_vs_<anchor>.pgn for N in {0,5,10,15}.
# Post-scoring derives effective Elo for each SF Skill config on our
# hardware; those numbers become the "SF-Skill-N" references for Phase B.
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE"
mkdir -p pgn/phaseA logs/phaseA

SF_IMG=eval2/stockfish:18
WRAP=wrappers/docker_engine.sh
GAMES=30
TC=120+1

# Anchor definitions
declare -a ANCHORS
ANCHORS=(
  "rustic    eval2/anchor-rustic:latest    1820"
  "asymptote eval2/anchor-asymptote:latest 2150"
)
SKILLS=(0 5 10 15)

for skill in "${SKILLS[@]}"; do
  for anc in "${ANCHORS[@]}"; do
    read -r anc_name anc_image anc_ccrl <<<"$anc"
    pgn="pgn/phaseA/sf_skill${skill}_vs_${anc_name}.pgn"
    log="logs/phaseA/sf_skill${skill}_vs_${anc_name}.log"
    if [ -s "$pgn" ]; then
      done=$(grep -cE '^\[Result "(1-0|0-1|1/2-1/2)"' "$pgn")
      [ "$done" -ge "$GAMES" ] && { echo "skip SF-Skill-$skill vs $anc_name ($done games)"; continue; }
    fi
    echo "phaseA: SF-Skill-$skill vs $anc_name (CCRL $anc_ccrl) at $TC ($GAMES games)"
    cutechess-cli \
      -engine name="sf_skill${skill}" cmd="$WRAP" arg="$SF_IMG" arg=--cpus=2 arg=--memory=1g proto=uci \
        option."Skill Level"="$skill" option.Threads=1 option.Hash=128 \
      -engine name="$anc_name" cmd="$WRAP" arg="$anc_image" arg=--cpus=2 arg=--memory=1g proto=uci \
      -each tc="$TC" \
      -openings file=fixtures/openings.epd format=epd order=random \
      -games 2 -rounds $((GAMES/2)) -repeat -concurrency 2 \
      -resign movecount=5 score=900 \
      -draw movenumber=40 movecount=6 score=10 \
      -pgnout "$pgn" min \
      > "$log" 2>&1 || true
  done
done
echo "Phase A done. Score with: python3 lib/score_phaseA.py"
