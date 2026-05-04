# Chess meta-analysis — synthesis for the paper

_Generated 2026-04-22 14:52 UTC._

This document synthesizes evidence across **57 chess-related folders** under `~/SANDBOX`, of which **29 are agent-built chess engines** (plus 0 engine *variants* on non-standard boards). The remainder are tournament runners, training-research repos, meta-studies, prototypes, or external corpora, tagged ``oos-…'' and documented in `FOLDER_TRIAGE.md`.

## Headline numbers

- **Corpus:** 57 chess-related folders under `~/SANDBOX` (excluding `chess-meta-analysis`).
- **Engines in scope:** 29 (language × agent combinations).
- **LOC** (engines only, excluding external corpora): ~416,338 lines across engines; ~2,902,261 total if we include studies/tools.
- **User prompts logged** across all sessions: 1440 (468 on engines).
- **Sessions** (Claude Code + Codex, main transcripts): 71.
- **Estimated agent spend:** $4,965.72 total, $2,148.16 on engines (list-price estimate).

_Token counts and pricing tables are in `scripts/common.py::PRICING_USD_PER_MTOK`; Anthropic and OpenAI discounts are not applied._

## Engine corpus (by language × agent × period)

| Project | Language | Agent | Model family | Period | Files | LOC | Prompts | USD | PGN | Perft hits |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|
| [chess-apl-codex54](projects/chess-apl-codex54.md) | APL | Claude Code + Codex | Opus 4.6, gpt-5 | 2026-03-05→2026-03-20 | 10 | 3,652 | 35 | $115.74 | 0 | 0 |
| [chess-assembly-codex](projects/chess-assembly-codex.md) | Assembly | Codex | gpt-5 | 2026-02-24→2026-02-25 | 9 | 12,310 | 12 | $47.01 | 0 | 0 |
| [chess-cobol-cc](projects/chess-cobol-cc.md) | C | Claude Code | Opus 4.6 | 2026-03-12→2026-03-30 | 4 | 11,578 | 46 | $518.44 | 0 | 0 |
| [chess-purec](projects/chess-purec.md) | C | — | — | 2026-02-16→2026-02-16 | 28 | 3,158 | 0 | $0.00 | 0 | 0 |
| [chess-purec-codex](projects/chess-purec-codex.md) | C | Codex | gpt-5 | 2026-02-19→2026-02-19 | 16 | 3,095 | 4 | $15.99 | 0 | 0 |
| [chess-why3-cc](projects/chess-why3-cc.md) | C | Claude Code (by name) | — | 2026-02-18→2026-02-19 | 234 | 91,558 | 0 | $0.00 | 0 | 0 |
| [chess-cplusplus-claude](projects/chess-cplusplus-claude.md) | C++ | Claude Code (by name) | — | 2026-02-16→2026-02-18 | 28 | 4,248 | 0 | $0.00 | 0 | 0 |
| [cplusplus-chess](projects/cplusplus-chess.md) | C++ | Codex | gpt-5 | 2026-02-10→2026-02-13 | 34 | 4,420 | 16 | $81.01 | 0 | 0 |
| [COBOL-chess](projects/COBOL-chess.md) | COBOL | Claude Code + Codex | Opus 4.6, gpt-5 | 2026-02-09→2026-04-16 | 76 | 8,890 | 33 | $356.45 | 0 | 0 |
| [chess-css-codex](projects/chess-css-codex.md) | HTML | Codex | gpt-5 | 2026-02-28→2026-03-01 | 22 | 38,684 | 17 | $27.14 | 0 | 0 |
| [chess-icon-codex](projects/chess-icon-codex.md) | Icon | Codex | gpt-5 | 2026-02-23→2026-02-24 | 22 | 3,217 | 6 | $19.51 | 0 | 0 |
| [chess-java](projects/chess-java.md) | Java | Codex | gpt-5 | 2026-02-17→2026-02-18 | 22 | 2,835 | 7 | $21.85 | 0 | 0 |
| [chess-java-cc](projects/chess-java-cc.md) | Java | Claude Code | Opus 4.6 | 2026-02-17→2026-03-10 | 35 | 4,884 | 3 | $7.74 | 0 | 0 |
| [chess-css-codex-guided](projects/chess-css-codex-guided.md) | JavaScript | Codex | gpt-5 | 2026-03-01→2026-03-01 | 4 | 2,077 | 9 | $11.10 | 0 | 0 |
| [chess-latex-codex-replication](projects/chess-latex-codex-replication.md) | LaTeX | Codex | gpt-5 | 2026-02-16→2026-02-17 | 46 | 5,222 | 15 | $119.73 | 0 | 0 |
| [latex-chess-engine](projects/latex-chess-engine.md) | LaTeX | Codex | gpt-5 | 2026-02-14→2026-02-26 | 23 | 41,185 | 14 | $5.71 | 0 | 0 |
| [lean-chess](projects/lean-chess.md) | Lean | Codex | gpt-5 | 2026-02-09→2026-02-10 | 15 | 2,333 | 21 | $123.23 | 0 | 0 |
| [chess-Rocq](projects/chess-Rocq.md) | OCaml | Claude Code | Opus 4.6 | 2026-02-15→2026-04-09 | 51 | 6,335 | 4 | $4.75 | 0 | 0 |
| [chess-why3](projects/chess-why3.md) | OCaml | Codex | gpt-5 | 2026-02-17→2026-02-18 | 46 | 4,530 | 9 | $23.92 | 0 | 0 |
| [chess-brainfuck](projects/chess-brainfuck.md) | Python | Codex | gpt-5 | 2026-02-20→2026-03-23 | 56 | 6,920 | 38 | $170.78 | 0 | 0 |
| [chess-brainfuck-cc](projects/chess-brainfuck-cc.md) | Python | Claude Code + Codex | Opus 4.6, gpt-5 | 2026-02-22→2026-03-31 | 18 | 7,879 | 58 | $160.58 | 0 | 0 |
| [chess-py](projects/chess-py.md) | Python | Codex | gpt-5 | 2026-02-11→2026-02-16 | 22 | 3,890 | 10 | $29.29 | 0 | 0 |
| [chess-py-cc](projects/chess-py-cc.md) | Python | Claude Code (by name) | — | — | 22 | 2,995 | 0 | $0.00 | 0 | 0 |
| [chess-sql](projects/chess-sql.md) | Python | — | — | 2026-02-16→2026-02-16 | 15 | 2,016 | 0 | $0.00 | 0 | 0 |
| [chess-ruby-cc](projects/chess-ruby-cc.md) | Ruby | Claude Code | Opus 4.6 | 2026-03-12→2026-03-17 | 22 | 2,964 | 46 | $148.17 | 0 | 0 |
| [chess-ruby-codex](projects/chess-ruby-codex.md) | Ruby | Codex | gpt-5 | 2026-03-12→2026-03-13 | 43 | 124,443 | 7 | $60.76 | 0 | 0 |
| [chess-rust-cc](projects/chess-rust-cc.md) | Rust | Claude Code (by name) | — | 2026-02-17→2026-02-17 | 27 | 5,872 | 0 | $0.00 | 0 | 0 |
| [chess-rust-cc-redo](projects/chess-rust-cc-redo.md) | Rust | Claude Code | Sonnet 4.6 | 2026-04-19→2026-04-22 | 18 | 3,329 | 55 | $63.94 | 0 | 0 |
| [chess-rust-codex](projects/chess-rust-codex.md) | Rust | Codex | gpt-5 | 2026-02-16→2026-02-17 | 8 | 1,819 | 3 | $15.32 | 0 | 0 |

