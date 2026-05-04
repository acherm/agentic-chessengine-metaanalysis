# chess-java-cc

_Evidence-based dossier. Generated 2026-04-22 14:52 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-java-cc` [R:chess-java-cc]
- **Primary language:** Java
- **Coding agent(s):** Claude Code, Claude Code subagents
- **Period:** 2026-03-10 20:09 → 2026-03-10 20:19
- **LOC by language:** Java (3698 LOC, 30 files), Markdown (924 LOC, 2 files), Shell (193 LOC, 1 files), XML (58 LOC, 1 files), Text (11 LOC, 1 files)
- **Totals:** 35 files, 4884 LOC [S:scan]
- **Git:** 5 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 1 main + 3 subagent transcripts [T:chess-java-cc/claude]
- Claude models seen: claude-opus-4-6
- Codex sessions: 0 [T:chess-java-cc/codex]
- Codex models seen: —

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 1 | 3 | 54 | 13943 | 1666421 | 223501 | $7.74 |
| Codex | 0 | 0 | 0 | 0 | 0 | — | $0.00 |
| **Total** |  |  |  |  |  |  | **$7.74** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| Board: bitboard | 18 | `SPECIFICATION.md` |
| Castling | 13 | `SPECIFICATION.md` |
| Transposition table | 13 | `SPECIFICATION.md` |
| Time management | 11 | `SPECIFICATION.md` |
| FEN parsing | 10 | `SPECIFICATION.md` |
| Zobrist hashing | 10 | `SPECIFICATION.md` |
| Material counting | 10 | `SPECIFICATION.md` |
| En passant | 7 | `SPECIFICATION.md` |
| Check/Checkmate | 7 | `SPECIFICATION.md` |
| Board: magic bitboards | 7 | `SPECIFICATION.md` |
| Opening book | 6 | `SPECIFICATION.md` |
| UCI protocol | 5 | `SPECIFICATION.md` |
| Promotion | 5 | `SPECIFICATION.md` |
| Evaluation/PST | 5 | `SPECIFICATION.md` |
| Perft | 4 | `SPECIFICATION.md` |
| History heuristic | 4 | `SPECIFICATION.md` |
| Principal-variation (PV) | 4 | `SPECIFICATION.md` |
| Null-move pruning | 4 | `SPECIFICATION.md` |
| Tapered evaluation | 4 | `SPECIFICATION.md` |
| King safety | 4 | `SPECIFICATION.md` |
| Pawn structure | 4 | `SPECIFICATION.md` |
| PGN | 3 | `ELO_REPORT.md` |
| Alpha-beta | 3 | `SPECIFICATION.md` |
| Quiescence | 3 | `SPECIFICATION.md` |
| Killer moves | 3 | `SPECIFICATION.md` |
| Late-move reduction (LMR) | 3 | `SPECIFICATION.md` |
| Aspiration windows | 3 | `SPECIFICATION.md` |
| Futility pruning | 3 | `SPECIFICATION.md` |
| Mobility | 3 | `SPECIFICATION.md` |
| Board: mailbox 8x8 | 2 | `SPECIFICATION.md` |
| Minimax/Negamax | 2 | `SPECIFICATION.md` |
| Iterative deepening | 2 | `SPECIFICATION.md` |
| Move ordering (MVV-LVA) | 2 | `SPECIFICATION.md` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Claude | Read | 19 |
| Claude | Glob | 5 |
| Claude | Edit | 2 |
| Claude | Agent | 1 |
| Claude | Write | 1 |

## Interaction profile

- Total user prompts (both agents): **6**
- Avg prompt length: 1482.2 chars
- Intent distribution:
  - FeatureRequest: 3
  - TestRequest: 2
  - Constraint: 2
  - Scenario: 2
  - Question: 2
  - ToolingBuild: 1
  - BugFixRequest: 1
  - Documentation: 1
  - Other: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Claude Code (subagent) — 2026-02-17 12:56 — session `agent-ab`_

```
Design a detailed implementation plan for a competitive chess engine in Java targeting ~1800+ Elo. The engine must support the UCI (Universal Chess Interface) protocol so it can be tested against other engines using tools like cutechess-cli.

