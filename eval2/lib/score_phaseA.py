"""Derive SF-Skill-N effective Elo from Phase A PGNs.

For each Skill level N and each anchor A:
  elo_from_A = anchor_ccrl + diff(sf_skillN vs A)

Inverse-variance-weighted mean across anchors gives the effective Elo
of SF-Skill-N on this hardware. That number is stored in
results/phaseA_sf_calibration.json and loaded by Phase B as a reference
point (instead of trusting SF's nominal UCI_Elo).
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
PGN = HERE / "pgn" / "phaseA"
OUT = HERE / "results" / "phaseA_sf_calibration.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

ANCHORS = {"rustic": 1820, "asymptote": 2150}
SKILLS = [0, 5, 10, 15]


def parse_pgn(path: Path, side_A: str, side_B: str) -> list[float]:
    """Return list of side_A's scores in [0, 0.5, 1]."""
    white = None
    scores = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        m = re.match(r'\[White "([^"]+)"\]', line)
        if m: white = m.group(1)
        m = re.match(r'\[Result "([^"]+)"\]', line)
        if m and white:
            r = m.group(1)
            if r != "*":
                s = {"1-0": 1.0, "0-1": 0.0, "1/2-1/2": 0.5}.get(r)
                if s is not None:
                    if white == side_A:   scores.append(s)
                    elif white == side_B: scores.append(1.0 - s)
                white = None
    return scores


def elo_diff(pct: float) -> float:
    p = max(1e-3, min(1 - 1e-3, pct))
    return -400.0 * math.log10(1.0 / p - 1.0)


def elo_se(pct: float, n: int) -> float:
    p = max(1e-3, min(1 - 1e-3, pct))
    return 400.0 / (math.log(10) * p * (1 - p)) * math.sqrt(p * (1 - p) / n)


def main() -> None:
    calibration = {}
    for skill in SKILLS:
        sf_name = f"sf_skill{skill}"
        per_anchor = {}
        for anc, anc_elo in ANCHORS.items():
            pgn = PGN / f"{sf_name}_vs_{anc}.pgn"
            if not pgn.exists(): continue
            scores = parse_pgn(pgn, sf_name, anc)
            if not scores: continue
            n = len(scores); s = sum(scores); pct = s / n
            if pct in (0.0, 1.0):
                per_anchor[anc] = {
                    "games": n, "score_pct": round(pct, 3),
                    "elo": None, "bound": "upper" if pct == 0.0 else "lower",
                    "elo_bound": round(anc_elo + (400 if pct == 1.0 else -400) * math.log10(max(n, 1)), 0),
                }
                continue
            d = elo_diff(pct)
            se = elo_se(pct, n)
            per_anchor[anc] = {
                "games": n, "score_pct": round(pct, 3),
                "elo": round(anc_elo + d, 1), "se": round(se, 1),
            }
        # IV-weighted mean across anchors with point estimates
        measured = [v for v in per_anchor.values() if v.get("elo") is not None]
        if measured:
            w = [1.0 / (v["se"] ** 2) for v in measured]
            total_w = sum(w)
            elo = sum(v["elo"] * wi for v, wi in zip(measured, w)) / total_w
            ci = 1.96 * math.sqrt(1 / total_w)
            calibration[sf_name] = {
                "skill_level": skill,
                "effective_elo": round(elo, 1),
                "ci95": round(ci, 1),
                "per_anchor": per_anchor,
            }
        else:
            calibration[sf_name] = {"skill_level": skill,
                                    "effective_elo": None, "per_anchor": per_anchor}
    OUT.write_text(json.dumps(calibration, indent=2))
    print(f"wrote {OUT}")
    print("\n=== SF-Skill effective Elo (from Phase A) ===")
    for name, d in calibration.items():
        elo = d.get("effective_elo")
        if elo is not None:
            print(f"  {name}: {elo:.0f} ± {d['ci95']:.0f} Elo")
        else:
            print(f"  {name}: no measurable score (saturated or missing)")


if __name__ == "__main__":
    main()