## Cross-language chess feature coverage (engines)

| Language | Projects | FEN parsing | UCI protocol | Perft | Castling | En passant | Promotion | Check/Checkmate | PGN | Board: 0x88 | Board: bitboard | Board: mailbox 8x8 | Minimax/Negamax | Alpha-beta | Iterative deepening | Quiescence | Transposition table | Zobrist hashing | Move ordering (MVV-LVA) | Killer moves | History heuristic | Principal-variation (PV) | Null-move pruning | Late-move reduction (LMR) | Late-move pruning (LMP) | Aspiration windows | Evaluation/PST | Tapered evaluation | King safety | Pawn structure | Mobility | Material counting | Opening book | Endgame tables | Time management | Board: magic bitboards | Futility pruning | Razoring | NNUE/neural eval |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| APL | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |  |  |  | 1 | 1 | 1 | 1 | 1 | 1 | 1 |  | 1 |  | 1 |  |  |  | 1 | 1 | 1 | 1 | 1 | 1 | 1 |  | 1 |  |  |  |  |
| Assembly | 1 | 1 | 1 |  | 1 |  | 1 | 1 |  |  |  | 1 |  | 1 | 1 | 1 | 1 | 1 |  |  |  | 1 | 1 |  |  | 1 |  | 1 |  | 1 |  | 1 | 1 |  | 1 |  | 1 |  |  |
| C | 4 | 4 | 4 | 3 | 4 | 3 | 4 | 4 | 3 | 1 | 2 | 2 | 4 | 3 | 4 | 4 | 4 | 3 | 3 | 4 | 4 | 4 | 3 | 4 | 2 | 4 | 2 | 4 | 2 | 4 | 3 | 4 | 3 | 2 | 4 | 2 | 3 | 2 | 1 |
| C++ | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |  | 2 |  | 1 | 1 | 1 | 2 | 2 | 2 | 2 | 1 | 1 | 2 | 2 | 1 | 1 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 1 |  | 2 | 1 | 2 | 1 |  |
| COBOL | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |  |  |  |  |
| HTML | 1 | 1 | 1 |  |  | 1 | 1 | 1 |  |  |  |  | 1 | 1 | 1 | 1 | 1 |  |  |  | 1 | 1 |  |  |  |  | 1 |  |  | 1 | 1 | 1 |  |  | 1 |  |  |  |  |
| Icon | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |  |  |  | 1 | 1 | 1 | 1 |  | 1 | 1 |  |  | 1 | 1 |  | 1 |  |  |  | 1 |  | 1 |  |  | 1 |  |  |  |  |
| Java | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |  | 1 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 1 | 1 | 1 | 1 | 1 |  | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 2 | 1 | 2 | 1 | 1 |  |  |
| JavaScript | 1 | 1 |  | 1 | 1 | 1 | 1 | 1 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 1 | 1 | 1 |  |  |  |  |  |  |
| LaTeX | 2 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 |  |  | 1 | 2 | 1 | 1 | 1 |  |  | 1 |  |  |  |  |  |  |  | 1 |  | 1 |  |  | 2 | 1 |  | 2 |  |  |  |  |
| Lean | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |  |  |  | 1 | 1 | 1 | 1 | 1 |  |  |  |  |  | 1 |  |  |  | 1 |  |  | 1 |  | 1 |  |  | 1 |  |  |  |  |
| OCaml | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 2 |  | 1 |  | 2 | 2 | 2 | 2 | 2 |  | 1 | 1 | 1 |  | 1 |  |  | 1 | 2 | 1 | 1 | 1 | 2 | 2 | 1 |  | 2 | 1 |  |  |  |
| Python | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 1 | 1 | 2 | 4 | 4 | 4 | 4 | 3 | 2 | 3 | 1 | 1 | 2 | 2 | 2 |  | 1 | 4 | 2 | 4 | 4 | 2 | 5 | 2 | 1 | 5 |  | 2 | 1 |  |
| Ruby | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 1 |  |  | 2 | 1 | 1 | 2 | 2 | 2 | 1 | 2 | 1 | 1 | 2 | 2 | 1 | 1 | 2 | 1 | 2 | 2 | 1 | 2 | 1 |  | 2 |  | 1 | 1 |  |
| Rust | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |  | 3 | 2 | 2 | 2 | 3 | 3 | 3 | 2 | 1 | 3 | 3 | 3 | 3 | 3 | 2 | 2 | 1 | 2 | 3 | 3 | 3 | 3 | 3 |  | 3 | 1 | 2 | 1 |  |

