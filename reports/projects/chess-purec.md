# chess-purec

_Evidence-based dossier. Generated 2026-04-22 14:53 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-purec` [R:chess-purec]
- **Primary language:** C
- **Coding agent(s):** Claude Code subagents
- **Period:** —
- **LOC by language:** C (2975 LOC, 23 files), Shell (149 LOC, 1 files), Text (19 LOC, 1 files), YAML (15 LOC, 3 files)
- **Totals:** 28 files, 3158 LOC [S:scan]
- **Git:** 5 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 5 subagent transcripts [T:chess-purec/claude]
- Claude models seen: —
- Codex sessions: 0 [T:chess-purec/codex]
- Codex models seen: —

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 0 | 0 | 0 | 0 | 0 | — | $0.00 |
| **Total** |  |  |  |  |  |  | **$0.00** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| Transposition table | 14 | `Makefile` |
| Board: bitboard | 13 | `Makefile` |
| Time management | 13 | `purec` |
| Castling | 12 | `selfplay.pgn` |
| Material counting | 12 | `purec` |
| FEN parsing | 11 | `purec.dSYM/Contents/Resources/DWARF/purec` |
| UCI protocol | 9 | `Makefile` |
| Board: mailbox 8x8 | 8 | `purec.dSYM/Contents/Resources/DWARF/purec` |
| Perft | 7 | `purec` |
| Zobrist hashing | 7 | `purec` |
| Null-move pruning | 7 | `purec` |
| Check/Checkmate | 6 | `purec.dSYM/Contents/Resources/DWARF/purec` |
| Quiescence | 6 | `purec` |
| Board: magic bitboards | 4 | `test_debug.dSYM/Contents/Resources/DWARF/test_debug` |
| Aspiration windows | 4 | `purec.dSYM/Contents/Resources/DWARF/purec` |
| En passant | 3 | `src/movegen.c` |
| Promotion | 2 | `src/see.c` |
| PGN | 2 | `play_stockfish.sh` |
| Razoring | 2 | `purec.dSYM/Contents/Resources/DWARF/purec` |
| Minimax/Negamax | 1 | `src/see.c` |
| Iterative deepening | 1 | `src/search.c` |
| Move ordering (MVV-LVA) | 1 | `src/movorder.h` |
| Killer moves | 1 | `src/movorder.c` |
| History heuristic | 1 | `src/movorder.c` |
| Principal-variation (PV) | 1 | `src/search.c` |
| Late-move reduction (LMR) | 1 | `src/search.c` |
| Late-move pruning (LMP) | 1 | `src/search.c` |
| Futility pruning | 1 | `src/search.c` |
| Tapered evaluation | 1 | `src/evaluate.c` |
| King safety | 1 | `src/evaluate.c` |
| Pawn structure | 1 | `src/evaluate.c` |
| Mobility | 1 | `src/evaluate.c` |
| Opening book | 1 | `play_stockfish.sh` |

## Interaction profile

- Total user prompts (both agents): **5**
- Avg prompt length: 3097.8 chars
- Intent distribution:
  - FeatureRequest: 3
  - Constraint: 3
  - TestRequest: 2
  - ToolingBuild: 2
  - Scenario: 2
  - Documentation: 1
  - BugFixRequest: 1
  - Other: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Claude Code (subagent) — 2026-02-15 18:47 — session `agent-ae`_

```
Design a detailed implementation plan for a chess engine in pure C targeting 2000+ Elo. The project directory is empty at /Users/mathieuacher/SANDBOX/chess-purec/.

Requirements:
- **Bitboard representation** (magic bitboards for sliding pieces)
- **Full UCI protocol** support
- **Target 2000+ Elo** rating
- Must be testable against other engines via cutechess-cli

Design a complete architecture covering:

