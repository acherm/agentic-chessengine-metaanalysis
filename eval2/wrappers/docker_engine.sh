#!/usr/bin/env bash
# Generic Docker-engine wrapper for cutechess-cli.
#
# cutechess-cli's `cmd=` field is a literal binary path, not shell-parsed,
# so we can't pass `cmd="docker run --rm ... image"` directly. Instead
# the runner scripts call:
#
#   cutechess-cli -engine cmd=wrappers/docker_engine.sh \
#                         arg=<image> \
#                         arg=[--cpus=N] arg=[--memory=Xm] \
#                         proto=uci ...
#
# We invoke `docker run` with sane defaults plus whatever extra args
# come after the image. Container is killed on stdin close because of
# `--init` (PID 1 reaps zombies / propagates SIGTERM).
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "usage: $0 <image> [extra docker run args...]" >&2
  exit 64
fi

IMAGE=$1
shift

# Match the defaults baked into lib/docker_engine.py. Tier C (LaTeX/SQL/BF)
# can override --memory/--cpus by passing extra args after the image.
exec docker run --rm -i --init --network=none \
     --cpus=1 --memory=512m --pids-limit=256 \
     "$@" "$IMAGE"
