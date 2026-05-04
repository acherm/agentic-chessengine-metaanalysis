#!/usr/bin/env python3
"""feature_compare.py — Pairwise similarity and qualitative analysis of feature hotspots.

Reads the JSON produced by feature_locator.py --hotspot and, for each pair of
engines that implement the feature, computes:

  1. Token-Jaccard   — raw lexical overlap after normalising the code
  2. Feature-Jaccard — presence/absence of known sub-features (e.g. stand-pat,
                       delta pruning, TT probe, …) compared as binary vectors

Optionally calls the Claude API (--llm) to produce:
  3. Structured extraction — which sub-features are present per engine
  4. Qualitative narrative — key differences, algorithmic lineage

Usage
-----
  # Similarity matrix only (no API):
    python3 scripts/feature_compare.py --input reports/features/quiescence.json

  # Full analysis with LLM (requires ANTHROPIC_API_KEY):
    python3 scripts/feature_compare.py --input reports/features/quiescence.json --llm

  # Any other feature hotspot:
    python3 scripts/feature_compare.py --input reports/features/alpha_beta.json --llm

Output
------
  reports/features/<name>.compare.txt   — similarity matrix + sub-feature table
  reports/features/<name>.analysis.txt  — LLM narrative (if --llm)
  reports/features/<name>.compare.json  — full structured data
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS_DIR))

# ---------------------------------------------------------------------------
# Algorithmic sub-feature catalogue for quiescence search
# (used when feature_name == "Quiescence"; generic token-Jaccard always runs)
# ---------------------------------------------------------------------------

QSEARCH_SUBFEATURES: dict[str, re.Pattern] = {
    "stand_pat":       re.compile(r"stand.?pat|standing.eval|static.eval", re.I),
    "beta_cutoff":     re.compile(r"stand.?pat\s*>=?\s*beta|return\s+beta|beta.cutoff", re.I),
    "alpha_update":    re.compile(r"(?:if|when|alpha)\s*[<>]=?\s*stand.?pat|alpha\s*:?=\s*(?:max\s*\(|stand)", re.I),
    "capture_only_gen":re.compile(r"cap.only|captures.only|gen.cap|capture.move|only.captures|tactical|CAP.ONLY", re.I),
    "delta_pruning":   re.compile(r"\bdelta\b", re.I),
    "see_pruning":     re.compile(r"\bSEE\b|static.exchange", re.I),
    "mvv_lva":         re.compile(r"\bMVV.?LVA\b|most.valuable|score.cap", re.I),
    "depth_limit":     re.compile(r"qdepth|q.?depth|QUIESCENCE.MAX.PLY|QSearchDepth|max.?ply", re.I),
    "check_evasion":   re.compile(r"in.check|is.check|check.*evasion|in_check|IN.CHECK|inCheck", re.I),
    "tt_probe":        re.compile(r"transposition|tt.probe|tt\.get|hash.look|TT\b", re.I),
    "promotions":      re.compile(r"\bpromot", re.I),
    "negamax_recurse": re.compile(r"-\s*(?:self\.)?(?:quiesc|qsearch|QUIESC|quiescence)\s*\(", re.I),
    "fail_soft":       re.compile(r"return\s+(?:score|best|value|stand.?pat)\s*$", re.I | re.MULTILINE),
}

# ---------------------------------------------------------------------------
# Algorithmic sub-feature catalogue for Transposition Table + Zobrist hashing
# ---------------------------------------------------------------------------

TT_SUBFEATURES: dict[str, re.Pattern] = {
    # Zobrist random table — array of random numbers indexed by piece×square
    "zobrist_table":    re.compile(
        r"zobrist|ZOBRIST|rand.*key|random.*\[|zob_key|piece_keys|piece_hash"
        r"|ZobristTable|random_table", re.I),
    # Incremental hash update via XOR on make/unmake move
    "incremental_hash": re.compile(
        r"hash\s*\^=|key\s*\^=|\.hash\s*\^=|pos_key\s*\^=|COMPUTE.*XOR"
        r"|xor.*hash|hash.*xor|\bXOR\b.*key|key.*\bXOR\b", re.I),
    # TT lookup / probe operation
    "tt_probe":         re.compile(
        r"tt\[|transposition.*\[|tt_probe|lookup_tt|get_tt|probe.*hash"
        r"|TT-PROBE|hash.?table\[|\.get\s*\(.*hash|entry\s*=.*\btt\b", re.I),
    # TT store / write operation
    "tt_store":         re.compile(
        r"tt\[.*\]\s*[=:]|store_tt|save_tt|TT-STORE|tt_store"
        r"|\.insert\s*\(|table\.put\(|write.*entry|entry\.score\s*=", re.I),
    # Depth check: stored depth must be >= remaining depth before trusting entry
    "depth_check":      re.compile(
        r"\.depth\s*>=|entry\.depth|tt_depth|depth\s*>=?\s*remaining"
        r"|hash_depth|stored.*depth|depth.*stored", re.I),
    # Exact-score flag (hit is exact, not a bound)
    "flag_exact":       re.compile(
        r"\bEXACT\b|NodeType::Exact|HashFlag::Exact|FLAG_EXACT"
        r"|SCORE_EXACT|EXACT_SCORE|HASH.EXACT|PV.NODE", re.I),
    # Lower-bound / fail-high / beta flag
    "flag_lower":       re.compile(
        r"LOWER.?BOUND|HashFlag::Lower|HASH.BETA|hash_beta"
        r"|FAIL.HIGH|CUT.NODE|flag.*lower|lower.*bound", re.I),
    # Upper-bound / fail-low / alpha flag
    "flag_upper":       re.compile(
        r"UPPER.?BOUND|HashFlag::Upper|HASH.ALPHA|hash_alpha"
        r"|FAIL.LOW|ALL.NODE|flag.*upper|upper.*bound", re.I),
    # PV/best/hash move stored in the TT entry (for move ordering)
    "best_move_stored": re.compile(
        r"best.?move|hash.?move|tt.?move|pv.?move|bestMove"
        r"|hashMove|HASH.MOVE|TT-MOVE|tt_move", re.I),
    # TT size is power-of-2 parameterized / uses index mask
    "tt_size_config":   re.compile(
        r"tt.?size|hash.?size|TT.MB|TT.SIZE|1\s*<<\s*\d"
        r"|hash.?mask|mask.*hash|tt.?mask", re.I),
    # Age or generation-based replacement (prefer newer entries)
    "age_replacement":  re.compile(
        r"\bage\b.*entry|entry.*\bage\b|generation|tt.*age"
        r"|age.*tt|replace.*old|older.*entry", re.I),
    # Depth-preferred replacement (only overwrite if new entry is deeper)
    "depth_replace":    re.compile(
        r"depth.*replace|replace.*depth|depth.prefer"
        r"|if.*depth\s*>.*entry|entry.*depth\s*<.*depth", re.I),
    # TT also consulted in quiescence search (not just main search)
    "tt_in_qsearch":    re.compile(
        r"qsearch.*tt|tt.*qsearch|quiesc.*transpos|transpos.*quiesc"
        r"|tt_probe.*qdepth|qdepth.*tt", re.I),
}

# Broader sub-feature sets for other common features can be added here.
GENERIC_SUBFEATURES: dict[str, dict[str, re.Pattern]] = {
    "Quiescence": QSEARCH_SUBFEATURES,
    "quiescence": QSEARCH_SUBFEATURES,
    "Transposition table": TT_SUBFEATURES,
    "transposition table": TT_SUBFEATURES,
    # ---------------------------------------------------------------------------
    # Algorithmic sub-feature catalogue for Evaluation / PST
    # ---------------------------------------------------------------------------
    "Evaluation/PST": {
        # Core eval
        "material_values":    re.compile(
            r"piece[_ ]?value|PIECE[_ ]VALUE|material[_ ]val|val_pawn|val_queen"
            r"|PIECE.VAL|MATERIAL_VALUES|pieceValue", re.I),
        "pst_table_lookup":   re.compile(
            r"PST\[|pst\[|PAWN_PST|KNIGHT_PST|piece_square_table"
            r"|MG_TABLES|EG_TABLES|PST::|\bpst\b.*\[|PSTABLE", re.I),
        "midgame_tables":     re.compile(
            r"MG_TABLES|midgame.*table|mg_pst|MG_PST|mg_val|mg\[|_mg\b"
            r"|mgTable|midTable|phase.*0", re.I),
        "endgame_tables":     re.compile(
            r"EG_TABLES|endgame.*table|eg_pst|EG_PST|eg_val|eg\[|_eg\b"
            r"|egTable|endTable", re.I),
        "tapered_eval":       re.compile(
            r"tapered|taper|lerp|interpolat|phase.*mg|mg.*eg|eg.*mg"
            r"|game_phase|gamephase|phaseScore|PHASE", re.I),
        "king_safety":        re.compile(
            r"king[_ ]?safety|king[_ ]?attack|king[_ ]?zone|pawn[_ ]?shield"
            r"|king[_ ]?tropism|shelter|KING_SAFETY", re.I),
        "passed_pawn":        re.compile(
            r"passed[_ ]?pawn|PASSED[_ ]PAWN|passedPawn|is_passed|passer", re.I),
        "mobility_terms":     re.compile(
            r"\bmobility\b|MOBILITY|mob_score|mobility_bonus|move_count.*eval"
            r"|attack.*count|attackCount", re.I),
        # Fingerprint: Sunfish piece values (P=100,N=280,B=320,R=479,Q=929,K=60000)
        "sunfish_vals":       re.compile(
            r"\b929\b|\b479\b|\b280\b", re.I),
        # Fingerprint: Wikipedia / CPW simplified (100,320,330,500,900 or 100,300,300,500,900)
        "cpw_simplified":     re.compile(
            r"\b900\b.*\b500\b|\b500\b.*\b900\b|queen.*900|900.*queen"
            r"|QUEEN.*=\s*900|900.*QUEEN|queen_value\s*=\s*900", re.I),
        # Custom positional computation (not table lookup — computed from geometry)
        "computed_positional": re.compile(
            r"centrality|forwardRank|distance.*king|king.*distance"
            r"|rank_of.*bonus|file.*center|center.*bonus|manhattan", re.I),
        # Phase / game-phase component
        "phase_computation":  re.compile(
            r"game_phase|gamephase|count.*phase|PIECE.PHASE|totalPhase"
            r"|phaseMaterial|phase_score", re.I),
        # Side-to-move perspective (negamax flip or explicit)
        "perspective_flip":   re.compile(
            r"stm.*score|score.*side|color.*\*.*score|if.*white|BLACK\s*\*\s*\-1"
            r"|side_to_move.*eval|SIDE.*SCORE|perspective", re.I),
    },
    "Alpha-beta": {
        "negamax":        re.compile(r"negamax|NegaMax", re.I),
        "alpha_update":   re.compile(r"alpha\s*=\s*(?:max|score|best)", re.I),
        "beta_cutoff":    re.compile(r"score\s*>=?\s*beta|beta.cutoff|return\s+beta", re.I),
        "null_move":      re.compile(r"null.move|NMP", re.I),
        "lmr":            re.compile(r"\bLMR\b|late.move.reduct", re.I),
        "pvs":            re.compile(r"\bPVS\b|principal.variation", re.I),
        "tt_probe":       re.compile(r"transposition|tt.probe|hash", re.I),
        "aspiration":     re.compile(r"aspiration", re.I),
        "iterative":      re.compile(r"iterative.deepen|iter.?deep", re.I),
        "check_extension":re.compile(r"check.ext|in.check.*depth", re.I),
    },
}


def _subfeatures_for(feature_name: str) -> dict[str, re.Pattern]:
    for key, d in GENERIC_SUBFEATURES.items():
        if d is not None and key.lower() in feature_name.lower():
            return d
    return {}


# ---------------------------------------------------------------------------
# Token-Jaccard similarity
# ---------------------------------------------------------------------------

_TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*|[0-9]+")

# Language-specific keywords to strip (noise for cross-language comparison)
_LANG_NOISE = frozenset([
    # C/C++/Java/Rust/Go control
    "if", "else", "for", "while", "return", "int", "void", "static", "const",
    "bool", "let", "mut", "fn", "pub", "self", "Self", "true", "false",
    # Python
    "def", "and", "or", "not", "in", "is", "None", "True", "False",
    # COBOL
    "PERFORM", "CALL", "MOVE", "IF", "END", "SECTION", "DIVISION",
    # Ruby
    "do", "end", "nil", "begin",
    # OCaml / Why3 / Lean
    "let", "rec", "fun", "match", "with", "when", "then",
])


def _tokenize(code: str) -> Counter:
    tokens = _TOKEN_RE.findall(code.lower())
    return Counter(t for t in tokens if t not in _LANG_NOISE and len(t) > 1)


def jaccard(a: Counter, b: Counter) -> float:
    intersection = sum((a & b).values())
    union = sum((a | b).values())
    return intersection / union if union else 0.0


def feature_jaccard(vec_a: dict[str, bool], vec_b: dict[str, bool]) -> float:
    keys = set(vec_a) | set(vec_b)
    if not keys:
        return 0.0
    both = sum(1 for k in keys if vec_a.get(k) and vec_b.get(k))
    either = sum(1 for k in keys if vec_a.get(k) or vec_b.get(k))
    return both / either if either else 0.0


# ---------------------------------------------------------------------------
# Sub-feature extraction
# ---------------------------------------------------------------------------

def extract_subfeatures(snippet: str, subfeatures: dict[str, re.Pattern]) -> dict[str, bool]:
    return {name: bool(pat.search(snippet)) for name, pat in subfeatures.items()}


# ---------------------------------------------------------------------------
# Text formatting helpers
# ---------------------------------------------------------------------------

def _heatmap_char(score: float) -> str:
    if score >= 0.80:
        return "██"
    if score >= 0.60:
        return "▓▓"
    if score >= 0.40:
        return "▒▒"
    if score >= 0.20:
        return "░░"
    return "  "


def _pct(f: float) -> str:
    return f"{f * 100:.0f}%"


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------

def load_hotspots(json_path: Path) -> dict[str, dict]:
    """Return {engine_name: {language, snippet, file, ...}} for engines with hotspots."""
    data = json.loads(json_path.read_text(encoding="utf-8"))
    result = {}
    for name, eng in data["engines"].items():
        hs = eng.get("hotspot")
        if hs and hs.get("snippet"):
            result[name] = {
                "language": eng.get("language") or "?",
                "tier": eng.get("tier") or "?",
                "corpus": eng.get("corpus") or "?",
                **hs,
            }
    return result, data["meta"]


def compute_matrices(
    hotspots: dict[str, dict],
    subfeatures: dict[str, re.Pattern],
) -> tuple[dict, dict, dict]:
    """Return (token_matrix, feature_matrix, subfeature_vectors)."""
    names = sorted(hotspots)
    tokens = {n: _tokenize(hotspots[n]["snippet"]) for n in names}
    subf_vecs = {n: extract_subfeatures(hotspots[n]["snippet"], subfeatures) for n in names}

    tok_mat: dict[tuple, float] = {}
    feat_mat: dict[tuple, float] = {}
    for a, b in combinations(names, 2):
        tok_mat[(a, b)] = jaccard(tokens[a], tokens[b])
        feat_mat[(a, b)] = feature_jaccard(subf_vecs[a], subf_vecs[b])

    return tok_mat, feat_mat, subf_vecs


def _text_matrix(
    names: list[str],
    mat: dict[tuple, float],
    label: str,
    top_n: int = 5,
) -> str:
    lines = [f"\n{'='*72}", f"{label} similarity (0–100 %)"]
    # Sort names by average similarity for better layout
    avg = {n: sum(mat.get((min(n, m), max(n, m)), 0) for m in names if m != n) / max(1, len(names) - 1)
           for n in names}
    ordered = sorted(names, key=lambda n: -avg[n])

    # Short labels for table
    short = {n: (n[:18] + "..") if len(n) > 20 else n for n in ordered}
    col_w = max(len(s) for s in short.values()) + 1

    # Header
    header = " " * col_w
    for n in ordered:
        header += short[n][:6].center(8)
    lines.append(header)

    for a in ordered:
        row = short[a].ljust(col_w)
        for b in ordered:
            if a == b:
                row += "  --  "
            else:
                key = (min(a, b), max(a, b))
                s = mat.get(key, 0.0)
                row += f"  {_pct(s):>4s} "
        lines.append(row)

    # Top pairs
    pairs = sorted(mat.items(), key=lambda x: -x[1])
    lines.append(f"\nTop {top_n} most-similar pairs:")
    for (a, b), s in pairs[:top_n]:
        ha = hotspots_global.get(a, {}).get("language", "?")
        hb = hotspots_global.get(b, {}).get("language", "?")
        lines.append(f"  {_pct(s):>4s}  {a} ({ha})  ↔  {b} ({hb})")

    lines.append(f"\nBottom {top_n} least-similar pairs:")
    for (a, b), s in pairs[-top_n:]:
        ha = hotspots_global.get(a, {}).get("language", "?")
        hb = hotspots_global.get(b, {}).get("language", "?")
        lines.append(f"  {_pct(s):>4s}  {a} ({ha})  ↔  {b} ({hb})")

    return "\n".join(lines)


def _text_subfeature_table(
    names: list[str],
    subf_vecs: dict[str, dict[str, bool]],
    subfeatures: dict[str, re.Pattern],
) -> str:
    if not subfeatures:
        return ""
    lines = ["\n" + "=" * 72, "Sub-feature presence matrix  (✓ = detected, · = absent)"]
    feat_names = list(subfeatures)
    col_w = max(len(n) for n in names) + 1

    # Header
    hdr = " " * col_w
    for f in feat_names:
        hdr += f[:10].center(12)
    lines.append(hdr)

    # Count totals
    totals = {f: 0 for f in feat_names}
    for n in sorted(names):
        row = n.ljust(col_w)
        for f in feat_names:
            v = subf_vecs[n].get(f, False)
            row += ("  ✓  " if v else "  ·  ").center(12)
            if v:
                totals[f] += 1
        lines.append(row)

    # Totals row
    tot_row = "TOTAL".ljust(col_w)
    for f in feat_names:
        tot_row += f"  {totals[f]}/{len(names)}  ".center(12)
    lines.append("-" * len(hdr))
    lines.append(tot_row)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# LLM analysis via Claude API
# ---------------------------------------------------------------------------

def _llm_analysis(
    feature_name: str,
    hotspots: dict[str, dict],
    subf_vecs: dict[str, dict[str, bool]],
    subfeatures: dict[str, re.Pattern],
    model: str = "claude-sonnet-4-6",
) -> str:
    try:
        import anthropic
    except ImportError:
        return "ERROR: anthropic package not installed. Run: pip3 install anthropic"

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return "ERROR: ANTHROPIC_API_KEY environment variable not set."

    client = anthropic.Anthropic(api_key=api_key)

    # Build prompt with all snippets
    snippets_block = ""
    for name in sorted(hotspots):
        eng = hotspots[name]
        lang = eng.get("language", "?")
        loc = eng.get("loc", "?")
        file_ = eng.get("file", "?")
        snippet = eng.get("snippet", "")
        # Truncate very long snippets
        if len(snippet) > 1200:
            snippet = snippet[:1200] + "\n... [truncated]"
        snippets_block += (
            f"\n--- ENGINE: {name}  LANGUAGE: {lang}  ({loc} LOC, {file_}) ---\n"
            f"```\n{snippet}\n```\n"
        )

    # Sub-feature summary
    sf_summary = ""
    if subfeatures:
        feat_names = list(subfeatures)
        for name in sorted(hotspots):
            vec = subf_vecs.get(name, {})
            present = [f for f in feat_names if vec.get(f)]
            absent = [f for f in feat_names if not vec.get(f)]
            sf_summary += f"  {name}: present={present}, absent={absent}\n"

    prompt = f"""You are analyzing implementations of **{feature_name}** across {len(hotspots)} chess engines written in different programming languages.

