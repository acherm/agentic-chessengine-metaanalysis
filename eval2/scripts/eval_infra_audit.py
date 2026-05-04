"""Populate tab_eval_infra by auditing each engine repo for evaluation
infrastructure the agent set up: cutechess invocation, custom Elo
scripts, Stockfish gauntlets, perft tests, random baselines, self-play,
and test-file counts.
"""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "lib"))
import manifest  # noqa: E402

LANGS = {
    "chess-purec": "C", "chess-purec-codex": "C",
    "chess-cplusplus-claude": "C++", "cplusplus-chess": "C++",
    "chess-rust-cc": "Rust", "chess-rust-codex": "Rust",
    "chess-rust-cc-redo": "Rust",
    "chess-java-cc": "Java", "chess-java": "Java",
    "chess-py": "Python", "chess-py-cc": "Python",
    "chess-ruby-cc": "Ruby", "chess-ruby-codex": "Ruby",
    "chess-Rocq": r"Rocq$\to$OCaml", "chess-why3-cc": r"Why3$\to$C",
    "chess-why3": r"Why3$\to$OCaml", "lean-chess": "Lean 4",
    "COBOL-chess": "COBOL", "chess-cobol-cc": "COBOL",
    "chess-icon-codex": "Icon", "chess-apl-codex54": "APL",
    "chess-css-codex": "CSS/HTML", "chess-css-codex-guided": "CSS/HTML",
    "chess-css-cc": "CSS/HTML",
    "chess-assembly-codex": "Assembly",
    "chess-brainfuck": "Brainfuck", "chess-brainfuck-cc": "Brainfuck",
    "chess-sql": "SQL", "chess-mojo": "Mojo",
    "chess-latex-codex-replication": "LaTeX",
    "latex-chess-engine": "LaTeX (TeX)",
    "chess-revisit-java-toRust-codex": r"Java$\to$Rust port",
    "chess-revisit-java-toCOBOL-codex": r"Java$\to$COBOL port",
    "chess-newlang-codex": "DSL (newlang)",
}


def search_repo(path: Path, patterns: list[str]) -> bool:
    """True if any of `patterns` appear in any text file under `path` (skipping target/, node_modules, .git)."""
    if not path or not path.is_dir(): return False
    skip = {".git", "target", "node_modules", "_build", ".lake", "__pycache__", "build"}
    for f in path.rglob("*"):
        if not f.is_file(): continue
        if any(part in skip for part in f.parts): continue
        if f.suffix.lower() not in {".py", ".sh", ".md", ".rs", ".java", ".c", ".cpp", ".h",
                                    ".rb", ".ml", ".v", ".go", ".js", ".ts", ".yml", ".yaml",
                                    ".toml", ".json", ".cob", ".cbl", ".s", ".asm", ".tex",
                                    ".sql", ".bf", ".icn", ".apl", ".lean", ""}:
            continue
        try:
            data = f.read_text(encoding="utf-8", errors="ignore").lower()
        except OSError:
            continue
        if any(p in data for p in patterns):
            return True
    return False


def has_file(path: Path, glob: str) -> bool:
    if not path or not path.is_dir(): return False
    return any(True for _ in path.rglob(glob) if all(s not in _.parts for s in (".git","target","_build","__pycache__","node_modules","build")))


def count_tests(path: Path) -> int:
    if not path or not path.is_dir(): return 0
    n = 0
    skip = {".git", "target", "_build", "__pycache__", "node_modules", "build"}
    for f in path.rglob("*"):
        if not f.is_file(): continue
        if any(s in f.parts for s in skip): continue
        nm = f.name.lower()
        if (nm.startswith("test_") or nm.endswith("_test.py") or nm.endswith("_test.go") or
            nm.endswith("_test.rs") or nm.startswith("test") and f.suffix == ".py" or
            "/tests/" in str(f).replace("\\", "/")):
            n += 1
    return n


def audit(name: str, path_str: str) -> dict:
    p = Path(path_str) if path_str else None
    cute = search_repo(p, ["cutechess-cli", "cutechess_cli", "cutechess.exe", "cutechess "])
    elo = search_repo(p, ["elo_estimate", "estimate_elo", "elo_test", "rating_estimate",
                          "calc_elo", "compute_elo", "elo_match", "play_match"])
    sf = search_repo(p, ["uci_limitstrength", "uci_elo", "stockfish", "limitstrength"])
    perft = (search_repo(p, ["perft(", "perft_test", "perft_count", "perft_command",
                             "test_perft", "kiwipete"]) or
             has_file(p, "*perft*"))
    rand = search_repo(p, ["random_mover", "random_opponent", "play_random", "randomengine"])
    self_play = search_repo(p, ["self_play", "selfplay", "self-play"])
    n_tests = count_tests(p)
    return {"cute": cute, "elo": elo, "sf": sf, "perft": perft,
            "rand": rand, "self": self_play, "n_tests": n_tests}


def main() -> None:
    engs, _ = manifest.load()
    rows = []
    for e in engs:
        if e.corpus not in ("main", "port", "dsl", "failure"): continue
        a = audit(e.name, e.path)
        rows.append({"engine": e.name, "lang": LANGS.get(e.name, e.tier or "?"), **a})
    rows.sort(key=lambda r: r["engine"].lower())

    out = [
        r"\begin{table}[ht]\centering\scriptsize",
        r"\caption{Evaluation infrastructure each agent set up without explicit user instruction. Cute.: cutechess-cli invoked. CustomElo: bespoke Elo-estimation script in the repo. SF: \stockfish{} gauntlet (with or without \texttt{UCI\_LimitStrength}). Perft: perft test code or harness present. Rand.: random-baseline opponent invoked. Self: self-play harness. \#Tests: count of test files at any depth. Detected from repository contents at corpus snapshot.}",
        r"\label{tab:eval-infra}",
        r"\resizebox{\textwidth}{!}{%",
        r"\begin{tabular}{l l c c c c c c r}",
        r"\toprule",
        r"Engine & Language & Cute. & CustomElo & SF & Perft & Rand. & Self & \#Tests \\",
        r"\midrule",
    ]
    c = lambda b: r"$\checkmark$" if b else " "
    for r in rows:
        eng = r["engine"].replace("_", r"\_")
        out.append(f"\\texttt{{{eng}}} & {r['lang']} & "
                   f"{c(r['cute'])} & {c(r['elo'])} & {c(r['sf'])} & "
                   f"{c(r['perft'])} & {c(r['rand'])} & {c(r['self'])} & {r['n_tests']} \\\\")
    out += [r"\bottomrule", r"\end{tabular}}", r"\end{table}"]

    out_tex = ROOT.parent / "paper" / "tables" / "tab_eval_infra.tex"
    out_tex.write_text("\n".join(out) + "\n")
    print(f"wrote {out_tex}")
    # quick coverage print
    pop = lambda k: sum(1 for r in rows if r[k])
    print(f"  cute={pop('cute')}/{len(rows)}  elo={pop('elo')}/{len(rows)}  "
          f"sf={pop('sf')}/{len(rows)}  perft={pop('perft')}/{len(rows)}  "
          f"rand={pop('rand')}/{len(rows)}  self={pop('self')}/{len(rows)}")


if __name__ == "__main__":
    main()
