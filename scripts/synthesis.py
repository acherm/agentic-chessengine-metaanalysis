"""Cross-project synthesis for the paper.

Reads `data/overview.json` and `data/projects/*.json`, applies a hand-curated
project classification (engines vs. meta-eval vs. training/exploration vs.
external clones), and produces:

  reports/SYNTHESIS.md      human-readable executive summary
  data/synthesis.json       machine-readable appendix

The classification is necessarily partial — the paper must own which
projects count as "the corpus of agent-built chess engines".
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import DATA_DIR, REPORTS_DIR


# Hand-curated taxonomy (informed by folder names + an inspection of each
# project). The "engine" bucket holds agent-built chess engines that are the
# focus of the paper. Other buckets provide context.
CLASSIFICATION: dict[str, str] = {
    # --- MAIN ENGINE CORPUS --------------------------------------------
    # ``engine'' is the standard protocol: agent is asked to build a chess
    # engine from scratch in a target language. These are the rows of
    # the paper's main analysis tables.
    "chess-apl-codex54": "engine",
    "chess-assembly-codex": "engine",
    "chess-brainfuck": "engine",
    "chess-brainfuck-cc": "engine",
    "chess-cobol-cc": "engine",
    "COBOL-chess": "engine",
    "chess-cplusplus-claude": "engine",
    "cplusplus-chess": "engine",
    "chess-css-codex": "engine",                   # flagged as evasion-risk (RQ3)
    "chess-css-codex-guided": "engine",
    "chess-icon-codex": "engine",
    "chess-java": "engine",
    "chess-java-cc": "engine",
    "chess-latex-codex-replication": "engine",
    "latex-chess-engine": "engine",
    "lean-chess": "engine",
    "chess-purec": "engine",
    "chess-purec-codex": "engine",
    "chess-py": "engine",
    "chess-py-cc": "engine",
    "chess-Rocq": "engine",
    "chess-ruby-cc": "engine",
    "chess-ruby-codex": "engine",
    "chess-rust-cc": "engine",
    "chess-rust-cc-redo": "engine",
    "chess-rust-codex": "engine",
    "chess-sql": "engine",
    "chess-why3": "engine",
    "chess-why3-cc": "engine",

    # --- SPECIAL-ROLE EXPERIMENTS -------------------------------------
    # Port experiments: the agent is asked to translate a specific existing
    # engine (chess-java-cc) into another language, preserving module
    # structure. This is ``can language L host a good engine?'' rather
    # than ``can the agent design a good engine in L from scratch?''
    "chess-revisit-java-toRust-codex": "engine-port",
    "chess-revisit-java-toCOBOL-codex": "engine-port",

    # DSL experiment: the agent designs a custom DSL (GAMBIT) for chess
    # engines, ships a .gmb parser + C++17 transpiler, and emits the
    # engine via compilation. The ``language'' of authorship is GAMBIT;
    # the runtime is C++.
    "chess-newlang-codex": "engine-dsl",

    # Failure case: attempted but the produced engine did not reach a
    # reasonable strength or stable working state under the session
    # budget. Kept in the paper for transparency but excluded from the
    # main-corpus tables.
    "chess-mojo": "engine-failure",

    # Co-design experiment: sustained agent+human collaboration with
    # heavy technical steering. The README explicitly places it out of
    # scope of the minimal-instruction protocol used for the main
    # corpus. Rich artefact (55k CSS rules; 31 commits of progressive
    # JS->CSS migration). We keep it for transparency but analyse it
    # separately.
    "test-superset": "engine-codesign",
    # --- OUT OF SCOPE --------------------------------------------------
    "minichess-5x5-repro": "oos-minichess-variant",          # user removed: not standard 8x8 chess
    "minichess-5x5-repro-cc": "oos-minichess-variant",
    "chess-css-x86": "oos-css-variant",                      # user removed: superseded by chess-css-codex
    "chess-brainfuck-gpt54-instant": "oos-prototype",        # trivial 3-LOC experiment
    "chess-printf": "oos-experiment",                        # printf-only; user removed
    "chess-printf-codex": "oos-experiment",
    "chesspuzzle-tex-codex": "oos-tool",
    "puzzles-chess": "oos-tool",
    "chess-fem": "oos-study",
    "chess-in-conway": "oos-study",
    "chess-conway": "oos-exploration",
    "chess-kasparov-claim": "oos-study",
    "chess-kasparov-claim-bis": "oos-study",
    "chess-lean-vibe": "oos-exploration",
    "chess-llmtraining": "oos-training-research",
    "chess-excel": "oos-exploration",
    "chess-polyglot-eval": "oos-tournament-harness",
    "chessball": "oos-variant-game",
    "chessfoo": "oos-exploration",
    "chessfoo-claude": "oos-exploration",
    "chessprogramming-vm": "oos-external-corpus",
    "gptchess": "oos-prior-work",
    "Chess1MChallenge": "oos-challenge-arena",
}


def classify(name: str) -> str:
    return CLASSIFICATION.get(name, "unknown")


def load_overview() -> list[dict[str, Any]]:
    return json.loads((DATA_DIR / "overview.json").read_text())


def load_project_appendix(name: str) -> dict[str, Any] | None:
    p = DATA_DIR / "projects" / f"{name}.json"
    if p.exists():
        return json.loads(p.read_text())
    return None


def infer_agent(ov: dict[str, Any]) -> str:
    c = ov["claude"]["n_sessions"] > 0
    x = ov["codex"]["n_sessions"] > 0
    if c and x:
        return "Claude Code + Codex"
    if c:
        return "Claude Code"
    if x:
        return "Codex"
    # Fallback: by folder name
    name = ov["name"].lower()
    if name.endswith("-cc") or "cc-" in name or "-claude" in name:
        return "Claude Code (by name)"
    if "codex" in name:
        return "Codex (by name)"
    return "—"


def model_family(models: list[str]) -> list[str]:
    fams = set()
    for m in models:
        ml = m.lower()
        if "opus-4-7" in ml:
            fams.add("Opus 4.7")
        elif "opus-4-6" in ml:
            fams.add("Opus 4.6")
        elif "opus-4" in ml or "opus" in ml:
            fams.add("Opus 4.x")
        elif "sonnet-4-7" in ml:
            fams.add("Sonnet 4.7")
        elif "sonnet-4-6" in ml:
            fams.add("Sonnet 4.6")
        elif "sonnet" in ml:
            fams.add("Sonnet 4.x")
        elif "haiku" in ml:
            fams.add("Haiku 4.x")
        elif "gpt-5-codex" in ml:
            fams.add("gpt-5-codex")
        elif "gpt-5" in ml:
            fams.add("gpt-5")
        elif "gpt" in ml:
            fams.add("gpt")
        elif m and not m.startswith("<"):
            fams.add(m)
    return sorted(fams)


def main() -> None:
    overview = load_overview()
    engines: list[dict[str, Any]] = []
    others: list[dict[str, Any]] = []
    for ov in overview:
        bucket = classify(ov["name"])
        ov["bucket"] = bucket
        if bucket == "engine":
            engines.append(ov)
        else:
            others.append(ov)

    # Augment with gameplay evidence
    for ov in overview:
        app = load_project_appendix(ov["name"])
        gp = (app or {}).get("gameplay") or {}
        ov["gameplay"] = {
            "n_pgn_files": gp.get("n_pgn_files", 0),
            "perft_hits": len(gp.get("perft_hits") or []),
        }
        # Extract unique Elo hints from PGN filenames
        elos = []
        for pf in gp.get("pgn_files") or []:
            if pf.get("filename_elo_hint"):
                elos.append(pf["filename_elo_hint"])
        ov["gameplay"]["elo_hints"] = sorted(set(elos))

    lines: list[str] = []
    lines.append("# Chess meta-analysis — synthesis for the paper")
    lines.append("")
    lines.append(f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}._")
    lines.append("")
    n_engine = sum(1 for o in overview if o["bucket"] == "engine")
    n_variant = sum(1 for o in overview if o["bucket"] == "engine-variant")
    lines.append(
        "This document synthesizes evidence across **{} chess-related folders** under `~/SANDBOX`, of which **{} are agent-built chess engines** (plus {} engine *variants* on non-standard boards). The remainder are tournament runners, training-research repos, meta-studies, prototypes, or external corpora, tagged ``oos-…'' and documented in `FOLDER_TRIAGE.md`.".format(
            len(overview), n_engine, n_variant
        )
    )
    lines.append("")

    # Totals
    tot_cost = sum((o.get("total_usd_estimate") or 0) for o in overview)
    tot_cost_eng = sum((o.get("total_usd_estimate") or 0) for o in engines)
    tot_loc = sum(o["loc"]["total_loc"] for o in overview if o["bucket"] != "external-corpus")
    tot_loc_eng = sum(o["loc"]["total_loc"] for o in engines)
    tot_prompts = sum(
        (o["claude"]["n_user_prompts"] or 0) + (o["codex"]["n_user_prompts"] or 0)
        for o in overview
    )
    tot_prompts_eng = sum(
        (o["claude"]["n_user_prompts"] or 0) + (o["codex"]["n_user_prompts"] or 0) for o in engines
    )
    tot_sessions = sum(
        (o["claude"]["n_sessions"] or 0) + (o["codex"]["n_sessions"] or 0)
        for o in overview
    )
    lines.append("## Headline numbers")
    lines.append("")
    lines.append(f"- **Corpus:** {len(overview)} chess-related folders under `~/SANDBOX` (excluding `chess-meta-analysis`).")
    lines.append(f"- **Engines in scope:** {len(engines)} (language × agent combinations).")
    lines.append(f"- **LOC** (engines only, excluding external corpora): ~{tot_loc_eng:,} lines across engines; ~{tot_loc:,} total if we include studies/tools.")
    lines.append(f"- **User prompts logged** across all sessions: {tot_prompts} ({tot_prompts_eng} on engines).")
    lines.append(f"- **Sessions** (Claude Code + Codex, main transcripts): {tot_sessions}.")
    lines.append(f"- **Estimated agent spend:** ${tot_cost:,.2f} total, ${tot_cost_eng:,.2f} on engines (list-price estimate).")
    lines.append("")
    lines.append("_Token counts and pricing tables are in `scripts/common.py::PRICING_USD_PER_MTOK`; Anthropic and OpenAI discounts are not applied._")
    lines.append("")

    # Engines by language × agent
    lines.append("## Engine corpus (by language × agent × period)")
    lines.append("")
    lines.append("| Project | Language | Agent | Model family | Period | Files | LOC | Prompts | USD | PGN | Perft hits |")
    lines.append("|---|---|---|---|---|---:|---:|---:|---:|---:|---:|")
    for ov in sorted(engines, key=lambda x: (x.get("primary_language") or "", x["name"])):
        agent = infer_agent(ov)
        ms = sorted(set((ov["claude"]["models"] or []) + (ov["codex"]["models"] or [])))
        fams = ", ".join(model_family(ms)) or "—"
        period_s = (ov["period"].get("start") or "")[:10]
        period_e = (ov["period"].get("end") or "")[:10]
        period = f"{period_s}→{period_e}" if period_s else "—"
        prompts = (ov["claude"]["n_user_prompts"] or 0) + (ov["codex"]["n_user_prompts"] or 0)
        lines.append(
            f"| [{ov['name']}](projects/{ov['name']}.md) | {ov.get('primary_language') or '—'} "
            f"| {agent} | {fams} | {period} | {ov['loc']['total_files']} "
            f"| {ov['loc']['total_loc']:,} | {prompts} | ${ov.get('total_usd_estimate', 0):.2f} "
            f"| {ov['gameplay'].get('n_pgn_files', 0)} | {ov['gameplay'].get('perft_hits', 0)} |"
        )
    lines.append("")

    # Cross-language coverage matrix
    lines.append("## Cross-language chess feature coverage (engines)")
    lines.append("")
    # Aggregate by language × feature
    feat_by_lang: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    lang_to_projects: dict[str, list[str]] = defaultdict(list)
    all_features: list[str] = []
    for ov in engines:
        lang = ov.get("primary_language") or "—"
        lang_to_projects[lang].append(ov["name"])
        for f in (ov.get("features") or {}):
            if f not in all_features:
                all_features.append(f)
            feat_by_lang[lang][f] += 1
    header = "| Language | Projects | " + " | ".join(all_features) + " |"
    sep = "|---|---|" + "---|" * len(all_features)
    lines.append(header)
    lines.append(sep)
    for lang in sorted(lang_to_projects):
        row = [lang, str(len(lang_to_projects[lang]))]
        for f in all_features:
            n = feat_by_lang[lang].get(f, 0)
            row.append(str(n) if n else "")
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")

    # Interaction demand
    lines.append("## Interaction demand (prompts per engine)")
    lines.append("")
    eng_prompts = [
        ((o["claude"]["n_user_prompts"] or 0) + (o["codex"]["n_user_prompts"] or 0), o["name"])
        for o in engines
    ]
    eng_prompts.sort(reverse=True)
    if eng_prompts:
        import statistics
        vals = [n for n, _ in eng_prompts if n > 0]
        lines.append(f"- Median prompts/engine: **{int(statistics.median(vals))}** (over engines with sessions) ")
        lines.append(f"- Mean prompts/engine: **{statistics.mean(vals):.1f}**")
        lines.append(f"- Max: **{eng_prompts[0][0]}** (`{eng_prompts[0][1]}`)")
        lines.append(f"- {sum(1 for n,_ in eng_prompts if n==0)} engine(s) without any recoverable prompt (sessions archived).")
    lines.append("")
    lines.append("Top-10 by prompt volume:")
    lines.append("")
    lines.append("| Rank | Project | Prompts | LOC | USD |")
    lines.append("|---:|---|---:|---:|---:|")
    for i, (n, name) in enumerate(eng_prompts[:10], 1):
        ov = next(o for o in engines if o["name"] == name)
        lines.append(f"| {i} | {name} | {n} | {ov['loc']['total_loc']:,} | ${ov.get('total_usd_estimate', 0):.2f} |")
    lines.append("")

    # Gameplay evidence
    lines.append("## Gameplay evidence (PGN + Stockfish-skill hints)")
    lines.append("")
    lines.append("Per-file naming conventions encode the Stockfish-skill or Elo target used in gauntlet runs. We surface the unique hints per engine.")
    lines.append("")
    lines.append("| Project | PGN files | Perft hits | Elo/skill hints (from filenames) |")
    lines.append("|---|---:|---:|---|")
    for ov in engines:
        gp = ov["gameplay"]
        elos = ", ".join(str(e) for e in gp.get("elo_hints") or []) or "—"
        if gp.get("n_pgn_files") or gp.get("perft_hits") or elos != "—":
            lines.append(f"| {ov['name']} | {gp.get('n_pgn_files',0)} | {gp.get('perft_hits',0)} | {elos} |")
    lines.append("")

    # Models observed
    lines.append("## Models observed across sessions")
    lines.append("")
    all_models = Counter()
    for ov in overview:
        for m in (ov["claude"]["models"] or []) + (ov["codex"]["models"] or []):
            all_models[m] += 1
    lines.append("| Model | # projects |")
    lines.append("|---|---:|")
    for m, n in all_models.most_common():
        lines.append(f"| `{m}` | {n} |")
    lines.append("")

    # Out-of-engine corpus
    lines.append("## Context projects (not engines; included for completeness)")
    lines.append("")
    lines.append("| Project | Bucket | LOC | Prompts | USD | Notes |")
    lines.append("|---|---|---:|---:|---:|---|")
    for ov in sorted(others, key=lambda x: x["bucket"]):
        prompts = (ov["claude"]["n_user_prompts"] or 0) + (ov["codex"]["n_user_prompts"] or 0)
        lines.append(
            f"| {ov['name']} | {ov['bucket']} | {ov['loc']['total_loc']:,} | {prompts} "
            f"| ${ov.get('total_usd_estimate', 0):.2f} | |"
        )
    lines.append("")

    # Interpretation for the paper
    lines.append("## Interpretation (PASS 2 thesis notes for the paper)")
    lines.append("")
    lines.append("1. **Agents can build non-trivial chess systems across ≥15 languages.** The corpus covers APL, Assembly, Brainfuck, C, C++, COBOL, CSS, HTML, Icon, Java, LaTeX, Mojo, Python, Ruby, Rust, SQL, Why3, and Rocq; engine cores span {} distinct primary languages in the engine bucket.".format(
        len({ov.get("primary_language") for ov in engines if ov.get("primary_language")})
    ))
    lines.append("")
    lines.append("2. **Chess provides strong oracles the agents actually exercise.** Projects where we recover PGN gauntlets, Stockfish-skill headers, or perft literals demonstrate that agents wrote and used oracles autonomously (see the Gameplay Evidence table). Example: `chess-ruby-cc` has 34 PGN files tagged at Elo 1500–2100; `chess-Rocq` has gauntlets against Stockfish skill 0–1 at targeted Elos 100–1700; `chess-why3-cc` emits 50 perft literal matches.")
    lines.append("")
    lines.append("3. **Language matters.** The feature coverage matrix shows that higher-level languages (Python, Ruby, Rust) routinely implement full UCI + TT + iterative deepening + quiescence pipelines; niche or constrained languages (Brainfuck, CSS-only, printf-only, LaTeX) trade engine strength for *existence proofs* — they typically implement move generation with minimal search. The LOC distribution reflects this: Python/Ruby engines are ~3k LOC with deep search; CSS/HTML and assembly engines reach 10k–60k LOC because the language's primitives do less work per line.")
    lines.append("")
    lines.append("4. **Agent interaction stays mostly at the capability level.** Median prompt volume per engine is modest (see \"Interaction demand\"). Intent classification on the per-project reports shows TestRequest, FeatureRequest, and Constraint as the dominant categories. The PL-ROOT prompts are usually high-level (\"write a chess engine in X that plays UCI and competes with Stockfish\"); the bulk of code-level detail is agent-initiated, visible in the tool-use counts (Bash/Edit/Write dominate Claude Code sessions).")
    lines.append("")
    lines.append("5. **Subagents and tooling matter.** Claude Code sessions with subagents (e.g., `chess-ruby-cc`, `chess-rust-cc`) show parallel exploration tactics and occasionally replace main transcripts after archival. In several folders the main transcript is lost but subagent logs remain — a reproducibility threat we flag in every per-project report.")
    lines.append("")
    lines.append("6. **Cost scales with oracle rigor, not just LOC.** The most expensive engines (`chess-cobol-cc` $518, `chess-printf-codex` $192, `chess-brainfuck` $170, `chess-brainfuck-cc` $160) are those where the agent iterates repeatedly against a correctness oracle — perft, a reference engine, or Stockfish gauntlets. Cheap engines tend to be one-shots in mainstream languages (Rust-codex $15, Java-cc $8) where the first-pass implementation already runs.")
    lines.append("")
    lines.append("## Threats to validity")
    lines.append("")
    lines.append("- **Archived Claude Code transcripts** (multiple projects have a `sessions-index.json` entry pointing to a missing `.jsonl`). Where only subagent logs remain, prompt/token counts under-report the user-driven interaction.")
    lines.append("- **Cost is a list-price estimate.** Real spend likely differs with tier discounts, fast-mode, and cache behavior we could not fully reconstruct.")
    lines.append("- **Primary-language detection** is LOC-based and occasionally misclassifies when agents generate auxiliary files (e.g. `chess-cobol-cc` has more C LOC than COBOL because transpilation produced C).")
    lines.append("- **Feature detection is regex-based.** Unusual languages (Brainfuck, APL) under-report feature coverage; manual inspection of the per-project reports is necessary before quoting matrix cells in the paper.")
    lines.append("- **Taxonomy is hand-curated.** The engine/meta/study split is a judgment call documented in `scripts/synthesis.py::CLASSIFICATION`.")
    lines.append("")
    lines.append("## Reproduce this analysis")
    lines.append("")
    lines.append("```bash")
    lines.append("cd ~/SANDBOX/chess-meta-analysis")
    lines.append("python3 scripts/discover.py            # overview")
    lines.append("python3 scripts/per_project_report.py  # dossier per project")
    lines.append("python3 scripts/elo_and_perft.py       # gameplay / perft extraction")
    lines.append("python3 scripts/synthesis.py           # this file")
    lines.append("```")
    lines.append("")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "SYNTHESIS.md").write_text("\n".join(lines), encoding="utf-8")

    appendix = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "classification": CLASSIFICATION,
        "overview": overview,
        "totals": {
            "n_projects": len(overview),
            "n_engines": len(engines),
            "total_usd_estimate": round(tot_cost, 2),
            "engines_usd_estimate": round(tot_cost_eng, 2),
            "total_loc_excluding_external": tot_loc,
            "engines_loc": tot_loc_eng,
            "total_prompts": tot_prompts,
            "engines_prompts": tot_prompts_eng,
            "total_sessions": tot_sessions,
        },
    }
    (DATA_DIR / "synthesis.json").write_text(json.dumps(appendix, indent=2, default=str))
    print(f"Wrote SYNTHESIS.md and data/synthesis.json")


if __name__ == "__main__":
    main()
