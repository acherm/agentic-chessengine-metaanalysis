"""Score PGNs and produce eval2/results/SUMMARY.md.

Extends the old eval/score_pgn.py with:
  - separate aggregation for SF-ladder gauntlets and anchor matches;
  - per-engine card under results/per_engine/<name>.json (preflight +
    ladder + anchors + RR + tactics merged);
  - calibration check that anchors land within ±50 Elo of their CCRL
    nominal; flags otherwise.
"""
from __future__ import annotations

import json
import math
import re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
PGN = HERE / "pgn"
RES = HERE / "results"

RE_HDR = re.compile(r'\[(\w+)\s+"([^"]*)"\]')


def parse_pgn(path: Path) -> list[dict]:
    games: list[dict] = []
    cur: dict = {}
    has_body = False
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            if cur and has_body:
                games.append(cur)
                cur = {}
                has_body = False
            continue
        if line.startswith("["):
            m = RE_HDR.match(line)
            if m:
                cur[m.group(1)] = m.group(2)
        else:
            has_body = True
    if cur and has_body:
        games.append(cur)
    return games


def score_for(game: dict, engine: str) -> float | None:
    w, b, r = game.get("White", ""), game.get("Black", ""), game.get("Result", "")
    if r == "*":
        return None
    if w == engine:
        return {"1-0": 1.0, "0-1": 0.0, "1/2-1/2": 0.5}.get(r)
    if b == engine:
        return {"1-0": 0.0, "0-1": 1.0, "1/2-1/2": 0.5}.get(r)
    return None


def elo_diff(score: float, eps: float = 1e-3) -> float:
    s = max(eps, min(1 - eps, score))
    return -400.0 * math.log10(1.0 / s - 1.0)


def elo_diff_se(n: int, score: float) -> float:
    if n <= 0:
        return math.inf
    s = max(1e-3, min(1 - 1e-3, score))
    return 400.0 / (math.log(10) * s * (1 - s)) * math.sqrt(s * (1 - s) / n)


def aggregate_inverse_variance(per_rung: list[dict]) -> tuple[float | None, float | None]:
    weights, ests = [], []
    for r in per_rung:
        if math.isinf(r["se"]) or r["se"] == 0:
            continue
        weights.append(1.0 / (r["se"] * r["se"]))
        ests.append(r["elo_est"])
    if not weights:
        return None, None
    total_w = sum(weights)
    elo = sum(e * w for e, w in zip(ests, weights)) / total_w
    ci95 = 1.96 * math.sqrt(1.0 / total_w)
    return round(elo, 1), round(ci95, 1)


def score_one_engine_vs_sf(engine: str, pgn_dir: Path = PGN) -> dict:
    per_rung_buckets: dict[int, list[float]] = defaultdict(list)
    for p in sorted(pgn_dir.glob(f"*{engine}*sf*.pgn")):
        m = re.search(r"sf(?P<rung>\d{3,4})", p.name)
        if not m:
            continue
        rung = int(m.group("rung"))
        for g in parse_pgn(p):
            s = score_for(g, engine)
            if s is not None:
                per_rung_buckets[rung].append(s)

    per_rung = []
    for rung in sorted(per_rung_buckets):
        results = per_rung_buckets[rung]
        n = len(results)
        s = sum(results) / n if n else 0
        d = elo_diff(s) if n else 0
        se = elo_diff_se(n, s)
        per_rung.append({
            "rung": rung, "n": n, "score": round(s, 3),
            "elo_diff": round(d, 1), "se": round(se, 1),
            "elo_est": round(rung + d, 1) if n else None,
        })
    elo, ci = aggregate_inverse_variance(per_rung)
    return {"per_rung": per_rung, "elo_iv": elo, "ci95": ci,
            "n_games": sum(r["n"] for r in per_rung)}


def calibration_check(anchors: list[dict], result: dict) -> list[str]:
    """Return human-readable warnings if anchors land far from CCRL nominal."""
    warns = []
    for a in anchors:
        a_name, nominal = a["name"], a["ccrl_40_4_elo"]
        elo = result.get(a_name, {}).get("elo_iv")
        if elo is None:
            warns.append(f"calibration: no SF result for anchor {a_name}")
            continue
        delta = elo - nominal
        if abs(delta) > 50:
            warns.append(
                f"calibration: anchor {a_name} measured Elo {elo} vs CCRL "
                f"nominal {nominal} (delta {delta:+.0f}); SF rungs may be "
                "miscalibrated on this hardware"
            )
    return warns
