# chess-apl-codex54

_Evidence-based dossier. Generated 2026-04-22 14:52 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-apl-codex54` [R:chess-apl-codex54]
- **Primary language:** APL
- **Coding agent(s):** Claude Code, Claude Code subagents, Codex
- **Period:** 2026-03-05 19:58 → 2026-03-20 15:33
- **LOC by language:** APL (2087 LOC, 1 files), Python (1258 LOC, 6 files), Markdown (297 LOC, 2 files), TOML (10 LOC, 1 files)
- **Totals:** 10 files, 3652 LOC [S:scan]
- **Git:** 3 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 1 main + 1 subagent transcripts [T:chess-apl-codex54/claude]
- Claude models seen: <synthetic>, claude-opus-4-6
- Codex sessions: 1 [T:chess-apl-codex54/codex]
- Codex models seen: gpt-5.4

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 1 | 9 | 58 | 6855 | 902121 | 170135 | $5.06 |
| Codex | 1 | 26 | 78170766 | 364058 | 74594432 | — | $110.68 |
| **Total** |  |  |  |  |  |  | **$115.74** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| Time management | 14 | `README.md` |
| Castling | 9 | `README.md` |
| UCI protocol | 8 | `pyproject.toml` |
| FEN parsing | 4 | `README.md` |
| Perft | 4 | `README.md` |
| Pawn structure | 4 | `README.md` |
| En passant | 3 | `README.md` |
| Promotion | 3 | `README.md` |
| Check/Checkmate | 3 | `README.md` |
| PGN | 3 | `README.md` |
| Alpha-beta | 3 | `README.md` |
| Quiescence | 3 | `README.md` |
| Transposition table | 3 | `README.md` |
| King safety | 3 | `README.md` |
| Iterative deepening | 2 | `README.md` |
| Tapered evaluation | 2 | `README.md` |
| Mobility | 2 | `README.md` |
| Material counting | 2 | `README.md` |
| Minimax/Negamax | 1 | `README.md` |
| Zobrist hashing | 1 | `README.md` |
| Move ordering (MVV-LVA) | 1 | `README.md` |
| History heuristic | 1 | `README.md` |
| Null-move pruning | 1 | `README.md` |
| Evaluation/PST | 1 | `src/apl/engine.apl` |
| Opening book | 1 | `README.md` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | exec_command | 474 |
| Codex | write_stdin | 299 |
| Claude | Bash | 18 |
| Codex | update_plan | 13 |
| Claude | Read | 3 |
| Claude | Edit | 2 |
| Claude | Agent | 1 |
| Claude | Write | 1 |
| Claude | Glob | 1 |

## Interaction profile

- Total user prompts (both agents): **35**
- Avg prompt length: 94.8 chars
- Intent distribution:
  - Other: 17
  - FeatureRequest: 8
  - Scenario: 7
  - TestRequest: 3
  - Documentation: 3
  - Question: 3
  - ToolingBuild: 2
  - Constraint: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-03-05 19:58 — session `rollout-`_

```
I want to build a chess engine in APL programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-03-05 20:16 | Codex | Other | hum I want a chess engine purely in APL... right now, the main logic is written in Python, with a small call to APL. It's not what I wanted… |
| 3 | 2026-03-05 20:42 | Codex | FeatureRequest,TestRequest | Add perft-style APL correctness tests first |
| 4 | 2026-03-05 21:04 | Codex | TestRequest,Scenario | is perft depth-4 possible? |
| 5 | 2026-03-05 21:23 | Codex | Other | it's correct, so good news... what do you mean by "Replace per-search GNU APL startup with a persistent APL worker, while keeping Python li… |
| 6 | 2026-03-05 21:26 | Codex | Other | let's go this way |
| 7 | 2026-03-05 21:34 | Codex | Other | go to next natural step |
| 8 | 2026-03-05 21:51 | Codex | FeatureRequest | let's go for Add alpha-beta pruning and move ordering in APL. Improve evaluation in APL with piece-square tables and mobility. |
| 9 | 2026-03-05 22:06 | Codex | FeatureRequest,Scenario | Add quiescence search and iterative deepening in APL. Add king safety, pawn structure, and phase-aware evaluation. before a larger match ba… |
| 10 | 2026-03-05 22:25 | Codex | Scenario | ok organize a match against Stockfish skill 1 |
| 11 | 2026-03-05 22:32 | Codex | Other | skill level 0 seems interesting... search depth 1 seems very limited for a chess engine |
| 12 | 2026-03-05 22:41 | Codex | FeatureRequest,ToolingBuild | implement time-aware iterative deepening first and then run Skill 0, certainly with also an experimental setup different with more time |
| 13 | 2026-03-05 22:52 | Codex | Other | go next steps |
| 14 | 2026-03-05 22:59 | Codex | Other | please go |
| 15 | 2026-03-05 23:10 | Codex | Other | run an Elo assessment |
| 16 | 2026-03-20 06:09 | Claude Code | Other | please analyze the code base and assess whether we can consider this chess engine implementation as a "pure" APL implementation... report o… |
| 17 | 2026-03-20 06:09 | Claude Code (subagent) | Scenario | Very thoroughly explore this chess engine codebase. I need to understand: 1. All files present, their languages, and sizes 2. The overall a… |
| 18 | 2026-03-20 10:29 | Claude Code | Documentation,Question | can you integrate this assessment as well as technical details in the README.md? |
| 19 | 2026-03-20 10:31 | Codex | Question | can you try to benchmark? the move-time seems very low... use a standard assessment Stockfish with UCI_LimitStrength=true at the 120+1s tim… |
| 20 | 2026-03-20 10:32 | Claude Code | FeatureRequest | create a git and commit |
| 21 | 2026-03-20 10:53 | Codex | Other | just 2 games yes |
| 22 | 2026-03-20 11:22 | Codex | Scenario | launch a 2 game |
| 23 | 2026-03-20 13:48 | Claude Code | FeatureRequest | create a git and commit |
| 24 | 2026-03-20 13:49 | Claude Code | Constraint | <local-command-caveat>Caveat: The messages below were generated by the user while running local commands. DO NOT respond to these messages … |
| 25 | 2026-03-20 13:49 | Claude Code | FeatureRequest | create a git and commit |
| 26 | 2026-03-20 13:51 | Codex | Other | yes please run such a benchmark... can you export games as PGN? |
| 27 | 2026-03-20 14:03 | Codex | Other | please debug |
| 28 | 2026-03-20 14:27 | Codex | Other | yes please |
| 29 | 2026-03-20 14:38 | Codex | Other | please |
| 30 | 2026-03-20 15:10 | Codex | Question,Scenario | can you organize a small tournament against a kind of "random" chess engine? |
| 31 | 2026-03-20 15:28 | Codex | Documentation | please update README accordingly with some estimation of strenght/Elo |
| 32 | 2026-03-20 15:30 | Claude Code | Other | please commit again, including PGN games if any... |
| 33 | 2026-03-20 15:31 | Claude Code | Other | please push to agentic-chessengine-apl-codex in Github |
| 34 | 2026-03-20 15:32 | Codex | Documentation | please update README and state that the chess engine has been developed by Mathieu Acher and Codex (5.3 extra high reasoning) |
| 35 | 2026-03-20 15:33 | Codex | Other | please commit/push |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `771aa4f` | 2026-03-20T16:33:26+01:00 | Mathieu Acher | Add README attribution |
| `28ef582` | 2026-03-20T16:31:01+01:00 | Mathieu Acher | Add PGN game results and engine/tooling improvements |
| `24ad9f3` | 2026-03-20T14:50:47+01:00 | Mathieu Acher | Initial commit: pure APL chess engine with Python UCI bridge |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **13** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, ToolingBuild) [2026-03-05 19:58] — I want to build a chess engine in APL programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engi… [T:Codex/rollout-]
- **BL-002** (FeatureRequest, TestRequest, Scenario) [2026-03-05 20:42] — Add perft-style APL correctness tests first [T:Codex/rollout-]
- **BL-003** (TestRequest, Scenario) [2026-03-05 21:04] — is perft depth-4 possible? [T:Codex/rollout-]
- **BL-004** (FeatureRequest) [2026-03-05 21:51] — let's go for Add alpha-beta pruning and move ordering in APL. Improve evaluation in APL with piece-square tables and mobility. [T:Codex/rollout-]
- **BL-005** (FeatureRequest, Scenario) [2026-03-05 22:06] — Add quiescence search and iterative deepening in APL. Add king safety, pawn structure, and phase-aware evaluation. before a larger match batch against weaker opposition to get a m… [T:Codex/rollout-]
- **BL-006** (Scenario) [2026-03-05 22:25] — ok organize a match against Stockfish skill 1 [T:Codex/rollout-]
- **BL-007** (FeatureRequest, ToolingBuild) [2026-03-05 22:41] — implement time-aware iterative deepening first and then run Skill 0, certainly with also an experimental setup different with more time [T:Codex/rollout-]
- **BL-008** (Scenario) [2026-03-20 06:09] — Very thoroughly explore this chess engine codebase. I need to understand: 1. All files present, their languages, and sizes 2. The overall architecture — what language(s) are used,… [T:Claude Code (subagent)/agent-a1]
- **BL-009** (Question) [2026-03-20 10:31] — can you try to benchmark? the move-time seems very low... use a standard assessment Stockfish with UCI_LimitStrength=true at the 120+1s time control, which is the time control Sto… [T:Codex/rollout-]
- **BL-010** (FeatureRequest) [2026-03-20 10:32] — create a git and commit [T:Claude Code/ce60d105]
- **BL-011** (Constraint) [2026-03-20 13:49] — <local-command-caveat>Caveat: The messages below were generated by the user while running local commands. DO NOT respond to these messages or otherwise consider them in your respo… [T:Claude Code/ce60d105]
- **BL-012** (Documentation) [2026-03-20 15:28] — please update README accordingly with some estimation of strenght/Elo [T:Codex/rollout-]
- **BL-013** (Documentation) [2026-03-20 15:32] — please update README and state that the chess engine has been developed by Mathieu Acher and Codex (5.3 extra high reasoning) [T:Codex/rollout-]

## Evidence pointers

- [R:chess-apl-codex54] — repo at `/Users/mathieuacher/SANDBOX/chess-apl-codex54`
- [T:chess-apl-codex54/claude] — Claude sessions at `~/.claude/projects/chess-apl-codex54...`
- [T:chess-apl-codex54/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-apl-codex54

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.