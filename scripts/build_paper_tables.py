"""Emit LaTeX tables for the paper (per-engine, not per-language).

Output under paper/tables/:
  tab_engines.tex        RQ1 + metadata: one row per engine
  tab_features_core.tex  RQ2 core features (rules, protocol, board rep)
  tab_features_search.tex    RQ2 search-algorithm features
  tab_features_eval.tex  RQ2 evaluation + strong-engine features
  tab_elo.tex            RQ4 Elo (PGN-derived + agent-claimed), per engine
  tab_cost.tex           RQ5 prompts, tokens, USD, hours, debug-ratio
  tab_eval_infra.tex     evaluation infrastructure per engine
  tab_effort_top10.tex   top-10 effort

Usage:
  python3 scripts/build_paper_tables.py
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from common import DATA_DIR, FEATURE_GROUPS

PAPER_TABLES = DATA_DIR.parent / "paper" / "tables"

# Per-engine display language (correcting LOC-based misclassifications).
DISPLAY_LANG: dict[str, str] = {
    "test-superset": "CSS + minimal JS",
    "chess-cobol-cc": "COBOL",
    "COBOL-chess": "COBOL",
    "chess-revisit-java-toCOBOL-codex": "COBOL",
    "chess-why3-cc": "Why3$\\to$C",
    "chess-why3": "Why3$\\to$OCaml",
    "chess-Rocq": "Rocq$\\to$OCaml",
    "chess-revisit-java-toRust-codex": "Rust",
    "chess-css-codex": "CSS/HTML",
    "chess-css-x86": "CSS/HTML",
    "chess-css-codex-guided": "CSS/HTML",
    "chess-latex-codex-replication": "LaTeX",
    "latex-chess-engine": "LaTeX (TeX)",
    "chess-brainfuck": "Brainfuck",
    "chess-brainfuck-cc": "Brainfuck",
    "chess-py-cc": "Python",
    "chess-apl-codex54": "APL",
    "chess-icon-codex": "Icon",
    "chess-mojo": "Mojo",
    "chess-assembly-codex": "Assembly",
    "chess-sql": "SQL",
    "chess-newlang-codex": "C++ (DSL host)",
    "lean-chess": "Lean 4",
    "minichess-5x5-repro": "Rust (5$\\times$5 variant)",
    "minichess-5x5-repro-cc": "Rust (5$\\times$5 variant)",
    "cplusplus-chess": "C++",
    "chess-cplusplus-claude": "C++",
    "chess-java-cc": "Java",
    "chess-java": "Java",
    "chess-ruby-cc": "Ruby",
    "chess-ruby-codex": "Ruby",
    "chess-rust-cc": "Rust",
    "chess-rust-codex": "Rust",
    "chess-purec": "C",
    "chess-purec-codex": "C",
    "chess-py": "Python",
}


def load_overview() -> list[dict[str, Any]]:
    return json.loads((DATA_DIR / "overview.json").read_text())


def load_project(name: str) -> dict[str, Any] | None:
    p = DATA_DIR / "projects" / f"{name}.json"
    if p.exists():
        return json.loads(p.read_text())
    return None


def display_language(ov: dict[str, Any]) -> str:
    return DISPLAY_LANG.get(ov["name"], ov.get("primary_language") or "—")


def agent_short(ov: dict[str, Any]) -> str:
    c = ov["claude"]["n_sessions"] > 0
    x = ov["codex"]["n_sessions"] > 0
    if c and x:
        return "CC+Codex"
    if c:
        return "CC"
    if x:
        return "Codex"
    # No live main transcripts. Fall back to the agent fingerprint
    # discover.py recorded (CC/Codex project directory existed even
    # after the JSONL transcripts were compacted away), then to the
    # naming convention if even that is missing. The zero in the
    # Prompts/USD columns speaks for itself about the missing
    # transcripts; the archival caveat is documented in Sec.~12.
    agents = ov.get("agents") or []
    has_cc = "Claude Code" in agents
    has_codex = "Codex" in agents
    if has_cc and has_codex:
        return "CC+Codex"
    if has_cc:
        return "CC"
    if has_codex:
        return "Codex"
    name = ov["name"].lower()
    if "codex" in name:
        return "Codex"
    if "-cc" in name or "claude" in name:
        return "CC"
    return "—"


def engines_list() -> list[dict[str, Any]]:
    """Main-corpus engines: scratch designs in a target language."""
    from synthesis import CLASSIFICATION
    ov = load_overview()
    return [o for o in ov if CLASSIFICATION.get(o["name"]) == "engine"]


def variants_list() -> list[dict[str, Any]]:
    """Placeholder --- minichess 5x5 variants were removed from the corpus."""
    return []


def special_list(role: str) -> list[dict[str, Any]]:
    from synthesis import CLASSIFICATION
    ov = load_overview()
    return [o for o in ov if CLASSIFICATION.get(o["name"]) == role]


SPECIAL_ROLE_LABEL = {
    "engine-port": "Port of chess-java-cc",
    "engine-dsl": "DSL design + transpile",
    "engine-failure": "Unconverged (failure)",
    "engine-codesign": "Agent-heavy co-design",
}


def tex_escape(s: str) -> str:
    r = (
        s.replace("\\", "\\textbackslash ")
        .replace("&", "\\&")
        .replace("%", "\\%")
        .replace("$", "\\$")
        .replace("#", "\\#")
        .replace("_", "\\_")
        .replace("~", "\\textasciitilde ")
        .replace("^", "\\textasciicircum ")
    )
    return r


def tex_lang(s: str) -> str:
    # Language strings already contain $\to$ etc. — pass through; escape other risky chars.
    return (
        s.replace("&", "\\&")
        .replace("%", "\\%")
        .replace("#", "\\#")
        .replace("_", "\\_")
    )


def has_feature(ov: dict[str, Any], feat: str) -> bool:
    feats = ov.get("features") or {}
    return feat in feats


# ----------------- tab_engines -------------------------------------------


def is_archived(ov: dict[str, Any]) -> bool:
    """True iff the project directory is fingerprinted as agent-driven
    (CC or Codex project dir present on disk) but no live main-session
    JSONL survived capture. Such engines show real agent activity in
    the repo and in subagent sidecars, but prompt/token/cost columns
    (which count main transcripts only) cannot be recovered."""
    if ov["claude"]["n_sessions"] > 0 or ov["codex"]["n_sessions"] > 0:
        return False
    agents = ov.get("agents") or []
    return any(
        a in ("Claude Code", "Codex")
        for a in agents
    )


def _engine_row(ov: dict[str, Any]) -> str:
    period_s = (ov["period"].get("start") or "")[:10]
    period_e = (ov["period"].get("end") or "")[:10]
    per = f"{period_s}$\\to${period_e}" if period_s else "—"
    if is_archived(ov):
        prompts_cell = "n/a"
        usd_cell = "n/a"
    else:
        prompts = (ov["claude"]["n_user_prompts"] or 0) + (ov["codex"]["n_user_prompts"] or 0)
        prompts_cell = str(prompts)
        usd_cell = f"\\${ov.get('total_usd_estimate', 0):.2f}"
    return (
        f"{tex_escape(ov['name'])} & {tex_lang(display_language(ov))} & "
        f"{agent_short(ov)} & {per} & "
        f"{ov['loc']['total_files']} & {ov['loc']['total_loc']:,} & "
        f"{prompts_cell} & {usd_cell} \\\\"
    )


def table_engines() -> str:
    engines = engines_list()
    engines.sort(key=lambda o: (display_language(o), o["name"]))
    lines = []
    lines.append("\\begin{table}[ht]\\centering\\small")
    lines.append("\\caption{\\RQ{1} Main-corpus engines. One row per agent$\\times$language session where the agent was asked to design a chess engine from scratch in a target language. Port, DSL, and failure experiments are reported separately in \\Cref{tab:rq1-special}. Minichess variants and the superseded chess-css-x86 are excluded per the folder triage. \\textbf{n/a} in the Prompts / USD columns means the engine's main session transcripts were compacted by \\claudecode{} before capture, so the underlying counts cannot be reconstructed --- the source on disk, the subagent sidecar logs, and the agent fingerprint (\\claudecode{} project directory present) confirm the engine \\emph{was} agent-built, only the main-loop metrics are lost. See \\Cref{sec:threats} for the full provenance note.}")
    lines.append("\\label{tab:rq1-engines}")
    lines.append("\\begin{tabular}{l l l l r r r r}")
    lines.append("\\toprule")
    lines.append("Engine & Language & Agent & Period & Files & LOC & Prompts & USD \\\\")
    lines.append("\\midrule")
    for ov in engines:
        lines.append(_engine_row(ov))
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table}")
    return "\n".join(lines) + "\n"


def table_engines_special() -> str:
    """Port / DSL / failure experiments, reported separately."""
    lines = []
    lines.append("\\begin{table}[ht]\\centering\\small")
    lines.append("\\caption{Special-role experiments. These follow a different protocol from the main corpus and are not averaged into the main-study numbers. \\emph{Port}: the agent is asked to translate a specific existing Java engine (chess-java-cc) into another language, preserving module structure. \\emph{DSL}: the agent designs a new chess-engine DSL (GAMBIT) and its C\\texttt{++}17 transpiler; the engine runs via generated C\\texttt{++}. \\emph{Failure}: an attempt that did not converge to a competitive engine within the user's budget.}")
    lines.append("\\label{tab:rq1-special}")
    lines.append("\\begin{tabular}{l l l l l r r r r}")
    lines.append("\\toprule")
    lines.append("Engine & Role & Language & Agent & Period & Files & LOC & Prompts & USD \\\\")
    lines.append("\\midrule")
    for role in ("engine-port", "engine-dsl", "engine-failure", "engine-codesign"):
        label = SPECIAL_ROLE_LABEL[role]
        engines = special_list(role)
        engines.sort(key=lambda o: o["name"])
        for ov in engines:
            period_s = (ov["period"].get("start") or "")[:10]
            period_e = (ov["period"].get("end") or "")[:10]
            per = f"{period_s}$\\to${period_e}" if period_s else "—"
            if is_archived(ov):
                prompts_cell = "n/a"
                usd_cell = "n/a"
            else:
                prompts = (ov["claude"]["n_user_prompts"] or 0) + (ov["codex"]["n_user_prompts"] or 0)
                prompts_cell = str(prompts)
                usd_cell = f"\\${ov.get('total_usd_estimate', 0):.2f}"
            lines.append(
                f"{tex_escape(ov['name'])} & {tex_escape(label)} & "
                f"{tex_lang(display_language(ov))} & {agent_short(ov)} & {per} & "
                f"{ov['loc']['total_files']} & {ov['loc']['total_loc']:,} & "
                f"{prompts_cell} & {usd_cell} \\\\"
            )
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table}")
    return "\n".join(lines) + "\n"


# ----------------- grouped feature tables --------------------------------


def _feature_table(title_caption: str, label: str, feats: list[str]) -> str:
    engines = engines_list()
    engines.sort(key=lambda o: (display_language(o), o["name"]))
    # Short column labels keep the table readable.
    SHORT = {
        "FEN parsing": "FEN",
        "UCI protocol": "UCI",
        "PGN": "PGN",
        "Castling": "Cas",
        "En passant": "EP",
        "Promotion": "Pro",
        "Check/Checkmate": "Chk",
        "Board: 0x88": "0x88",
        "Board: bitboard": "BB",
        "Board: magic bitboards": "MBB",
        "Board: mailbox 8x8": "MB8",
        "Board: mailbox 10x12": "MB10",
        "Perft": "Perft",
        "Minimax/Negamax": "Neg",
        "Alpha-beta": "$\\alpha\\beta$",
        "Iterative deepening": "ID",
        "Quiescence": "Qs",
        "Transposition table": "TT",
        "Zobrist hashing": "Zob",
        "Move ordering (MVV-LVA)": "MVV",
        "Killer moves": "Kil",
        "History heuristic": "His",
        "Principal-variation (PV)": "PV",
        "Null-move pruning": "NMP",
        "Late-move reduction (LMR)": "LMR",
        "Late-move pruning (LMP)": "LMP",
        "Aspiration windows": "Asp",
        "Futility pruning": "Fut",
        "Razoring": "Raz",
        "Material counting": "Mat",
        "Evaluation/PST": "PST",
        "Tapered evaluation": "Tap",
        "King safety": "KS",
        "Pawn structure": "PS",
        "Mobility": "Mob",
        "Opening book": "Bk",
        "Endgame tables": "EGT",
        "Time management": "TM",
        "NNUE/neural eval": "NNUE",
    }
    lines = []
    lines.append("\\begin{table}[ht]\\centering\\scriptsize")
    lines.append(f"\\caption{{{title_caption}}}")
    lines.append(f"\\label{{{label}}}")
    cols = "".join("c" for _ in feats)
    lines.append(f"\\begin{{tabular}}{{l l {cols}}}")
    lines.append("\\toprule")
    header = "Engine & Language & " + " & ".join(SHORT.get(f, f[:4]) for f in feats) + " \\\\"
    lines.append(header)
    lines.append("\\midrule")
    for ov in engines:
        row = [tex_escape(ov["name"]), tex_lang(display_language(ov))]
        for f in feats:
            row.append("\\checkmark" if has_feature(ov, f) else "")
        lines.append(" & ".join(row) + " \\\\")
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table}")
    return "\n".join(lines) + "\n"


def table_features_core() -> str:
    feats = FEATURE_GROUPS["Rules & protocol"] + FEATURE_GROUPS["Board representation"]
    caption = "\\RQ{2} Core features: rules, protocol, and board representation. A \\checkmark indicates the feature was detected by regex in the repository's source or documentation. For constrained-execution-model engines (Brainfuck, LaTeX), missing \\checkmark may reflect detection limits rather than absence; we cross-reference the per-engine dossier before drawing claims. Notice the diversity of board representations --- 0$\\times$88 mailbox, bitboards, 8$\\times$8 arrays --- agents pick per engine, not per language."
    return _feature_table(caption, "tab:rq2-core", feats)


def table_features_search() -> str:
    feats = FEATURE_GROUPS["Search core"] + FEATURE_GROUPS["Search extensions"]
    caption = "\\RQ{2} Search features. Core (Minimax/Negamax, $\\alpha\\beta$, iterative deepening, quiescence, transposition table, Zobrist hashing, perft) and extensions (MVV-LVA ordering, killer moves, history heuristic, PV move, null-move pruning, LMR, LMP, aspiration windows, futility, razoring). `Core-only' engines stop at the left block; `advanced' engines pick a subset from the right block. The distribution of the right block is what separates an~\\elo{1500} from an~\\elo{2000} agent-built engine in the same language."
    return _feature_table(caption, "tab:rq2-search", feats)


def table_features_eval() -> str:
    feats = FEATURE_GROUPS["Evaluation"] + FEATURE_GROUPS["Strong-engine features"]
    caption = "\\RQ{2} Evaluation and strong-engine features. Material, PST, tapered mid/endgame scoring, king safety, pawn-structure terms, mobility; and the `frontier' extras (opening book, endgame tables, time management, NNUE). NNUE appears in a single engine in the corpus, and endgame tables only where C/C\\texttt{++} tooling makes them practical."
    return _feature_table(caption, "tab:rq2-eval", feats)


# ----------------- RQ4 Elo -----------------------------------------------


def table_elo() -> str:
    engines = engines_list()
    rows = []
    for ov in engines:
        pr = load_project(ov["name"]) or {}
        pgn_agg = (pr.get("elo_analysis") or {}).get("aggregate") or {}
        enrich = (pr.get("enrichment") or {}).get("agent_elo_claims") or {}
        vals = [v for v in (enrich.get("values") or []) if 400 <= v <= 3500]
        rows.append({
            "name": ov["name"],
            "lang": display_language(ov),
            "agent": agent_short(ov),
            "n_games": pgn_agg.get("n_games", 0),
            "elo_pgn": pgn_agg.get("elo_estimate"),
            "ci": pgn_agg.get("ci95"),
            "claim_min": min(vals) if vals else None,
            "claim_max": max(vals) if vals else None,
        })
    rows.sort(key=lambda r: -(r["elo_pgn"] or r["claim_max"] or -1))
    lines = []
    lines.append("\\begin{table}[ht]\\centering\\small")
    lines.append("\\caption{\\RQ{4} Estimated playing strength per engine. `PGN Elo' is the inverse-variance aggregate of games mined from the repository's \\pgn{} files against calibrated \\stockfish{} opponents. Em-dash means no such gauntlet survived in-tree. `Agent-claimed' is the min--max band of Elo numbers the agent itself stated in its session transcripts (values clipped to 400--3500). The table thus combines two evidence streams --- PGN gameplay and in-session claims --- giving coverage where either stream alone would be sparse.}")
    lines.append("\\label{tab:rq4-elo}")
    lines.append("\\begin{tabular}{l l l r r r r}")
    lines.append("\\toprule")
    lines.append("Engine & Language & Agent & Games & PGN Elo & CI95 & Agent-claimed \\\\")
    lines.append("\\midrule")
    for r in rows:
        elo = f"{int(r['elo_pgn'])}" if r["elo_pgn"] is not None else "—"
        ci = f"$\\pm${r['ci']}" if r.get("ci") else "—"
        if r["claim_min"] and r["claim_max"] and r["claim_min"] != r["claim_max"]:
            claim = f"{r['claim_min']}--{r['claim_max']}"
        elif r["claim_max"]:
            claim = f"{r['claim_max']}"
        else:
            claim = "—"
        lines.append(
            f"{tex_escape(r['name'])} & {tex_lang(r['lang'])} & {r['agent']} & "
            f"{r['n_games']} & {elo} & {ci} & {claim} \\\\"
        )
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table}")
    return "\n".join(lines) + "\n"


# ----------------- RQ5 cost (per engine, sorted by USD) -------------------


def table_cost() -> str:
    engines = engines_list()
    rows = []
    for ov in engines:
        pr = load_project(ov["name"]) or {}
        enrich = (pr.get("enrichment") or {}).get("difficulty") or {}
        prompts = (ov["claude"]["n_user_prompts"] or 0) + (ov["codex"]["n_user_prompts"] or 0)
        tok_c = ov["claude"]["tokens"] or {}
        tok_x = ov["codex"]["tokens"] or {}
        tot_in = (
            tok_c.get("input", 0) + tok_c.get("cache_read", 0) + tok_c.get("cache_creation", 0)
            + tok_x.get("input", 0) + tok_x.get("cache_read", 0)
        )
        tot_out = tok_c.get("output", 0) + tok_x.get("output", 0)
        usd = ov.get("total_usd_estimate") or 0.0
        rows.append({
            "name": ov["name"],
            "lang": display_language(ov),
            "agent": agent_short(ov),
            "archived": is_archived(ov),
            "prompts": prompts,
            "in_tok": tot_in,
            "out_tok": tot_out,
            "usd": usd,
            "hrs": enrich.get("session_hours_longest"),
            "debug_ratio": enrich.get("debug_ratio"),
        })
    # Archived-transcript rows sink to the bottom; real rows sort by USD desc.
    rows.sort(key=lambda r: (r["archived"], -r["usd"]))
    lines = []
    lines.append("\\begin{table}[ht]\\centering\\small")
    lines.append("\\caption{\\RQ{5} Cost, tokens, and difficulty per engine. `In' = input + cache-read + cache-creation tokens; `Out' = model output tokens. `Hours' = wallclock span of the longest main transcript whose cwd equals the project. `Debug' = fraction of user prompts containing debugging-intent keywords. USD is a list-price estimate (no account discounts). Rows with \\textbf{n/a} in every numeric column correspond to engines whose main session transcripts were compacted by \\claudecode{} before capture; see \\Cref{sec:threats} for the provenance note.}")
    lines.append("\\label{tab:rq5-cost}")
    lines.append("\\begin{tabular}{l l l r r r r r r}")
    lines.append("\\toprule")
    lines.append("Engine & Language & Agent & Prompts & In (kTok) & Out (kTok) & USD & Hours & Debug \\\\")
    lines.append("\\midrule")
    for r in rows:
        if r["archived"]:
            lines.append(
                f"{tex_escape(r['name'])} & {tex_lang(r['lang'])} & {r['agent']} & "
                f"n/a & n/a & n/a & n/a & n/a & n/a \\\\"
            )
            continue
        hrs = f"{r['hrs']:.1f}" if r["hrs"] is not None else "—"
        dbg = f"{r['debug_ratio']:.2f}" if r.get("debug_ratio") is not None else "—"
        lines.append(
            f"{tex_escape(r['name'])} & {tex_lang(r['lang'])} & {r['agent']} & "
            f"{r['prompts']} & {r['in_tok']/1000:,.0f} & {r['out_tok']/1000:,.0f} & "
            f"\\${r['usd']:.2f} & {hrs} & {dbg} \\\\"
        )
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table}")
    return "\n".join(lines) + "\n"


# ----------------- Eval infrastructure -----------------------------------


def table_eval_infra() -> str:
    engines = engines_list()
    rows = []
    for ov in engines:
        pr = load_project(ov["name"]) or {}
        ei = (pr.get("enrichment") or {}).get("eval_infrastructure") or {}
        tests = (pr.get("enrichment") or {}).get("test_evidence") or {}
        rows.append({
            "name": ov["name"],
            "lang": display_language(ov),
            "cutechess": ei.get("cutechess-cli", 0) > 0,
            "custom_elo": ei.get("Custom Elo script", 0) > 0,
            "sf": ei.get("Stockfish gauntlet", 0) > 0,
            "perft": ei.get("Perft tests", 0) > 0 or tests.get("has_perft_tests"),
            "random": ei.get("Random baseline", 0) > 0,
            "self": ei.get("Self-play", 0) > 0,
            "tests": tests.get("n_test_files", 0),
        })
    rows.sort(key=lambda r: (r["lang"], r["name"]))
    lines = []
    lines.append("\\begin{table}[ht]\\centering\\scriptsize")
    lines.append("\\caption{Evaluation infrastructure set up by the agent, detected from transcripts and tool invocations. Cute.=cutechess-cli; CustomElo=bespoke Elo-estimation script; SF=Stockfish gauntlet at calibrated \\texttt{UCI\\_Elo}; Perft=perft tests as code/harness; Rand.=random-baseline opponent; Self=self-play. \\#Tests=count of repository test files.}")
    lines.append("\\label{tab:eval-infra}")
    lines.append("\\begin{tabular}{l l c c c c c c r}")
    lines.append("\\toprule")
    lines.append("Engine & Language & Cute. & CustomElo & SF & Perft & Rand. & Self & \\#Tests \\\\")
    lines.append("\\midrule")
    def m(b) -> str:
        return "\\checkmark" if b else ""
    for r in rows:
        lines.append(
            f"{tex_escape(r['name'])} & {tex_lang(r['lang'])} & "
            f"{m(r['cutechess'])} & {m(r['custom_elo'])} & {m(r['sf'])} & "
            f"{m(r['perft'])} & {m(r['random'])} & {m(r['self'])} & "
            f"{r['tests']} \\\\"
        )
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table}")
    return "\n".join(lines) + "\n"


# ----------------- Top-10 effort -----------------------------------------


def table_effort_top10() -> str:
    engines = engines_list()
    rows = []
    for ov in engines:
        pr = load_project(ov["name"]) or {}
        enrich = (pr.get("enrichment") or {}).get("difficulty") or {}
        prompts = (ov["claude"]["n_user_prompts"] or 0) + (ov["codex"]["n_user_prompts"] or 0)
        rows.append({
            "name": ov["name"],
            "lang": display_language(ov),
            "prompts": prompts,
            "usd": ov.get("total_usd_estimate") or 0.0,
            "loc": ov["loc"]["total_loc"],
            "hrs": enrich.get("session_hours_longest"),
            "debug": enrich.get("debug_ratio"),
        })
    rows.sort(key=lambda r: -r["prompts"])
    lines = []
    lines.append("\\begin{table}[ht]\\centering\\small")
    lines.append("\\caption{Top 10 engines by user-prompt volume. Prompt volume is a coarse but comparable proxy for interaction intensity; it correlates with USD spend but not with LOC. Long prompt tails mark engines where the agent hit a correctness-oracle loop and iterated.}")
    lines.append("\\label{tab:rq5-effort}")
    lines.append("\\begin{tabular}{r l l r r r r r}")
    lines.append("\\toprule")
    lines.append("\\# & Engine & Language & Prompts & LOC & USD & Hours & Debug \\\\")
    lines.append("\\midrule")
    for i, r in enumerate(rows[:10], start=1):
        hrs = f"{r['hrs']:.1f}" if r["hrs"] is not None else "—"
        dbg = f"{r['debug']:.2f}" if r.get("debug") is not None else "—"
        lines.append(
            f"{i} & {tex_escape(r['name'])} & {tex_lang(r['lang'])} & "
            f"{r['prompts']} & {r['loc']:,} & \\${r['usd']:.2f} & {hrs} & {dbg} \\\\"
        )
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table}")
    return "\n".join(lines) + "\n"


def table_novelty() -> str:
    """RQ3 novelty summary (per-engine)."""
    nov = json.loads((DATA_DIR / "novelty.json").read_text()) if (DATA_DIR / "novelty.json").exists() else {}
    engines = engines_list()
    engines.sort(key=lambda o: (display_language(o), o["name"]))
    lines = []
    lines.append("\\begin{table}[ht]\\centering\\scriptsize")
    lines.append("\\caption{\\RQ{3} Novelty evidence, per engine. `Class.' is our classification: ``scratch'' means the engine-core files contain no chess-library import, no canonical-engine fingerprint, and no self-reported copy claim; ``lib-asst'' means the engine core imports an external chess library; ``fp-match'' means a distinctive fingerprint (e.g., \\texttt{python-chess} API surface) appears inside the engine core; ``copy-claim'' means the transcript contains explicit authorship language (``ported from X'', ``adapt from X'', \\ldots). `Core imp.' and `Core fp.' are the engine-core-only evidence streams (test/harness files are scored separately). `Tool dep.' flags a chess library used only in the evaluation tooling. `Strong' and `Weak' are counts of transcript mentions of canonical engines (``adapt from''/``port from'' vs.\\ ``like''/``based on'').}")
    lines.append("\\label{tab:rq3-novelty}")
    lines.append("\\begin{tabular}{l l l l l c c c}")
    lines.append("\\toprule")
    lines.append("Engine & Lang. & Class. & Core imp. & Core fp. & Tool dep. & Strong & Weak \\\\")
    lines.append("\\midrule")
    for ov in engines:
        r = nov.get(ov["name"], {})
        cls = r.get("classification", "?")
        core_i = ", ".join(r.get("source_chess_imports") or []) or "—"
        core_f = ", ".join(r.get("canonical_fingerprints") or []) or "—"
        tool_d = "\\checkmark" if (r.get("source_chess_imports_tooling") or r.get("manifest_chess_libs")) else ""
        s = len(r.get("strong_copy_hits") or [])
        w = len(r.get("weak_reference_hits") or [])
        lines.append(
            f"{tex_escape(ov['name'])} & {tex_lang(display_language(ov))} & "
            f"{cls} & {tex_escape(core_i)} & {tex_escape(core_f)} & "
            f"{tool_d} & {s} & {w} \\\\"
        )
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table}")
    return "\n".join(lines) + "\n"


def _fit_to_textwidth(body: str) -> str:
    """Wrap the inner \\begin{tabular}...\\end{tabular} of a table body in
    \\resizebox{\\textwidth}{!}{...} so that wide tables shrink to fit the
    one-column A4 layout without cropping at the right margin. Caption and
    label stay outside the box (they stay at full body font size)."""
    open_tag = "\\begin{tabular}"
    close_tag = "\\end{tabular}"
    i = body.find(open_tag)
    j = body.find(close_tag)
    if i == -1 or j == -1:
        return body
    j_end = j + len(close_tag)
    return (
        body[:i]
        + "\\resizebox{\\textwidth}{!}{%\n"
        + body[i:j_end]
        + "\n}"
        + body[j_end:]
    )


def main() -> None:
    PAPER_TABLES.mkdir(parents=True, exist_ok=True)
    raw = {
        "tab_engines.tex": table_engines(),
        "tab_engines_special.tex": table_engines_special(),
        "tab_features_core.tex": table_features_core(),
        "tab_features_search.tex": table_features_search(),
        "tab_features_eval.tex": table_features_eval(),
        "tab_elo.tex": table_elo(),
        "tab_cost.tex": table_cost(),
        "tab_eval_infra.tex": table_eval_infra(),
        "tab_effort_top10.tex": table_effort_top10(),
        "tab_novelty.tex": table_novelty(),
    }
    # Wide tables that overflow \textwidth on A4 single-column layout.
    # We scale them to fit; narrow tables render at native size.
    WIDE = {
        "tab_engines.tex",
        "tab_engines_special.tex",
        "tab_features_core.tex",
        "tab_features_search.tex",
        "tab_features_eval.tex",
        "tab_elo.tex",
        "tab_cost.tex",
        "tab_eval_infra.tex",
        "tab_novelty.tex",
    }
    outputs = {
        name: (_fit_to_textwidth(body) if name in WIDE else body)
        for name, body in raw.items()
    }
    # Remove the old per-language coverage table file; no longer generated.
    stale = PAPER_TABLES / "tab_coverage.tex"
    if stale.exists():
        stale.unlink()
    stale2 = PAPER_TABLES / "tab_features.tex"
    if stale2.exists():
        stale2.unlink()
    stale3 = PAPER_TABLES / "tab_difficulty.tex"
    if stale3.exists():
        stale3.unlink()
    for name, body in outputs.items():
        (PAPER_TABLES / name).write_text(body, encoding="utf-8")
        print(f"wrote {name}")


if __name__ == "__main__":
    main()
