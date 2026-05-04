#!/usr/bin/env bash
# One-shot focused refinement: chess-ruby-codex vs sf_skill5, 30 more games at TC=120+1.
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE"
WRAP=wrappers/docker_engine.sh
PGN=pgn/anchor/chess-ruby-codex_vs_sf_skill5.pgn
LOG=logs/anchor/chess-ruby-codex_vs_sf_skill5_refine.log
cutechess-cli \
  -engine name="chess-ruby-codex" cmd="$WRAP" arg=eval2/chess-ruby-codex:latest arg=--cpus=2 arg=--memory=1g proto=uci \
  -engine name="sf_skill5" cmd="$WRAP" arg=eval2/stockfish:18 arg=--cpus=2 arg=--memory=1g proto=uci \
    "option.Skill Level=5" option.Threads=1 option.Hash=128 \
  -each tc=120+1 \
  -openings file=fixtures/openings.epd format=epd order=random \
  -games 2 -rounds 15 -repeat -concurrency 2 \
  -resign movecount=5 score=900 \
  -draw movenumber=40 movecount=6 score=10 \
  -pgnout "$PGN" min \
  > "$LOG" 2>&1
