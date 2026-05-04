# cplusplus-chess

_Evidence-based dossier. Generated 2026-04-22 14:55 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/cplusplus-chess` [R:cplusplus-chess]
- **Primary language:** C++
- **Coding agent(s):** Codex
- **Period:** 2026-02-10 11:14 → 2026-02-13 15:20
- **LOC by language:** C++ (2889 LOC, 13 files), C (550 LOC, 14 files), Python (504 LOC, 2 files), Markdown (244 LOC, 2 files), Shell (177 LOC, 2 files), Text (56 LOC, 1 files)
- **Totals:** 34 files, 4420 LOC [S:scan]
- **Git:** 1 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:cplusplus-chess/claude]
- Claude models seen: —
- Codex sessions: 1 [T:cplusplus-chess/codex]
- Codex models seen: gpt-5.2, gpt-5.3-codex

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 1 | 16 | 55733481 | 460408 | 53877504 | — | $81.01 |
| **Total** |  |  |  |  |  |  | **$81.01** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| FEN parsing | 11 | `README.md` |
| UCI protocol | 10 | `CMakeLists.txt` |
| Transposition table | 8 | `CMakeLists.txt` |
| Perft | 7 | `CMakeLists.txt` |
| Pawn structure | 7 | `tools/eval_dataset.cpp` |
| Time management | 7 | `README.md` |
| Castling | 5 | `tools/openings.pgn` |
| Board: bitboard | 5 | `CMakeLists.txt` |
| Zobrist hashing | 5 | `CMakeLists.txt` |
| Evaluation/PST | 5 | `docs/tuning_pipeline.md` |
| Material counting | 5 | `tools/uci_match.cpp` |
| En passant | 4 | `src/board.cpp` |
| Check/Checkmate | 4 | `tools/uci_match.cpp` |
| Promotion | 3 | `tests/perft_tests.cpp` |
| PGN | 3 | `README.md` |
| Null-move pruning | 3 | `src/board.cpp` |
| Minimax/Negamax | 2 | `src/search.cpp` |
| Quiescence | 2 | `src/search.cpp` |
| King safety | 2 | `docs/tuning_pipeline.md` |
| Mobility | 2 | `docs/tuning_pipeline.md` |
| Move ordering (MVV-LVA) | 1 | `src/search.cpp` |
| Principal-variation (PV) | 1 | `src/search.cpp` |
| Aspiration windows | 1 | `src/search.cpp` |
| Futility pruning | 1 | `src/search.cpp` |
| Opening book | 1 | `README.md` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | exec_command | 298 |
| Codex | write_stdin | 166 |
| Codex | update_plan | 25 |

## Interaction profile

- Total user prompts (both agents): **16**
- Avg prompt length: 654.6 chars
- Intent distribution:
  - FeatureRequest: 6
  - Other: 5
  - Scenario: 5
  - ToolingBuild: 3
  - Constraint: 2
  - Documentation: 2
  - TestRequest: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-02-10 11:14 — session `rollout-`_

```
I want to build a chess engine in C++ programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-10 11:40 | Codex | Other | Please estimate the Elo rating (Stockfish is installed) |
| 3 | 2026-02-10 13:16 | Codex | Other | great! let's now to improve significantly the Elo of the engine |
| 4 | 2026-02-10 15:01 | Codex | Constraint | I don't have specific opinions about time-control, I want the most accurate way to assess the Elo and also further improve the chess engine |
| 5 | 2026-02-10 18:12 | Codex | FeatureRequest,ToolingBuild | mathieuacher@Mathieus-MacBook-Pro cplusplus-chess % SF_ELO=2200 GAMES=100 TC=60+0.6 bash /Users/mathieuacher/SANDBOX/cplusplus-chess/tools/… |
| 6 | 2026-02-10 18:53 | Codex | Scenario | Indexing opening suite... Started game 1 of 10 (cpp vs stockfish) Finished game 1 (cpp vs stockfish): 1-0 {White mates} Score of cpp vs sto… |
| 7 | 2026-02-10 20:37 | Codex | Constraint,Scenario | Started game 40 of 40 (stockfish vs cpp) Finished game 40 (stockfish vs cpp): 0-1 {Black mates} Score of cpp vs stockfish: 22 - 14 - 4 [0.6… |
| 8 | 2026-02-11 13:03 | Codex | Scenario | Started game 200 of 200 (stockfish vs cpp) Finished game 200 (stockfish vs cpp): 0-1 {Black mates} Score of cpp vs stockfish: 123 - 67 - 10… |
| 9 | 2026-02-12 06:27 | Codex | Other | Score of cpp vs stockfish: 65 - 32 - 3 [0.665] 100 ... cpp playing White: 34 - 14 - 2 [0.700] 50 ... cpp playing Black: 31 - 18 - 1 [0.630]… |
| 10 | 2026-02-12 19:33 | Codex | Other | SF_ELO=2350 GAMES=100 TC=60+0.6 OPEN_PLIES=12 SRAND=1 SF_THREADS=1 bash /Users/mathieuacher/SANDBOX/cplusplus-chess/tools/run_cutechess.sh … |
| 11 | 2026-02-12 19:35 | Codex | FeatureRequest | the tuning pipeline is an exciting research direction... but first, can you create a git and commit everything? |
| 12 | 2026-02-12 20:18 | Codex | FeatureRequest,Documentation | let's go now for the tuning pipeline... document what you mean by "weights" first and the general approach. Then implement it |
| 13 | 2026-02-12 20:19 | Codex | FeatureRequest,Documentation | let's go now for the tuning pipeline... document what you mean by "weights" first and the general approach. Then implement it |
| 14 | 2026-02-12 21:02 | Codex | FeatureRequest,ToolingBuild | info: cutechess-cli: /usr/local/bin/cutechess-cli info: engine: /Users/mathieuacher/SANDBOX/cplusplus-chess/build/cplusplus_chess info: sto… |
| 15 | 2026-02-13 04:27 | Codex | Other | Warning: stockfish doesn't have option Ponder |
| 16 | 2026-02-13 15:16 | Codex | Scenario | Score of cpp vs stockfish: 81 - 105 - 14 [0.440] 200 ... cpp playing White: 45 - 48 - 7 [0.485] 100 ... cpp playing Black: 36 - 57 - 7 [0.3… |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `bb35d8a` | 2026-02-12T20:38:16+01:00 | Mathieu Acher | Initial commit |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **10** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, ToolingBuild) [2026-02-10 11:14] — I want to build a chess engine in C++ programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engi… [T:Codex/rollout-]
- **BL-002** (Constraint) [2026-02-10 15:01] — I don't have specific opinions about time-control, I want the most accurate way to assess the Elo and also further improve the chess engine [T:Codex/rollout-]
- **BL-003** (FeatureRequest, ToolingBuild, Scenario) [2026-02-10 18:12] — mathieuacher@Mathieus-MacBook-Pro cplusplus-chess % SF_ELO=2200 GAMES=100 TC=60+0.6 bash /Users/mathieuacher/SANDBOX/cplusplus-chess/tools/run_cutechess.sh info: cutechess-cli: /u… [T:Codex/rollout-]
- **BL-004** (Scenario) [2026-02-10 18:53] — Indexing opening suite... Started game 1 of 10 (cpp vs stockfish) Finished game 1 (cpp vs stockfish): 1-0 {White mates} Score of cpp vs stockfish: 1 - 0 - 0 [1.000] 1 Started game… [T:Codex/rollout-]
- **BL-005** (Constraint, Scenario) [2026-02-10 20:37] — Started game 40 of 40 (stockfish vs cpp) Finished game 40 (stockfish vs cpp): 0-1 {Black mates} Score of cpp vs stockfish: 22 - 14 - 4 [0.600] 40 ... cpp playing White: 10 - 7 - 3… [T:Codex/rollout-]
- **BL-006** (Scenario) [2026-02-11 13:03] — Started game 200 of 200 (stockfish vs cpp) Finished game 200 (stockfish vs cpp): 0-1 {Black mates} Score of cpp vs stockfish: 123 - 67 - 10 [0.640] 200 ... cpp playing White: 64 -… [T:Codex/rollout-]
- **BL-007** (FeatureRequest) [2026-02-12 19:35] — the tuning pipeline is an exciting research direction... but first, can you create a git and commit everything? [T:Codex/rollout-]
- **BL-008** (FeatureRequest, Documentation) [2026-02-12 20:18] — let's go now for the tuning pipeline... document what you mean by "weights" first and the general approach. Then implement it [T:Codex/rollout-]
- **BL-009** (FeatureRequest, ToolingBuild) [2026-02-12 21:02] — info: cutechess-cli: /usr/local/bin/cutechess-cli info: engine: /Users/mathieuacher/SANDBOX/cplusplus-chess/build/cplusplus_chess info: stockfish: /opt/homebrew/bin/stockfish (UCI… [T:Codex/rollout-]
- **BL-010** (Scenario) [2026-02-13 15:16] — Score of cpp vs stockfish: 81 - 105 - 14 [0.440] 200 ... cpp playing White: 45 - 48 - 7 [0.485] 100 ... cpp playing Black: 36 - 57 - 7 [0.395] 100 ... White vs Black: 102 - 84 - 1… [T:Codex/rollout-]

## Evidence pointers

- [R:cplusplus-chess] — repo at `/Users/mathieuacher/SANDBOX/cplusplus-chess`
- [T:cplusplus-chess/claude] — Claude sessions at `~/.claude/projects/cplusplus-chess...`
- [T:cplusplus-chess/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/cplusplus-chess

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.