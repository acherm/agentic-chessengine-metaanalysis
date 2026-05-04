"""Build the unified strength-evidence table for RQ4.

Each row gives, for one engine, all the "evidence of strength" we have:
  - Self-claimed Elo (point or band, from repo bench files or transcripts)
  - PGN-derived Elo (mined from in-tree gauntlets — existing tab_elo column)
  - Anchor-based Elo (Phase B inverse-variance aggregate, all 5 anchors)
  - Round-robin Elo (Bradley-Terry MLE on 506 head-to-head games)
  - Δ : anchor minus self-claim (the Pattern A / Pattern B signal)
  - Perft : "k/n" — checks passed in the preflight perft suite

Output: paper/tables/tab_strength.tex.
"""
from __future__ import annotations
import json, math, re, sys
from pathlib import Path
from glob import glob

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "lib"))
import manifest  # noqa: E402

# ---------- Anchor Elo (manual all-5-anchor combination) ----------
ANCHORS = {"rustic": 1820, "asymptote": 2150,
           "sf_skill0": 900, "sf_skill5": 1658,
           "sf_skill10": 2004, "sf_skill15": 2325}

def parse_pgn(path: Path, engine: str):
    text = path.read_text(errors="ignore")
    w = d = l = 0
    for game in re.split(r'(?=^\[Event ")', text, flags=re.M):
        if not game.strip(): continue
        wm = re.search(r'\[White "([^"]+)"', game)
        bm = re.search(r'\[Black "([^"]+)"', game)
        rm = re.search(r'\[Result "([^"]+)"', game)
        if not (wm and bm and rm): continue
        W, B, R = wm.group(1), bm.group(1), rm.group(1)
        if engine not in (W, B): continue
        if R == "1-0":   (w if W == engine else l for _ in [None])
        if R == "1-0": w += 1 if W == engine else 0; l += 1 if B == engine else 0
        elif R == "0-1": w += 1 if B == engine else 0; l += 1 if W == engine else 0
        elif R == "1/2-1/2": d += 1
    return w, d, l

def anchor_elo(name: str):
    pairs = []
    for anc, anc_elo in ANCHORS.items():
        f = ROOT / "pgn" / "anchor" / f"{name}_vs_{anc}.pgn"
        if not f.is_file(): continue
        w, d, l = parse_pgn(f, name)
        n = w + d + l
        if n == 0: continue
        s = (w + 0.5 * d) / n
        if 0 < s < 1:
            ediff = 400 * math.log10(s / (1 - s))
            elo = anc_elo + ediff
            se = 400 / (n ** 0.5)
            pairs.append((elo, se))
    if not pairs: return None
    weights = [1 / (s ** 2) for _, s in pairs]
    total = sum(weights)
    elo = sum(e * w for (e, _), w in zip(pairs, weights)) / total
    se = (1 / total) ** 0.5
    return (round(elo), round(1.96 * se))

# ---------- RR Elo (n=26 final pass) ----------
RR_ELO = {
    "chess-java-cc": 2050, "chess-revisit-java-toRust-codex": 2037,
    "chess-rust-cc-redo": 1989, "chess-rust-cc": 1882,
    "chess-ruby-cc": 1816, "chess-cplusplus-claude": 1816, "chess-rust-codex": 1801,
    "chess-py": 1771, "chess-why3-cc": 1714, "chess-py-cc": 1714,
    "cplusplus-chess": 1686, "chess-newlang-codex": 1678, "chess-java": 1665,
    "chess-purec": 1645, "chess-assembly-codex": 1631,
    "chess-revisit-java-toCOBOL-codex": 1590, "chess-purec-codex": 1555,
    "COBOL-chess": 1519, "chess-cobol-cc": 1511, "chess-ruby-codex": 1511,
    "lean-chess": 1511, "chess-Rocq": 1481, "chess-why3": 1474,
    "chess-icon-codex": 1442, "chess-apl-codex54": 1285,
    "chess-latex-codex-replication": 1218,
}

