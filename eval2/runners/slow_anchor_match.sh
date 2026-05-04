#!/usr/bin/env bash
# slow_anchor_match.sh — CCRL-anchored Elo for in-loop agent use,
# at the SAME TC the canonical Phase B uses (120s base + 1s/move).
#
# Identical to quick_anchor_match.sh except:
#   - TC=120+1 instead of 30+0.3 (matches Phase B / certification TC)
#   - 20 games per anchor instead of 15 (keeps CI tighter despite slower TC)
#   - ~30-40 min wall per call instead of ~12-15
#
# When to use this instead of quick_anchor_match.sh:
#   ALWAYS when the agent's iteration target is post-retry Phase B Elo.
#   The fast (30+0.3) signal optimises for fast-TC strength, which may
#   not transfer to the certification TC (120+1).
#
# Usage:
#   ./slow_anchor_match.sh <engine_uci_command>
#
# Output (one line, parseable):
#   RESULT: anchored Elo = N ± CI  (vs Rustic + SF Skill 10, TC=120+1)
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE"

ENG_CMD=${1:?"engine command required (path or full invocation)"}
TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

WRAP=wrappers/docker_engine.sh
SF_IMG=eval2/stockfish:18
TC=120+1
GAMES=20

# If the engine cmd is a single path, wrap directly; otherwise take it verbatim
if [ -f "$ENG_CMD" ] && [ -x "$ENG_CMD" ]; then
  ENG_ARGS=(cmd="$ENG_CMD" proto=uci)
else
  ENG_ARGS=(cmd=bash arg=-c "arg=$ENG_CMD" proto=uci)
fi

run_pair() {
  local opp=$1; shift
  local opp_args=("$@")
  cutechess-cli \
    -engine name=engine "${ENG_ARGS[@]}" \
    -engine name="$opp" "${opp_args[@]}" \
    -each tc=$TC \
    -openings file=fixtures/openings.epd format=epd order=random \
    -games 2 -rounds $((GAMES/2)) -repeat -concurrency 2 \
    -resign movecount=5 score=900 \
    -draw movenumber=40 movecount=6 score=10 \
    -pgnout "$TMPDIR/${opp}.pgn" min \
    > "$TMPDIR/${opp}.log" 2>&1 || true
}

run_pair rustic     cmd="$WRAP" arg=eval2/anchor-rustic:latest arg=--cpus=2 arg=--memory=1g proto=uci
run_pair sf_skill10 cmd="$WRAP" arg="$SF_IMG"               arg=--cpus=2 arg=--memory=1g proto=uci \
                    "option.Skill Level=10" option.Threads=1 option.Hash=128

python3 - "$TMPDIR" <<'PY'
import math, re, sys
from pathlib import Path
ANCHOR = {"rustic": 1820, "sf_skill10": 2004}
def parse(p, eng="engine"):
    txt = Path(p).read_text(errors="ignore")
    w=d=l=0
    for g in re.split(r'(?=^\[Event ")', txt, flags=re.M):
        if not g.strip(): continue
        wm=re.search(r'\[White "([^"]+)"',g); bm=re.search(r'\[Black "([^"]+)"',g); rm=re.search(r'\[Result "([^"]+)"',g)
        if not(wm and bm and rm): continue
        W,B,R = wm.group(1),bm.group(1),rm.group(1)
        if eng not in (W,B): continue
        if R=='1-0':   (None if W==eng else None); w += 1 if W==eng else 0; l += 1 if B==eng else 0
        elif R=='0-1': w += 1 if B==eng else 0; l += 1 if W==eng else 0
        elif R=='1/2-1/2': d+=1
    return w,d,l
tmp = Path(sys.argv[1])
pairs = []
for opp, anc in ANCHOR.items():
    pgn = tmp/f"{opp}.pgn"
    if not pgn.is_file(): continue
    w,d,l = parse(pgn); n = w+d+l
    if n == 0:
        print(f"  {opp}: 0 games (engine crashed or no PGNs)"); continue
    s = (w+0.5*d)/n
    if 0 < s < 1:
        ediff = 400*math.log10(s/(1-s))
        elo = anc + ediff
        se = 400/(n**0.5)
        pairs.append((elo, se))
        print(f"  vs {opp:<11} ({anc}): {w}-{d}-{l} ({100*s:.0f}%) → {elo:.0f} ± {1.96*se:.0f}")
    else:
        print(f"  vs {opp:<11} ({anc}): {w}-{d}-{l} ({100*s:.0f}%) (saturated)")
if not pairs:
    print("RESULT: no measurable signal (all anchors saturated)"); sys.exit(0)
weights = [1/(s**2) for _, s in pairs]
total = sum(weights)
elo = sum(e*w for (e,_), w in zip(pairs, weights)) / total
se = (1/total)**0.5
print(f"\nRESULT: anchored Elo = {elo:.0f} ± {1.96*se:.0f}  (TC=120+1, {sum(1 for _ in pairs)} measurable anchors)")
PY
