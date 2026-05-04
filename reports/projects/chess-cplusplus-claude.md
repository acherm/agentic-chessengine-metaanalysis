# chess-cplusplus-claude

_Evidence-based dossier. Generated 2026-04-22 14:52 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-cplusplus-claude` [R:chess-cplusplus-claude]
- **Primary language:** C++
- **Coding agent(s):** Claude Code subagents
- **Period:** —
- **LOC by language:** C++ (2868 LOC, 11 files), C (784 LOC, 11 files), Shell (341 LOC, 2 files), Markdown (179 LOC, 1 files), Text (76 LOC, 3 files)
- **Totals:** 28 files, 4248 LOC [S:scan]
- **Git:** 5 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 18 subagent transcripts [T:chess-cplusplus-claude/claude]
- Claude models seen: —
- Codex sessions: 0 [T:chess-cplusplus-claude/codex]
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
| Time management | 23 | `test_sk10.pgn` |
| Castling | 20 | `test_sk10.pgn` |
| Transposition table | 12 | `CMakeLists.txt` |
| Board: bitboard | 11 | `CMakeLists.txt` |
| UCI protocol | 8 | `CMakeLists.txt` |
| Perft | 8 | `CMakeLists.txt` |
| Promotion | 8 | `ELO_REPORT.md` |
| Material counting | 8 | `ELO_REPORT.md` |
| FEN parsing | 5 | `tests/perft_test.cpp` |
| En passant | 5 | `src/movepick.cpp` |
| Quiescence | 5 | `ELO_REPORT.md` |
| Zobrist hashing | 5 | `ELO_REPORT.md` |
| Check/Checkmate | 4 | `src/search.cpp` |
| Null-move pruning | 4 | `ELO_REPORT.md` |
| Board: magic bitboards | 3 | `ELO_REPORT.md` |
| Killer moves | 3 | `ELO_REPORT.md` |
| History heuristic | 3 | `ELO_REPORT.md` |
| Tapered evaluation | 3 | `ELO_REPORT.md` |
| PGN | 2 | `benchmark.sh` |
| Move ordering (MVV-LVA) | 2 | `ELO_REPORT.md` |
| Principal-variation (PV) | 2 | `ELO_REPORT.md` |
| Late-move reduction (LMR) | 2 | `ELO_REPORT.md` |
| Late-move pruning (LMP) | 2 | `ELO_REPORT.md` |
| Futility pruning | 2 | `ELO_REPORT.md` |
| Razoring | 2 | `ELO_REPORT.md` |
| Evaluation/PST | 2 | `src/evaluate.cpp` |
| King safety | 2 | `ELO_REPORT.md` |
| Pawn structure | 2 | `ELO_REPORT.md` |
| Mobility | 2 | `ELO_REPORT.md` |
| Alpha-beta | 1 | `ELO_REPORT.md` |
| Iterative deepening | 1 | `src/search.cpp` |
| Aspiration windows | 1 | `src/search.cpp` |

## Interaction profile

- Total user prompts (both agents): **18**
- Avg prompt length: 2403.3 chars
- Intent distribution:
  - BugFixRequest: 10
  - Constraint: 10
  - FeatureRequest: 9
  - TestRequest: 9
  - Scenario: 6
  - Documentation: 4
  - Other: 4
  - ToolingBuild: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Claude Code (subagent) — 2026-02-10 18:52 — session `agent-a1`_

```
Design a detailed implementation plan for a C++ chess engine with these requirements:

**Target**: 2000+ Elo rating
**Board representation**: Bitboards (64-bit integers)
**Testing**: cutechess-cli for engine-vs-engine matches
**Protocol**: UCI (Universal Chess Interface) for compatibility with cutechess-cli and GUIs

Design the full architecture including:

1. **Project structure** - files, build system (CMake or Makefile)
2. **Bitboard representation** - how to represent board state, piece positions, castling rights, en passant
3. **Move generation** - pseudo-legal then legal filtering, magic bitboards for sliding pieces, precomputed attack tables
4. **Move encoding** - compact move representation
5. **Search algorithm** - iterative deepening + alpha-beta + PVS (principal variation search)
6. **Search enhancements** needed for 2000+ Elo:
   - Quiescence search
   - Transposition table (Zobrist hashing)
   - Null-move pruning
   - Late move reductions (LMR)
   - Killer moves and history heuristic
   - Aspiration windows
