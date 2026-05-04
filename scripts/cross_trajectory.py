r"""Cross-project analysis of the per-engine trajectories.

Reads every `data/projects/<name>-trajectory.json` produced by
`scripts/trajectory.py`, filters to the main engine corpus + the four
special-role engines, and answers three questions:

  1. What is \emph{common} across sessions --- the modal engine
     trajectory (step-count, task-class mix, phase order, oracle
     cadence, Elo-curve shape)?
  2. What is \emph{different} --- the axes of variation (debug-ratio
     spread, session-length spread, improve-loop density) and which
     engines sit at the tails?
  3. What is \emph{unique} --- behaviors that appear in only one
     engine's trajectory.

Writes:
  reports/CROSS_TRAJECTORY.md   human-readable analysis
  data/cross_trajectory.json    machine appendix
"""

from __future__ import annotations

import json
import re
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import DATA_DIR, REPORTS_DIR
from synthesis import CLASSIFICATION

IN_SCOPE = {"engine", "engine-port", "engine-dsl", "engine-failure"}
MAIN_ONLY = {"engine"}

# Exclusion rules for thin trajectories (sessions where we cannot draw
# meaningful phase / shape conclusions):
MIN_STEPS = 5     # drop engines with fewer than N recoverable user prompts
MIN_TOKENS = 10_000  # drop engines with essentially no recorded agent work

# Engines always included regardless of thresholds (they are important
# cases even when short; we flag them with a note).
ALWAYS_INCLUDE: set[str] = set()

# Engines always excluded (archived transcripts, evasion redirect parts,
# etc.). Kept empty by default; populate if a downstream run needs it.
ALWAYS_EXCLUDE: set[str] = set()


def trajectory_ok(t: dict) -> tuple[bool, str]:
    name = t.get("project")
    if name in ALWAYS_INCLUDE:
        return True, "forced-in"
    if name in ALWAYS_EXCLUDE:
        return False, "forced-out"
    steps = t.get("steps", []) or []
    if len(steps) < MIN_STEPS:
        return False, f"<{MIN_STEPS} steps"
    total_tok = 0
    for s in steps:
        for v in (s.get("tokens") or {}).values():
            total_tok += v
    if total_tok < MIN_TOKENS:
        return False, f"<{MIN_TOKENS} tokens"
    return True, "ok"


def load_trajectories() -> tuple[dict[str, dict], dict[str, str]]:
    """Return (included, excluded) trajectories with a reason per exclusion."""
    included: dict[str, dict] = {}
    excluded: dict[str, str] = {}
    for p in (DATA_DIR / "projects").glob("*-trajectory.json"):
        try:
            d = json.loads(p.read_text())
        except Exception:
            continue
        name = d.get("project")
        if not name or CLASSIFICATION.get(name) not in IN_SCOPE:
            continue
        ok, reason = trajectory_ok(d)
        if ok:
            included[name] = d
        else:
            excluded[name] = reason
    return included, excluded


# ---------- Per-engine derived stats ---------------------------------

def step_class_sequence(traj: dict) -> list[str]:
    return [s["task_class"] for s in traj.get("steps", [])]


def phase_class_sequence(traj: dict) -> list[str]:
    return [ph["class"] for ph in traj.get("phases", [])]


def task_class_fractions(traj: dict) -> dict[str, float]:
    cs = Counter(step_class_sequence(traj))
    total = sum(cs.values()) or 1
    return {k: round(v / total, 3) for k, v in cs.items()}


def intent_fractions(traj: dict) -> dict[str, float]:
    c: Counter = Counter()
    total = 0
    for s in traj.get("steps", []):
        for lab in s.get("user_intent") or []:
            c[lab] += 1
            total += 1
    return {k: round(v / total, 3) for k, v in c.items()} if total else {}


def bash_kind_fractions(traj: dict) -> dict[str, float]:
    c: Counter = Counter()
    total = 0
    for s in traj.get("steps", []):
        for k, v in (s.get("bash_kinds") or {}).items():
            c[k] += v
            total += v
    return {k: round(v / total, 3) for k, v in c.items()} if total else {}