Below are the extracted hotspot functions (the primary function implementing this feature in each engine):

{snippets_block}

Sub-feature detection summary (regex-based, may have false positives/negatives):
{sf_summary}

Please provide a structured analysis covering:

## 1. Algorithmic Core
Is this fundamentally the same algorithm across all implementations? What is the canonical algorithm being implemented? Does it match the standard formulation from chessprogramming.org or textbooks?

## 2. Common Pattern
Describe the "skeleton" shared by most implementations — the invariant structure that appears regardless of language.

## 3. Key Variations
What are the main algorithmic differences (not syntactic)? Group engines by variation:
- Which engines have delta pruning? Which omit it?
- Which use a depth limit? Which do unbounded qsearch?
- Which probe the transposition table?
- Any other meaningful variation?

## 4. Outliers
Are any implementations significantly different — either simpler, more complex, or using a different algorithm entirely?

## 5. Origin Hypothesis
Based on the code patterns, do these look like:
(a) Independent implementations of a common spec (e.g. chessprogramming.org)?
(b) Copies/translations of a single reference implementation?
(c) Genuinely diverse approaches?
Cite specific code patterns that support your hypothesis.

## 6. Cross-Language Translation Quality
For the subset of languages where you can judge (C, Python, Rust, Java, Ruby, OCaml): how faithfully does each implementation translate the algorithm? Are there translation artifacts or language-idiomatic improvements?

