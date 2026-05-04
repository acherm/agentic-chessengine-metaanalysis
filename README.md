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

## The 34 engine repositories

Each engine analysed in this study is released as its own public
repository under the [`acherm`](https://github.com/acherm) account,
following the naming convention
`agentic-chessengine-<lang>[-<agent>][-<variant>]`. Each repo carries
an MIT licence, a per-language `.gitignore`, and a `README.md` naming
the primary coding agent (`-cc` = Claude Code, Opus 4.6 / 4.7;
`-codex` = Codex, GPT-5-codex, with one APL run on GPT-5.4).
`-from-<lang>-codex` marks an agent-driven port from another language;
`-codexfailure` flags a session that failed to reach a playable engine
and is preserved as a negative result.

| # | Local folder | Language | Agent | GitHub repo |
|--:|---|---|---|---|
|  1 | `chess-apl-codex54` | APL | Codex | [`agentic-chessengine-apl-codex`](https://github.com/acherm/agentic-chessengine-apl-codex) |
|  2 | `chess-assembly-codex` | x86-64 Asm | Codex | [`agentic-chessengine-assembly-codex`](https://github.com/acherm/agentic-chessengine-assembly-codex) |
|  3 | `chess-brainfuck` | Brainfuck (failure) | Codex | [`agentic-chessengine-brainfuck-codexfailure`](https://github.com/acherm/agentic-chessengine-brainfuck-codexfailure) |
|  4 | `chess-brainfuck-cc` | Brainfuck | Claude Code | [`agentic-chessengine-brainfuck`](https://github.com/acherm/agentic-chessengine-brainfuck) |
|  5 | `chess-cobol-cc` | COBOL | Claude Code | [`agentic-chessengine-cobol-cc`](https://github.com/acherm/agentic-chessengine-cobol-cc) |
|  6 | `COBOL-chess` | COBOL | Codex | [`agentic-chessengine-cobol-codex`](https://github.com/acherm/agentic-chessengine-cobol-codex) |
|  7 | `chess-cplusplus-claude` | C++ | Claude Code | [`agentic-chessengine-cpp-cc`](https://github.com/acherm/agentic-chessengine-cpp-cc) |
|  8 | `cplusplus-chess` | C++ | Codex | [`agentic-chessengine-cpp-codex`](https://github.com/acherm/agentic-chessengine-cpp-codex) |
|  9 | `chess-css-codex` | CSS/HTML (evasion) | Codex | [`agentic-chessengine-css-codex`](https://github.com/acherm/agentic-chessengine-css-codex) |
| 10 | `chess-css-codex-guided` | CSS/HTML (strict) | Codex | [`agentic-chessengine-css-codex-guided`](https://github.com/acherm/agentic-chessengine-css-codex-guided) |
| 11 | `chess-icon-codex` | Icon | Codex | [`agentic-chessengine-icon-codex`](https://github.com/acherm/agentic-chessengine-icon-codex) |
| 12 | `chess-java` | Java | Codex | [`agentic-chessengine-java-codex`](https://github.com/acherm/agentic-chessengine-java-codex) |
| 13 | `chess-java-cc` | Java | Claude Code | [`agentic-chessengine-java-cc`](https://github.com/acherm/agentic-chessengine-java-cc) |
| 14 | `chess-latex-codex-replication` | LaTeX (expl3) | Codex | [`agentic-chessengine-latex-codex-replication`](https://github.com/acherm/agentic-chessengine-latex-codex-replication) |
| 15 | `latex-chess-engine` | TeX | Codex | [`agentic-chessengine-latex-TeXCCChess`](https://github.com/acherm/agentic-chessengine-latex-TeXCCChess) |
| 16 | `lean-chess` | Lean 4 | Codex | [`agentic-chessengine-lean-codex`](https://github.com/acherm/agentic-chessengine-lean-codex) |
| 17 | `chess-mojo` | Mojo (failure) | Codex | [`agentic-chessengine-mojo-codexfailure`](https://github.com/acherm/agentic-chessengine-mojo-codexfailure) |
| 18 | `chess-newlang-codex` | C++/GAMBIT DSL | Codex | [`agentic-chessengine-dsl-newlang-codex`](https://github.com/acherm/agentic-chessengine-dsl-newlang-codex) |
| 19 | `chess-purec` | C | Claude Code | [`agentic-chessengine-c-cc`](https://github.com/acherm/agentic-chessengine-c-cc) |
| 20 | `chess-purec-codex` | C | Codex | [`agentic-chessengine-c-codex`](https://github.com/acherm/agentic-chessengine-c-codex) |
| 21 | `chess-py` | Python | Codex | [`agentic-chessengine-python-codex`](https://github.com/acherm/agentic-chessengine-python-codex) |
| 22 | `chess-py-cc` | Python | Claude Code | [`agentic-chessengine-python-cc`](https://github.com/acherm/agentic-chessengine-python-cc) |
| 23 | `chess-revisit-java-toRust-codex` | Rust (port from Java) | Codex | [`agentic-chessengine-rust-from-java-codex`](https://github.com/acherm/agentic-chessengine-rust-from-java-codex) |
| 24 | `chess-Rocq` | Rocq → OCaml | Claude Code | [`agentic-chessengine-rocq-cc`](https://github.com/acherm/agentic-chessengine-rocq-cc) |
| 25 | `chess-ruby-cc` | Ruby | Claude Code | [`agentic-chessengine-ruby-cc`](https://github.com/acherm/agentic-chessengine-ruby-cc) |
| 26 | `chess-ruby-codex` | Ruby | Codex | [`agentic-chessengine-ruby-codex`](https://github.com/acherm/agentic-chessengine-ruby-codex) |
| 27 | `chess-rust-cc` | Rust | Claude Code | [`agentic-chessengine-rust-cc`](https://github.com/acherm/agentic-chessengine-rust-cc) |
| 28 | `chess-rust-cc-redo` | Rust | Claude Code | [`agentic-chessengine-rust-cc-redo`](https://github.com/acherm/agentic-chessengine-rust-cc-redo) |
| 29 | `chess-rust-codex` | Rust | Codex | [`agentic-chessengine-rust-codex`](https://github.com/acherm/agentic-chessengine-rust-codex) |
| 30 | `chess-sql` | SQL | Claude Code | [`agentic-chessengine-sql-cc`](https://github.com/acherm/agentic-chessengine-sql-cc) |
| 31 | `chess-why3` | Why3 → OCaml | Codex | [`agentic-chessengine-why3-codex`](https://github.com/acherm/agentic-chessengine-why3-codex) |
| 32 | `chess-why3-cc` | Why3 → C | Claude Code | [`agentic-chessengine-why3-cc`](https://github.com/acherm/agentic-chessengine-why3-cc) |
| 33 | `test-superset` | CSS + minimal JS | Claude Code | [`agentic-chessengine-css-ChessCSS`](https://github.com/acherm/agentic-chessengine-css-ChessCSS) |
| 34 | `chess-revisit-java-toCOBOL-codex` † | COBOL (port from Java) | Codex | [`agentic-chessengine-cobol-from-java-codex`](https://github.com/acherm/agentic-chessengine-cobol-from-java-codex) |

† Materialised from the sub-folder `chess-revisit-java-toCOBOL/` inside
the Rust port working tree (#23) into its own SANDBOX directory before
release.

## License

No license specified yet — pending finalisation alongside the
accompanying paper. Contact the author before redistributing or
relying on this material.
