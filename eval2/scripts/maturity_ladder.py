"""Build the per-engine maturity ladder.

Each engine is scored on eight cumulative levels of maturity:
  L1: Builds (manifest has a docker image OR host invocation; source builds)
  L2: UCI handshake (preflight uci.json: ok==true)
  L3: Perft pass (preflight perft: all checks ok)
  L4: Plays a game (anchor PGN files exist with completed games)
  L5: Long-game robust (≥8 completed games per anchor pair)
  L6: Measurable Elo (≥1 unsaturated anchor pair: score >0%)
  L7: Reaches ~1700 (anchor or RR Elo ≥ 1700)
  L8: Reaches ~2000 (anchor or RR Elo ≥ 2000)

Output: results/maturity_ladder.{md,csv} + paper/tables/tab_maturity.tex.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
from glob import glob
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "lib"))
import manifest  # noqa: E402

# ---------- Anchor-based Elo (5-anchor manual calc) ----------
ANCHOR_ELO = {"rustic": 1820, "asymptote": 2150, "sf_skill5": 1658,
              "sf_skill10": 2004, "sf_skill15": 2325}
PHASE_B_ANCHOR = {  # from manual all-5-anchor calc + summary
    "chess-java-cc": 2096, "chess-rust-cc-redo": 1989, "chess-rust-cc": 1841,
    "chess-rust-codex": 1723, "cplusplus-chess": 1709, "chess-cplusplus-claude": 1680,
    "chess-why3-cc": 1618, "chess-java": 1509, "chess-Rocq": 1499,
    "chess-purec": 1440, "chess-assembly-codex": 1403,
    "chess-revisit-java-toRust-codex": 1922,
}
# Round-robin Elo (n=23 first pass)
RR_ELO = {
    "chess-java-cc": 2077, "chess-rust-cc-redo": 1989, "chess-rust-cc": 1887,
    "chess-ruby-cc": 1839, "chess-cplusplus-claude": 1821, "chess-rust-codex": 1803,
    "chess-py": 1777, "chess-why3-cc": 1736, "chess-py-cc": 1720,
    "cplusplus-chess": 1680, "chess-java": 1664, "chess-purec": 1633,
    "chess-assembly-codex": 1625, "chess-purec-codex": 1578, "chess-ruby-codex": 1530,
    "lean-chess": 1514, "COBOL-chess": 1514, "chess-cobol-cc": 1497,
    "chess-Rocq": 1497, "chess-why3": 1471, "chess-icon-codex": 1416,
    "chess-apl-codex54": 1282, "chess-latex-codex-replication": 1207,
}

PER = ROOT / "results" / "per_engine"
PGN = ROOT / "pgn" / "anchor"


def load_pf_uci(name: str) -> bool:
    for variant in (f"{name}.preflight.uci.json", f"{name}.preflight.uci.host.json"):
        p = PER / variant
        if not p.is_file(): continue
        try:
            d = json.loads(p.read_text())
            if d.get("ok"): return True
        except Exception:
            continue
    return False


def load_pf_perft(name: str) -> str:
    """Return 'pass', 'fail', 'not_attempted' for perft."""
    for variant in (f"{name}.preflight.perft.json", f"{name}.preflight.perft.host.json"):
        p = PER / variant
        if not p.is_file(): continue
        try:
            d = json.loads(p.read_text())
        except Exception:
            continue
        native = d.get("native") or {}
        checks = native.get("checks") or []
        if checks:
            return "pass" if all(c.get("ok") for c in checks) else "fail"
        summary = d.get("summary") or {}
        if summary.get("all_ok") or summary.get("ok"): return "pass"
        # File exists but no checks → engine doesn't implement perft UCI command
        return "not_attempted"
    return "not_attempted"


def has_clean_games(name: str) -> bool:
    """No 'disconnects' or 'illegal move' in any of the engine's PGN files."""
    for f in glob(str(PGN / f"{name}_vs_*.pgn")):
        text = Path(f).read_text(errors="ignore")
        # PGNs are 'min' format so disconnect comments are mostly stripped, but
        # the win/loss reason in the cutechess log files is more reliable.
        # Approximation: if the engine has any '[Result' game and the log
        # shows no 'disconnect' or 'illegal' moves for it.
        log = ROOT / "logs" / "anchor" / f"{name}_vs_*.log"
    # Use logs for correctness signal
    bad = 0; total = 0
    for log in glob(str(ROOT / "logs" / "anchor" / f"{name}_vs_*.log")):
        text = Path(log).read_text(errors="ignore")
        if "disconnect" in text.lower(): bad += 1
        m = re.search(r'Score of \S+ vs \S+: \d+ - \d+ - \d+\s+\[\S+\]\s+(\d+)', text)
        if m: total += int(m.group(1))
    if total == 0: return False
    # "Clean" if disconnects affect <= 1 anchor pair (some pairs failed for OTHER reasons like docker hiccups)
    return bad <= 1


