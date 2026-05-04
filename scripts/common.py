"""Common helpers for the chess meta-analysis toolkit.

This module centralizes paths, language detection, and utility functions used
by the discovery, session-extraction, and reporting scripts.

The tool is intentionally dependency-free (stdlib only) so it can run on any
machine with Python 3.10+.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

HOME = Path(os.path.expanduser("~"))
SANDBOX = HOME / "SANDBOX"
META_DIR = SANDBOX / "chess-meta-analysis"
DATA_DIR = META_DIR / "data"
REPORTS_DIR = META_DIR / "reports"
CLAUDE_PROJECTS = HOME / ".claude" / "projects"
CODEX_SESSIONS = HOME / ".codex" / "sessions"
CODEX_HISTORY = HOME / ".codex" / "history.jsonl"

# Folders that are chess-related but don't start with "chess-" --- include by
# absolute path. The sentinel directory `chess-meta-analysis` is always
# excluded.
EXTRA_PROJECT_NAMES = [
    "COBOL-chess",
    "cplusplus-chess",
    "latex-chess-engine",
    "lean-chess",
    "minichess-5x5-repro",
    "minichess-5x5-repro-cc",
    "gptchess",
    "puzzles-chess",
    "test-superset",   # ChessCSS --- CSS chess engine via agent-heavy co-design
]

# Nested projects that should be treated as separate engines. Value is the
# canonical name we use in reports.
NESTED_PROJECTS: dict[str, str] = {
    # project-folder-name/subpath --> canonical logical name
    "chess-revisit-java-toRust-codex/chess-revisit-java-toCOBOL": "chess-revisit-java-toCOBOL-codex",
}


def discover_projects() -> list[tuple[str, Path]]:
    """Return [(logical_name, absolute_path), ...] for every in-scope folder.

    Logical_name may differ from folder name for nested projects. Callers
    that write per-project artifacts keyed by name use this for stable
    identifiers.
    """
    out: list[tuple[str, Path]] = []
    if SANDBOX.exists():
        for p in sorted(SANDBOX.iterdir()):
            if not p.is_dir():
                continue
            if p.name == "chess-meta-analysis":
                continue
            if p.name.lower().startswith("chess") or p.name in EXTRA_PROJECT_NAMES:
                out.append((p.name, p))
    for rel, logical in NESTED_PROJECTS.items():
        p = SANDBOX / rel
        if p.exists():
            out.append((logical, p))
    return out


# File extensions → canonical language name. Keep focused; many chess projects
# mix multiple languages, so we classify the "primary" language later.
EXT_TO_LANG: dict[str, str] = {
    ".py": "Python",
    ".rs": "Rust",
    ".go": "Go",
    ".java": "Java",
    ".c": "C",
    ".h": "C",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".hpp": "C++",
    ".hh": "C++",
    ".cs": "C#",
    ".js": "JavaScript",
    ".mjs": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".html": "HTML",
    ".htm": "HTML",
    ".css": "CSS",
    ".scss": "CSS",
    ".rb": "Ruby",
    ".lua": "Lua",
    ".pl": "Perl",
    ".sh": "Shell",
    ".bash": "Shell",
    ".zsh": "Shell",
    ".asm": "Assembly",
    ".s": "Assembly",
    ".S": "Assembly",
    ".nasm": "Assembly",
    ".bf": "Brainfuck",
    ".cob": "COBOL",
    ".cbl": "COBOL",
    ".cobol": "COBOL",
    ".sql": "SQL",
    ".tex": "LaTeX",
    ".sty": "LaTeX",
    ".ltx": "LaTeX",
    ".lean": "Lean",
    ".v": "Coq/Rocq",
    ".mojo": "Mojo",
    ".🔥": "Mojo",
    ".apl": "APL",
    ".dyalog": "APL",
    ".aplf": "APL",
    ".icn": "Icon",
    ".why": "Why3",
    ".mlw": "Why3",
    ".whyml": "Why3",
    ".m": "Objective-C/Matlab",
    ".ml": "OCaml",
    ".mli": "OCaml",
    ".scala": "Scala",
    ".kt": "Kotlin",
    ".swift": "Swift",
    ".zig": "Zig",
    ".hs": "Haskell",
    ".elm": "Elm",
    ".clj": "Clojure",
    ".dart": "Dart",
    ".nim": "Nim",
    ".cr": "Crystal",
    ".d": "D",
    ".f90": "Fortran",
    ".f95": "Fortran",
    ".f03": "Fortran",
    ".for": "Fortran",
    ".adb": "Ada",
    ".ads": "Ada",
    ".pas": "Pascal",
    ".pp": "Pascal",
    ".r": "R",
    ".R": "R",
    ".jl": "Julia",
    ".vb": "Visual Basic",
    ".bas": "Visual Basic",
    ".ps1": "PowerShell",
    ".md": "Markdown",
    ".txt": "Text",
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".toml": "TOML",
    ".xml": "XML",
}

# Directories ignored for LOC computation (standard noise + language-specific
# build/install artifacts).
IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "dist",
    "build",
    "target",
    "out",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".tox",
    ".ruff_cache",
    "coverage",
    ".idea",
    ".vscode",
    ".cache",
    "vendor",
    "deps",
    ".stack-work",
    "bin",
    "obj",
    ".next",
    ".nuxt",
    ".parcel-cache",
    ".turbo",
    "Pods",
    "DerivedData",
    ".dart_tool",
    "cmake-build-debug",
    "cmake-build-release",
    # Vendored third-party tooling often checked into these engine projects
    # as submodules or copies. They are NOT authored by the agent and must
    # be excluded from LOC / feature / novelty counts.
    "cutechess",
    "cutechess-cli",
    "stockfish",
    "stockfish-src",
    "fairy-stockfish",
    "Stockfish",
    "lc0",
    "leela",
    "leela-chess-zero",
    "syzygy",
}

# Roughly, Anthropic API prices per million tokens (as of early 2026).
# These are used *only* to estimate spend from token counts we observe in
# logs. Treat as approximations; we document our assumptions in the report.
PRICING_USD_PER_MTOK = {
    "claude-opus-4-6": {"input": 15.0, "cached_input": 1.50, "cache_write": 18.75, "output": 75.0},
    "claude-opus-4-7": {"input": 15.0, "cached_input": 1.50, "cache_write": 18.75, "output": 75.0},
    "claude-opus-4-1": {"input": 15.0, "cached_input": 1.50, "cache_write": 18.75, "output": 75.0},
    "claude-opus-4": {"input": 15.0, "cached_input": 1.50, "cache_write": 18.75, "output": 75.0},
    "claude-sonnet-4-5": {"input": 3.0, "cached_input": 0.30, "cache_write": 3.75, "output": 15.0},
    "claude-sonnet-4-6": {"input": 3.0, "cached_input": 0.30, "cache_write": 3.75, "output": 15.0},
    "claude-sonnet-4-7": {"input": 3.0, "cached_input": 0.30, "cache_write": 3.75, "output": 15.0},
    "claude-sonnet-4": {"input": 3.0, "cached_input": 0.30, "cache_write": 3.75, "output": 15.0},
    "claude-haiku-4-5": {"input": 1.0, "cached_input": 0.10, "cache_write": 1.25, "output": 5.0},
    # Codex / OpenAI — approximations
    "gpt-5-codex": {"input": 1.25, "cached_input": 0.125, "output": 10.0},
    "gpt-5": {"input": 1.25, "cached_input": 0.125, "output": 10.0},
    "gpt-5.4": {"input": 1.25, "cached_input": 0.125, "output": 10.0},
    "o4-mini": {"input": 1.10, "cached_input": 0.275, "output": 4.40},
}


def ext_lang(ext: str) -> str | None:
    return EXT_TO_LANG.get(ext.lower())


def claude_slug(path: Path) -> str:
    """Convert an absolute path to the Claude-Code project slug format."""
    p = str(path.resolve())
    return p.replace("/", "-")


def claude_session_dir(project_dir: Path) -> Path:
    return CLAUDE_PROJECTS / claude_slug(project_dir)


def iter_jsonl(path: Path) -> Iterable[dict]:
    """Yield JSON objects, tolerating malformed lines and empty lines."""
    try:
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        return


def is_git_repo(path: Path) -> bool:
    return (path / ".git").exists()


def git(cmd: list[str], cwd: Path) -> str:
    try:
        r = subprocess.run(
            ["git", *cmd],
            cwd=str(cwd),
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        return r.stdout.strip()
    except Exception:
        return ""


@dataclass
class LocStats:
    files_by_lang: dict[str, int] = field(default_factory=dict)
    loc_by_lang: dict[str, int] = field(default_factory=dict)
    total_files: int = 0
    total_loc: int = 0


def compute_loc(root: Path) -> LocStats:
    """Walk root and count files + lines, grouped by language."""
    stats = LocStats()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS and not d.startswith(".")]
        for name in filenames:
            if name.startswith("."):
                continue
            p = Path(dirpath) / name
            ext = p.suffix
            lang = ext_lang(ext)
            if not lang:
                continue
            try:
                if p.stat().st_size > 20 * 1024 * 1024:
                    # Skip very large files (probably PGN dumps or binaries).
                    continue
                with p.open("rb") as fh:
                    content = fh.read()
                # Decode leniently.
                try:
                    text = content.decode("utf-8", errors="replace")
                except Exception:
                    continue
                loc = text.count("\n") + (0 if text.endswith("\n") or not text else 1)
            except Exception:
                continue
            stats.files_by_lang[lang] = stats.files_by_lang.get(lang, 0) + 1
            stats.loc_by_lang[lang] = stats.loc_by_lang.get(lang, 0) + loc
            stats.total_files += 1
            stats.total_loc += loc
    return stats


def primary_language(loc: LocStats) -> str | None:
    """Pick the primary *code* language (skip Markdown/Text/JSON-ish)."""
    NONCODE = {"Markdown", "Text", "JSON", "YAML", "TOML", "XML"}
    candidates = [(lang, n) for lang, n in loc.loc_by_lang.items() if lang not in NONCODE]
    if not candidates:
        return None
    candidates.sort(key=lambda x: -x[1])
    return candidates[0][0]


def fmt_ts(iso: str | None) -> str:
    if not iso:
        return ""
    try:
        d = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return d.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return iso


def safe_int(x) -> int:
    try:
        return int(x or 0)
    except Exception:
        return 0


def detect_agent_suffix(name: str) -> str | None:
    """Naming convention: '-cc' => Claude Code, '-codex' => Codex."""
    n = name.lower()
    if n.endswith("-cc") or "-cc-" in n:
        return "Claude Code"
    if n.endswith("-codex") or "-codex-" in n or "codex" in n:
        return "Codex"
    if "claude" in n:
        return "Claude Code"
    return None


# Chess-specific feature patterns used for lightweight code detection.
# Patterns are intentionally permissive (many of these engines use unusual
# languages where conventional code doesn't apply).
CHESS_PATTERNS = {
    # Core / rules
    "FEN parsing": re.compile(r"\b(fen|FEN)\b"),
    "UCI protocol": re.compile(r"\b(uci|UCI|position\s+startpos|go\s+depth|bestmove)\b"),
    "Perft": re.compile(r"\b[Pp]erft\b"),
    "Castling": re.compile(r"castling|kingside|queenside|O-O"),
    "En passant": re.compile(r"en[_ ]?passant|enpassant", re.I),
    "Promotion": re.compile(r"\bpromot", re.I),
    "Check/Checkmate": re.compile(r"checkmate|stalemate|in[_ ]?check", re.I),
    "PGN": re.compile(r"\bPGN\b|\.pgn"),
    # Board representation (fine-grained)
    "Board: 0x88": re.compile(r"\b0x88\b|0X88"),
    "Board: bitboard": re.compile(r"bitboard|\bu64\b|BitBoard", re.I),
    "Board: magic bitboards": re.compile(r"magic[_ ]?bitboard|magic[_ ]?number|precomputed[_ ]?magic", re.I),
    "Board: mailbox 8x8": re.compile(r"mailbox|8x8[_ ]?board|8\s*x\s*8\s*array|board\[8\]\[8\]|board\[64\]", re.I),
    "Board: mailbox 10x12": re.compile(r"10x12|10\s*x\s*12"),
    # Search core
    "Minimax/Negamax": re.compile(r"minimax|negamax|MiniMax|NegaMax", re.I),
    "Alpha-beta": re.compile(r"alpha[- ]?beta|alphabeta", re.I),
    "Iterative deepening": re.compile(r"iterative[_ ]?deepen", re.I),
    "Quiescence": re.compile(r"quiescence|qsearch", re.I),
    "Transposition table": re.compile(r"transposition|\bTT\b|zobrist", re.I),
    "Zobrist hashing": re.compile(r"zobrist|hash[_ ]?key\s*=", re.I),
    # Search extensions (finer)
    "Move ordering (MVV-LVA)": re.compile(r"\bMVV[- ]?LVA\b", re.I),
    "Killer moves": re.compile(r"killer[_ ]move|killer[_ ]?heur", re.I),
    "History heuristic": re.compile(r"history[_ ]heuristic|history[_ ]table", re.I),
    "Principal-variation (PV)": re.compile(r"\bprincipal[_ ]variation\b|\bPV[_ ]?move\b|\bPVS\b", re.I),
    "Null-move pruning": re.compile(r"null[_ -]?move", re.I),
    "Late-move reduction (LMR)": re.compile(r"\bLMR\b|late[_ ]move[_ ]reduct", re.I),
    "Late-move pruning (LMP)": re.compile(r"\bLMP\b|late[_ ]move[_ ]prun", re.I),
    "Aspiration windows": re.compile(r"aspiration[_ ]?window", re.I),
    "Futility pruning": re.compile(r"futility", re.I),
    "Razoring": re.compile(r"razor", re.I),
    # Evaluation (finer)
    "Evaluation/PST": re.compile(r"piece[_ ]?square|\bPST\b", re.I),
    "Tapered evaluation": re.compile(r"tapered|phased[_ ]?eval|midgame[_ ]?endgame|mg[_ ]?eg", re.I),
    "King safety": re.compile(r"king[_ ]?safety|pawn[_ ]?shelter|king[_ ]?tropism", re.I),
    "Pawn structure": re.compile(r"pawn[_ ]?structure|passed[_ ]?pawn|isolated[_ ]?pawn|doubled[_ ]?pawn|backward[_ ]?pawn", re.I),
    "Mobility": re.compile(r"\bmobility\b", re.I),
    "Material counting": re.compile(r"material|piece[_ ]?value", re.I),
    # Meta / strong-engine features
    "Opening book": re.compile(r"opening[_ ]?book|polyglot|ecol", re.I),
    "Endgame tables": re.compile(r"syzygy|tablebase|nalimov|gaviota", re.I),
    "Time management": re.compile(r"time[_ ]?management|wtime|btime|movetime|time[_ ]?control", re.I),
    "NNUE/neural eval": re.compile(r"\bNNUE\b|neural[_ ]network|efficiently[_ ]updatable", re.I),
}

# Feature groups (for grouped table views in the paper).
FEATURE_GROUPS: dict[str, list[str]] = {
    "Rules & protocol": [
        "FEN parsing", "UCI protocol", "PGN", "Castling", "En passant",
        "Promotion", "Check/Checkmate",
    ],
    "Board representation": [
        "Board: 0x88", "Board: bitboard", "Board: magic bitboards",
        "Board: mailbox 8x8", "Board: mailbox 10x12",
    ],
    "Search core": [
        "Minimax/Negamax", "Alpha-beta", "Iterative deepening", "Quiescence",
        "Transposition table", "Zobrist hashing", "Perft",
    ],
    "Search extensions": [
        "Move ordering (MVV-LVA)", "Killer moves", "History heuristic",
        "Principal-variation (PV)", "Null-move pruning",
        "Late-move reduction (LMR)", "Late-move pruning (LMP)",
        "Aspiration windows", "Futility pruning", "Razoring",
    ],
    "Evaluation": [
        "Material counting", "Evaluation/PST", "Tapered evaluation",
        "King safety", "Pawn structure", "Mobility",
    ],
    "Strong-engine features": [
        "Opening book", "Endgame tables", "Time management", "NNUE/neural eval",
    ],
}


def scan_features(root: Path, max_bytes_per_file: int = 2_000_000) -> dict[str, list[str]]:
    """Return {feature: [relative-paths where matched]}. Only code/docs files."""
    hits: dict[str, list[str]] = {k: [] for k in CHESS_PATTERNS}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS and not d.startswith(".")]
        for name in filenames:
            if name.startswith("."):
                continue
            p = Path(dirpath) / name
            if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".tar", ".gz", ".bz2", ".bin", ".exe", ".o", ".so", ".dylib"}:
                continue
            try:
                if p.stat().st_size > max_bytes_per_file:
                    continue
                with p.open("rb") as fh:
                    raw = fh.read()
                text = raw.decode("utf-8", errors="replace")
            except Exception:
                continue
            for feat, pat in CHESS_PATTERNS.items():
                if pat.search(text):
                    hits[feat].append(str(p.relative_to(root)))
    return hits


def short_quote(text: str, limit: int = 160) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > limit:
        return text[: limit - 1] + "…"
    return text
