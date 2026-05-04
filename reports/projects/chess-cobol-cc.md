# chess-cobol-cc

_Evidence-based dossier. Generated 2026-04-22 14:52 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-cobol-cc` [R:chess-cobol-cc]
- **Primary language:** C
- **Coding agent(s):** Claude Code, Claude Code subagents
- **Period:** 2026-03-12 19:37 → 2026-03-30 18:28
- **LOC by language:** C (8118 LOC, 3 files), COBOL (3460 LOC, 1 files)
- **Totals:** 4 files, 11578 LOC [S:scan]
- **Git:** not a git repo

## Phase 0 — Session artifacts

- Claude Code sessions: 1 main + 7 subagent transcripts [T:chess-cobol-cc/claude]
- Claude models seen: <synthetic>, claude-opus-4-6
- Codex sessions: 0 [T:chess-cobol-cc/codex]
- Codex models seen: —

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 1 | 46 | 1937 | 591930 | 166713533 | 11943652 | $518.44 |
| Codex | 0 | 0 | 0 | 0 | 0 | — | $0.00 |
| **Total** |  |  |  |  |  |  | **$518.44** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| Time management | 45 | `cobolchess` |
| Castling | 25 | `phase5_vs1500.pgn` |
| FEN parsing | 20 | `cobolchess` |
| UCI protocol | 20 | `cobolchess` |
| Futility pruning | 3 | `chess-engine.c.l.h` |
| Evaluation/PST | 3 | `chess-engine.c.l.h` |
| Material counting | 3 | `chess-engine.c.l.h` |
| Check/Checkmate | 2 | `phase4d_timefix.pgn` |
| Transposition table | 2 | `chess-engine-test2` |
| En passant | 1 | `chess-engine.cob` |
| Promotion | 1 | `chess-engine.cob` |
| Minimax/Negamax | 1 | `chess-engine.cob` |
| Alpha-beta | 1 | `chess-engine.cob` |
| Iterative deepening | 1 | `chess-engine.cob` |
| Quiescence | 1 | `chess-engine.cob` |
| Move ordering (MVV-LVA) | 1 | `chess-engine.cob` |
| Killer moves | 1 | `chess-engine.cob` |
| History heuristic | 1 | `chess-engine.cob` |
| Principal-variation (PV) | 1 | `chess-engine.cob` |
| Late-move reduction (LMR) | 1 | `chess-engine.cob` |
| Aspiration windows | 1 | `chess-engine.cob` |
| Tapered evaluation | 1 | `chess-engine.cob` |
| Pawn structure | 1 | `chess-engine.cob` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Claude | Bash | 712 |
| Claude | Edit | 178 |
| Claude | Read | 143 |
| Claude | Grep | 57 |
| Claude | TaskOutput | 53 |
| Claude | Write | 9 |
| Claude | ToolSearch | 2 |
| Claude | Agent | 2 |

## Interaction profile

- Total user prompts (both agents): **37**
- Avg prompt length: 3914.9 chars
- Intent distribution:
  - Other: 19
  - FeatureRequest: 17
  - TestRequest: 16
  - Constraint: 15
  - BugFixRequest: 14
  - Scenario: 10
  - ToolingBuild: 9
  - Documentation: 5

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Claude Code — 2026-03-12 19:37 — session `9d9bb74e`_

```
I want to build a chess engine in COBOL (using GNU Cobol)… at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of “similar” levels.
```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-03-12 19:37 | Claude Code (subagent) | FeatureRequest,TestRequest | I want to build a chess engine in COBOL (using GNU Cobol)… at the end, I want to test this chess engine and assess its Elo rating, typicall… |
| 3 | 2026-03-12 19:41 | Claude Code | Other | Let's go for Phase 1 |
| 4 | 2026-03-12 19:41 | Claude Code (subagent) | Other | Let's go for Phase 1 |
| 5 | 2026-03-12 20:40 | Claude Code | Other | go to Phase 2 |
| 6 | 2026-03-12 20:40 | Claude Code (subagent) | Other | go to Phase 2 |
| 7 | 2026-03-12 21:44 | Claude Code | Other | go |
| 8 | 2026-03-12 21:44 | Claude Code (subagent) | Other | go |
| 9 | 2026-03-12 21:50 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 10 | 2026-03-12 21:52 | Claude Code | FeatureRequest,BugFixRequest | This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the c… |
| 11 | 2026-03-12 21:52 | Claude Code (subagent) | FeatureRequest,BugFixRequest | This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the c… |
| 12 | 2026-03-12 22:54 | Claude Code | Other | continue |
| 13 | 2026-03-12 22:54 | Claude Code (subagent) | Other | continue |
| 14 | 2026-03-13 08:46 | Claude Code | Other | continue |
| 15 | 2026-03-13 08:46 | Claude Code (subagent) | Other | continue |
| 16 | 2026-03-13 09:15 | Claude Code | Other | yes |
| 17 | 2026-03-13 09:15 | Claude Code (subagent) | Other | yes |
| 18 | 2026-03-14 08:23 | Claude Code | Other | status? |
| 19 | 2026-03-14 08:23 | Claude Code (subagent) | Other | status? |
| 20 | 2026-03-14 08:24 | Claude Code | Other | please go ahead and try to improve the Elo |
| 21 | 2026-03-14 08:24 | Claude Code (subagent) | Other | please go ahead and try to improve the Elo |
| 22 | 2026-03-16 19:49 | Claude Code | Other | please go ahead and try to improve the Elo |
| 23 | 2026-03-16 19:49 | Claude Code (subagent) | Other | please go ahead and try to improve the Elo |
| 24 | 2026-03-16 19:51 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 25 | 2026-03-16 19:53 | Claude Code | FeatureRequest,BugFixRequest | This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the c… |
| 26 | 2026-03-16 19:53 | Claude Code (subagent) | FeatureRequest,BugFixRequest | This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the c… |
| 27 | 2026-03-20 15:24 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 28 | 2026-03-20 15:26 | Claude Code | FeatureRequest,BugFixRequest | This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the c… |
| 29 | 2026-03-20 15:26 | Claude Code (subagent) | FeatureRequest,BugFixRequest | This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the c… |
| 30 | 2026-03-21 00:29 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 31 | 2026-03-21 00:30 | Claude Code | FeatureRequest,BugFixRequest | This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the c… |
| 32 | 2026-03-21 00:30 | Claude Code (subagent) | FeatureRequest,BugFixRequest | This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the c… |
| 33 | 2026-03-23 13:46 | Claude Code (subagent) | FeatureRequest,Constraint | I have a COBOL chess engine at ~1627 Elo. It currently has: - Alpha-beta with iterative deepening and aspiration windows - Quiescence searc… |
| 34 | 2026-03-23 14:53 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 35 | 2026-03-23 14:55 | Claude Code | FeatureRequest,BugFixRequest | This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the c… |
| 36 | 2026-03-23 20:20 | Claude Code (subagent) | Scenario | I'm working on a COBOL chess engine (chess-engine.cob). The engine currently has: - Alpha-beta with iterative deepening (max 20 plies) - Qu… |
| 37 | 2026-03-26 06:35 | Claude Code | Other | no refine the Elo assessment |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **5** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, ToolingBuild) [2026-03-12 19:37] — I want to build a chess engine in COBOL (using GNU Cobol)… at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines… [T:Claude Code/9d9bb74e]
- **BL-002** (FeatureRequest, BugFixRequest, TestRequest, Documentation, Constraint) [2026-03-12 21:50] — Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previous actions. This summary should be thor… [T:Claude Code (subagent)/agent-ac]
- **BL-003** (FeatureRequest, BugFixRequest, TestRequest, ToolingBuild, Constraint, Scenario) [2026-03-12 21:52] — This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation. Summary: 1. Primary Request… [T:Claude Code/9d9bb74e]
- **BL-004** (FeatureRequest, Constraint) [2026-03-23 13:46] — I have a COBOL chess engine at ~1627 Elo. It currently has: - Alpha-beta with iterative deepening and aspiration windows - Quiescence search with delta pruning - MVV-LVA move orde… [T:Claude Code (subagent)/agent-ad]
- **BL-005** (Scenario) [2026-03-23 20:20] — I'm working on a COBOL chess engine (chess-engine.cob). The engine currently has: - Alpha-beta with iterative deepening (max 20 plies) - Quiescence search with delta pruning - Lat… [T:Claude Code (subagent)/agent-a2]

## Evidence pointers

- [R:chess-cobol-cc] — repo at `/Users/mathieuacher/SANDBOX/chess-cobol-cc`
- [T:chess-cobol-cc/claude] — Claude sessions at `~/.claude/projects/chess-cobol-cc...`
- [T:chess-cobol-cc/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-cobol-cc

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.