## Interaction demand (prompts per engine)

- Median prompts/engine: **14** (over engines with sessions) 
- Mean prompts/engine: **20.3**
- Max: **58** (`chess-brainfuck-cc`)
- 6 engine(s) without any recoverable prompt (sessions archived).

Top-10 by prompt volume:

| Rank | Project | Prompts | LOC | USD |
|---:|---|---:|---:|---:|
| 1 | chess-brainfuck-cc | 58 | 7,879 | $160.58 |
| 2 | chess-rust-cc-redo | 55 | 3,329 | $63.94 |
| 3 | chess-ruby-cc | 46 | 2,964 | $148.17 |
| 4 | chess-cobol-cc | 46 | 11,578 | $518.44 |
| 5 | chess-brainfuck | 38 | 6,920 | $170.78 |
| 6 | chess-apl-codex54 | 35 | 3,652 | $115.74 |
| 7 | COBOL-chess | 33 | 8,890 | $356.45 |
| 8 | lean-chess | 21 | 2,333 | $123.23 |
| 9 | chess-css-codex | 17 | 38,684 | $27.14 |
| 10 | cplusplus-chess | 16 | 4,420 | $81.01 |

## Gameplay evidence (PGN + Stockfish-skill hints)

Per-file naming conventions encode the Stockfish-skill or Elo target used in gauntlet runs. We surface the unique hints per engine.

