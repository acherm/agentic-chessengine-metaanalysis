"""Emit reports/ENGINES.md --- a clean, self-contained manifest of every
chess engine in the corpus, designed to be handed to another session
(e.g. a Claude Code session refining the eval infrastructure).

The manifest pulls from:
  - data/overview.json           primary-language, LOC, agent, period, USD
  - data/elo.json                PGN-derived Elo per engine
  - data/projects/<name>.json    agent-claimed Elo band, tests/perft, novelty
  - eval/build_plan.py::DEFAULTS build/run command defaults per engine
  - reports/CONSISTENCY.md       prior-source Elo numbers where available
  - synthesis.py::CLASSIFICATION the taxonomy bucket per engine

Downstream audience: the canonical eval harness and anyone scripting
gauntlets/round-robins over the corpus. The Markdown is intended to be
read standalone.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
DATA = REPO / "data"
REPORTS = REPO / "reports"
EVAL = REPO / "eval"

sys.path.insert(0, str(HERE))
from synthesis import CLASSIFICATION  # type: ignore
from build_paper_tables import DISPLAY_LANG  # type: ignore

# Import the eval defaults so build/cmd stay in sync.
sys.path.insert(0, str(EVAL))
try:
    import build_plan  # type: ignore
    ENGINE_DEFAULTS = build_plan.DEFAULTS
except Exception:
    ENGINE_DEFAULTS = {}


# Human-facing category label per classification bucket.
CATEGORY_LABEL = {
    "engine": "Main corpus",
    "engine-port": "Java$\\to$language port",
    "engine-dsl": "DSL-design + transpile",
    "engine-failure": "Unconverged",
    "engine-codesign": "Agent-heavy co-design",
}

# Prior-source Elo transcribed from scripts/consistency_report.py (kept
# synchronized when the consistency script is regenerated).
PRIOR_ELO = {
    "chess-purec": {"polyglot": 2210, "blog": "Tier 1 ~1950-2200"},
    "chess-rust-cc": {"polyglot": None, "blog": "Tier 1 ~1950-2200"},
    "chess-rust-codex": {"polyglot": None, "blog": "Tier 1 ~1950-2200"},
    "chess-purec-codex": {"polyglot": None, "blog": "Tier 1 ~1950-2200"},
    "chess-java-cc": {"polyglot": None, "blog": "Tier 1 ~2200"},
    "chess-py": {"polyglot": None, "blog": "Tier 1 ~1950-2200"},
    "chess-cplusplus-claude": {"polyglot": 1835, "blog": "Tier 2 ~1700-1900"},
    "chess-why3-cc": {"polyglot": None, "blog": "Tier 2 ~1700-1900"},
    "chess-java": {"polyglot": None, "blog": "Tier 2 ~1700-1900"},
    "chess-py-cc": {"polyglot": None, "blog": "Tier 2 ~1700-1900"},
    "chess-why3": {"polyglot": None, "blog": "Tier 2 ~1530-1560"},
    "COBOL-chess": {"polyglot": 1598, "blog": "Tier 2 ~1530-1560"},
    "chess-Rocq": {"polyglot": 1575, "blog": "Tier 3 ~1450"},
    "latex-chess-engine": {"polyglot": 1292, "blog": "Tier 3 ~1280"},
    "chess-sql": {"polyglot": 1019, "blog": "Tier 3 ~1120"},
    "chess-latex-codex-replication": {"polyglot": None, "blog": "Tier 3 ~900"},
    "lean-chess": {"polyglot": 1484, "blog": None},
    "cplusplus-chess": {"polyglot": 2044, "blog": None},
    "chess-newlang-codex": {"polyglot": None, "blog": "Tier 1 ~1950-2200"},
}


def load_overview() -> dict[str, dict]:
    return {o["name"]: o for o in json.loads((DATA / "overview.json").read_text())}


def load_elo() -> dict:
    p = DATA / "elo.json"
    return json.loads(p.read_text()) if p.exists() else {}


def load_project(name: str) -> dict:
    p = DATA / "projects" / f"{name}.json"
    return json.loads(p.read_text()) if p.exists() else {}


def agent_short(ov: dict) -> str:
    c = ov["claude"]["n_sessions"] > 0
    x = ov["codex"]["n_sessions"] > 0
    if c and x:
        return "CC+Codex"
    if c:
        return "CC"
    if x:
        return "Codex"
    n = ov["name"].lower()
    if "codex" in n:
        return "Codex (by name)"
    if "-cc" in n or "claude" in n:
        return "CC (by name)"
    return "—"


def model_family(ov: dict) -> str:
    fams = set()
    for m in (ov["claude"]["models"] or []) + (ov["codex"]["models"] or []):
        ml = (m or "").lower()
        if "opus-4-7" in ml: fams.add("Opus 4.7")
        elif "opus-4-6" in ml: fams.add("Opus 4.6")
        elif "opus" in ml: fams.add("Opus 4.x")
        elif "sonnet" in ml: fams.add("Sonnet 4.x")
        elif "haiku" in ml: fams.add("Haiku 4.x")
        elif "gpt-5-codex" in ml: fams.add("gpt-5-codex")
        elif "gpt-5.3-codex" in ml: fams.add("gpt-5.3-codex")
        elif "gpt-5.4" in ml: fams.add("gpt-5.4")
        elif "gpt-5" in ml: fams.add("gpt-5")
        elif m and not m.startswith("<"): fams.add(m)
    return ", ".join(sorted(fams)) or "—"


def display_language(ov: dict) -> str:
    """Plain-Markdown language string (no LaTeX)."""
    name = ov["name"]
    tex = DISPLAY_LANG.get(name, ov.get("primary_language") or "—")
    # Strip LaTeX escapes for Markdown output
    return (
        tex.replace("$\\to$", "→")
        .replace("$\\times$", "×")
        .replace("\\texttt{", "")
        .replace("}", "")
        .replace("\\", "")
    )


def elo_cell(name: str, elo_idx: dict, pr: dict) -> str:
    agg = (elo_idx.get(name, {}).get("aggregate") or {})
    est = agg.get("elo_estimate")
    ci = agg.get("ci95")
    n = agg.get("n_games", 0)
    claims = pr.get("enrichment", {}).get("agent_elo_claims", {}).get("values", []) or []
    claims = [v for v in claims if 400 <= v <= 3500]
    parts = []
    if est is not None:
        parts.append(f"PGN: {int(est)}±{ci} (N={n})")
    if claims:
        cmin, cmax = min(claims), max(claims)
        parts.append(f"claimed: {cmin}{'–'+str(cmax) if cmin!=cmax else ''}")
    prior = PRIOR_ELO.get(name, {})
    if prior.get("polyglot") is not None:
        parts.append(f"polyglot-eval: {prior['polyglot']}")
    if prior.get("blog"):
        parts.append(f"blog: {prior['blog']}")
    return "; ".join(parts) or "—"


def evidence_cell(name: str, elo_idx: dict, pr: dict) -> str:
    n_games = (elo_idx.get(name, {}).get("aggregate") or {}).get("n_games", 0) or 0
    gp = pr.get("gameplay", {})
    pgns = gp.get("n_pgn_files", 0)
    perft = len(gp.get("perft_hits", []) or [])
    tests = (pr.get("enrichment", {}).get("test_evidence", {}) or {}).get("n_test_files", 0)
    return f"{n_games} rated games, {pgns} PGN files, {perft} perft hits, {tests} test files"


def novelty_cell(pr: dict) -> str:
    n = pr.get("novelty") or {}
    cls = n.get("classification", "—")
    deps = n.get("manifest_chess_libs") or []
    imps = n.get("source_chess_imports") or []
    fps = n.get("canonical_fingerprints") or []
    notes = []
    if deps: notes.append("deps=" + ",".join(deps))
    if imps: notes.append("core-imports=" + ",".join(imps))
    if fps:  notes.append("fingerprints=" + ",".join(fps))
    return cls + (": " + "; ".join(notes) if notes else "")


def render_row(name: str, ov: dict, elo_idx: dict) -> str:
    pr = load_project(name)
    defaults = ENGINE_DEFAULTS.get(name, {})
    cmd = defaults.get("cmd", "# TODO")
    build = defaults.get("build", "") or "—"
    notes = defaults.get("notes", "")
    agent = agent_short(ov)
    models = model_family(ov)
    period_s = (ov.get("period", {}).get("start") or "")[:10]
    period_e = (ov.get("period", {}).get("end") or "")[:10]
    period = f"{period_s} → {period_e}" if period_s else "—"
    prompts = (ov["claude"]["n_user_prompts"] or 0) + (ov["codex"]["n_user_prompts"] or 0)
    usd = ov.get("total_usd_estimate", 0) or 0
    loc = ov["loc"]["total_loc"]
    files = ov["loc"]["total_files"]
    lang = display_language(ov)
    elo = elo_cell(name, elo_idx, pr)
    ev = evidence_cell(name, elo_idx, pr)
    novelty = novelty_cell(pr)
    return (
        f"### {name}\n"
        f"- **Language:** {lang}\n"
        f"- **Agent / model:** {agent} · {models}\n"
        f"- **Period:** {period}\n"
        f"- **Path:** `{ov['path']}`\n"
        f"- **Size:** {files} files, {loc:,} LOC; {prompts} user prompts; ${usd:.2f} est.\n"
        f"- **Build:** `{build}`\n"
        f"- **UCI launch:** `{cmd}` (run from the engine path)\n"
        f"- **Current Elo evidence:** {elo}\n"
        f"- **Game/test evidence:** {ev}\n"
        f"- **Novelty classification:** {novelty}\n"
        + (f"- **Notes:** {notes}\n" if notes else "")
    )


def main() -> None:
    ov_idx = load_overview()
    elo_idx = load_elo()

    # Gather engines by category (main corpus, then special-role).
    by_cat: dict[str, list[str]] = {"engine": [], "engine-port": [], "engine-dsl": [], "engine-failure": [], "engine-codesign": []}
    for name in ov_idx:
        bucket = CLASSIFICATION.get(name)
        if bucket in by_cat:
            by_cat[bucket].append(name)
    for cat in by_cat:
        by_cat[cat].sort(key=lambda n: (display_language(ov_idx[n]), n))

    lines: list[str] = []
    lines.append("# Agent-built chess engines --- canonical manifest")
    lines.append("")
    lines.append(f"_Generated by `scripts/engines_manifest.py`. Keep in sync by re-running discovery + enrichment before handing off._")
    lines.append("")
    lines.append("This file lists every chess engine we consider, grouped by study role. The intended consumer is a downstream session that refines the Elo evaluation harness under `eval/`. Each row gives the primary language, the coding agent + model family, the repository path, the build and UCI-launch commands, the current best Elo evidence (from this corpus plus prior runs), and the novelty classification from the RQ3 audit. Out-of-scope folders (tools, studies, external corpora, variants) live in `FOLDER_TRIAGE.md` and are not repeated here.")
    lines.append("")

    # Summary table at the top for quick scanning.
    lines.append("## Summary table")
    lines.append("")
    lines.append("| Engine | Language | Agent | LOC | Prompts | USD | Best Elo evidence | Cat. |")
    lines.append("|---|---|---|---:|---:|---:|---|---|")
    for cat in ("engine", "engine-port", "engine-dsl", "engine-failure", "engine-codesign"):
        for name in by_cat[cat]:
            ov = ov_idx[name]
            pr = load_project(name)
            prompts = (ov["claude"]["n_user_prompts"] or 0) + (ov["codex"]["n_user_prompts"] or 0)
            usd = ov.get("total_usd_estimate", 0) or 0
            elo = elo_cell(name, elo_idx, pr)
            cat_lbl = {"engine": "main", "engine-port": "port", "engine-dsl": "DSL",
                       "engine-failure": "failure", "engine-codesign": "co-design"}[cat]
            lines.append(
                f"| `{name}` | {display_language(ov)} | {agent_short(ov)} | "
                f"{ov['loc']['total_loc']:,} | {prompts} | ${usd:.2f} | "
                f"{elo} | {cat_lbl} |"
            )
    lines.append("")

    # Full per-engine blocks, grouped by category.
    for cat in ("engine", "engine-port", "engine-dsl", "engine-failure", "engine-codesign"):
        if not by_cat[cat]:
            continue
        label = {
            "engine": "Main corpus (from-scratch designs)",
            "engine-port": "Special role: Java → language ports",
            "engine-dsl": "Special role: DSL design + transpile",
            "engine-failure": "Special role: unconverged attempts",
            "engine-codesign": "Special role: agent-heavy co-design",
        }[cat]
        lines.append(f"## {label}")
        lines.append("")
        for name in by_cat[cat]:
            ov = ov_idx[name]
            lines.append(render_row(name, ov, elo_idx))

    # Notes for the downstream session.
    lines.append("## Notes for the evaluation harness")
    lines.append("")
    lines.append("- **Time control.** Default is 120+1 (CCRL 40/4 anchor); see `eval/README.md`. Slower engines (LaTeX, Brainfuck, COBOL) may need a move-time fallback (`st=10` or longer); document overrides per engine in `eval/engines.yaml`.")
    lines.append("- **Weak-engine tier.** Engines that score $\\leq 1/20$ at the lowest Stockfish rung (UCI\\_Elo 800) should be demoted to a round-robin among themselves plus a random-legal-move baseline. Current suspects: Brainfuck (both), chess-mojo (failure), chess-latex-codex-replication.")
    lines.append("- **Single-opponent inflation.** `chess-java-cc` currently shows ~2600 PGN Elo from a single 2200-rated gauntlet; a full ladder sweep at 120+1 is required to confirm or refute. The blog's Tier-1 (~2200) is the prior.")
    lines.append("- **Evasion-risk.** `chess-css-codex` uses python-chess inside `src/chess_css/engine.py`; the `strict-css/` subdirectory is the user-requested compliant variant. The harness should launch the strict variant when \"CSS engine\" is evaluated, not the original.")
    lines.append("- **Special-role engines follow different protocols.** Port/DSL/failure experiments are reported in their own paper section and should not be pooled with the main corpus for any averaged metric.")
    lines.append("- **Prior evaluations are anchors.** `chess-polyglot-eval/metrics.json` and the 2026-02 blog post give priors for roughly half the main corpus; see `reports/CONSISTENCY.md` for per-engine deltas and likely causes.")
    lines.append("")
    lines.append("## Regenerating this file")
    lines.append("")
    lines.append("```bash")
    lines.append("cd ~/SANDBOX/chess-meta-analysis")
    lines.append("python3 scripts/discover.py")
    lines.append("python3 scripts/elo_and_perft.py")
    lines.append("python3 scripts/extract_elo.py")
    lines.append("python3 scripts/enrich_projects.py")
    lines.append("python3 scripts/novelty_analysis.py")
    lines.append("python3 scripts/engines_manifest.py   # this file")
    lines.append("```")

    out = REPORTS / "ENGINES.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    total = sum(len(by_cat[c]) for c in by_cat)
    print(f"Wrote {out}  ({total} engines: {len(by_cat['engine'])} main, "
          f"{len(by_cat['engine-port'])} port, {len(by_cat['engine-dsl'])} DSL, "
          f"{len(by_cat['engine-failure'])} failure, "
          f"{len(by_cat['engine-codesign'])} co-design)")


if __name__ == "__main__":
    main()
