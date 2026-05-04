"""Q6 — eval / domain-knowledge inventory (mirror of Q4 for chess knowledge).

For each engine, grep for evaluation-feature keyword strings AND count
tuned constants in eval-related source files (proxy for tuning effort).

Output: results/eval_inventory.md.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "lib"))
import manifest

# Catalogue of 22 eval / chess-knowledge features.
EVAL_FEATURES: list[tuple[str, list[str]]] = [
    # Material / piece-square tables
    ("PSQT",           [r"\bPSQT\b", r"piece[\s_-]*square[\s_-]*table", r"piece_square"]),
    ("tapered-eval",   [r"taper", r"middlegame.*endgame", r"midgame.*endgame", r"\bphase\b.*\beval\b"]),
    # Pawn structure
    ("passed-pawn",    [r"passed[\s_-]*pawn"]),
    ("isolated-pawn",  [r"isolated[\s_-]*pawn"]),
    ("doubled-pawn",   [r"doubled[\s_-]*pawn"]),
    ("backward-pawn",  [r"backward[\s_-]*pawn"]),
    ("pawn-chain",     [r"pawn[\s_-]*chain", r"connected[\s_-]*pawn"]),
    # King safety
    ("king-safety",    [r"king[\s_-]*safety", r"king[\s_-]*shelter", r"king[\s_-]*shield"]),
    ("pawn-shield",    [r"pawn[\s_-]*shield", r"pawn[\s_-]*storm"]),
    ("king-zone",      [r"king[\s_-]*zone", r"king[\s_-]*ring", r"king[\s_-]*attackers"]),
    # Piece-specific positional terms
    ("bishop-pair",    [r"bishop[\s_-]*pair"]),
    ("rook-open-file", [r"rook.*open[\s_-]*file", r"open[\s_-]*file.*rook"]),
    ("rook-7th-rank",  [r"rook.*7th", r"rook.*seventh", r"rook_on_seventh"]),
    ("knight-outpost", [r"knight[\s_-]*outpost", r"\boutpost\b"]),
    ("bad-bishop",     [r"bad[\s_-]*bishop"]),
    # Mobility
    ("mobility",       [r"\bmobility\b"]),
    # Center / space
    ("center-control", [r"center[\s_-]*control", r"\bcentre[\s_-]*control"]),
    ("space-eval",     [r"\bspace[\s_-]*(eval|score|bonus)"]),
    # Endgame knowledge
    ("endgame-table",  [r"endgame[\s_-]*table", r"\bsyzygy\b", r"\bgaviota\b"]),
    ("KPK",            [r"\bKPK\b", r"king.*pawn.*king", r"king_pawn_king"]),
    # Misc
    ("tempo",          [r"\btempo[\s_-]*(bonus|eval|score)"]),
    ("contempt",       [r"contempt"]),
]

SOURCE_EXTS = {".c", ".h", ".cc", ".cpp", ".hpp", ".rs", ".java", ".py",
               ".rb", ".ml", ".mli", ".v", ".lean", ".lean4", ".ts", ".js",
               ".cob", ".cbl", ".cpy", ".s", ".asm", ".icn", ".apl", ".sql",
               ".gmb", ".bf", ".tex", ".mlw"}
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


def eval_files(srcs: list[Path]) -> list[Path]:
    """Heuristic: files whose name contains 'eval', 'evaluate', 'evaluation',
    or 'score' (excluding test/spec). Falls back to all source if none."""
    keep = []
    for p in srcs:
        n = p.name.lower()
        if any(k in n for k in ("eval", "evaluate", "evaluation", "score")) \
           and "test" not in n and "spec" not in n:
            keep.append(p)
    return keep or srcs


def text_blob(paths: list[Path]) -> str:
    chunks = []
    for p in paths:
        try:
            chunks.append(p.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            continue
    return "\n".join(chunks)


def count_tuned_constants(blob: str) -> int:
    """Heuristic count of integer/float literals in an eval blob.
    Excludes 0, 1, 2 (common indices), bit-pattern hex, and 8/64/128
    (board sizes). Counts a value as a likely tuned constant if it's
    a number ≥10 and ≤32000."""
    # Match integers and floats, exclude common board/bit constants.
    nums = re.findall(r"\b(\d{2,5})\b", blob)
    EXCLUDE = {"10", "16", "32", "64", "100", "128", "256", "512",
               "1000", "1024", "2048", "4096", "8192", "16384", "32768"}
    filtered = [n for n in nums if n not in EXCLUDE and 10 <= int(n) <= 32000]
    return len(filtered)


def feature_hits(blob: str) -> dict[str, bool]:
    return {label: any(re.search(p, blob, re.IGNORECASE) for p in patterns)
            for label, patterns in EVAL_FEATURES}


def main() -> None:
    engs, _ = manifest.load()
    rows = []
    for e in engs:
        if e.corpus != "main":
            continue
        if not e.path or not Path(e.path).is_dir():
            continue
        all_srcs = collect_sources(Path(e.path))
        eval_srcs = eval_files(all_srcs)
        blob = text_blob(eval_srcs)
        hits = feature_hits(blob)
        count = sum(1 for v in hits.values() if v)
        consts = count_tuned_constants(blob)
        rows.append({"engine": e.name, "tier": e.tier,
                     "n_eval_files": len(eval_srcs), "blob_kb": len(blob) // 1024,
                     "count": count, "constants": consts, "hits": hits})

    # Two sortings: by feature count, by constant count
    rows.sort(key=lambda r: (-r["count"], -r["constants"]))

    labels = [l for l, _ in EVAL_FEATURES]
    out = ["# Eval / domain-knowledge inventory (Q6)", "",
           "Mirror of Q4 for chess-knowledge features in evaluation code.",
           "Each cell is ✓ if a pattern for that eval term appears in the engine's eval-related source files.",
           "**Tuned constants** is a count of integer literals (10..32000) in eval files — a proxy for how much",
           "weight tuning the eval has received (a serious eval has hundreds; a sketch has dozens).",
           f"Catalogue: {len(labels)} eval features.",
           "",
           "| Engine | Tier | Eval features | Tuned constants | " + " | ".join(labels) + " |",
           "|---|---|---:|---:|" + "|".join([":---:"] * len(labels)) + "|"]
    for r in rows:
        marks = ["✓" if r["hits"][l] else " " for l in labels]
        out.append(f"| {r['engine']} | {r['tier']} | {r['count']}/{len(labels)} | {r['constants']} | "
                   + " | ".join(marks) + " |")

    out.append("")
    out.append("## Summary")
    out.append("")
    out.append(f"- Engines analysed: {len(rows)}")
    out.append(f"- Median eval feature count: {sorted([r['count'] for r in rows])[len(rows)//2] if rows else 0}")
    out.append(f"- Median tuned-constant count: {sorted([r['constants'] for r in rows])[len(rows)//2] if rows else 0}")
    out.append(f"- Eval-rich engines (≥10 features): " + ", ".join(r["engine"] for r in rows if r["count"] >= 10))
    out.append(f"- Eval-poor engines (≤3 features): " + ", ".join(r["engine"] for r in rows if r["count"] <= 3))

    out_path = HERE / "results" / "eval_inventory.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(out) + "\n")
    print(f"wrote {out_path}")
    for r in rows:
        print(f"  {r['engine']:<35} {r['count']:>2}/{len(labels)} features, "
              f"{r['constants']:>4} tuned constants, {r['n_eval_files']} eval files")


if __name__ == "__main__":
    main()