| Project | PGN files | Perft hits | Elo/skill hints (from filenames) |
|---|---:|---:|---|

## Models observed across sessions

| Model | # projects |
|---|---:|
| `gpt-5.3-codex` | 27 |
| `claude-opus-4-6` | 10 |
| `gpt-5.4` | 7 |
| `<synthetic>` | 6 |
| `gpt-5.2` | 4 |
| `claude-sonnet-4-6` | 1 |
| `gpt-5` | 1 |
| `gpt-5-codex` | 1 |
| `openai/gpt-5` | 1 |

## Context projects (not engines; included for completeness)

| Project | Bucket | LOC | Prompts | USD | Notes |
|---|---|---:|---:|---:|---|
| test-superset | engine-codesign | 224,772 | 0 | $0.00 | |
| chess-newlang-codex | engine-dsl | 4,658 | 21 | $113.04 | |
| chess-mojo | engine-failure | 3,472 | 7 | $24.06 | |
| chess-revisit-java-toRust-codex | engine-port | 11,141 | 33 | $330.57 | |
| chess-revisit-java-toCOBOL-codex | engine-port | 6,770 | 28 | $241.16 | |
| Chess1MChallenge | oos-challenge-arena | 233,944 | 138 | $280.96 | |
| chess-css-x86 | oos-css-variant | 60,470 | 13 | $16.08 | |
| chess-printf | oos-experiment | 1,020 | 0 | $0.00 | |
| chess-printf-codex | oos-experiment | 55,639 | 118 | $191.88 | |
| chess-conway | oos-exploration | 1,366 | 0 | $0.00 | |
| chess-excel | oos-exploration | 2,935 | 16 | $48.15 | |
| chess-lean-vibe | oos-exploration | 0 | 0 | $0.00 | |
| chessfoo | oos-exploration | 1,007 | 10 | $2.23 | |
| chessfoo-claude | oos-exploration | 8,392 | 0 | $0.00 | |
| chessprogramming-vm | oos-external-corpus | 1,384,448 | 302 | $655.83 | |
| minichess-5x5-repro | oos-minichess-variant | 22,558 | 120 | $305.81 | |
| minichess-5x5-repro-cc | oos-minichess-variant | 5,814 | 20 | $62.69 | |
| gptchess | oos-prior-work | 74,114 | 0 | $0.00 | |
| chess-brainfuck-gpt54-instant | oos-prototype | 3 | 0 | $0.00 | |
| chess-fem | oos-study | 235,408 | 0 | $0.00 | |
| chess-in-conway | oos-study | 13,956 | 0 | $0.00 | |
| chess-kasparov-claim | oos-study | 6,026 | 0 | $0.00 | |
| chess-kasparov-claim-bis | oos-study | 3,405 | 0 | $0.00 | |
| chesspuzzle-tex-codex | oos-tool | 58,242 | 27 | $117.11 | |
| puzzles-chess | oos-tool | 714 | 0 | $0.00 | |
| chess-polyglot-eval | oos-tournament-harness | 15,322 | 4 | $6.16 | |
| chess-llmtraining | oos-training-research | 10,313 | 27 | $289.43 | |
| chessball | oos-variant-game | 40,014 | 88 | $132.40 | |

