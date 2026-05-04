"""Extract gameplay evidence (PGNs, Elo hints) and perft outputs per project.

Findings are appended to `data/projects/<name>.json` under keys:
  - pgn_files: list of {path, n_games, results, elos, time_control, sample_headers}
  - perft_evidence: list of {file, match}  (textual matches of perft lines in the repo)
  - gauntlet_filenames: list of gauntlet PGN basenames with Elo hints

Usage:
  python3 scripts/elo_and_perft.py             # all projects
  python3 scripts/elo_and_perft.py chess-py    # single
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

from common import DATA_DIR, SANDBOX, IGNORED_DIRS, discover_projects


# PGN header / result patterns (bounded to avoid catastrophic backtracking).
RE_HDR = re.compile(r'\[(\w+)\s+"([^"]*)"\]')
RE_RESULT = re.compile(r'\b(1-0|0-1|1/2-1/2|\*)\b')
RE_PERFT = re.compile(r"\bperft\s*\(?(\d+)\)?\s*[:=]?\s*([0-9_,]+)", re.I)
RE_ELO = re.compile(r"(?:elo|sf|skill)[_-]?(\d+)", re.I)


def parse_pgn(path: Path) -> dict[str, Any] | None:
    try:
        if path.stat().st_size > 20 * 1024 * 1024:
            return None
        raw = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None
    games = raw.split("\n\n[Event ")
    n_games = len(games) if raw.lstrip().startswith("[Event") else len(games) - 1
    results: dict[str, int] = {}
    whites: set[str] = set()
    blacks: set[str] = set()
    whites_elo: list[int] = []
    blacks_elo: list[int] = []
    time_controls: set[str] = set()
    for m in RE_HDR.finditer(raw):
        k, v = m.group(1), m.group(2)
        if k == "Result":
            results[v] = results.get(v, 0) + 1
        elif k == "White":
            whites.add(v)
        elif k == "Black":
            blacks.add(v)
        elif k == "WhiteElo":
            if v.isdigit():
                whites_elo.append(int(v))
        elif k == "BlackElo":
            if v.isdigit():
                blacks_elo.append(int(v))
        elif k == "TimeControl":
            time_controls.add(v)
    # Fallback: if n_games miscounted and we have results, use result count
    if n_games <= 0 and results:
        n_games = sum(results.values())
    hint = RE_ELO.search(path.name)
    return {
        "path": str(path),
        "name": path.name,
        "n_games": max(n_games, 0),
        "results": results,
        "whites": sorted(whites)[:10],
        "blacks": sorted(blacks)[:10],
        "whites_elo_range": [min(whites_elo), max(whites_elo)] if whites_elo else None,
        "blacks_elo_range": [min(blacks_elo), max(blacks_elo)] if blacks_elo else None,
        "time_controls": sorted(time_controls)[:5],
        "filename_elo_hint": int(hint.group(1)) if hint else None,
    }


def scan_perft(root: Path, max_per_file: int = 5_000_000) -> list[dict[str, Any]]:
    hits = []
    for dp, dns, fns in __import__("os").walk(root):
        dns[:] = [d for d in dns if d not in IGNORED_DIRS and not d.startswith(".")]
        for name in fns:
            if name.startswith("."):
                continue
            p = Path(dp) / name
            ext = p.suffix.lower()
            if ext in {".png", ".jpg", ".pdf", ".zip", ".tar", ".gz", ".bin", ".exe", ".o", ".so"}:
                continue
            try:
                if p.stat().st_size > max_per_file:
                    continue
                text = p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            for m in RE_PERFT.finditer(text):
                depth = m.group(1)
                val = m.group(2).replace(",", "").replace("_", "")
                hits.append({"file": str(p.relative_to(root)), "depth": int(depth), "value": val})
            if len(hits) >= 200:
                return hits
    return hits


def scan_project(project_dir: Path) -> dict[str, Any]:
    pgn_files = []
    for p in project_dir.rglob("*.pgn"):
        parts = set(p.parts)
        if IGNORED_DIRS & parts:
            continue
        meta = parse_pgn(p)
        if meta:
            pgn_files.append(meta)
    # Summarize by name hints
    gauntlet = [f for f in pgn_files if "gauntlet" in f["name"] or "tournament" in f["name"]]
    perft = scan_perft(project_dir)
    return {
        "n_pgn_files": len(pgn_files),
        "pgn_files": pgn_files[:80],
        "gauntlet_count": len(gauntlet),
        "perft_hits": perft,
    }


def main(argv: list[str]) -> None:
    projects_dir = DATA_DIR / "projects"
    all_targets = {name: path for name, path in discover_projects()}
    if argv:
        targets = [(a, all_targets.get(a) or (SANDBOX / a)) for a in argv]
    else:
        targets = list(all_targets.items())
    for logical, p in targets:
        if not p.exists():
            continue
        print(f"→ {logical}")
        data = scan_project(p)
        appendix = projects_dir / f"{logical}.json"
        if appendix.exists():
            prior = json.loads(appendix.read_text())
        else:
            prior = {"name": logical, "path": str(p)}
        prior["gameplay"] = data
        appendix.write_text(json.dumps(prior, indent=2, default=str))
        print(f"  pgn={data['n_pgn_files']} gauntlet={data['gauntlet_count']} perft_hits={len(data['perft_hits'])}")


if __name__ == "__main__":
    main(sys.argv[1:])
