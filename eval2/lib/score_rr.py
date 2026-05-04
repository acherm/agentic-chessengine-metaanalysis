"""Score the round-robin pgn/rr/*.pgn into Bradley-Terry-style Elo,
anchored to chess-rust-cc-redo's Phase B Elo (1989). Uses a small
prior-game count to keep the MLE finite when an engine has 100% or 0%.
"""
from __future__ import annotations
import math, re, statistics as stat
from collections import defaultdict
from glob import glob
from pathlib import Path

ANCHOR = "chess-rust-cc-redo"
ANCHOR_ELO = 1989.0
PRIOR_GAMES = 0.5  # virtual draw vs every opponent — keeps MLE finite

# Phase B anchor Elo (from results/anchor_summary.md + manual all-5-anchor calc).
PHASE_B = {
    "chess-java-cc": 2096, "chess-rust-cc-redo": 1989, "chess-rust-cc": 1841,
    "chess-rust-codex": 1723, "cplusplus-chess": 1709, "chess-cplusplus-claude": 1680,
    "chess-why3-cc": 1618, "chess-java": 1509, "chess-Rocq": 1499,
    "chess-purec": 1440, "chess-assembly-codex": 1403,
    # Bounded engines (saturated 0% vs all Phase B anchors). Stamped at the
    # per-anchor floor of ~1276-1438. RR will give the first real signal.
    "chess-purec-codex": 1438, "chess-ruby-codex": 1438, "chess-ruby-cc": 1349,
    "chess-py": 1349, "chess-py-cc": 1349, "chess-cobol-cc": 1276,
    "COBOL-chess": 1276, "chess-why3": 1276, "lean-chess": 1276,
    "chess-apl-codex54": 1276, "chess-icon-codex": 1276,
    "chess-latex-codex-replication": 1276,
    # Port/DSL engines added in n=26 pass
    "chess-revisit-java-toRust-codex": 1922,   # Phase B 1922 ± 106
    # chess-revisit-java-toCOBOL-codex and chess-newlang-codex: no Phase B anchor data
}

def parse_all() -> dict[str, dict[str, list[int]]]:
    """results[A][B] = [W, D, L] from A's perspective."""
    results: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(lambda: [0, 0, 0]))
    for pgn in glob("pgn/rr/*.pgn"):
        text = Path(pgn).read_text()
        for game in re.split(r'(?=^\[Event ")', text, flags=re.M):
            if not game.strip(): continue
            w = re.search(r'\[White "([^"]+)"', game)
            b = re.search(r'\[Black "([^"]+)"', game)
            r = re.search(r'\[Result "([^"]+)"', game)
            if not (w and b and r): continue
            W, B, R = w.group(1), b.group(1), r.group(1)
            if R == "1-0":
                results[W][B][0] += 1; results[B][W][2] += 1
            elif R == "0-1":
                results[W][B][2] += 1; results[B][W][0] += 1
            elif R == "1/2-1/2":
                results[W][B][1] += 1; results[B][W][1] += 1
    return results

def fit_elo(results, n_iter=2000, damping=0.3) -> dict[str, float]:
    engines = list(results.keys())
    elos = {e: 1500.0 for e in engines}
    for _ in range(n_iter):
        grad = defaultdict(float); hess = defaultdict(float)
        for A in engines:
            for B in engines:
                if A == B: continue
                wdl = results[A].get(B, [0, 0, 0])
                n = sum(wdl)
                sa = wdl[0] + 0.5 * wdl[1] + 0.5 * PRIOR_GAMES
                n_eff = n + PRIOR_GAMES
                ea = 1.0 / (1.0 + 10 ** ((elos[B] - elos[A]) / 400.0))
                grad[A] += (sa - n_eff * ea)
                hess[A] += n_eff * ea * (1 - ea)
        for e in engines:
            if hess[e] > 1e-9:
                elos[e] += (400.0 / math.log(10)) * grad[e] / hess[e] * damping
        if ANCHOR in elos:
            d = ANCHOR_ELO - elos[ANCHOR]
            for e in engines: elos[e] += d
    return elos

def per_engine_record(results, engine):
    w = d = l = 0
    for opp, wdl in results[engine].items():
        w += wdl[0]; d += wdl[1]; l += wdl[2]
    return w, d, l, len(results[engine])

def correlations(elos, ref):
    common = [(e, elos[e], ref[e]) for e in elos if e in ref]
    if len(common) < 5: return None, None, len(common)
    xs = [x[1] for x in common]; ys = [x[2] for x in common]
    mx, my = stat.mean(xs), stat.mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = (sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys)) ** 0.5
    pearson = num / den if den else 0
    rxs = [sorted(xs).index(x) for x in xs]
    rys = [sorted(ys).index(y) for y in ys]
    mx, my = stat.mean(rxs), stat.mean(rys)
    num = sum((a - mx) * (b - my) for a, b in zip(rxs, rys))
    den = (sum((a - mx) ** 2 for a in rxs) * sum((b - my) ** 2 for b in rys)) ** 0.5
    spearman = num / den if den else 0
    return pearson, spearman, len(common)

if __name__ == "__main__":
    results = parse_all()
    elos = fit_elo(results)
    ranked = sorted(elos.keys(), key=lambda e: -elos[e])
    print(f"{'Engine':<33} {'RR Elo':>6} {'PhB':>5} {'Δ':>5}  {'opp':>3} {'W':>3} {'D':>3} {'L':>3}  {'%':>5}")
    print("-" * 86)
    for e in ranked:
        w, d, l, opp = per_engine_record(results, e)
        g = w + d + l
        pct = 100 * (w + 0.5 * d) / g if g else 0
        pb = PHASE_B.get(e, "?")
        diff = round(elos[e] - pb) if isinstance(pb, int) else "?"
        ds = f"{diff:+d}" if isinstance(diff, int) else "  ?"
        print(f"  {e:<31} {round(elos[e]):>5}  {pb:>4}  {ds:>4}    {opp:>2}  {w:>2}  {d:>2}  {l:>2}   {pct:>4.1f}")
    p, s, n = correlations(elos, PHASE_B)
    print(f"\n  Pearson r  (RR vs PhB, n={n}) : {p:.3f}")
    print(f"  Spearman ρ (RR vs PhB, n={n}) : {s:.3f}")
    print(f"  Total games: {sum(sum(sum(wdl) for wdl in row.values()) for row in results.values()) // 2}")