# ---------- Self-claimed Elo (from repo bench files + agent transcripts) ----------
# Format: ("point", v) | ("band", lo, hi) | None.
# Compiled from EVAL2_FINDINGS.md §0/§4/§15 and per-repo notes.
SELF = {
    "chess-purec":          ("point", 1997),
    "chess-purec-codex":    ("band", 1670, 1972),
    "chess-cplusplus-claude":("point", 1897),
    "cplusplus-chess":      ("point", 2087),
    "chess-rust-cc":        ("point", 2110),
    "chess-rust-codex":     ("point", 2043),
    "chess-rust-cc-redo":   ("point", 1879),
    "chess-why3-cc":        ("point", 1882),
    "chess-assembly-codex": ("point", 2481),
    "chess-java":           ("point", 1806),
    "chess-java-cc":        ("point", 2212),
    "chess-py":             ("point", 1800),       # session: 50 games vs SF UCI_Elo=1800 at 250ms → 52% → ~1814 (band 1707-1893)
    "chess-py-cc":          ("band", 1500, 1800),  # subagent: pre-measurement planning band; never ran the gauntlet
    "chess-ruby-cc":        ("point", 1840),
    "chess-ruby-codex":     ("point", 920),
    "chess-Rocq":           ("point", 1500),
    "chess-why3":           ("point", 1008),
    "lean-chess":           None,
    "COBOL-chess":          ("band", 1600, 1700),  # SPECIFICATION.md: "~1600-1700 Elo"
    "chess-cobol-cc":       ("point", 1630),       # session: converged "~1630 Elo" across 100 games on SF 1400/1500/1600/1700
    "chess-icon-codex":     None,   # only relative −301 vs SF Skill 0; no absolute claim
    "chess-apl-codex54":    ("point", 1040),    # README: 6-game calibration vs SF UCI_Elo=1320 → 1040.4
    "chess-latex-codex-replication": ("point", 546),
    "latex-chess-engine":   ("point", 1300),
    "chess-sql":            ("band", 900, 1020),  # TOURNAMENT_REPORT.md: "~900-1020 Elo" (conservative 800-1000)
    "chess-brainfuck":      ("point", 1582),  # docs/elo-assessment-2026-03-06.md: 24-game gauntlet vs SF UCI_Elo 1320-1750 → 1582 (CI 1428-1736)
    "chess-brainfuck-cc":   ("point", 578),
    "chess-mojo":           ("point", 1100),
    "chess-revisit-java-toRust-codex":  None,  # only relative to JavaCC parent
    "chess-revisit-java-toCOBOL-codex": None,
    "chess-newlang-codex":  ("point", 2170),    # README: 56.8% vs UCI_Elo=2150, 42.2% vs 2200 → ~2170
}

# ---------- PGN Elo (preserved from existing tab_elo) ----------
PGN_ELO = {
    "chess-purec": (2147, 20),  "chess-rust-cc": (2110, 45),
    "chess-why3-cc": (1991, 59), "chess-rust-cc-redo": (1853, 25),
    "chess-ruby-cc": (1840, 35), "chess-purec-codex": (1836, 32),
    "chess-rust-codex": (1746, 36), "chess-why3": (1008, 58),
    "chess-latex-codex-replication": (546, 213),
}

# ---------- Perft (preflight perft files) ----------
def perft_status(name: str) -> str:
    for variant in (f"{name}.preflight.perft.json", f"{name}.preflight.perft.host.json"):
        p = ROOT / "results" / "per_engine" / variant
        if not p.is_file(): continue
        try:
            d = json.loads(p.read_text())
        except Exception:
            continue
        native = d.get("native") or {}
        checks = native.get("checks") or []
        if checks:
            ok = sum(1 for c in checks if c.get("ok"))
            return f"{ok}/{len(checks)}"
        if (d.get("summary") or {}).get("ok"): return "ok"
        return "n/a"
    return "—"

LANG = {
    "chess-purec": "C", "chess-purec-codex": "C",
    "chess-cplusplus-claude": "C++", "cplusplus-chess": "C++",
    "chess-rust-cc": "Rust", "chess-rust-codex": "Rust",
    "chess-rust-cc-redo": "Rust",
    "chess-java-cc": "Java", "chess-java": "Java",
    "chess-py": "Python", "chess-py-cc": "Python",
    "chess-ruby-cc": "Ruby", "chess-ruby-codex": "Ruby",
    "chess-Rocq": r"Rocq$\to$OCaml", "chess-why3-cc": r"Why3$\to$C",
    "chess-why3": r"Why3$\to$OCaml", "lean-chess": "Lean 4",
    "COBOL-chess": "COBOL", "chess-cobol-cc": "COBOL",
    "chess-icon-codex": "Icon", "chess-apl-codex54": "APL",
    "chess-assembly-codex": "x86-64 asm",
    "chess-brainfuck": "Brainfuck", "chess-brainfuck-cc": "Brainfuck",
    "chess-sql": "SQL",
    "chess-latex-codex-replication": "LaTeX",
    "latex-chess-engine": "TeX",
    "chess-revisit-java-toRust-codex": r"Java$\to$Rust",
    "chess-revisit-java-toCOBOL-codex": r"Java$\to$COBOL",
    "chess-newlang-codex": "DSL/Mini",
    "chess-css-codex": "CSS/HTML", "chess-css-codex-guided": "CSS/HTML",
    "chess-css-cc": "CSS/HTML",
    "chess-mojo": "Mojo",
}


