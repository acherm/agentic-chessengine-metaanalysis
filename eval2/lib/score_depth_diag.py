"""Analyze depth + time-per-move distributions from depth_diag PGNs.

Output: results/depth_diag_report.md with per-engine search-depth profile.
Answers "depth-limited vs eval-limited" for each strong engine.
"""
from __future__ import annotations

import json
import re
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
PGN = HERE / "pgn" / "depth_diag"
OUT = HERE / "results" / "depth_diag_report.md"
OUT.parent.mkdir(parents=True, exist_ok=True)

ANN_RE = re.compile(r'\{[^}]*?([-+]?\d+(?:\.\d+)?)/(\d+)\s+(\d+(?:\.\d+)?)(s|ms)?\}')


def parse_pgn_for_engine(path: Path, target_engine: str) -> list[tuple[int, float, float]]:
    """Returns [(depth, time_s, eval_cp)] for moves played by target_engine.

    PGN structure: a game is `[tag]` lines + blank line + move text + blank line.
    We split on the `[Event "..."]` boundary so each "game" includes BOTH its
    header tags and its moves.
    """
    out: list[tuple[int, float, float]] = []
    text = path.read_text()
    # Each game starts with [Event ; everything up to the next [Event is one game.
    games = re.split(r'(?=^\[Event ")', text, flags=re.M)
    for game in games:
        if not game.strip():
            continue
        h = {}
        for line in game.splitlines():
            line = line.strip()
            m = re.match(r'\[(\w+)\s+"([^"]*)"\]', line)
            if m:
                h[m.group(1)] = m.group(2)
        if "White" not in h:
            continue
        if h.get("White") != target_engine and h.get("Black") != target_engine:
            continue
        is_white = (h.get("White") == target_engine)
        # Move text = everything after the last header line. Easiest: drop tag lines.
        move_text = "\n".join(
            line for line in game.splitlines()
            if not line.strip().startswith("[")
        )
        anns = ANN_RE.findall(move_text)
        for i, (eval_val, depth, time_val, unit) in enumerate(anns):
            side_is_white = (i % 2 == 0)
            if (is_white and side_is_white) or (not is_white and not side_is_white):
                t = float(time_val) / (1000 if unit == "ms" else 1)
                out.append((int(depth), t, float(eval_val)))
    return out


def summarize(samples: list[tuple[int, float, float]]) -> dict:
    if not samples:
        return {"n": 0}
    depths = [d for d, _, _ in samples]
    times = [t for _, t, _ in samples]
    return {
        "n_moves": len(samples),
        "depth_avg": round(statistics.mean(depths), 1),
        "depth_median": round(statistics.median(depths), 0),
        "depth_min": min(depths),
        "depth_max": max(depths),
        "depth_p90": round(statistics.quantiles(depths, n=10)[8] if len(depths) >= 10 else max(depths), 1),
        "time_avg_s": round(statistics.mean(times), 2),
        "time_median_s": round(statistics.median(times), 2),
        "time_max_s": round(max(times), 2),
    }


def main() -> None:
    rows = []
    for p in sorted(PGN.glob("*.pgn")):
        # filename: <engine>_vs_<opp>.pgn — extract engine
        m = re.match(r"(.+)_vs_(.+)\.pgn", p.name)
        if not m: continue
        eng = m.group(1)
        samples = parse_pgn_for_engine(p, eng)
        s = summarize(samples)
        s["engine"] = eng
        rows.append(s)

    rows.sort(key=lambda r: -(r.get("depth_avg") or 0))
    lines = ["# Depth-utilization diagnostic", "",
             "Per-engine search depth + time-per-move profile from games vs Rustic at 120+1.",
             "",
             "| Engine | Moves | Avg depth | Median | p90 | Max | Avg time (s) | Median (s) |",
             "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for r in rows:
        if r.get("n_moves", 0) == 0:
            lines.append(f"| {r['engine']} | 0 | (no annotated games) | | | | | |")
            continue
        lines.append(
            f"| {r['engine']} | {r['n_moves']} | {r['depth_avg']} | "
            f"{r['depth_median']:.0f} | {r['depth_p90']} | {r['depth_max']} | "
            f"{r['time_avg_s']} | {r['time_median_s']} |"
        )
    OUT.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT}")
    for r in rows:
        if r.get("n_moves"):
            print(f"  {r['engine']}: avg depth {r['depth_avg']}, max {r['depth_max']}, "
                  f"avg time {r['time_avg_s']}s")


if __name__ == "__main__":
    main()
