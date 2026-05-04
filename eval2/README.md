# eval2 — canonical chess-engine evaluation harness

A reproducible, container-isolated protocol producing a single Elo
estimate per agent-built engine, plus functional-correctness
diagnostics, plus a tactical-suite signal. Replaces `../eval/`.

## What's in scope

- 28 main-corpus engines listed in `manifest.yaml` (`corpus: main`).
- 3 special-role engines (ports + DSL) reported separately.
- 3 external CCRL anchor engines: TSCP 1.81 (~1750), MadChess 3.2 (~2200),
  CounterGo 4.0 (~2400).
- Stockfish 16.1, pinned in Docker, used as the calibrated UCI_Elo ladder.

## Locked design decisions

| Knob | Choice | Rationale |
|---|---|---|
| Stockfish | **16.1**, in Docker | last release with widely-cited UCI_Elo curve against CCRL 40/4 |
| Time-control anchor | **120+1** (CCRL 40/4) | matches what UCI_LimitStrength is tuned for |
| Containerization | Docker per engine + per anchor | reproducibility; clean process-tree kills |
| Calibration | SF-vs-SF + SF-vs-3 anchors | one ladder isn't enough; cross-check with known-Elo engines |
| Tactics | WAC-100 + mate-in-2 | complement, especially for Tier-C engines where game-Elo is bounded |
| Compute budget | ~3 days, 1 machine | two-pass strategy (fast bracket → focused 120+1) makes it fit |
| Slow engines | own tier with `st=30s/60s` and reduced ladder | LaTeX/SQL/BF can't honor 120+1 |

See `../.claude/.../memory/project_eval2_design.md` for the standing
record.

## Five phases (and what they cost)

| # | Phase | Wall-time (est.) | Output |
|---|---|---:|---|
| 0 | Build all images | ~3 h | `eval2/<image>:tag` for SF + 3 anchors + 28 engines |
| 1 | Preflight gate (UCI / perft / illegal-move audit / WAC-100) | ~3 h | `results/per_engine/<name>.preflight.*.json` |
| 2 | Calibration (SF-vs-SF + SF-vs-anchors) | ~6 h | `pgn/calibration/`, calibration warnings |
| 3a | Pass-1 bracket (30+0.3, full ladder, SPRT) | ~12 h | `pgn/pass1/`; rough Elo per engine |
| 3b | Pass-2 focused (120+1, ±2 rungs, SPRT) | ~20 h | `pgn/pass2/`; calibrated Elo per engine |
| 4 | Within-tier round-robin (60+0.6) | ~12 h | `pgn/rr/`; cross-engine ranking |
| 5 | Slow battery (Tier C only, st=30s/60s) | ~6 h | `pgn/slow/`; bounded Elo + tactic % |
| | **Total** | **~62 h** | + buffer for re-runs |

## Directory layout

```
eval2/
├── README.md                    this file
├── manifest.yaml                engines + tier + image (the source of truth)
├── ladder.json                  SF rungs + per-tier TC + phase budgets
├── docker/
│   ├── stockfish/               SF 16.1 image
│   ├── anchors/{tscp,madchess,countergo}/
│   └── engines/<name>/          one Dockerfile per engine
├── preflight/
│   ├── uci_handshake.py
│   ├── perft_audit.py           native perft when available; else replay-and-validate
│   └── tactics.py
├── lib/
│   ├── manifest.py              YAML-lite parser (no PyYAML dep)
│   ├── docker_engine.py         compose `docker run` cutechess commands
│   ├── sprt.py                  SPRT early-stop
│   ├── score.py                 PGN → Elo (IV + per-rung)
│   └── random_mover.py          baseline UCI engine (uses python-chess)
├── runners/
│   ├── build_images.sh          phase 0
│   ├── run_preflight.sh         phase 1
│   ├── run_calibration.sh       phase 2
│   ├── run_pass1_bracket.sh     phase 3a
│   ├── run_pass2_focused.sh     phase 3b
│   ├── run_tier_rr.sh           phase 4
│   ├── run_slow_battery.sh      phase 5
│   └── score_all.sh             rebuild SUMMARY.md from current PGNs
├── fixtures/
│   ├── openings.epd             20 opening positions (copied from eval/)
│   ├── perft_suite.epd          startpos + Kiwipete + 4 CPW positions
│   ├── wac100.epd               Win-At-Chess subset (stub; populate)
│   └── mate_in_2.epd            mate-in-2 set (stub; populate)
├── pgn/                         all PGNs (gitignore)
├── logs/                        cutechess + container logs
└── results/
    ├── per_engine/<name>.card.json
    ├── per_engine/<name>.preflight.*.json
    ├── calibration.json
    ├── missing_dockerfiles.txt
    └── SUMMARY.md
```

