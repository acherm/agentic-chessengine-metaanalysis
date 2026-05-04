"""Emit a step-wise trajectory per engine, summarizing what the agent did
between consecutive human prompts.

For each engine we produce reports/projects/<name>-TRAJECTORY.md with:
  - a step-by-step table (one row per human prompt + the work that followed)
  - automatic phase grouping (adjacent steps with similar task class)
  - stagnation detection (consecutive debug steps without new-feature progress)
  - cumulative Elo-claim evolution
  - a task-class distribution (% of tokens spent on feature / debug / eval / ...)

The segmentation unit is a *step*: a human prompt and the stretch of
agent work (tool uses, file writes, bash commands) that follows it until
the next human prompt (or end of session).

Usage:
  python3 scripts/trajectory.py               # all in-scope engines
  python3 scripts/trajectory.py chess-ruby-cc # one
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import (
    CODEX_SESSIONS,
    DATA_DIR,
    REPORTS_DIR,
    claude_session_dir,
    discover_projects,
    iter_jsonl,
    safe_int,
    short_quote,
)

# ---------- Intent + task-class classification --------------------------

INTENT_PATTERNS = [
    ("FeatureRequest", re.compile(r"\b(add|implement|build|create|write|develop|introduce|make)\b", re.I)),
    ("BugFixRequest", re.compile(r"\b(fix|bug|broken|doesn'?t work|fails?|failure|error|issue|regression|incorrect|wrong|illegal|crash|segfault)\b", re.I)),
    ("RefactorRequest", re.compile(r"\b(refactor|clean ?up|simplify|restructure|rename|split|extract|move.+to)\b", re.I)),
    ("TestRequest", re.compile(r"\btest(s|ing)?\b|perft|unit[- ]test|smoke[- ]?test", re.I)),
    ("Documentation", re.compile(r"\bdocument|readme|\bdocs?\b|explain|describe", re.I)),
    ("ToolingBuild", re.compile(r"\b(build|compile|makefile|cmake|cargo|gradle|install|setup|configure|toolchain)\b", re.I)),
    ("Constraint", re.compile(r"\b(must|cannot|do not|don'?t|only|without|restrict|forbid|avoid|no )\b", re.I)),
    ("Question", re.compile(r"^\s*(how|why|what|where|when|which|who|can you|could you|do you)\b", re.I)),
    ("Scenario", re.compile(r"\b(play|game|position|opening|endgame|mate in|perft|match|tournament|gauntlet|stockfish)\b", re.I)),
    ("Improve", re.compile(r"\b(improve|better|stronger|faster|tune|optim)", re.I)),
    ("Steer", re.compile(r"^\s*(go|continue|proceed|yes|ok|okay|next|keep going|let'?s go)\b", re.I)),
    ("Meta", re.compile(r"\b(status|summary|progress|what'?s next|where are we)\b", re.I)),
]

# Bash command kinds --- rough but discriminative.
BASH_KIND_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("build", re.compile(r"\b(cargo\s+build|cargo\s+check|make\b|cmake|gradle|mvn|dune\s+build|lake\s+build|tsc\b|rustc\b|gcc\b|g\+\+|clang)\b", re.I)),
    ("test", re.compile(r"\b(cargo\s+test|pytest|npm\s+test|rake\s+test|dune\s+test|lake\s+test|go\s+test|mocha|jest|rspec)\b", re.I)),
    ("perft", re.compile(r"\bperft\b", re.I)),
    ("gauntlet", re.compile(r"\b(cutechess-cli|estimate_elo|elo_test|run_matches|run_gauntlet|run_swiss|run_tournament)\b", re.I)),
    ("uci_run", re.compile(r"echo.*uci|printf.*uci|\bposition\b.*\bstartpos\b|\bbestmove\b", re.I)),
    ("stockfish", re.compile(r"\bstockfish\b", re.I)),
    ("git", re.compile(r"^\s*git\s+", re.I)),
    ("package", re.compile(r"\b(cargo\s+add|cargo\s+install|pip\s+install|gem\s+install|npm\s+install|apt\s+install|brew\s+install|opam\s+install|mojo\s+package)\b", re.I)),
    ("inspect", re.compile(r"^\s*(ls|cat|head|tail|grep|rg|find|wc|tree|file|pwd)\b", re.I)),
]


def classify_intent(text: str) -> list[str]:
    hits = []
    for name, pat in INTENT_PATTERNS:
        if pat.search(text):
            hits.append(name)
    return hits or ["Other"]


def classify_bash(cmd: str) -> str:
    for kind, pat in BASH_KIND_PATTERNS:
        if pat.search(cmd):
            return kind
    return "other"


# ---------- Event model -------------------------------------------------

@dataclass
class Event:
    """Atomic event in chronological order inside a session."""
    ts: str
    kind: str         # "user_prompt" | "tool_use" | "assistant_text"
    agent: str        # "claude" | "codex"
    # kind-specific payload
    text: str = ""    # for user_prompt / assistant_text
    tool_name: str = ""
    tool_input: dict = field(default_factory=dict)
    # Usage (present on assistant messages)
    tokens: dict[str, int] = field(default_factory=dict)
    model: str = ""


@dataclass
class Step:
    """A human prompt + the agent work that follows until the next prompt."""
    index: int
    ts_start: str
    ts_end: str
    duration_s: float | None
    user_prompt: str
    user_intent: list[str]
    agent: str
    n_events: int = 0
    tool_counts: Counter = field(default_factory=Counter)
    files_written: list[str] = field(default_factory=list)
    files_edited: list[str] = field(default_factory=list)
    files_read: list[str] = field(default_factory=list)
    bash_commands: list[str] = field(default_factory=list)
    bash_kinds: Counter = field(default_factory=Counter)
    tokens: dict[str, int] = field(default_factory=lambda: {
        "input": 0, "output": 0, "cache_read": 0, "cache_creation": 0,
        "reasoning": 0,
    })
    elo_mentions: list[int] = field(default_factory=list)
    task_class: str = ""
    stagnation: bool = False


# ---------- Source walkers ---------------------------------------------

RE_ELO = re.compile(r"(?:≈|~|approximately|about|roughly|final|estimated)?\s*(\d{3,4})\s*(?:Elo|ELO|elo)\b")


def _flatten_content(content) -> str:
    if isinstance(content, str):
        return content
    parts: list[str] = []
    if isinstance(content, list):
        for b in content:
            if isinstance(b, dict):
                if b.get("type") == "text":
                    parts.append(str(b.get("text", "")))
                elif b.get("type") == "thinking":
                    parts.append(str(b.get("thinking", "")))
    return " ".join(parts)


def walk_claude_session(jsonl: Path) -> list[Event]:
    """Extract chronological events from a single Claude Code JSONL."""
    events: list[Event] = []
    for obj in iter_jsonl(jsonl):
        otype = obj.get("type")
        ts = obj.get("timestamp", "")
        if otype == "user":
            msg = obj.get("message") or {}
            content = msg.get("content")
            text = _flatten_content(content) if isinstance(content, list) else (
                content if isinstance(content, str) else ""
            )
            # Filter synthetic / tool-result / local-stdout wrappers
            if not text:
                continue
            if text.startswith("<"):
                continue
            if text.startswith("Caveat:") or text.startswith("[Request interrupted"):
                continue
            # Discard short system-ish echoes that leak from tool-search or
            # approval UIs. Keep genuine short human prompts (``go'',
            # ``continue'', ``yes'') -- these are specifically in the allow-list.
            SHORT_ALLOW = {"go", "continue", "yes", "ok", "okay", "next", "proceed",
                           "status?", "status", "no", "stop"}
            stripped = text.strip().lower().rstrip(".!?")
            if stripped in {"tool loaded"}:
                continue
            events.append(Event(ts=ts, kind="user_prompt", agent="claude", text=text))
        elif otype == "assistant":
            msg = obj.get("message") or {}
            usage = msg.get("usage") or {}
            tokens = {
                "input": safe_int(usage.get("input_tokens")),
                "output": safe_int(usage.get("output_tokens")),
                "cache_read": safe_int(usage.get("cache_read_input_tokens")),
                "cache_creation": safe_int(usage.get("cache_creation_input_tokens")),
                "reasoning": 0,
            }
            model = msg.get("model", "")
            content = msg.get("content")
            text = _flatten_content(content)
            if text:
                events.append(Event(ts=ts, kind="assistant_text", agent="claude",
                                    text=text, tokens=tokens, model=model))
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        events.append(Event(
                            ts=ts, kind="tool_use", agent="claude",
                            tool_name=block.get("name", "unknown"),
                            tool_input=block.get("input") or {},
                        ))
    return events


def walk_codex_session(jsonl: Path, project_path: str) -> list[Event]:
    """Extract chronological events from a Codex rollout filtered to a project.

    Returns [] if the session's cwd does not match the project path.
    """
    # Cheap cwd filter
    try:
        with jsonl.open("rb") as fh:
            head = fh.read(200_000)
        needle = f'"cwd":"{project_path}"'.encode()
        needle_s = f'"cwd": "{project_path}"'.encode()
        if needle not in head and needle_s not in head:
            return []
    except Exception:
        return []
    events: list[Event] = []
    current_model = ""
    for obj in iter_jsonl(jsonl):
        otype = obj.get("type")
        ts = obj.get("timestamp", "")
        payload = obj.get("payload") or {}
        if otype == "turn_context":
            current_model = payload.get("model", current_model)
        elif otype == "event_msg":
            ptype = payload.get("type")
            if ptype == "user_message":
                text = payload.get("message", "")
                if text and not text.startswith("<environment_context>"):
                    events.append(Event(ts=ts, kind="user_prompt", agent="codex", text=text))
            elif ptype == "agent_message":
                text = payload.get("message", "")
                if text:
                    events.append(Event(ts=ts, kind="assistant_text", agent="codex",
                                        text=text, model=current_model))
            elif ptype == "token_count":
                info = payload.get("info") or {}
                last = (info.get("last_token_usage") if isinstance(info, dict) else None) or {}
                if last:
                    # Attach as synthetic event carrying tokens for the preceding turn
                    events.append(Event(
                        ts=ts, kind="assistant_text", agent="codex", text="",
                        tokens={
                            "input": safe_int(last.get("input_tokens")),
                            "output": safe_int(last.get("output_tokens")),
                            "cache_read": safe_int(last.get("cached_input_tokens")),
                            "cache_creation": 0,
                            "reasoning": safe_int(last.get("reasoning_output_tokens")),
                        },
                        model=current_model,
                    ))
        elif otype == "response_item":
            ptype = payload.get("type")
            if ptype == "function_call":
                name = payload.get("name", "") or ""
                try:
                    args = json.loads(payload.get("arguments") or "{}")
                except Exception:
                    args = {}
                # Normalize: Codex's main shell tool is `shell` with
                # {"command": [...]} (newer rollouts) or `exec_command`
                # with {"cmd": "..."} (older rollouts). Both must be
                # routed to a Bash event so downstream bash-kind
                # classification picks them up.
                if name in ("shell", "exec_command"):
                    cmd_raw = args.get("command") or args.get("cmd")
                    if isinstance(cmd_raw, list):
                        cmd = " ".join(cmd_raw)
                    else:
                        cmd = str(cmd_raw or "")
                    events.append(Event(
                        ts=ts, kind="tool_use", agent="codex",
                        tool_name="Bash", tool_input={"command": cmd},
                    ))
                elif name == "apply_patch":
                    patch = args.get("input") or args.get("patch") or ""
                    # Extract file paths from patch headers like "*** Add File: foo/bar.py"
                    files_add = re.findall(r"^\*\*\* Add File:\s*(.+)$", patch, re.M)
                    files_upd = re.findall(r"^\*\*\* Update File:\s*(.+)$", patch, re.M)
                    files_del = re.findall(r"^\*\*\* Delete File:\s*(.+)$", patch, re.M)
                    for f in files_add:
                        events.append(Event(ts=ts, kind="tool_use", agent="codex",
                                            tool_name="Write",
                                            tool_input={"file_path": f.strip()}))
                    for f in files_upd:
                        events.append(Event(ts=ts, kind="tool_use", agent="codex",
                                            tool_name="Edit",
                                            tool_input={"file_path": f.strip()}))
                    for f in files_del:
                        events.append(Event(ts=ts, kind="tool_use", agent="codex",
                                            tool_name="Delete",
                                            tool_input={"file_path": f.strip()}))
                else:
                    events.append(Event(ts=ts, kind="tool_use", agent="codex",
                                        tool_name=name, tool_input=args))
            elif ptype == "local_shell_call":
                # Codex variant with shell args
                action = payload.get("action") or {}
                cmd_raw = action.get("command")
                if isinstance(cmd_raw, list):
                    cmd = " ".join(cmd_raw)
                else:
                    cmd = str(cmd_raw or "")
                events.append(Event(ts=ts, kind="tool_use", agent="codex",
                                    tool_name="Bash", tool_input={"command": cmd}))
            elif ptype == "custom_tool_call":
                # Older Codex rollouts serialise apply_patch as a custom
                # tool call with the unified-diff content under
                # payload.input rather than as a function_call with JSON
                # arguments. Extract file writes/edits/deletes the same way.
                name = payload.get("name", "") or ""
                if name == "apply_patch":
                    patch = payload.get("input") or ""
                    files_add = re.findall(r"^\*\*\* Add File:\s*(.+)$", patch, re.M)
                    files_upd = re.findall(r"^\*\*\* Update File:\s*(.+)$", patch, re.M)
                    files_del = re.findall(r"^\*\*\* Delete File:\s*(.+)$", patch, re.M)
                    for f in files_add:
                        events.append(Event(ts=ts, kind="tool_use", agent="codex",
                                            tool_name="Write",
                                            tool_input={"file_path": f.strip()}))
                    for f in files_upd:
                        events.append(Event(ts=ts, kind="tool_use", agent="codex",
                                            tool_name="Edit",
                                            tool_input={"file_path": f.strip()}))
                    for f in files_del:
                        events.append(Event(ts=ts, kind="tool_use", agent="codex",
                                            tool_name="Delete",
                                            tool_input={"file_path": f.strip()}))
    return events


def gather_events(project_path: Path) -> list[Event]:
    """Merged, time-sorted event list from all Claude + Codex sessions of the project."""
    events: list[Event] = []
    # Claude
    slug = claude_session_dir(project_path)
    if slug.exists():
        for jsonl in sorted(slug.rglob("*.jsonl")):
            events.extend(walk_claude_session(jsonl))
    # Codex
    if CODEX_SESSIONS.exists():
        target = str(project_path.resolve())
        for jsonl in CODEX_SESSIONS.rglob("*.jsonl"):
            events.extend(walk_codex_session(jsonl, target))
    events.sort(key=lambda e: e.ts or "")
    return events


# ---------- Step segmentation & classification -------------------------


PRICING = {  # per-1M-token list prices (subset — enough to estimate USD)
    "claude-opus-4-6":   {"input": 15.0, "cached_input": 1.5, "cache_write": 18.75, "output": 75.0},
    "claude-opus-4-7":   {"input": 15.0, "cached_input": 1.5, "cache_write": 18.75, "output": 75.0},
    "claude-sonnet-4-6": {"input": 3.0, "cached_input": 0.3, "cache_write": 3.75, "output": 15.0},
    "claude-sonnet-4-7": {"input": 3.0, "cached_input": 0.3, "cache_write": 3.75, "output": 15.0},
    "gpt-5-codex":       {"input": 1.25, "cached_input": 0.125, "output": 10.0, "cache_write": 1.25},
    "gpt-5.4":           {"input": 1.25, "cached_input": 0.125, "output": 10.0, "cache_write": 1.25},
    "gpt-5.3-codex":     {"input": 1.25, "cached_input": 0.125, "output": 10.0, "cache_write": 1.25},
}


def _price(model: str) -> dict[str, float] | None:
    ml = (model or "").lower()
    for k, v in PRICING.items():
        if ml.startswith(k) or k.startswith(ml):
            return v
    if "opus" in ml:
        return PRICING["claude-opus-4-6"]
    if "sonnet" in ml:
        return PRICING["claude-sonnet-4-6"]
    if "gpt" in ml or "codex" in ml:
        return PRICING["gpt-5-codex"]
    return None


def _step_usd(tokens: dict[str, int], model: str) -> float:
    p = _price(model)
    if not p:
        return 0.0
    return round(
        (tokens["input"] / 1e6) * p["input"]
        + (tokens["cache_read"] / 1e6) * p.get("cached_input", p["input"])
        + (tokens["cache_creation"] / 1e6) * p.get("cache_write", p["input"])
        + (tokens["output"] / 1e6) * p["output"],
        4,
    )


def _parse_ts(ts: str) -> datetime | None:
    try:
        return datetime.fromisoformat((ts or "").replace("Z", "+00:00"))
    except Exception:
        return None


def classify_step(step: Step) -> str:
    """Heuristic task-class for a step.

    Priority: what the agent did (actions) before what the user said
    (intent). Short steering prompts like ``go''/``continue'' are
    classified by the downstream action, not by the prompt.
    """
    intents = set(step.user_intent)
    bash_kinds = step.bash_kinds
    n_new = len(step.files_written)
    n_edit = len(step.files_edited)
    n_tools = sum(step.tool_counts.values())

    # Empty-action meta: short acknowledgement with nothing done.
    if n_tools < 2 and n_new == 0 and n_edit == 0 and (intents <= {"Steer", "Meta", "Question", "Other"}):
        return "meta"

    # eval-class: any gauntlet/stockfish bash call OR perft-heavy step.
    g = bash_kinds.get("gauntlet", 0) + bash_kinds.get("stockfish", 0)
    p = bash_kinds.get("perft", 0)
    if g >= 1:
        return "eval"
    if p >= 2 and n_new == 0:
        return "eval"

    # debug-class: action-pattern based. Edit-heavy steps with no new
    # files and a build/test cycle are iterative fixing, whether or not
    # the prompt literally says "bug".
    if "BugFixRequest" in intents and n_tools >= 2:
        return "debug"
    if n_edit >= 2 and n_new == 0 and (bash_kinds.get("build", 0) + bash_kinds.get("test", 0)) >= 1:
        return "debug"
    if n_edit >= 5 and n_new == 0:
        return "debug"

    # test-class
    if "TestRequest" in intents and (n_new >= 1 or bash_kinds.get("test", 0) >= 1):
        return "test"
    if bash_kinds.get("test", 0) >= 2 and n_new == 0:
        return "test"
    if bash_kinds.get("uci_run", 0) >= 3 and n_new == 0:
        # The agent is smoke-testing the UCI interface repeatedly.
        return "test"

    # feature
    if n_new >= 1:
        return "feature"
    if ("Improve" in intents or "FeatureRequest" in intents) and n_tools >= 2:
        return "feature"

    # refactor
    if n_edit >= 1 and n_new == 0:
        if "RefactorRequest" in intents or bash_kinds.get("build", 0) >= 1:
            return "refactor"

    # docs
    if "Documentation" in intents and any(f.endswith(".md") for f in step.files_written):
        return "docs"

    # tooling
    if "ToolingBuild" in intents or bash_kinds.get("package", 0) >= 1:
        return "tooling"

    if n_tools == 0:
        return "meta"
    return "other"


def detect_stagnation(steps: list[Step]) -> None:
    """Flag runs of ≥3 consecutive debug steps without new files as stagnation."""
    run = 0
    run_start = None
    for i, s in enumerate(steps):
        if s.task_class == "debug" and len(s.files_written) == 0:
            run += 1
            if run_start is None:
                run_start = i
        else:
            if run >= 3:
                for j in range(run_start, i):
                    steps[j].stagnation = True
            run = 0
            run_start = None
    if run >= 3 and run_start is not None:
        for j in range(run_start, len(steps)):
            steps[j].stagnation = True


def segment(events: list[Event]) -> list[Step]:
    """Walk events; each human prompt starts a new step.

    Claude Code's JSONL sometimes emits the same human prompt twice
    (once when the user presses enter, once on session-resume replay);
    the first copy carries no tool uses because the agent had not yet
    reacted. We merge a just-opened empty step into the next step when
    their prompts match, so the work accrues to the correct row.
    """
    steps: list[Step] = []
    current: Step | None = None
    last_assistant_model = ""
    for e in events:
        if e.kind == "user_prompt":
            # Merge back-to-back identical empty prompts
            if (
                current is not None
                and current.n_events == 0
                and current.user_prompt.strip() == e.text.strip()
            ):
                current.ts_start = e.ts  # move forward; tools coming belong here
                continue
            if current is not None:
                steps.append(current)
            current = Step(
                index=len(steps) + 1,
                ts_start=e.ts,
                ts_end=e.ts,
                duration_s=None,
                user_prompt=e.text,
                user_intent=classify_intent(e.text),
                agent=e.agent,
            )
            continue
        if current is None:
            # Events before the first user_prompt: ignore (system preamble).
            continue
        current.n_events += 1
        if e.ts > current.ts_end:
            current.ts_end = e.ts
        if e.kind == "assistant_text":
            if e.model:
                last_assistant_model = e.model
            for k, v in (e.tokens or {}).items():
                current.tokens[k] = current.tokens.get(k, 0) + v
            # Harvest Elo mentions from assistant text only (user mentions are
            # already covered by intent).
            for m in RE_ELO.finditer(e.text or ""):
                v = int(m.group(1))
                if 400 <= v <= 3500:
                    current.elo_mentions.append(v)
        elif e.kind == "tool_use":
            current.tool_counts[e.tool_name] += 1
            inp = e.tool_input or {}
            if e.tool_name == "Write":
                fp = inp.get("file_path") or inp.get("path") or ""
                if fp:
                    current.files_written.append(fp)
            elif e.tool_name == "Edit":
                fp = inp.get("file_path") or inp.get("path") or ""
                if fp:
                    current.files_edited.append(fp)
            elif e.tool_name == "Read":
                fp = inp.get("file_path") or inp.get("path") or ""
                if fp:
                    current.files_read.append(fp)
            elif e.tool_name == "Bash":
                cmd = inp.get("command") or ""
                if cmd:
                    kind = classify_bash(cmd)
                    current.bash_kinds[kind] += 1
                    if len(current.bash_commands) < 12:
                        current.bash_commands.append(cmd[:180])
    if current is not None:
        steps.append(current)
    # Compute durations and classify.
    for s in steps:
        a = _parse_ts(s.ts_start)
        b = _parse_ts(s.ts_end)
        if a and b:
            s.duration_s = (b - a).total_seconds()
        s.task_class = classify_step(s)
    detect_stagnation(steps)
    return steps


# ---------- Phase grouping ---------------------------------------------


def group_phases(steps: list[Step]) -> list[dict[str, Any]]:
    """Group consecutive steps with the same task_class into phases."""
    phases: list[dict[str, Any]] = []
    if not steps:
        return phases
    cur = {
        "class": steps[0].task_class,
        "start": steps[0].index, "end": steps[0].index,
        "ts_start": steps[0].ts_start, "ts_end": steps[0].ts_end,
        "steps": [steps[0].index],
        "new_files": list(steps[0].files_written),
        "tokens": dict(steps[0].tokens),
        "elos": list(steps[0].elo_mentions),
    }
    for s in steps[1:]:
        same = s.task_class == cur["class"]
        # Allow an occasional off-class step to not split the phase if the
        # surrounding majority agrees.
        if same:
            cur["end"] = s.index
            cur["ts_end"] = s.ts_end
            cur["steps"].append(s.index)
            cur["new_files"].extend(s.files_written)
            for k, v in s.tokens.items():
                cur["tokens"][k] = cur["tokens"].get(k, 0) + v
            cur["elos"].extend(s.elo_mentions)
        else:
            phases.append(cur)
            cur = {
                "class": s.task_class,
                "start": s.index, "end": s.index,
                "ts_start": s.ts_start, "ts_end": s.ts_end,
                "steps": [s.index],
                "new_files": list(s.files_written),
                "tokens": dict(s.tokens),
                "elos": list(s.elo_mentions),
            }
    phases.append(cur)
    return phases


# ---------- Rendering ---------------------------------------------------


def _ts_short(ts: str) -> str:
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).strftime("%m-%d %H:%M")
    except Exception:
        return ts[:16] if ts else ""


def _fmt_dur(secs: float | None) -> str:
    if not secs or secs <= 0:
        return "—"
    m, s = divmod(int(secs), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}h{m:02d}"
    if m:
        return f"{m}m{s:02d}"
    return f"{s}s"


def _fmt_tokens(tok: dict[str, int]) -> str:
    kin = tok.get("input", 0) + tok.get("cache_read", 0) + tok.get("cache_creation", 0)
    kout = tok.get("output", 0)
    return f"{kin/1000:,.0f}k/{kout/1000:,.0f}k"


def render_markdown(project: str, steps: list[Step], phases: list[dict[str, Any]], model_guess: str) -> str:
    lines: list[str] = []
    total_in = sum(s.tokens["input"] + s.tokens["cache_read"] + s.tokens["cache_creation"] for s in steps)
    total_out = sum(s.tokens["output"] for s in steps)
    total_usd = sum(_step_usd(s.tokens, model_guess) for s in steps)
    total_dur = sum((s.duration_s or 0) for s in steps)
    n_files_new = sum(len(s.files_written) for s in steps)
    n_files_edit = sum(len(s.files_edited) for s in steps)
    bash_total: Counter = Counter()
    for s in steps:
        bash_total.update(s.bash_kinds)
    classes: Counter = Counter()
    tokens_by_class: dict[str, int] = {}
    for s in steps:
        classes[s.task_class] += 1
        t = s.tokens["input"] + s.tokens["cache_read"] + s.tokens["cache_creation"] + s.tokens["output"]
        tokens_by_class[s.task_class] = tokens_by_class.get(s.task_class, 0) + t

    lines.append(f"# {project} — session trajectory")
    lines.append("")
    lines.append(f"_Step-wise evolution of the coding-agent session(s) for `{project}`._")
    lines.append(f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}._")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append(f"- **Steps (human prompts)**: {len(steps)}")
    lines.append(f"- **Wallclock span of agent work**: {_fmt_dur(total_dur)}")
    lines.append(f"- **Tokens** (input+cache / output): {total_in/1000:,.0f}k / {total_out/1000:,.0f}k")
    lines.append(f"- **Estimated cost (list price)**: ${total_usd:,.2f}")
    lines.append(f"- **Files written** (new): {n_files_new}  ·  **edited**: {n_files_edit}")
    if bash_total:
        bk = ", ".join(f"{k}={v}" for k, v in bash_total.most_common())
        lines.append(f"- **Bash-command kinds**: {bk}")
    if classes:
        cb = ", ".join(f"{k}={v}" for k, v in classes.most_common())
        lines.append(f"- **Task-class distribution (by step count)**: {cb}")
    lines.append("")

    # Elo evolution
    elos_series = []
    for s in steps:
        # take max Elo mentioned in assistant text of this step (conservative)
        hi = max(s.elo_mentions) if s.elo_mentions else None
        if hi is not None:
            elos_series.append((s.index, s.ts_start, hi))
    if elos_series:
        lines.append("## Claimed-Elo evolution")
        lines.append("")
        lines.append("| Step | Time | Claimed Elo (max in assistant text) |")
        lines.append("|---:|---|---:|")
        for idx, ts, v in elos_series:
            lines.append(f"| {idx} | {_ts_short(ts)} | {v} |")
        lines.append("")

    # Stagnation episodes
    stag_runs: list[tuple[int, int]] = []
    i = 0
    while i < len(steps):
        if steps[i].stagnation:
            j = i
            while j < len(steps) and steps[j].stagnation:
                j += 1
            stag_runs.append((steps[i].index, steps[j - 1].index))
            i = j
        else:
            i += 1
    if stag_runs:
        lines.append("## Stagnation episodes")
        lines.append("")
        for a, b in stag_runs:
            span = b - a + 1
            ts = steps[a - 1].ts_start
            lines.append(f"- **Steps {a}–{b}** ({span} steps, starting {_ts_short(ts)}): consecutive debug prompts with no new source files. See step table below for the tool-use profile.")
        lines.append("")

    # Phases
    lines.append("## Phases (adjacent steps with same task class)")
    lines.append("")
    lines.append("| # | Class | Steps | Wallclock | New files | Tokens (in/out) | Elo claims |")
    lines.append("|---:|---|---|---|---:|---|---|")
    for i, ph in enumerate(phases, 1):
        a = _parse_ts(ph["ts_start"]); b = _parse_ts(ph["ts_end"])
        dur = _fmt_dur((b - a).total_seconds()) if (a and b) else "—"
        elos = ph["elos"]
        elo_cell = f"{min(elos)}→{max(elos)}" if elos else "—"
        step_span = f"{ph['start']}–{ph['end']}" if ph['start'] != ph['end'] else str(ph['start'])
        lines.append(
            f"| {i} | {ph['class']} | {step_span} | {dur} | {len(ph['new_files'])} | "
            f"{_fmt_tokens(ph['tokens'])} | {elo_cell} |"
        )
    lines.append("")

    # Step-by-step table
    lines.append("## Step-by-step timeline")
    lines.append("")
    lines.append("| # | Time | Intent | Class | Tools (top) | New | Edit | Bash kinds | Tokens (in/out) | Stag. | User prompt (short) |")
    lines.append("|---:|---|---|---|---|---:|---:|---|---|:-:|---|")
    for s in steps:
        tools_top = ", ".join(f"{k}×{v}" for k, v in s.tool_counts.most_common(4))
        bks = ", ".join(f"{k}×{v}" for k, v in s.bash_kinds.most_common(4)) or "—"
        stag = "🛑" if s.stagnation else ""
        prompt = short_quote(s.user_prompt, 80).replace("|", "\\|")
        lines.append(
            f"| {s.index} | {_ts_short(s.ts_start)} | {','.join(s.user_intent[:2])} | "
            f"{s.task_class} | {tools_top} | {len(s.files_written)} | "
            f"{len(s.files_edited)} | {bks} | {_fmt_tokens(s.tokens)} | {stag} | {prompt} |"
        )
    lines.append("")

    # Appendix: file creation log (first 30)
    lines.append("## Files created (first 40, in order)")
    lines.append("")
    seen = []
    for s in steps:
        for f in s.files_written:
            if f in seen:
                continue
            seen.append(f)
            lines.append(f"- Step {s.index}: `{f}`")
            if len(seen) >= 40:
                break
        if len(seen) >= 40:
            break
    if not seen:
        lines.append("_(none detected in tool-use stream)_")

    return "\n".join(lines) + "\n"


# ---------- Driver ------------------------------------------------------


def _guess_model(steps: list[Step]) -> str:
    """Pick the most frequent non-synthetic model across assistant events."""
    # We didn't track per-step models explicitly; approximate via agent kind.
    agents = Counter(s.agent for s in steps)
    if agents.get("claude", 0) >= agents.get("codex", 0):
        return "claude-opus-4-6"
    return "gpt-5-codex"


def process(project_name: str, project_path: Path) -> tuple[list[Step], list[dict[str, Any]]]:
    events = gather_events(project_path)
    steps = segment(events)
    phases = group_phases(steps)
    return steps, phases


def main(argv: list[str]) -> None:
    targets = discover_projects()
    if argv:
        targets = [(n, p) for n, p in targets if n in set(argv)]
    outdir_md = REPORTS_DIR / "projects"
    outdir_md.mkdir(parents=True, exist_ok=True)
    outdir_json = DATA_DIR / "projects"
    outdir_json.mkdir(parents=True, exist_ok=True)
    for name, path in targets:
        steps, phases = process(name, path)
        if not steps:
            print(f"→ {name}: no events (skipped)")
            continue
        model = _guess_model(steps)
        md = render_markdown(name, steps, phases, model)
        (outdir_md / f"{name}-TRAJECTORY.md").write_text(md, encoding="utf-8")
        # JSON appendix (compact)
        payload = {
            "project": name,
            "model_guess": model,
            "n_steps": len(steps),
            "steps": [
                {
                    "index": s.index,
                    "ts_start": s.ts_start,
                    "ts_end": s.ts_end,
                    "duration_s": s.duration_s,
                    "agent": s.agent,
                    "user_prompt": s.user_prompt[:240],
                    "user_intent": s.user_intent,
                    "task_class": s.task_class,
                    "tool_counts": dict(s.tool_counts),
                    "files_written": s.files_written,
                    "files_edited": s.files_edited,
                    "bash_kinds": dict(s.bash_kinds),
                    "tokens": s.tokens,
                    "elo_mentions": s.elo_mentions,
                    "stagnation": s.stagnation,
                    "bash_samples": s.bash_commands[:5],
                }
                for s in steps
            ],
            "phases": phases,
        }
        (outdir_json / f"{name}-trajectory.json").write_text(
            json.dumps(payload, indent=2, default=str), encoding="utf-8"
        )
        print(f"→ {name}: {len(steps)} steps, {len(phases)} phases → {name}-TRAJECTORY.md")


if __name__ == "__main__":
    main(sys.argv[1:])
