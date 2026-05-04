# chess-py-cc

_Evidence-based dossier. Generated 2026-04-22 14:53 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-py-cc` [R:chess-py-cc]
- **Primary language:** Python
- **Coding agent(s):** Claude Code subagents
- **Period:** —
- **LOC by language:** Python (2968 LOC, 21 files), Shell (27 LOC, 1 files)
- **Totals:** 22 files, 2995 LOC [S:scan]
- **Git:** not a git repo

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 1 subagent transcripts [T:chess-py-cc/claude]
- Claude models seen: —
- Codex sessions: 0 [T:chess-py-cc/codex]
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
| Transposition table | 8 | `tables/zobrist.py` |
| Material counting | 7 | `tables/pst.py` |
| UCI protocol | 6 | `main.py` |
| Castling | 6 | `tests/test_movegen.py` |
| Promotion | 6 | `tests/test_movegen.py` |
| Board: bitboard | 6 | `engine/board.py` |
| FEN parsing | 5 | `tools/perft_bench.py` |
| Check/Checkmate | 5 | `tests/test_search.py` |
| Perft | 4 | `tools/perft_bench.py` |
| En passant | 4 | `tables/zobrist.py` |
| Board: mailbox 8x8 | 4 | `engine/board.py` |
| Time management | 4 | `tools/run_tournament.sh` |
| Zobrist hashing | 3 | `tables/zobrist.py` |
| Move ordering (MVV-LVA) | 3 | `engine/movorder.py` |
| Null-move pruning | 3 | `tests/test_board.py` |
| Evaluation/PST | 3 | `tables/pst.py` |
| Quiescence | 2 | `engine/movegen.py` |
| Killer moves | 2 | `engine/movorder.py` |
| Tapered evaluation | 2 | `tables/pst.py` |
| PGN | 1 | `tools/run_tournament.sh` |
| Alpha-beta | 1 | `engine/search.py` |
| Iterative deepening | 1 | `engine/search.py` |
| History heuristic | 1 | `engine/movorder.py` |
| Principal-variation (PV) | 1 | `engine/search.py` |
| Late-move reduction (LMR) | 1 | `engine/search.py` |
| Aspiration windows | 1 | `engine/search.py` |
| Futility pruning | 1 | `engine/search.py` |
| Razoring | 1 | `engine/search.py` |
| King safety | 1 | `engine/evaluate.py` |
| Pawn structure | 1 | `engine/evaluate.py` |
| Mobility | 1 | `engine/evaluate.py` |

## Interaction profile

- Total user prompts (both agents): **1**
- Avg prompt length: 3051.0 chars
- Intent distribution:
  - FeatureRequest: 1
  - TestRequest: 1
  - ToolingBuild: 1
  - Scenario: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Claude Code (subagent) — 2026-02-18 21:32 — session `agent-ae`_

```
Design a detailed implementation plan for a chess engine written from scratch in Python (no python-chess library). The engine should be as strong as possible and support the UCI protocol for testing with cutechess-cli.

Requirements:
- From scratch: board representation, move generation, validation — all custom
- Maximum strength: all reasonable optimizations for a Python engine
- UCI protocol support for cutechess-cli Elo testing
- Clean, modular architecture

Consider these key components and design the architecture:

1. **Board Representation**: Bitboards using Python's arbitrary-precision integers (one per piece type per color = 12 bitboards). Include occupancy bitboards. Squares numbered 0-63 (a1=0, h8=63).

2. **Move Generation**: 
   - Precomputed attack tables for knights, kings
   - Sliding piece attacks (rooks, bishops, queens) — magic bitboards are complex in Python, so consider classical approach or Kindergarten/obstruction difference
   - Pawn moves (single push, double push, captures, en passant, promotions)
   - Castling with full legality checks
   - Legal move generation (filter pseudo-legal moves that leave king in check)

3. **Move Encoding**: Pack moves into integers: from_sq (6 bits), to_sq (6 bits), flags (4 bits for captures, promotions, castling, en passant)

4. **Search Algorithm**:
   - Iterative deepening with alpha-beta (negamax)
   - Transposition table (Zobrist hashing)
   - Quiescence search
   - Null-move pruning
   - Late-move reductions (LMR)
```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **1** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, ToolingBuild, Scenario) [2026-02-18 21:32] — Design a detailed implementation plan for a chess engine written from scratch in Python (no python-chess library). The engine should be as strong as possible and support the UCI p… [T:Claude Code (subagent)/agent-ae]

## Evidence pointers

- [R:chess-py-cc] — repo at `/Users/mathieuacher/SANDBOX/chess-py-cc`
- [T:chess-py-cc/claude] — Claude sessions at `~/.claude/projects/chess-py-cc...`
- [T:chess-py-cc/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-py-cc

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.