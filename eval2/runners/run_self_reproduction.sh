#!/usr/bin/env bash
# Self-reproduction runner: replay each engine's original self-eval
# conditions (TC, SF Hash, UCI_Elo rungs) to verify that our eval2
# setup reproduces the originally-claimed Elo. Paper-relevant diagnostic
# that shows how much of each engine's claim is methodology vs strength.
#
# Reads per-engine config from runners/self_reproduction.yaml.
# Output PGNs under pgn/self_reproduction/<engine>_vs_sfN.pgn.
#
# NOT to be confused with run_anchor_gauntlet.sh (the canonical
# CCRL-anchored measurement). This runner uses SF UCI_Elo as the
# opponent — the SAME knob we know is compressed — precisely to
# reproduce what the agents who built these engines actually did.
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE"
mkdir -p pgn/self_reproduction logs/self_reproduction

# Parse engine list from YAML. Simple flat-key reader (no PyYAML dep).
python3 - <<'PY' > /tmp/self_repro_plan.tsv
import sys, re
from pathlib import Path

path = Path("runners/self_reproduction.yaml")
engines = {}
cur = None
for raw in path.read_text().splitlines():
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
        elif v and v[0] == v[-1] and v[0] in ('"', "'"):
            v = v[1:-1]
        elif v.isdigit():
            v = int(v)
        engines[cur][k] = v

# Emit TSV: engine \t tc \t sf_hash \t games_per_rung \t elos(comma) \t notes
for name, cfg in engines.items():
    tc = cfg.get("tc", "10+0.1")
    sf_hash = cfg.get("sf_hash", 128) or 128
    gpr = cfg.get("games_per_rung", 20) or 20
    elos = cfg.get("sf_elos", [])
    if not elos: continue
    elos_s = ",".join(str(e) for e in elos if e >= 1320)  # skip below SF's UCI_Elo floor
    print(f"{name}\t{tc}\t{sf_hash}\t{gpr}\t{elos_s}")
PY

WRAP=wrappers/docker_engine.sh
SF_IMG=eval2/stockfish:16.1

while IFS=$'\t' read -r engine tc sf_hash gpr elos; do
  [ -z "$engine" ] && continue
  # Get docker image from manifest
  image=$(python3 -c "
import sys; sys.path.insert(0,'lib')
import manifest
m = manifest.by_name(manifest.load()[0])
e = m.get('$engine')
print(e.image if e else '', end='')")
  [ -z "$image" ] && { echo "skip $engine (not in manifest)"; continue; }
  # Verify image exists
  if ! docker image inspect "$image" >/dev/null 2>&1; then
    echo "skip $engine (image $image not built)"; continue
  fi
  IFS=',' read -r -a rungs <<<"$elos"
  for rung in "${rungs[@]}"; do
    pgn="pgn/self_reproduction/${engine}_vs_sf${rung}_tc${tc//[:\/+]/_}_h${sf_hash}.pgn"
    log="logs/self_reproduction/${engine}_vs_sf${rung}.log"
    if [ -s "$pgn" ]; then
      done=$(grep -cE '^\[Result "(1-0|0-1|1/2-1/2)"' "$pgn")
      [ "$done" -ge $((gpr-2)) ] && { echo "skip $engine vs sf${rung} ($done games)"; continue; }
    fi
    echo "self-repro: $engine vs sf${rung} at $tc hash=$sf_hash ($gpr games)"
    cutechess-cli \
      -engine name="$engine" cmd="$WRAP" arg="$image" arg=--cpus=2 arg=--memory=1g proto=uci \
      -engine name="sf${rung}" cmd="$WRAP" arg="$SF_IMG" arg=--cpus=2 arg=--memory=1g proto=uci \
        option.UCI_LimitStrength=true option.UCI_Elo="$rung" option.Threads=1 option.Hash="$sf_hash" \
      -each tc="$tc" \
      -openings file=fixtures/openings.epd format=epd order=random \
      -games 2 -rounds $((gpr/2)) -repeat -concurrency 2 \
      -resign movecount=5 score=900 \
      -draw movenumber=40 movecount=6 score=10 \
      -pgnout "$pgn" min \
      > "$log" 2>&1 || true
  done
done < /tmp/self_repro_plan.tsv

echo "self-reproduction done. PGNs in pgn/self_reproduction/, logs in logs/self_reproduction/."
