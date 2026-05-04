"""Compile the Q2 self-reproduction results into a per-engine summary.

For each engine in pgn/self_repro/, parse all PGNs, compute a per-rung
score and Elo estimate using the exact opponent-Elo label the agent
themselves used (UCI_LimitStrength label OR Skill-Level effective Elo
from Phase A), aggregate via inverse-variance, and report alongside:
  - the engine's own self-claim
  - our anchor-based Elo
  - the round-robin Elo
  - the original methodology configuration (TC, hash, opponent set)

Output: results/self_repro_summary.md
"""
from __future__ import annotations
import json, math, re, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SF_SKILL_ELO = {0: 600, 5: 1658, 7: 1818, 10: 2004, 12: 2150, 14: 2245, 15: 2325, 20: 2750}
# (5/10/15 measured in Phase A; others linearly interpolated)


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
        if R == "1-0":
            if W == engine: w += 1
            else: l += 1
        elif R == "0-1":
            if B == engine: w += 1
            else: l += 1
        elif R == "1/2-1/2":
            d += 1
    return w, d, l


def pair_files(engine: str):
    """Yield (opp_name, opp_elo_label, pgn_path)."""
    for f in sorted((ROOT / "pgn" / "self_repro").glob(f"{engine}_vs_*.pgn")):
        m = re.match(rf"{re.escape(engine)}_vs_(sf_(?:e|sk)\d+)\.pgn$", f.name)
        if not m: continue
        opp = m.group(1)
        if opp.startswith("sf_e"):
            elo = int(opp[4:])
        else:
            sk = int(opp[5:])
            elo = SF_SKILL_ELO.get(sk, 1500 + 100 * sk)  # fallback linear
        yield opp, elo, f


def score_engine(engine: str):
    pairs = []
    raw = []
    for opp, elo, pgn in pair_files(engine):
        w, d, l = parse_pgn(pgn, engine)
        n = w + d + l
        if n == 0: continue
        s = (w + 0.5 * d) / n
        raw.append({"opp": opp, "opp_elo": elo, "w": w, "d": d, "l": l, "score_pct": 100*s})
        if 0 < s < 1:
            ediff = 400 * math.log10(s / (1 - s))
            est = elo + ediff
            se = 400 / (n ** 0.5)
            pairs.append((est, se))
    if not pairs:
        return {"elo": None, "ci": None, "raw": raw}
    weights = [1 / (s ** 2) for _, s in pairs]
    total = sum(weights)
    elo = sum(e * w for (e, _), w in zip(pairs, weights)) / total
    se = (1 / total) ** 0.5
    return {"elo": round(elo), "ci": round(1.96 * se), "raw": raw}


# Reference numbers (anchor + RR + self-claim) — keep in sync with
# tab_elo / EVAL2_FINDINGS.md.
ANCHOR = {
    "chess-purec": (1440, 193), "chess-purec-codex": (1504, 160),
    "chess-rust-cc": (1841, 99), "chess-rust-cc-redo": (2023, 100),
    "chess-rust-codex": (1756, 103), "chess-cplusplus-claude": (1675, 103),
    "cplusplus-chess": (1660, 111), "chess-java-cc": (2071, 95),
    "chess-ruby-cc": (1719, 110), "chess-why3-cc": (1598, 163),
    "chess-Rocq": (1499, 171), "chess-assembly-codex": (1403, 196),
}
RR = {
    "chess-purec": 1645, "chess-purec-codex": 1555, "chess-rust-cc": 1882,
    "chess-rust-cc-redo": 1989, "chess-rust-codex": 1801,
    "chess-cplusplus-claude": 1816, "cplusplus-chess": 1686,
    "chess-java-cc": 2050, "chess-ruby-cc": 1816, "chess-why3-cc": 1714,
    "chess-Rocq": 1481, "chess-assembly-codex": 1631,
}
SELF_CLAIM = {
    "chess-purec": "1997", "chess-purec-codex": "1670–1972",
    "chess-rust-cc": "2110", "chess-rust-cc-redo": "1879",
    "chess-rust-codex": "2043", "chess-cplusplus-claude": "1897",
    "cplusplus-chess": "2087", "chess-java-cc": "2212",
    "chess-ruby-cc": "1840", "chess-why3-cc": "1882",
    "chess-Rocq": "1500", "chess-assembly-codex": "2481",
}


def main():
    rows = []
    for f in sorted((ROOT / "pgn" / "self_repro").iterdir()):
        if not f.is_dir(): continue
    # We don't have subdirs; collect engine names from PGNs
    engines = sorted({re.match(r"^(.+?)_vs_sf_(?:e|sk)\d+\.pgn$", p.name).group(1)
                      for p in (ROOT / "pgn" / "self_repro").glob("*.pgn")
                      if re.match(r"^(.+?)_vs_sf_(?:e|sk)\d+\.pgn$", p.name)})
    print(f"engines with self-repro PGNs: {len(engines)}\n")
    rows = []
    for e in engines:
        r = score_engine(e)
        rows.append({"engine": e, **r})

    # Emit a markdown summary
    md = ["# Q2 self-reproduction summary (host-native, original methodology)", "",
          "Each engine was run on host hardware against host Stockfish 18, "
          "using the *engine's own original* opponent set (UCI_Elo rungs or "
          "SF Skill levels), original TC, and original Hash size (per "
          "`runners/self_reproduction.yaml`). The `Repro` column is the "
          "Elo we measure under the engine's own methodology; the `Anchor` "
          "and `RR` columns are the rigorous measurements.",
          "",
          "| Engine | Self-claim | **Repro** | Anchor (Phase B) | RR | Δ self vs anchor | Δ self vs repro |",
          "|---|---|---:|---:|---:|---:|---:|"]
    for r in rows:
        e = r["engine"]
        repro = f"{r['elo']} ± {r['ci']}" if r["elo"] is not None else "—"
        anc = f"{ANCHOR[e][0]} ± {ANCHOR[e][1]}" if e in ANCHOR else "—"
        rr = str(RR[e]) if e in RR else "—"
        sc = SELF_CLAIM.get(e, "—")
        # Δ self vs anchor (mid-band for self if needed)
        try:
            sc_mid = sum(int(x) for x in sc.replace("–","-").split("-"))/sc.count("-",0,len(sc.replace("–","-"))) if "-" in sc.replace("–","-") else int(sc)
            da = ANCHOR[e][0] - sc_mid if e in ANCHOR else None
            dr = (r["elo"] - sc_mid) if (r["elo"] is not None and sc_mid is not None) else None
        except Exception:
            da = dr = None
        md.append(f"| `{e}` | {sc} | **{repro}** | {anc} | {rr} | "
                  f"{('%+d' % round(da)) if da is not None else '—'} | "
                  f"{('%+d' % round(dr)) if dr is not None else '—'} |")
    md.append("")
    md.append("## Per-rung scores (Stockfish opponent strength is the agent's own label)")
    md.append("")
    for r in rows:
        if not r["raw"]: continue
        md.append(f"### `{r['engine']}` (repro: {r['elo']} ± {r['ci']} from rungs)")
        md.append("")
        md.append("| Opponent | Opp Elo | W | D | L | Score% |")
        md.append("|---|---:|---:|---:|---:|---:|")
        for x in r["raw"]:
            md.append(f"| {x['opp']} | {x['opp_elo']} | {x['w']} | {x['d']} | {x['l']} | {x['score_pct']:.0f}% |")
        md.append("")

    out = ROOT / "results" / "self_repro_summary.md"
    out.write_text("\n".join(md) + "\n")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