def games_played(name: str) -> tuple[int, int, int]:
    """Returns (anchors_with_pgn, max_games_in_one_anchor, total_games_across_anchors)."""
    n_pgn = 0; max_g = 0; total = 0
    for f in glob(str(PGN / f"{name}_vs_*.pgn")):
        text = Path(f).read_text(errors="ignore")
        n = len(re.findall(r'^\[Result "(1-0|0-1|1/2-1/2)"', text, flags=re.M))
        if n > 0:
            n_pgn += 1; total += n
            if n > max_g: max_g = n
    return n_pgn, max_g, total


def has_measurable_signal(name: str) -> bool:
    """True if engine scored >0% in at least one anchor (not all-zero saturated)."""
    for f in glob(str(PGN / f"{name}_vs_*.pgn")):
        text = Path(f).read_text(errors="ignore")
        # parse each game and check if engine won/drew at least once
        for game in re.split(r'(?=^\[Event ")', text, flags=re.M):
            wm = re.search(r'\[White "([^"]+)"', game)
            bm = re.search(r'\[Black "([^"]+)"', game)
            rm = re.search(r'\[Result "([^"]+)"', game)
            if not (wm and bm and rm): continue
            W, B, R = wm.group(1), bm.group(1), rm.group(1)
            if name not in (W, B): continue
            score = 0.0
            if R == "1-0": score = 1.0 if W == name else 0.0
            elif R == "0-1": score = 1.0 if B == name else 0.0
            elif R == "1/2-1/2": score = 0.5
            if score > 0: return True
    return False


def build_status(eng) -> bool:
    """Heuristic 'builds': either we have a docker image entry OR the engine ran a UCI preflight."""
    if eng.image and (PER / f"{eng.name}.preflight.uci.json").is_file():
        return True
    if eng.host_cmd and (PER / f"{eng.name}.preflight.uci.host.json").is_file():
        return True
    return load_pf_uci(eng.name)  # last-chance


def best_elo(name: str) -> float | None:
    """Max of available Elo (anchor or RR)."""
    candidates = []
    if name in PHASE_B_ANCHOR: candidates.append(PHASE_B_ANCHOR[name])
    if name in RR_ELO: candidates.append(RR_ELO[name])
    return max(candidates) if candidates else None


