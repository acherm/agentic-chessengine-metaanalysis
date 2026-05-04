# chess-purec-codex

_Evidence-based dossier. Generated 2026-04-22 14:53 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-purec-codex` [R:chess-purec-codex]
- **Primary language:** C
- **Coding agent(s):** Codex
- **Period:** 2026-02-19 08:41 → 2026-02-19 10:08
- **LOC by language:** C (2483 LOC, 1 files), JSON (242 LOC, 11 files), Python (196 LOC, 1 files), Markdown (113 LOC, 1 files), Shell (61 LOC, 2 files)
- **Totals:** 16 files, 3095 LOC [S:scan]
- **Git:** not a git repo

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:chess-purec-codex/claude]
- Claude models seen: —
- Codex sessions: 1 [T:chess-purec-codex/codex]
- Codex models seen: gpt-5.3-codex

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 1 | 4 | 10971984 | 95464 | 10580736 | — | $15.99 |
| **Total** |  |  |  |  |  |  | **$15.99** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| PGN | 14 | `README.md` |
| Time management | 14 | `README.md` |
| Castling | 12 | `results/bench40-sf1800.pgn` |
| Late-move reduction (LMR) | 9 | `README.md` |
| Perft | 4 | `Makefile` |
| UCI protocol | 3 | `README.md` |
| Material counting | 3 | `results/lmrsee-bench40-sf1900.pgn` |
| FEN parsing | 2 | `scripts/perft_check.sh` |
| Check/Checkmate | 2 | `results/bench80-sf1600.pgn` |
| Quiescence | 2 | `README.md` |
| Transposition table | 2 | `README.md` |
| Zobrist hashing | 2 | `README.md` |
| Null-move pruning | 2 | `README.md` |
| Aspiration windows | 2 | `README.md` |
| Opening book | 2 | `README.md` |
| Promotion | 1 | `src/engine.c` |
| Minimax/Negamax | 1 | `src/engine.c` |
| Alpha-beta | 1 | `README.md` |
| Iterative deepening | 1 | `README.md` |
| Killer moves | 1 | `src/engine.c` |
| History heuristic | 1 | `src/engine.c` |
| Principal-variation (PV) | 1 | `README.md` |
| Tapered evaluation | 1 | `README.md` |
| Pawn structure | 1 | `README.md` |
| Mobility | 1 | `README.md` |
| Endgame tables | 1 | `README.md` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | exec_command | 85 |
| Codex | write_stdin | 34 |

## Interaction profile

- Total user prompts (both agents): **4**
- Avg prompt length: 100.0 chars
- Intent distribution:
  - Other: 3
  - FeatureRequest: 1
  - TestRequest: 1
  - ToolingBuild: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-02-19 08:41 — session `rollout-`_

```
I want to build a chess engine in C programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-19 09:44 | Codex | Other | please give an estimate of Elo by running a bench |
| 3 | 2026-02-19 09:50 | Codex | Other | please significantly improve the chess engine |
| 4 | 2026-02-19 10:00 | Codex | Other | do the next major jump (LMR + SEE pruning + stronger eval terms) and run another controlled Elo bench. |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **1** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, ToolingBuild) [2026-02-19 08:41] — I want to build a chess engine in C programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engine… [T:Codex/rollout-]

## Evidence pointers

- [R:chess-purec-codex] — repo at `/Users/mathieuacher/SANDBOX/chess-purec-codex`
- [T:chess-purec-codex/claude] — Claude sessions at `~/.claude/projects/chess-purec-codex...`
- [T:chess-purec-codex/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-purec-codex

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.