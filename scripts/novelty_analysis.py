"""RQ3: novelty / no-copy analysis.

For each agent-built engine, we look for evidence that the code is
either (a) a genuine from-scratch synthesis, (b) uses an external chess
library for part of the pipeline, or (c) textually matches a canonical
open-source engine's distinctive fingerprint.

Three evidence streams:

  1. **Dependency manifests.** We parse each project's package manifest
     (pyproject.toml, requirements.txt, Cargo.toml, Gemfile, package.json,
     pom.xml, build.gradle, go.mod, Makefile) and flag entries that are
     known chess libraries.

  2. **Source imports.** We grep source files for language-specific
     import statements that pull in known chess libraries (Python
     `import chess`, Rust `use shakmaty`, JS `require('chess.js')`,
     Ruby `require 'chess'`, etc.).

  3. **Canonical-engine fingerprints.** A small, hand-curated set of
     distinctive constants/strings taken from well-known open-source
     engines --- if any agent engine contains them, it is a smoking-gun
     copy. The most famous single fingerprint is Sunfish's piece-value
     table `{P=100, N=280, B=320, R=479, Q=929, K=60000}`; python-chess
     exposes distinctive class names; chess.js uses a specific
     `PIECE_SYMBOLS` string.

  4. **Transcript mining.** We grep every agent transcript whose cwd is
     the project for "based on X", "adapt from X", "follow the X design",
     "port of X" where X is a canonical engine/library. These are the
     self-reported copying signals.

Writes:
  data/novelty.json           per-engine findings
  paper/tables/tab_novelty.tex  summary table for the paper
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from common import (
    CODEX_SESSIONS,
    DATA_DIR,
    IGNORED_DIRS,
    claude_session_dir,
    discover_projects,
    iter_jsonl,
    short_quote,
)

# -----------------------------------------------------------------------
# Canonical chess libraries (per language / build system)
# -----------------------------------------------------------------------

# Manifest-level dependencies. Name match is case-insensitive.
CANONICAL_DEPS: dict[str, list[str]] = {
    "python-chess": ["chess", "python-chess"],
    "pychess": ["pychess"],
    "sunfish": ["sunfish"],
    "chess.js": ["chess.js", "chessjs"],
    "chess-rules (npm)": ["chess-rules"],
    "shakmaty (Rust)": ["shakmaty"],
    "cozy-chess (Rust)": ["cozy-chess"],
    "chess-rs (Rust)": ["chess"],
    "pgn-reader (Rust)": ["pgn-reader"],
    "ruby-chess": ["ruby-chess"],
    "chess (Ruby gem)": ["chess"],
    "chesspresso (Java)": ["chesspresso"],
    "jchess (Java)": ["jchess"],
    "stockfish-py": ["stockfish"],  # invokes Stockfish as subprocess
    "cutechess-cli": ["cutechess"],  # not a library but a tool
}

# Language-specific import/require patterns. Kept conservative to avoid
# false positives (e.g., Python's \\bchess\\b would match a comment).
SOURCE_IMPORTS: list[tuple[str, re.Pattern]] = [
    ("python: import chess", re.compile(r"^\s*(?:from|import)\s+chess(?:\b|\.)", re.M)),
    ("python: pychess", re.compile(r"^\s*(?:from|import)\s+pychess", re.M)),
    ("python: sunfish", re.compile(r"^\s*(?:from|import)\s+sunfish", re.M)),
    ("python: stockfish", re.compile(r"^\s*(?:from|import)\s+stockfish", re.M)),
    ("rust: shakmaty", re.compile(r"^\s*use\s+shakmaty(?:::|;)", re.M)),
    ("rust: cozy_chess", re.compile(r"^\s*use\s+cozy_chess", re.M)),
    ("rust: pgn_reader", re.compile(r"^\s*use\s+pgn_reader", re.M)),
    ("rust: chess crate", re.compile(r"^\s*use\s+chess(?:::|;)", re.M)),
    ("js: chess.js", re.compile(r"require\(['\"]chess\.js['\"]\)|from\s+['\"]chess\.js['\"]")),
    ("ruby: chess gem", re.compile(r"^\s*require\s+['\"]chess['\"]", re.M)),
    ("java: chesspresso", re.compile(r"import\s+chesspresso", re.I)),
    ("java: bhlangonia", re.compile(r"import\s+bhlangonia", re.I)),
    ("go: dylhunn/dragontoothmg", re.compile(r"dylhunn/dragontoothmg")),
    ("go: notnil/chess", re.compile(r"github\.com/notnil/chess")),
]


# -----------------------------------------------------------------------
# Canonical-engine fingerprints. These are strings/constants so specific
# that a textual match implies a copy.
# -----------------------------------------------------------------------

# Sunfish: a famous Python minichess engine. Its piece values and the
# 120-char initial-board string are the cleanest fingerprint in chess.
SUNFISH_PIECE_VALUES = re.compile(
    r"['\"]P['\"]\s*[:=]\s*100\b.*?"
    r"['\"]N['\"]\s*[:=]\s*280\b.*?"
    r"['\"]B['\"]\s*[:=]\s*320\b.*?"
    r"['\"]R['\"]\s*[:=]\s*479\b.*?"
    r"['\"]Q['\"]\s*[:=]\s*929\b.*?"
    r"['\"]K['\"]\s*[:=]\s*60000\b",
    re.S,
)
SUNFISH_INITIAL = re.compile(
    r"""['"]         # opening quote
    \s{9}\\n         # 10 spaces + newline
    \s{9}\\n         # padding rows
    \s+rnbqkbnr""",
    re.X,
)
# Fallback fingerprint: Sunfish's 120-char initial board string fragment.
SUNFISH_INITIAL_STR = "rnbqkbnr\n pppppppp"
# python-chess: unmistakable symbol surface.
PYTHON_CHESS_API = re.compile(
    r"chess\.(?:Board\b|Move\.from_uci\b|engine\.SimpleEngine\b|pgn\.Game\b|polyglot\b)"
)
# chess.js: specific piece-symbol ordering
CHESS_JS_PIECES = re.compile(r"PIECE_SYMBOLS\s*=\s*\[?[\"']p['\"],\s*['\"]n['\"],\s*['\"]b['\"]", re.I)
# TSCP (Tom Kerrigan's Simple Chess Program, a classic C tutorial engine).
# Its move ordering uses a specific comment block; we look for the
# characteristic `#define KNIGHT 1` + `#define BISHOP 2` + `#define ROOK 3`
# contiguous sequence.
TSCP_PIECE_DEFS = re.compile(
    r"#define\s+PAWN\s+0\b[^\n]*\n\s*"
    r"#define\s+KNIGHT\s+1\b[^\n]*\n\s*"
    r"#define\s+BISHOP\s+2\b[^\n]*\n\s*"
    r"#define\s+ROOK\s+3\b[^\n]*\n\s*"
    r"#define\s+QUEEN\s+4\b[^\n]*\n\s*"
    r"#define\s+KING\s+5\b",
    re.M,
)

CANONICAL_FINGERPRINTS: dict[str, re.Pattern] = {
    "Sunfish piece-values": SUNFISH_PIECE_VALUES,
    "python-chess API surface": PYTHON_CHESS_API,
    "chess.js PIECE_SYMBOLS": CHESS_JS_PIECES,
    "TSCP #define pieces": TSCP_PIECE_DEFS,
}


# -----------------------------------------------------------------------
# Transcript mining: explicit "copy/adapt/follow/port" phrases
# -----------------------------------------------------------------------

# Two patterns, ordered from strong to weak evidence.
#
# STRONG: explicit authorship verbs. Positive evidence the agent
# intentionally reused a canonical engine's code.
STRONG_COPY_VERBS = (
    r"(?:port(?:ed|ing)?\s+from|adapt(?:ed|ing)?\s+from|"
    r"translat(?:ed|ing)?\s+from|copy\s+of|copied\s+from|"
    r"reuse\s+of|reusing|stripped[- ]down\s+version\s+of|"
    r"fork(?:ed)?\s+of|implement(?:ation)?\s+of\s+.{0,20}\balgorithm)"
)
# WEAK: casual comparison / design reference. Usually not a copy
# (e.g., "like Stockfish's NNUE features"). Recorded separately as
# "canonical reference" evidence.
WEAK_COPY_VERBS = (
    r"(?:based\s+on|follow(?:ing)?\s+the|inspired\s+by|like|"
    r"similar\s+to|modeled\s+after)"
)
CANONICAL_TARGETS = (
    r"(?:Stockfish|Sunfish|python-chess|pychess|chess\.js|"
    r"Mediocre|Carballo|Rustic|Shakmaty|TSCP|Crafty|Fruit|"
    r"GNU\s*Chess|Tom\s+Kerrigan|Fairy-Stockfish|Leela)"
)

RE_STRONG_COPY = re.compile(
    r"\b" + STRONG_COPY_VERBS + r"\s+(?:the\s+)?" + CANONICAL_TARGETS + r"\b",
    re.I,
)
RE_WEAK_REFERENCE = re.compile(
    r"\b" + WEAK_COPY_VERBS + r"\s+(?:the\s+)?" + CANONICAL_TARGETS + r"\b",
    re.I,
)


# -----------------------------------------------------------------------
# Per-engine scan
# -----------------------------------------------------------------------


def _scan_requirements_txt(text: str) -> list[str]:
    """Parse a requirements.txt-like file: one package spec per line."""
    hits: list[str] = []
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        # Package name is the leading [A-Za-z0-9_.\-] run.
        m = re.match(r"([A-Za-z0-9][A-Za-z0-9_.\-]*)", line)
        if not m:
            continue
        pkg = m.group(1).lower()
        if pkg in {"chess", "python-chess"}:
            hits.append("python-chess")
        elif pkg in {"sunfish"}:
            hits.append("sunfish")
        elif pkg in {"stockfish"}:
            hits.append("stockfish-py")
        elif pkg in {"pychess"}:
            hits.append("pychess")
    return hits


def _scan_pyproject(text: str) -> list[str]:
    """Parse pyproject.toml dependencies = [...] list and tool.poetry.dependencies."""
    hits: list[str] = []
    # Match dependencies blocks.
    blocks = re.findall(r"(?:^|\n)dependencies\s*=\s*\[(.*?)\]", text, re.S)
    blocks += re.findall(r"\[tool\.poetry\.dependencies\](.*?)(?=\n\[|\Z)", text, re.S)
    blocks += re.findall(r"\[project\.dependencies\](.*?)(?=\n\[|\Z)", text, re.S)
    for blk in blocks:
        hits.extend(_scan_requirements_txt(blk.replace('"', "").replace("'", "")))
    return hits


def _scan_cargo_toml(text: str) -> list[str]:
    """Parse Cargo.toml dependencies / dev-dependencies tables."""
    hits: list[str] = []
    # Find [dependencies], [dev-dependencies], [build-dependencies] sections.
    sections = re.findall(
        r"\[(?:dev-|build-)?dependencies\](.*?)(?=\n\[|\Z)", text, re.S
    )
    # Also the table-of-tables form e.g. [dependencies.shakmaty]
    header_deps = re.findall(
        r"\[(?:dev-|build-)?dependencies\.([A-Za-z0-9_-]+)\]", text
    )
    for blk in sections:
        for line in blk.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = re.match(r"([A-Za-z0-9_-]+)\s*=", line)
            if not m:
                continue
            header_deps.append(m.group(1))
    for pkg in header_deps:
        p = pkg.lower()
        if p == "shakmaty":
            hits.append("shakmaty (Rust)")
        elif p == "cozy-chess" or p == "cozy_chess":
            hits.append("cozy-chess (Rust)")
        elif p == "pgn-reader":
            hits.append("pgn-reader (Rust)")
        elif p == "chess":
            hits.append("chess-rs (Rust)")
    return hits


def _scan_gemfile(text: str) -> list[str]:
    hits: list[str] = []
    for m in re.finditer(r"^\s*gem\s+['\"]([A-Za-z0-9_.-]+)['\"]", text, re.M):
        p = m.group(1).lower()
        if p in ("chess", "ruby-chess"):
            hits.append("chess (Ruby gem)")
    return hits


def _scan_package_json(text: str) -> list[str]:
    hits: list[str] = []
    try:
        data = json.loads(text)
    except Exception:
        return hits
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        for name in (data.get(key) or {}):
            n = name.lower()
            if n == "chess.js":
                hits.append("chess.js")
            elif n == "chessjs":
                hits.append("chess.js")
            elif n == "chess-rules":
                hits.append("chess-rules (npm)")
    return hits


def _scan_pom_gradle(text: str) -> list[str]:
    hits: list[str] = []
    if re.search(r"chesspresso", text, re.I):
        hits.append("chesspresso (Java)")
    return hits


def _scan_gomod(text: str) -> list[str]:
    hits: list[str] = []
    if re.search(r"github\.com/notnil/chess", text):
        hits.append("notnil/chess (Go)")
    if re.search(r"github\.com/dylhunn/dragontoothmg", text):
        hits.append("dragontoothmg (Go)")
    return hits


def scan_manifests(root: Path) -> list[dict[str, Any]]:
    """Parse language-specific manifests and report chess-library dependencies."""
    hits: list[dict[str, Any]] = []
    handlers = {
        "requirements.txt": ("python", _scan_requirements_txt),
        "pyproject.toml": ("python", _scan_pyproject),
        "setup.py": ("python", lambda t: _scan_requirements_txt(t)),
        "Cargo.toml": ("rust", _scan_cargo_toml),
        "package.json": ("js", _scan_package_json),
        "Gemfile": ("ruby", _scan_gemfile),
        "Gemfile.lock": ("ruby", _scan_gemfile),
        "pom.xml": ("java", _scan_pom_gradle),
        "build.gradle": ("java", _scan_pom_gradle),
        "build.gradle.kts": ("java", _scan_pom_gradle),
        "go.mod": ("go", _scan_gomod),
    }
    for dp, dns, fns in __import__("os").walk(root):
        dns[:] = [d for d in dns if d not in IGNORED_DIRS and not d.startswith(".")]
        for name in fns:
            if name not in handlers:
                continue
            p = Path(dp) / name
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            lang, scanner = handlers[name]
            chess_libs = sorted(set(scanner(text)))
            if chess_libs:
                hits.append({
                    "file": str(p.relative_to(root)),
                    "type": lang,
                    "chess_libs": chess_libs,
                })
    return hits


def scan_imports(root: Path, max_bytes: int = 2_000_000) -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    for dp, dns, fns in __import__("os").walk(root):
        dns[:] = [d for d in dns if d not in IGNORED_DIRS and not d.startswith(".")]
        for name in fns:
            if name.startswith("."):
                continue
            p = Path(dp) / name
            ext = p.suffix.lower()
            if ext not in {".py", ".rs", ".js", ".mjs", ".ts", ".tsx", ".rb", ".java",
                           ".kt", ".go", ".c", ".h", ".cpp", ".cc", ".cxx", ".hpp"}:
                continue
            try:
                if p.stat().st_size > max_bytes:
                    continue
                text = p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            for label, pat in SOURCE_IMPORTS:
                m = pat.search(text)
                if m:
                    hits.append({
                        "file": str(p.relative_to(root)),
                        "label": label,
                        "match": short_quote(m.group(0), 120),
                    })
    return hits


def scan_fingerprints(root: Path, max_bytes: int = 2_000_000) -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    for dp, dns, fns in __import__("os").walk(root):
        dns[:] = [d for d in dns if d not in IGNORED_DIRS and not d.startswith(".")]
        for name in fns:
            if name.startswith("."):
                continue
            p = Path(dp) / name
            if p.suffix.lower() in {".png", ".jpg", ".pdf", ".zip", ".gz", ".tar",
                                    ".bin", ".exe", ".o", ".so"}:
                continue
            try:
                if p.stat().st_size > max_bytes:
                    continue
                text = p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            for label, pat in CANONICAL_FINGERPRINTS.items():
                if pat.search(text):
                    hits.append({
                        "file": str(p.relative_to(root)),
                        "label": label,
                    })
            if SUNFISH_INITIAL_STR in text:
                hits.append({
                    "file": str(p.relative_to(root)),
                    "label": "Sunfish initial-board string",
                })
    return hits


def _flatten_content(content) -> str:
    if isinstance(content, str):
        return content
    parts: list[str] = []
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    parts.append(str(block.get("text", "")))
                elif block.get("type") == "thinking":
                    parts.append(str(block.get("thinking", "")))
    return " ".join(parts)


def _record_match(container: list[dict[str, Any]], agent: str, role: str, ts, text: str, m) -> None:
    s = max(0, m.start() - 60)
    e = min(len(text), m.end() + 60)
    container.append({
        "agent": agent,
        "role": role,
        "ts": ts,
        "match": m.group(0),
        "context": short_quote(text[s:e], 200),
    })


def scan_transcripts_for_copy_intent(project_dir: Path) -> dict[str, list[dict[str, Any]]]:
    """Return two lists: strong (authorship) and weak (reference) mentions."""
    strong: list[dict[str, Any]] = []
    weak: list[dict[str, Any]] = []
    # Claude Code
    slug = claude_session_dir(project_dir)
    if slug.exists():
        for jsonl in slug.rglob("*.jsonl"):
            for obj in iter_jsonl(jsonl):
                otype = obj.get("type")
                if otype in ("user", "assistant"):
                    msg = obj.get("message") or {}
                    text = _flatten_content(msg.get("content")) or ""
                    for m in RE_STRONG_COPY.finditer(text):
                        _record_match(strong, "claude", otype, obj.get("timestamp"), text, m)
                    for m in RE_WEAK_REFERENCE.finditer(text):
                        _record_match(weak, "claude", otype, obj.get("timestamp"), text, m)
    # Codex
    target = str(project_dir.resolve())
    needle = f'"cwd":"{target}"'
    needle_spaced = f'"cwd": "{target}"'
    if CODEX_SESSIONS.exists():
        for jsonl in CODEX_SESSIONS.rglob("*.jsonl"):
            try:
                with jsonl.open("rb") as fh:
                    head = fh.read(200_000)
                if needle.encode() not in head and needle_spaced.encode() not in head:
                    continue
            except Exception:
                continue
            for obj in iter_jsonl(jsonl):
                payload = obj.get("payload") or {}
                if obj.get("type") == "event_msg":
                    ptype = payload.get("type")
                    if ptype in ("user_message", "agent_message"):
                        text = payload.get("message") or ""
                        role = "user" if ptype == "user_message" else "assistant"
                        for m in RE_STRONG_COPY.finditer(text):
                            _record_match(strong, "codex", role, obj.get("timestamp"), text, m)
                        for m in RE_WEAK_REFERENCE.finditer(text):
                            _record_match(weak, "codex", role, obj.get("timestamp"), text, m)
                elif obj.get("type") == "response_item":
                    ptype = payload.get("type")
                    if ptype == "reasoning":
                        for s in payload.get("summary") or []:
                            if isinstance(s, dict):
                                text = s.get("text") or ""
                                for m in RE_STRONG_COPY.finditer(text):
                                    _record_match(strong, "codex", "reasoning", obj.get("timestamp"), text, m)
                                for m in RE_WEAK_REFERENCE.finditer(text):
                                    _record_match(weak, "codex", "reasoning", obj.get("timestamp"), text, m)
    return {"strong_copy": strong, "weak_reference": weak}


def classify_engine(findings: dict[str, Any]) -> str:
    """Bucket: 'scratch' | 'library-assisted' | 'copy-claim' | 'fingerprint-match'.

    Priority (strongest evidence first):
      1. fingerprint-match --- textually distinctive constants from a
         canonical engine appear verbatim in the code.
      2. copy-claim --- the agent self-reports porting/adapting a
         canonical engine in transcripts.
      3. library-assisted --- the manifest or source declares an
         external chess library dependency.
      4. scratch --- no external-engine evidence found; no manifest
         dependency, no source import, no distinctive constant, no
         self-reported copy intent.
    """
    if findings["canonical_fingerprints"]:  # core fingerprints only
        return "fingerprint-match"
    if findings["strong_copy_hits"]:
        return "copy-claim"
    if findings["source_chess_imports"]:    # core imports only
        return "library-assisted"
    # Manifest deps without core imports => dev/tooling-only dependency.
    # Engine core remains scratch-built.
    return "scratch"


# Heuristic: files whose path contains any of these tokens are tooling
# (test harness, gauntlet scripts, legality validators, benchmark rigs),
# NOT the engine core. A chess-library import here does not mean the
# engine itself is library-assisted.
TOOLING_PATH_TOKENS = {
    "test", "tests", "spec", "specs", "harness", "scripts", "tools",
    "bench", "benchmark", "benchmarks", "artifacts", "tournament",
    "gauntlet", "results", "selftest", "eval", "evaluation",
    "cutechess", "lichess", "examples", "example",
}


def _is_tooling(path: str) -> bool:
    parts = {p.lower() for p in path.replace("\\", "/").split("/")}
    if parts & TOOLING_PATH_TOKENS:
        return True
    basename = path.rsplit("/", 1)[-1].lower()
    if any(basename.startswith(tok) for tok in (
        "test_", "play_", "bench_", "run_", "eval_", "pgn2", "pgn_",
        "gauntlet", "tournament", "selftest", "analyze_", "analyse_",
        "legality_", "check_", "match_", "compare_")):
        return True
    if any(tok in basename for tok in ("_test.", "_spec.", "_bench.", "_harness.")):
        return True
    return False


def process(project_dir: Path) -> dict[str, Any]:
    manifests = scan_manifests(project_dir)
    manifest_chess_libs = sorted({
        lib for m in manifests for lib in (m["chess_libs"] or [])
    })
    imports = scan_imports(project_dir)
    # Split into engine-core vs tooling imports
    imports_core = [i for i in imports if not _is_tooling(i["file"])]
    imports_tooling = [i for i in imports if _is_tooling(i["file"])]
    source_chess_imports_core = sorted({i["label"] for i in imports_core})
    source_chess_imports_tooling = sorted({i["label"] for i in imports_tooling})
    fingerprints = scan_fingerprints(project_dir)
    fingerprints_core = [f for f in fingerprints if not _is_tooling(f["file"])]
    fingerprints_tooling = [f for f in fingerprints if _is_tooling(f["file"])]
    canonical_fingerprints_core = sorted({f["label"] for f in fingerprints_core})
    canonical_fingerprints_tooling = sorted({f["label"] for f in fingerprints_tooling})
    transcripts = scan_transcripts_for_copy_intent(project_dir)
    out = {
        "manifests": manifests,
        "manifest_chess_libs": manifest_chess_libs,
        "imports_core": imports_core,
        "imports_tooling": imports_tooling,
        "source_chess_imports": source_chess_imports_core,       # engine-core only
        "source_chess_imports_tooling": source_chess_imports_tooling,
        "fingerprints_core": fingerprints_core,
        "fingerprints_tooling": fingerprints_tooling,
        "canonical_fingerprints": canonical_fingerprints_core,    # engine-core only
        "canonical_fingerprints_tooling": canonical_fingerprints_tooling,
        "strong_copy_hits": transcripts["strong_copy"],
        "weak_reference_hits": transcripts["weak_reference"],
    }
    out["classification"] = classify_engine(out)
    return out


def main(argv: list[str]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    all_targets = {name: path for name, path in discover_projects()}
    from synthesis import CLASSIFICATION
    # Restrict to engines + variants by default; allow explicit arg.
    if argv:
        targets = [(a, all_targets.get(a)) for a in argv]
    else:
        targets = [
            (name, path) for name, path in all_targets.items()
            if CLASSIFICATION.get(name) in ("engine", "engine-variant")
        ]
    results: dict[str, dict[str, Any]] = {}
    for logical, p in targets:
        if not p or not p.exists():
            continue
        print(f"→ {logical}")
        r = process(p)
        results[logical] = r
        # Merge into per-project json
        appendix = DATA_DIR / "projects" / f"{logical}.json"
        if appendix.exists():
            try:
                prior = json.loads(appendix.read_text())
            except Exception:
                prior = {"name": logical, "path": str(p)}
        else:
            prior = {"name": logical, "path": str(p)}
        prior["novelty"] = r
        appendix.parent.mkdir(parents=True, exist_ok=True)
        appendix.write_text(json.dumps(prior, indent=2, default=str))
        print(
            f"    class={r['classification']}  "
            f"deps={r['manifest_chess_libs']}  "
            f"imports={r['source_chess_imports']}  "
            f"fingerprints={r['canonical_fingerprints']}  "
            f"strong_copy={len(r['strong_copy_hits'])}  "
            f"weak_ref={len(r['weak_reference_hits'])}"
        )
    (DATA_DIR / "novelty.json").write_text(json.dumps(results, indent=2, default=str))
    print(f"Wrote data/novelty.json ({len(results)} engines)")


if __name__ == "__main__":
    main(sys.argv[1:])
