# Agentic chess-engine meta-analysis

Scripts and analysis material for an empirical study of chess-engine
projects built with frontier coding agents (Claude Code, Codex) across
many programming languages. The accompanying paper is in preparation.

## What's here

```
.
├── README.md                 — this file
├── scripts/                  — Python analysis toolkit (stdlib only) for the
│                               first-pass session/prompt/feature extraction
├── eval2/                    — independent strength-evaluation harness
│   ├── lib/                  — scoring scripts (anchor IV-combine, round-robin
│   │                           Bradley-Terry MLE, unified BT MLE pooled across
│   │                           streams, Phase A SF-Skill calibration, …)
│   ├── runners/              — shell drivers for the gauntlet, round-robin,
│   │                           targeted-skill anchor passes, retry experiment
│   ├── docker/               — pinned-binary anchor and engine images
│   ├── manifest.yaml         — engine registry consumed by the runners
│   ├── pgn/                  — game records (anchor matches + round-robin)
│   ├── results/              — Markdown summaries + per-run JSONs
│   └── scripts/              — feature/algorithm inventory, NPS bench, plot
├── data/                     — extracted aggregates
│   ├── overview.json         — one row per project
│   ├── synthesis.json        — aggregate totals + classification
│   ├── novelty.json          — engine-vs-canonical novelty audit
│   ├── elo.json              — strength evidence
│   ├── se_capabilities.json  — software-engineering activity matrix
│   └── projects/             — per-project session JSONs
└── reports/
    ├── EVAL2_FINDINGS.md     — current findings (latest)
    ├── SYNTHESIS.md          — earlier synthesis pass
    ├── OVERVIEW.md           — corpus summary table
    └── projects/             — per-project Markdown dossiers
```

`reports/EVAL2_FINDINGS.md` is the most recent integrated narrative;
sections 19 and 20 cover the chess-purec retry experiment (n=1 causal
test of the broken-reward-signal hypothesis) and the unified
Bradley-Terry MLE that pools every game played at TC=120s+1s.

## Reproduce

The first-pass extraction toolkit is Python 3.10+ stdlib only:

```bash
python3 scripts/discover.py            # corpus discovery, ~2-3 min
python3 scripts/per_project_report.py  # per-project Markdown + JSON
python3 scripts/elo_and_perft.py       # gameplay evidence
python3 scripts/synthesis.py           # cross-project synthesis
```

It reads `~/SANDBOX/chess-*` engine folders plus the local Claude Code
and Codex session caches (`~/.claude/projects/...`,
`~/.codex/sessions/...`). On a different host you would point
`scripts/common.py:DATA_PATHS` at your own session cache.

The strength-evaluation harness (`eval2/`) requires Docker (for pinned
anchor binaries: Stockfish 18, Rustic Alpha 3.0.4, Asymptote 0.7) and
`cutechess-cli`. From `eval2/`:

```bash
./runners/run_phaseA_sf_calibration.sh   # SF Skill -> Elo on this hardware
./runners/run_anchor_gauntlet.sh         # 5-anchor SPRT-capped per engine
./runners/run_round_robin.sh             # 26-engine head-to-head
./runners/run_targeted_skills.sh         # information-region anchor pass
python3 lib/score_combined_bt.py         # unified BT MLE -> results/
```

The engine paths in `eval2/manifest.yaml` are absolute and point at the
authors' working tree; on a different host they would need to be
updated to match the local layout.

## Headline observations (from `reports/EVAL2_FINDINGS.md`)

- 34 agent-built chess engines were studied (29 main-corpus +
  5 special-role experiments) across 15 primary programming
  languages.
- Top-tier engines reach ~2000-2100 Elo on a CCRL-anchored
  TC=120s+1s harness (chess-java-cc, chess-rust-cc-redo, the
  Codex Java→Rust port).
- Most agents over-state their own engine's Elo by 200-1100
  Elo, traceable to using `UCI_LimitStrength` as a calibrated
  ladder (it is not, on the modern hardware where the agents
  measured).
- A single n=1 retry experiment, holding the engine source and
  the model fixed and only swapping the in-loop reward signal
  for an anchored match, recovered +383 Elo in 30 prompts at
  ~$0.08 per Elo — supporting the broken-reward-signal
  hypothesis pending replication on additional engines.

## Reading conventions

`[R:<project>]` repo folder · `[T:<project>/<agent>]` session log ·
`[G:<hash>]` git commit · `[L:run_<n>]` command output ·
`[S:scan]` statistic from one of the scripts.

## Limitations

- Many older Claude Code transcripts have been archived; where only
  subagent logs remain, prompt/token counts under-report user-driven
  interaction.
- Cost is a list-price estimate; real spend depends on tier discounts
  and cache-hit rates we could not fully reconstruct.
- Feature detection is regex-based and can under-detect engines
  written in unusual languages (Brainfuck, APL, raw assembly).
- The Stockfish-Skill-to-Elo calibration in Phase A is hardware-dependent;
  re-running on a different host requires re-doing Phase A.

## License

No license specified yet — pending finalisation alongside the
accompanying paper. Contact the author before redistributing or
relying on this material.

## Citation

Companion paper in preparation. Until then, cite as:

> Acher M., *Agent-built chess engines: a polyglot meta-analysis*.
> Manuscript in preparation, 2026.
