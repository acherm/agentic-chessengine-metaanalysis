#!/usr/bin/env bash
# quick_anchor_match.sh — fast CCRL-anchored Elo for in-loop agent use.
#
# Designed to be called by a coding agent during a tuning loop:
#   1. agent edits engine code
#   2. agent rebuilds binary
#   3. agent calls this script with the engine binary path
#   4. script plays 30 games (15 vs Rustic + 15 vs SF Skill 10) at TC=30+0.3
#   5. script prints a one-line CCRL-anchored Elo with 95% CI
#   6. agent decides whether to keep the change
#
# Total wall-time: ~12-15 minutes per call at concurrency=2 on M-class CPU.
# Faster than the full Phase B (which uses 5 anchors at 120+1) by ~10×.
# Sacrifices: some precision (±50-80 Elo CI typical) and TC mismatch with
# final 120+1 evaluation. Adequate as a tuning signal; final certification
# should always be a full Phase B run.
#
# Usage:
#   ./quick_anchor_match.sh <engine_uci_command>
#
# Examples:
#   ./quick_anchor_match.sh "/path/to/my-engine/build/release/engine"
#   ./quick_anchor_match.sh "java -jar /path/to/engine.jar"
#   ./quick_anchor_match.sh "python3 -u /path/to/engine.py"
#
# Prereqs (built once via build_images.sh):
#   - eval2/anchor-rustic:latest        (CCRL 1820)
#   - eval2/stockfish:18                 (Skill 10 ≈ 2004 measured)
#   - cutechess-cli, fixtures/openings.epd

set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")"/.. && pwd)
cd "$HERE"

if [ $# -lt 1 ]; then
  echo "usage: $0 '<engine UCI command>'" >&2
  echo "e.g.: $0 '/Users/mathieuacher/SANDBOX/chess-purec/purec'" >&2
  exit 64
fi

ENGINE_CMD="$1"
LABEL="${2:-engine}"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

# Match parameters — tunable, but defaults are sensible
TC="${TC:-30+0.3}"           # tuning-loop TC; mid between blitz and CCRL
GAMES_PER_REF="${GAMES:-15}"  # 15 games per ref → 30 total → ~12-15 min
WRAP="$HERE/wrappers/docker_engine.sh"
SF_IMG=eval2/stockfish:18
RUSTIC_IMG=eval2/anchor-rustic:latest
RUSTIC_CCRL=1820
SF_SKILL10_ELO=2004   # from Phase A calibration

# Confirm anchors are available
docker image inspect "$SF_IMG" >/dev/null 2>&1 || { echo "missing $SF_IMG" >&2; exit 65; }
docker image inspect "$RUSTIC_IMG" >/dev/null 2>&1 || { echo "missing $RUSTIC_IMG" >&2; exit 65; }

run_pair() {
  local ref_name=$1
  local pgn="$WORK/${ref_name}.pgn"
  local ref_args
  case "$ref_name" in
    rustic)
      ref_args=(cmd="$WRAP" arg="$RUSTIC_IMG" arg=--cpus=2 arg=--memory=1g proto=uci)
      ;;
    sf_skill10)
      ref_args=(cmd="$WRAP" arg="$SF_IMG" arg=--cpus=2 arg=--memory=1g proto=uci
                "option.Skill Level=10" option.Threads=1 option.Hash=128)
      ;;
    *) echo "unknown ref $ref_name" >&2; return 1 ;;
  esac
  cutechess-cli \
    -engine name="$LABEL" cmd=bash arg=-lc "arg=exec $ENGINE_CMD" proto=uci \
    -engine name="$ref_name" "${ref_args[@]}" \
    -each tc="$TC" \
    -openings file=fixtures/openings.epd format=epd order=random \
    -games 2 -rounds $((GAMES_PER_REF/2)) -repeat -concurrency 2 \
    -resign movecount=5 score=900 \
    -draw movenumber=40 movecount=6 score=10 \
    -pgnout "$pgn" min \
    > "$WORK/${ref_name}.log" 2>&1 || true
}

echo "[quick_anchor] running 2 pairings at $TC ($((2*GAMES_PER_REF)) games total)..." >&2
run_pair rustic
run_pair sf_skill10

# Score
python3 - <<PY
import re, math, sys
def score_pgn(path, eng):
    if not __import__("os").path.exists(path): return None
    white=None; scores=[]
    for line in open(path):
        line=line.strip()
        m=re.match(r'\[White "([^"]+)"\]', line);
        if m: white=m.group(1)
        m=re.match(r'\[Result "([^"]+)"\]', line)
        if m and white:
            r=m.group(1)
            if r!="*":
                s={"1-0":1.0,"0-1":0.0,"1/2-1/2":0.5}[r]
                scores.append(s if white=="$LABEL" else 1-s); white=None
    return scores if scores else None

def estimate(scores, ref_elo):
    n=len(scores); s=sum(scores); pct=s/n
    pc=max(1e-3,min(1-1e-3,pct))
    diff=-400*math.log10(1/pc-1)
    se=400/(math.log(10)*pc*(1-pc))*math.sqrt(pc*(1-pc)/n)
    return ref_elo+diff, se, n, pct

pts=[]; rows=[]
for ref, ref_elo in [("rustic", $RUSTIC_CCRL), ("sf_skill10", $SF_SKILL10_ELO)]:
    sc = score_pgn(f"$WORK/{ref}.pgn", ref)
    if not sc:
        rows.append(f"  vs {ref:11s}: no games"); continue
    e, se, n, pct = estimate(sc, ref_elo)
    if 0.02 < pct < 0.98:
        pts.append((e, se))
        rows.append(f"  vs {ref:11s} ({ref_elo}): {sum(sc):.1f}/{n}={pct:.0%} → {e:.0f} ±{se:.0f}")
    else:
        rows.append(f"  vs {ref:11s} ({ref_elo}): {sum(sc):.1f}/{n}={pct:.0%} (saturated)")

print("\n".join(rows))
if not pts:
    print("RESULT: no measurable Elo (saturation in both pairings — try a different anchor pair)")
else:
    w = [1/(s**2) for _,s in pts]; T=sum(w)
    elo = sum(e*wi for (e,_),wi in zip(pts,w))/T
    ci = 1.96*math.sqrt(1/T)
    print(f"RESULT: anchored Elo = {elo:.0f} ± {ci:.0f}  (95% CI; n={len(pts)} measurable refs)")
PY
