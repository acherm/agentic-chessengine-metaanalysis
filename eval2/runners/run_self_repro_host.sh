#!/usr/bin/env bash
# Q2 self-reproduction sweep — host-native (no Docker).
#
# For every engine listed in runners/self_reproduction.yaml that has a
# binary path and is not flagged skip/already_done, we run cutechess
# directly on host hardware vs host Stockfish 18, using the engine's
# original TC + hash + opponent grid. The resulting per-engine "self-
# Elo" estimate goes alongside the anchor-based Elo for the paper.
#
# Usage:
#   ./runners/run_self_repro_host.sh                 # all configured engines
#   ./runners/run_self_repro_host.sh chess-purec-codex chess-cplusplus-claude
#
# Output:
#   pgn/self_repro/<engine>_vs_<opp>.pgn
#   logs/self_repro/<engine>_vs_<opp>.log
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE"
mkdir -p pgn/self_repro logs/self_repro

SF_BIN=$(command -v stockfish || true)
if [ -z "$SF_BIN" ]; then
  echo "ERROR: host stockfish not found. Install via 'brew install stockfish'." >&2
  exit 1
fi
echo "host stockfish: $SF_BIN"

# Read YAML and emit per-rung match plans (engine name args optional)
python3 - "$@" <<'PY' > /tmp/self_repro_plan.tsv
import re, sys
from pathlib import Path

targets = set(sys.argv[1:])

# Manifest of engine repo roots (mirror of eval2/manifest.yaml host_cwd)
REPO_ROOTS = {
    "chess-purec":              "/Users/mathieuacher/SANDBOX/chess-purec",
    "chess-purec-codex":        "/Users/mathieuacher/SANDBOX/chess-purec-codex",
    "chess-rust-cc":            "/Users/mathieuacher/SANDBOX/chess-rust-cc",
    "chess-rust-cc-redo":       "/Users/mathieuacher/SANDBOX/chess-rust-cc-redo",
    "chess-rust-codex":         "/Users/mathieuacher/SANDBOX/chess-rust-codex",
    "chess-cplusplus-claude":   "/Users/mathieuacher/SANDBOX/chess-cplusplus-claude",
    "cplusplus-chess":          "/Users/mathieuacher/SANDBOX/cplusplus-chess",
    "chess-java":               "/Users/mathieuacher/SANDBOX/chess-java",
    "chess-java-cc":            "/Users/mathieuacher/SANDBOX/chess-java-cc",
    "chess-ruby-cc":            "/Users/mathieuacher/SANDBOX/chess-ruby-cc",
    "chess-why3-cc":            "/Users/mathieuacher/SANDBOX/chess-why3-cc",
    "chess-Rocq":               "/Users/mathieuacher/SANDBOX/chess-Rocq",
    "chess-assembly-codex":     "/Users/mathieuacher/SANDBOX/chess-assembly-codex",
}

# Parse the YAML by hand — keep this self-contained.
yaml_path = Path("runners/self_reproduction.yaml")
engines = {}; cur = None
for raw in yaml_path.read_text().splitlines():
    line = raw.split("#", 1)[0].rstrip()
    if not line.strip(): continue
    m = re.match(r"^  (\S+):\s*$", line)
    if m:
        cur = m.group(1); engines[cur] = {}; continue
    m = re.match(r"^    (\w+):\s*(.*)$", line)
    if m and cur:
        k, v = m.group(1), m.group(2).strip()
        if v.startswith("[") and v.endswith("]"):
            v = [int(x.strip()) for x in v[1:-1].split(",") if x.strip()]
        elif v in ("true", "false"):
            v = (v == "true")
        elif v and v[0] == v[-1] and v[0] in ('"', "'"):
            v = v[1:-1]
        elif v.lstrip("-").isdigit():
            v = int(v)
        engines[cur][k] = v

for name, cfg in engines.items():
    if cfg.get("skip"): continue
    if cfg.get("already_done"): continue
    if targets and name not in targets: continue
    binary = cfg.get("binary", "")
    repo = REPO_ROOTS.get(name, "")
    if not binary or not repo: continue
    binary_path = Path(repo) / binary
    if not binary_path.exists():
        # Tolerate java JARs by checking *.jar later in shell
        if not name.startswith("chess-java"): continue
    tc = cfg.get("tc", "10+0.1") or "10+0.1"
    sf_hash = cfg.get("sf_hash", 128) or 128
    gpr = cfg.get("games_per_rung", 20) or 20
    sf_elos = cfg.get("sf_elos", []) or []
    sf_skills = cfg.get("sf_skill_levels", []) or []
    if sf_elos:
        for elo in sf_elos:
            if elo < 1320: continue   # SF UCI_Elo floor
            print(f"{name}\telo\t{elo}\t{tc}\t{sf_hash}\t{gpr}\t{repo}\t{binary}")
    elif sf_skills:
        for sk in sf_skills:
            print(f"{name}\tskill\t{sk}\t{tc}\t{sf_hash}\t{gpr}\t{repo}\t{binary}")
PY

# Build engine cmd
engine_cmd_for() {
  local name=$1 repo=$2 binary=$3
  case "$name" in
    chess-java|chess-java-cc)
      # Find a runnable jar
      local jar=$(ls "$repo"/target/*.jar "$repo"/build/libs/*.jar 2>/dev/null | grep -viE "original|sources|javadoc" | head -1 || true)
      [ -z "$jar" ] && return 1
      ENG=("cmd=java" "arg=-jar" "arg=$jar" "proto=uci")
      return 0;;
    *)
      ENG=("cmd=$repo/$binary" "proto=uci")
      return 0;;
  esac
}

WALL_START=$(date +%s)
while IFS=$'\t' read -r engine kind val tc sf_hash gpr repo binary; do
  [ -z "$engine" ] && continue
  if [ "$kind" = "elo" ]; then
    opp_name="sf_e${val}"
    sf_args=("option.UCI_LimitStrength=true" "option.UCI_Elo=$val")
  else
    opp_name="sf_sk${val}"
    sf_args=("option.Skill Level=$val")
  fi
  pgn="pgn/self_repro/${engine}_vs_${opp_name}.pgn"
  log="logs/self_repro/${engine}_vs_${opp_name}.log"
  if [ -s "$pgn" ]; then
    done=$(grep -cE '^\[Result "(1-0|0-1|1/2-1/2)"' "$pgn" 2>/dev/null || true)
    if [ "$done" -ge $((gpr-2)) ]; then
      echo "skip $engine vs $opp_name ($done games)"; continue
    fi
  fi
  if ! engine_cmd_for "$engine" "$repo" "$binary"; then
    echo "skip $engine: cannot resolve binary"; continue
  fi
  echo "[+ $(($(date +%s) - WALL_START))s] self-repro: $engine vs $opp_name ($gpr games at $tc, hash=$sf_hash)"
  cutechess-cli \
    -engine name="$engine" "${ENG[@]}" \
    -engine name="$opp_name" cmd="$SF_BIN" proto=uci option.Threads=1 option.Hash="$sf_hash" "${sf_args[@]}" \
    -each tc="$tc" \
    -openings file=fixtures/openings.epd format=epd order=random \
    -games 2 -rounds $((gpr/2)) -repeat -concurrency 2 \
    -resign movecount=5 score=900 \
    -draw movenumber=40 movecount=6 score=10 \
    -pgnout "$pgn" min \
    > "$log" 2>&1 || true
done < /tmp/self_repro_plan.tsv

echo "self-reproduction complete. PGNs in pgn/self_repro/, logs in logs/self_repro/."
