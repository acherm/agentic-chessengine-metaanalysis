"""Build the first-prompts appendix.

For every chess-engine project in data/projects, find the earliest
*build* session per agent (postmortem analysis sessions are filtered
out using the same heuristic as scripts/recompute_costs.py) and
extract its first user prompt. Engines with no recoverable build
session (only postmortem analysis is in the local cache) are reported
separately so a postmortem prompt is never presented as if it were
the agent's build instruction.

Categories:
  C1 — Canonical "build engine in <PL>" template ("I want to build a chess
       engine in X programming language... at the end, ... Elo rating ...
       'similar' levels"). The Tier-1 generative prompt.
  C2 — Translation/port prompt ("translate Java to X", "preserve features").
  C3 — Plan-driven prompt (the user supplies a structured plan / spec).
  C4 — Inspired-by / replication / external-source prompt
       ("inspired by ...", "reproduce the paper at ...").
  C5 — Analysis / refactor of an existing engine treated as a build
       seed: the agent inherits a checked-in implementation and the
       first prompt asks for spec extraction, audit, or in-place
       rewrite that subsequently produces engine-core writes. (Distinct
       from postmortem-only sessions, which are filtered out entirely.)
  C6 — Other / experimental.

Output:
  paper/appendix/A9-first-prompts.tex
  results/first_prompts.md
"""
from __future__ import annotations
import json, re
from pathlib import Path

# Postmortem-session detector (port + extension of the regex in
# scripts/recompute_costs.py — kept in sync but extended here to catch
# 'in-depth analysis' / 'understand (this|the) code base' phrasings the
# cost script's regex misses).
ANALYSIS_RE = re.compile(
    r'(analyz[es]|analyse|please analyze|review the (repo|code|repository)'
    r'|review this repo|README|'
    r'backlog|annotate|document the architecture|assess whether|'
    r'post-session|post-mortem|introspect|strategy analyst|'
    r'reorganize the first|consider chess\.bf and reorganize'
    r'|in-depth analysis|understand this code base'
    r'|understand the code base|understand the basic architecture)',
    re.IGNORECASE,
)
BUILD_VOCAB_RE = re.compile(
    r'(build|implement|write|create|develop)\s+(a\s+)?(chess|engine)',
    re.IGNORECASE,
)


def is_postmortem(sess: dict) -> bool:
    """Same heuristic as scripts/recompute_costs.py:is_postmortem().

    True if (analysis vocab in first prompt) OR (no engine-core writes
    AND <=5 prompts AND not a build prompt AND single-turn).
    """
    tu = sess.get('tool_uses', {}) or {}
    writes = tu.get('Write', 0) + tu.get('Edit', 0) + tu.get('apply_patch', 0)
    turns = sess.get('turns', 0)
    fp = sess.get('first_prompt_sample', '') or ''
    if ANALYSIS_RE.search(fp):
        return True
    if writes <= 3 and turns <= 5:
        if BUILD_VOCAB_RE.search(fp):
            return False
        if turns <= 1:
            return True
    return False

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT.parent / "data" / "projects"
APP_OUTS = [
    ROOT.parent / "paper" / "appendix" / "A9-first-prompts.tex",
    ROOT.parent / "emse" / "appendix" / "A9-first-prompts.tex",
]
MD_OUT = ROOT / "results" / "first_prompts.md"

# Engines included in the strength evidence + RR; everything else is
# auxiliary / experimental.
CORE_ENGINES = {
    "chess-purec","chess-purec-codex","chess-cplusplus-claude","cplusplus-chess",
    "chess-rust-cc","chess-rust-codex","chess-rust-cc-redo",
    "chess-java-cc","chess-java","chess-py","chess-py-cc",
    "chess-ruby-cc","chess-ruby-codex","chess-Rocq","chess-why3-cc",
    "chess-why3","lean-chess","COBOL-chess","chess-cobol-cc",
    "chess-icon-codex","chess-apl-codex54","chess-assembly-codex",
    "chess-brainfuck","chess-brainfuck-cc","chess-sql","chess-mojo",
    "chess-latex-codex-replication","latex-chess-engine",
    "chess-revisit-java-toRust-codex","chess-revisit-java-toCOBOL-codex",
    "chess-newlang-codex",
    "chess-css-codex","chess-css-codex-guided","chess-css-cc",
}