Be concise and specific. Reference engine names and languages when making claims."""

    response = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


# ---------------------------------------------------------------------------
# Report assembly
# ---------------------------------------------------------------------------

hotspots_global: dict = {}  # set before matrix calls so top/bottom pairs can look up lang


def build_report(
    feature_name: str,
    hotspots: dict[str, dict],
    tok_mat: dict,
    feat_mat: dict,
    subf_vecs: dict,
    subfeatures: dict,
    meta: dict,
) -> str:
    names = sorted(hotspots)
    lines = [
        "=" * 72,
        f"COMPARISON REPORT  —  Feature: {feature_name}",
        f"Engines analysed: {len(names)} / {meta['total_engines']} total",
        f"(engines missing quiescence: see notes below)",
        "=" * 72,
        "",
        "Legend: engines without hotspot extraction (no quiescence detected):",
    ]
    for n, eng in sorted(meta.get("_engines_raw", {}).items()):
        pass  # filled below if needed

    lines.append(_text_subfeature_table(names, subf_vecs, subfeatures))
    lines.append(_text_matrix(names, feat_mat, "Feature-Jaccard", top_n=8))
    lines.append(_text_matrix(names, tok_mat, "Token-Jaccard", top_n=8))

    # Per-engine summary line
    lines.append("\n" + "=" * 72)
    lines.append("Per-engine summary")
    lines.append("-" * 72)
    for n in names:
        eng = hotspots[n]
        lang = eng.get("language", "?")
        loc = eng.get("loc", 0)
        file_ = eng.get("file", "?")
        avg_tok = sum(
            tok_mat.get((min(n, m), max(n, m)), 0)
            for m in names if m != n
        ) / max(1, len(names) - 1)
        avg_feat = sum(
            feat_mat.get((min(n, m), max(n, m)), 0)
            for m in names if m != n
        ) / max(1, len(names) - 1)
        lines.append(
            f"  {n:45s} {lang:12s}  {loc:4d} LOC  "
            f"avg-tok={_pct(avg_tok)}  avg-feat={_pct(avg_feat)}  {file_}"
        )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--input", required=True, metavar="JSON",
                   help="Path to the .json produced by feature_locator.py --hotspot")
    p.add_argument("--llm", action="store_true",
                   help="Call Claude API for qualitative analysis (needs ANTHROPIC_API_KEY)")
    p.add_argument("--model", default="claude-sonnet-4-6",
                   help="Claude model to use for LLM analysis (default: claude-sonnet-4-6)")
    p.add_argument("--output", metavar="DIR",
                   help="Output directory (default: same directory as --input)")
    args = p.parse_args(argv)

    json_path = Path(args.input)
    if not json_path.exists():
        sys.exit(f"ERROR: {json_path} not found. Run feature_locator.py --hotspot first.")

    hotspots, meta = load_hotspots(json_path)
    global hotspots_global
    hotspots_global = hotspots

    print(f"Loaded {len(hotspots)} engine hotspots from {json_path.name}")
    feature_name = meta.get("feature", json_path.stem)

    subfeatures = _subfeatures_for(feature_name)
    if subfeatures:
        print(f"Using {len(subfeatures)} sub-feature detectors for '{feature_name}'")
    else:
        print("No sub-feature catalogue for this feature; running token-Jaccard only.")

    print("Computing similarity matrices…")
    tok_mat, feat_mat, subf_vecs = compute_matrices(hotspots, subfeatures)

    out_dir = Path(args.output) if args.output else json_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^a-zA-Z0-9_-]", "_", feature_name.lower())

    report_txt = build_report(feature_name, hotspots, tok_mat, feat_mat, subf_vecs, subfeatures, meta)
    compare_path = out_dir / f"{safe}.compare.txt"
    compare_path.write_text(report_txt, encoding="utf-8")
    print(f"Comparison report: {compare_path}")

    # JSON dump
    compare_json = {
        "meta": meta,
        "feature": feature_name,
        "engines": {
            n: {
                "language": hotspots[n]["language"],
                "loc": hotspots[n]["loc"],
                "file": hotspots[n]["file"],
                "subfeatures": subf_vecs.get(n, {}),
                "avg_token_jaccard": sum(
                    tok_mat.get((min(n, m), max(n, m)), 0) for m in hotspots if m != n
                ) / max(1, len(hotspots) - 1),
                "avg_feature_jaccard": sum(
                    feat_mat.get((min(n, m), max(n, m)), 0) for m in hotspots if m != n
                ) / max(1, len(hotspots) - 1),
            }
            for n in hotspots
        },
        "pairwise_token_jaccard": {f"{a}|||{b}": v for (a, b), v in tok_mat.items()},
        "pairwise_feature_jaccard": {f"{a}|||{b}": v for (a, b), v in feat_mat.items()},
    }
    json_out = out_dir / f"{safe}.compare.json"
    json_out.write_text(json.dumps(compare_json, indent=2), encoding="utf-8")
    print(f"Comparison JSON : {json_out}")

    if args.llm:
        print("Calling Claude API for qualitative analysis…")
        analysis = _llm_analysis(feature_name, hotspots, subf_vecs, subfeatures, model=args.model)
        analysis_path = out_dir / f"{safe}.analysis.txt"
        analysis_path.write_text(analysis, encoding="utf-8")
        print(f"LLM analysis    : {analysis_path}")
        print("\n" + "=" * 72)
        print(analysis)
    else:
        print("\nRun with --llm to get Claude's qualitative analysis.")


if __name__ == "__main__":
    main()
