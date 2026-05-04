"""Unified Bradley-Terry MLE over Phase B + round-robin games.

Pools every game between every pair of engines (anchor or corpus) at
TC=120+1 into one Bradley-Terry log-likelihood. Multiple anchor nodes
are held FIXED at their known Elo (Rustic CCRL 1820, Asymptote CCRL
2150, Stockfish Skill levels from Phase A calibration); free engine
nodes are solved by Newton-Raphson. Per-engine CIs from a paired-game
bootstrap.

Why this is better than per-anchor IV-combine + separate RR:
  - Saturated anchor pairs contribute *no* signal in the IV-combine
    (they get bounds, not measurements). In BT they constrain the MLE
    one-sidedly: a 0/9 vs Rustic still says "this engine is at most
    Rustic's Elo minus a few hundred", which propagates to every
    other estimate via shared opponents.
  - Per-engine evidence aggregates over BOTH anchor pairs AND corpus
    pairs. chess-purec (4 of 5 anchors saturated) goes from "1 measurable
    anchor + 23 corpus opponents" instead of "1 measurable anchor".
  - Multi-anchor pin removes the chess-rust-cc-redo dependency: now
    the Elo scale is anchored to 5+ external rating points
    simultaneously.

Output:
  results/combined_bt_summary.md
"""
from __future__ import annotations
import json, math, random, re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Anchor nodes with FIXED Elo (constrain the MLE absolute scale).
ANCHORS_FIXED = {
    "rustic":     1820.0,  # CCRL 40/4 published
    "asymptote":  2150.0,  # CCRL 40/4 published
    "sf_skill0":   900.0,  # Phase A bound (<1229 vs Rustic 1820)
    "sf_skill5":  1658.0,  # Phase A measured
    "sf_skill10": 2004.0,  # Phase A measured
    "sf_skill15": 2325.0,  # Phase A measured
}


def parse_all_pgns() -> dict[tuple[str, str], list[float]]:
    """Returns {(A, B): [score_for_A_per_game]} for all pairs in pgn/anchor + pgn/rr.

    Per-game score: 1.0 if A won, 0.5 if drawn, 0.0 if A lost. Each game
    appears once with the pair canonically ordered (A < B alphabetically)
    and the score expressed from A's perspective.
    """
    games: dict[tuple[str, str], list[float]] = defaultdict(list)
    pgn_paths = list((ROOT / "pgn" / "anchor").glob("*.pgn")) + list((ROOT / "pgn" / "rr").glob("*.pgn"))
    # Include any pgn/anchor.<label>/ subdirectories (post-retry / experimental engines)
    for sub in (ROOT / "pgn").iterdir():
        if sub.is_dir() and sub.name.startswith("anchor."):
            pgn_paths.extend(sub.glob("*.pgn"))
    for pgn in pgn_paths:
        text = pgn.read_text(errors="ignore")
        for g in re.split(r'(?=^\[Event ")', text, flags=re.M):
            if not g.strip(): continue
            wm = re.search(r'\[White "([^"]+)"', g)
            bm = re.search(r'\[Black "([^"]+)"', g)
            rm = re.search(r'\[Result "([^"]+)"', g)
            if not (wm and bm and rm): continue
            W, B, R = wm.group(1), bm.group(1), rm.group(1)
            if W == B: continue
            # Canonical pair order
            A_eng, B_eng = sorted([W, B])
            if R == "1-0":
                score_W = 1.0
            elif R == "0-1":
                score_W = 0.0
            elif R == "1/2-1/2":
                score_W = 0.5
            else:
                continue
            score_for_A = score_W if A_eng == W else (1.0 - score_W)
            games[(A_eng, B_eng)].append(score_for_A)
    return games


def fit_bt(games: dict[tuple[str, str], list[float]],
           anchors: dict[str, float] = ANCHORS_FIXED,
           n_iter: int = 800, damping: float = 0.4) -> dict[str, float]:
    """Newton-Raphson Bradley-Terry MLE with anchor nodes pinned."""
    nodes = set()
    for A, B in games: nodes.add(A); nodes.add(B)
    nodes |= set(anchors)
    elos = {n: anchors.get(n, 1500.0) for n in nodes}

    for it in range(n_iter):
        grad = defaultdict(float)
        hess = defaultdict(float)
        for (A, B), per_game in games.items():
            n = len(per_game)
            if n == 0: continue
            score_A = sum(per_game)
            ea = 1.0 / (1.0 + 10 ** ((elos[B] - elos[A]) / 400.0))
            grad[A] += (score_A - n * ea)
            grad[B] -= (score_A - n * ea)
            h = n * ea * (1 - ea)
            hess[A] += h; hess[B] += h
        # Newton step (skip anchors)
        for n in nodes:
            if n in anchors: continue
            if hess[n] > 1e-9:
                elos[n] += (400.0 / math.log(10)) * grad[n] / hess[n] * damping
    return elos


