#!/usr/bin/env bash
# Build all docker images: stockfish + 3 anchors + every engine that has
# a Dockerfile under docker/engines/<name>/.
#
# For each engine, we rsync its source repo (manifest `path:`) into a
# throwaway build context at <tmp>/src/, copy the engine's Dockerfile,
# then `docker build`.
#
# Usage:
#   ./runners/build_images.sh                      # build everything missing
#   ./runners/build_images.sh chess-rust-cc        # one engine
#   ./runners/build_images.sh --rebuild            # force rebuild all
set -euo pipefail

HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE"

REBUILD=0
TARGETS=()
for arg in "$@"; do
  case "$arg" in
    --rebuild) REBUILD=1 ;;
    *) TARGETS+=("$arg") ;;
  esac
done

FAILED=()

build_one_simple() {
  local image=$1 dockerfile=$2 context=$3
  if [ "$REBUILD" -eq 0 ] && docker image inspect "$image" >/dev/null 2>&1; then
    echo "skip $image (exists; pass --rebuild to override)"
    return
  fi
  echo "build $image"
  if ! docker build -t "$image" -f "$dockerfile" "$context"; then
    echo "FAILED $image" >&2
    FAILED+=("$image")
  fi
}

# 1. Stockfish + anchors (no source rsync needed; self-contained Dockerfiles)
build_one_simple eval2/stockfish:16.1            docker/stockfish/Dockerfile        docker/stockfish/
build_one_simple eval2/anchor-tscp181:latest     docker/anchors/tscp/Dockerfile     docker/anchors/tscp/
build_one_simple eval2/anchor-madchess32:latest  docker/anchors/madchess/Dockerfile docker/anchors/madchess/
build_one_simple eval2/anchor-countergo40:latest docker/anchors/countergo/Dockerfile docker/anchors/countergo/

# 2. Engine images: enumerate via manifest.yaml using the lib parser.
# (Avoid `mapfile` because macOS ships bash 3.2 which lacks it.)
ENGINE_TSV=$(mktemp)
trap 'rm -f "$ENGINE_TSV"' EXIT
python3 - >"$ENGINE_TSV" <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, str(Path("lib")))
import manifest
engs, _ = manifest.load()
for e in engs:
    df = Path("docker/engines") / e.name / "Dockerfile"
    print(f"{e.name}\t{e.path}\t{e.image}\t{df}\t{1 if df.exists() else 0}")
PY

missing_dockerfile=()
while IFS= read -r line; do
  [ -z "$line" ] && continue
  IFS=$'\t' read -r name src image dfile has <<<"$line"
  if [ ${#TARGETS[@]} -gt 0 ]; then
    skip=1
    for t in "${TARGETS[@]}"; do [ "$t" = "$name" ] && skip=0; done
    [ $skip -eq 1 ] && continue
  fi
  if [ "$has" -eq 0 ]; then
    missing_dockerfile+=("$name")
    continue
  fi
  if [ "$REBUILD" -eq 0 ] && docker image inspect "$image" >/dev/null 2>&1; then
    echo "skip $image (exists)"
    continue
  fi
  if [ ! -d "$src" ]; then
    echo "WARN $name: source path $src does not exist on host; skipping" >&2
    continue
  fi
  tmp=$(mktemp -d)
  trap 'rm -rf "$tmp"' EXIT
  # Exclude common build artefacts so host-built (often Mac) binaries
  # don't leak into the Linux container and confuse `make`/strip.
  rsync -a --exclude='.git' --exclude='target' --exclude='build' \
        --exclude='node_modules' --exclude='__pycache__' \
        --exclude='_build' --exclude='.lake' \
        --exclude='*.dSYM' --exclude='*.dylib' --exclude='*.so' \
        --exclude='*.o' --exclude='*.a' --exclude='*.exe' \
        --exclude='*.pgn' --exclude='*.pdf' \
        "$src"/ "$tmp/src/"
  cp "$dfile" "$tmp/Dockerfile"
  echo "build $image  (src=$src)"
  if ! docker build -t "$image" "$tmp"; then
    echo "FAILED $image" >&2
    FAILED+=("$image")
  fi
  rm -rf "$tmp"
done < "$ENGINE_TSV"

if [ ${#FAILED[@]} -gt 0 ]; then
  printf '%s\n' "${FAILED[@]}" > results/build_failures.txt
  echo
  echo "Build failures: ${#FAILED[@]} (see results/build_failures.txt)"
fi

if [ ${#missing_dockerfile[@]} -gt 0 ]; then
  echo
  echo "Missing Dockerfile (skipped):"
  for n in "${missing_dockerfile[@]}"; do echo "  - $n"; done
  printf '%s\n' "${missing_dockerfile[@]}" > results/missing_dockerfiles.txt
fi
echo "build_images.sh done."