## Interpretation (PASS 2 thesis notes for the paper)

1. **Agents can build non-trivial chess systems across ≥15 languages.** The corpus covers APL, Assembly, Brainfuck, C, C++, COBOL, CSS, HTML, Icon, Java, LaTeX, Mojo, Python, Ruby, Rust, SQL, Why3, and Rocq; engine cores span 15 distinct primary languages in the engine bucket.

2. **Chess provides strong oracles the agents actually exercise.** Projects where we recover PGN gauntlets, Stockfish-skill headers, or perft literals demonstrate that agents wrote and used oracles autonomously (see the Gameplay Evidence table). Example: `chess-ruby-cc` has 34 PGN files tagged at Elo 1500–2100; `chess-Rocq` has gauntlets against Stockfish skill 0–1 at targeted Elos 100–1700; `chess-why3-cc` emits 50 perft literal matches.

3. **Language matters.** The feature coverage matrix shows that higher-level languages (Python, Ruby, Rust) routinely implement full UCI + TT + iterative deepening + quiescence pipelines; niche or constrained languages (Brainfuck, CSS-only, printf-only, LaTeX) trade engine strength for *existence proofs* — they typically implement move generation with minimal search. The LOC distribution reflects this: Python/Ruby engines are ~3k LOC with deep search; CSS/HTML and assembly engines reach 10k–60k LOC because the language's primitives do less work per line.

4. **Agent interaction stays mostly at the capability level.** Median prompt volume per engine is modest (see "Interaction demand"). Intent classification on the per-project reports shows TestRequest, FeatureRequest, and Constraint as the dominant categories. The PL-ROOT prompts are usually high-level ("write a chess engine in X that plays UCI and competes with Stockfish"); the bulk of code-level detail is agent-initiated, visible in the tool-use counts (Bash/Edit/Write dominate Claude Code sessions).

5. **Subagents and tooling matter.** Claude Code sessions with subagents (e.g., `chess-ruby-cc`, `chess-rust-cc`) show parallel exploration tactics and occasionally replace main transcripts after archival. In several folders the main transcript is lost but subagent logs remain — a reproducibility threat we flag in every per-project report.

6. **Cost scales with oracle rigor, not just LOC.** The most expensive engines (`chess-cobol-cc` $518, `chess-printf-codex` $192, `chess-brainfuck` $170, `chess-brainfuck-cc` $160) are those where the agent iterates repeatedly against a correctness oracle — perft, a reference engine, or Stockfish gauntlets. Cheap engines tend to be one-shots in mainstream languages (Rust-codex $15, Java-cc $8) where the first-pass implementation already runs.

## Threats to validity

- **Archived Claude Code transcripts** (multiple projects have a `sessions-index.json` entry pointing to a missing `.jsonl`). Where only subagent logs remain, prompt/token counts under-report the user-driven interaction.
- **Cost is a list-price estimate.** Real spend likely differs with tier discounts, fast-mode, and cache behavior we could not fully reconstruct.
- **Primary-language detection** is LOC-based and occasionally misclassifies when agents generate auxiliary files (e.g. `chess-cobol-cc` has more C LOC than COBOL because transpilation produced C).
- **Feature detection is regex-based.** Unusual languages (Brainfuck, APL) under-report feature coverage; manual inspection of the per-project reports is necessary before quoting matrix cells in the paper.
- **Taxonomy is hand-curated.** The engine/meta/study split is a judgment call documented in `scripts/synthesis.py::CLASSIFICATION`.

## Reproduce this analysis

```bash
cd ~/SANDBOX/chess-meta-analysis
python3 scripts/discover.py            # overview
python3 scripts/per_project_report.py  # dossier per project
python3 scripts/elo_and_perft.py       # gameplay / perft extraction
python3 scripts/synthesis.py           # this file
```
