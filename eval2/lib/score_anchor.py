"""Anchor-based Elo scoring — the canonical Elo computation for eval2.

For each engine E and each anchor A:
  score(E vs A) = wins + 0.5*draws
  pct(E vs A)   = score / games
  diff_elo      = -400 * log10(1/pct - 1)   # from A's frame; negate for E
  E_elo_via_A   = A.ccrl_40_4_elo + E_diff   # where E_diff is from E's frame

Across multiple anchors, we combine via inverse-variance weighting:
  E_elo_final = sum(E_elo_via_A * w_A) / sum(w_A)    where w_A = 1/SE(E_via_A)^2

We flag cross-anchor disagreements (any two anchor estimates differing
by > DISAGREE_ELO) as diagnostic ("anchor_disagree" in the card).

Engines that score 0.0 or 1.0 against an anchor (no signal) get a
ONE-SIDED BOUND instead of a point estimate:
  score = 0.0 → E_elo_via_A < A.ccrl_40_4_elo - 400*log10(games)  (pessimistic)
  score = 1.0 → E_elo_via_A > A.ccrl_40_4_elo + 400*log10(games)  (optimistic)
"""
from __future__ import annotations

import json
import math
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
PGN = HERE / "pgn"
RES = HERE / "results"

DISAGREE_ELO = 80.0  # flag if two anchor estimates differ by more than this

# Phase-A-measured effective Elo for SF Skill configurations (loaded from
# results/phaseA_sf_calibration.json at runtime; falls back to defaults below).
SF_SKILL_ELOS_DEFAULT = {
    "sf_skill0": 900.0,    # Phase A bounded at <1229 vs Rustic 1820; midpoint estimate 900 ± 300
    "sf_skill5": 1658.0,
    "sf_skill10": 2004.0,
    "sf_skill15": 2325.0,
}


def load_reference_elos() -> dict[str, float]:
    """Pull external anchor + Phase-A-measured SF effective Elo into one map."""
    refs = {"rustic": 1820.0, "asymptote": 2150.0}
    p = Path(__file__).resolve().parent.parent / "results" / "phaseA_sf_calibration.json"
    if p.exists():
        cal = json.loads(p.read_text())
        for name, d in cal.items():
            if d.get("effective_elo") is not None:
                refs[name] = d["effective_elo"]
    else:
        refs.update(SF_SKILL_ELOS_DEFAULT)
    return refs


@dataclass
class AnchorPair:
    anchor: str            # anchor name
    anchor_elo: float      # anchor's CCRL 40/4 rating
    n: int                 # games played
    wins: int
    draws: int
    losses: int
    score_pct: float       # wins + 0.5*draws, in [0,1]
    elo_via_anchor: float | None  # None if saturated (0 or 1)
    elo_se: float | None
    bound: str | None      # 'upper' / 'lower' / None


def parse_pgn(path: Path, engine_name: str, opp_name: str) -> list[float]:
    """Return list of engine-perspective scores [0, 0.5, 1]."""
    scores = []
    white = None
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
                    if white == engine_name:
                        scores.append(s)
                    elif white == opp_name:
                        scores.append(1.0 - s)
                white = None
    return scores


def elo_from_score(pct: float) -> float:
    pct = max(1e-3, min(1 - 1e-3, pct))
    return -400.0 * math.log10(1.0 / pct - 1.0)


def elo_se(pct: float, n: int) -> float:
    pct = max(1e-3, min(1 - 1e-3, pct))
    return 400.0 / (math.log(10) * pct * (1 - pct)) * math.sqrt(pct * (1 - pct) / n)


def score_vs_anchor(engine: str, anchor: str, anchor_elo: float, pgn_path: Path) -> AnchorPair | None:
    if not pgn_path.exists():
        return None
    scores = parse_pgn(pgn_path, engine, anchor)
    if not scores:
        return None
    n = len(scores)
    w = sum(1 for s in scores if s == 1.0)
    d = sum(1 for s in scores if s == 0.5)
    l = n - w - d
    pct = sum(scores) / n
    saturated = (w == n) or (l == n)
    if saturated:
        if w == n:
            bound = "lower"
            elo_est = anchor_elo + 400 * math.log10(max(n, 1))
        else:
            bound = "upper"
            elo_est = anchor_elo - 400 * math.log10(max(n, 1))
        return AnchorPair(
            anchor=anchor, anchor_elo=anchor_elo,
            n=n, wins=w, draws=d, losses=l, score_pct=pct,
            elo_via_anchor=round(elo_est, 0), elo_se=None, bound=bound,
        )
    diff = elo_from_score(pct)
    se = elo_se(pct, n)
    return AnchorPair(
        anchor=anchor, anchor_elo=anchor_elo,
        n=n, wins=w, draws=d, losses=l, score_pct=round(pct, 3),
        elo_via_anchor=round(anchor_elo + diff, 1), elo_se=round(se, 1), bound=None,
    )


def combine_anchors(pairs: list[AnchorPair]) -> dict:
    """Inverse-variance weighted combine. Excludes saturated (bounded) pairs."""
    measured = [p for p in pairs if p.elo_se is not None]
    if not measured:
        # All anchors saturated or missing; return the tightest bound we have.
        if not pairs:
            return {"elo": None, "ci95": None, "status": "no_data"}
        # Pick the informative one (engine between bounds if possible).
        upper = [p for p in pairs if p.bound == "upper"]
        lower = [p for p in pairs if p.bound == "lower"]
        out = {"elo": None, "ci95": None, "status": "bounded"}
        if lower:
            out["lower_bound"] = max(p.elo_via_anchor for p in lower)
        if upper:
            out["upper_bound"] = min(p.elo_via_anchor for p in upper)
        return out

    weights = [1.0 / (p.elo_se ** 2) for p in measured]
    total_w = sum(weights)
    elo = sum(p.elo_via_anchor * w for p, w in zip(measured, weights)) / total_w
    ci = 1.96 * math.sqrt(1.0 / total_w)
    # Disagreement check
    elos = [p.elo_via_anchor for p in measured]
    spread = (max(elos) - min(elos)) if len(elos) >= 2 else 0.0
    disagree = spread > DISAGREE_ELO
    return {
        "elo": round(elo, 1),
        "ci95": round(ci, 1),
        "status": "disagreement" if disagree else "ok",
        "spread_elo": round(spread, 1),
        "per_anchor": [
            {"anchor": p.anchor, "elo": p.elo_via_anchor, "se": p.elo_se,
             "score_pct": p.score_pct, "games": p.n}
            for p in measured
        ],
    }


def score_engine(engine: str, anchors: list[tuple[str, float]],
                 pgn_dir: Path = PGN / "anchor") -> dict:
    pairs: list[AnchorPair] = []
    for anc_name, anc_elo in anchors:
        pgn = pgn_dir / f"{engine}_vs_{anc_name}.pgn"
        p = score_vs_anchor(engine, anc_name, anc_elo, pgn)
        if p: pairs.append(p)
    combined = combine_anchors(pairs)
    combined["engine"] = engine
    combined["raw_pairs"] = [
        {"anchor": p.anchor, "anchor_elo": p.anchor_elo, "games": p.n,
         "W/D/L": f"{p.wins}/{p.draws}/{p.losses}",
         "score_pct": p.score_pct, "elo": p.elo_via_anchor, "se": p.elo_se,
         "bound": p.bound}
        for p in pairs
    ]
    return combined
