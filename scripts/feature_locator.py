#!/usr/bin/env python3
"""feature_locator.py — Locate feature implementations across all chess engines.

Find every file + line where a named chess feature (e.g. quiescence search,
alpha-beta, transposition table) appears, with surrounding code context.
Results are written as JSON for programmatic analysis and as a readable text
summary for manual review.

Usage examples
--------------
# List all known features:
  python3 scripts/feature_locator.py --list-features

# Locate a known feature (from CHESS_PATTERNS in common.py):
  python3 scripts/feature_locator.py --feature "Quiescence"

# Ad-hoc regex pattern (with an explicit label):
  python3 scripts/feature_locator.py --pattern "quiesc|qsearch|q_search" --name "quiescence"

# More context lines, restrict to one engine, save elsewhere:
  python3 scripts/feature_locator.py --feature "Alpha-beta" --context 6 \\
      --engine chess-purec --output reports/features/

# Multiple patterns for the same feature concept:
  python3 scripts/feature_locator.py \\
      --pattern "null[_ -]?move" --pattern "NMP" --name "null_move_pruning"

Output
------
  reports/features/<name>.json   — structured JSON (all engines × matches)
  reports/features/<name>.txt    — human-readable summary
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Make sure the scripts/ package is importable regardless of CWD.
_SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS_DIR))

from common import CHESS_PATTERNS, EXT_TO_LANG, IGNORED_DIRS, primary_language, compute_loc

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

META_DIR = _SCRIPTS_DIR.parent
MANIFEST_PATH = META_DIR / "eval2" / "manifest.yaml"
DEFAULT_OUTPUT_DIR = META_DIR / "reports" / "features"

# File suffixes we never want to open (binary / build artifacts).
_BINARY_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".svg",
    ".pdf", ".zip", ".tar", ".gz", ".bz2", ".xz", ".7z",
    ".bin", ".exe", ".o", ".so", ".dylib", ".a", ".lib",
    ".class", ".jar", ".pyc", ".pyo",
    ".wasm", ".woff", ".woff2", ".ttf", ".otf",
    ".mp3", ".mp4", ".avi", ".mov",
}

# Max bytes per file before we skip (avoid huge PGN dumps, etc.).
_MAX_FILE_BYTES = 2_000_000

# Languages considered "non-code" for --code-only mode.
_NON_CODE_LANGS = {"Markdown", "Text", "JSON", "YAML", "TOML", "XML"}


# ---------------------------------------------------------------------------
# Manifest reader (stdlib YAML-free, handles simple YAML lists)
# ---------------------------------------------------------------------------

def _load_engines_from_manifest(manifest: Path) -> list[dict]:
    """Parse manifest.yaml with stdlib (no PyYAML dependency).

    Returns list of dicts with at least: name, path, tier, corpus.
    Only handles the simple scalar-value YAML produced by this project.
    """
    import re as _re
    engines: list[dict] = []
    current: dict | None = None
    list_started = False

    with manifest.open("r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            stripped = line.strip()

            if stripped.startswith("#") or not stripped:
                continue

            # New engine entry
            if _re.match(r"^\s{0,2}-\s+name:", line):
                if current:
                    engines.append(current)
                current = {}
                m = _re.match(r"^\s*-\s+name:\s*(.+)$", line)
                if m:
                    current["name"] = m.group(1).strip()
                continue

            if current is None:
                # e.g. "engines:" header line
                continue

            # key: value pairs (indented under current engine)
            m = _re.match(r"^\s+(\w+):\s*(.*)", line)
            if m:
                key, val = m.group(1), m.group(2).strip()
                # Strip inline comments
                if " #" in val:
                    val = val[: val.index(" #")].strip()
                # Strip surrounding quotes
                val = val.strip('"').strip("'")
                # Booleans
                if val.lower() == "true":
                    val = True
                elif val.lower() == "false":
                    val = False
                current[key] = val

    if current:
        engines.append(current)

    return engines


# ---------------------------------------------------------------------------
# Core: line-level search
# ---------------------------------------------------------------------------

def _iter_source_files(root: Path, code_only: bool = False):
    """Yield (Path, relative_str) for every searchable source file under root."""
    for dirpath, dirnames, filenames in os.walk(root):
        # Prune ignored directories in-place.
        dirnames[:] = [
            d for d in dirnames
            if d not in IGNORED_DIRS and not d.startswith(".")
        ]
        for fname in sorted(filenames):
            if fname.startswith("."):
                continue
            p = Path(dirpath) / fname
            if p.suffix.lower() in _BINARY_SUFFIXES:
                continue
            # Only code / text files (suffix must be known or be extensionless).
            ext = p.suffix.lower()
            if ext and ext not in EXT_TO_LANG:
                continue
            if code_only and EXT_TO_LANG.get(ext) in _NON_CODE_LANGS:
                continue
            try:
                if p.stat().st_size > _MAX_FILE_BYTES:
                    continue
            except OSError:
                continue
            yield p, str(p.relative_to(root))


def search_engine(
    engine_path: Path,
    patterns: list[re.Pattern],
    context: int = 3,
    code_only: bool = False,
) -> list[dict]:
    """Search one engine directory; return list of match dicts."""
    matches: list[dict] = []

    for file_path, rel in _iter_source_files(engine_path, code_only=code_only):
        try:
            raw = file_path.read_bytes()
            text = raw.decode("utf-8", errors="replace")
        except OSError:
            continue

        lines = text.splitlines()
        for lineno, line_text in enumerate(lines, start=1):
            for pat in patterns:
                if pat.search(line_text):
                    lo = max(0, lineno - 1 - context)
                    hi = min(len(lines), lineno + context)
                    ctx = [
                        {
                            "line": lo + i + 1,
                            "text": lines[lo + i],
                            "match": (lo + i + 1 == lineno),
                        }
                        for i in range(hi - lo)
                    ]
                    matches.append(
                        {
                            "file": rel,
                            "line": lineno,
                            "text": line_text,
                            "pattern": pat.pattern,
                            "context": ctx,
                        }
                    )
                    break  # one match per line is enough

    return matches


# ---------------------------------------------------------------------------
# Hotspot extraction: find the enclosing function for the best match
# ---------------------------------------------------------------------------

# File extension → language family for function-boundary detection.
_EXT_TO_FAMILY: dict[str, str] = {
    ".c": "brace",   ".h": "brace",   ".cpp": "brace", ".cc": "brace",
    ".cxx": "brace", ".hpp": "brace", ".hh": "brace",
    ".java": "brace", ".rs": "brace", ".go": "brace",
    ".js": "brace",  ".mjs": "brace", ".ts": "brace",  ".tsx": "brace",
    ".cs": "brace",  ".kt": "brace",  ".scala": "brace",
    ".swift": "brace", ".zig": "brace", ".d": "brace",
    ".py": "indent",  ".mojo": "indent",
    ".rb": "ruby",
    ".lua": "lua",
    ".icn": "keyword_end",
    ".ml": "ocaml",   ".mli": "ocaml",
    ".why": "ocaml",  ".mlw": "ocaml",  ".whyml": "ocaml",
    ".v": "coq",
    ".lean": "lean",
    ".cob": "cobol",  ".cbl": "cobol",  ".cobol": "cobol",
    ".s": "asm",  ".S": "asm",  ".asm": "asm",  ".nasm": "asm",
    ".apl": "apl",  ".dyalog": "apl",
    ".sql": "sql",
}

_CTRL_FLOW = re.compile(
    r"^\s*(if|else|elif|for|while|switch|do|catch|try|return|case|break|"
    r"continue|throw|raise|unless|until|end|pass|assert|print)\b"
)
_COMMENT_LINE = re.compile(r"^\s*(?://|/\*|\*|#|--|\(\*|;)")


_BRACE_FUNC_HEADER = re.compile(
    # Optional access/storage modifiers
    r"^\s*(?:(?:pub(?:\([^)]*\))?|private|protected|public|static|async|override|"
    r"virtual|inline|extern|constexpr|template\s*<[^>]*>|unsafe|final)\s+)*"
    # Return type and function name with open-paren somewhere on the line
    r"(?:[\w*&<>:,\[\]]+\s+){0,5}\w[\w<>:,*&]*\s*\([^;{(]*\)"
    r"(?:\s*(?:const|noexcept|override|->[\w<>:,*&\s]+))?\s*\{?\s*(?://.*)?$"
)


def _brace_extract(lines: list[str], match_idx: int, max_lines: int = 120) -> tuple[int, int]:
    """Brace-language extractor. All indices 0-based.

    Walks backward from match_idx to find the nearest function-header line
    (a line with identifier(params) that is not control-flow or a comment),
    then finds the matching closing brace.
    """
    n = len(lines)

    # Cumulative brace depth BEFORE each line (used only for finding closing }).
    depths = [0] * (n + 1)
    for i, ln in enumerate(lines):
        depths[i + 1] = depths[i] + ln.count("{") - ln.count("}")

    # Walk backward (inclusive of match_idx) for a function-header line.
    header_idx = max(0, match_idx - max_lines)
    for i in range(match_idx, max(0, match_idx - max_lines) - 1, -1):
        ln = lines[i]
        if not ln.strip() or _COMMENT_LINE.match(ln):
            continue
        if _CTRL_FLOW.match(ln):
            continue
        # Function header: has identifier(params) and looks like a declaration.
        if (
            _BRACE_FUNC_HEADER.match(ln)
            or re.match(r"\s*(?:fn|func)\s+\w", ln)
        ):
            header_idx = i
            break

    # Scan forward from header to find the opening {.
    open_idx = header_idx
    for i in range(header_idx, min(n, header_idx + 10)):
        if "{" in lines[i]:
            open_idx = i
            break

    # Find the matching } by tracking depth from the opening {.
    depth_at_open = depths[open_idx]
    func_end = min(n - 1, open_idx + max_lines)
    for i in range(open_idx + 1, min(n, open_idx + max_lines + 1)):
        if depths[i + 1] <= depth_at_open:
            func_end = i
            break

    return header_idx, func_end


def _indent_extract(lines: list[str], match_idx: int, max_lines: int = 120) -> tuple[int, int]:
    """Python-style indentation extractor."""
    n = len(lines)

    def indent_of(ln: str) -> int:
        return len(ln) - len(ln.lstrip())

    match_indent = indent_of(lines[match_idx]) if lines[match_idx].strip() else 999

    # Walk backward for `def` at same-or-lower indent (include match line itself).
    header_idx = max(0, match_idx - max_lines)
    for i in range(match_idx, max(0, match_idx - max_lines) - 1, -1):
        ln = lines[i]
        if re.match(r"\s*(?:async\s+)?def\s+\w", ln):
            if indent_of(ln) <= match_indent:
                header_idx = i
                break

    header_indent = indent_of(lines[header_idx])

    # Walk forward until a non-blank line returns to the same/lower indent.
    func_end = min(n - 1, header_idx + max_lines)
    for i in range(header_idx + 1, min(n, header_idx + max_lines)):
        ln = lines[i]
        if ln.strip() and not ln.strip().startswith("#"):
            if indent_of(ln) <= header_indent and i > header_idx + 1:
                func_end = i - 1
                break
    else:
        func_end = min(n - 1, header_idx + max_lines)

    return header_idx, func_end


def _keyword_end_extract(
    lines: list[str],
    match_idx: int,
    max_lines: int,
    opener: re.Pattern,
    nested_openers: re.Pattern | None = None,
) -> tuple[int, int]:
    """Generic keyword/end extractor (Ruby, Lua, Icon, …)."""
    n = len(lines)
    closer = re.compile(r"^\s*end\b")

    header_idx = max(0, match_idx - max_lines)
    for i in range(match_idx, max(0, match_idx - max_lines) - 1, -1):
        if opener.match(lines[i]):
            header_idx = i
            break

    depth = 0
    func_end = min(n - 1, header_idx + max_lines)
    for i in range(header_idx, min(n, header_idx + max_lines)):
        if opener.match(lines[i]) or (nested_openers and nested_openers.match(lines[i])):
            depth += 1
        elif closer.match(lines[i]):
            depth -= 1
            if depth == 0:
                func_end = i
                break

    return header_idx, func_end


def _find_header(lines, match_idx, kw_re, max_back, max_fwd=40):
    """Walk backward (then forward as fallback) for a keyword-matching header line."""
    n = len(lines)
    # Backward from match (inclusive)
    for i in range(match_idx, max(0, match_idx - max_back) - 1, -1):
        if kw_re.match(lines[i]):
            return i
    # Forward fallback — useful when match is in a doc comment preceding the def
    for i in range(match_idx + 1, min(n, match_idx + max_fwd)):
        if kw_re.match(lines[i]):
            return i
    return max(0, match_idx - max_back // 4)  # narrow fallback window


def _ocaml_extract(lines: list[str], match_idx: int, max_lines: int = 120) -> tuple[int, int]:
    """OCaml / Why3: `let [rec] name ... = ...` delimited by next top-level `let` or `;;`."""
    n = len(lines)
    top_let = re.compile(r"^let\b")
    header_idx = _find_header(lines, match_idx, top_let, max_lines)

    func_end = min(n - 1, header_idx + max_lines)
    for i in range(header_idx + 1, min(n, header_idx + max_lines)):
        if top_let.match(lines[i]) or lines[i].strip() == ";;":
            func_end = i - 1
            break

    return header_idx, func_end


def _coq_extract(lines: list[str], match_idx: int, max_lines: int = 120) -> tuple[int, int]:
    """Coq/Rocq: Definition/Fixpoint/Lemma … terminated by a `.` at end of a statement."""
    n = len(lines)
    coq_kw = re.compile(
        r"^(?:Definition|Fixpoint|Lemma|Theorem|Function|Program|Equations|"
        r"Inductive|Record|Instance)\b",
        re.I,
    )
    header_idx = _find_header(lines, match_idx, coq_kw, max_lines)

    func_end = min(n - 1, header_idx + max_lines)
    for i in range(header_idx, min(n, header_idx + max_lines)):
        stripped = lines[i].rstrip()
        if stripped.endswith(".") and not stripped.endswith("..") and i > header_idx:
            func_end = i
            break

    return header_idx, func_end


def _lean_extract(lines: list[str], match_idx: int, max_lines: int = 120) -> tuple[int, int]:
    """Lean: `def / theorem / lemma` at col 0."""
    n = len(lines)
    lean_kw = re.compile(r"^(?:noncomputable\s+|partial\s+)?(?:def|theorem|lemma|abbrev)\s+\w")
    header_idx = _find_header(lines, match_idx, lean_kw, max_lines)

    func_end = min(n - 1, header_idx + max_lines)
    for i in range(header_idx + 1, min(n, header_idx + max_lines)):
        if lean_kw.match(lines[i]):
            func_end = i - 1
            break

    return header_idx, func_end


def _cobol_extract(lines: list[str], match_idx: int, max_lines: int = 120) -> tuple[int, int]:
    """COBOL: paragraph/section name (IDENTIFIER[.| SECTION.]) at fixed columns."""
    n = len(lines)
    # Paragraph: identifier starting at col 7-8 (0-based 6-7), followed by optional SECTION and .
    para = re.compile(r"^[ ]{4,8}[A-Z0-9][A-Z0-9-]+(?:\s+SECTION)?\.", re.I)

    header_idx = max(0, match_idx - max_lines)
    for i in range(match_idx - 1, max(0, match_idx - max_lines) - 1, -1):
        if para.match(lines[i]):
            header_idx = i
            break

    func_end = min(n - 1, header_idx + max_lines)
    for i in range(header_idx + 1, min(n, header_idx + max_lines)):
        if para.match(lines[i]):
            func_end = i - 1
            break

    return header_idx, func_end


def _asm_extract(lines: list[str], match_idx: int, max_lines: int = 120) -> tuple[int, int]:
    """Assembly: label at col 0 (identifier:)."""
    n = len(lines)
    label = re.compile(r"^[A-Za-z_.][A-Za-z0-9_.]*:\s*(?:;.*)?$")

    header_idx = max(0, match_idx - max_lines)
    for i in range(match_idx - 1, max(0, match_idx - max_lines) - 1, -1):
        if label.match(lines[i]):
            header_idx = i
            break

    func_end = min(n - 1, header_idx + max_lines)
    for i in range(header_idx + 1, min(n, header_idx + max_lines)):
        if label.match(lines[i]):
            func_end = i - 1
            break

    return header_idx, func_end


def _apl_extract(lines: list[str], match_idx: int, max_lines: int = 120) -> tuple[int, int]:
    """APL: ∇FunctionName opens, bare ∇ closes (GNU APL / Dyalog)."""
    n = len(lines)
    nabla_def = re.compile(r"^∇\w")   # function start: ∇Name...
    nabla_end = re.compile(r"^∇\s*$") # function end: ∇ alone

    # Walk backward to find enclosing ∇Name (stop at a bare ∇ — would be prev func end)
    header_idx = None
    for i in range(match_idx, max(0, match_idx - max_lines) - 1, -1):
        if nabla_def.match(lines[i]):
            header_idx = i
            break
        if nabla_end.match(lines[i]) and i < match_idx:
            break  # crossed previous function boundary

    # Fallback: walk forward (match may be a constant before the function)
    if header_idx is None:
        for i in range(match_idx + 1, min(n, match_idx + max_lines)):
            if nabla_def.match(lines[i]):
                header_idx = i
                break

    if header_idx is None:
        half = max_lines // 2
        return max(0, match_idx - half), min(n - 1, match_idx + half)

    # Walk forward to find bare ∇ (end of function)
    func_end = min(n - 1, header_idx + max_lines)
    for i in range(header_idx + 1, min(n, header_idx + max_lines)):
        if nabla_end.match(lines[i]):
            func_end = i
            break

    return header_idx, func_end


def extract_function(
    lines: list[str],
    match_lineno: int,  # 1-indexed
    file_path: Path,
    max_lines: int = 120,
) -> tuple[int, int, str]:
    """Return (start_lineno, end_lineno, code_snippet) for the function enclosing match_lineno."""
    ext = file_path.suffix.lower()
    family = _EXT_TO_FAMILY.get(ext, "fallback")
    idx = match_lineno - 1  # 0-based

    if family == "brace":
        s, e = _brace_extract(lines, idx, max_lines)
    elif family == "indent":
        s, e = _indent_extract(lines, idx, max_lines)
    elif family == "ruby":
        opener = re.compile(r"^\s*def\s+\w")
        nested = re.compile(r"^\s*(?:if|while|for|do|begin|case|class|module|unless|until)\b")
        s, e = _keyword_end_extract(lines, idx, max_lines, opener, nested)
    elif family == "lua":
        opener = re.compile(r"^\s*(?:local\s+)?function\s+\w")
        s, e = _keyword_end_extract(lines, idx, max_lines, opener)
    elif family == "keyword_end":  # Icon
        opener = re.compile(r"^\s*procedure\s+\w")
        s, e = _keyword_end_extract(lines, idx, max_lines, opener)
    elif family == "ocaml":
        s, e = _ocaml_extract(lines, idx, max_lines)
    elif family == "coq":
        s, e = _coq_extract(lines, idx, max_lines)
    elif family == "lean":
        s, e = _lean_extract(lines, idx, max_lines)
    elif family == "cobol":
        s, e = _cobol_extract(lines, idx, max_lines)
    elif family == "asm":
        s, e = _asm_extract(lines, idx, max_lines)
    elif family == "apl":
        s, e = _apl_extract(lines, idx, max_lines)
    else:
        half = max_lines // 2
        s = max(0, idx - half)
        e = min(len(lines) - 1, idx + half)

    snippet = "\n".join(lines[s : e + 1])
    return s + 1, e + 1, snippet  # back to 1-indexed


def _pattern_keywords(patterns: list[re.Pattern]) -> list[str]:
    """Extract plain alphabetic hints from pattern strings, plus short stems.

    e.g. 'quiescence' → ['quiescence', 'quiesc'] so we also match 'quiesce',
    'qsearch' stays as-is since it's already short.
    """
    kws: list[str] = []
    for pat in patterns:
        for part in re.split(r"[|[\](){}+*?.\\^$\s_\-]", pat.pattern):
            if len(part) >= 4 and part.isalpha():
                kws.append(part.lower())
    # Add stems (6-char prefix) for long keywords, so 'quiescence' → 'quiesc'
    stems = [kw[:6] for kw in kws if len(kw) > 7]
    return list(dict.fromkeys(kws + stems))  # deduplicate, preserve order


def _score_match(m: dict, keywords: list[str]) -> float:
    """Higher = more likely to be the primary implementation."""
    score: float = 0.0
    fname = Path(m["file"]).name.lower()
    text = m["text"]
    text_lower = text.lower()

    # Penalise tests
    if "test" in fname or "spec" in fname:
        score -= 25
    # Reward search / engine / eval filenames
    for hint in ("search", "engine", "alpha", "minimax", "eval", "negamax"):
        if hint in fname:
            score += 6
    # Penalise deep / build-artifact paths
    score -= m["file"].count("/") * 0.8

    # Detect function-definition lines across language families:
    is_func_def = bool(
        # Keyword-based (Python, Rust, Go, OCaml, Lean, Coq, …)
        re.search(
            r"\b(def|fn|func|function|procedure|SECTION|let\s+rec|let|"
            r"Fixpoint|Definition|Theorem|Lemma)\b",
            text, re.I,
        )
        # C/C++/Java style: identifier(...) at end of the declaration (not control flow)
        or (
            re.search(r"\w+\s*\([^;{(]*\)\s*(?:const\s*)?\{?\s*(?://.*)?$", text.strip())
            and not _CTRL_FLOW.match(text)
            and not _COMMENT_LINE.match(text)
        )
        # APL: ∇FunctionName opens a function
        or bool(re.match(r"^∇\w", text))
    )
    if is_func_def:
        score += 12

    # Feature keyword in / near the function name
    for kw in keywords:
        esc = re.escape(kw)
        if (
            # Language-agnostic keyword function families
            re.search(rf"(?:def|fn|func|function|procedure|let\s+rec|let)\s+\w*{esc}", text, re.I)
            # C-style: keyword IS the identifier directly before (
            or (is_func_def and re.search(rf"\b{esc}\w*\s*\(", text, re.I))
            # APL: keyword appears anywhere in ∇Name... line
            or (is_func_def and re.match(r"^∇", text) and kw in text_lower)
        ):
            score += 20
        if kw in text_lower:
            score += 3

    return score


_FUNC_DEF_RE: dict[str, re.Pattern] = {
    "brace":       re.compile(r"^\s*\w[\w\s*&<>,]*\w\s*\([^;{(]*\)\s*(?:const\s*)?\{?\s*(?://.*)?$"),
    "indent":      re.compile(r"^\s*(?:async\s+)?def\s+\w"),
    "ruby":        re.compile(r"^\s*def\s+\w"),
    "lua":         re.compile(r"^\s*(?:local\s+)?function\s+\w"),
    "keyword_end": re.compile(r"^\s*procedure\s+\w"),
    "ocaml":       re.compile(r"^let\s+(?:rec\s+)?\w"),
    "coq":         re.compile(r"^(?:Definition|Fixpoint|Lemma|Theorem|Function|Equations)\s+\w", re.I),
    "lean":        re.compile(r"^(?:noncomputable\s+|partial\s+)?(?:def|theorem|lemma|abbrev)\s+\w"),
    "cobol":       re.compile(r"^[ ]{4,8}[A-Z0-9][A-Z0-9-]+(?:\s+SECTION)?\."),
    "asm":         re.compile(r"^[A-Za-z_.][A-Za-z0-9_.]*:\s*(?:;.*)?$"),
    "apl":         re.compile(r"^∇\w"),
    "sql":         re.compile(r"^\s*CREATE\s+(?:OR\s+REPLACE\s+)?(?:FUNCTION|PROCEDURE)\s+\w", re.I),
}


def _find_func_def_by_stem(
    lines: list[str],
    file_path: Path,
    stems: list[str],
) -> int | None:
    """Scan the file for a function definition whose name contains a keyword stem.

    Returns the 1-indexed line number of the best match, or None.
    Useful when the actual function is named 'quiesce' but the search keyword is
    'quiescence' — the def line never appears in the pattern-match results.
    """
    ext = file_path.suffix.lower()
    family = _EXT_TO_FAMILY.get(ext, "fallback")
    func_re = _FUNC_DEF_RE.get(family)
    if not func_re:
        return None

    for lineno, line in enumerate(lines, start=1):
        if func_re.match(line) and not _CTRL_FLOW.match(line):
            line_lower = line.lower()
            for stem in stems:
                if stem in line_lower:
                    return lineno
    return None


def compute_hotspot(
    engine_matches: list[dict],
    patterns: list[re.Pattern],
    engine_path: Path,
    max_lines: int = 120,
) -> dict | None:
    """Pick the best match for an engine and extract its enclosing function.

    Two-pass strategy:
    1. Score all pattern matches; pick the best.
    2. Also scan for function definitions whose names contain keyword stems
       (catches e.g. 'Fixpoint quiesce' when pattern is 'quiescence').
    Use whichever anchor line has the higher score.
    """
    if not engine_matches:
        return None

    keywords = _pattern_keywords(patterns)
    best = max(engine_matches, key=lambda m: _score_match(m, keywords))
    best_score = _score_match(best, keywords)

    # Use the most-matched file as the authoritative source for stem scanning.
    by_file: dict[str, list[dict]] = {}
    for m in engine_matches:
        by_file.setdefault(m["file"], []).append(m)
    primary_file = max(by_file, key=lambda f: len(by_file[f]))

    full_path = engine_path / primary_file
    try:
        text = full_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        # Fall back to the best-scored match's file
        full_path = engine_path / best["file"]
        try:
            text = full_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return None

    lines = text.splitlines()

    # Secondary scan: function def whose name contains a keyword stem.
    stems = [kw for kw in keywords if 5 <= len(kw) <= 7]  # stems only
    func_def_lineno = _find_func_def_by_stem(lines, full_path, stems) if stems else None

    if func_def_lineno is not None:
        pseudo = {"file": primary_file, "line": func_def_lineno, "text": lines[func_def_lineno - 1]}
        func_def_score = _score_match(pseudo, keywords)
        if func_def_score >= best_score - 5:  # prefer func-def unless match clearly wins
            anchor_line = func_def_lineno
            anchor_file = primary_file
        else:
            anchor_line = best["line"]
            anchor_file = best["file"]
            if anchor_file != primary_file:
                full_path = engine_path / anchor_file
                lines = full_path.read_text(encoding="utf-8", errors="replace").splitlines()
    else:
        anchor_line = best["line"]
        anchor_file = best["file"]
        if anchor_file != primary_file:
            full_path = engine_path / anchor_file
            try:
                lines = full_path.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                return None

    start_ln, end_ln, snippet = extract_function(lines, anchor_line, full_path, max_lines)

    return {
        "file": str(full_path.relative_to(engine_path)),
        "anchor_line": anchor_line,
        "func_start": start_ln,
        "func_end": end_ln,
        "loc": end_ln - start_ln + 1,
        "snippet": snippet,
        "score": max(best_score, _score_match({"file": str(full_path.relative_to(engine_path)),
                                                "line": anchor_line,
                                                "text": lines[anchor_line - 1]}, keywords)),
    }


def _hotspot_text_report(result: dict) -> str:
    """One block per engine: just the extracted function, annotated with language."""
    m = result["meta"]
    out: list[str] = []
    sep = "=" * 72

    out.append(sep)
    out.append(f"HOTSPOT REPORT  —  Feature: {m['feature']}")
    out.append(f"Patterns: {', '.join(m['patterns'])}")
    out.append(f"Generated: {m['generated_at']}")
    out.append(
        f"Engines with feature: {m['engines_with_feature']} / {m['total_engines']}"
    )
    out.append(sep)

    for eng_name in sorted(result["engines"]):
        eng = result["engines"][eng_name]
        lang = eng.get("language") or "?"
        hs = eng.get("hotspot")
        out.append("")

        if not hs:
            tag = "[NO] " if not eng.get("has_feature") else "[?]  "
            out.append(f"{tag} {eng_name}  ({lang})")
            continue

        out.append(f"[YES] {eng_name}  ({lang})")
        out.append(f"      {hs['file']}  lines {hs['func_start']}–{hs['func_end']}  ({hs['loc']} LOC)")
        out.append("-" * 72)
        for i, ln in enumerate(hs["snippet"].splitlines(), start=hs["func_start"]):
            marker = ">>>" if i == hs["anchor_line"] else "   "
            out.append(f"{marker} {i:5d}  {ln}")
        out.append("-" * 72)

    out.append("")
    out.append(sep)
    out.append("Engines WITHOUT the feature:")
    for eng_name in sorted(result["engines"]):
        eng = result["engines"][eng_name]
        if not eng.get("has_feature"):
            out.append(f"  - {eng_name}  ({eng.get('language') or '?'})")

    return "\n".join(out)


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def _text_report(result: dict) -> str:
    lines: list[str] = []
    m = result["meta"]
    lines.append("=" * 72)
    lines.append(f"Feature: {m['feature']}")
    lines.append(f"Patterns: {', '.join(m['patterns'])}")
    lines.append(f"Generated: {m['generated_at']}")
    lines.append(
        f"Engines with feature: {m['engines_with_feature']} / {m['total_engines']}"
    )
    lines.append("=" * 72)
    lines.append("")

    for eng_name, eng in sorted(result["engines"].items()):
        tag = "[YES]" if eng["has_feature"] else "[NO] "
        lang = eng.get("language") or "?"
        mc = eng.get("match_count", 0)
        lines.append(f"{tag} {eng_name}  ({lang})  — {mc} match(es)")

        for m_item in eng.get("matches", []):
            lines.append(f"  {m_item['file']}:{m_item['line']}")
            for ctx in m_item["context"]:
                marker = ">>>" if ctx["match"] else "   "
                lines.append(f"    {marker} {ctx['line']:4d}  {ctx['text']}")
            lines.append("")

        if not eng.get("has_feature"):
            lines.append("")

    # Summary table at the end
    lines.append("=" * 72)
    lines.append("Summary (engines WITHOUT the feature):")
    without = [n for n, e in result["engines"].items() if not e["has_feature"]]
    for n in sorted(without):
        lines.append(f"  - {n}  ({result['engines'][n].get('language') or '?'})")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------

def run(
    feature_name: str,
    patterns: list[re.Pattern],
    manifest: Path = MANIFEST_PATH,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    context: int = 3,
    engine_filter: str | None = None,
    code_only: bool = False,
    hotspot: bool = False,
    hotspot_max_lines: int = 120,
) -> dict:
    engines_cfg = _load_engines_from_manifest(manifest)
    if not engines_cfg:
        sys.exit(f"ERROR: could not parse any engines from {manifest}")

    result: dict = {
        "meta": {
            "feature": feature_name,
            "patterns": [p.pattern for p in patterns],
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_engines": 0,
            "engines_with_feature": 0,
        },
        "engines": {},
    }

    for eng in engines_cfg:
        name = eng.get("name", "unknown")
        if engine_filter and name != engine_filter:
            continue

        path_str = eng.get("path", "")
        eng_path = Path(path_str) if path_str else None

        if not eng_path or not eng_path.exists():
            result["engines"][name] = {
                "path": path_str,
                "language": None,
                "has_feature": False,
                "match_count": 0,
                "matches": [],
                "note": "path not found on this host",
            }
            result["meta"]["total_engines"] += 1
            continue

        # Determine primary language
        loc = compute_loc(eng_path)
        lang = primary_language(loc)

        matches = search_engine(eng_path, patterns, context=context, code_only=code_only)

        hs = None
        if hotspot and matches:
            hs = compute_hotspot(matches, patterns, eng_path, max_lines=hotspot_max_lines)

        result["engines"][name] = {
            "path": path_str,
            "language": lang,
            "tier": eng.get("tier"),
            "corpus": eng.get("corpus"),
            "has_feature": len(matches) > 0,
            "match_count": len(matches),
            "matches": matches,
            **({"hotspot": hs} if hotspot else {}),
        }
        result["meta"]["total_engines"] += 1
        if matches:
            result["meta"]["engines_with_feature"] += 1

    output_dir.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", feature_name.lower())

    json_path = output_dir / f"{safe_name}.json"
    txt_path = output_dir / f"{safe_name}.txt"

    json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    txt_path.write_text(_text_report(result), encoding="utf-8")

    if hotspot:
        hs_txt_path = output_dir / f"{safe_name}.hotspot.txt"
        hs_txt_path.write_text(_hotspot_text_report(result), encoding="utf-8")

    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--list-features",
        action="store_true",
        help="Print all feature names defined in CHESS_PATTERNS and exit.",
    )
    p.add_argument(
        "--feature",
        metavar="NAME",
        help="Name of a known feature (key in CHESS_PATTERNS). "
             "Use --list-features to see all options.",
    )
    p.add_argument(
        "--pattern",
        metavar="REGEX",
        action="append",
        dest="patterns",
        default=[],
        help="Additional / custom regex pattern(s). May be repeated.",
    )
    p.add_argument(
        "--name",
        metavar="LABEL",
        help="Label to use for the output files when using --pattern "
             "(defaults to the first pattern string).",
    )
    p.add_argument(
        "--context",
        type=int,
        default=3,
        metavar="N",
        help="Lines of context to show around each match (default: 3).",
    )
    p.add_argument(
        "--engine",
        metavar="NAME",
        help="Restrict search to a single engine (by manifest name).",
    )
    p.add_argument(
        "--output",
        metavar="DIR",
        default=str(DEFAULT_OUTPUT_DIR),
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR}).",
    )
    p.add_argument(
        "--manifest",
        metavar="PATH",
        default=str(MANIFEST_PATH),
        help=f"Path to manifest.yaml (default: {MANIFEST_PATH}).",
    )
    p.add_argument(
        "--code-only",
        action="store_true",
        help="Skip Markdown, plain-text, JSON, YAML, and other non-code files. "
             "Useful to cut through session logs and documentation noise.",
    )
    p.add_argument(
        "--hotspot",
        action="store_true",
        help="For each engine, extract the single best function that implements "
             "the feature (language-aware boundary detection). Produces "
             "<name>.hotspot.txt — one code block per engine, ideal for "
             "cross-language comparison. Implies --code-only.",
    )
    p.add_argument(
        "--hotspot-max-lines",
        type=int,
        default=120,
        metavar="N",
        help="Maximum lines to extract per function hotspot (default: 120).",
    )
    p.add_argument(
        "--json-only",
        action="store_true",
        help="Skip writing the .txt summary file.",
    )
    return p


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.list_features:
        print("Known features (usable with --feature):")
        for name in sorted(CHESS_PATTERNS):
            pat = CHESS_PATTERNS[name].pattern
            print(f"  {name!r:45s}  pattern: {pat}")
        return

    # Collect compiled patterns.
    compiled: list[re.Pattern] = []
    feature_name: str

    if args.feature:
        if args.feature not in CHESS_PATTERNS:
            closest = [k for k in CHESS_PATTERNS if args.feature.lower() in k.lower()]
            hint = f"  Did you mean: {closest}" if closest else ""
            sys.exit(f"ERROR: unknown feature {args.feature!r}.{hint}\n"
                     "Run --list-features to see all options.")
        compiled.append(CHESS_PATTERNS[args.feature])
        feature_name = args.feature
    else:
        feature_name = args.name or (args.patterns[0] if args.patterns else None)
        if not feature_name:
            parser.error("Specify --feature NAME or --pattern REGEX (optionally with --name).")

    for raw_pat in args.patterns:
        try:
            compiled.append(re.compile(raw_pat, re.IGNORECASE))
        except re.error as exc:
            sys.exit(f"ERROR: bad regex {raw_pat!r}: {exc}")

    if not compiled:
        parser.error("No patterns to search. Use --feature or --pattern.")

    # --hotspot implies --code-only (no point extracting functions from docs).
    code_only = args.code_only or args.hotspot

    print(f"Searching for: {feature_name!r}")
    print(f"Patterns: {[p.pattern for p in compiled]}")
    if not args.hotspot:
        print(f"Context lines: {args.context}")
    if args.hotspot:
        print(f"Mode: hotspot  (max {args.hotspot_max_lines} lines/function)")
    if args.engine:
        print(f"Engine filter: {args.engine}")

    result = run(
        feature_name=feature_name,
        patterns=compiled,
        manifest=Path(args.manifest),
        output_dir=Path(args.output),
        context=args.context,
        engine_filter=args.engine,
        code_only=code_only,
        hotspot=args.hotspot,
        hotspot_max_lines=args.hotspot_max_lines,
    )

    meta = result["meta"]
    print(
        f"\nDone. {meta['engines_with_feature']}/{meta['total_engines']} engines "
        f"implement '{feature_name}'."
    )
    out = Path(args.output)
    safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", feature_name.lower())
    print(f"  JSON    : {out / (safe_name + '.json')}")
    print(f"  Text    : {out / (safe_name + '.txt')}")
    if args.hotspot:
        print(f"  Hotspot : {out / (safe_name + '.hotspot.txt')}")


if __name__ == "__main__":
    main()