The project uses Maven as the build system. The directory is empty — this is from scratch.

Requirements:
1. **UCI Protocol**: Full UCI compliance so it works with cutechess-cli, Arena, etc.
2. **Target Elo ~1800+**: This requires serious search and evaluation.

Please design the architecture covering these components:

### Board Representation
- Bitboard-based representation (64-bit longs for each piece type/color)
- FEN parsing and generation
- Zobrist hashing for transposition tables

### Move Generation
- Legal move generation using bitboards
- Special moves: castling, en passant, promotions
- Attack tables (magic bitboards or precomputed sliding piece attacks)
- Perft testing for correctness validation

### Search
- Iterative deepening with alpha-beta pruning
- Principal Variation Search (PVS)
- Transposition table (hash table)
- Quiescence search with SEE (Static Exchange Evaluation)
- Null-move pruning
- Late Move Reductions (LMR)
- Killer move heuristic
- History heuristic for move ordering
- Aspiration windows
- Time management

### Evaluation
- Material counting
- Piece-square tables (middlegame and endgame)
- Tapered evaluation (interpolate between middlegame and endgame based on game phase)
- Pawn structure evaluation (double
```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-17 15:53 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 3 | 2026-03-10 20:10 | Claude Code | FeatureRequest,Question | could you specify a specification of the current chess engine (including supported features and design choices) in such a way I can share i… |
| 4 | 2026-03-10 20:10 | Claude Code (subagent) | Scenario | Very thoroughly explore this chess engine codebase. I need to understand every feature, algorithm, data structure, and design choice. Speci… |
| 5 | 2026-03-10 20:18 | Claude Code | Question | why 1800+? |
| 6 | 2026-03-10 20:19 | Claude Code | Other | yes pleae |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `fe25b94` | 2026-02-19T09:46:49+01:00 | Mathieu Acher | Add calibrated Elo results at 120+1 TC matching SF calibration |
| `d747e48` | 2026-02-18T11:33:10+01:00 | Mathieu Acher | Update Elo report with calibration analysis and corrected estimates |
| `d0d43a6` | 2026-02-18T10:25:14+01:00 | Mathieu Acher | Add configurable Elo testing script |
| `201399e` | 2026-02-18T08:41:44+01:00 | Mathieu Acher | Add Elo assessment report and match PGNs |
| `f909c32` | 2026-02-17T20:46:19+01:00 | Mathieu Acher | Implement UCI chess engine with bitboard representation targeting ~1800+ Elo |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **4** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, ToolingBuild, Constraint, Scenario) [2026-02-17 12:56] — Design a detailed implementation plan for a competitive chess engine in Java targeting ~1800+ Elo. The engine must support the UCI (Universal Chess Interface) protocol so it can b… [T:Claude Code (subagent)/agent-ab]
- **BL-002** (FeatureRequest, BugFixRequest, TestRequest, Documentation, Constraint) [2026-02-17 15:53] — Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previous actions. This summary should be thor… [T:Claude Code (subagent)/agent-ac]
- **BL-003** (FeatureRequest, Question) [2026-03-10 20:10] — could you specify a specification of the current chess engine (including supported features and design choices) in such a way I can share it to a coding agent that could try to im… [T:Claude Code/50f80dc4]
- **BL-004** (Scenario) [2026-03-10 20:10] — Very thoroughly explore this chess engine codebase. I need to understand every feature, algorithm, data structure, and design choice. Specifically investigate: 1. Board representa… [T:Claude Code (subagent)/agent-a3]

## Evidence pointers

- [R:chess-java-cc] — repo at `/Users/mathieuacher/SANDBOX/chess-java-cc`
- [T:chess-java-cc/claude] — Claude sessions at `~/.claude/projects/chess-java-cc...`
- [T:chess-java-cc/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-java-cc

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.