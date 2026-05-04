# chess-assembly-codex

_Evidence-based dossier. Generated 2026-04-22 14:52 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-assembly-codex` [R:chess-assembly-codex]
- **Primary language:** Assembly
- **Coding agent(s):** Codex
- **Period:** 2026-02-24 13:03 → 2026-02-25 14:36
- **LOC by language:** Assembly (9494 LOC, 2 files), C (1922 LOC, 1 files), Python (820 LOC, 5 files), Markdown (74 LOC, 1 files)
- **Totals:** 9 files, 12310 LOC [S:scan]
- **Git:** not a git repo

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:chess-assembly-codex/claude]
- Claude models seen: —
- Codex sessions: 1 [T:chess-assembly-codex/codex]
- Codex models seen: gpt-5.3-codex

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 1 | 12 | 32952290 | 184660 | 31765120 | — | $47.01 |
| **Total** |  |  |  |  |  |  | **$47.01** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| UCI protocol | 6 | `README.md` |
| Time management | 5 | `Makefile` |
| Castling | 4 | `README.md` |
| Transposition table | 4 | `README.md` |
| Quiescence | 3 | `README.md` |
| Zobrist hashing | 3 | `scripts/asm_core.py` |
| Material counting | 2 | `src/core/core.s` |
| FEN parsing | 1 | `scripts/uci_bridge.py` |
| Promotion | 1 | `scripts/asm_core.py` |
| Check/Checkmate | 1 | `src/core/core_impl.c` |
| Board: mailbox 8x8 | 1 | `src/core/core_impl.c` |
| Alpha-beta | 1 | `scripts/asm_core.py` |
| Iterative deepening | 1 | `README.md` |
| Principal-variation (PV) | 1 | `README.md` |
| Null-move pruning | 1 | `README.md` |
| Aspiration windows | 1 | `README.md` |
| Futility pruning | 1 | `README.md` |
| Tapered evaluation | 1 | `README.md` |
| Pawn structure | 1 | `src/core/core_impl.c` |
| Opening book | 1 | `scripts/asm_core.py` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | exec_command | 198 |
| Codex | write_stdin | 92 |
| Codex | update_plan | 2 |

## Interaction profile

- Total user prompts (both agents): **12**
- Avg prompt length: 84.1 chars
- Intent distribution:
  - FeatureRequest: 5
  - Other: 5
  - Question: 2
  - TestRequest: 1
  - ToolingBuild: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-02-24 13:03 — session `rollout-`_

```
I want to build a chess engine in assembly language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-24 16:39 | Codex | Other | I'm mainly interested by having a strong chess engine in assembly (the UCI handling can even be done by another script and high-level langu… |
| 3 | 2026-02-24 17:53 | Codex | FeatureRequest | yes go to assembly make/unmake + alpha-beta depth 3+ with move ordering, |
| 4 | 2026-02-24 18:07 | Codex | FeatureRequest | implement castling and en-passant generation plus quiescence |
| 5 | 2026-02-24 20:00 | Codex | Other | please significantly improve the chess engine and Elo... be ambitious and reach 2500+ Elo |
| 6 | 2026-02-25 07:35 | Codex | FeatureRequest | yes add repetition + 50-move rule handling in assembly |
| 7 | 2026-02-25 08:11 | Codex | Question | can you run a 10 games bench on strong Stockfish to refine the Elo? |
| 8 | 2026-02-25 13:05 | Codex | Other | please have a tighter estimate |
| 9 | 2026-02-25 13:22 | Codex | Question | can you detail the list of chess engine features implemented as well as description of the overall architecture? |
| 10 | 2026-02-25 13:31 | Codex | Other | can we consider it is more a C-like chess engine? |
| 11 | 2026-02-25 13:32 | Codex | FeatureRequest | try to implement advanced features to try reaching 2800+ Elo |
| 12 | 2026-02-25 14:14 | Codex | Other | let's go for SEE/capture pruning quality, pawn hash + eval cache |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **5** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, ToolingBuild) [2026-02-24 13:03] — I want to build a chess engine in assembly language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of … [T:Codex/rollout-]
- **BL-002** (FeatureRequest) [2026-02-24 17:53] — yes go to assembly make/unmake + alpha-beta depth 3+ with move ordering, [T:Codex/rollout-]
- **BL-003** (FeatureRequest) [2026-02-24 18:07] — implement castling and en-passant generation plus quiescence [T:Codex/rollout-]
- **BL-004** (FeatureRequest) [2026-02-25 07:35] — yes add repetition + 50-move rule handling in assembly [T:Codex/rollout-]
- **BL-005** (FeatureRequest) [2026-02-25 13:32] — try to implement advanced features to try reaching 2800+ Elo [T:Codex/rollout-]

## Evidence pointers

- [R:chess-assembly-codex] — repo at `/Users/mathieuacher/SANDBOX/chess-assembly-codex`
- [T:chess-assembly-codex/claude] — Claude sessions at `~/.claude/projects/chess-assembly-codex...`
- [T:chess-assembly-codex/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-assembly-codex

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.