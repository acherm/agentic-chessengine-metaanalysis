"""Estimate an Elo per engine from repo evidence.

For each project we scan PGN files and try to compute an engine Elo from its
games against a *calibrated* opponent (typically Stockfish run with
`UCI_LimitStrength` at a known `UCI_Elo`). The conversion is the standard
logistic:

    score  ∈ (0, 1)
    diff   = -400 · log10(1/score − 1)
    elo    = opponent_elo + diff

We aggregate across opponents with inverse-variance weighting; SE of the Elo
diff for a match of N games is approximated by 400 / (ln(10) · sqrt(N · s·(1−s))).

This is an evidence-extraction pass — it tells us what the repo ALREADY
claims or has played, not a new controlled evaluation. Limitations we flag:
small N, mixed time controls, unknown opponent tuning, no ratings anchor
across engines.

Output:
  data/elo.json                      # per-engine Elo estimate + provenance
  updates: data/projects/<name>.json # same, embedded
  updates: reports/OVERVIEW.md       # new column
  updates: reports/SYNTHESIS.md      # new section

Usage:
  python3 scripts/extract_elo.py            # all projects
  python3 scripts/extract_elo.py chess-py   # one
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path
from typing import Any

from common import DATA_DIR, IGNORED_DIRS, REPORTS_DIR, SANDBOX, discover_projects


RE_HDR = re.compile(r'\[(\w+)\s+"([^"]*)"\]')
RE_STOCKFISH = re.compile(
    r"(stockfish|sf[\s_-]*l?\d+|sf\d+|skill\d+|stockfish-\d+|sf-l\d+)",
    re.I,
)
RE_ELO_HINT = re.compile(r"(?:elo|sf|skill|UCI_Elo)[_ -]?(\d{3,4})", re.I)
RE_CLAIM = re.compile(r"(?:approximately\s+|≈|~|about\s+)?\s*(\d{3,4})\s*(?:elo|ELO|Elo)\b")
# Stockfish skill-level -> approximate published Elo (CCRL/published
# calibration used by the per-engine compute_elo.py scripts in the
# corpus). Used when the opponent tag is "SF-L<N>" / "sf_level<N>"
# rather than a UCI_Elo anchor; the skill-level axis is coarser
# than UCI_Elo but still gives a usable opponent rating.
SF_SKILL_TO_ELO = {
    0: 1100, 1: 1350, 2: 1450, 3: 1500, 4: 1575, 5: 1650,
    6: 1750, 7: 1825, 8: 1900, 9: 1950, 10: 2000, 11: 2100,
    12: 2200, 13: 2400, 14: 2500, 15: 2500, 16: 2700,
    17: 2900, 18: 3100, 19: 3350, 20: 3600,
}
RE_SF_SKILL = re.compile(r"sf[\s_-]*l?(\d+)\b|skill[\s_-]*(\d+)\b", re.I)


def sf_skill_to_elo(name: str) -> int | None:
    """If `name` encodes a Stockfish skill level (e.g. 'SF-L8',
    'sf_level10', 'skill5'), return the approximate Elo from
    SF_SKILL_TO_ELO; otherwise None. Distinguished from RE_ELO_HINT
    because small two-digit integers are skill levels, not Elo."""
    m = RE_SF_SKILL.search(name or "")
    if not m:
        return None
    lvl_raw = m.group(1) or m.group(2)
    try:
        lvl = int(lvl_raw)
    except (TypeError, ValueError):
        return None
    # Only interpret as skill when the integer is in the 0--20 range;
    # larger numbers are almost certainly meant to be an Elo directly
    # (e.g. 'sf_1800' or 'UCI_Elo=1800').
    if 0 <= lvl <= 20:
        return SF_SKILL_TO_ELO.get(lvl)
    return None


def score_to_elo_diff(score: float, eps: float = 1e-3) -> float:
    s = max(eps, min(1 - eps, score))
    return -400.0 * math.log10(1.0 / s - 1.0)


def elo_diff_se(n_games: int, score: float) -> float:
    """Rough SE of an Elo diff from N games at observed score s.

    Derived from Var(score) = s(1−s)/N and the derivative of Elo diff wrt s.
    """
    if n_games <= 0:
        return math.inf
    s = max(1e-3, min(1 - 1e-3, score))
    var_s = s * (1 - s) / n_games
    # dDiff/ds = 400 / (ln 10 · s · (1 − s))
    d = 400.0 / (math.log(10) * s * (1 - s))
    return d * math.sqrt(var_s)


def parse_pgn_games(path: Path) -> list[dict[str, Any]]:
    """Return a list of games with White/Black/Result/optional WhiteElo/BlackElo/TC."""
    try:
        if path.stat().st_size > 25 * 1024 * 1024:
            return []
        raw = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    games: list[dict[str, Any]] = []
    cur: dict[str, Any] = {}
    has_body = False
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            if cur and has_body:
                games.append(cur)
                cur = {}
                has_body = False
            continue
        if line.startswith("["):
            m = RE_HDR.match(line)
            if not m:
                continue
            if cur.get("_started") and not has_body:
                # new header block starting without blank line
                pass
            cur[m.group(1)] = m.group(2)
            cur["_started"] = True
        else:
            has_body = True
    if cur and has_body:
        games.append(cur)
    return games


def guess_opponent_elo(game: dict[str, Any], fname_hint: int | None) -> tuple[str | None, int | None]:
    """Return (agent_color, opponent_elo_guess) for one game.

    agent_color in {"w", "b"}; opponent_elo_guess may be None if unknown.
    """
    white = game.get("White", "") or ""
    black = game.get("Black", "") or ""
    welo = game.get("WhiteElo", "")
    belo = game.get("BlackElo", "")
    w_is_sf = bool(RE_STOCKFISH.search(white))
    b_is_sf = bool(RE_STOCKFISH.search(black))
    agent_color: str | None = None
    opp_elo: int | None = None
    if w_is_sf and not b_is_sf:
        agent_color = "b"
        if welo.isdigit():
            opp_elo = int(welo)
    elif b_is_sf and not w_is_sf:
        agent_color = "w"
        if belo.isdigit():
            opp_elo = int(belo)
    elif w_is_sf and b_is_sf:
        # self-play between two SF levels — skip
        return None, None
    # If no SF identified, try via UCI_Elo in name.
    if opp_elo is None:
        if w_is_sf:
            m = RE_ELO_HINT.search(white)
            if m:
                opp_elo = int(m.group(1))
        elif b_is_sf:
            m = RE_ELO_HINT.search(black)
            if m:
                opp_elo = int(m.group(1))
    # Stockfish-skill-level opponent ("SF-L8" / "sf_level10" / "skill5")
    # --- map skill to approximate published Elo.
    if opp_elo is None:
        if w_is_sf:
            opp_elo = sf_skill_to_elo(white)
        elif b_is_sf:
            opp_elo = sf_skill_to_elo(black)
    # Fallback to filename hint
    if opp_elo is None and fname_hint:
        opp_elo = fname_hint
    return agent_color, opp_elo


def agent_score(game: dict[str, Any], agent_color: str) -> float | None:
    res = game.get("Result", "")
    if res == "*":
        return None
    if agent_color == "w":
        return {"1-0": 1.0, "0-1": 0.0, "1/2-1/2": 0.5}.get(res)
    return {"1-0": 0.0, "0-1": 1.0, "1/2-1/2": 0.5}.get(res)


def aggregate_matches(matches: list[dict[str, Any]]) -> dict[str, Any]:
    """matches: [{opp_elo, n_games, agent_score_sum}, ...] → Elo estimate."""
    weights: list[float] = []
    estimates: list[float] = []
    per_opp = []
    for m in matches:
        if m["n_games"] < 2:
            continue
        score = m["agent_score_sum"] / m["n_games"]
        diff = score_to_elo_diff(score)
        se = elo_diff_se(m["n_games"], score)
        if math.isinf(se) or se == 0:
            continue
        est = m["opp_elo"] + diff
        w = 1.0 / (se * se)
        estimates.append(est)
        weights.append(w)
        per_opp.append(
            {
                "opp_elo": m["opp_elo"],
                "n_games": m["n_games"],
                "score": round(score, 3),
                "elo_diff": round(diff, 1),
                "se": round(se, 1),
                "elo_est": round(est, 1),
            }
        )
    if not weights:
        return {"n_games": sum(m["n_games"] for m in matches), "per_opp": per_opp}
    total_w = sum(weights)
    elo = sum(e * w for e, w in zip(estimates, weights)) / total_w
    se = math.sqrt(1.0 / total_w)
    return {
        "elo_estimate": round(elo, 1),
        "ci95": round(1.96 * se, 1),
        "n_games": sum(m["n_games"] for m in matches if m["n_games"] > 0),
        "per_opp": per_opp,
    }


def scan_project_pgns(root: Path) -> list[dict[str, Any]]:
    """Aggregate all PGN files in the repo into per-opponent matches."""
    buckets: dict[int, dict[str, Any]] = {}
    file_count = 0
    for p in root.rglob("*.pgn"):
        if IGNORED_DIRS & set(p.parts):
            continue
        file_count += 1
        hint_m = RE_ELO_HINT.search(p.name)
        fname_hint = int(hint_m.group(1)) if hint_m else None
        # Cross-check against skill-level filenames (e.g. sf_level8.pgn):
        # a UCI_Elo hint already takes precedence, but many gauntlets
        # are driven by Stockfish skill rather than UCI_Elo.
        if fname_hint is None:
            fname_hint = sf_skill_to_elo(p.name)
        games = parse_pgn_games(p)
        for g in games:
            agent_color, opp_elo = guess_opponent_elo(g, fname_hint)
            if agent_color is None or opp_elo is None:
                continue
            score = agent_score(g, agent_color)
            if score is None:
                continue
            b = buckets.setdefault(opp_elo, {"opp_elo": opp_elo, "n_games": 0, "agent_score_sum": 0.0})
            b["n_games"] += 1
            b["agent_score_sum"] += score
    return list(buckets.values())


def scan_claims(root: Path) -> list[dict[str, Any]]:
    """Grep top-level docs for agent-claimed Elo numbers."""
    candidates = []
    for name in ("README.md", "ASSESSMENT.md", "NOTES.md", "STATUS.md", "RESULTS.md", "readme.md"):
        p = root / name
        if p.exists():
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            for m in RE_CLAIM.finditer(text):
                val = int(m.group(1))
                if 50 <= val <= 3500:
                    # Keep a small snippet for evidence
                    s = max(0, m.start() - 60)
                    e = min(len(text), m.end() + 60)
                    candidates.append({"file": name, "elo": val, "context": text[s:e].replace("\n", " ")})
    return candidates


def process(project_dir: Path) -> dict[str, Any]:
    matches = scan_project_pgns(project_dir)
    elo_agg = aggregate_matches(matches)
    claims = scan_claims(project_dir)
    return {
        "name": project_dir.name,
        "path": str(project_dir),
        "matches": matches,
        "aggregate": elo_agg,
        "agent_claims": claims,
    }


def write_synthesis_hook(all_elo: dict[str, dict[str, Any]]) -> None:
    """Append a short 'Estimated Elo' section to SYNTHESIS.md if absent."""
    syn = REPORTS_DIR / "SYNTHESIS.md"
    if not syn.exists():
        return
    text = syn.read_text()
    marker = "## Estimated Elo (mined from PGN evidence)"
    if marker in text:
        # Replace existing block up to the next H2.
        before, after = text.split(marker, 1)
        tail = after.split("\n## ", 1)
        rest = "\n## " + tail[1] if len(tail) > 1 else ""
    else:
        before = text
        rest = ""
    rows = []
    rows.append(marker)
    rows.append("")
    rows.append("_Best-effort per-engine Elo from the PGN files in each repo, using score-to-Elo logistic and inverse-variance aggregation across opponents. Lower bounds: games were played under the user's budget; more compute could push numbers higher. An 'agent-claimed' column reports the strongest claim found in top-level docs._")
    rows.append("")
    rows.append("| Project | N games | Opponents | Estimated Elo | CI95 | Agent-claimed |")
    rows.append("|---|---:|---|---:|---:|---|")
    for name in sorted(all_elo):
        d = all_elo[name]
        agg = d.get("aggregate") or {}
        est = agg.get("elo_estimate")
        ci = agg.get("ci95")
        n = agg.get("n_games", 0)
        opps = ", ".join(str(o["opp_elo"]) for o in (agg.get("per_opp") or [])) or "—"
        claim_vals = sorted({c["elo"] for c in (d.get("agent_claims") or [])}, reverse=True)
        claim_s = ", ".join(str(v) for v in claim_vals[:3]) or "—"
        rows.append(
            f"| {name} | {n} | {opps} | {est if est is not None else '—'} | {'±' + str(ci) if ci else '—'} | {claim_s} |"
        )
    rows.append("")
    new_block = "\n".join(rows)
    syn.write_text(before.rstrip() + "\n\n" + new_block + "\n" + rest)


def main(argv: list[str]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    all_targets = {name: path for name, path in discover_projects()}
    if argv:
        targets = [(a, all_targets.get(a) or (SANDBOX / a)) for a in argv]
    else:
        targets = list(all_targets.items())
    result: dict[str, dict[str, Any]] = {}
    for logical, p in targets:
        if not p.exists():
            continue
        print(f"→ {logical}")
        d = process(p)
        d["name"] = logical
        result[logical] = d
        appendix = DATA_DIR / "projects" / f"{logical}.json"
        if appendix.exists():
            try:
                prior = json.loads(appendix.read_text())
            except Exception:
                prior = {"name": logical, "path": str(p)}
        else:
            prior = {"name": logical, "path": str(p)}
        prior["elo_analysis"] = d
        appendix.parent.mkdir(parents=True, exist_ok=True)
        appendix.write_text(json.dumps(prior, indent=2, default=str))
        agg = d.get("aggregate") or {}
        est = agg.get("elo_estimate")
        n = agg.get("n_games", 0)
        claims = sorted({c["elo"] for c in (d.get("agent_claims") or [])})
        print(f"    n_games={n}  elo_est={est}  claims={claims}")
    (DATA_DIR / "elo.json").write_text(json.dumps(result, indent=2, default=str))
    write_synthesis_hook(result)
    print(f"Wrote data/elo.json and updated reports/SYNTHESIS.md")


if __name__ == "__main__":
    main(sys.argv[1:])
