"""Cross-check our per-engine Elo numbers against two prior sources:

  (1) the `chess-polyglot-eval` repository (metrics.json) --- an earlier
      evaluation run by the first author over a subset of 9 engines;
  (2) the Feb 2026 blog post tier list at
      blog.mathieuacher.com/FromScratchChessEnginesPolyglot/
      (transcribed by hand below, short quotes ≤ 25 words).

Output: reports/CONSISTENCY.md  --- a review aid, not a paper deliverable.
"""

from __future__ import annotations

import json
from pathlib import Path

from common import DATA_DIR, REPORTS_DIR, SANDBOX

POLYGLOT_METRICS = SANDBOX / "chess-polyglot-eval" / "metrics.json"

# Blog Feb 2026 tier list --- quoted numbers / bands from
# https://blog.mathieuacher.com/FromScratchChessEnginesPolyglot/
# The mapping to our logical project names is hand-curated.
BLOG_TIERS: dict[str, dict[str, str]] = {
    "chess-java-cc":     {"blog_name": "JavaCC",      "tier": "1", "elo": "~2200"},
    "chess-rust-cc":     {"blog_name": "RustCC",      "tier": "1", "elo": "~1950-2200"},
    "chess-purec":       {"blog_name": "PureC",       "tier": "1", "elo": "~1950-2200"},
    "chess-newlang-codex": {"blog_name": "CppCodex",  "tier": "1", "elo": "~1950-2200"},
    "chess-rust-codex":  {"blog_name": "RustCodex",   "tier": "1", "elo": "~1950-2200"},
    "chess-purec-codex": {"blog_name": "PureCCodex",  "tier": "1", "elo": "~1950-2200"},
    "chess-py":          {"blog_name": "ChessPy",     "tier": "1", "elo": "~1950-2200"},
    "chess-cplusplus-claude": {"blog_name": "Claudius", "tier": "2", "elo": "~1700-1900"},
    "chess-why3-cc":     {"blog_name": "Why3CC",      "tier": "2", "elo": "~1700-1900"},
    "chess-java":        {"blog_name": "JavaCodex",   "tier": "2", "elo": "~1700-1900"},
    "chess-py-cc":       {"blog_name": "PyCC",        "tier": "2", "elo": "~1700-1900"},
    "chess-why3":        {"blog_name": "Why3Codex",   "tier": "2", "elo": "~1530-1560"},
    "COBOL-chess":       {"blog_name": "CoboChess",   "tier": "2", "elo": "~1530-1560"},
    "chess-Rocq":        {"blog_name": "ChessRocq",   "tier": "3", "elo": "~1450"},
    "latex-chess-engine": {"blog_name": "TeXCCChess", "tier": "3", "elo": "~1280"},
    "chess-sql":         {"blog_name": "SQLChess",    "tier": "3", "elo": "~1120"},
    "chess-latex-codex-replication": {"blog_name": "TeXCodex", "tier": "3", "elo": "~900"},
}


def load_polyglot() -> dict[str, dict]:
    if not POLYGLOT_METRICS.exists():
        return {}
    data = json.loads(POLYGLOT_METRICS.read_text())
    out = {}
    for p in data:
        out[p["project"]] = p
    return out


def load_ours() -> tuple[dict, dict, dict]:
    overview = json.loads((DATA_DIR / "overview.json").read_text())
    overview_by_name = {o["name"]: o for o in overview}
    elo = json.loads((DATA_DIR / "elo.json").read_text()) if (DATA_DIR / "elo.json").exists() else {}
    # Collect enrichment agent-claimed band per project
    claims = {}
    proj_dir = DATA_DIR / "projects"
    for f in proj_dir.glob("*.json"):
        try:
            d = json.loads(f.read_text())
        except Exception:
            continue
        en = (d.get("enrichment") or {}).get("agent_elo_claims") or {}
        vals = [v for v in (en.get("values") or []) if 400 <= v <= 3500]
        if vals:
            claims[d["name"]] = {"min": min(vals), "max": max(vals), "count": len(vals)}
    return overview_by_name, elo, claims