def fmt_self(v):
    if v is None: return "—"
    kind = v[0]
    if kind == "point": return str(v[1])
    if kind == "band": return f"{v[1]}--{v[2]}"
    return "—"


def fmt_anchor(v):
    if v is None: return "—"
    return f"{v[0]} $\\pm$ {v[1]}"


def fmt_rr(v):
    return str(v) if v is not None else "—"


def fmt_pgn(v):
    if v is None: return "—"
    return f"{v[0]} $\\pm$ {v[1]}"


def fmt_delta(anchor, self_):
    if anchor is None or self_ is None: return "—"
    if self_[0] == "band":
        # mid of band
        sv = (self_[1] + self_[2]) / 2
    else:
        sv = self_[1]
    d = round(anchor[0] - sv)
    sign = "+" if d > 0 else ""
    return f"${sign}{d}$"


def main():
    engs, _ = manifest.load()
    rows = []
    for e in engs:
        if e.corpus not in ("main", "port", "dsl", "failure"): continue
        a = anchor_elo(e.name)
        rows.append({
            "engine": e.name,
            "lang": LANG.get(e.name, "—"),
            "self": SELF.get(e.name),
            "pgn": PGN_ELO.get(e.name),
            "anchor": a,
            "rr": RR_ELO.get(e.name),
            "perft": perft_status(e.name),
        })
    # Sort by best of (anchor, RR), descending; engines with neither at the bottom
    def key(r):
        cand = []
        if r["anchor"]: cand.append(r["anchor"][0])
        if r["rr"] is not None: cand.append(r["rr"])
        return -(max(cand) if cand else 0), r["engine"].lower()
    rows.sort(key=key)

    out = [
        r"% Auto-generated by eval2/scripts/build_strength_table.py.",
        r"\begin{table}[ht]\centering\scriptsize",
        r"\caption{Evidence of strength per engine. \textbf{Self}: Elo number(s) the engine itself reports (single value or min--max band, from repository bench files plus agent-transcript claims). \textbf{PGN}: inverse-variance aggregate over games mined from in-tree \pgn{} files vs calibrated \stockfish{} opponents (the agent's own gauntlet methodology). \textbf{Anchor}: Phase B inverse-variance aggregate vs five external references (Rustic, Asymptote, \stockfish{} Skill 5/10/15) at TC$=$120s$+$1s/move on this hardware (\Cref{sec:rq4:anchor}). \textbf{RR}: Bradley-Terry MLE on 649 head-to-head games among the 26 corpus engines that completed the round-robin (\Cref{sec:rq4:rr}). $\Delta$: Anchor minus Self (positive = self-underestimate Pattern B, negative = self-overestimate Pattern A; midpoint of band used for $\Delta$). \textbf{Perft}: number of pseudo-legal-move-count checks passed out of the standard preflight battery (Kiwipete plus an 18-position suite). ``---'' = no data. Rows sorted by best of (anchor, RR), descending.}",
        r"\label{tab:rq4-elo}",
        r"\resizebox{\textwidth}{!}{%",
        r"\begin{tabular}{l l r r r r r c}",
        r"\toprule",
        r"Engine & Language & Self & PGN & Anchor & RR & $\Delta$ & Perft \\",
        r"\midrule",
    ]
    for r in rows:
        eng = r["engine"].replace("_", r"\_")
        out.append(
            f"\\texttt{{{eng}}} & {r['lang']} & "
            f"{fmt_self(r['self'])} & "
            f"{fmt_pgn(r['pgn'])} & "
            f"{fmt_anchor(r['anchor'])} & "
            f"{fmt_rr(r['rr'])} & "
            f"{fmt_delta(r['anchor'], r['self'])} & "
            f"{r['perft']} \\\\")
    out += [r"\bottomrule", r"\end{tabular}}", r"\end{table}"]

    out_tex = ROOT.parent / "paper" / "tables" / "tab_elo.tex"
    out_tex.write_text("\n".join(out) + "\n")
    print(f"wrote {out_tex}")
    # Quick coverage report
    n = len(rows)
    s = lambda k: sum(1 for r in rows if r[k] not in (None, "—"))
    print(f"  rows: {n}")
    print(f"  self-claim: {s('self')}/{n}")
    print(f"  pgn:       {s('pgn')}/{n}")
    print(f"  anchor:    {s('anchor')}/{n}")
    print(f"  rr:        {s('rr')}/{n}")
    print(f"  perft:     {sum(1 for r in rows if r['perft'] not in ('—','n/a'))}/{n}")


if __name__ == "__main__":
    main()
