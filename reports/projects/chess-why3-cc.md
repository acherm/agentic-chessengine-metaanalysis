# chess-why3-cc

_Evidence-based dossier. Generated 2026-04-22 14:53 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-why3-cc` [R:chess-why3-cc]
- **Primary language:** C
- **Coding agent(s):** Claude Code subagents
- **Period:** —
- **LOC by language:** C (44283 LOC, 124 files), C++ (18378 LOC, 45 files), Text (15092 LOC, 13 files), OCaml (9772 LOC, 24 files), Why3 (1608 LOC, 8 files), LaTeX (862 LOC, 1 files), Markdown (634 LOC, 7 files), Shell (486 LOC, 4 files)
- **Totals:** 234 files, 91558 LOC [S:scan]
- **Git:** 3 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 6 subagent transcripts [T:chess-why3-cc/claude]
- Claude models seen: —
- Codex sessions: 0 [T:chess-why3-cc/codex]
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
| Castling | 62 | `fixup.sh` |
| Board: bitboard | 45 | `tests/elo_test.sh` |
| Time management | 44 | `ocaml/uci.ml` |
| UCI protocol | 39 | `ocaml/uci.ml` |
| Transposition table | 39 | `ocaml/uci.ml` |
| Material counting | 39 | `ocaml/engine.ml` |
| Promotion | 34 | `ocaml/bridge.ml` |
| En passant | 32 | `ocaml/bridge.ml` |
| Quiescence | 30 | `ocaml/engine.ml` |
| FEN parsing | 26 | `ocaml/uci.ml` |
| Check/Checkmate | 26 | `ocaml/engine.ml` |
| Null-move pruning | 26 | `ocaml/engine.ml` |
| Opening book | 24 | `tests/setup_engines.sh` |
| PGN | 23 | `tests/setup_engines.sh` |
| Pawn structure | 22 | `ocaml/search_ocaml.ml` |
| Perft | 18 | `Makefile` |
| Minimax/Negamax | 18 | `tests/elo_test.sh` |
| Alpha-beta | 18 | `ocaml/engine.ml` |
| Zobrist hashing | 18 | `ocaml/uci.ml` |
| Killer moves | 17 | `tests/elo_test.sh` |
| Iterative deepening | 16 | `ocaml/uci.ml` |
| Principal-variation (PV) | 15 | `tests/results/ASSESSMENT.md` |
| NNUE/neural eval | 15 | `tests/setup_engines.sh` |
| Late-move reduction (LMR) | 13 | `ocaml/search_ocaml.ml` |
| Move ordering (MVV-LVA) | 11 | `tests/elo_test.sh` |
| Board: magic bitboards | 10 | `tests/engines/bbc` |
| Evaluation/PST | 9 | `tests/engines/shallowblue-src/README.md` |
| Mobility | 9 | `tests/results/ASSESSMENT.md` |
| History heuristic | 8 | `tests/elo_test.sh` |
| Tapered evaluation | 7 | `tests/elo_test.sh` |
| King safety | 6 | `tests/results/ASSESSMENT.md` |
| Board: 0x88 | 5 | `tests/elo_test.sh` |
| Endgame tables | 5 | `tests/engines/bbc-src/pgn/bbc_1.3_nnue_vs_vice/Arena Tournament.at` |
| Aspiration windows | 4 | `ocaml/uci.ml` |
| Razoring | 4 | `tests/engines/bbc-src/README.md` |
| Board: mailbox 8x8 | 2 | `tests/elo_test.sh` |
| Futility pruning | 2 | `tests/results/ASSESSMENT.md` |
| Late-move pruning (LMP) | 1 | `tests/engines/bbc-src/issues/BBC1.vs.Plankton64mt_04.txt` |

## Interaction profile

- Total user prompts (both agents): **6**
- Avg prompt length: 2698.5 chars
- Intent distribution:
  - TestRequest: 6
  - ToolingBuild: 3
  - Scenario: 3
  - FeatureRequest: 3
  - Constraint: 3
  - BugFixRequest: 2
  - Documentation: 2

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Claude Code (subagent) — 2026-02-17 12:55 — session `agent-aa`_

```
Research the following topics thoroughly:

