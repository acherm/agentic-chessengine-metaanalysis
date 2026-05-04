"""Track when each chess-specific feature first appears in a session.

For each engine we walk the agent's Write / Edit / apply_patch tool uses
in chronological order, match the *new content* of every edit against
the 38 CHESS_PATTERNS (common.py), and record the first step at which
each feature was introduced. We also build a cumulative-feature-count
curve per engine.

Outputs, per engine:
  reports/projects/<name>-FEATURES.md   textual Gantt-like view
  data/projects/<name>-features.json    machine-readable map

When invoked with no args we compute everything for three representative
engines (Ruby, COBOL, Brainfuck) and also emit a combined PGFPlots
figure at paper/figures/fig_feature_growth.tex.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import (
    CHESS_PATTERNS,
    CODEX_SESSIONS,
    DATA_DIR,
    FEATURE_GROUPS,
    REPORTS_DIR,
    SANDBOX,
    claude_session_dir,
    iter_jsonl,
    short_quote,
)

# Four representatives spanning the paper's five language categories.
# Ruby (mainstream GP), COBOL (legacy), LaTeX-TeX (domain-specific /
# typesetting-macro), Brainfuck (strictly esoteric).
DEFAULT_ENGINES = [
    "chess-ruby-cc",
    "chess-cobol-cc",
    "chess-latex-codex-replication",   # LaTeX: Codex from-scratch replication
    "chess-brainfuck-cc",
]

CANONICAL_FEATURE_ORDER: list[str] = sum(
    (FEATURE_GROUPS[k] for k in [
        "Rules & protocol", "Board representation", "Search core",
        "Search extensions", "Evaluation", "Strong-engine features",
    ]), []
)

# Group label (for colouring) per feature.
FEATURE_GROUP: dict[str, str] = {}
for g, feats in FEATURE_GROUPS.items():
    for f in feats:
        FEATURE_GROUP[f] = g


# ---------- Event stream ------------------------------------------------

@dataclass
class WriteEvt:
    ts: str
    step: int
    agent: str
    file: str
    content: str
    kind: str  # "Write" / "Edit" / "MultiEdit" / "apply_patch:add" / "apply_patch:upd"


def _flatten_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        out = []
        for b in content:
            if isinstance(b, dict):
                if b.get("type") == "text":
                    out.append(str(b.get("text", "")))
                elif b.get("type") == "thinking":
                    out.append(str(b.get("thinking", "")))
        return " ".join(out)
    return ""


def walk_claude(project_dir: Path) -> list[WriteEvt]:
    """Yield WriteEvt in chronological order across all Claude Code JSONLs."""
    events: list[tuple[str, dict]] = []
    slug = claude_session_dir(project_dir)
    if not slug.exists():
        return []
    for jsonl in slug.rglob("*.jsonl"):
        for obj in iter_jsonl(jsonl):
            ts = obj.get("timestamp", "")
            events.append((ts, obj))
    events.sort(key=lambda x: x[0] or "")
    out: list[WriteEvt] = []
    step = 0
    for ts, obj in events:
        otype = obj.get("type")
        if otype == "user":
            msg = obj.get("message") or {}
            content = msg.get("content")
            text = _flatten_text(content) if isinstance(content, list) else (
                content if isinstance(content, str) else ""
            )
            if not text or text.startswith("<") or text.startswith("Caveat:") or text.startswith("[Request interrupted"):
                continue
            step += 1
        elif otype == "assistant":
            msg = obj.get("message") or {}
            content = msg.get("content")
            if not isinstance(content, list):
                continue
            for block in content:
                if not isinstance(block, dict) or block.get("type") != "tool_use":
                    continue
                name = block.get("name") or ""
                inp = block.get("input") or {}
                if name == "Write":
                    fp = inp.get("file_path") or ""
                    body = inp.get("content") or ""
                    if fp and body:
                        out.append(WriteEvt(ts=ts, step=max(step, 1), agent="claude",
                                            file=fp, content=body, kind="Write"))
                elif name == "Edit":
                    fp = inp.get("file_path") or ""
                    new = inp.get("new_string") or ""
                    if fp and new:
                        out.append(WriteEvt(ts=ts, step=max(step, 1), agent="claude",
                                            file=fp, content=new, kind="Edit"))
                elif name == "MultiEdit":
                    fp = inp.get("file_path") or ""
                    for e in inp.get("edits") or []:
                        new = (e or {}).get("new_string") or ""
                        if fp and new:
                            out.append(WriteEvt(ts=ts, step=max(step, 1), agent="claude",
                                                file=fp, content=new, kind="MultiEdit"))
    return out


RE_APPLY_ADD = re.compile(r"^\*\*\* Add File:\s*(.+)$", re.M)
RE_APPLY_UPD = re.compile(r"^\*\*\* Update File:\s*(.+)$", re.M)

# Heredoc-based file creation inside exec_command.
# Captures: target path, heredoc body. Supports `cat > foo <<'EOF' ... EOF`
# and `tee -a foo <<EOF ... EOF`, with optional single-quoted delimiter.
RE_HEREDOC = re.compile(
    r"(?:cat|tee(?:\s+-a)?|tee\s+-a?)\s*>\s*([^\s<|;&]+)\s*<<\s*[-~]?\s*['\"]?(\w+)['\"]?\s*\n(.*?)\n\2",
    re.S,
)
# `printf 'content' > path` / `echo '...' > path` (simpler, one-line payloads).
RE_PRINTF_REDIR = re.compile(
    r"(?:printf|echo)\s+(?:-[a-zA-Z]+\s+)?(?:'(?P<q1>(?:\\'|[^'])*)'|\"(?P<q2>(?:\\\"|[^\"])*)\")\s*>\s*(?P<path>[^\s<|;&]+)",
)


def extract_heredoc_writes(cmd: str) -> list[tuple[str, str]]:
    """Return [(path, body)] for heredoc-style file creations in a shell cmd."""
    out: list[tuple[str, str]] = []
    for m in RE_HEREDOC.finditer(cmd):
        path, _delim, body = m.group(1), m.group(2), m.group(3)
        out.append((path, body))
    for m in RE_PRINTF_REDIR.finditer(cmd):
        body = m.group("q1") or m.group("q2") or ""
        out.append((m.group("path"), body))
    return out


def walk_codex(project_dir: Path) -> list[WriteEvt]:
    """Yield WriteEvt from Codex rollouts whose cwd matches the project."""
    target = str(project_dir.resolve())
    needle = f'"cwd":"{target}"'.encode()
    needle_s = f'"cwd": "{target}"'.encode()
    if not CODEX_SESSIONS.exists():
        return []
    events: list[tuple[str, dict]] = []
    for jsonl in CODEX_SESSIONS.rglob("*.jsonl"):
        try:
            with jsonl.open("rb") as fh:
                head = fh.read(200_000)
            if needle not in head and needle_s not in head:
                continue
        except Exception:
            continue
        for obj in iter_jsonl(jsonl):
            ts = obj.get("timestamp", "")
            events.append((ts, obj))
    events.sort(key=lambda x: x[0] or "")
    out: list[WriteEvt] = []
    step = 0
    for ts, obj in events:
        otype = obj.get("type")
        payload = obj.get("payload") or {}
        if otype == "event_msg" and payload.get("type") == "user_message":
            m = payload.get("message", "")
            if m and not m.startswith("<environment_context>"):
                step += 1
        elif otype == "response_item" and payload.get("type") == "function_call":
            name = payload.get("name", "")
            try:
                args = json.loads(payload.get("arguments") or "{}")
            except Exception:
                args = {}
            # ---- exec_command / shell: file creations via heredoc ----
            if name in ("exec_command", "shell"):
                cmd = args.get("cmd") or args.get("command") or ""
                if isinstance(cmd, list):
                    cmd = " ".join(cmd)
                cmd = str(cmd)
                for path, body in extract_heredoc_writes(cmd):
                    if body:
                        out.append(WriteEvt(
                            ts=ts, step=max(step, 1), agent="codex",
                            file=path, content=body, kind="heredoc",
                        ))
                continue
            if name != "apply_patch":
                continue
            patch = args.get("input") or args.get("patch") or ""
            if not patch:
                continue
            # Split the patch into per-file segments and collect added lines.
            files: list[tuple[str, str, list[str]]] = []  # (kind, file, added_lines)
            cur_file = None
            cur_kind = None
            cur_add: list[str] = []
            for line in patch.splitlines():
                am = RE_APPLY_ADD.match(line)
                um = RE_APPLY_UPD.match(line)
                if am:
                    if cur_file:
                        files.append((cur_kind, cur_file, cur_add))
                    cur_kind, cur_file, cur_add = "apply_patch:add", am.group(1).strip(), []
                elif um:
                    if cur_file:
                        files.append((cur_kind, cur_file, cur_add))
                    cur_kind, cur_file, cur_add = "apply_patch:upd", um.group(1).strip(), []
                elif line.startswith("+") and not line.startswith("+++"):
                    cur_add.append(line[1:])
            if cur_file:
                files.append((cur_kind, cur_file, cur_add))
            for kind, f, adds in files:
                body = "\n".join(adds)
                if body:
                    out.append(WriteEvt(ts=ts, step=max(step, 1), agent="codex",
                                        file=f, content=body, kind=kind))
    return out


def walk_exported_md(project_dir: Path) -> list[WriteEvt]:
    """Parse a Claude Code terminal-dump export at
    `data/projects/claudecode/<project-name>.md` into WriteEvt objects.

    Format recognized:
      - User prompts: consecutive lines wrapped in ``│ ... │`` boxes.
        Each contiguous box-block counts as one human prompt; step
        counter increments.
      - Tool calls: lines matching ``^⏺ (Update|Write|MultiEdit)\\(path\\)``,
        followed by a diff block whose lines look like ``NN +text`` or
        ``NN -text``; we collect the `+` lines as the ``new content''.

    Timestamps are synthetic (step-indexed) since the export strips them.
    """
    md = (project_dir.parent / "chess-meta-analysis" / "data" / "projects"
          / "claudecode" / f"{project_dir.name}.md")
    if not md.exists():
        return []
    out: list[WriteEvt] = []
    step = 0
    in_box_block = False
    current_tool: tuple[str, str] | None = None  # (kind, file)
    current_body: list[str] = []

    TOOL_RE = re.compile(r"^⏺\s+(Update|Write|MultiEdit)\(([^)]+)\)")
    DIFF_LINE_RE = re.compile(r"^\s*\d+\s+\+(.*)$")

    def flush_tool():
        nonlocal current_tool, current_body, step
        if current_tool and current_body:
            kind, file = current_tool
            body = "\n".join(current_body)
            if body.strip():
                out.append(WriteEvt(
                    ts=f"step-{step:04d}", step=max(step, 1), agent="claude-md",
                    file=file, content=body, kind=kind.lower(),
                ))
        current_tool = None
        current_body = []

    with md.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            # Box-block detection for user prompts
            stripped = line.lstrip()
            is_box_line = stripped.startswith("│") and stripped.rstrip().endswith("│")
            if is_box_line:
                if not in_box_block:
                    in_box_block = True
                    # A new box-block starts — flush any open tool and
                    # advance the step counter. The `Welcome back!` box
                    # and other UI chrome also trigger; the extra step
                    # increment is harmless for feature-trajectory use.
                    flush_tool()
                    step += 1
                continue
            elif in_box_block and not stripped:
                # blank separator — leaves the box block
                in_box_block = False
                continue
            else:
                in_box_block = False

            # Tool invocation detector
            m = TOOL_RE.match(line)
            if m:
                flush_tool()
                kind, file = m.group(1), m.group(2).strip()
                current_tool = (kind, file)
                current_body = []
                continue

            # Continuation inside a tool invocation: capture `+` additions.
            if current_tool is not None:
                dm = DIFF_LINE_RE.match(line)
                if dm:
                    current_body.append(dm.group(1))
                    continue
                # End of diff block: next "⏺" restart OR a blank line
                # after additions. Keep the tool open a bit longer in
                # case the diff is multi-block; flush on next tool line.

    flush_tool()
    return out


def collect_writes(project_dir: Path) -> list[WriteEvt]:
    evts = walk_claude(project_dir) + walk_codex(project_dir) + walk_exported_md(project_dir)
    evts.sort(key=lambda e: (e.ts or ""))
    return evts


# ---------- Feature first-appearance ------------------------------------

@dataclass
class Appearance:
    feature: str
    step: int
    ts: str
    file: str
    kind: str
    snippet: str


def scan_features(evts: list[WriteEvt]) -> tuple[dict[str, Appearance], list[int]]:
    """Return (feature_name -> first Appearance, cumulative count per step)."""
    first: dict[str, Appearance] = {}
    per_step_count: Counter = Counter()
    max_step = 0
    for e in evts:
        max_step = max(max_step, e.step)
        for feat, pat in CHESS_PATTERNS.items():
            if feat in first:
                continue
            m = pat.search(e.content)
            if not m:
                continue
            s = max(0, m.start() - 40)
            end = min(len(e.content), m.end() + 40)
            snippet = short_quote(e.content[s:end].replace("\n", " "), 120)
            first[feat] = Appearance(
                feature=feat, step=e.step, ts=e.ts, file=e.file,
                kind=e.kind, snippet=snippet,
            )
            per_step_count[e.step] += 1
    cumulative = []
    running = 0
    for step in range(1, max_step + 1):
        running += per_step_count.get(step, 0)
        cumulative.append(running)
    return first, cumulative


# ---------- Markdown rendering ------------------------------------------

def render_markdown(name: str, first: dict[str, Appearance], cumulative: list[int], n_writes: int) -> str:
    lines: list[str] = []
    lines.append(f"# {name} — feature-introduction trajectory")
    lines.append("")
    lines.append(f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_")
    lines.append("")
    lines.append(f"Source: {n_writes} Write/Edit/apply_patch events scanned against the 38-pattern chess-feature catalog (see `scripts/common.py::CHESS_PATTERNS`).")
    lines.append("")
    lines.append(f"- **Distinct features detected**: {len(first)} / {len(CHESS_PATTERNS)}")
    lines.append(f"- **Total session steps**: {len(cumulative)}")
    lines.append(f"- **Feature introduction density**: {len(first)} features in {len(cumulative)} steps ≈ {len(first)/max(1,len(cumulative)):.2f} features/step")
    lines.append("")
    lines.append("## Feature appearance order (earliest first)")
    lines.append("")
    lines.append("| # | Step | Feature | Group | File | Kind |")
    lines.append("|---:|---:|---|---|---|---|")
    ordered = sorted(first.values(), key=lambda a: (a.step, a.feature))
    for i, a in enumerate(ordered, 1):
        grp = FEATURE_GROUP.get(a.feature, "—")
        file_short = a.file
        if "/" in file_short:
            file_short = "…/" + file_short.rsplit("/", 1)[1]
        lines.append(f"| {i} | {a.step} | {a.feature} | {grp} | `{file_short}` | {a.kind} |")
    lines.append("")
    lines.append("## Per-group introduction timeline")
    lines.append("")
    for g, feats in FEATURE_GROUPS.items():
        present = [f for f in feats if f in first]
        if not present:
            continue
        lines.append(f"### {g}")
        lines.append("")
        lines.append("| Feature | Step | File |")
        lines.append("|---|---:|---|")
        present.sort(key=lambda f: first[f].step)
        for f in present:
            a = first[f]
            file_short = a.file
            if "/" in file_short:
                file_short = "…/" + file_short.rsplit("/", 1)[1]
            lines.append(f"| {a.feature} | {a.step} | `{file_short}` |")
        lines.append("")
    lines.append("## Cumulative feature count per step")
    lines.append("")
    lines.append("Each row: after step $k$, the agent had touched a cumulative total of $n(k)$ distinct features in newly-written content.")
    lines.append("")
    lines.append("```")
    chars = []
    for k, n in enumerate(cumulative, start=1):
        chars.append(f"step {k:>3}: {n:>2}  " + "█" * n)
    lines.append("\n".join(chars))
    lines.append("```")
    return "\n".join(lines) + "\n"


# ---------- PGFPlots figure ---------------------------------------------

CAT_HINT = {
    "chess-ruby-cc":       ("Ruby (mainstream)",      "blue!70!black",  "*"),
    "chess-java-cc":       ("Java (mainstream)",      "cyan!60!black",  "o"),
    "chess-cobol-cc":      ("COBOL (legacy)",         "red!70!black",   "square*"),
    "chess-latex-codex-replication": ("LaTeX (Codex, scratch)", "purple!70!black", "triangle*"),
    "latex-chess-engine":  ("LaTeX/TeX (CC, incremental)", "violet!70!black", "pentagon*"),
    "chess-brainfuck-cc":  ("Brainfuck (esoteric)",   "green!45!black", "diamond*"),
}

# Category colour used for per-feature dots in the Gantt figure.
GROUP_COLOR = {
    "Rules & protocol":        "teal",
    "Board representation":    "orange!80!black",
    "Search core":             "blue!70!black",
    "Search extensions":       "red!70!black",
    "Evaluation":              "purple!70!black",
    "Strong-engine features":  "olive!70!black",
}

# Display-shortened feature names for the Y-axis labels.
SHORT_NAME = {
    "FEN parsing": "FEN",
    "UCI protocol": "UCI",
    "PGN": "PGN",
    "Castling": "castling",
    "En passant": "en passant",
    "Promotion": "promotion",
    "Check/Checkmate": "check/mate",
    "Board: 0x88": "0x88",
    "Board: bitboard": "bitboard",
    "Board: magic bitboards": "magic BB",
    "Board: mailbox 8x8": "mailbox",
    "Board: mailbox 10x12": "10x12 mailbox",
    "Minimax/Negamax": "negamax",
    "Alpha-beta": r"$\alpha\beta$",
    "Iterative deepening": "iter-deep",
    "Quiescence": "quiescence",
    "Transposition table": "TT",
    "Zobrist hashing": "Zobrist",
    "Perft": "perft",
    "Move ordering (MVV-LVA)": "MVV-LVA",
    "Killer moves": "killers",
    "History heuristic": "history",
    "Principal-variation (PV)": "PV",
    "Null-move pruning": "null-move",
    "Late-move reduction (LMR)": "LMR",
    "Late-move pruning (LMP)": "LMP",
    "Aspiration windows": "aspiration",
    "Futility pruning": "futility",
    "Razoring": "razoring",
    "Material counting": "material",
    "Evaluation/PST": "PST",
    "Tapered evaluation": "tapered",
    "King safety": "king safety",
    "Pawn structure": "pawn struct.",
    "Mobility": "mobility",
    "Opening book": "book",
    "Endgame tables": "tablebase",
    "Time management": "time mgmt",
    "NNUE/neural eval": "NNUE",
}


def render_combined_figure(records: list[tuple[str, list[int]]]) -> str:
    """Emit PGFPlots code for a feature-growth curve per engine (4 engines)."""
    L: list[str] = []
    L.append("% Auto-generated by scripts/feature_trajectory.py --- do not edit.")
    L.append(r"\begin{figure}[ht]")
    L.append(r"\centering")
    L.append(r"\begin{tikzpicture}")
    L.append(r"\begin{axis}[")
    L.append(r"  width=0.95\linewidth, height=0.5\linewidth,")
    L.append(r"  xlabel={Session progress (step / total steps)},")
    L.append(r"  ylabel={Cumulative distinct features introduced},")
    L.append(r"  xmin=0, xmax=1.02,")
    L.append(r"  ymin=0, ymax=36,")
    L.append(r"  grid=both, grid style={gray!20},")
    L.append(r"  legend style={font=\footnotesize, at={(0.98,0.02)}, anchor=south east, draw=none, fill=white, fill opacity=0.8, text opacity=1},")
    L.append(r"  tick label style={font=\footnotesize},")
    L.append(r"  label style={font=\footnotesize},")
    L.append(r"]")
    for name, cumulative in records:
        label, color, mark = CAT_HINT.get(name, (name, "black", "*"))
        total = len(cumulative) or 1
        coords = []
        for step, n in enumerate(cumulative, start=1):
            coords.append(f"({step/total:.3f},{n})")
        L.append(rf"  \addplot[color={color}, mark={mark}, mark options={{fill={color}}}, thick] coordinates {{ {' '.join(coords)} }};")
        L.append(rf"  \addlegendentry{{{label}}}")
    L.append(r"\end{axis}")
    L.append(r"\end{tikzpicture}")
    L.append(r"\caption{Cumulative distinct chess-engine features introduced into the repository over normalized session progress, for four representative engines --- one per language category (mainstream general-purpose, legacy, domain-specific markup, esoteric). Feature counts are first-appearances under the 38-pattern catalog of \Cref{sec:rq2}, matched against the \emph{new} content of every Write / Edit / apply\_patch event. The four trajectories take qualitatively different shapes, discussed in \Cref{sec:rq2:trajectory}.}")
    L.append(r"\label{fig:feature-growth}")
    L.append(r"\end{figure}")
    return "\n".join(L) + "\n"


def render_gantt_subplot(name: str, first: dict[str, Appearance], n_steps: int) -> str:
    """Emit a TikZ/PGFPlots sub-axis for one engine's feature-Gantt.

    Y axis: features detected in this engine, grouped top-to-bottom in the
    canonical order (rules & protocol → board representation → search core
    → search extensions → evaluation → strong-engine features). Each feature
    gets a dot at its first-appearance step and a thin horizontal bar from
    that step to the end of the session. Colour = feature group.
    """
    present: list[tuple[str, str, int]] = []  # (feature, group, first_step)
    for f in CANONICAL_FEATURE_ORDER:
        if f in first:
            present.append((f, FEATURE_GROUP[f], first[f].step))
    if not present:
        return ""
    # Assign y-positions (top row = first feature); add small gap between groups.
    y_pos: dict[str, float] = {}
    y = 0.5
    prev_group = None
    for feat, group, _ in present:
        if prev_group is not None and group != prev_group:
            y += 0.8  # gap between groups
        y += 1
        y_pos[feat] = y
        prev_group = group
    total_y = y + 1
    # Label + tick list for the Y axis (using LaTeX-safe short names).
    yticks = []
    ylabels = []
    for feat, _, _ in present:
        ypos = y_pos[feat]
        label = SHORT_NAME.get(feat, feat)
        yticks.append(f"{ypos}")
        ylabels.append(label)

    # Group features by colour for single-legend addplots.
    by_group: dict[str, list[tuple[float, int]]] = {}
    for feat, group, step in present:
        by_group.setdefault(group, []).append((y_pos[feat], step))
    # Bars (first_step → session end) per group, thin lines for continuity.

    lines: list[str] = []
    title_label = CAT_HINT.get(name, (name, "", ""))[0]
    lines.append(r"\begin{tikzpicture}")
    lines.append(r"\begin{axis}[")
    lines.append(r"  width=\linewidth, height=10cm,")
    lines.append(rf"  title={{\footnotesize {title_label}}},")
    lines.append(r"  title style={yshift=-2pt},")
    lines.append(r"  xlabel={\footnotesize session step (absolute)},")
    lines.append(rf"  xmin=0, xmax={n_steps + 1},")
    lines.append(rf"  ymin=0, ymax={total_y:.1f},")
    lines.append(r"  ytick={" + ",".join(yticks) + r"},")
    lines.append(r"  yticklabels={" + ",".join(ylabels) + r"},")
    lines.append(r"  tick label style={font=\tiny},")
    lines.append(r"  label style={font=\footnotesize},")
    lines.append(r"  grid=both, grid style={gray!15, very thin},")
    lines.append(r"  axis y line=left, axis x line=bottom,")
    lines.append(r"  enlarge y limits=false,")
    lines.append(r"  every tick/.style={thin, gray!40},")
    lines.append(r"]")
    # Draw a thin horizontal bar for each feature (first_step → end).
    for feat, group, step in present:
        color = GROUP_COLOR.get(group, "black")
        ypos = y_pos[feat]
        lines.append(rf"  \addplot[color={color}, opacity=0.35, line width=1.5pt, forget plot] coordinates {{ ({step},{ypos}) ({n_steps},{ypos}) }};")
    # Dots per group (so a legend can show one entry per group later).
    seen_groups: set[str] = set()
    for group in FEATURE_GROUPS:
        pts = by_group.get(group) or []
        if not pts:
            continue
        color = GROUP_COLOR.get(group, "black")
        coords = " ".join(f"({step},{y:.2f})" for y, step in pts)
        lines.append(rf"  \addplot+[only marks, mark=*, mark size=2pt, color={color}, mark options={{fill={color}}}, forget plot] coordinates {{ {coords} }};")
        seen_groups.add(group)
    lines.append(r"\end{axis}")
    lines.append(r"\end{tikzpicture}")
    return "\n".join(lines) + "\n"


def render_feature_gantt_figure(engines_data: list[tuple[str, dict[str, Appearance], int]]) -> str:
    """4-panel Gantt: one engine per subfigure, shared colour scheme by group."""
    L: list[str] = []
    L.append("% Auto-generated by scripts/feature_trajectory.py --- do not edit.")
    L.append(r"\begin{figure*}[ht]")
    L.append(r"\centering")
    # Legend (plain text with small coloured squares).
    legend_items = []
    for g in FEATURE_GROUPS:
        color = GROUP_COLOR[g]
        g_tex = g.replace("&", r"\&")
        legend_items.append(
            rf"\tikz[baseline=-0.6ex]\fill[{color}, rounded corners=0.5pt] (0,0) rectangle (0.5em,0.5em); \footnotesize {g_tex}"
        )
    L.append(r"{\footnotesize " + r" \quad ".join(legend_items) + r"}\par\vspace{0.6em}")
    L.append("")
    # 2x2 grid of subfigures (4 engines, filled exactly).
    COLS = 2
    for i, (name, first, n_steps) in enumerate(engines_data):
        sub = render_gantt_subplot(name, first, n_steps)
        L.append(r"\begin{minipage}[t]{0.49\textwidth}")
        L.append(sub)
        L.append(r"\end{minipage}")
        at_row_end = (i % COLS) == (COLS - 1)
        at_last = i == len(engines_data) - 1
        if at_row_end or at_last:
            L.append(r"")
            L.append(r"\vspace{0.6em}")
        else:
            L.append(r"\hfill")
    L.append(r"\caption{Feature-introduction Gantt for four representative engines covering the paper's main language categories (the specialized / academic category is omitted because its sessions are too short to support a trajectory view; Java is omitted because only its spec-extraction follow-up session survives rather than the authoring session; the canonical TeXCCChess LaTeX engine is omitted for the same reason). For each engine, each row is a chess-engine feature detected in the repository (rows grouped by category and colour); a dot marks the step at which the feature first appeared in newly-written content, and a thin horizontal bar extends from that step to the end of the session as a ``feature lifetime'' indicator. Ruby dumps nearly all features in a single early \emph{plan-implementation} step; COBOL accretes features gradually across 30$+$ steps with no single dominant burst; LaTeX front-loads rules and basic search and then stabilises; Brainfuck exhibits long stretches of null activity before a late burst of search features.}")
    L.append(r"\label{fig:feature-gantt}")
    L.append(r"\end{figure*}")
    return "\n".join(L) + "\n"
    """Emit PGFPlots code for a feature-growth curve per engine."""
    L: list[str] = []
    L.append("% Auto-generated by scripts/feature_trajectory.py --- do not edit.")
    L.append(r"\begin{figure}[ht]")
    L.append(r"\centering")
    L.append(r"\begin{tikzpicture}")
    L.append(r"\begin{axis}[")
    L.append(r"  width=0.95\linewidth, height=0.5\linewidth,")
    L.append(r"  xlabel={Session progress (step / total steps)},")
    L.append(r"  ylabel={Cumulative distinct features introduced},")
    L.append(r"  xmin=0, xmax=1.02,")
    L.append(r"  ymin=0, ymax=36,")
    L.append(r"  grid=both, grid style={gray!20},")
    L.append(r"  legend style={font=\footnotesize, at={(0.98,0.02)}, anchor=south east, draw=none, fill=white, fill opacity=0.8, text opacity=1},")
    L.append(r"  tick label style={font=\footnotesize},")
    L.append(r"  label style={font=\footnotesize},")
    L.append(r"]")
    for name, cumulative in records:
        label, color, mark = CAT_HINT.get(name, (name, "black", "*"))
        total = len(cumulative) or 1
        coords = []
        for step, n in enumerate(cumulative, start=1):
            coords.append(f"({step/total:.3f},{n})")
        L.append(rf"  \addplot[color={color}, mark={mark}, mark options={{fill={color}}}, thick] coordinates {{ {' '.join(coords)} }};")
        L.append(rf"  \addlegendentry{{{label}}}")
    L.append(r"\end{axis}")
    L.append(r"\end{tikzpicture}")
    L.append(r"\caption{Cumulative distinct chess-engine features introduced into the repository over normalized session progress, for three representative engines --- one mainstream general-purpose (Ruby), one legacy (COBOL), one esoteric (Brainfuck). Feature counts are first-appearances under the 38-pattern catalog of \Cref{sec:rq2}, matched against the \emph{new} content of every Write / Edit / apply\_patch event. Mainstream and legacy engines front-load their feature set (most features introduced in the first third of the session); the esoteric engine accretes features more slowly and plateaus lower. The three curves illustrate how feature-introduction cadence, not just final feature count, varies by language category.}")
    L.append(r"\label{fig:feature-growth}")
    L.append(r"\end{figure}")
    return "\n".join(L) + "\n"


# ---------- Driver ------------------------------------------------------

def process_one(name: str) -> tuple[dict[str, Appearance], list[int], int]:
    project_dir = SANDBOX / name
    evts = collect_writes(project_dir)
    first, cumulative = scan_features(evts)
    return first, cumulative, len(evts)


def save_outputs(name: str, first: dict[str, Appearance], cumulative: list[int], n_writes: int) -> None:
    md_dir = REPORTS_DIR / "projects"
    md_dir.mkdir(parents=True, exist_ok=True)
    (md_dir / f"{name}-FEATURES.md").write_text(
        render_markdown(name, first, cumulative, n_writes), encoding="utf-8"
    )
    jdir = DATA_DIR / "projects"
    jdir.mkdir(parents=True, exist_ok=True)
    (jdir / f"{name}-features.json").write_text(
        json.dumps(
            {
                "project": name,
                "n_write_events": n_writes,
                "cumulative": cumulative,
                "first_appearances": {
                    k: {"step": v.step, "ts": v.ts, "file": v.file, "kind": v.kind, "snippet": v.snippet}
                    for k, v in first.items()
                },
            },
            indent=2, default=str,
        ),
        encoding="utf-8",
    )


def main(argv: list[str]) -> None:
    targets = argv or DEFAULT_ENGINES
    records: list[tuple[str, list[int]]] = []
    gantt_data: list[tuple[str, dict[str, Appearance], int]] = []
    for name in targets:
        first, cumulative, n_writes = process_one(name)
        save_outputs(name, first, cumulative, n_writes)
        print(f"→ {name}: {len(first)} features detected, {n_writes} write events, {len(cumulative)} steps")
        records.append((name, cumulative))
        gantt_data.append((name, first, len(cumulative)))
    # Combined figures when we produced the default set.
    if not argv or set(argv) == set(DEFAULT_ENGINES):
        fig_dir = REPO_FIG()
        fig_dir.mkdir(parents=True, exist_ok=True)
        (fig_dir / "fig_feature_growth.tex").write_text(
            render_combined_figure(records), encoding="utf-8"
        )
        print(f"wrote {fig_dir / 'fig_feature_growth.tex'}")
        (fig_dir / "fig_feature_gantt.tex").write_text(
            render_feature_gantt_figure(gantt_data), encoding="utf-8"
        )
        print(f"wrote {fig_dir / 'fig_feature_gantt.tex'}")


def REPO_FIG() -> Path:
    return Path(__file__).resolve().parent.parent / "paper" / "figures"


if __name__ == "__main__":
    main(sys.argv[1:])
