"""Q4 — search-algorithm feature inventory.

For each engine in the manifest (corpus=main, not skipped), grep its
source files for canonical search-algorithm keyword strings. Build a
presence matrix and a per-engine "algorithm count" (out of a fixed
catalogue of 18 well-known techniques).

Output: results/algo_inventory.md with a markdown table + counts.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "lib"))
import manifest

# Catalogue: (label, list of regex alternatives, case-insensitive).
# A feature is "present" if ANY of its patterns is found in any source file.
SEARCH_FEATURES: list[tuple[str, list[str]]] = [
    ("alpha-beta",     [r"\balpha[\s_-]*beta\b", r"\bAB\b", r"alphaBeta", r"alpha_beta"]),
    ("PVS",            [r"\bPVS\b", r"principal[\s_-]*variation", r"\bzero[\s_-]*window\b"]),
    ("LMR",            [r"\bLMR\b", r"late[\s_-]*move[\s_-]*reduction"]),
    ("LMP",            [r"\bLMP\b", r"late[\s_-]*move[\s_-]*pruning"]),
    ("NMP",            [r"\bNMP\b", r"null[\s_-]*move[\s_-]*pruning", r"null_move", r"nullMove"]),
    ("TT",             [r"transposition", r"\bTT\b", r"\bttable\b", r"hash[\s_-]*table"]),
    ("Zobrist",        [r"zobrist"]),
    ("aspiration",     [r"aspiration[\s_-]*window", r"aspiration"]),
    ("futility",       [r"futility[\s_-]*pruning", r"futility"]),
    ("razor",          [r"razor"]),
    ("killer",         [r"killer[\s_-]*move", r"\bkillers?\b"]),
    ("history-heur",   [r"history[\s_-]*heuristic", r"history[\s_-]*table", r"\bhistory\b"]),
    ("counter-move",   [r"counter[\s_-]*move", r"counterMove"]),
    ("MVV-LVA",        [r"\bMVV[\s_-]*LVA\b", r"\bMVV\b"]),
    ("SEE",            [r"\bSEE\b", r"static[\s_-]*exchange"]),
    ("IID",            [r"\bIID\b", r"internal[\s_-]*iterative[\s_-]*deepening"]),
    ("quiescence",     [r"quiescence", r"\bqsearch\b", r"\bqs\b\("]),
    ("iterative-deep", [r"iterative[\s_-]*deepening", r"iter[\s_-]*deep"]),
    ("repetition",     [r"repetition", r"3[\s_-]*fold", r"threefold"]),
    ("50-move",        [r"50[\s_-]*move", r"fifty[\s_-]*move", r"halfmove[\s_-]*clock"]),
]

# Source-file extensions we'll grep.
SOURCE_EXTS = {".c", ".h", ".cc", ".cpp", ".hpp", ".rs", ".java", ".py",
               ".rb", ".ml", ".mli", ".v", ".lean", ".lean4", ".ts", ".js",
               ".cob", ".cbl", ".cpy", ".s", ".asm", ".icn", ".apl", ".sql",
               ".gmb", ".bf", ".tex", ".mlw"}

# Skip dirs that don't contain real source.
SKIP_DIRS = {".git", "target", "build", "_build", ".lake", "node_modules",
             "__pycache__", "results", "elo_results", "tournaments",
             "benchmarks", "match-2200", "matches", "tests"}


def collect_sources(root: Path) -> list[Path]:
    out = []
    for p in root.rglob("*"):
        if not p.is_file(): continue
        if any(part in SKIP_DIRS for part in p.parts): continue
        if p.suffix.lower() in SOURCE_EXTS:
            out.append(p)
    return out


def text_blob(paths: list[Path]) -> str:
    chunks = []
    for p in paths:
        try:
            chunks.append(p.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            continue
    return "\n".join(chunks)


def feature_hits(blob: str) -> dict[str, bool]:
    hits = {}
    for label, patterns in SEARCH_FEATURES:
        hit = any(re.search(p, blob, re.IGNORECASE) for p in patterns)
        hits[label] = hit
    return hits


def main() -> None:
    engs, _ = manifest.load()
    rows = []
    for e in engs:
        if e.corpus != "main":
            continue
        if not e.path or not Path(e.path).is_dir():
            continue
        srcs = collect_sources(Path(e.path))
        blob = text_blob(srcs)
        hits = feature_hits(blob)
        count = sum(1 for v in hits.values() if v)
        rows.append({"engine": e.name, "tier": e.tier, "n_files": len(srcs),
                     "blob_kb": len(blob) // 1024, "count": count, "hits": hits})

    rows.sort(key=lambda r: -r["count"])

    # Output
    labels = [l for l, _ in SEARCH_FEATURES]
    out = ["# Search-algorithm inventory (Q4)", "",
           "Per-engine grep for canonical search-algorithm keyword strings.",
           "Each cell is ✓ if at least one pattern for that technique appears in the engine's source.",
           f"Catalogue: {len(labels)} techniques.",
           "",
           "| Engine | Tier | Count | " + " | ".join(labels) + " |",
           "|---|---|---:|" + "|".join([":---:"] * len(labels)) + "|"]
    for r in rows:
        marks = ["✓" if r["hits"][l] else " " for l in labels]
        out.append(f"| {r['engine']} | {r['tier']} | {r['count']}/{len(labels)} | " + " | ".join(marks) + " |")
    out.append("")
    out.append("## Summary")
    out.append("")
    out.append(f"- Engines analysed: {len(rows)}")
    out.append(f"- Median feature count: {sorted([r['count'] for r in rows])[len(rows)//2] if rows else 0}")
    out.append(f"- Top-feature engines (≥15): " + ", ".join(r["engine"] for r in rows if r["count"] >= 15))
    out.append(f"- Sparse-feature engines (≤5): " + ", ".join(r["engine"] for r in rows if r["count"] <= 5))

    out_path = HERE / "results" / "algo_inventory.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(out) + "\n")
    print(f"wrote {out_path}")
    for r in rows:
        print(f"  {r['engine']:<35} {r['count']:>2}/{len(labels)} features  ({r['n_files']} files, {r['blob_kb']} KB)")


if __name__ == "__main__":
    main()