1. **File structure** - How to organize the source files
2. **Board representation** - Bitboard layout, Zobrist hashing, piece encoding
3. **Move generation** - Magic bitboards, precomputed tables, legal move gen
4. **Search** - Iterative deepening, PVS/alpha-beta, quiescence, null-move pruning, LMR, killer moves, history heuristic, aspiration windows
5. **Evaluation** - Material, piece-square tables (tapered midgame/endgame), pawn structure, king safety, mobility, passed pawns
6. **Transposition table** - Zobrist keys, TT entries, replacement scheme
7. **Move ordering** - PV move, MVV-LVA for captures, killers, history
8. **Time management** - Allocating time per move
9. **UCI protocol** - Full command handling
10. **Perft testing** - For validating move generation correctness

For each module, describe:
- Key data structures (with C struct definitions where helpful)
- Core algorithms and techniques
- Important implementation details/pitfalls
- Dependencies between modules

Also recommend an incremental build order (milestones) so the engine can be tested at each stage.

F
```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-15 19:56 | Claude Code (subagent) | FeatureRequest,BugFixRequest | I'm debugging a chess engine perft failure. The engine is at /Users/mathieuacher/SANDBOX/chess-purec. From the starting position, perft 4 g… |
| 3 | 2026-02-16 16:00 | Claude Code (subagent) | Other | I'm looking to improve a chess engine from ~2100 to 2300+ Elo. Please thoroughly explore the current search, evaluation, and move ordering … |
| 4 | 2026-02-16 16:01 | Claude Code (subagent) | FeatureRequest,Constraint | I'm improving a chess engine from ~2100 to 2300+ Elo. Based on thorough code analysis, here's what's already implemented and what's missing… |
| 5 | 2026-02-16 16:06 | Claude Code (subagent) | ToolingBuild | Explore the chess engine codebase at /Users/mathieuacher/SANDBOX/chess-purec. I need to understand: 1. All source files and their purposes … |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `9bfdd78` | 2026-02-16T22:44:11+01:00 | Mathieu Acher | Improve PureC from ~2100 to ~2200 Elo with SEE, search pruning, and eval upgrades |
| `1405914` | 2026-02-16T16:59:11+01:00 | Mathieu Acher | Add Elo gauntlet results: PureC ~2100 Elo vs Stockfish |
| `0708978` | 2026-02-16T14:44:15+01:00 | Mathieu Acher | Fix awk field indices in play_stockfish.sh result parsing |
| `3d15d9c` | 2026-02-16T13:09:40+01:00 | Mathieu Acher | Fix illegal PV moves and add Stockfish gauntlet script |
| `8dfb0cb` | 2026-02-16T12:35:01+01:00 | Mathieu Acher | Implement PureC chess engine with bitboard representation and UCI support |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **4** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, Documentation, ToolingBuild, Constraint, Scenario) [2026-02-15 18:47] — Design a detailed implementation plan for a chess engine in pure C targeting 2000+ Elo. The project directory is empty at /Users/mathieuacher/SANDBOX/chess-purec/. Requirements: -… [T:Claude Code (subagent)/agent-ae]
- **BL-002** (FeatureRequest, BugFixRequest, TestRequest, Constraint, Scenario) [2026-02-15 19:56] — I'm debugging a chess engine perft failure. The engine is at /Users/mathieuacher/SANDBOX/chess-purec. From the starting position, perft 4 gives 202329 but the correct answer is 19… [T:Claude Code (subagent)/agent-ad]
- **BL-003** (FeatureRequest, Constraint) [2026-02-16 16:01] — I'm improving a chess engine from ~2100 to 2300+ Elo. Based on thorough code analysis, here's what's already implemented and what's missing. Design a concrete implementation plan … [T:Claude Code (subagent)/agent-a0]
- **BL-004** (ToolingBuild) [2026-02-16 16:06] — Explore the chess engine codebase at /Users/mathieuacher/SANDBOX/chess-purec. I need to understand: 1. All source files and their purposes 2. The Makefile structure 3. Key data st… [T:Claude Code (subagent)/agent-a5]

## Evidence pointers

- [R:chess-purec] — repo at `/Users/mathieuacher/SANDBOX/chess-purec`
- [T:chess-purec/claude] — Claude sessions at `~/.claude/projects/chess-purec...`
- [T:chess-purec/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-purec

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.