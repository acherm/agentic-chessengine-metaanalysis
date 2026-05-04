#!/usr/bin/env bash
# Wrap a Python UCI bridge so stdin is read line-by-line without
# Python's TextIOWrapper buffer holding lines back. Some engines
# in this corpus (e.g. chess-assembly-codex) have UCI bridges that
# use `for line in sys.stdin:` — under cutechess-cli's pipe stdin
# the buffer can hold the second `go` for >10s, triggering a
# spurious time-loss / disconnect.
#
# Usage:
#   uci_unbuffered.sh <cwd> <python-bridge-script> [bridge-args...]
#
# We read stdin one line at a time in bash and pipe it into a
# Python process spawned with stdbuf -oL -eL and -u.
set -e
CWD=$1; shift
SCRIPT=$1; shift
cd "$CWD"
exec stdbuf -oL -eL python3 -u "$SCRIPT" "$@" < <(while IFS= read -r line; do printf '%s\n' "$line"; done)
