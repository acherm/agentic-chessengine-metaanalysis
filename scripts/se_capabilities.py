"""Characterise software-engineering capabilities exhibited per session.

Moves beyond a "did the agent produce code?" view to a "which SE
activities did the agent actually do?" view. The output is both a
machine-readable per-engine profile (counts per capability) and a
human-readable report that corroborates the paper's claim that
coding-agent sessions display a broad spectrum of SE behaviour ---
not only implementation, but also requirements reasoning, protocol
engineering, testing, debugging, build/tooling, benchmarking,
code comprehension, refactoring, performance engineering, and
documentation.

Inputs:
  data/projects/<name>-trajectory.json   produced by scripts/trajectory.py

Outputs:
  data/se_capabilities.json              per-engine {capability: count}
  reports/SE_CAPABILITIES.md             human-readable synthesis with
                                         representative examples

Usage:
  python3 scripts/se_capabilities.py              # all engines + variants
  python3 scripts/se_capabilities.py chess-ruby-cc   # one engine
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import DATA_DIR, REPORTS_DIR

# ---------- Taxonomy ---------------------------------------------------

# Ten SE capabilities, tied to concrete evidence streams in the
# trajectory data. Keys are short identifiers; labels and evidence rules
# are documented here so the full codebook is one file to read.
# The taxonomy went through one revision cycle: the initial 13-category
# frame split implementation / protocol-engineering / refactoring and
# treated requirements-spec / architecture-design separately. Auditing
# the matrix revealed that those splits were brittle --- "new source file
# with SRC_EXTS" is too narrow a signal for implementation (most coding
# happens through edits), protocol work is indistinguishable from the
# implementation it lives inside, and the refactoring/design splits
# picked up too few events to be informative. We merged them. The
# reduced frame also has broader tagging rules for implementation
# (new OR edited source) and testing (any perft / UCI / cutechess /
# engine-smoke-run bash activity, plus test-path files).
SE_CAPABILITIES: dict[str, dict[str, Any]] = {
    "design": {
        "label": "Design \\& specification",
        "description": (
            "Up-front design activity: reading or authoring SPECIFICATION, "
            "ARCHITECTURE, PLAN, ROADMAP, REQUIREMENTS, DESIGN, or README "
            "documents; the first pass of a build-system manifest; or a "
            "multi-file layout step (new files across $\\geq$2 directories). "
            "Captures both 'interpret the user's goal into a plan' and "
            "'decide the top-level module structure'."
        ),
    },
    "implementation": {
        "label": "Implementation",
        "description": (
            "Writing or editing source files in a canonical programming "
            "language --- the core code-authoring activity. Fires on new "
            "source files and on edits to existing source files; explicitly "
            "subsumes wire-format parser work (UCI, FEN, PGN, SAN) and "
            "edit-only iterations (refactoring, small rewrites), which in "
            "earlier drafts of this frame were separate categories but "
            "could not be reliably disentangled from ordinary implementation "
            "in the trajectory data."
        ),
    },
    "testing": {
        "label": "Testing",
        "description": (
            "Correctness-oriented verification: running perft, invoking the "
            "engine under UCI to check it boots and plays legal moves, "
            "running a test harness (pytest, cargo test, dune test, "
            "cutechess), editing test-path files (\\texttt{tests/}, "
            "\\texttt{test\\_*}, \\texttt{*\\_test.*}). Distinct from "
            "benchmarking, which measures strength rather than correctness."
        ),
    },
    "debugging": {
        "label": "Debugging",
        "description": (
            "Fix-oriented iteration: the user reports a bug (BugFixRequest "
            "intent), the prompt contains debugging vocabulary "
            "(``bug'', ``fix'', ``illegal'', ``segfault''), the step class "
            "is \\texttt{debug}, or the step edits existing files with a "
            "build/test cycle and no new authoring. Evidence of "
            "self-correction rather than first-pass generation."
        ),
    },
    "build-tooling": {
        "label": "Build \\& tooling",
        "description": (
            "Build-system edits (Makefile, Cargo.toml, CMakeLists.txt, "
            "pyproject.toml, Gemfile, lakefile, dune-project, package.json) "
            "after the initial manifest, package installs, and compile "
            "invocations. The first-authoring of a manifest counts as "
            "\\emph{design}; subsequent build-config work counts here."
        ),
    },
    "version-control": {
        "label": "Version control",
        "description": "git add/commit/log/branch/diff operations.",
    },
    "benchmarking-eval": {
        "label": "Benchmarking \\& evaluation",
        "description": (
            "Strength-measurement activity: running cutechess-cli or "
            "Stockfish as an opponent, authoring bespoke Elo-estimation "
            "scripts or tournament drivers, touching files with "
            "\\texttt{elo}/\\texttt{tournament}/\\texttt{gauntlet} in the name. "
            "Distinct from testing (which is correctness)."
        ),
    },
    "code-comprehension": {
        "label": "Code comprehension",
        "description": (
            "Read / Grep / Glob / WebSearch tool uses and \\texttt{cat}/"
            "\\texttt{head}/\\texttt{grep}-style inspection bash. Evidence "
            "of the agent exploring existing code or external references "
            "before editing."
        ),
    },
    "performance-eng": {
        "label": "Performance engineering",
        "description": (
            "\\texttt{--release} / \\texttt{-O2} / \\texttt{-O3} flags, "
            "profiling invocations, or performance vocabulary in the user "
            "prompt (``optimise'', ``faster'', ``bottleneck'', ``nodes/"
            "sec''). Evidence that the agent treats runtime performance "
            "as a first-class concern."
        ),
    },
    "documentation": {
        "label": "Documentation",
        "description": (
            "Writing or editing Markdown files that are not the "
            "design/spec/plan docs (those belong to \\emph{design}). "
            "Evidence of narrative writing as part of the delivery."
        ),
    },
}

# ---------- Language-category mapping ---------------------------------

# Five paper-taxonomy buckets (RQ1), keyed by engine name. Driven by
# the *target* language / protocol, not by LOC (which mis-labels e.g.
# chess-cobol-cc as C because GnuCOBOL emits C).
LANG_CATEGORY: dict[str, str] = {
    # mainstream general-purpose
    "chess-cplusplus-claude": "mainstream",
    "cplusplus-chess": "mainstream",
    "chess-java": "mainstream",
    "chess-java-cc": "mainstream",
    "chess-mojo": "mainstream",
    "chess-purec": "mainstream",
    "chess-purec-codex": "mainstream",
    "chess-py": "mainstream",
    "chess-py-cc": "mainstream",
    "chess-ruby-cc": "mainstream",
    "chess-ruby-codex": "mainstream",
    "chess-rust-cc": "mainstream",
    "chess-rust-cc-redo": "mainstream",
    "chess-rust-codex": "mainstream",
    "chess-revisit-java-toRust-codex": "mainstream",
    # specialized / academic / agent-designed DSL
    "chess-Rocq": "specialized",
    "chess-apl-codex54": "specialized",
    "chess-icon-codex": "specialized",
    "chess-why3": "specialized",
    "chess-why3-cc": "specialized",
    "lean-chess": "specialized",
    "chess-newlang-codex": "specialized",  # engine-dsl special-role
    # domain-specific / markup
    "chess-css-codex": "domain-specific",
    "chess-css-codex-guided": "domain-specific",
    "chess-latex-codex-replication": "domain-specific",
    "latex-chess-engine": "domain-specific",
    "chess-sql": "domain-specific",
    "test-superset": "domain-specific",
    # legacy
    "COBOL-chess": "legacy",
    "chess-cobol-cc": "legacy",
    "chess-revisit-java-toCOBOL-codex": "legacy",
    "chess-assembly-codex": "legacy",
    # strictly esoteric
    "chess-brainfuck": "esoteric",
    "chess-brainfuck-cc": "esoteric",
}

CATEGORY_ORDER = ["mainstream", "specialized", "domain-specific", "legacy", "esoteric"]
CATEGORY_LABEL = {
    "mainstream": "Mainstream general-purpose",
    "specialized": "Specialized / academic",
    "domain-specific": "Domain-specific / markup",
    "legacy": "Legacy",
    "esoteric": "Esoteric",
}


# ---------- Tagging rules ----------------------------------------------

DOC_NAME_RE = re.compile(
    r"(SPECIFICATION|ARCHITECTURE|PLAN|ROADMAP|REQUIREMENTS|DESIGN|README)",
    re.I,
)
BUILD_MANIFEST_RE = re.compile(
    r"(CMakeLists\.txt|Cargo\.toml|lakefile|dune-project|pyproject\.toml|"
    r"package\.json|Gemfile|Makefile|setup\.py|setup\.cfg|pom\.xml|"
    r"build\.gradle|go\.mod|stack\.yaml)$"
)
PROTOCOL_NAME_RE = re.compile(r"(uci|pgn|fen|san|parser|protocol)", re.I)
TEST_PATH_RE = re.compile(r"(/|^)(test|tests|spec|specs)/|(^|/)(test_|_test\.)", re.I)
SRC_EXTS = {
    ".py", ".rs", ".c", ".h", ".cpp", ".cc", ".hpp", ".cxx", ".java",
    ".rb", ".go", ".lua", ".ml", ".mli", ".lean", ".v", ".why", ".mlw",
    ".cob", ".cpy", ".cobol", ".bf", ".apl", ".aplf", ".icn", ".mojo",
    ".asm", ".s", ".S", ".tex", ".sty", ".ltx", ".css", ".scss", ".html",
    ".js", ".mjs", ".ts", ".tsx", ".sql", ".kt", ".swift", ".scala",
    ".hs", ".zig", ".d", ".jl", ".nim", ".cr",
}
DOC_MD_RE = re.compile(r"\.md$", re.I)
BUG_VOCAB = re.compile(
    r"\b(bug|fix|broken|doesn'?t work|fails?|error|wrong|incorrect|"
    r"illegal|segfault|crash|hang|regression|issue)\b",
    re.I,
)
PERF_VOCAB = re.compile(
    r"\b(perf|performance|profile|profiling|optimi[sz]e|optimi[sz]ation|"
    r"faster|slower|bottleneck|nodes[\s/]?sec|nps|throughput|latency|"
    r"release build|O[23])\b",
    re.I,
)
REFACTOR_VOCAB = re.compile(
    r"\b(refactor|restructur|rename|extract|cleanup|split\s+(file|module|function))\b",
    re.I,
)
SPEC_VOCAB = re.compile(
    r"\b(spec(?:ification)?|plan|architecture|design|requirement|blueprint|"
    r"contract)\b",
    re.I,
)


def file_ext(p: str) -> str:
    return Path(p).suffix.lower()


BENCH_FILE_RE = re.compile(
    r"(elo|benchmark|tournament|gauntlet|estimate_elo|elo_test)",
    re.I,
)


def tag_step(step: dict) -> set[str]:
    tags: set[str] = set()
    tool_counts = step.get("tool_counts") or {}
    bash_kinds = step.get("bash_kinds") or {}
    bash_samples = step.get("bash_samples") or []
    new_files = step.get("files_written") or []
    edit_files = step.get("files_edited") or []
    read_files = step.get("files_read") or []
    all_touched = new_files + edit_files
    n_new = len(new_files)
    n_edit = len(edit_files)
    prompt = (step.get("user_prompt") or "").lower()
    intent = set(step.get("user_intent") or [])
    task_class = step.get("task_class", "")

    # --- design & specification ---------------------------------------
    # Up-front planning: spec/arch/plan docs, first-authoring of a build
    # manifest, or a multi-file layout step. Subsequent build-config
    # edits go to build-tooling instead.
    if any(DOC_NAME_RE.search(Path(f).name) for f in all_touched):
        tags.add("design")
    if SPEC_VOCAB.search(prompt) and (n_new >= 1 or n_edit >= 1):
        tags.add("design")
    if any(BUILD_MANIFEST_RE.search(Path(f).name) for f in new_files):
        tags.add("design")
    if n_new >= 3:
        dirs = {str(Path(f).parent) for f in new_files}
        if len(dirs) >= 2:
            tags.add("design")

    # --- implementation -----------------------------------------------
    # Fire on any step that writes OR edits a source file. This is the
    # main fix from the earlier draft of the frame: the narrower
    # "new source file only" rule missed most coding activity because
    # agents do most work through edits. Protocol engineering and small
    # refactoring rewrites are subsumed here.
    src_touched = [f for f in all_touched if file_ext(f) in SRC_EXTS]
    if src_touched:
        tags.add("implementation")

    # --- testing ------------------------------------------------------
    # Any test-path file (tests/, test_*, *_test.*) and a broad set of
    # correctness-checking bash kinds: perft (exhaustive move-generation
    # count), test harness invocations, and uci_run (smoke-run the
    # engine under UCI to check it boots and plays legal moves, which
    # is how every engine in the corpus is first verified).
    if any(TEST_PATH_RE.search(f) for f in all_touched):
        tags.add("testing")
    if (
        bash_kinds.get("test", 0) > 0
        or bash_kinds.get("perft", 0) > 0
        or bash_kinds.get("uci_run", 0) > 0
    ):
        tags.add("testing")

    # --- debugging ----------------------------------------------------
    if "BugFixRequest" in intent:
        tags.add("debugging")
    if BUG_VOCAB.search(prompt):
        tags.add("debugging")
    if task_class == "debug":
        tags.add("debugging")
    # Edit-heavy with a build/test/uci cycle and no new authoring is an
    # operational debug loop even without explicit vocab.
    if n_edit >= 2 and n_new == 0 and (
        bash_kinds.get("build", 0)
        + bash_kinds.get("test", 0)
        + bash_kinds.get("uci_run", 0)
        >= 1
    ):
        tags.add("debugging")

    # --- build & tooling ----------------------------------------------
    # Subsequent build-config edits (first authoring goes to design),
    # package installs, and compile invocations.
    if any(
        BUILD_MANIFEST_RE.search(Path(f).name) for f in edit_files
    ):
        tags.add("build-tooling")
    if (
        bash_kinds.get("build", 0) > 0
        or bash_kinds.get("package", 0) > 0
    ):
        tags.add("build-tooling")

    # --- version control ----------------------------------------------
    if bash_kinds.get("git", 0) > 0:
        tags.add("version-control")

    # --- benchmarking & evaluation ------------------------------------
    if (
        bash_kinds.get("gauntlet", 0) > 0
        or bash_kinds.get("stockfish", 0) > 0
    ):
        tags.add("benchmarking-eval")
    if any(BENCH_FILE_RE.search(Path(f).name) for f in all_touched):
        tags.add("benchmarking-eval")

    # --- code comprehension -------------------------------------------
    explore_tools = (
        tool_counts.get("Read", 0)
        + tool_counts.get("Grep", 0)
        + tool_counts.get("Glob", 0)
        + tool_counts.get("WebSearch", 0)
        + tool_counts.get("WebFetch", 0)
    )
    if explore_tools >= 3 or bash_kinds.get("inspect", 0) >= 3:
        tags.add("code-comprehension")
    if read_files:
        tags.add("code-comprehension")

    # --- performance engineering --------------------------------------
    if PERF_VOCAB.search(prompt):
        tags.add("performance-eng")
    for cmd in bash_samples:
        if re.search(r"--release\b|-O2\b|-O3\b|\btime\s+|\bperf\s+|criterion",
                     cmd or ""):
            tags.add("performance-eng")
            break

    # --- documentation ------------------------------------------------
    # Markdown files that are NOT the design/spec/plan docs (those
    # already count for design).
    for f in new_files + edit_files:
        if DOC_MD_RE.search(f) and not DOC_NAME_RE.search(Path(f).name):
            tags.add("documentation")
            break

    return tags


# ---------- Aggregation ------------------------------------------------

# Ordinal intensity levels per capability per engine. We rank by the
# *share* of the session's steps in which the capability was exercised
# (rather than raw count), because step counts span two orders of
# magnitude across the corpus (1 step for the shortest main transcript
# to 192 for the longest). A capability with 5% coverage means roughly
# "the agent reached for it every 20 steps" regardless of how long the
# session ran.
LIKERT_LABELS = {0: "—", 1: "\u25cf", 2: "\u25cf\u25cf", 3: "\u25cf\u25cf\u25cf"}
LIKERT_NAMES = {0: "absent", 1: "light", 2: "moderate", 3: "heavy"}


def likert_level(n_events: int, n_steps: int) -> int:
    """0 absent / 1 light / 2 moderate / 3 heavy.

    Threshold rationale: 0 events is absent. A single event (one step)
    is light regardless of session length. Above 1 event we use share:
    (1,5%] remains light, (5%,20%] is moderate, >20% is heavy. The 5%
    / 20% cuts are intentionally coarse --- the scale is an ordinal
    indicator, not a precise rate."""
    if n_events <= 0:
        return 0
    if n_events == 1:
        return 1
    share = n_events / max(1, n_steps)
    if share > 0.20:
        return 3
    if share > 0.05:
        return 2
    return 1


def aggregate_engine(name: str, traj_path: Path) -> dict[str, Any]:
    try:
        traj = json.loads(traj_path.read_text())
    except Exception:
        return {}
    steps = traj.get("steps") or []
    per_cap: Counter = Counter()
    per_cap_steps: dict[str, list[int]] = defaultdict(list)
    for s in steps:
        caps = tag_step(s)
        for c in caps:
            per_cap[c] += 1
            per_cap_steps[c].append(s.get("index"))
    n_steps = len(steps)
    levels = {c: likert_level(per_cap[c], n_steps) for c in SE_CAPABILITIES}
    return {
        "name": name,
        "n_steps": n_steps,
        "capabilities": dict(per_cap),
        "capability_levels": levels,
        "capability_step_indices": {k: sorted(v) for k, v in per_cap_steps.items()},
        "n_distinct_capabilities": sum(1 for v in levels.values() if v > 0),
    }


def example_step_ref(engine: dict[str, Any], cap: str) -> str:
    idxs = engine.get("capability_step_indices", {}).get(cap, [])
    if not idxs:
        return ""
    return f"step {idxs[0]}" if len(idxs) == 1 else f"steps {idxs[0]}--{idxs[-1]} ({len(idxs)} hits)"


# ---------- Rendering --------------------------------------------------

def short_engine_name(name: str) -> str:
    return name.replace("chess-", "")


def render_report(engines: list[dict[str, Any]]) -> str:
    if not engines:
        return "# SE capabilities\n\n_No engines with trajectory data found._\n"

    n_engines = len(engines)
    # Cross-engine aggregates
    cap_engine_counts: Counter = Counter()  # capability -> #engines with >=1
    cap_event_counts: Counter = Counter()   # capability -> total events
    for e in engines:
        for c, n in e.get("capabilities", {}).items():
            cap_engine_counts[c] += 1 if n >= 1 else 0
            cap_event_counts[c] += n

    # Sort capabilities by engine-coverage (descending), then by event count
    cap_order = sorted(
        SE_CAPABILITIES.keys(),
        key=lambda c: (-cap_engine_counts[c], -cap_event_counts[c]),
    )

    L: list[str] = []
    L.append("# Software-engineering capabilities exhibited across the corpus")
    L.append("")
    L.append(f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}._")
    L.append("")
    L.append(
        "This report characterises the software-engineering activities "
        "observable in the agent sessions, beyond \"the agent produced code\". "
        f"Across {n_engines} engines (main corpus + special-role), each "
        "session is segmented into steps; each step is tagged against a "
        f"{len(SE_CAPABILITIES)}-capability taxonomy derived from the paper's "
        "research questions. A step can carry multiple tags."
    )
    L.append("")

    # Coding frame table
    L.append("## Capability taxonomy")
    L.append("")
    L.append("| ID | Label | Description |")
    L.append("|---|---|---|")
    for cid, meta in SE_CAPABILITIES.items():
        desc = meta["description"].replace("|", "\\|")
        L.append(f"| `{cid}` | {meta['label']} | {desc} |")
    L.append("")

    # Coverage table
    L.append("## Corpus coverage: how many engines exhibit each capability")
    L.append("")
    L.append("| Capability | # engines (of {n}) | Share | Total events |".format(n=n_engines))
    L.append("|---|---:|---:|---:|")
    for c in cap_order:
        n_eng = cap_engine_counts[c]
        pct = 100.0 * n_eng / max(1, n_engines)
        L.append(f"| {SE_CAPABILITIES[c]['label']} | {n_eng} | {pct:.0f}\\% | {cap_event_counts[c]} |")
    L.append("")

    L.append("## Per-engine intensity profile (Likert)")
    L.append("")
    L.append(
        "One row per engine; each column carries a 4-level ordinal intensity "
        "for that capability: `—` absent (0 steps), `\u25cf` light (1 step or "
        "\u22645% of the session), `\u25cf\u25cf` moderate (5--20%), "
        "`\u25cf\u25cf\u25cf` heavy (>20%). `Dist` is the number of "
        "capabilities exercised at any level (absent excluded)."
    )
    L.append("")
    # Short column headers
    SHORT_L = {
        "design": "Design",
        "implementation": "Impl",
        "testing": "Test",
        "debugging": "Debug",
        "build-tooling": "Build",
        "version-control": "VCS",
        "benchmarking-eval": "Bench",
        "code-comprehension": "Read",
        "performance-eng": "Perf",
        "documentation": "Docs",
    }
    header_L = "| Engine | Steps | " + " | ".join(SHORT_L[c] for c in cap_order) + " | Dist |"
    sep_L = "|---|---:|" + "---:|" * (len(cap_order) + 1)
    L.append(header_L)
    L.append(sep_L)
    engines_sorted_L = sorted(engines, key=lambda e: -e.get("n_distinct_capabilities", 0))
    for e in engines_sorted_L:
        row = [f"`{e['name']}`", str(e.get("n_steps", 0))]
        for c in cap_order:
            lvl = e.get("capability_levels", {}).get(c, 0)
            row.append(LIKERT_LABELS[lvl])
        row.append(str(e.get("n_distinct_capabilities", 0)))
        L.append("| " + " | ".join(row) + " |")
    L.append("")

    L.append("### Per-engine raw event counts (for reference)")
    L.append("")
    L.append(
        "Same row ordering; each cell is the raw step count for the "
        "capability. Included so reviewers can recompute any intensity "
        "level without re-running the tagger."
    )
    L.append("")
    # Short column headers
    SHORT = {
        "design": "Design",
        "implementation": "Impl",
        "testing": "Test",
        "debugging": "Debug",
        "build-tooling": "Build",
        "version-control": "VCS",
        "benchmarking-eval": "Bench",
        "code-comprehension": "Read",
        "performance-eng": "Perf",
        "documentation": "Docs",
    }
    header = "| Engine | Steps | " + " | ".join(SHORT[c] for c in cap_order) + " | Dist |"
    sep = "|---|---:|" + "---:|" * (len(cap_order) + 1)
    L.append(header)
    L.append(sep)
    engines_sorted = sorted(engines, key=lambda e: -e.get("n_distinct_capabilities", 0))
    for e in engines_sorted:
        row = [f"`{e['name']}`", str(e.get("n_steps", 0))]
        for c in cap_order:
            n = e.get("capabilities", {}).get(c, 0)
            row.append(str(n) if n else "")
        row.append(str(e.get("n_distinct_capabilities", 0)))
        L.append("| " + " | ".join(row) + " |")
    L.append("")

    # ---- Breakdown by language category (paper's RQ1 taxonomy) ----
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for e in engines:
        cat = LANG_CATEGORY.get(e["name"])
        if cat:
            by_cat[cat].append(e)

    L.append("## Breakdown by language category")
    L.append("")
    L.append(
        "Engines are grouped by the paper's RQ1 language taxonomy "
        "(mainstream general-purpose, specialized/academic, domain-specific/markup, "
        "legacy, esoteric). Each cell is the share of engines in that category "
        "that exhibited the capability at least once. Bottom rows: number of "
        "engines and median steps per engine in the category."
    )
    L.append("")

    cat_sizes = {c: len(by_cat.get(c, [])) for c in CATEGORY_ORDER}
    # Per-category, per-capability engine counts
    cat_cap_eng: dict[str, Counter] = {c: Counter() for c in CATEGORY_ORDER}
    cat_cap_ev: dict[str, Counter] = {c: Counter() for c in CATEGORY_ORDER}
    cat_median_steps: dict[str, float] = {}
    cat_mean_dist: dict[str, float] = {}
    for c in CATEGORY_ORDER:
        engs = by_cat.get(c, [])
        for e in engs:
            for cap, n in e.get("capabilities", {}).items():
                cat_cap_ev[c][cap] += n
                if n >= 1:
                    cat_cap_eng[c][cap] += 1
        steps = sorted(e.get("n_steps", 0) for e in engs)
        cat_median_steps[c] = steps[len(steps) // 2] if steps else 0.0
        dists = [e.get("n_distinct_capabilities", 0) for e in engs]
        cat_mean_dist[c] = sum(dists) / len(dists) if dists else 0.0

    # Heatmap-style table: rows = capabilities (saturation-ordered),
    # cols = categories.
    header = "| Capability | " + " | ".join(
        f"{CATEGORY_LABEL[c]}<br/>(n={cat_sizes[c]})" for c in CATEGORY_ORDER
    ) + " |"
    sep = "|---|" + "---:|" * len(CATEGORY_ORDER)
    L.append(header)
    L.append(sep)
    for cap in cap_order:
        row = [SE_CAPABILITIES[cap]["label"]]
        for c in CATEGORY_ORDER:
            n = cat_cap_eng[c].get(cap, 0)
            total = cat_sizes[c]
            if total == 0:
                row.append("—")
            else:
                pct = 100.0 * n / total
                row.append(f"{n}/{total} ({pct:.0f}\\%)")
        L.append("| " + " | ".join(row) + " |")
    # Footer rows
    L.append(
        "| **Median steps/engine** | "
        + " | ".join(f"{cat_median_steps[c]:.0f}" for c in CATEGORY_ORDER)
        + " |"
    )
    L.append(
        "| **Mean distinct capabilities/engine** | "
        + " | ".join(f"{cat_mean_dist[c]:.1f}" for c in CATEGORY_ORDER)
        + " |"
    )
    L.append("")

    # Narrative commentary: which capabilities differ sharply across
    # categories, and which are category-invariant.
    L.append("### Category-sensitive vs category-invariant capabilities")
    L.append("")
    ranked: list[tuple[str, float, dict[str, float]]] = []
    for cap in cap_order:
        shares = {c: (cat_cap_eng[c].get(cap, 0) / cat_sizes[c] if cat_sizes[c] else 0.0)
                  for c in CATEGORY_ORDER}
        spread = max(shares.values()) - min(shares.values())
        ranked.append((cap, spread, shares))
    ranked.sort(key=lambda t: -t[1])
    L.append("Capabilities ranked by across-category spread (max share minus min share):")
    L.append("")
    L.append("| Capability | Spread | Highest category | Lowest category |")
    L.append("|---|---:|---|---|")
    for cap, spread, shares in ranked:
        hi_c = max(shares, key=lambda c: shares[c])
        lo_c = min(shares, key=lambda c: shares[c])
        L.append(
            f"| {SE_CAPABILITIES[cap]['label']} | {spread*100:.0f} pp | "
            f"{CATEGORY_LABEL[hi_c]} ({shares[hi_c]*100:.0f}\\%) | "
            f"{CATEGORY_LABEL[lo_c]} ({shares[lo_c]*100:.0f}\\%) |"
        )
    L.append("")

    # Per-category paradigm engine: the one with the largest distinct-capability set.
    L.append("### Representative engine per category (largest distinct-capability set)")
    L.append("")
    for c in CATEGORY_ORDER:
        engs = by_cat.get(c, [])
        if not engs:
            L.append(f"- **{CATEGORY_LABEL[c]}**: _no engines in category._")
            continue
        top = max(engs, key=lambda e: (e.get("n_distinct_capabilities", 0),
                                        e.get("n_steps", 0)))
        L.append(
            f"- **{CATEGORY_LABEL[c]}** ({len(engs)} engines): "
            f"`{top['name']}` exercises {top.get('n_distinct_capabilities', 0)} "
            f"of {len(SE_CAPABILITIES)} capabilities across "
            f"{top.get('n_steps', 0)} steps."
        )
    L.append("")

    # Paradigm case per capability: engine with the most events
    L.append("## Paradigm cases: the engine most exemplifying each capability")
    L.append("")
    for c in cap_order:
        top = max(engines, key=lambda e: e.get("capabilities", {}).get(c, 0))
        top_n = top.get("capabilities", {}).get(c, 0)
        if top_n == 0:
            continue
        example = example_step_ref(top, c)
        L.append(f"- **{SE_CAPABILITIES[c]['label']}** "
                 f"`{c}`: `{top['name']}` ({top_n} tagged steps; {example}).")
    L.append("")

    # Universality / rarity commentary
    universal = [c for c in cap_order if cap_engine_counts[c] >= int(0.8 * n_engines)]
    majority = [c for c in cap_order if int(0.5 * n_engines) <= cap_engine_counts[c] < int(0.8 * n_engines)]
    rare = [c for c in cap_order if cap_engine_counts[c] < int(0.5 * n_engines)]
    L.append("## Saturation summary")
    L.append("")
    L.append(f"- **Universal (\\geq 80\\% of engines):** {', '.join('`'+c+'`' for c in universal) or '_none_'}.")
    L.append(f"- **Majority (50--80\\% of engines):** {', '.join('`'+c+'`' for c in majority) or '_none_'}.")
    L.append(f"- **Selective (< 50\\% of engines):** {', '.join('`'+c+'`' for c in rare) or '_none_'}.")
    L.append("")

    L.append("## Notes and caveats")
    L.append("")
    L.append(
        "- Tagging rules are heuristic, file-path + bash-command + prompt-vocabulary "
        "based. A step can be mis-tagged; the coarse coverage pattern (which "
        "capabilities are universal vs.\\ rare) is robust, individual rows should "
        "be spot-checked against the per-engine trajectory reports."
    )
    L.append(
        "- Engines with archived main transcripts (`chess-java-cc`, the second "
        "TeX engine, two `-cc` projects whose main JSONL is gone) show reduced "
        "capability counts because tool-use events cannot be recovered; see the "
        "provenance notes in the corresponding per-engine dossiers."
    )
    L.append(
        "- The `implementation` count is deliberately a count of *steps that "
        "wrote at least one new source file*, not a count of LOC. A Ruby engine "
        "built in one big step carries `implementation`=1 despite writing "
        "thousands of lines; the debug / testing / benchmarking counts are "
        "typically higher. Read the profile table as ``was this activity "
        "exercised?'' not ``how much code did this activity produce?''"
    )
    return "\n".join(L) + "\n"


LIKERT_TEX = {
    0: "$-$",
    1: "$\\bullet$",
    2: "$\\bullet\\bullet$",
    3: "$\\bullet\\bullet\\bullet$",
}


ARCHIVED_ENGINES = {
    "chess-cplusplus-claude", "chess-purec", "chess-py-cc",
    "chess-rust-cc", "chess-sql", "chess-why3-cc", "test-superset",
}


def render_latex_matrix(engines: list[dict[str, Any]]) -> str:
    """Full per-engine x capability Likert matrix as a LaTeX table.

    Rows are sorted by language category (mainstream, specialized,
    domain-specific, legacy, esoteric) then by intensity (summed Likert)
    descending within category, then by name. A horizontal rule
    separates categories so readers can see the per-category gradient
    at a glance."""
    cap_order = list(SE_CAPABILITIES.keys())
    SHORT = {
        "design":             "Design",
        "implementation":     "Impl",
        "testing":            "Test",
        "debugging":          "Debug",
        "build-tooling":      "Build",
        "version-control":    "VCS",
        "benchmarking-eval":  "Bench",
        "code-comprehension": "Read",
        "performance-eng":    "Perf",
        "documentation":      "Docs",
    }
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for e in engines:
        cat = LANG_CATEGORY.get(e["name"])
        if cat:
            by_cat[cat].append(e)
    for c in CATEGORY_ORDER:
        by_cat[c].sort(
            key=lambda e: (
                -sum(e.get("capability_levels", {}).values()),
                e["name"],
            )
        )

    L: list[str] = []
    L.append("\\begin{table*}[t]\\centering\\scriptsize")
    L.append(
        "\\caption{SE-activity intensity profile per engine, grouped "
        "by the RQ1 language taxonomy. Each cell is the Likert level "
        "on the share of the session's steps tagged with that "
        "capability: $-$ absent, $\\bullet$ light (1 event or "
        "$\\leq$5\\%), $\\bullet\\bullet$ moderate (5--20\\%), "
        "$\\bullet\\bullet\\bullet$ heavy ($>$20\\%). \\textsc{Steps} "
        "= total trajectory steps; \\textsc{\\#Caps} = number of "
        "capabilities exercised at any level; \\textsc{Int.} = summed "
        "Likert (0--30). Horizontal rules separate language "
        "categories; rows within each category are sorted by intensity "
        "descending. Column abbreviations: Design (design \\& spec), "
        "Impl (implementation --- writing or editing source files), "
        "Test (testing --- perft, UCI smoke, test harness), Debug "
        "(debugging), Build (build \\& tooling), VCS (version control), "
        "Bench (benchmarking --- strength measurement), Read (code "
        "comprehension), Perf (performance engineering), Docs "
        "(documentation). A dagger ($^\\dagger$) marks engines whose "
        "main session transcripts were compacted by \\claudecode{} "
        "before capture: the row reflects only the surviving "
        "subagent sidecars, which is a strict lower bound on the "
        "session's actual SE activity (\\Cref{sec:threats}).}"
    )
    L.append("\\label{tab:rq1-se-matrix}")
    L.append("\\resizebox{\\textwidth}{!}{%")
    cols = "l l " + "c" * len(cap_order) + " r r r"
    L.append(f"\\begin{{tabular}}{{{cols}}}")
    L.append("\\toprule")
    header = ["Engine", "Lang."]
    header.extend(SHORT[c] for c in cap_order)
    header.extend(["Steps", "\\#Caps", "Int."])
    L.append(" & ".join(header) + " \\\\")
    L.append("\\midrule")

    display_lang = {
        "chess-cplusplus-claude": "C++", "cplusplus-chess": "C++",
        "chess-java": "Java", "chess-java-cc": "Java",
        "chess-mojo": "Mojo", "chess-purec": "C", "chess-purec-codex": "C",
        "chess-py": "Python", "chess-py-cc": "Python",
        "chess-ruby-cc": "Ruby", "chess-ruby-codex": "Ruby",
        "chess-rust-cc": "Rust", "chess-rust-cc-redo": "Rust",
        "chess-rust-codex": "Rust",
        "chess-revisit-java-toRust-codex": "Rust (port)",
        "chess-Rocq": "Rocq", "chess-apl-codex54": "APL",
        "chess-icon-codex": "Icon", "chess-why3": "Why3",
        "chess-why3-cc": "Why3", "lean-chess": "Lean",
        "chess-newlang-codex": "DSL",
        "chess-css-codex": "CSS", "chess-css-codex-guided": "CSS",
        "chess-latex-codex-replication": "LaTeX",
        "latex-chess-engine": "LaTeX", "chess-sql": "SQL",
        "test-superset": "CSS",
        "COBOL-chess": "COBOL", "chess-cobol-cc": "COBOL",
        "chess-revisit-java-toCOBOL-codex": "COBOL (port)",
        "chess-assembly-codex": "Asm",
        "chess-brainfuck": "Brainfuck", "chess-brainfuck-cc": "Brainfuck",
    }

    for ci, c in enumerate(CATEGORY_ORDER):
        engs = by_cat.get(c, [])
        if not engs:
            continue
        if ci > 0:
            L.append("\\midrule")
        for e in engs:
            levels = e.get("capability_levels", {})
            tot = sum(levels.values())
            nm = e["name"]
            dagger = "$^\\dagger$" if nm in ARCHIVED_ENGINES else ""
            row = [
                "\\texttt{" + nm.replace("_", "\\_") + "}" + dagger,
                display_lang.get(nm, "?"),
            ]
            row.extend(LIKERT_TEX[levels.get(cap, 0)] for cap in cap_order)
            row.extend([
                str(e.get("n_steps", 0)),
                str(e.get("n_distinct_capabilities", 0)),
                str(tot),
            ])
            L.append(" & ".join(row) + " \\\\")
    L.append("\\bottomrule")
    L.append("\\end{tabular}%")
    L.append("}")
    L.append("\\end{table*}")
    return "\n".join(L) + "\n"


def main(argv: list[str]) -> None:
    # Import at call time because synthesis.py loads overview.json lazily.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from synthesis import CLASSIFICATION  # type: ignore

    proj_dir = DATA_DIR / "projects"
    # Select engines + special-role (ports/DSL/failure/codesign); skip OOS.
    if argv:
        names = argv
    else:
        overview = json.loads((DATA_DIR / "overview.json").read_text())
        names = [o["name"] for o in overview
                 if CLASSIFICATION.get(o["name"]) in
                    {"engine", "engine-port", "engine-dsl",
                     "engine-failure", "engine-codesign"}]

    engines: list[dict[str, Any]] = []
    for name in sorted(names):
        traj = proj_dir / f"{name}-trajectory.json"
        if not traj.exists():
            continue
        agg = aggregate_engine(name, traj)
        if not agg:
            continue
        engines.append(agg)

    # Persist machine-readable view
    out_json = DATA_DIR / "se_capabilities.json"
    out_json.write_text(
        json.dumps({"engines": engines, "taxonomy": SE_CAPABILITIES},
                   indent=2, default=str),
        encoding="utf-8",
    )
    # Render
    report = render_report(engines)
    out_md = REPORTS_DIR / "SE_CAPABILITIES.md"
    out_md.write_text(report, encoding="utf-8")
    # LaTeX matrix for inclusion in the paper
    tex = render_latex_matrix(engines)
    out_tex = Path(__file__).resolve().parent.parent / "paper" / "tables" / "tab_se_matrix.tex"
    out_tex.parent.mkdir(parents=True, exist_ok=True)
    out_tex.write_text(tex, encoding="utf-8")
    print(f"Wrote {out_json}, {out_md}, and {out_tex}  ({len(engines)} engines)")


if __name__ == "__main__":
    main(sys.argv[1:])
