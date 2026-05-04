# COBOL-chess

_Evidence-based dossier. Generated 2026-04-22 14:52 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/COBOL-chess` [R:COBOL-chess]
- **Primary language:** COBOL
- **Coding agent(s):** Claude Code, Claude Code subagents, Codex
- **Period:** 2026-02-09 09:42 → 2026-04-16 09:40
- **LOC by language:** COBOL (3854 LOC, 11 files), Text (2181 LOC, 1 files), Markdown (1149 LOC, 4 files), JSON (983 LOC, 55 files), Python (681 LOC, 4 files), Shell (42 LOC, 1 files)
- **Totals:** 76 files, 8890 LOC [S:scan]
- **Git:** 1 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 1 main + 5 subagent transcripts [T:COBOL-chess/claude]
- Claude models seen: <synthetic>, claude-opus-4-6
- Codex sessions: 2 [T:COBOL-chess/codex]
- Codex models seen: gpt-5.2, gpt-5.4

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 1 | 8 | 53152 | 44782 | 5121398 | 474819 | $20.74 |
| Codex | 2 | 25 | 236150053 | 1146954 | 232432640 | — | $335.71 |
| **Total** |  |  |  |  |  |  | **$356.45** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| Castling | 61 | `ARCHITECTURE.md` |
| Time management | 61 | `ARCHITECTURE.md` |
| PGN | 60 | `ARCHITECTURE.md` |
| FEN parsing | 27 | `ARCHITECTURE.md` |
| Material counting | 13 | `SPECIFICATION.md` |
| UCI protocol | 11 | `SPECIFICATION.md` |
| Perft | 9 | `SPECIFICATION.md` |
| Promotion | 9 | `ARCHITECTURE.md` |
| Transposition table | 8 | `ARCHITECTURE.md` |
| Quiescence | 7 | `SPECIFICATION.md` |
| Check/Checkmate | 6 | `ARCHITECTURE.md` |
| Board: 0x88 | 6 | `SPECIFICATION.md` |
| Alpha-beta | 6 | `SPECIFICATION.md` |
| Board: mailbox 8x8 | 5 | `SPECIFICATION.md` |
| Iterative deepening | 5 | `SPECIFICATION.md` |
| Null-move pruning | 5 | `ARCHITECTURE.md` |
| Aspiration windows | 5 | `ARCHITECTURE.md` |
| Pawn structure | 5 | `ARCHITECTURE.md` |
| Zobrist hashing | 4 | `ARCHITECTURE.md` |
| Move ordering (MVV-LVA) | 4 | `ARCHITECTURE.md` |
| Killer moves | 4 | `ARCHITECTURE.md` |
| History heuristic | 4 | `ARCHITECTURE.md` |
| Principal-variation (PV) | 4 | `ARCHITECTURE.md` |
| Late-move reduction (LMR) | 4 | `ARCHITECTURE.md` |
| Opening book | 4 | `ARCHITECTURE.md` |
| En passant | 3 | `ARCHITECTURE.md` |
| Minimax/Negamax | 3 | `ARCHITECTURE.md` |
| Late-move pruning (LMP) | 3 | `ARCHITECTURE.md` |
| King safety | 3 | `SPECIFICATION_BACKLOG.md` |
| Board: bitboard | 2 | `ARCHITECTURE.md` |
| Evaluation/PST | 2 | `SPECIFICATION.md` |
| Mobility | 2 | `ARCHITECTURE.md` |
| Endgame tables | 2 | `ARCHITECTURE.md` |
| Tapered evaluation | 1 | `2026-03-19-163737-you-are-a-post-session-backlog-strategy-analyst.txt` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | exec_command | 900 |
| Codex | write_stdin | 836 |
| Claude | Bash | 41 |
| Codex | update_plan | 6 |
| Claude | Read | 5 |
| Claude | Agent | 5 |
| Claude | Write | 2 |
| Codex | request_user_input | 2 |
| Claude | Glob | 1 |
| Claude | Edit | 1 |

## Interaction profile

- Total user prompts (both agents): **36**
- Avg prompt length: 1665.2 chars
- Intent distribution:
  - FeatureRequest: 18
  - TestRequest: 15
  - ToolingBuild: 15
  - Scenario: 14
  - BugFixRequest: 12
  - Other: 11
  - Constraint: 9
  - Documentation: 4
  - Question: 2
  - RefactorRequest: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-02-09 09:42 — session `rollout-`_

```
I want to build a chess engine in COBOL (GNUCobol)... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-09 10:25 | Codex | FeatureRequest,BugFixRequest | PLEASE IMPLEMENT THIS PLAN: # COBOL (GnuCOBOL) UCI Chess Engine + Elo Harness ## Summary Build a playable chess engine in **GNUCobol 3.2.x*… |
| 3 | 2026-02-09 11:26 | Codex | FeatureRequest,ToolingBuild | mathieuacher@Mathieus-MacBook-Pro COBOL-chess % make build make: Nothing to be done for `build'. |
| 4 | 2026-02-09 12:42 | Codex | BugFixRequest,ToolingBuild | mathieuacher@Mathieus-MacBook-Pro COBOL-chess % python3 tools/elo_calc.py /Users/mathieuacher/SANDBOX/COBOL-chess/results/match_20260209_13… |
| 5 | 2026-02-09 18:37 | Codex | Other | it's working but it's not accurate: there is a mix of games with white and black side, and it seems to assume that the engine under study a… |
| 6 | 2026-02-09 18:47 | Codex | Other | Elo rating of cobochess is not good at all... before trying to improve it, is it possible to investigate whether there is a misconfiguratio… |
| 7 | 2026-02-09 19:37 | Codex | Other | depth 4: is it for cobochess? such a depth is very low |
| 8 | 2026-02-09 19:41 | Codex | Other | I basically want to see games of the best "variant" of cobochess |
| 9 | 2026-02-09 19:57 | Codex | Other | OK... the current implementation is very weak. Try to significantly improve the engine |
| 10 | 2026-02-10 10:19 | Codex | Other | good... let's try to beat Stockfish @1600 now |
| 11 | 2026-02-10 17:34 | Codex | Other | sounds good, and indeed estimated 1600 Elo... now try to significanlty improve the strenght of the engine |
| 12 | 2026-02-10 18:38 | Codex | Other | continue... |
| 13 | 2026-02-10 21:45 | Codex | Question | how to assess new Elo rating ? |
| 14 | 2026-02-10 21:47 | Codex | FeatureRequest,TestRequest | mathieuacher@Mathieus-MacBook-Pro COBOL-chess % make clean build rm -f bin/cobochess *.o cobc -free -O2 -frecursive -Wall -x -o bin/coboche… |
| 15 | 2026-02-10 22:16 | Codex | FeatureRequest,BugFixRequest | mathieuacher@Mathieus-MacBook-Pro COBOL-chess % cd /Users/mathieuacher/SANDBOX/COBOL-chess && make clean build && make perft && make uci-sm… |
| 16 | 2026-02-10 22:28 | Codex | FeatureRequest,BugFixRequest | mathieuacher@Mathieus-MacBook-Pro COBOL-chess % cd /Users/mathieuacher/SANDBOX/COBOL-chess && make clean build && make perft rm -f bin/cobo… |
| 17 | 2026-02-11 07:46 | Codex | FeatureRequest,BugFixRequest | mathieuacher@Mathieus-MacBook-Pro COBOL-chess % cd /Users/mathieuacher/SANDBOX/COBOL-chess && make clean build && make perft && make uci-sm… |
| 18 | 2026-02-11 08:10 | Codex | FeatureRequest,TestRequest | mathieuacher@Mathieus-MacBook-Pro COBOL-chess % cd /Users/mathieuacher/SANDBOX/COBOL-chess xattr -l bin/cobochess xattr -d com.apple.quaran… |
| 19 | 2026-02-11 08:24 | Codex | FeatureRequest,BugFixRequest | mathieuacher@Mathieus-MacBook-Pro COBOL-chess % cd /Users/mathieuacher/SANDBOX/COBOL-chess && make clean build && make perft && make uci-sm… |
| 20 | 2026-02-11 09:20 | Codex | FeatureRequest,BugFixRequest | still the issue to build cd /Users/mathieuacher/SANDBOX/COBOL-chess && make clean build && make perft && make uci-smoke rm -f bin/cobochess… |
| 21 | 2026-02-11 10:01 | Codex | Other | I didn't give the permission but actually fine with the last command, sorry |
| 22 | 2026-02-11 10:20 | Codex | FeatureRequest,BugFixRequest | /Users/mathieuacher/SANDBOX/COBOL-chess/bin/cobochess: Mach header magic cputype cpusubtype caps filetype ncmds sizeofcmds flags MH_MAGIC A… |
| 23 | 2026-02-11 10:31 | Codex | FeatureRequest,BugFixRequest | mathieuacher@Mathieus-MacBook-Pro COBOL-chess % cd /Users/mathieuacher/SANDBOX/COBOL-chess && make clean build && make perft && make uci-sm… |
| 24 | 2026-02-11 10:49 | Codex | FeatureRequest,BugFixRequest | mathieuacher@Mathieus-MacBook-Pro COBOL-chess % cd /Users/mathieuacher/SANDBOX/COBOL-chess && make clean build && make perft && make uci-sm… |
| 25 | 2026-03-19 12:54 | Claude Code | FeatureRequest,BugFixRequest | You are a “Post-Session Backlog & Strategy Analyst” operating locally inside the current repository. PRIMARY GOAL Produce an evidence-based… |
| 26 | 2026-03-19 13:05 | Claude Code (subagent) | BugFixRequest,TestRequest | Read the Codex session file at ~/.codex/sessions/2026/02/09/rollout-2026-02-09T10-42-20-019c41c7-d33c-7e03-89a7-1691d6ab564a.jsonl This is … |
| 27 | 2026-03-19 13:05 | Claude Code (subagent) | Other | Read the Codex session file at ~/.codex/sessions/2026/02/19/rollout-2026-02-19T13-01-27-019c75c6-c737-7522-b22d-99cdb231bd10.jsonl This is … |
| 28 | 2026-03-19 13:05 | Claude Code (subagent) | FeatureRequest,TestRequest | Read ALL COBOL source files and copybooks in /Users/mathieuacher/SANDBOX/COBOL-chess. Specifically read: - src/main.cob - src/board.cob - s… |
| 29 | 2026-03-19 13:05 | Claude Code (subagent) | TestRequest,Scenario | Analyze the match results in /Users/mathieuacher/SANDBOX/COBOL-chess/results/ 1. List all .json files and read each one to get match metada… |
| 30 | 2026-03-19 14:00 | Codex | FeatureRequest,Documentation | Please analyze thorughly the repo and write a README.md to document the architecture and features (being heavily inspired by the README of … |
| 31 | 2026-03-19 14:07 | Claude Code | FeatureRequest,Documentation | can you write the content of README.md in another Markdown file called SPECIFICATION.md? |
| 32 | 2026-03-19 14:33 | Claude Code | FeatureRequest | nice! the Feature Backlog is correct (based on user request), but I'd like to have another perspective, more centric to what the agent has … |
| 33 | 2026-03-19 14:33 | Claude Code (subagent) | Constraint | I need to verify which specific chess engine features are actually present in the final codebase at /Users/mathieuacher/SANDBOX/COBOL-chess… |
| 34 | 2026-03-19 15:34 | Claude Code | Other | please git commit and push to Github in agentic-chessengine-cobol-codex |
| 35 | 2026-03-19 15:37 | Claude Code | Constraint | <local-command-caveat>Caveat: The messages below were generated by the user while running local commands. DO NOT respond to these messages … |
| 36 | 2026-04-16 09:40 | Claude Code | Constraint | <local-command-caveat>Caveat: The messages below were generated by the user while running local commands. DO NOT respond to these messages … |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `faf0f16` | 2026-03-19T16:36:49+01:00 | Mathieu Acher | Initial commit: cobochess — COBOL (GnuCOBOL) UCI chess engine (~1600-1700 Elo) |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **18** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, ToolingBuild) [2026-02-09 09:42] — I want to build a chess engine in COBOL (GNUCobol)... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "… [T:Codex/rollout-]
- **BL-002** (FeatureRequest, BugFixRequest, TestRequest, Documentation, ToolingBuild, Constraint, Scenario) [2026-02-09 10:25] — PLEASE IMPLEMENT THIS PLAN: # COBOL (GnuCOBOL) UCI Chess Engine + Elo Harness ## Summary Build a playable chess engine in **GNUCobol 3.2.x** that speaks **UCI**, using a **0x88 ma… [T:Codex/rollout-]
- **BL-003** (FeatureRequest, ToolingBuild) [2026-02-09 11:26] — mathieuacher@Mathieus-MacBook-Pro COBOL-chess % make build make: Nothing to be done for `build'. [T:Codex/rollout-]
- **BL-004** (BugFixRequest, ToolingBuild, Scenario) [2026-02-09 12:42] — mathieuacher@Mathieus-MacBook-Pro COBOL-chess % python3 tools/elo_calc.py /Users/mathieuacher/SANDBOX/COBOL-chess/results/match_20260209_131301.pgn --baseline-elo 1320 Traceback (… [T:Codex/rollout-]
- **BL-005** (FeatureRequest, TestRequest, ToolingBuild, Scenario) [2026-02-10 21:47] — mathieuacher@Mathieus-MacBook-Pro COBOL-chess % make clean build rm -f bin/cobochess *.o cobc -free -O2 -frecursive -Wall -x -o bin/cobochess src/main.cob src/board.cob src/fen.co… [T:Codex/rollout-]
- **BL-006** (FeatureRequest, BugFixRequest, TestRequest, ToolingBuild, Scenario) [2026-02-10 22:16] — mathieuacher@Mathieus-MacBook-Pro COBOL-chess % cd /Users/mathieuacher/SANDBOX/COBOL-chess && make clean build && make perft && make uci-smoke rm -f bin/cobochess *.o cobc -free -… [T:Codex/rollout-]
- **BL-007** (FeatureRequest, BugFixRequest, TestRequest, ToolingBuild, Scenario) [2026-02-10 22:28] — mathieuacher@Mathieus-MacBook-Pro COBOL-chess % cd /Users/mathieuacher/SANDBOX/COBOL-chess && make clean build && make perft rm -f bin/cobochess *.o *.c *.i *.c.h *.c.l*.h cobc -f… [T:Codex/rollout-]
- **BL-008** (FeatureRequest, TestRequest, ToolingBuild, Scenario) [2026-02-11 08:10] — mathieuacher@Mathieus-MacBook-Pro COBOL-chess % cd /Users/mathieuacher/SANDBOX/COBOL-chess xattr -l bin/cobochess xattr -d com.apple.quarantine bin/cobochess || true # if the whol… [T:Codex/rollout-]
- **BL-009** (FeatureRequest, BugFixRequest, TestRequest, ToolingBuild, Scenario) [2026-02-11 09:20] — still the issue to build cd /Users/mathieuacher/SANDBOX/COBOL-chess && make clean build && make perft && make uci-smoke rm -f bin/cobochess *.o *.c *.i *.c.h *.c.l*.h cobc -free -… [T:Codex/rollout-]
- **BL-010** (FeatureRequest, BugFixRequest, ToolingBuild, Constraint) [2026-02-11 10:20] — /Users/mathieuacher/SANDBOX/COBOL-chess/bin/cobochess: Mach header magic cputype cpusubtype caps filetype ncmds sizeofcmds flags MH_MAGIC ARM64 ALL 0x00 EXECUTE 12 1256 NOUNDEFS D… [T:Codex/rollout-]
- **BL-011** (FeatureRequest, BugFixRequest, RefactorRequest, TestRequest, Documentation, ToolingBuild, Constraint, Scenario) [2026-03-19 12:54] — You are a “Post-Session Backlog & Strategy Analyst” operating locally inside the current repository. PRIMARY GOAL Produce an evidence-based, reproducible post-session report using… [T:Claude Code/fe558a17]
- **BL-012** (BugFixRequest, TestRequest, Constraint) [2026-03-19 13:05] — Read the Codex session file at ~/.codex/sessions/2026/02/09/rollout-2026-02-09T10-42-20-019c41c7-d33c-7e03-89a7-1691d6ab564a.jsonl This is a large JSONL file (~37MB). I need you t… [T:Claude Code (subagent)/agent-a0]
- **BL-013** (FeatureRequest, TestRequest, Scenario) [2026-03-19 13:05] — Read ALL COBOL source files and copybooks in /Users/mathieuacher/SANDBOX/COBOL-chess. Specifically read: - src/main.cob - src/board.cob - src/fen.cob - src/attack.cob - src/movege… [T:Claude Code (subagent)/agent-a4]
- **BL-014** (TestRequest, Scenario) [2026-03-19 13:05] — Analyze the match results in /Users/mathieuacher/SANDBOX/COBOL-chess/results/ 1. List all .json files and read each one to get match metadata (they are small) 2. Read the first 20… [T:Claude Code (subagent)/agent-ae]
- **BL-015** (FeatureRequest, Documentation) [2026-03-19 14:00] — Please analyze thorughly the repo and write a README.md to document the architecture and features (being heavily inspired by the README of https://github.com/acherm/agentic-chesse… [T:Codex/rollout-]
- **BL-016** (FeatureRequest) [2026-03-19 14:33] — nice! the Feature Backlog is correct (based on user request), but I'd like to have another perspective, more centric to what the agent has done... basically, numerous "features" h… [T:Claude Code/fe558a17]
- **BL-017** (Constraint) [2026-03-19 14:33] — I need to verify which specific chess engine features are actually present in the final codebase at /Users/mathieuacher/SANDBOX/COBOL-chess. Read the following files and list ever… [T:Claude Code (subagent)/agent-a7]
- **BL-018** (Constraint) [2026-03-19 15:37] — <local-command-caveat>Caveat: The messages below were generated by the user while running local commands. DO NOT respond to these messages or otherwise consider them in your respo… [T:Claude Code/fe558a17]

## Evidence pointers

- [R:COBOL-chess] — repo at `/Users/mathieuacher/SANDBOX/COBOL-chess`
- [T:COBOL-chess/claude] — Claude sessions at `~/.claude/projects/COBOL-chess...`
- [T:COBOL-chess/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/COBOL-chess

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.