## Reproducing the run

Prerequisites on the host:
- `docker` (the harness only ever invokes engines via `docker run`).
- `cutechess-cli` (>= 1.2).
- Python 3.10+.
- `python-chess` on the host (used by random-mover and external legal-move audit only).

End-to-end:

```bash
cd ~/SANDBOX/chess-meta-analysis/eval2

# Phase 0: build everything (one-off; ~3 h)
./runners/build_images.sh

# Phase 1: preflight gate
./runners/run_preflight.sh

# Phase 2: calibration
./runners/run_calibration.sh

# Phase 3a: bracket pass (run overnight if possible)
./runners/run_pass1_bracket.sh

# Phase 3b: focused pass (REQUIRES low background load — accurate timing)
./runners/run_pass2_focused.sh

# Phase 4: tier round-robins
./runners/run_tier_rr.sh

# Phase 5: slow battery
./runners/run_slow_battery.sh

# Re-score whenever PGNs change
./runners/score_all.sh
```

Each runner is idempotent — re-running skips pairings whose PGN already
has games. Crash recovery is just re-running.

## Reading the results

- `results/SUMMARY.md` — the headline table: Elo (IV agg.) + 95% CI +
  preflight pass/fail + WAC %.
- `results/per_engine/<name>.card.json` — full per-engine card.
- `results/calibration.json` — anchor-vs-SF deltas; ⚠ if any anchor
  lands >50 Elo from CCRL nominal.

## Functional-correctness reading

The preflight gate doubles as a correctness oracle. An engine whose
`preflight_perft_ok = false` but headline Elo is high should be
manually inspected — it's likely cheating (e.g., shipping illegal
moves Stockfish auto-loses to) or timing-control exploiting.

## Known limitations / threats

1. **`UCI_LimitStrength` is non-monotone in extremes.** Phase 2
   detects it; flagged anchors mean the Elo numbers near that rung
   should carry a footnote.
2. **Hardware sensitivity at 120+1.** Run Pass-2 on an unloaded box.
   Hardware fingerprint is recorded in each card.
3. **Some engines need licensed runtimes** (Dyalog APL, Mojo). Their
   Dockerfiles are not yet written; they will land in
   `results/missing_dockerfiles.txt` and need manual attention.
4. **Tier C is bounded, not point-estimated.** The slow battery yields
   "between random and SF1000" for engines that can't honor real TCs.
5. **Anchor sources are GitHub `master` at build time.** The Dockerfiles
   pin to a tag, but transitively-fetched dependencies aren't pinned.
   If anchor calibration drifts on rebuild, that's why.

## Differences from old `../eval/`

- Real YAML manifest with **tier classification**.
- All engines run in Docker (old harness ran on host).
- **External anchor engines** for cross-validating SF UCI_Elo.
- **Preflight gate** kills broken engines before they pollute the ladder.
- **Two-pass** (fast bracket + focused 120+1) instead of single 200-game ladder.
- **SPRT early-stop** at every pairing.
- **Tier-C special protocol** instead of `notes:` warnings.
- **Tactical suite** (WAC + mate-in-2) as a first-class metric.