1. **WhyML / Why3 language capabilities**: What are the key features and limitations of WhyML for writing a chess engine? Consider:
   - Data types (arrays, records, algebraic types)
   - Mutable state support
   - Extraction to OCaml (or C) — how does code extraction work?
   - Standard library (what's available: arrays, hash tables, etc.)
   - Limitations: no floating point? No I/O? How to handle UCI protocol?

2. **WhyML code extraction**: How does `why3 extract` work? Can you extract WhyML to OCaml and then compile it as a standalone binary? What are the gotchas?

3. **Chess engine in WhyML/Why3**: Search the web for any existing projects or papers that have built a chess engine or similar game engine in Why3/WhyML. 

4. **Elo testing tools**: What tools exist for testing chess engine Elo? (cutechess-cli, fastchess, OpenBench, etc.) How do they work?

5. **UCI protocol basics**: What's needed for a chess engine to communicate via UCI?

Search the web for information on these topics. Provide detailed findings.
```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-17 13:00 | Claude Code (subagent) | FeatureRequest,TestRequest | Design a detailed implementation plan for a chess engine written in WhyML (Why3's programming language) that will be extracted to OCaml and… |
| 3 | 2026-02-17 16:01 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 4 | 2026-02-18 16:50 | Claude Code (subagent) | TestRequest,Scenario | Research what chess engines are commonly available for Elo calibration testing on macOS, and how to properly set up a chess engine rating t… |
| 5 | 2026-02-18 19:53 | Claude Code (subagent) | TestRequest,ToolingBuild | Explore the project structure at /Users/mathieuacher/SANDBOX/chess-why3-cc. I need to understand: 1. Where the main chess engine binary is … |
| 6 | 2026-02-19 01:07 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `8cbf6a2` | 2026-02-19T15:44:12+01:00 | Mathieu Acher | Update ASSESSMENT.md with 1000-game tournament results and full engine analysis |
| `81a2d5b` | 2026-02-19T10:48:34+01:00 | Mathieu Acher | Add Elo evaluation framework with round-robin tournament against real engines |
| `15b0de1` | 2026-02-18T17:48:38+01:00 | Mathieu Acher | WhyChess: chess engine in WhyML (Why3) with OCaml UCI wrapper |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **5** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (TestRequest, ToolingBuild, Scenario) [2026-02-17 12:55] — Research the following topics thoroughly: 1. **WhyML / Why3 language capabilities**: What are the key features and limitations of WhyML for writing a chess engine? Consider: - Dat… [T:Claude Code (subagent)/agent-aa]
- **BL-002** (FeatureRequest, TestRequest, ToolingBuild, Constraint, Scenario) [2026-02-17 13:00] — Design a detailed implementation plan for a chess engine written in WhyML (Why3's programming language) that will be extracted to OCaml and compiled as a standalone UCI-compatible… [T:Claude Code (subagent)/agent-aa]
- **BL-003** (FeatureRequest, BugFixRequest, TestRequest, Documentation, Constraint) [2026-02-17 16:01] — Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previous actions. This summary should be thor… [T:Claude Code (subagent)/agent-ac]
- **BL-004** (TestRequest, Scenario) [2026-02-18 16:50] — Research what chess engines are commonly available for Elo calibration testing on macOS, and how to properly set up a chess engine rating tournament. I need to find: 1. What engin… [T:Claude Code (subagent)/agent-a5]
- **BL-005** (TestRequest, ToolingBuild) [2026-02-18 19:53] — Explore the project structure at /Users/mathieuacher/SANDBOX/chess-why3-cc. I need to understand: 1. Where the main chess engine binary is built (look at dune files, Makefile) 2. … [T:Claude Code (subagent)/agent-a1]

## Evidence pointers

- [R:chess-why3-cc] — repo at `/Users/mathieuacher/SANDBOX/chess-why3-cc`
- [T:chess-why3-cc/claude] — Claude sessions at `~/.claude/projects/chess-why3-cc...`
- [T:chess-why3-cc/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-why3-cc

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.