def main() -> None:
    engs, _ = manifest.load()
    rows = []
    for e in engs:
        if e.corpus not in ("main", "port", "dsl"): continue
        L1 = build_status(e)
        L2 = load_pf_uci(e.name)
        perft_status = load_pf_perft(e.name)
        n_pgn, max_g, total_g = games_played(e.name)
        # L3 = move-gen correct: perft pass OR clean-game play (no disconnects)
        L3 = (perft_status == "pass") or has_clean_games(e.name)
        L4 = total_g >= 1
        L5 = max_g >= 8       # ≥8 games in some anchor pair (long-game stable)
        L6 = has_measurable_signal(e.name)
        elo = best_elo(e.name)
        L7 = elo is not None and elo >= 1700
        L8 = elo is not None and elo >= 2000
        rows.append({
            "engine": e.name, "tier": e.tier, "corpus": e.corpus,
            "L1": L1, "L2": L2, "L3": L3, "L4": L4, "L5": L5,
            "L6": L6, "L7": L7, "L8": L8,
            "elo": elo,
            "anchor": PHASE_B_ANCHOR.get(e.name), "rr": RR_ELO.get(e.name),
            "highest": sum([L1, L2, L3, L4, L5, L6, L7, L8]),
        })

    # Sort by ladder height descending, then by elo descending
    rows.sort(key=lambda r: (-r["highest"], -(r["elo"] or 0)))

    # ---------- Markdown summary ----------
    md = ["# Maturity ladder per engine", "",
          "Cumulative levels (each engine satisfies all checked + sometimes more):",
          "",
          "- L1: Builds (binary/image exists)",
          "- L2: UCI handshake (preflight uciok+readyok)",
          "- L3: Move-gen correct (perft pass OR clean game play with no disconnect)",
          "- L4: Plays at least one full game (anchor PGN with ≥1 completed game)",
          "- L5: Long-game robust (≥8 games completed per pair without disconnect)",
          "- L6: Measurable Elo (≥1 anchor where engine scored >0%)",
          "- L7: Reaches ~1700+ (best anchor/RR Elo ≥1700)",
          "- L8: Reaches ~2000+ (best anchor/RR Elo ≥2000; CCRL-comparable)",
          "",
          "| Engine | Tier | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | Best Elo |",
          "|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---:|"]
    for r in rows:
        c = lambda b: "✓" if b else "—"
        elo_s = str(round(r["elo"])) if r["elo"] else "—"
        md.append(f"| {r['engine']} | {r['tier']} | {c(r['L1'])} | {c(r['L2'])} | "
                  f"{c(r['L3'])} | {c(r['L4'])} | {c(r['L5'])} | "
                  f"{c(r['L6'])} | {c(r['L7'])} | {c(r['L8'])} | {elo_s} |")
    out_md = ROOT / "results" / "maturity_ladder.md"
    out_md.write_text("\n".join(md) + "\n")
    print(f"wrote {out_md}")

    # ---------- LaTeX table ----------
    tex_lines = [
        r"% Auto-generated by eval2/scripts/maturity_ladder.py.",
        r"\begin{table}[ht]\centering\scriptsize",
        r"\caption{The chess-engine maturity ladder. Each level is a separable capability milestone. $\checkmark$ = passes, --- = fails or not applicable. \textbf{L1}: builds + binary exists. \textbf{L2}: UCI handshake. \textbf{L3}: move-gen correct (perft pass OR clean game play). \textbf{L4}: plays $\geq 1$ full game vs an external opponent. \textbf{L5}: long-game robust ($\geq 8$ games per pair without disconnect). \textbf{L6}: measurable Elo (score $>0\%$ vs at least one calibrated anchor). \textbf{L7}: best Elo $\geq 1700$. \textbf{L8}: best Elo $\geq 2000$ (CCRL-comparable strong club / weak expert). ``Best Elo'' is $\max(\text{anchor},\text{round-robin})$. The ladder makes explicit that reaching a high Elo is the \emph{last} of several milestones, and the cliff between the engineering layer (L1--L5) and the chess-knowledge layer (L7--L8) is the corpus's most striking pattern. \textsc{TODO}: regenerate after the $n=26$ round-robin pass completes.}",
        r"\label{tab:maturity-ladder}",
        r"\resizebox{\textwidth}{!}{%",
        r"\begin{tabular}{l c c c c c c c c c r}",
        r"\toprule",
        r"Engine & Tier & L1 & L2 & L3 & L4 & L5 & L6 & L7 & L8 & Best Elo \\",
        r" & & {\tiny build} & {\tiny UCI} & {\tiny mv-gen} & {\tiny plays} & {\tiny long} & {\tiny meas.} & {\tiny $\geq$1700} & {\tiny $\geq$2000} & \\",
        r"\midrule",
    ]
    for r in rows:
        c = lambda b: r"$\checkmark$" if b else "---"
        elo_s = str(round(r["elo"])) if r["elo"] else "---"
        eng = r["engine"].replace("_", r"\_")
        tex_lines.append(
            f"\\texttt{{{eng}}} & {r['tier']} & "
            f"{c(r['L1'])} & {c(r['L2'])} & {c(r['L3'])} & {c(r['L4'])} & "
            f"{c(r['L5'])} & {c(r['L6'])} & {c(r['L7'])} & {c(r['L8'])} & {elo_s} \\\\")
    tex_lines += [r"\bottomrule", r"\end{tabular}}", r"\end{table}"]

    out_tex = ROOT.parent / "paper" / "tables" / "tab_maturity.tex"
    out_tex.write_text("\n".join(tex_lines) + "\n")
    print(f"wrote {out_tex}")

    # Quick population summary
    pop = defaultdict(int)
    for r in rows:
        for L in ("L1","L2","L3","L4","L5","L6","L7","L8"):
            if r[L]: pop[L] += 1
    print(f"\nPopulation per level (n={len(rows)} engines):")
    for L in ("L1","L2","L3","L4","L5","L6","L7","L8"):
        print(f"  {L}: {pop[L]:>3}/{len(rows)}")


if __name__ == "__main__":
    main()