def classify(text: str) -> str:
    t = text.lower()
    # C1: canonical "I want to build...assess its Elo rating...similar levels"
    if (("i want to build a chess engine" in t or "i'd like to build a chess engine" in t)
        and "elo" in t and "similar" in t):
        return "C1"
    # C2: translation/port
    if (("translate" in t or "translation" in t or "translating" in t or "port" in t)
        and ("chess engine" in t or "java" in t)):
        return "C2"
    # C3: plan-driven
    if t.startswith("implement the following plan") or "implementation plan" in t[:200]:
        return "C3"
    # C4: inspired-by / external-source
    if ("inspired by" in t or "inspiration" in t or "reproduce this paper" in t
        or "github.com" in t[:200] or "arxiv.org" in t[:200]
        or "https://" in t[:120]):
        return "C4"
    # C5: spec / analysis / refactor of an existing engine
    if ("specification of the current" in t or "analyse" in t or "analyze" in t
        or "review this repo" in t or "in-depth analysis" in t
        or "audit" in t or "post-session" in t):
        return "C5"
    return "C6"


def main():
    rows = []
    postmortem_only = []  # (engine, agent, first_ts, prompt) tuples
    for f in sorted(DATA.glob("*.json")):
        if "-trajectory" in f.name or "-features" in f.name or "-instant" in f.name: continue
        try: d = json.loads(f.read_text())
        except: continue
        name = d.get("name", f.stem)
        for agent in ("claude", "codex"):
            a = d.get(agent, {})
            if not isinstance(a, dict): continue
            sessions = a.get("sessions") or []
            if not sessions: continue
            sessions = sorted(sessions, key=lambda s: s.get("first_ts", ""))
            build_sessions = [s for s in sessions if not is_postmortem(s)]
            if not build_sessions:
                # No build session in cache for this (engine, agent). Record
                # the earliest postmortem prompt separately so it never
                # masquerades as a build instruction.
                s0 = sessions[0]
                fp = (s0.get("first_prompt_sample") or "").strip()
                if name in CORE_ENGINES and fp:
                    postmortem_only.append({
                        "engine": name,
                        "agent": "CC" if agent == "claude" else "Codex",
                        "first_ts": (s0.get("first_ts") or "")[:10],
                        "n_sessions": a.get("n_sessions", len(sessions)),
                        "prompt": fp,
                    })
                continue
            s0 = build_sessions[0]
            prompt = s0.get("first_prompt_sample", "")
            if not prompt: continue
            rows.append({
                "engine": name,
                "agent": "CC" if agent == "claude" else "Codex",
                "first_ts": s0.get("first_ts", "")[:10],
                "n_sessions": a.get("n_sessions", len(sessions)),
                "prompt": prompt.strip(),
                "category": classify(prompt),
            })
    # Filter to the core engines (avoid auxiliary "chessfoo", "chessball" etc.)
    rows_core = [r for r in rows if r["engine"] in CORE_ENGINES]
    engines_with_build = {r["engine"] for r in rows_core}
    postmortem_only_engines = sorted({p["engine"] for p in postmortem_only
                                      if p["engine"] not in engines_with_build})

    # Category counts (core only)
    counts = {}
    for r in rows_core: counts[r["category"]] = counts.get(r["category"], 0) + 1
    print(f"Core engines analyzed: {len(rows_core)} sessions across {len({r['engine'] for r in rows_core})} engines")
    for k in sorted(counts): print(f"  {k}: {counts[k]}")

    # ---- Markdown summary ----
    md = ["# First user prompt per engine session", "",
          "Classified category from `eval2/scripts/first_prompts.py`:",
          "",
          "- **C1** Canonical: `I want to build a chess engine in X programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of \"similar\" levels`",
          "- **C2** Translation/port (e.g., Java→Rust)",
          "- **C3** Plan-driven (user-supplied implementation plan)",
          "- **C4** Inspired-by / external-source / replication",
          "- **C5** Analysis / refactor / audit of an existing engine",
          "- **C6** Other",
          "",
          "## Category counts (core-engine sessions)",
          ""]
    for k in sorted(counts):
        md.append(f"- {k}: **{counts[k]}**")
    md.append("")
    md.append("## Per-engine first prompts (core engines only)")
    md.append("")
    for r in sorted(rows_core, key=lambda x: (x["engine"].lower(), x["agent"])):
        md.append(f"### `{r['engine']}` — {r['agent']} ({r['first_ts']}, {r['n_sessions']} sessions, **{r['category']}**)")
        md.append("")
        md.append("> " + r["prompt"][:600].replace("\n", "\n> "))
        md.append("")
    if postmortem_only_engines:
        md.append("## Engines with no build session in local cache")
        md.append("")
        md.append("The following engines have only postmortem analysis sessions in")
        md.append("the local transcript cache; the original build session was either")
        md.append("not recorded (e.g., the engine pre-existed and the agent was only")
        md.append("asked to inspect it) or not retained. Their earliest postmortem")
        md.append("prompt is shown below for reference but is **not** a build")
        md.append("instruction and is excluded from the category counts above.")
        md.append("")
        for p in sorted(postmortem_only, key=lambda x: (x["engine"].lower(), x["agent"])):
            if p["engine"] not in postmortem_only_engines: continue
            md.append(f"### `{p['engine']}` — {p['agent']} ({p['first_ts']}, {p['n_sessions']} sessions, *postmortem-only*)")
            md.append("")
            md.append("> " + p["prompt"][:600].replace("\n", "\n> "))
            md.append("")
    MD_OUT.write_text("\n".join(md) + "\n")
    print(f"wrote {MD_OUT}")
    print(f"  postmortem-only engines (no build session in cache): "
          f"{', '.join(postmortem_only_engines) if postmortem_only_engines else '(none)'}")

    # ---- LaTeX appendix ----
    tex = [
        r"\section{First-prompt analysis: how each session was kicked off}",
        r"\label{app:first-prompts}",
        "",
        r"This appendix lists the first user prompt of each chess-engine session in the corpus, classified into six categories. The objective is to make the entry point of each agent run reproducible: every \emph{measurable} engine in the strength table (\Cref{tab:rq4-elo}) was started with one of these prompts; the most common one is a single template (\textbf{C1}) that we publish verbatim below so that any future replication points at the same instruction.",
        "",
        r"\subsection*{Categories}",
        "",
        r"\begin{description}[leftmargin=1.5em, style=nextline]",
        r"\item[\textbf{C1 --- Canonical generative.}] The template prompt: ``\emph{I want to build a chess engine in [LANG] programming language\ldots\ at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of `similar' levels.}''",
        r"\item[\textbf{C2 --- Translation / port.}] Take an existing engine in language $A$ and translate it to language $B$ (typically with ``preserve features and architecture'').",
        r"\item[\textbf{C3 --- Plan-driven.}] User-supplied structured implementation plan (often produced by a previous agent run); the agent executes the plan step by step.",
        r"\item[\textbf{C4 --- Inspired-by / replication.}] Prompt cites an external artefact (paper, repository, technique writeup) and asks the agent to apply or extend it.",
        r"\item[\textbf{C5 --- Analysis / refactor as build seed.}] The engine source already exists in the working tree; the prompt asks for specification extraction, code audit, or in-place rewrite, and the session subsequently produces engine-core writes (i.e.\ it is a build session even though the entry-point reads as analysis). \emph{Distinct from postmortem-only sessions, which are filtered out of the per-agent first-prompt selection and reported separately below.}",
        r"\item[\textbf{C6 --- Other.}] Experiments and one-offs (typically not in the strength table).",
        r"\end{description}",
        "",
        r"\subsection*{Category distribution across the corpus}",
        "",
    ]

    tex.append(r"\begin{table}[h]\centering\small")
    tex.append(r"\caption{First-prompt category counts across core-engine sessions ($n=" + str(len(rows_core)) + r"$ sessions, $n="
               + str(len({r['engine'] for r in rows_core})) + r"$ distinct engines).}")
    tex.append(r"\begin{tabular}{l r p{0.55\linewidth}}")
    tex.append(r"\toprule")
    tex.append(r"Category & \# Sessions & Engines (\textsc{cc}: Claude Code; \textsc{cdx}: Codex) \\")
    tex.append(r"\midrule")
    cat_labels = {
        "C1": "Canonical",
        "C2": "Translation/port",
        "C3": "Plan-driven",
        "C4": "Inspired-by",
        "C5": "Analysis/refactor",
        "C6": "Other",
    }
    for k in sorted(counts):
        engines_in_cat = [
            f"\\texttt{{{r['engine']}}}\\,(\\textsc{{{r['agent'].lower().replace('codex','cdx')}}})"
            for r in sorted(rows_core, key=lambda x: x["engine"].lower())
            if r["category"] == k
        ]
        tex.append(f"{k} ({cat_labels[k]}) & {counts[k]} & " + ", ".join(engines_in_cat) + r" \\")
    tex.append(r"\bottomrule\end{tabular}\label{tab:first-prompts}\end{table}")
    tex.append("")

    tex.append(r"\subsection*{Per-engine first prompts}")
    tex.append("")
    tex.append(r"Reproduced verbatim, truncated to $\sim$400 characters where longer.")
    tex.append("")

    def latex_escape(s: str) -> str:
        s = s.replace("\\", r"\textbackslash{}")
        for ch in ["&", "%", "#", "$", "_", "{", "}"]:
            s = s.replace(ch, "\\" + ch)
        s = s.replace("~", r"\textasciitilde{}").replace("^", r"\textasciicircum{}")
        return s.replace("\n", r" \\ ")

    for r in sorted(rows_core, key=lambda x: (x["engine"].lower(), x["agent"])):
        tex.append(r"\paragraph{\texttt{" + r["engine"].replace("_", r"\_") + r"} ("
                   + r["agent"] + ", " + r["first_ts"] + ", " + r["category"] + r")}")
        tex.append(r"\textit{`` " + latex_escape(r["prompt"][:400]) + r" ''}")
        tex.append("")

    if postmortem_only_engines:
        tex.append(r"\subsection*{Engines with no build session in local cache}")
        tex.append("")
        tex.append(r"The engines listed below have only \emph{postmortem analysis} sessions in the local transcript cache; the original engine-building session is not available (the engine source pre-existed and the agent was only invited to inspect it, or the build transcript was not retained). Their earliest postmortem prompt is reproduced for transparency but is \textbf{not} a build instruction --- these engines are excluded from the C1--C6 counts and from the per-engine listing above.")
        tex.append("")
        for p in sorted(postmortem_only, key=lambda x: (x["engine"].lower(), x["agent"])):
            if p["engine"] not in postmortem_only_engines: continue
            tex.append(r"\paragraph{\texttt{" + p["engine"].replace("_", r"\_") + r"} ("
                       + p["agent"] + ", " + p["first_ts"] + r", \emph{postmortem-only})}")
            tex.append(r"\textit{`` " + latex_escape(p["prompt"][:400]) + r" ''}")
            tex.append("")

    body = "\n".join(tex) + "\n"
    for out in APP_OUTS:
        if out.parent.exists():
            out.write_text(body)
            print(f"wrote {out}")


if __name__ == "__main__":
    main()
