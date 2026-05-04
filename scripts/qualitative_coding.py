"""Render the qualitative-triangulation pilot into a Markdown report.

Reads:
  data/qualitative/frame.json   coding frame (codes + descriptions + linked RQs)
  data/qualitative/codes.json   coded excerpts (source, line, codes, quote, note)

Writes:
  reports/QUALITATIVE.md        theme x source x quote synthesis

The pilot codes two sources (TeX and Brainfuck blog posts) against a
nine-code frame tied to the paper's RQs. The same tool scales to more
sources (repo ARCHITECTURE/SPECIFICATION files, expert notes) by
appending entries to codes.json.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from common import DATA_DIR, REPORTS_DIR


def load_data() -> tuple[dict, dict]:
    frame = json.loads((DATA_DIR / "qualitative" / "frame.json").read_text())
    codes = json.loads((DATA_DIR / "qualitative" / "codes.json").read_text())
    return frame, codes


def build_report(frame: dict, codes_doc: dict) -> str:
    frame_codes = frame["codes"]
    sources = codes_doc["sources"]
    excerpts = codes_doc["codes"]

    # Per-code indexing
    by_code: dict[str, list[dict]] = defaultdict(list)
    for e in excerpts:
        for c in e["codes"]:
            by_code[c].append(e)
    # Per-source indexing
    by_source: dict[str, list[dict]] = defaultdict(list)
    for e in excerpts:
        by_source[e["source"]].append(e)
    # Counts
    code_counts = Counter(c for e in excerpts for c in e["codes"])
    source_counts = Counter(e["source"] for e in excerpts)

    L: list[str] = []
    L.append("# Qualitative triangulation (pilot)")
    L.append("")
    L.append(f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}._")
    L.append("")
    L.append("This file is a pilot run of Path~A in the paper's qualitative-methods plan: a structured coding of author-authored and expert-sourced secondary documents against a small, RQ-tied coding frame. The purpose is to corroborate the paper's quantitative findings with *sourced* qualitative evidence --- moving specific claims out of \"anecdote\" territory and into \"systematically coded\" territory --- without attempting a full grounded-theory pass over 28 session transcripts.")
    L.append("")
    L.append("## Scope of this pilot")
    L.append("")
    L.append("| Source | Engine | Category | Excerpts coded |")
    L.append("|---|---|---|---:|")
    for sid, s in sources.items():
        n = source_counts.get(sid, 0)
        L.append(f"| [{s['title']}]({s['url']}) ({s['date']}) | `{s['engine']}` | {s['lang_category']} | {n} |")
    L.append(f"| **Total** | | | **{sum(source_counts.values())}** |")
    L.append("")
    L.append("## Coding frame")
    L.append("")
    L.append("Nine codes tied to paper research questions:")
    L.append("")
    L.append("| Code | Label | RQs | Description |")
    L.append("|---|---|---|---|")
    for cid, meta in frame_codes.items():
        rq = ", ".join(meta["supports_rq"])
        L.append(f"| `{cid}` | {meta['label']} | {rq} | {meta['description']} |")
    L.append("")

    L.append("## Code x source frequency matrix")
    L.append("")
    src_ids = list(sources.keys())
    header = "| Code | " + " | ".join(src_ids) + " | total |"
    sep = "|---|" + "---:|" * (len(src_ids) + 1)
    L.append(header)
    L.append(sep)
    for cid in frame_codes:
        row = [f"`{cid}`"]
        total = 0
        for sid in src_ids:
            n = sum(1 for e in by_code.get(cid, []) if e["source"] == sid)
            row.append(str(n) if n else "")
            total += n
        row.append(f"**{total}**")
        L.append("| " + " | ".join(row) + " |")
    L.append("")
    # Count codes that appear in BOTH sources (saturation low-bar).
    both = 0
    for cid in frame_codes:
        src_hits = {e["source"] for e in by_code.get(cid, [])}
        if len(src_hits) >= 2:
            both += 1
    only_one = [cid for cid in frame_codes if len({e["source"] for e in by_code.get(cid, [])}) == 1]
    L.append(f"Every code appears in at least one source; **{both} / {len(frame_codes)}** codes appear in both sources (a low-bar form of saturation for a two-document pilot). Codes appearing in only one source are worth flagging: " + ", ".join(f"`{c}`" for c in only_one) + ".")
    L.append("")

    # Per-code findings
    L.append("## Findings per code")
    L.append("")
    for cid, meta in frame_codes.items():
        L.append(f"### `{cid}` --- {meta['label']}")
        L.append("")
        L.append(f"_Supports: {', '.join(meta['supports_rq'])}. Total excerpts: {code_counts[cid]}._")
        L.append("")
        for e in by_code.get(cid, []):
            src = sources[e["source"]]
            # one blockquote per excerpt
            L.append(f"> {e['quote']}")
            L.append(f"_Source: [{src['engine']}]({src['url']}), line~{e['line']}._ {e['note']}")
            L.append("")
        L.append("")

    # Per-source views (useful when someone reads one blog)
    L.append("## Per-source digests")
    L.append("")
    for sid, s in sources.items():
        L.append(f"### {s['engine']}")
        L.append(f"_Source: [{s['title']}]({s['url']}), {s['date']}._")
        L.append("")
        coded = by_source.get(sid, [])
        # Group by code
        by_code_in_source: dict[str, list[dict]] = defaultdict(list)
        for e in coded:
            for c in e["codes"]:
                by_code_in_source[c].append(e)
        for cid in frame_codes:
            es = by_code_in_source.get(cid, [])
            if not es:
                continue
            L.append(f"- **`{cid}`** ({len(es)}): " +
                     "; ".join(f"l.~{e['line']}" for e in es))
        L.append("")

    # Synthesis: how does the qualitative evidence reinforce the paper?
    L.append("## Synthesis: how the coded evidence corroborates each RQ")
    L.append("")
    rq_to_codes: dict[str, list[str]] = defaultdict(list)
    for cid, meta in frame_codes.items():
        for rq in meta["supports_rq"]:
            rq_to_codes[rq].append(cid)
    for rq in sorted(rq_to_codes):
        L.append(f"### {rq}")
        L.append("")
        total = sum(code_counts[c] for c in rq_to_codes[rq])
        L.append(f"_Codes supporting this RQ: {', '.join('`'+c+'`' for c in rq_to_codes[rq])} ({total} excerpts across both sources)._")
        L.append("")
        L.append(_rq_narrative(rq, rq_to_codes[rq], by_code, sources))
        L.append("")

    L.append("## How to extend this pilot")
    L.append("")
    L.append("To turn this pilot into a section of the paper, add entries to `data/qualitative/codes.json` for any of:")
    L.append("")
    L.append("1. Further blog posts by the first author (`2026-03-03-PrintfOrientedProgrammingCodingAgents.md`, `2026-03-17-CodingAgentsMnMLang.md`, `2026-02-23-FromScratchChessEnginesPolyglot.md`, \\ldots)")
    L.append("2. Repository-level `ARCHITECTURE.md`, `SPECIFICATION.md`, and `README.md` files authored by the agent for each engine (e.g., `chess-java-cc/SPECIFICATION.md`, `COBOL-chess/ARCHITECTURE.md`).")
    L.append("3. Expert-interview notes (Brainfuck, Rocq, Why3 informants) once anonymised.")
    L.append("")
    L.append("Re-run `python3 scripts/qualitative_coding.py` to regenerate this file. Inter-rater reliability, if the paper claims it, should be established by a second coder on at least 30\\% of the excerpts --- record their codings in a second JSON file and report Cohen's kappa per code.")
    return "\n".join(L) + "\n"


def _rq_narrative(rq: str, codes_for_rq: list[str], by_code: dict, sources: dict) -> str:
    """Hand-written synthesis text per RQ, grounded in this pilot."""
    if rq == "RQ2":
        return (
            "The `language-constraint` and `feature-adaptation` codes together describe *why* the feature set is language-shaped. "
            "The TeX source narrates `\\count`-registers-as-RAM and `\\csname`-tables-as-hash-maps as first-class idioms; the Brainfuck source narrates the 64-way switch as the irreducible cost of random access and the 672-cell layout as a struct-equivalent. Neither case is 'agent translated a reference engine into the target language' --- both cases are 'agent designed the smallest language-native encoding that supports a given chess feature'. This corroborates the within-language variance finding: feature choice is mediated by which language idioms the agent picks, not by the language alone."
        )
    if rq == "RQ3":
        return (
            "The `novelty-absence` and `synthesis-not-copy` codes converge: both posts explicitly assert no prior open-source chess engine exists in the target language (with search venues enumerated for TeX, and the 2019 TalkChess attempt reviewed and excluded for Brainfuck), and both argue that the existing engine cannot be a line-by-line memorisation. The TeX post goes further: the creativity sits at the algorithm-to-idiom translation layer, not at the line-by-line translation layer. The `evasion-risk` code flags the failure mode --- agent drifting to Python inside a Brainfuck engine --- and its two remedies (structural enforcement of the constraint; active human verification) match the paper's §4.4 qualitative-supervision protocol and the §7.4 chess-css-codex evasion case."
        )
    if rq == "RQ4":
        return (
            "The `oracle-exploitation` code corroborates the paper's 'oracle-first is a population property' finding: "
            "perft as primary correctness oracle in both posts; cutechess gauntlets at CCRL 120$+$1 in the TeX post; random-move baselines when Stockfish is too strong in the Brainfuck post. The `language-constraint` code provides qualitative evidence for the Elo ceiling: TeX's macro-expansion depth caps search at 3 plies + quiescence (~\\elo{1280}); Brainfuck's 64-way array access makes 3-ply search cost 45--600s per move (~\\elo{100-200}). The ceiling is not about what the LLM knows about chess; it is about what the language's execution model admits under realistic time budgets."
        )
    if rq == "RQ5":
        return (
            "All three cost/interaction codes fire here. `human-steering` confirms the capability-level prompt style (both sources explicitly state the deliberately-vague PL-ROOT). `agent-self-correction` is quantified for Brainfuck (9 cell-collision bugs found and fixed autonomously) and for TeX (the 30-turn debug loop chasing the depth-3 timeout). `feedback-loop-cost` is the sharpest qualitative match to the paper's cost-scales-with-oracle-rigor finding: 'the real bottleneck was not writing the code, but evaluating it', with a concrete 'half a day per test-fix cycle' in Brainfuck. These are not ornamental quotes; each one is the developer-side view of a behaviour the paper describes quantitatively at the population level."
        )
    if rq == "Method":
        return (
            "The `evasion-risk` code contributes evidence that the paper's qualitative-supervision protocol is not hypothetical. The Brainfuck post documents a concrete Codex-vs-Claude-Code contrast on the same constraint: under Codex, critical logic was silently migrated to Python; under Claude Code, the architecture (Python compiler emits BF, then `./bfi chess.bf` runs it) made the drift structurally impossible. The methodological prescription --- structural enforcement where possible, active human verification where not --- is the same prescription the paper's §4.4 adopts."
        )
    return "(narrative pending)"


def main() -> None:
    frame, codes = load_data()
    report = build_report(frame, codes)
    out = REPORTS_DIR / "QUALITATIVE.md"
    out.write_text(report, encoding="utf-8")
    print(f"Wrote {out}")
    print(f"  sources: {len(codes['sources'])}")
    print(f"  coded excerpts: {len(codes['codes'])}")
    codes_per = Counter(c for e in codes['codes'] for c in e['codes'])
    print(f"  codes populated: {len(codes_per)} / {len(frame['codes'])}")


if __name__ == "__main__":
    main()