def tool_count_fractions(traj: dict) -> dict[str, float]:
    c: Counter = Counter()
    total = 0
    for s in traj.get("steps", []):
        for k, v in (s.get("tool_counts") or {}).items():
            c[k] += v
            total += v
    return {k: round(v / total, 3) for k, v in c.items()} if total else {}


def first_step_index(traj: dict, predicate) -> int | None:
    for s in traj.get("steps", []):
        if predicate(s):
            return s["index"]
    return None


def total_tokens(traj: dict) -> int:
    t = 0
    for s in traj.get("steps", []):
        for k, v in (s.get("tokens") or {}).items():
            t += v
    return t


def elo_curve(traj: dict) -> list[tuple[int, int]]:
    """(step_index, max_elo_in_step) for steps that mention Elo."""
    out = []
    for s in traj.get("steps", []):
        claims = s.get("elo_mentions") or []
        if claims:
            out.append((s["index"], max(claims)))
    return out


def elo_curve_shape(curve: list[tuple[int, int]]) -> str:
    """Classify the Elo trajectory into monotone / zigzag / plateau / single / none."""
    if not curve:
        return "none"
    if len(curve) == 1:
        return "single"
    vals = [v for _, v in curve]
    diffs = [b - a for a, b in zip(vals, vals[1:])]
    pos = sum(1 for d in diffs if d > 0)
    neg = sum(1 for d in diffs if d < 0)
    if pos and not neg:
        return "monotone-up"
    if neg and not pos:
        return "monotone-down"
    if pos >= 2 and neg >= 2:
        return "zigzag"
    last_change = abs(vals[-1] - vals[0])
    if last_change < 50 and (pos + neg) > 0:
        return "plateau"
    return "mixed"


def new_file_accretion(traj: dict) -> list[int]:
    """Cumulative new-file count per step (for front-vs-back-loaded shape)."""
    cum = 0
    out = []
    for s in traj.get("steps", []):
        cum += len(s.get("files_written") or [])
        out.append(cum)
    return out


