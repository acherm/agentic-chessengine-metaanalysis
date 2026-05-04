"""Produce reports/FOLDER_TRIAGE.md --- an internal-review manifest of
every chess-related folder encountered, with in-/out-of-scope
classification and a human-readable reason.

This is a review aid, not a paper deliverable. The paper's corpus is
the `engine` + `engine-variant` buckets only.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import DATA_DIR, REPORTS_DIR, discover_projects

from synthesis import CLASSIFICATION


# Short per-project triage notes (reasons, manually curated).
TRIAGE_NOTES: dict[str, str] = {
    # engines
    "chess-apl-codex54": "APL engine (CC+Codex). Perft + gauntlet evidence.",
    "chess-assembly-codex": "x86 Assembly engine (Codex). ~12k LOC hand-written asm.",
    "chess-brainfuck": "BF engine via Python code-gen (Codex).",
    "chess-brainfuck-cc": "BF engine via Python code-gen (CC+Codex). ~100–200 Elo.",
    "chess-cobol-cc": "COBOL engine (CC). ~$518 spend, ~1600 Elo claim.",
    "COBOL-chess": "Second COBOL engine (CC), cobochess. Full UCI + perft + cutechess harness. (The vendored cutechess-cli source tree is now excluded from LOC counts.)",
    "chess-revisit-java-toCOBOL-codex": "Port experiment (engine-port): Codex translates chess-java-cc to GNU COBOL. Different protocol from scratch builds; reported separately in paper.",
    "chess-cplusplus-claude": "C++ engine (CC).",
    "cplusplus-chess": "C++ engine with CMake + perft (CC).",
    "chess-css-codex": "CSS engine (Codex). Evasion-risk case: initial sessions used python-chess under the hood; after qualitative review the first author redirected the agent to produce a strict-CSS variant under strict-css/. Documented as an RQ3 case.",
    "chess-css-codex-guided": "Small pure-HTML+CSS+JS experiment (Codex, 4 files) with legal move generation and perft 1--3. Separate repository from chess-css-codex; used as a second Codex try on the same premise.",
    "chess-css-x86": "CSS/HTML variant superseded by chess-css-codex --- user removed from engine corpus.",
    "chess-icon-codex": "Icon-language engine (Codex).",
    "chess-java": "Java engine (Codex).",
    "chess-java-cc": "Java engine (CC). Surprising 2600-range Elo in PGN; flagged for re-eval.",
    "chess-latex-codex-replication": "LaTeX replication attempt (Codex). ~800 Elo MLE.",
    "latex-chess-engine": "TeXCCChess --- canonical pure-TeX engine (CC). Claims ``first chess engine in pure TeX'' at ~1300 Elo.",
    "lean-chess": "Lean 4 engine with perft harness (CC).",
    "chess-mojo": "Failure case (engine-failure): Codex produced a Mojo UCI scaffold + perft + alpha-beta search but the engine plateaued at $\\approx$900 Elo and did not converge to a competitive pipeline. Included for transparency, excluded from main analysis tables.",
    "test-superset": "Co-design experiment (engine-codesign): ChessCSS --- a 55k-rule, ~17MB pure-CSS chess engine built in 31 commits over 5 days (2026-02-27 to 2026-03-03). The agent (Claude Code) progressively replaced JavaScript logic with CSS rules (:has() selectors, CSS if(), z-index argmax + elementFromPoint for move selection). The engine's README explicitly notes the author had to 'drive the agent with technical expertise ... and encourage the agents to not giving up with CSS' --- that is, the session protocol differs from the corpus's minimal-instruction default. Reported separately from the main corpus for that reason; treated as a cousin to the ports/DSL/failure special-role bucket.",
    "chess-newlang-codex": "DSL experiment (engine-dsl): Codex designs the GAMBIT DSL (.gmb) and its C++17 transpiler; engine runs via generated C++. Reported separately in paper.",
    "chess-purec": "Plain-C engine (CC). ~2100 Elo.",
    "chess-purec-codex": "Plain-C engine (Codex). ~1800 Elo.",
    "chess-py": "Python engine (Codex).",
    "chess-py-cc": "Python engine (CC); main transcript archived, subagent logs only.",
    "chess-revisit-java-toRust-codex": "Port experiment (engine-port): Codex translates chess-java-cc to Rust. Different protocol from scratch builds; reported separately in paper.",
    "chess-Rocq": "Rocq/Coq specification extracted to OCaml (CC).",
    "chess-ruby-cc": "Ruby engine (CC). ~1840 Elo on 420 rated games.",
    "chess-ruby-codex": "Ruby engine (Codex). Less rigorous gauntlets.",
    "chess-rust-cc": "Rust engine (CC). ~2100 Elo; transcript largely archived.",
    "chess-rust-codex": "Rust engine (Codex). ~1750 Elo.",
    "chess-sql": "SQL engine (CC).",
    "chess-why3": "Why3 engine extracted to OCaml (Codex).",
    "chess-why3-cc": "Why3 engine with C extraction (CC). ~2000 Elo.",
    # variants
    "minichess-5x5-repro": "Gardner 5x5 minichess weak-solver (Rust). Variant game, not standard 8x8 chess --- user removed from engine corpus.",
    "minichess-5x5-repro-cc": "Gardner 5x5 minichess (CC). Same --- removed.",
    # OOS
    "chess-brainfuck-gpt54-instant": "Trivial 3-LOC one-shot experiment; not a working engine.",
    "chess-printf": "Printf-only experiment (CC). User removed from scope.",
    "chess-printf-codex": "Printf-only experiment (Codex). User removed from scope.",
    "chesspuzzle-tex-codex": "PGN → TeX puzzle renderer; not an engine.",
    "puzzles-chess": "Puzzle/SVG renderer; not an engine.",
    "chess-fem": "Feature-engineering study of FIDE/LLM play; not an engine.",
    "chess-in-conway": "Chess-inside-Conway's-Life simulation; not an engine.",
    "chess-conway": "Chess/Conway exploration; not an engine.",
    "chess-kasparov-claim": "Study of Kasparov-claim narrative; analytical not constructive.",
    "chess-kasparov-claim-bis": "Follow-up study of Kasparov-claim.",
    "chess-lean-vibe": "Empty Lean prototype.",
    "chess-llmtraining": "LLM fine-tuning research, not an engine built by the agent.",
    "chess-excel": "Excel-based board, no search pipeline.",
    "chess-polyglot-eval": "Tournament harness that runs multiple engines; tool, not engine.",
    "chessball": "Chess×football variant; out of scope for chess engines.",
    "chessfoo": "Sandbox exploration (JavaScript).",
    "chessfoo-claude": "TypeScript port of chessfoo; exploration.",
    "chessprogramming-vm": "Cloned third-party corpus of classical engines, not agent-built.",
    "gptchess": "Prior-published GPT-chess study by M. Acher; not an agent-built engine.",
    "Chess1MChallenge": "Hugging Face arena (Gradio) for a course-style LLM chess challenge; not an agent-built engine.",
}


def main() -> None:
    projects = discover_projects()
    ov_path = DATA_DIR / "overview.json"
    ov = {o["name"]: o for o in json.loads(ov_path.read_text())} if ov_path.exists() else {}
    lines: list[str] = []
    lines.append("# Folder triage (internal review)")
    lines.append("")
    lines.append(f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_")
    lines.append("")
    lines.append("Every chess-related folder under `~/SANDBOX` is listed here with its in-/out-of-scope classification and a one-line rationale. The paper's corpus is the **engine** + **engine-variant** buckets.")
    lines.append("")
    # Count buckets
    buckets: dict[str, int] = {}
    for logical, _ in projects:
        b = CLASSIFICATION.get(logical, "unknown")
        buckets[b] = buckets.get(b, 0) + 1
    lines.append("## Counts by bucket")
    lines.append("")
    lines.append("| Bucket | Folders |")
    lines.append("|---|---:|")
    for b in sorted(buckets):
        lines.append(f"| `{b}` | {buckets[b]} |")
    lines.append(f"| **Total discovered** | **{len(projects)}** |")
    lines.append("")
    lines.append("## Per-folder triage")
    lines.append("")
    lines.append("| Folder | Bucket | Primary lang. | LOC | Sessions | Note |")
    lines.append("|---|---|---|---:|---:|---|")
    for logical, path in sorted(projects):
        b = CLASSIFICATION.get(logical, "unknown")
        o = ov.get(logical, {})
        lang = o.get("primary_language") or "—"
        loc = o.get("loc", {}).get("total_loc", 0)
        sessions = (o.get("claude", {}).get("n_sessions") or 0) + (o.get("codex", {}).get("n_sessions") or 0)
        note = TRIAGE_NOTES.get(logical, "")
        lines.append(f"| `{logical}` | `{b}` | {lang} | {loc:,} | {sessions} | {note} |")
    lines.append("")
    lines.append("## Scope rules")
    lines.append("")
    lines.append("- **engine** — a chess-playing system built by a frontier agent; plays standard 8×8 chess.")
    lines.append("- **engine-variant** — engine for a non-standard variant (Gardner 5×5 minichess in our corpus).")
    lines.append("- **oos-…** — out of scope. Subtypes: `tool` (renderers, harnesses), `study` (observational papers), `exploration` (unfinished prototypes), `prior-work` (predates the agent era or is the user's own published research), `training-research` (LLM fine-tuning), `variant-game` (not chess), `external-corpus` (cloned third-party engines).")
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "FOLDER_TRIAGE.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote reports/FOLDER_TRIAGE.md ({len(projects)} folders)")


if __name__ == "__main__":
    main()