def render_report() -> str:
    pg = load_polyglot()
    ov, elo, claims = load_ours()

    # Build a combined key set so we cover everything mentioned anywhere.
    keys = set(BLOG_TIERS) | set(pg)
    # Include engines we have elo data for as well.
    keys |= {k for k, v in elo.items() if (v.get("aggregate") or {}).get("elo_estimate") is not None}
    keys = sorted(keys)

    lines: list[str] = []
    lines.append("# Consistency report: paper vs. blog post vs. polyglot-eval")
    lines.append("")
    lines.append("_Comparison of the Elo numbers this paper reports against two prior evaluation runs by the first author:_")
    lines.append("- **Blog post (2026-02)**: `blog.mathieuacher.com/FromScratchChessEnginesPolyglot/`, tier-list numbers transcribed in `scripts/consistency_report.py`.")
    lines.append("- **polyglot-eval**: `~/SANDBOX/chess-polyglot-eval/metrics.json`, an earlier evaluation run over 9 engines.")
    lines.append("- **This paper**: per-engine PGN-derived Elo (inverse-variance aggregate) + agent-claimed Elo band mined from session transcripts.")
    lines.append("")
    lines.append("## Per-engine comparison")
    lines.append("")
    lines.append("| Engine | Lang. | Polyglot-eval Elo (method, N) | Blog tier / Elo | Ours: PGN Elo (N) | Ours: agent-claimed | Discrepancy note |")
    lines.append("|---|---|---|---|---|---|---|")
    discrepancies: list[tuple[str, str]] = []
    for name in keys:
        lang = (ov.get(name) or {}).get("primary_language") or (pg.get(name, {}).get("language", "—"))
        pg_entry = pg.get(name) or {}
        pg_elo = (pg_entry.get("elo") or {}).get("estimated_elo")
        pg_method = (pg_entry.get("elo") or {}).get("method", "")
        pg_n = (pg_entry.get("elo") or {}).get("games")
        blog = BLOG_TIERS.get(name, {})
        blog_cell = f"{blog.get('tier','')} / {blog.get('elo','')}" if blog else "—"
        our_entry = elo.get(name, {})
        our_agg = our_entry.get("aggregate") or {}
        our_elo = our_agg.get("elo_estimate")
        our_n = our_agg.get("n_games")
        our_cell = f"{int(our_elo)} (N={our_n})" if our_elo is not None else "—"
        claim = claims.get(name, {})
        claim_cell = f"{claim['min']}–{claim['max']} (n={claim['count']})" if claim else "—"
        pg_cell = f"{pg_elo} ({pg_method or '-'}, N={pg_n})" if pg_elo is not None else "—"
        # Compute a rough discrepancy note
        note = ""
        if our_elo and pg_elo and abs(our_elo - pg_elo) > 200:
            note = f"**Δ={int(our_elo - pg_elo):+d}** vs polyglot-eval"
            discrepancies.append((name, f"polyglot-eval={pg_elo} vs ours={int(our_elo)}"))
        elif our_elo and blog.get("elo") and "-" not in blog["elo"]:
            try:
                blog_mid = int(blog["elo"].replace("~", ""))
                if abs(our_elo - blog_mid) > 200:
                    note = f"**Δ={int(our_elo - blog_mid):+d}** vs blog"
                    discrepancies.append((name, f"blog~{blog_mid} vs ours={int(our_elo)}"))
            except Exception:
                pass
        lines.append(f"| {name} | {lang} | {pg_cell} | {blog_cell} | {our_cell} | {claim_cell} | {note} |")

    lines.append("")
    lines.append("## Discrepancies to investigate (|Δ| ≥ 200 Elo)")
    lines.append("")
    if not discrepancies:
        lines.append("_None._")
    for name, reason in discrepancies:
        lines.append(f"- `{name}`: {reason}")

    lines.append("")
    lines.append("## Likely causes of discrepancies")
    lines.append("")
    lines.append("1. **Different opponent ladders.** Our PGN-derived Elo aggregates only what survives in-tree; polyglot-eval used a deliberately-designed ladder (1320 / 1500 / 1700 / 1900 / 2100) at 120+1. The engine faced different mixes.")
    lines.append("2. **Time-control mismatch.** `UCI_LimitStrength` is calibrated for 120+1 (CCRL 40/4). Many of our surviving PGNs were played at 10+0.1 or 30+0.3; the Elo-vs-opponent mapping is not identical.")
    lines.append("3. **Inflated single-opponent wins.** When only one PGN survives (e.g.\\ `chess-java-cc` with a single 2200-level gauntlet in which the Java engine scored heavily), the logistic Elo estimate extrapolates far above the opponent's Elo --- a known artifact.")
    lines.append("4. **Evolving engines.** The blog snapshot is February 2026; several engines received further iterations between February and April. Our April numbers reflect the final state of the repository.")
    lines.append("")
    lines.append("## What to report in the paper")
    lines.append("")
    lines.append("- Cite the blog tier list as a prior estimate and report our own per-engine numbers alongside, flagging the method mismatch.")
    lines.append("- Commit to a **unified re-evaluation pass** (see `eval/README.md`) using the polyglot-eval opponent ladder at 120+1 for a single directly comparable Elo per engine.")
    lines.append("- Use the blog-quoted performance deltas (e.g.\\ ``C\\texttt{++} reaches depth 22--25 in 10s; COBOL depth 9; SQL depth 2'') as concrete evidence of the language-ceiling effect in §Discussion.")
    return "\n".join(lines) + "\n"


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "CONSISTENCY.md").write_text(render_report(), encoding="utf-8")
    print(f"Wrote reports/CONSISTENCY.md")


if __name__ == "__main__":
    main()