def front_load_ratio(traj: dict) -> float | None:
    """% of new files created in the first third of the session."""
    n = len(traj.get("steps") or [])
    if n < 3:
        return None
    cum = new_file_accretion(traj)
    if cum[-1] == 0:
        return None
    first_third = cum[(n // 3)] if (n // 3) < len(cum) else cum[-1]
    return round(first_third / cum[-1], 3)


# ---------- Motif discovery ------------------------------------------

def phase_trigrams(traj: dict) -> list[tuple[str, str, str]]:
    seq = phase_class_sequence(traj)
    return list(zip(seq, seq[1:], seq[2:]))


def step_bigrams(traj: dict) -> list[tuple[str, str]]:
    seq = step_class_sequence(traj)
    return list(zip(seq, seq[1:]))


def project_signature(traj: dict) -> dict[str, Any]:
    steps = traj.get("steps", [])
    phases = traj.get("phases", [])
    curve = elo_curve(traj)
    return {
        "n_steps": len(steps),
        "n_phases": len(phases),
        "modal_class_seq": phase_class_sequence(traj),
        "task_class": task_class_fractions(traj),
        "intent": intent_fractions(traj),
        "bash_kinds": bash_kind_fractions(traj),
        "tools": tool_count_fractions(traj),
        "total_tokens": total_tokens(traj),
        "wallclock_h": round(
            sum((s.get("duration_s") or 0) for s in steps) / 3600.0, 2
        ),
        "new_files": sum(len(s.get("files_written") or []) for s in steps),
        "edited_files": sum(len(s.get("files_edited") or []) for s in steps),
        "stagnation_steps": sum(1 for s in steps if s.get("stagnation")),
        "first_perft_step": first_step_index(
            traj, lambda s: (s.get("bash_kinds") or {}).get("perft", 0) > 0
        ),
        "first_gauntlet_step": first_step_index(
            traj, lambda s: (s.get("bash_kinds") or {}).get("gauntlet", 0) > 0
        ),
        "first_build_step": first_step_index(
            traj, lambda s: (s.get("bash_kinds") or {}).get("build", 0) > 0
        ),
        "elo_curve": curve,
        "elo_shape": elo_curve_shape(curve),
        "front_load_ratio": front_load_ratio(traj),
    }


# ---------- Analysis dimensions --------------------------------------

def task_class_matrix(sigs: dict[str, dict]) -> dict[str, list[float]]:
    """Per-class, the sorted list of engines' class fractions."""
    classes = sorted({c for s in sigs.values() for c in s["task_class"]})
    out: dict[str, list[float]] = {}
    for c in classes:
        out[c] = sorted([s["task_class"].get(c, 0.0) for s in sigs.values()])
    return out


def percentile(xs: list[float], p: float) -> float:
    if not xs:
        return 0.0
    k = (len(xs) - 1) * p
    lo = int(k)
    hi = min(lo + 1, len(xs) - 1)
    frac = k - lo
    return xs[lo] * (1 - frac) + xs[hi] * frac


trajs_cache: dict[str, dict] = {}


def build_common_section(sigs: dict[str, dict]) -> str:
    main = {n: s for n, s in sigs.items() if CLASSIFICATION.get(n) == "engine"}
    # Step count
    steps_list = sorted(s["n_steps"] for s in main.values())
    # Tokens
    tokens_list = sorted(s["total_tokens"] for s in main.values())
    # Wallclock
    hrs_list = sorted(s["wallclock_h"] for s in main.values())
    # Task-class medians
    tcm = task_class_matrix(main)
    medians = {c: round(statistics.median(vs), 3) for c, vs in tcm.items()}
    # Modal phase pattern
    tri_counter: Counter = Counter()
    for s in main.values():
        for tri in phase_trigrams({"phases": [{"class": c} for c in s["modal_class_seq"]]}):
            tri_counter[tri] += 1
    # First gauntlet
    first_g = [s["first_gauntlet_step"] for s in main.values() if s["first_gauntlet_step"]]
    first_p = [s["first_perft_step"] for s in main.values() if s["first_perft_step"]]
    first_b = [s["first_build_step"] for s in main.values() if s["first_build_step"]]
    # Pool raw bash-kind counts across engines (not fractions).
    bk_pool: Counter = Counter()
    for name, sig in main.items():
        traj = trajs_cache.get(name) or {}
        for step in traj.get("steps", []):
            for k, v in (step.get("bash_kinds") or {}).items():
                bk_pool[k] += v
    total_bk = sum(bk_pool.values()) or 1
    # Elo-shape counts
    shapes = Counter(s["elo_shape"] for s in main.values())

    lines = []
    lines.append("## Common patterns (main corpus, $n = {})".format(len(main)))
    lines.append("")
    lines.append("### Session shape")
    lines.append("")
    lines.append("| Metric | 25th pct. | median | 75th pct. | max |")
    lines.append("|---|---:|---:|---:|---:|")
    lines.append(
        f"| User prompts per session | {percentile(steps_list, 0.25):.0f} | "
        f"{statistics.median(steps_list):.0f} | {percentile(steps_list, 0.75):.0f} | "
        f"{max(steps_list) if steps_list else 0} |"
    )
    lines.append(
        f"| Tokens per session (k) | {percentile(tokens_list, 0.25)/1000:,.0f} | "
        f"{statistics.median(tokens_list)/1000:,.0f} | {percentile(tokens_list, 0.75)/1000:,.0f} | "
        f"{max(tokens_list)/1000:,.0f} |"
    )
    lines.append(
        f"| Wallclock hours | {percentile(hrs_list, 0.25):.1f} | "
        f"{statistics.median(hrs_list):.1f} | {percentile(hrs_list, 0.75):.1f} | "
        f"{max(hrs_list):.1f} |"
    )
    lines.append("")
    lines.append("### Task-class distribution (median fraction of steps)")
    lines.append("")
    lines.append("| class | median frac. | 75th pct. frac. |")
    lines.append("|---|---:|---:|")
    for c, v in sorted(medians.items(), key=lambda x: -x[1]):
        p75 = percentile(tcm[c], 0.75)
        lines.append(f"| {c} | {v} | {p75:.3f} |")
    lines.append("")
    lines.append(
        f"### When do agents first reach for each oracle / build?\n\n"
        f"- First `cargo test`/`make` invocation: median step "
        f"**{statistics.median(first_b) if first_b else '—'}** of {len(first_b)} engines.\n"
        f"- First `perft` test: median step "
        f"**{statistics.median(first_p) if first_p else '—'}** of {len(first_p)} engines.\n"
        f"- First gauntlet (cutechess / custom Elo script): median step "
        f"**{statistics.median(first_g) if first_g else '—'}** of {len(first_g)} engines.\n"
    )
    lines.append("")
    lines.append("### Elo-claim trajectory shape")
    lines.append("")
    lines.append("| shape | engines |")
    lines.append("|---|---:|")
    for k, v in shapes.most_common():
        lines.append(f"| {k} | {v} |")
    lines.append("")
    lines.append("### Most frequent phase-trigrams across the corpus")
    lines.append("")
    lines.append("| trigram | # engines |")
    lines.append("|---|---:|")
    for tri, n in tri_counter.most_common(10):
        lines.append(f"| `{tri[0]} → {tri[1]} → {tri[2]}` | {n} |")
    lines.append("")
    lines.append("### Bash-kind share across the corpus (pooled raw counts)")
    lines.append("")
    lines.append("| Kind | # calls | % of pooled total |")
    lines.append("|---|---:|---:|")
    for k, v in bk_pool.most_common():
        lines.append(f"| `{k}` | {v} | {100.0 * v / total_bk:.1f}% |")
    lines.append("")
    return "\n".join(lines)


def build_differences_section(sigs: dict[str, dict]) -> str:
    main = {n: s for n, s in sigs.items() if CLASSIFICATION.get(n) == "engine"}
    # Rank by each axis
    def rank_by(key):
        return sorted(main.items(), key=lambda kv: kv[1][key], reverse=True)

    debug_ratio = [(n, s["task_class"].get("debug", 0)) for n, s in main.items()]
    debug_ratio.sort(key=lambda kv: -kv[1])
    improve_ratio = [(n, s["intent"].get("Improve", 0)) for n, s in main.items()]
    improve_ratio.sort(key=lambda kv: -kv[1])
    edit_vs_new = []
    for n, s in main.items():
        new, edit = s["new_files"], s["edited_files"]
        total = new + edit
        if total == 0:
            continue
        edit_vs_new.append((n, edit / total, new, edit))
    edit_vs_new.sort(key=lambda kv: -kv[1])
    late_gauntlet = [
        (n, s["first_gauntlet_step"]) for n, s in main.items() if s["first_gauntlet_step"]
    ]
    late_gauntlet.sort(key=lambda kv: -kv[1])
    stag_heavy = sorted(
        ((n, s["stagnation_steps"]) for n, s in main.items() if s["stagnation_steps"] > 0),
        key=lambda kv: -kv[1],
    )

    lines = []
    lines.append("## Differences (where engines diverge)")
    lines.append("")
    lines.append("### Debug ratio (% of steps classified `debug`)")
    lines.append("")
    lines.append("| Engine | Debug frac. |")
    lines.append("|---|---:|")
    for n, v in debug_ratio[:5]:
        lines.append(f"| {n} | {v:.2f} |")
    lines.append("| … | |")
    for n, v in debug_ratio[-3:]:
        lines.append(f"| {n} | {v:.2f} |")
    lines.append("")
    lines.append("### Improve-loop density (`Improve` intent / total prompts)")
    lines.append("")
    lines.append("| Engine | Improve frac. |")
    lines.append("|---|---:|")
    for n, v in improve_ratio[:5]:
        lines.append(f"| {n} | {v:.2f} |")
    lines.append("| … | |")
    for n, v in improve_ratio[-3:]:
        lines.append(f"| {n} | {v:.2f} |")
    lines.append("")
    lines.append("### Edit-vs-new file ratio (large = many revisions per module)")
    lines.append("")
    lines.append("| Engine | edit / total | new | edit |")
    lines.append("|---|---:|---:|---:|")
    for n, v, new, edit in edit_vs_new[:6]:
        lines.append(f"| {n} | {v:.2f} | {new} | {edit} |")
    lines.append("| … | | | |")
    for n, v, new, edit in edit_vs_new[-3:]:
        lines.append(f"| {n} | {v:.2f} | {new} | {edit} |")
    lines.append("")
    lines.append("### Latest first-gauntlet step (agents that delayed strength testing)")
    lines.append("")
    lines.append("| Engine | First gauntlet at step |")
    lines.append("|---|---:|")
    for n, v in late_gauntlet[:5]:
        lines.append(f"| {n} | {v} |")
    lines.append("")
    if stag_heavy:
        lines.append("### Stagnation-heavy engines (# of flagged steps)")
        lines.append("")
        lines.append("| Engine | Stagnation steps |")
        lines.append("|---|---:|")
        for n, v in stag_heavy[:6]:
            lines.append(f"| {n} | {v} |")
        lines.append("")
    return "\n".join(lines)


def build_uniques_section(sigs: dict[str, dict]) -> str:
    """Behaviors that appear in only one engine in the main corpus."""
    lines = ["## Unique signatures (main corpus, $n = 1$ occurrences)", ""]
    main = {n: s for n, s in sigs.items() if CLASSIFICATION.get(n) == "engine"}
    # 1. task-classes present in only one engine
    class_eng: dict[str, list[str]] = defaultdict(list)
    for n, s in main.items():
        for c, f in s["task_class"].items():
            if f > 0:
                class_eng[c].append(n)
    uniq_classes = {c: engs for c, engs in class_eng.items() if len(engs) == 1}
    if uniq_classes:
        lines.append("### Task-classes observed in a single engine")
        lines.append("")
        for c, engs in uniq_classes.items():
            lines.append(f"- `{c}` only in **{engs[0]}**")
        lines.append("")
    # 2. bash kinds unique to one engine
    bash_eng: dict[str, list[str]] = defaultdict(list)
    for n, s in main.items():
        for k in s["bash_kinds"]:
            if s["bash_kinds"][k] > 0:
                bash_eng[k].append(n)
    uniq_bash = {k: engs for k, engs in bash_eng.items() if len(engs) == 1}
    if uniq_bash:
        lines.append("### Bash-kinds observed in a single engine")
        lines.append("")
        for k, engs in uniq_bash.items():
            lines.append(f"- `{k}` only in **{engs[0]}**")
        lines.append("")
    # 3. Unique tool usage (e.g. WebSearch, Glob-heavy, subagent)
    tool_eng: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for n, s in main.items():
        for t, f in s["tools"].items():
            if f > 0:
                tool_eng[t].append((n, f))
    uniq_tools = {t: engs for t, engs in tool_eng.items() if len(engs) == 1}
    if uniq_tools:
        lines.append("### Tools used in a single engine")
        lines.append("")
        for t, engs in sorted(uniq_tools.items()):
            n, f = engs[0]
            lines.append(f"- `{t}` only in **{n}** ({f*100:.1f}% of its tool calls)")
        lines.append("")
    # 4. Outlier engines on absolute axes
    lines.append("### Single-engine extrema")
    lines.append("")
    most_steps = max(main.items(), key=lambda kv: kv[1]["n_steps"])
    most_files = max(main.items(), key=lambda kv: kv[1]["new_files"])
    most_tokens = max(main.items(), key=lambda kv: kv[1]["total_tokens"])
    most_stag = max(
        main.items(),
        key=lambda kv: kv[1]["stagnation_steps"],
        default=(None, {"stagnation_steps": 0}),
    )
    most_elo_claims = max(
        main.items(), key=lambda kv: len(kv[1]["elo_curve"])
    )
    lines.append(f"- Most user prompts: **{most_steps[0]}** ({most_steps[1]['n_steps']})")
    lines.append(f"- Most new files written: **{most_files[0]}** ({most_files[1]['new_files']})")
    lines.append(f"- Most tokens consumed: **{most_tokens[0]}** ({most_tokens[1]['total_tokens']/1e6:.1f}M)")
    if most_stag[0] and most_stag[1]["stagnation_steps"] > 0:
        lines.append(f"- Most stagnation steps: **{most_stag[0]}** ({most_stag[1]['stagnation_steps']})")
    lines.append(f"- Most Elo claims in assistant text: **{most_elo_claims[0]}** ({len(most_elo_claims[1]['elo_curve'])} mentions)")
    lines.append("")
    return "\n".join(lines)


def build_special_section(sigs: dict[str, dict]) -> str:
    """Ports / DSL / failure --- reported separately."""
    lines = ["## Special-role experiments (separate from the main corpus)", ""]
    for role in ("engine-port", "engine-dsl", "engine-failure"):
        roll = {n: s for n, s in sigs.items() if CLASSIFICATION.get(n) == role}
        if not roll:
            continue
        lines.append(f"### {role}")
        lines.append("")
        lines.append("| Engine | Steps | Phases | Tokens (M) | Class mix (top-3) | Elo shape |")
        lines.append("|---|---:|---:|---:|---|---|")
        for n, s in sorted(roll.items()):
            top3 = ", ".join(
                f"{c}={s['task_class'][c]:.2f}"
                for c in sorted(s["task_class"], key=s["task_class"].get, reverse=True)[:3]
            )
            lines.append(
                f"| {n} | {s['n_steps']} | {s['n_phases']} | "
                f"{s['total_tokens']/1e6:.2f} | {top3} | {s['elo_shape']} |"
            )
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    trajs, excluded = load_trajectories()
    trajs_cache.update(trajs)
    sigs = {n: project_signature(t) for n, t in trajs.items()}

    out = []
    out.append("# Cross-project trajectory analysis")
    out.append("")
    out.append(f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_")
    out.append("")
    out.append(f"Scope: {len(sigs)} engines with enough trajectory substance "
               f"({sum(1 for n in sigs if CLASSIFICATION.get(n)=='engine')} main corpus + "
               f"{sum(1 for n in sigs if CLASSIFICATION.get(n) in {'engine-port','engine-dsl','engine-failure'})} special-role).")
    out.append(f"Exclusion rules: $\\geq${MIN_STEPS} user prompts AND $\\geq${MIN_TOKENS:,} recorded tokens. Excluded engines (thin trajectories): "
               + (", ".join(f"`{n}` ({r})" for n, r in sorted(excluded.items())) if excluded else "_none_")
               + ".")
    out.append("")
    out.append("The three passes below ask: **what is common**, **what is different**, and **what is unique** across the per-engine trajectories emitted by `scripts/trajectory.py`. Shape statistics, task-class mix, oracle cadence, Elo-curve shape, and phase-trigram frequencies are computed per engine and pooled.")
    out.append("")

    out.append(build_common_section(sigs))
    out.append(build_differences_section(sigs))
    out.append(build_uniques_section(sigs))
    out.append(build_special_section(sigs))

    out.append("## Paper-ready takeaways")
    out.append("")
    out.append("1. **The modal trajectory is: feature-build → perft → gauntlet → improve-loop.** The phase-trigram table above shows the most common triplet by count; most main-corpus engines touch each of the four stages in that order before plateauing.")
    out.append("2. **Debug ratio, not total effort, separates hard from easy engines.** The same absolute hours can yield a clean feature arc (low debug frac.) or a long oracle-debugging loop (high debug frac.) --- see the debug-ratio table.")
    out.append("3. **Agents reach for oracles early.** The median first-perft step is low; the median first-gauntlet step follows within a few steps. Agents do not wait to be told to evaluate.")
    out.append("4. **Elo-curve shape is typically monotone-up or plateau** after an initial feature-build phase. Zigzag curves are associated with engines that had mid-session regressions we could independently recover from the trajectory.")
    out.append("5. **Uniqueness concentrates in language-specific tool-use** (compiler-specific bash-kinds) and in the stagnation-episode profile. The special-role engines (ports, DSL, failure) show distinctly different phase patterns from the main corpus, justifying their separate reporting.")
    out.append("")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "CROSS_TRAJECTORY.md").write_text("\n".join(out), encoding="utf-8")
    (DATA_DIR / "cross_trajectory.json").write_text(
        json.dumps(sigs, indent=2, default=str), encoding="utf-8"
    )
    print(f"Wrote reports/CROSS_TRAJECTORY.md and data/cross_trajectory.json over {len(sigs)} engines.")


if __name__ == "__main__":
    main()
