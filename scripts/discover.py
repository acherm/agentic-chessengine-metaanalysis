"""Discover chess-related folders under ~/SANDBOX and classify them.

For each candidate:
  - primary language
  - coding agent (Claude Code / Codex / both / unknown)
  - period (first ts, last ts from sessions; fallback to git)
  - LOC + file breakdown
  - chess-specific features detected
  - git stats (commits, authors)
  - attached session summary (# sessions, # prompts, models, $ estimate)

Writes:
  data/overview.json
  reports/OVERVIEW.md

Usage:
  python3 scripts/discover.py
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import (
    DATA_DIR,
    REPORTS_DIR,
    SANDBOX,
    CODEX_SESSIONS,
    claude_session_dir,
    compute_loc,
    detect_agent_suffix,
    discover_projects,
    fmt_ts,
    git,
    is_git_repo,
    primary_language,
    scan_features,
)
import extract_sessions as sess


def git_summary(repo: Path) -> dict[str, Any]:
    if not is_git_repo(repo):
        return {"is_git": False}
    first = git(["log", "--reverse", "--format=%aI|%s", "--no-merges"], repo).splitlines()
    last = git(["log", "--format=%aI|%s", "--no-merges", "-1"], repo).splitlines()
    nb = git(["rev-list", "--count", "HEAD"], repo) or "0"
    authors = git(["shortlog", "-sne", "HEAD"], repo).splitlines()
    return {
        "is_git": True,
        "n_commits": int(nb) if nb.isdigit() else 0,
        "first_commit": first[0] if first else "",
        "last_commit": last[0] if last else "",
        "authors": authors,
    }


def classify(project: Path, codex_index, logical_name: str | None = None) -> dict[str, Any]:
    name = logical_name or project.name
    print(f"→ scanning {name}")
    loc = compute_loc(project)
    prim = primary_language(loc)
    features = scan_features(project)
    features_summary = {k: len(v) for k, v in features.items() if v}

    # Sessions
    claude = sess.scan_claude_for_project(project)
    codex_sessions = sess.filter_codex_for_project(codex_index, project)
    codex = sess.aggregate_sessions(codex_sessions, agent="Codex")

    # Agent detection
    agents = []
    if claude["n_sessions"] > 0 or claude_session_dir(project).exists():
        agents.append("Claude Code")
    if codex["n_sessions"] > 0:
        agents.append("Codex")
    if not agents:
        guess = detect_agent_suffix(name)
        if guess:
            agents.append(guess + " (by-name, no sessions)")

    # Period
    starts, ends = [], []
    for t in (claude.get("first_ts"), codex.get("first_ts")):
        if t:
            starts.append(t)
    for t in (claude.get("last_ts"), codex.get("last_ts")):
        if t:
            ends.append(t)
    git_info = git_summary(project)
    if git_info.get("is_git"):
        fc = (git_info.get("first_commit") or "").split("|", 1)[0]
        lc = (git_info.get("last_commit") or "").split("|", 1)[0]
        if fc:
            starts.append(fc)
        if lc:
            ends.append(lc)

    period = {
        "start": min(starts) if starts else "",
        "end": max(ends) if ends else "",
    }

    total_cost = round(
        (claude.get("cost", {}).get("usd_estimate", 0.0) or 0.0)
        + (codex.get("cost", {}).get("usd_estimate", 0.0) or 0.0),
        2,
    )

    return {
        "name": name,
        "path": str(project),
        "primary_language": prim,
        "agents": agents,
        "period": period,
        "loc": {
            "total_files": loc.total_files,
            "total_loc": loc.total_loc,
            "by_lang": loc.loc_by_lang,
            "files_by_lang": loc.files_by_lang,
        },
        "features": features_summary,
        "feature_paths": features,
        "claude": {
            "n_sessions": claude["n_sessions"],
            "n_user_prompts": claude["n_user_prompts"],
            "n_assistant_messages": claude["n_assistant_messages"],
            "models": claude["models"],
            "tool_uses": claude["tool_uses"],
            "tokens": claude["cost"]["tokens_total"],
            "usd": claude["cost"]["usd_estimate"],
            "first_ts": claude["first_ts"],
            "last_ts": claude["last_ts"],
        },
        "codex": {
            "n_sessions": codex["n_sessions"],
            "n_user_prompts": codex["n_user_prompts"],
            "n_assistant_messages": codex["n_assistant_messages"],
            "models": codex["models"],
            "tool_uses": codex["tool_uses"],
            "tokens": codex["cost"]["tokens_total"],
            "usd": codex["cost"]["usd_estimate"],
            "first_ts": codex["first_ts"],
            "last_ts": codex["last_ts"],
        },
        "git": git_info,
        "total_usd_estimate": total_cost,
    }


def write_overview(items: list[dict[str, Any]]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with (REPORTS_DIR / "OVERVIEW.md").open("w") as fh:
        fh.write(render_overview_md(items))
    with (DATA_DIR / "overview.json").open("w") as fh:
        json.dump(items, fh, indent=2, default=str)


def render_overview_md(items: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    lines.append("# Chess meta-analysis — overview")
    lines.append("")
    lines.append(f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}  ")
    lines.append(f"Projects scanned: {len(items)}  ")
    lines.append("")
    lines.append("## Summary table")
    lines.append("")
    lines.append(
        "| Project | Language | Agents | Period | Files | LOC | Sessions | Prompts | USD (est.) |"
    )
    lines.append(
        "|---|---|---|---|---:|---:|---:|---:|---:|"
    )
    items_sorted = sorted(items, key=lambda x: (x.get("period", {}).get("start") or ""))
    for it in items_sorted:
        agents = ", ".join(it.get("agents") or []) or "—"
        ps = fmt_ts(it["period"].get("start"))
        pe = fmt_ts(it["period"].get("end"))
        per = f"{ps} → {pe}" if ps else "—"
        ns = (it["claude"]["n_sessions"] or 0) + (it["codex"]["n_sessions"] or 0)
        np = (it["claude"]["n_user_prompts"] or 0) + (it["codex"]["n_user_prompts"] or 0)
        lines.append(
            f"| {it['name']} | {it.get('primary_language') or '—'} | {agents} | {per} "
            f"| {it['loc']['total_files']} | {it['loc']['total_loc']} | {ns} | {np} "
            f"| ${it.get('total_usd_estimate') or 0:.2f} |"
        )
    lines.append("")
    lines.append("## Chess feature coverage (per project)")
    lines.append("")
    # Collect all features observed anywhere.
    all_features: list[str] = []
    for it in items:
        for k in (it.get("features") or {}).keys():
            if k not in all_features:
                all_features.append(k)
    if all_features:
        header = "| Project | " + " | ".join(all_features) + " |"
        sep = "|---|" + "---|" * len(all_features)
        lines.append(header)
        lines.append(sep)
        for it in items_sorted:
            feats = it.get("features") or {}
            row = [it["name"]]
            for f in all_features:
                row.append("✓" if f in feats else "")
            lines.append("| " + " | ".join(row) + " |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    print("Indexing Codex sessions…")
    codex_index = sess.scan_codex_index()
    print(f"  indexed {len(codex_index)} Codex sessions")
    targets = discover_projects()
    items: list[dict[str, Any]] = []
    for logical, p in targets:
        try:
            items.append(classify(p, codex_index, logical_name=logical))
        except Exception as e:
            print(f"!! failed on {logical}: {e}")
    write_overview(items)
    print(f"Wrote {len(items)} projects to data/overview.json and reports/OVERVIEW.md")


if __name__ == "__main__":
    main()