def bootstrap_cis(games, anchors, n_boot=200, seed=20260502):
    """Resample games per pair (with replacement), refit, return per-engine ±95% CI."""
    rng = random.Random(seed)
    elos_per_engine = defaultdict(list)
    for b in range(n_boot):
        boot_games = {}
        for pair, per_game in games.items():
            n = len(per_game)
            if n == 0: continue
            sampled = [per_game[rng.randrange(n)] for _ in range(n)]
            boot_games[pair] = sampled
        # Light fit (200 iter is enough on already-good init)
        elos = fit_bt(boot_games, anchors, n_iter=200, damping=0.4)
        for eng, e in elos.items():
            if eng not in anchors:
                elos_per_engine[eng].append(e)
    cis = {}
    for eng, samples in elos_per_engine.items():
        samples.sort()
        lo = samples[int(0.025 * len(samples))]
        hi = samples[int(0.975 * len(samples))]
        cis[eng] = (hi - lo) / 2  # half-width ≈ ±95%
    return cis


# Reference numbers for comparison
PHASE_B = {  # inverse-variance combined, from earlier scoring
    "chess-java-cc": (2096, 132),
    "chess-rust-cc-redo": (1989, 105),
    "chess-rust-cc": (1841, 99),
    "chess-rust-codex": (1723, 103),
    "cplusplus-chess": (1709, 111),
    "chess-cplusplus-claude": (1680, 103),
    "chess-why3-cc": (1618, 163),
    "chess-java": (1509, 131),
    "chess-Rocq": (1499, 171),
    "chess-purec": (1440, 193),
    "chess-assembly-codex": (1403, 196),
    "chess-revisit-java-toRust-codex": (1922, 106),
    "chess-newlang-codex": (1758, 143),
    "chess-icon-codex": (1008, 248),
    "chess-apl-codex54": (709, 248),
    "chess-brainfuck": (1392, 136),
    "chess-sql": (518, 248),
}
RR = {
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
    "chess-latex-codex-replication": 1207,
}


def main():
    print("Parsing PGNs ...")
    games = parse_all_pgns()
    n_pairs = len(games)
    n_games = sum(len(v) for v in games.values())
    print(f"  Total pairs: {n_pairs}")
    print(f"  Total games: {n_games}")
    print()
    print("Fitting unified BT MLE ...")
    elos = fit_bt(games, ANCHORS_FIXED)
    print("Bootstrapping CIs (200 resamples) ...")
    cis = bootstrap_cis(games, ANCHORS_FIXED, n_boot=200)

    nodes = sorted([n for n in elos if n not in ANCHORS_FIXED], key=lambda n: -elos[n])
    md = ["# Unified Bradley-Terry Elo: Phase B + round-robin pooled",
          "",
          f"BT MLE over **{n_games:,} games** across **{n_pairs} unique pairs**, "
          "anchored simultaneously to Rustic (1820), Asymptote (2150), and "
          "Stockfish Skill 0/5/10/15 (Phase A calibration). All games at TC=120+1.",
          "",
          "Per-engine CIs from a paired-game bootstrap (n=200 resamples).",
          "",
          "| Engine | **BT Elo** | ±95% CI | Phase B | RR | Δ(BT − Phase B) | Δ(BT − RR) |",
          "|---|---:|---:|---:|---:|---:|---:|"]
    for n in nodes:
        e = round(elos[n])
        ci = round(cis.get(n, 0))
        pb = PHASE_B.get(n)
        rr = RR.get(n)
        pb_s = f"{pb[0]} ± {pb[1]}" if pb else "—"
        rr_s = str(rr) if rr is not None else "—"
        d_pb = f"{e - pb[0]:+d}" if pb else "—"
        d_rr = f"{e - rr:+d}" if rr is not None else "—"
        md.append(f"| `{n}` | **{e}** | ±{ci} | {pb_s} | {rr_s} | {d_pb} | {d_rr} |")
    out = ROOT / "results" / "combined_bt_summary.md"
    out.write_text("\n".join(md) + "\n")
    print(f"\nWrote {out}")
    print(f"\nTop 5 by BT Elo:")
    for n in nodes[:8]:
        print(f"  {n:<35} {round(elos[n]):>5} ± {round(cis.get(n, 0)):>3}")


if __name__ == "__main__":
    main()
