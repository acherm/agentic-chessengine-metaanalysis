# chess-sql

_Evidence-based dossier. Generated 2026-04-22 14:53 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-sql` [R:chess-sql]
- **Primary language:** Python
- **Coding agent(s):** Claude Code subagents
- **Period:** —
- **LOC by language:** Python (1150 LOC, 8 files), SQL (725 LOC, 4 files), Markdown (81 LOC, 1 files), Shell (60 LOC, 2 files)
- **Totals:** 15 files, 2016 LOC [S:scan]
- **Git:** 1 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 3 subagent transcripts [T:chess-sql/claude]
- Claude models seen: —
- Codex sessions: 0 [T:chess-sql/codex]
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
| FEN parsing | 7 | `uci_wrapper.py` |
| Castling | 6 | `engine.py` |
| UCI protocol | 5 | `uci_wrapper.py` |
| Check/Checkmate | 5 | `TOURNAMENT_REPORT.md` |
| En passant | 4 | `engine.py` |
| Promotion | 4 | `engine.py` |
| Evaluation/PST | 4 | `TOURNAMENT_REPORT.md` |
| Material counting | 4 | `TOURNAMENT_REPORT.md` |
| Perft | 3 | `uci_wrapper.py` |
| Time management | 3 | `TOURNAMENT_REPORT.md` |
| Minimax/Negamax | 2 | `TOURNAMENT_REPORT.md` |
| PGN | 1 | `tools/run_tournament.sh` |
| Quiescence | 1 | `TOURNAMENT_REPORT.md` |
| Move ordering (MVV-LVA) | 1 | `TOURNAMENT_REPORT.md` |
| King safety | 1 | `TOURNAMENT_REPORT.md` |
| Pawn structure | 1 | `TOURNAMENT_REPORT.md` |

## Interaction profile

- Total user prompts (both agents): **3**
- Avg prompt length: 2861.3 chars
- Intent distribution:
  - Constraint: 3
  - FeatureRequest: 2
  - TestRequest: 2
  - Scenario: 2
  - ToolingBuild: 1
  - BugFixRequest: 1
  - Documentation: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Claude Code (subagent) — 2026-02-15 18:47 — session `agent-ac`_

```
I'm planning a chess engine written in **pure SQL (SQLite)** with a thin Python UCI wrapper for Elo testing via cutechess-cli.

User constraints:
- **SQLite** as the database
- **Pure SQL queries/CTEs** — all chess logic (move generation, evaluation, search) must be expressed as SQL. The Python wrapper only handles UCI protocol and feeds positions into SQLite.
- **cutechess-cli** for Elo testing against weak engines

Please design a detailed implementation plan covering:

1. **Board Representation**: How to represent a chess position in SQLite-friendly format. Consider using a 64-character string (piece placement) plus metadata (side to move, castling, en passant, clocks). The wrapper populates a `position` table.

2. **Lookup Tables (schema.sql)**: Pre-computed tables needed:
   - Piece values (material)
   - Piece-square tables (positional bonuses per square per piece)
   - Move offsets for each piece type
   - Square coordinates (rank, file for each index 0-63)

3. **Move Generation (moves.sql)**: The hardest part. A CTE-based query that generates all legal moves from a position. Cover:
   - Pawn moves (forward, double push, captures, en passant, promotion)
   - Knight moves (fixed offsets with board-edge wrapping checks)
   - Sliding pieces (bishop, rook, queen) via recursive CTEs
   - King moves (including castling)
   - Legality filtering (king not in check after move)
   - Think about how to handle board-edge wrapping (file wrapping for offsets like ±1, ±7, ±9)

4. **E
```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-16 16:05 | Claude Code (subagent) | Constraint,Scenario | Read the tournament PGN file at /Users/mathieuacher/SANDBOX/chess-sql/tournament.pgn and analyze a few representative games. I want to unde… |
| 3 | 2026-02-16 16:08 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `30e5631` | 2026-02-16T17:17:56+01:00 | Mathieu Acher | Implement chess engine with all chess logic in pure SQL (SQLite) |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **3** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, ToolingBuild, Constraint, Scenario) [2026-02-15 18:47] — I'm planning a chess engine written in **pure SQL (SQLite)** with a thin Python UCI wrapper for Elo testing via cutechess-cli. User constraints: - **SQLite** as the database - **P… [T:Claude Code (subagent)/agent-ac]
- **BL-002** (Constraint, Scenario) [2026-02-16 16:05] — Read the tournament PGN file at /Users/mathieuacher/SANDBOX/chess-sql/tournament.pgn and analyze a few representative games. I want to understand: 1. Typical game lengths (ply cou… [T:Claude Code (subagent)/agent-a5]
- **BL-003** (FeatureRequest, BugFixRequest, TestRequest, Documentation, Constraint) [2026-02-16 16:08] — Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previous actions. This summary should be thor… [T:Claude Code (subagent)/agent-ac]

## Evidence pointers

- [R:chess-sql] — repo at `/Users/mathieuacher/SANDBOX/chess-sql`
- [T:chess-sql/claude] — Claude sessions at `~/.claude/projects/chess-sql...`
- [T:chess-sql/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-sql

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.