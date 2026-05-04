"""Parse Claude Code and Codex session logs into a normalized schema.

Output per project:
  - user_prompts (raw + short quote)
  - assistant turn count
  - tool_use summary (top tool names, counts)
  - token usage (input/output/cached)
  - model(s) used
  - timeline (session_start, session_end)
  - estimated cost USD (best effort using PRICING_USD_PER_MTOK)
  - per-session summaries

Usage:
  python3 scripts/extract_sessions.py                # scan all chess-* dirs
  python3 scripts/extract_sessions.py chess-java-cc  # single project
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from common import (
    CLAUDE_PROJECTS,
    CODEX_SESSIONS,
    DATA_DIR,
    PRICING_USD_PER_MTOK,
    SANDBOX,
    claude_session_dir,
    iter_jsonl,
    safe_int,
    short_quote,
)

# ---------- Claude Code ---------------------------------------------------


def parse_claude_session(jsonl: Path) -> dict[str, Any]:
    info: dict[str, Any] = {
        "path": str(jsonl),
        "session_id": jsonl.stem,
        "user_prompts": [],
        "assistant_messages": 0,
        "tool_uses": Counter(),
        "tokens": {
            "input": 0,
            "output": 0,
            "cache_read": 0,
            "cache_creation": 0,
        },
        "models": set(),
        "first_ts": None,
        "last_ts": None,
        "turns": 0,
        "num_events": 0,
        "has_sidechain": False,
    }
    for obj in iter_jsonl(jsonl):
        info["num_events"] += 1
        ts = obj.get("timestamp")
        if ts:
            if not info["first_ts"]:
                info["first_ts"] = ts
            info["last_ts"] = ts
        if obj.get("isSidechain"):
            info["has_sidechain"] = True
        otype = obj.get("type")
        if otype == "user":
            msg = obj.get("message", {})
            content = msg.get("content")
            # content can be string or list of blocks
            texts: list[str] = []
            if isinstance(content, str):
                texts.append(content)
            elif isinstance(content, list):
                for block in content:
                    if isinstance(block, dict):
                        if block.get("type") == "text":
                            texts.append(str(block.get("text", "")))
                        elif block.get("type") == "tool_result":
                            # Skip tool results -- they're not human prompts
                            pass
            # Keep only prompts that plausibly come from the human
            # (ignore tool_result-bearing user turns which are empty here).
            for t in texts:
                if t and not t.startswith("<local-command-stdout>") and not t.startswith("[Request interrupted"):
                    info["user_prompts"].append({"ts": ts, "text": t})
        elif otype == "assistant":
            info["assistant_messages"] += 1
            msg = obj.get("message", {})
            model = msg.get("model")
            if model:
                info["models"].add(model)
            usage = msg.get("usage", {}) or {}
            info["tokens"]["input"] += safe_int(usage.get("input_tokens"))
            info["tokens"]["output"] += safe_int(usage.get("output_tokens"))
            info["tokens"]["cache_read"] += safe_int(usage.get("cache_read_input_tokens"))
            info["tokens"]["cache_creation"] += safe_int(usage.get("cache_creation_input_tokens"))
            content = msg.get("content")
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        info["tool_uses"][block.get("name") or "unknown"] += 1
        elif otype in {"tool_use", "tool_result"}:
            pass
    info["models"] = sorted(info["models"])
    info["tool_uses"] = dict(info["tool_uses"])
    info["turns"] = len(info["user_prompts"])
    return info


def scan_claude_for_project(project_dir: Path) -> dict[str, Any]:
    """Collect Claude Code sessions for a project.

    Claude Code's on-disk layout has shifted over versions:
      - main session as `<slug>/<uuid>.jsonl` at the top level (newer)
      - sidecar transcripts under `<slug>/<uuid>/subagents/*.jsonl`
      - a `sessions-index.json` describing each session's metadata
    We read whatever is available and count only top-level (non-subagent)
    transcripts as "main sessions" while still extracting prompts/tokens
    from subagent transcripts for completeness.
    """
    slug_dir = claude_session_dir(project_dir)
    sessions: list[dict[str, Any]] = []
    subagent_sessions: list[dict[str, Any]] = []
    missing_from_index: list[str] = []
    if slug_dir.exists():
        for jsonl in sorted(slug_dir.glob("*.jsonl")):
            sessions.append(parse_claude_session(jsonl))
        # Subagents (often the only evidence left after cleanup)
        for jsonl in sorted(slug_dir.rglob("*.jsonl")):
            if jsonl.parent == slug_dir:
                continue
            subagent_sessions.append(parse_claude_session(jsonl))
        # sessions-index.json: lightweight pointer to transcripts that may
        # no longer be on disk. Capture them to report coverage gaps.
        idx = slug_dir / "sessions-index.json"
        if idx.exists():
            try:
                data = json.loads(idx.read_text())
                for e in data.get("entries", []):
                    fp = e.get("fullPath")
                    if fp and not Path(fp).exists():
                        missing_from_index.append(fp)
            except Exception:
                pass
    agg = aggregate_sessions(sessions, agent="Claude Code")
    sub_agg = aggregate_sessions(subagent_sessions, agent="Claude Code (subagent)")
    agg["sessions"] = sessions
    agg["session_dir"] = str(slug_dir)
    agg["subagent_sessions_count"] = len(subagent_sessions)
    agg["subagent_tokens"] = sub_agg["cost"]["tokens_total"]
    agg["subagent_usd"] = sub_agg["cost"]["usd_estimate"]
    agg["subagents"] = subagent_sessions
    agg["missing_from_index"] = missing_from_index
    return agg


# ---------- Codex ---------------------------------------------------------


def parse_codex_session(jsonl: Path) -> dict[str, Any]:
    """Parse a Codex rollout JSONL. May span multiple projects."""
    info: dict[str, Any] = {
        "path": str(jsonl),
        "session_id": jsonl.stem,
        "user_prompts": [],
        "assistant_messages": 0,
        "tool_uses": Counter(),
        "tokens": {"input": 0, "output": 0, "cache_read": 0, "reasoning_output": 0},
        "models": set(),
        "first_ts": None,
        "last_ts": None,
        "cwds": set(),
    }
    last_token_total: dict[str, int] | None = None
    for obj in iter_jsonl(jsonl):
        ts = obj.get("timestamp")
        if ts:
            if not info["first_ts"]:
                info["first_ts"] = ts
            info["last_ts"] = ts
        otype = obj.get("type")
        payload = obj.get("payload", {}) or {}
        if otype == "session_meta":
            cwd = payload.get("cwd")
            if cwd:
                info["cwds"].add(cwd)
        elif otype == "turn_context":
            cwd = payload.get("cwd")
            if cwd:
                info["cwds"].add(cwd)
            model = payload.get("model")
            if model:
                info["models"].add(model)
        elif otype == "event_msg":
            ptype = payload.get("type")
            if ptype == "user_message":
                # Filter env context preambles
                msg = payload.get("message", "")
                if msg and not msg.startswith("<environment_context>"):
                    info["user_prompts"].append({"ts": ts, "text": msg})
            elif ptype == "token_count":
                info_blk = payload.get("info") or {}
                tku = (info_blk.get("total_token_usage") if isinstance(info_blk, dict) else None) or {}
                # Codex emits cumulative totals; we'll take max (last).
                last_token_total = {
                    "input": safe_int(tku.get("input_tokens")),
                    "output": safe_int(tku.get("output_tokens")),
                    "cache_read": safe_int(tku.get("cached_input_tokens")),
                    "reasoning_output": safe_int(tku.get("reasoning_output_tokens")),
                }
            elif ptype == "agent_message":
                info["assistant_messages"] += 1
        elif otype == "response_item":
            ptype = payload.get("type")
            if ptype == "function_call":
                info["tool_uses"][payload.get("name") or "unknown"] += 1
            elif ptype == "local_shell_call":
                info["tool_uses"]["local_shell"] += 1
    if last_token_total:
        info["tokens"] = last_token_total
    info["models"] = sorted(info["models"])
    info["cwds"] = sorted(info["cwds"])
    info["tool_uses"] = dict(info["tool_uses"])
    info["turns"] = len(info["user_prompts"])
    return info


def scan_codex_index() -> list[dict[str, Any]]:
    """Parse *every* Codex session; slow but one-shot."""
    all_sessions = []
    if not CODEX_SESSIONS.exists():
        return all_sessions
    for jsonl in CODEX_SESSIONS.rglob("*.jsonl"):
        all_sessions.append(parse_codex_session(jsonl))
    return all_sessions


def filter_codex_for_project(all_codex: list[dict[str, Any]], project_dir: Path) -> list[dict[str, Any]]:
    target = str(project_dir.resolve())
    hits = []
    for s in all_codex:
        for cwd in s.get("cwds") or []:
            if cwd == target or cwd.startswith(target + "/"):
                hits.append(s)
                break
    return hits


# ---------- Aggregation + costing -----------------------------------------


def estimate_cost(sessions: list[dict[str, Any]]) -> dict[str, float]:
    totals = {"input": 0, "output": 0, "cache_read": 0, "cache_creation": 0}
    cost = 0.0
    per_model: dict[str, dict[str, int]] = defaultdict(lambda: {"input": 0, "output": 0, "cache_read": 0, "cache_creation": 0})
    for s in sessions:
        tok = s.get("tokens", {}) or {}
        models = s.get("models") or ["unknown"]
        # Prefer a real model name; skip synthetic/empty markers.
        real = [m for m in models if m and not m.startswith("<")]
        m = real[0] if real else (models[0] if models else "unknown")
        for k, v in tok.items():
            totals[k] = totals.get(k, 0) + safe_int(v)
            per_model[m][k] = per_model[m].get(k, 0) + safe_int(v)
    for model, tok in per_model.items():
        m = (model or "").lower()
        price = PRICING_USD_PER_MTOK.get(m)
        if not price:
            # Try prefix / family match, e.g. "claude-opus-4-7-20260118" → opus-4-7
            for k, v in PRICING_USD_PER_MTOK.items():
                if m.startswith(k) or k.startswith(m):
                    price = v
                    break
        if not price:
            # Fallback heuristics by family
            if "opus" in m:
                price = PRICING_USD_PER_MTOK["claude-opus-4-6"]
            elif "sonnet" in m:
                price = PRICING_USD_PER_MTOK["claude-sonnet-4-6"]
            elif "haiku" in m:
                price = PRICING_USD_PER_MTOK["claude-haiku-4-5"]
            elif "gpt" in m or "codex" in m or m.startswith("o"):
                price = PRICING_USD_PER_MTOK["gpt-5-codex"]
        if not price:
            continue
        cost += (tok.get("input", 0) / 1e6) * price.get("input", 0)
        cost += (tok.get("cache_read", 0) / 1e6) * price.get("cached_input", 0)
        cost += (tok.get("cache_creation", 0) / 1e6) * price.get("cache_write", price.get("input", 0))
        cost += (tok.get("output", 0) / 1e6) * price.get("output", 0)
    return {"tokens_total": totals, "usd_estimate": round(cost, 2)}


def aggregate_sessions(sessions: list[dict[str, Any]], agent: str) -> dict[str, Any]:
    agg: dict[str, Any] = {
        "agent": agent,
        "n_sessions": len(sessions),
        "n_user_prompts": 0,
        "n_assistant_messages": 0,
        "tool_uses": Counter(),
        "models": set(),
        "first_ts": None,
        "last_ts": None,
    }
    for s in sessions:
        agg["n_user_prompts"] += len(s.get("user_prompts", []))
        agg["n_assistant_messages"] += s.get("assistant_messages", 0)
        for k, v in (s.get("tool_uses") or {}).items():
            agg["tool_uses"][k] += v
        agg["models"].update(s.get("models") or [])
        fs = s.get("first_ts")
        ls = s.get("last_ts")
        if fs and (agg["first_ts"] is None or fs < agg["first_ts"]):
            agg["first_ts"] = fs
        if ls and (agg["last_ts"] is None or ls > agg["last_ts"]):
            agg["last_ts"] = ls
    agg["tool_uses"] = dict(agg["tool_uses"].most_common())
    agg["models"] = sorted(agg["models"])
    agg["cost"] = estimate_cost(sessions)
    return agg


# ---------- CLI -----------------------------------------------------------


def run_for_project(project_dir: Path, codex_index: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    claude = scan_claude_for_project(project_dir)
    codex_sessions = filter_codex_for_project(codex_index or [], project_dir)
    codex = aggregate_sessions(codex_sessions, agent="Codex")
    codex["sessions"] = codex_sessions
    return {
        "project": project_dir.name,
        "path": str(project_dir),
        "claude": claude,
        "codex": codex,
    }


def main(argv: list[str]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    codex_index = scan_codex_index()
    if argv:
        targets = [SANDBOX / a for a in argv]
    else:
        targets = sorted([p for p in SANDBOX.iterdir() if p.is_dir() and p.name.startswith("chess")])
    for project_dir in targets:
        if not project_dir.exists():
            print(f"skip: {project_dir} not found", file=sys.stderr)
            continue
        result = run_for_project(project_dir, codex_index)
        out = DATA_DIR / f"sessions_{project_dir.name}.json"
        with out.open("w") as fh:
            json.dump(result, fh, indent=2, default=str)
        cl = result["claude"]
        cd = result["codex"]
        print(
            f"{project_dir.name}: claude={cl['n_sessions']}s/{cl['n_user_prompts']}p/${cl['cost']['usd_estimate']}"
            f"  codex={cd['n_sessions']}s/{cd['n_user_prompts']}p/${cd['cost']['usd_estimate']}"
        )


if __name__ == "__main__":
    main(sys.argv[1:])
