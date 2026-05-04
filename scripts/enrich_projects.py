"""Enrich per-project data with evaluation-method evidence, test inventory,
and difficulty components.

For each project we compute:
  - agent_elo_claims: (val, context, source) triples mined from user/assistant
    messages in Claude Code and Codex transcripts (not just docs).
  - eval_method: which evaluation infrastructure the agent set up
    (cutechess-cli, custom Elo script, Stockfish gauntlets, random baseline,
    perft-only). Detected by pattern-matching tool calls and prompts.
  - test_evidence: count of test files in the repo, breakdown by test kind
    (perft, unit, integration).
  - difficulty: session duration (hours), total tokens, #debugging-intent
    prompts, debugging/total ratio, #``go''-style prompts.

Writes: data/projects/<name>.json  (merged)

Usage:
  python3 scripts/enrich_projects.py          # all
  python3 scripts/enrich_projects.py chess-py # one
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import (
    CODEX_SESSIONS,
    DATA_DIR,
    IGNORED_DIRS,
    SANDBOX,
    claude_session_dir,
    discover_projects,
    iter_jsonl,
    short_quote,
)

# ---------- Elo claim mining ----------------------------------------------

RE_ELO_CLAIM = re.compile(
    r"(?:(?:≈|~|approximately\s+|about\s+|roughly\s+|final\s+|estimated\s+)?)"
    r"(\d{3,4})\s*(?:\+/-\s*\d+\s*)?(?:Elo|ELO|elo)\b"
)

# Patterns identifying evaluation infrastructure.
EVAL_PATTERNS = {
    "cutechess-cli": re.compile(r"\bcutechess[-_]?cli\b", re.I),
    "Stockfish gauntlet": re.compile(r"\bstockfish\b.*\b(?:UCI_LimitStrength|UCI_Elo|skill[_ ]?\d+|skill level)", re.I),
    "Custom Elo script": re.compile(r"estimate[_ ]?elo|compute[_ ]?elo|elo[_ ]?test|elo_summary", re.I),
    "Random baseline": re.compile(r"random[_ ]?(?:move|legal|opponent|player|baseline)", re.I),
    "Perft tests": re.compile(r"\bperft\b", re.I),
    "Self-play": re.compile(r"self[_ ]?play|selfplay", re.I),
    "Lichess tie-in": re.compile(r"\blichess\b", re.I),
}

DEBUG_PATTERNS = re.compile(
    r"\b(?:bug|broken|doesn'?t work|fails?|failure|crash|error|wrong|illegal|"
    r"undefined|segfault|segmentation|stack overflow|regression|incorrect|invalid|fix|"
    r"revert|not working|still wrong|issue)\b",
    re.I,
)
GO_PATTERNS = re.compile(r"^\s*(go|continue|proceed|yes|ok|okay|keep going|next|more|improve|push on|do it)\s*\.?\s*$", re.I)
CAP_PATTERNS = re.compile(r"\b(implement|add|build|create|develop|design|write|introduce)\b", re.I)


def mine_claude(project_dir: Path) -> dict[str, Any]:
    """Parse Claude Code transcripts for Elo claims, eval patterns, and text."""
    slug = claude_session_dir(project_dir)
    elo: list[dict[str, Any]] = []
    evals = Counter()
    debug_prompts = 0
    go_prompts = 0
    cap_prompts = 0
    total_prompts = 0
    first_ts: str | None = None
    last_ts: str | None = None
    tool_texts: list[str] = []
    if not slug.exists():
        return {"elo_claims": elo, "eval_hits": dict(evals), "debug_prompts": 0, "go_prompts": 0,
                "cap_prompts": 0, "total_prompts": 0, "duration_hours": None}
    for jsonl in slug.rglob("*.jsonl"):
        for obj in iter_jsonl(jsonl):
            ts = obj.get("timestamp")
            if ts:
                if first_ts is None or ts < first_ts:
                    first_ts = ts
                if last_ts is None or ts > last_ts:
                    last_ts = ts
            otype = obj.get("type")
            if otype == "user":
                msg = obj.get("message") or {}
                content = msg.get("content")
                text = _flatten_content(content)
                if text and not text.startswith("<"):
                    total_prompts += 1
                    if DEBUG_PATTERNS.search(text):
                        debug_prompts += 1
                    if GO_PATTERNS.match(text):
                        go_prompts += 1
                    if CAP_PATTERNS.search(text):
                        cap_prompts += 1
                    _record_elo(text, elo, ts, source="claude/user")
                    _record_eval_hits(text, evals)
            elif otype == "assistant":
                msg = obj.get("message") or {}
                content = msg.get("content")
                text = _flatten_content(content)
                if text:
                    _record_elo(text, elo, ts, source="claude/assistant")
                    _record_eval_hits(text, evals)
                    # Also look at tool_use blocks (Bash commands)
                    if isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict) and block.get("type") == "tool_use":
                                inp = block.get("input") or {}
                                cmd = inp.get("command") or ""
                                if cmd:
                                    tool_texts.append(cmd)
                                    _record_eval_hits(cmd, evals)
    duration = None
    if first_ts and last_ts:
        try:
            f = datetime.fromisoformat(first_ts.replace("Z", "+00:00"))
            l = datetime.fromisoformat(last_ts.replace("Z", "+00:00"))
            duration = round((l - f).total_seconds() / 3600, 1)
        except Exception:
            pass
    return {
        "elo_claims": elo,
        "eval_hits": dict(evals),
        "debug_prompts": debug_prompts,
        "go_prompts": go_prompts,
        "cap_prompts": cap_prompts,
        "total_prompts": total_prompts,
        "duration_hours": duration,
    }


def mine_codex(project_dir: Path) -> dict[str, Any]:
    """Parse Codex rollouts whose session cwd equals the project path.

    Strict filter: we only include a rollout when its `session_meta` or
    `turn_context` event names this project's absolute path as the working
    directory. Any other way a session might "mention" the path (e.g. in a
    tool-call argument or in a grep result) is excluded to avoid inflating
    the session-duration metric.
    """
    target = str(project_dir.resolve())
    needle = f'"cwd":"{target}"'
    needle_spaced = f'"cwd": "{target}"'
    elo: list[dict[str, Any]] = []
    evals = Counter()
    debug_prompts = 0
    go_prompts = 0
    cap_prompts = 0
    total_prompts = 0
    first_ts: str | None = None
    last_ts: str | None = None
    if not CODEX_SESSIONS.exists():
        return {"elo_claims": elo, "eval_hits": dict(evals), "debug_prompts": 0, "go_prompts": 0,
                "cap_prompts": 0, "total_prompts": 0, "duration_hours": None}
    for jsonl in CODEX_SESSIONS.rglob("*.jsonl"):
        # Strict pre-filter: only sessions whose cwd is exactly this project.
        try:
            with jsonl.open("rb") as fh:
                head = fh.read(200_000)
            if needle.encode() not in head and needle_spaced.encode() not in head:
                continue
        except Exception:
            continue
        for obj in iter_jsonl(jsonl):
            ts = obj.get("timestamp")
            if ts:
                if first_ts is None or ts < first_ts:
                    first_ts = ts
                if last_ts is None or ts > last_ts:
                    last_ts = ts
            otype = obj.get("type")
            payload = obj.get("payload") or {}
            if otype == "event_msg":
                ptype = payload.get("type")
                if ptype == "user_message":
                    text = payload.get("message") or ""
                    if text and not text.startswith("<environment_context>"):
                        total_prompts += 1
                        if DEBUG_PATTERNS.search(text):
                            debug_prompts += 1
                        if GO_PATTERNS.match(text):
                            go_prompts += 1
                        if CAP_PATTERNS.search(text):
                            cap_prompts += 1
                        _record_elo(text, elo, ts, source="codex/user")
                        _record_eval_hits(text, evals)
                elif ptype == "agent_message":
                    text = payload.get("message") or ""
                    if text:
                        _record_elo(text, elo, ts, source="codex/assistant")
                        _record_eval_hits(text, evals)
            elif otype == "response_item":
                ptype = payload.get("type")
                if ptype == "reasoning":
                    summ = payload.get("summary") or []
                    for s in summ:
                        if isinstance(s, dict):
                            t = s.get("text") or ""
                            _record_elo(t, elo, ts, source="codex/reasoning")
                            _record_eval_hits(t, evals)
                elif ptype == "function_call":
                    args = payload.get("arguments") or ""
                    if args:
                        _record_eval_hits(args, evals)
    duration = None
    if first_ts and last_ts:
        try:
            f = datetime.fromisoformat(first_ts.replace("Z", "+00:00"))
            l = datetime.fromisoformat(last_ts.replace("Z", "+00:00"))
            duration = round((l - f).total_seconds() / 3600, 1)
        except Exception:
            pass
    return {
        "elo_claims": elo,
        "eval_hits": dict(evals),
        "debug_prompts": debug_prompts,
        "go_prompts": go_prompts,
        "cap_prompts": cap_prompts,
        "total_prompts": total_prompts,
        "duration_hours": duration,
    }


def _flatten_content(content) -> str:
    """Concatenate text blocks from a Claude Code message content."""
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


def _record_elo(text: str, out: list[dict[str, Any]], ts: str | None, source: str) -> None:
    if not text:
        return
    for m in RE_ELO_CLAIM.finditer(text):
        val = int(m.group(1))
        if 50 <= val <= 3500:
            s = max(0, m.start() - 60)
            e = min(len(text), m.end() + 60)
            ctx = text[s:e].replace("\n", " ")
            out.append({"elo": val, "ts": ts, "source": source, "context": short_quote(ctx, 200)})


def _record_eval_hits(text: str, counter: Counter) -> None:
    if not text:
        return
    for k, pat in EVAL_PATTERNS.items():
        if pat.search(text):
            counter[k] += 1


# ---------- Test-evidence scan --------------------------------------------

TEST_DIR_NAMES = {"test", "tests", "spec", "specs", "t"}
TEST_FILE_PATTERNS = [
    re.compile(r"^test[_-].+\.(py|rb|rs|js|ts|go|java|cpp|cc|c|hs|lua|ml|lean|v|why|mlw)$"),
    re.compile(r".+[_-]test\.(py|rb|rs|js|ts|go|java|cpp|cc|c|hs|lua|ml|lean|v|why|mlw)$"),
    re.compile(r".+[_-]spec\.rb$"),
    re.compile(r".+Test\.java$"),
    re.compile(r".+Tests\.java$"),
]


def test_inventory(project: Path) -> dict[str, Any]:
    test_files: list[str] = []
    perft_tests = 0
    for dirpath, dirnames, filenames in os.walk(project):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS and not d.startswith(".")]
        rel = Path(dirpath).relative_to(project)
        parts_lower = {p.lower() for p in rel.parts}
        in_test_dir = bool(parts_lower & TEST_DIR_NAMES)
        for name in filenames:
            if any(pat.match(name) for pat in TEST_FILE_PATTERNS):
                test_files.append(str(rel / name))
            elif in_test_dir and not name.startswith("."):
                if not name.endswith((".md", ".txt", ".json", ".log")):
                    test_files.append(str(rel / name))
            if "perft" in name.lower():
                perft_tests += 1
    # Also count perft mentions in test files
    return {
        "n_test_files": len(test_files),
        "test_files": test_files[:40],
        "has_perft_tests": perft_tests > 0,
        "perft_test_files": perft_tests,
    }


# ---------- Main ----------------------------------------------------------


def enrich(project_dir: Path) -> dict[str, Any]:
    claude = mine_claude(project_dir)
    codex = mine_codex(project_dir)
    tests = test_inventory(project_dir)
    all_claims = sorted(claude["elo_claims"] + codex["elo_claims"], key=lambda x: x.get("ts") or "")
    elo_values = sorted({c["elo"] for c in all_claims})
    # Difficulty: session duration (pick longest), total prompts, debug ratio
    session_hrs = max(
        [x for x in [claude.get("duration_hours"), codex.get("duration_hours")] if x is not None],
        default=None,
    )
    total = claude["total_prompts"] + codex["total_prompts"]
    debug = claude["debug_prompts"] + codex["debug_prompts"]
    cap = claude["cap_prompts"] + codex["cap_prompts"]
    goc = claude["go_prompts"] + codex["go_prompts"]
    difficulty = {
        "session_hours_longest": session_hrs,
        "total_prompts": total,
        "debug_prompts": debug,
        "cap_prompts": cap,
        "go_prompts": goc,
        "debug_ratio": round(debug / total, 3) if total else None,
        "go_ratio": round(goc / total, 3) if total else None,
    }
    return {
        "agent_elo_claims": {
            "values": elo_values,
            "samples": all_claims[:20],
        },
        "eval_infrastructure": _merge_counters(claude["eval_hits"], codex["eval_hits"]),
        "test_evidence": tests,
        "difficulty": difficulty,
    }


def _merge_counters(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, 0) + v
    return out


def main(argv: list[str]) -> None:
    projects_dir = DATA_DIR / "projects"
    all_targets = {name: path for name, path in discover_projects()}
    if argv:
        targets = [(a, all_targets.get(a) or (SANDBOX / a)) for a in argv]
    else:
        targets = list(all_targets.items())
    for logical, p in targets:
        if not p.exists():
            continue
        print(f"→ {logical}")
        enriched = enrich(p)
        appendix = projects_dir / f"{logical}.json"
        if appendix.exists():
            try:
                prior = json.loads(appendix.read_text())
            except Exception:
                prior = {"name": logical, "path": str(p)}
        else:
            prior = {"name": logical, "path": str(p)}
        prior["enrichment"] = enriched
        appendix.parent.mkdir(parents=True, exist_ok=True)
        appendix.write_text(json.dumps(prior, indent=2, default=str))
        claims = enriched["agent_elo_claims"]["values"]
        evals = enriched["eval_infrastructure"]
        tests = enriched["test_evidence"]["n_test_files"]
        d = enriched["difficulty"]
        print(f"    claims={claims[:6]}  eval={list(evals)[:4]}  tests={tests}  debug_ratio={d.get('debug_ratio')}  hrs={d.get('session_hours_longest')}")


if __name__ == "__main__":
    main(sys.argv[1:])