7. **Evaluation function**:
   - Material counting
   - Piece-square tables (middlegame + endgame with tapered eval)
   - Pawn structure (doubled, isolated, passed pawns)
   - King safety
   - Mobility
8. **UCI protocol** implementation - enough to work with cutechess-cli (position, go, bestmove, etc.)
9. **Time management** - allocating time per move
10. **Testing strategy** - perft for move generation correctness, cutechess-cli setup

Provide a phased implem
```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-10 20:33 | Claude Code (subagent) | FeatureRequest,BugFixRequest | I'm working on a chess engine in /Users/mathieuacher/SANDBOX/chess-cplusplus-claude/. The engine crashes at depth 15 in the search. The nod… |
| 3 | 2026-02-10 20:49 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 4 | 2026-02-10 22:03 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 5 | 2026-02-11 07:48 | Claude Code (subagent) | Other | Explore the chess engine search code thoroughly. I need to understand: 1. In `src/search.cpp` and `src/search.h`: What search techniques ar… |
| 6 | 2026-02-11 07:48 | Claude Code (subagent) | Scenario | Explore the chess engine evaluation code thoroughly. I need to understand: 1. In `src/evaluate.h` and `src/evaluate.cpp`: What evaluation f… |
| 7 | 2026-02-11 07:49 | Claude Code (subagent) | BugFixRequest,TestRequest | I'm designing improvements for a chess engine (Claudius) currently rated ~1650 Elo. The goal is to significantly strengthen it. Here's what… |
| 8 | 2026-02-11 10:54 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 9 | 2026-02-16 20:55 | Claude Code (subagent) | Other | Thoroughly explore the chess engine search implementation in /Users/mathieuacher/SANDBOX/chess-cplusplus-claude/src/search.cpp and /Users/m… |
| 10 | 2026-02-16 20:55 | Claude Code (subagent) | Scenario | Thoroughly explore the chess engine evaluation and move picking in /Users/mathieuacher/SANDBOX/chess-cplusplus-claude/src/evaluate.cpp, /Us… |
| 11 | 2026-02-16 20:56 | Claude Code (subagent) | FeatureRequest,BugFixRequest | I'm working on a chess engine (Claudius) currently at ~1850 Elo, targeting 2000-2200 Elo. The engine uses C++17, magic bitboards, tapered P… |
| 12 | 2026-02-17 11:42 | Claude Code (subagent) | Other | I'm looking at a chess engine (Claudius) at ~1920 Elo trying to reach 2000+. Explore src/search.cpp, src/search.h, src/movepick.h, src/move… |
| 13 | 2026-02-17 11:42 | Claude Code (subagent) | Scenario | I'm looking at a chess engine (Claudius) at ~1920 Elo trying to reach 2000+. Explore src/evaluate.cpp, src/evaluate.h, src/position.h, src/… |
| 14 | 2026-02-17 11:44 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Design an implementation plan for pushing a chess engine (Claudius) from ~1920 Elo to 2000+ Elo. The engine is in /Users/mathieuacher/SANDB… |
| 15 | 2026-02-17 11:47 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 16 | 2026-02-17 15:27 | Claude Code (subagent) | Other | Thoroughly analyze the chess engine's search implementation in src/search.cpp and src/search.h. I need to understand: 1. The complete list … |
| 17 | 2026-02-17 15:27 | Claude Code (subagent) | BugFixRequest,Constraint | Thoroughly analyze the chess engine's evaluation (src/evaluate.cpp, src/evaluate.h) and move ordering (src/movepick.h, src/movepick.cpp) fo… |
| 18 | 2026-02-17 15:31 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Design a concrete Batch 5 implementation plan for the Claudius chess engine to push from ~1946 to 2000+ Elo. The engine is C++17, single-th… |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `97e5511` | 2026-02-18T20:56:09+01:00 | Mathieu Acher | Batch 5: search improvements, ~2000 Elo (+54 from ~1946) |
| `b843fe0` | 2026-02-17T16:24:59+01:00 | Mathieu Acher | Update Elo report with Batch 4 results (~1946 Elo) |
| `b9b1e51` | 2026-02-17T16:22:47+01:00 | Mathieu Acher | Batch 4: search + eval enhancements, ~1946 Elo (+26 from ~1920) |
| `39285ab` | 2026-02-17T12:33:11+01:00 | Mathieu Acher | Batch 3: advanced search features, ~1920 Elo (+70 from ~1850) |
| `ccca712` | 2026-02-16T21:51:57+01:00 | Mathieu Acher | Claudius chess engine v1.0 — ~1850 Elo |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **11** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, ToolingBuild, Scenario) [2026-02-10 18:52] — Design a detailed implementation plan for a C++ chess engine with these requirements: **Target**: 2000+ Elo rating **Board representation**: Bitboards (64-bit integers) **Testing*… [T:Claude Code (subagent)/agent-a1]
- **BL-002** (FeatureRequest, BugFixRequest, TestRequest, Constraint, Scenario) [2026-02-10 20:33] — I'm working on a chess engine in /Users/mathieuacher/SANDBOX/chess-cplusplus-claude/. The engine crashes at depth 15 in the search. The node counts are extremely low (83K at depth… [T:Claude Code (subagent)/agent-a1]
- **BL-003** (FeatureRequest, BugFixRequest, TestRequest, Documentation, Constraint) [2026-02-10 20:49] — Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previous actions. This summary should be thor… [T:Claude Code (subagent)/agent-ac]
- **BL-004** (Scenario) [2026-02-11 07:48] — Explore the chess engine evaluation code thoroughly. I need to understand: 1. In `src/evaluate.h` and `src/evaluate.cpp`: What evaluation features are currently implemented? Look … [T:Claude Code (subagent)/agent-aa]
- **BL-005** (BugFixRequest, TestRequest, Constraint, Scenario) [2026-02-11 07:49] — I'm designing improvements for a chess engine (Claudius) currently rated ~1650 Elo. The goal is to significantly strengthen it. Here's what's currently implemented and what's miss… [T:Claude Code (subagent)/agent-aa]
- **BL-006** (Scenario) [2026-02-16 20:55] — Thoroughly explore the chess engine evaluation and move picking in /Users/mathieuacher/SANDBOX/chess-cplusplus-claude/src/evaluate.cpp, /Users/mathieuacher/SANDBOX/chess-cplusplus… [T:Claude Code (subagent)/agent-a4]
- **BL-007** (FeatureRequest, BugFixRequest, TestRequest, Constraint) [2026-02-16 20:56] — I'm working on a chess engine (Claudius) currently at ~1850 Elo, targeting 2000-2200 Elo. The engine uses C++17, magic bitboards, tapered PeSTO eval, and alpha-beta with PVS. **Wh… [T:Claude Code (subagent)/agent-a1]
- **BL-008** (Scenario) [2026-02-17 11:42] — I'm looking at a chess engine (Claudius) at ~1920 Elo trying to reach 2000+. Explore src/evaluate.cpp, src/evaluate.h, src/position.h, src/position.cpp to identify safe, conservat… [T:Claude Code (subagent)/agent-a6]
- **BL-009** (FeatureRequest, BugFixRequest, Constraint) [2026-02-17 11:44] — Design an implementation plan for pushing a chess engine (Claudius) from ~1920 Elo to 2000+ Elo. The engine is in /Users/mathieuacher/SANDBOX/chess-cplusplus-claude. ## Key constr… [T:Claude Code (subagent)/agent-af]
- **BL-010** (BugFixRequest, Constraint) [2026-02-17 15:27] — Thoroughly analyze the chess engine's evaluation (src/evaluate.cpp, src/evaluate.h) and move ordering (src/movepick.h, src/movepick.cpp) for improvement opportunities. The engine … [T:Claude Code (subagent)/agent-af]
- **BL-011** (FeatureRequest, BugFixRequest, TestRequest, Constraint) [2026-02-17 15:31] — Design a concrete Batch 5 implementation plan for the Claudius chess engine to push from ~1946 to 2000+ Elo. The engine is C++17, single-threaded, uses magic bitboards and PeSTO e… [T:Claude Code (subagent)/agent-a0]

## Evidence pointers

- [R:chess-cplusplus-claude] — repo at `/Users/mathieuacher/SANDBOX/chess-cplusplus-claude`
- [T:chess-cplusplus-claude/claude] — Claude sessions at `~/.claude/projects/chess-cplusplus-claude...`
- [T:chess-cplusplus-claude/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-cplusplus-claude

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.