# chess-polyglot-eval

_Evidence-based dossier. Generated 2026-04-22 14:53 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-polyglot-eval` [R:chess-polyglot-eval]
- **Primary language:** Python
- **Coding agent(s):** Claude Code subagents, Codex
- **Period:** 2026-02-19 17:12 → 2026-02-19 18:04
- **LOC by language:** Python (7613 LOC, 7 files), JSON (4031 LOC, 5 files), Markdown (2555 LOC, 7 files), HTML (837 LOC, 1 files), Shell (286 LOC, 1 files)
- **Totals:** 21 files, 15322 LOC [S:scan]
- **Git:** 5 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 85 subagent transcripts [T:chess-polyglot-eval/claude]
- Claude models seen: —
- Codex sessions: 1 [T:chess-polyglot-eval/codex]
- Codex models seen: gpt-5.3-codex

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 1 | 4 | 4281273 | 31348 | 3952640 | — | $6.16 |
| **Total** |  |  |  |  |  |  | **$6.16** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| Time management | 268 | `metrics.json` |
| Castling | 255 | `generate_session_viewer.py` |
| FEN parsing | 209 | `generate_session_viewer.py` |
| Material counting | 14 | `generate_session_viewer.py` |
| UCI protocol | 13 | `metrics.json` |
| Opening book | 11 | `metrics.json` |
| Board: bitboard | 9 | `metrics.json` |
| Board: mailbox 8x8 | 8 | `generate_session_viewer.py` |
| Minimax/Negamax | 8 | `metrics.json` |
| Alpha-beta | 8 | `metrics.json` |
| Iterative deepening | 8 | `metrics.json` |
| Quiescence | 8 | `metrics.json` |
| Transposition table | 8 | `metrics.json` |
| En passant | 7 | `generate_session_viewer.py` |
| Board: 0x88 | 7 | `metrics.json` |
| Killer moves | 7 | `metrics.json` |
| Principal-variation (PV) | 7 | `metrics.json` |
| Null-move pruning | 7 | `metrics.json` |
| Late-move reduction (LMR) | 7 | `metrics.json` |
| Aspiration windows | 7 | `metrics.json` |
| Futility pruning | 7 | `metrics.json` |
| Evaluation/PST | 7 | `generate_session_viewer.py` |
| King safety | 7 | `generate_session_viewer.py` |
| Perft | 6 | `generate_session_viewer.py` |
| Promotion | 6 | `collect_metrics.py` |
| PGN | 6 | `collect_metrics.py` |
| Board: magic bitboards | 6 | `metrics.json` |
| Zobrist hashing | 6 | `generate_session_viewer.py` |
| Move ordering (MVV-LVA) | 6 | `metrics.json` |
| Razoring | 6 | `generate_session_viewer.py` |
| Tapered evaluation | 6 | `generate_session_viewer.py` |
| Pawn structure | 6 | `generate_session_viewer.py` |
| Mobility | 6 | `generate_session_viewer.py` |
| Check/Checkmate | 5 | `AI_SESSIONS_ANALYSIS.md` |
| History heuristic | 5 | `metrics.json` |
| Late-move pruning (LMP) | 4 | `collect_metrics.py` |
| Board: mailbox 10x12 | 1 | `tournaments/ENGINES_REPORT.md` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | exec_command | 59 |

## Interaction profile

- Total user prompts (both agents): **89**
- Avg prompt length: 1547.1 chars
- Intent distribution:
  - Documentation: 49
  - Scenario: 43
  - FeatureRequest: 42
  - ToolingBuild: 36
  - TestRequest: 32
  - Constraint: 18
  - BugFixRequest: 18
  - Other: 12

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Claude Code (subagent) — 2026-02-16 18:11 — session `agent-a8`_

```
Explore the following chess engine projects in /Users/mathieuacher/SANDBOX. For each one, identify:
- Programming language and build system
- Directory structure and key files (README, source files, tests, config)
- Any documented features (e.g., move generation, search algorithms, evaluation, opening books, UCI support)
- Any Elo ratings mentioned
- Lines of code / project size
- Whether it was built with Codex or Claude Code (check for any agent markers, CLAUDE.md, .codex files, git logs, etc.)
- Any test suites or benchmarks

Projects to explore:
1. /Users/mathieuacher/SANDBOX/lean-chess
2. /Users/mathieuacher/SANDBOX/chess-cplusplus-claude
3. /Users/mathieuacher/SANDBOX/chess-py

Be very thorough - read READMEs, key source files, config files, and any documentation.
```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-16 18:11 | Claude Code (subagent) | FeatureRequest,TestRequest | Explore the following chess engine projects in /Users/mathieuacher/SANDBOX. For each one, identify: - Programming language and build system… |
| 3 | 2026-02-16 18:11 | Claude Code (subagent) | FeatureRequest,TestRequest | Explore the following chess engine projects in /Users/mathieuacher/SANDBOX. For each one, identify: - Programming language and build system… |
| 4 | 2026-02-16 18:16 | Claude Code (subagent) | TestRequest,Documentation | Design an implementation plan for analyzing 9 chess engine projects in /Users/mathieuacher/SANDBOX/. The deliverables are: 1. **A Python sc… |
| 5 | 2026-02-16 19:16 | Claude Code (subagent) | FeatureRequest,Documentation | Explore /Users/mathieuacher/SANDBOX/lean-chess thoroughly. I need to understand: 1. File structure (ls -la recursive, key directories) 2. L… |
| 6 | 2026-02-16 19:16 | Claude Code (subagent) | FeatureRequest,Documentation | Explore /Users/mathieuacher/SANDBOX/chess-cplusplus-claude thoroughly. I need to understand: 1. File structure (ls -la recursive, key direc… |
| 7 | 2026-02-16 19:16 | Claude Code (subagent) | FeatureRequest,Documentation | Explore /Users/mathieuacher/SANDBOX/chess-py thoroughly. I need to understand: 1. File structure (ls -la recursive, key directories) 2. Lan… |
| 8 | 2026-02-16 19:16 | Claude Code (subagent) | FeatureRequest,Documentation | Explore /Users/mathieuacher/SANDBOX/COBOL-chess thoroughly. I need to understand: 1. File structure (ls -la recursive, key directories) 2. … |
| 9 | 2026-02-16 19:16 | Claude Code (subagent) | FeatureRequest,Documentation | Explore /Users/mathieuacher/SANDBOX/cplusplus-chess thoroughly. I need to understand: 1. File structure (ls -la recursive, key directories)… |
| 10 | 2026-02-16 19:16 | Claude Code (subagent) | FeatureRequest,Documentation | Explore /Users/mathieuacher/SANDBOX/latex-chess-engine thoroughly. I need to understand: 1. File structure (ls -la recursive, key directori… |
| 11 | 2026-02-16 19:16 | Claude Code (subagent) | FeatureRequest,Documentation | Explore /Users/mathieuacher/SANDBOX/chess-sql thoroughly. I need to understand: 1. File structure (ls -la recursive, key directories) 2. La… |
| 12 | 2026-02-16 19:16 | Claude Code (subagent) | FeatureRequest,Documentation | Explore /Users/mathieuacher/SANDBOX/chess-purec thoroughly. I need to understand: 1. File structure (ls -la recursive, key directories) 2. … |
| 13 | 2026-02-16 19:16 | Claude Code (subagent) | FeatureRequest,Documentation | Explore /Users/mathieuacher/SANDBOX/chess-Rocq thoroughly. I need to understand: 1. File structure (ls -la recursive, key directories) 2. L… |
| 14 | 2026-02-16 20:55 | Claude Code (subagent) | Documentation,Scenario | Thoroughly investigate /Users/mathieuacher/SANDBOX/chess-py for agent provenance clues. Check: 1. Is there a .git directory? If so, check A… |
| 15 | 2026-02-16 20:55 | Claude Code (subagent) | Documentation | Thoroughly investigate /Users/mathieuacher/SANDBOX/chess-cplusplus-claude for better Elo estimation and provenance. Check: 1. Read ALL PGN … |
| 16 | 2026-02-16 20:55 | Claude Code (subagent) | Documentation | Investigate /Users/mathieuacher/SANDBOX/lean-chess for agent provenance. Check: 1. Is there a .git directory? If so, check ALL git log entr… |
| 17 | 2026-02-16 20:55 | Claude Code (subagent) | Documentation,ToolingBuild | Investigate /Users/mathieuacher/SANDBOX/COBOL-chess for agent provenance. Check: 1. Is there a .git directory? If so, check ALL git log ent… |
| 18 | 2026-02-16 20:56 | Claude Code (subagent) | Constraint,Scenario | I need an in-depth analysis of chess-related features across 9 chess engine projects. For each project below, I need you to READ the actual… |
| 19 | 2026-02-16 21:09 | Claude Code (subagent) | FeatureRequest,ToolingBuild | I need to understand how each of the 9 chess engines can be invoked as UCI engines for tournament play. For each project below, find: 1. **… |
| 20 | 2026-02-16 21:09 | Claude Code (subagent) | TestRequest,Scenario | Look at the existing tournament/match scripts across the chess projects to understand the patterns used. I need to design a unified tournam… |
| 21 | 2026-02-16 21:13 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 22 | 2026-02-16 21:15 | Claude Code (subagent) | FeatureRequest,ToolingBuild | Check which chess engine binaries/executables exist and are ready to run. For each of these 9 projects, verify if the engine binary/script … |
| 23 | 2026-02-16 21:17 | Claude Code (subagent) | FeatureRequest,ToolingBuild | Design a unified tournament system for evaluating 9 chess engines. This will be a Python script called `run_tournament.py` in `/Users/mathi… |
| 24 | 2026-02-16 21:26 | Claude Code (subagent) | FeatureRequest,TestRequest | Verify the following engine binaries and working directories exist. For each, just print whether it exists or not: 1. /Users/mathieuacher/S… |
| 25 | 2026-02-17 05:34 | Claude Code (subagent) | Other | In the chess-py and latex-chess-engine projects, check how their engines were previously invoked with cutechess-cli. Look for any wrapper s… |
| 26 | 2026-02-17 08:20 | Claude Code (subagent) | BugFixRequest,TestRequest | Very thorough analysis of the AI coding sessions that built the chess-purec engine at /Users/mathieuacher/SANDBOX/chess-purec. I need to un… |
| 27 | 2026-02-17 08:20 | Claude Code (subagent) | BugFixRequest,TestRequest | Very thorough analysis of the AI coding sessions that built the cplusplus-chess engine (Codex-built) at /Users/mathieuacher/SANDBOX/cpluspl… |
| 28 | 2026-02-17 08:20 | Claude Code (subagent) | BugFixRequest,TestRequest | Very thorough analysis of the AI coding sessions that built chess-cplusplus-claude (Claudius) at /Users/mathieuacher/SANDBOX/chess-cplusplu… |
| 29 | 2026-02-17 08:20 | Claude Code (subagent) | BugFixRequest,TestRequest | Very thorough analysis of the AI coding sessions that built lean-chess (LeanChess) at /Users/mathieuacher/SANDBOX/lean-chess. I need to und… |
| 30 | 2026-02-17 08:20 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Very thorough analysis of the AI coding sessions that built COBOL-chess (CoboChess) at /Users/mathieuacher/SANDBOX/COBOL-chess. I need to u… |
| 31 | 2026-02-17 08:20 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Very thorough analysis of the AI coding sessions that built chess-Rocq (ChessRocq) at /Users/mathieuacher/SANDBOX/chess-Rocq. I need to und… |
| 32 | 2026-02-17 08:21 | Claude Code (subagent) | BugFixRequest,TestRequest | Very thorough analysis of the AI coding sessions that built chess-py (ChessPy) at /Users/mathieuacher/SANDBOX/chess-py. I need to understan… |
| 33 | 2026-02-17 08:21 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Very thorough analysis of the AI coding sessions that built latex-chess-engine (TeXChess) at /Users/mathieuacher/SANDBOX/latex-chess-engine… |
| 34 | 2026-02-17 08:21 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Very thorough analysis of the AI coding sessions that built chess-sql (SQLChess) at /Users/mathieuacher/SANDBOX/chess-sql. I need to unders… |
| 35 | 2026-02-17 08:27 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 36 | 2026-02-17 08:30 | Claude Code (subagent) | TestRequest,Scenario | I need to understand what speed/performance metrics each of these 9 chess engines reports during UCI search. For each engine, search the so… |
| 37 | 2026-02-17 08:31 | Claude Code (subagent) | TestRequest,Scenario | For each of these chess engine projects, find the EXACT format of the perft command they accept via UCI/stdin. Search for how they parse th… |
| 38 | 2026-02-17 09:35 | Claude Code (subagent) | Other | Search across all 9 chess engine project directories for AI coding session data files. Look for: 1. Claude Code session files: `.claude/`, … |
| 39 | 2026-02-17 09:51 | Claude Code (subagent) | FeatureRequest,Documentation | Explore /Users/mathieuacher/SANDBOX/chess-mojo thoroughly: 1. Read the README if it exists 2. Check if there's a working UCI engine binary … |
| 40 | 2026-02-17 09:51 | Claude Code (subagent) | Documentation | Explore /Users/mathieuacher/SANDBOX/chess-rust-cc thoroughly: 1. Read the README if it exists 2. Check if there's a working UCI engine bina… |
| 41 | 2026-02-17 09:51 | Claude Code (subagent) | Documentation | Explore /Users/mathieuacher/SANDBOX/chess-rust-codex thoroughly: 1. Read the README if it exists 2. Check if there's a working UCI engine b… |
| 42 | 2026-02-17 09:52 | Claude Code (subagent) | Documentation | Explore /Users/mathieuacher/SANDBOX/chess-latex-codex-replication thoroughly: 1. Read the README if it exists 2. Check if there's a working… |
| 43 | 2026-02-17 09:52 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 44 | 2026-02-17 09:54 | Claude Code (subagent) | FeatureRequest,TestRequest | Verify the following 4 new chess engine projects exist and check their binary/command details: 1. chess-mojo: Check if `build/mojo_engine` … |
| 45 | 2026-02-17 13:43 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 46 | 2026-02-17 15:51 | Claude Code (subagent) | Documentation,Scenario | Search across all chess engine project directories in /Users/mathieuacher/SANDBOX/ for internal Elo assessments. Look for: 1. In chess-late… |
| 47 | 2026-02-17 15:54 | Claude Code (subagent) | Documentation | Read the following files and report their full contents: 1. /Users/mathieuacher/SANDBOX/latex-chess-engine/elo-games.pgn - just the first 2… |
| 48 | 2026-02-17 15:54 | Claude Code (subagent) | Other | Search across ALL chess engine project directories in /Users/mathieuacher/SANDBOX/ for any internal Elo assessment close to 2300 (say 2200-… |
| 49 | 2026-02-18 07:43 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 50 | 2026-02-18 09:29 | Claude Code (subagent) | Scenario | I need to understand the engine registry, cutechess-cli runner, and infrastructure in the existing tournament system to design a new Swiss-… |
| 51 | 2026-02-18 09:30 | Claude Code (subagent) | Scenario | Design a Swiss-system chess tournament script for 13 engines of varying speed tiers. The script will be at `/Users/mathieuacher/SANDBOX/che… |
| 52 | 2026-02-19 08:43 | Claude Code (subagent) | FeatureRequest,Documentation | I need to determine which coding agent (Codex vs Claude Code) was used to create these two LaTeX chess engine projects: 1. /Users/mathieuac… |
| 53 | 2026-02-19 09:37 | Claude Code (subagent) | Documentation,Scenario | Do a very thorough investigation of the chess engine at /Users/mathieuacher/SANDBOX/chess-java-cc. I need to understand what makes this eng… |
| 54 | 2026-02-19 09:37 | Claude Code (subagent) | Documentation,Scenario | Do a very thorough investigation of the chess engine at /Users/mathieuacher/SANDBOX/chess-rust-cc. I need to understand its features to com… |
| 55 | 2026-02-19 09:37 | Claude Code (subagent) | Other | Do a thorough investigation of these chess engines to understand their features. For each, look at source code and identify the key chess e… |
| 56 | 2026-02-19 10:56 | Claude Code (subagent) | Scenario | Analyze these 3 chess engines for a comparative report. For each, identify: board representation, search algorithm, search enhancements (nu… |
| 57 | 2026-02-19 10:56 | Claude Code (subagent) | Scenario | Analyze these 3 chess engines for a comparative report. For each, identify: board representation, search algorithm, search enhancements (nu… |
| 58 | 2026-02-19 10:56 | Claude Code (subagent) | Scenario | Analyze these 4 chess engines for a comparative report. For each, identify: board representation, search algorithm, search enhancements (nu… |
| 59 | 2026-02-19 10:56 | Claude Code (subagent) | Scenario | Analyze these 3 chess engines for a comparative report. For each, identify: board representation, search algorithm, search enhancements (nu… |
| 60 | 2026-02-19 12:30 | Claude Code (subagent) | FeatureRequest,TestRequest | For each of these chess engines, investigate whether they support perft testing and what correctness validation exists. For each engine: 1.… |
| … | | | | _+29 more prompts_ |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `ed779b6` | 2026-02-27T07:12:10+01:00 | Mathieu Acher | Fix AsmCodex TC configuration and rerun gauntlet (Elo 1328 → 2198) |
| `bcb0284` | 2026-02-26T12:19:24+01:00 | Mathieu Acher | Add AsmCodex engine and Swiss tournament (18 engines, 10 rounds, 900 games) |
| `c9cfd6e` | 2026-02-23T07:22:42+01:00 | Mathieu Acher | Add reproducible benchmark infrastructure and Elo assessment for 20 engines |
| `c393e8d` | 2026-02-16T22:04:06+01:00 | Mathieu Acher | Improve Elo estimation, provenance detection, and add in-depth feature analysis |
| `f6897a6` | 2026-02-16T21:47:17+01:00 | Mathieu Acher | Add chess polyglot evaluation: metrics collector and analysis report |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **64** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, Documentation, ToolingBuild, Scenario) [2026-02-16 18:11] — Explore the following chess engine projects in /Users/mathieuacher/SANDBOX. For each one, identify: - Programming language and build system - Directory structure and key files (RE… [T:Claude Code (subagent)/agent-a8]
- **BL-002** (TestRequest, Documentation, ToolingBuild, Constraint, Scenario) [2026-02-16 18:16] — Design an implementation plan for analyzing 9 chess engine projects in /Users/mathieuacher/SANDBOX/. The deliverables are: 1. **A Python script** (`analyze.py`) that auto-collects… [T:Claude Code (subagent)/agent-a9]
- **BL-003** (FeatureRequest, Documentation, ToolingBuild, Scenario) [2026-02-16 19:16] — Explore /Users/mathieuacher/SANDBOX/lean-chess thoroughly. I need to understand: 1. File structure (ls -la recursive, key directories) 2. Language used, build system 3. Any .claud… [T:Claude Code (subagent)/agent-a1]
- **BL-004** (FeatureRequest, Documentation, ToolingBuild, Scenario) [2026-02-16 19:16] — Explore /Users/mathieuacher/SANDBOX/chess-cplusplus-claude thoroughly. I need to understand: 1. File structure (ls -la recursive, key directories) 2. Language used, build system 3… [T:Claude Code (subagent)/agent-a4]
- **BL-005** (FeatureRequest, Documentation, ToolingBuild, Scenario) [2026-02-16 19:16] — Explore /Users/mathieuacher/SANDBOX/chess-py thoroughly. I need to understand: 1. File structure (ls -la recursive, key directories) 2. Language used, build system 3. Any .claude/… [T:Claude Code (subagent)/agent-ab]
- **BL-006** (FeatureRequest, Documentation, ToolingBuild, Scenario) [2026-02-16 19:16] — Explore /Users/mathieuacher/SANDBOX/COBOL-chess thoroughly. I need to understand: 1. File structure (ls -la recursive, key directories) 2. Language used, build system 3. Any .clau… [T:Claude Code (subagent)/agent-a8]
- **BL-007** (FeatureRequest, Documentation, ToolingBuild, Scenario) [2026-02-16 19:16] — Explore /Users/mathieuacher/SANDBOX/cplusplus-chess thoroughly. I need to understand: 1. File structure (ls -la recursive, key directories) 2. Language used, build system 3. Any .… [T:Claude Code (subagent)/agent-aa]
- **BL-008** (FeatureRequest, Documentation, ToolingBuild, Scenario) [2026-02-16 19:16] — Explore /Users/mathieuacher/SANDBOX/latex-chess-engine thoroughly. I need to understand: 1. File structure (ls -la recursive, key directories) 2. Language used, build system 3. An… [T:Claude Code (subagent)/agent-a9]
- **BL-009** (FeatureRequest, Documentation, ToolingBuild, Scenario) [2026-02-16 19:16] — Explore /Users/mathieuacher/SANDBOX/chess-sql thoroughly. I need to understand: 1. File structure (ls -la recursive, key directories) 2. Language used, build system 3. Any .claude… [T:Claude Code (subagent)/agent-ac]
- **BL-010** (FeatureRequest, Documentation, ToolingBuild, Scenario) [2026-02-16 19:16] — Explore /Users/mathieuacher/SANDBOX/chess-purec thoroughly. I need to understand: 1. File structure (ls -la recursive, key directories) 2. Language used, build system 3. Any .clau… [T:Claude Code (subagent)/agent-a5]
- **BL-011** (FeatureRequest, Documentation, ToolingBuild, Scenario) [2026-02-16 19:16] — Explore /Users/mathieuacher/SANDBOX/chess-Rocq thoroughly. I need to understand: 1. File structure (ls -la recursive, key directories) 2. Language used, build system 3. Any .claud… [T:Claude Code (subagent)/agent-ae]
- **BL-012** (Documentation, Scenario) [2026-02-16 20:55] — Thoroughly investigate /Users/mathieuacher/SANDBOX/chess-py for agent provenance clues. Check: 1. Is there a .git directory? If so, check ALL git log entries for Co-Authored-By ma… [T:Claude Code (subagent)/agent-ad]
- **BL-013** (Documentation) [2026-02-16 20:55] — Thoroughly investigate /Users/mathieuacher/SANDBOX/chess-cplusplus-claude for better Elo estimation and provenance. Check: 1. Read ALL PGN files in results/ directory — parse the … [T:Claude Code (subagent)/agent-a3]
- **BL-014** (Documentation) [2026-02-16 20:55] — Investigate /Users/mathieuacher/SANDBOX/lean-chess for agent provenance. Check: 1. Is there a .git directory? If so, check ALL git log entries for Co-Authored-By markers 2. Any CL… [T:Claude Code (subagent)/agent-a3]
- **BL-015** (Documentation, ToolingBuild) [2026-02-16 20:55] — Investigate /Users/mathieuacher/SANDBOX/COBOL-chess for agent provenance. Check: 1. Is there a .git directory? If so, check ALL git log entries for Co-Authored-By markers 2. Any C… [T:Claude Code (subagent)/agent-af]
- **BL-016** (Constraint, Scenario) [2026-02-16 20:56] — I need an in-depth analysis of chess-related features across 9 chess engine projects. For each project below, I need you to READ the actual source files (not just grep keywords) a… [T:Claude Code (subagent)/agent-ad]
- **BL-017** (FeatureRequest, ToolingBuild, Scenario) [2026-02-16 21:09] — I need to understand how each of the 9 chess engines can be invoked as UCI engines for tournament play. For each project below, find: 1. **How to run the UCI engine** — what comma… [T:Claude Code (subagent)/agent-ab]
- **BL-018** (TestRequest, Scenario) [2026-02-16 21:09] — Look at the existing tournament/match scripts across the chess projects to understand the patterns used. I need to design a unified tournament runner. Read these files: 1. /Users/… [T:Claude Code (subagent)/agent-a5]
- **BL-019** (FeatureRequest, BugFixRequest, TestRequest, Documentation, Constraint) [2026-02-16 21:13] — Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previous actions. This summary should be thor… [T:Claude Code (subagent)/agent-ac]
- **BL-020** (FeatureRequest, ToolingBuild, Scenario) [2026-02-16 21:15] — Check which chess engine binaries/executables exist and are ready to run. For each of these 9 projects, verify if the engine binary/script exists and report the exact path: 1. lea… [T:Claude Code (subagent)/agent-ab]
- **BL-021** (FeatureRequest, ToolingBuild, Constraint, Scenario) [2026-02-16 21:17] — Design a unified tournament system for evaluating 9 chess engines. This will be a Python script called `run_tournament.py` in `/Users/mathieuacher/SANDBOX/chess-polyglot-eval/`. #… [T:Claude Code (subagent)/agent-a1]
- **BL-022** (FeatureRequest, TestRequest, ToolingBuild) [2026-02-16 21:26] — Verify the following engine binaries and working directories exist. For each, just print whether it exists or not: 1. /Users/mathieuacher/SANDBOX/chess-purec/purec 2. /Users/mathi… [T:Claude Code (subagent)/agent-a4]
- **BL-023** (BugFixRequest, TestRequest, Documentation, Scenario) [2026-02-17 08:20] — Very thorough analysis of the AI coding sessions that built the chess-purec engine at /Users/mathieuacher/SANDBOX/chess-purec. I need to understand the FULL development story. Exa… [T:Claude Code (subagent)/agent-a1]
- **BL-024** (BugFixRequest, TestRequest, Documentation) [2026-02-17 08:20] — Very thorough analysis of the AI coding sessions that built the cplusplus-chess engine (Codex-built) at /Users/mathieuacher/SANDBOX/cplusplus-chess. I need to understand the FULL … [T:Claude Code (subagent)/agent-af]
- **BL-025** (BugFixRequest, TestRequest, Documentation, Scenario) [2026-02-17 08:20] — Very thorough analysis of the AI coding sessions that built chess-cplusplus-claude (Claudius) at /Users/mathieuacher/SANDBOX/chess-cplusplus-claude. I need to understand the FULL … [T:Claude Code (subagent)/agent-af]
- **BL-026** (BugFixRequest, TestRequest, Documentation, Scenario) [2026-02-17 08:20] — Very thorough analysis of the AI coding sessions that built lean-chess (LeanChess) at /Users/mathieuacher/SANDBOX/lean-chess. I need to understand the FULL development story. Exam… [T:Claude Code (subagent)/agent-a5]
- **BL-027** (FeatureRequest, BugFixRequest, TestRequest, Documentation, ToolingBuild, Scenario) [2026-02-17 08:20] — Very thorough analysis of the AI coding sessions that built COBOL-chess (CoboChess) at /Users/mathieuacher/SANDBOX/COBOL-chess. I need to understand the FULL development story. Ex… [T:Claude Code (subagent)/agent-ae]
- **BL-028** (FeatureRequest, BugFixRequest, TestRequest, Documentation, ToolingBuild) [2026-02-17 08:20] — Very thorough analysis of the AI coding sessions that built chess-Rocq (ChessRocq) at /Users/mathieuacher/SANDBOX/chess-Rocq. I need to understand the FULL development story. Exam… [T:Claude Code (subagent)/agent-aa]
- **BL-029** (BugFixRequest, TestRequest, Documentation, Scenario) [2026-02-17 08:21] — Very thorough analysis of the AI coding sessions that built chess-py (ChessPy) at /Users/mathieuacher/SANDBOX/chess-py. I need to understand the FULL development story. Examine: 1… [T:Claude Code (subagent)/agent-a8]
- **BL-030** (FeatureRequest, BugFixRequest, TestRequest, Documentation, ToolingBuild) [2026-02-17 08:21] — Very thorough analysis of the AI coding sessions that built latex-chess-engine (TeXChess) at /Users/mathieuacher/SANDBOX/latex-chess-engine. I need to understand the FULL developm… [T:Claude Code (subagent)/agent-a6]
- **BL-031** (FeatureRequest, BugFixRequest, TestRequest, Documentation, ToolingBuild) [2026-02-17 08:21] — Very thorough analysis of the AI coding sessions that built chess-sql (SQLChess) at /Users/mathieuacher/SANDBOX/chess-sql. I need to understand the FULL development story. Examine… [T:Claude Code (subagent)/agent-a7]
- **BL-032** (TestRequest, Scenario) [2026-02-17 08:30] — I need to understand what speed/performance metrics each of these 9 chess engines reports during UCI search. For each engine, search the source code for: 1. Does it support a `per… [T:Claude Code (subagent)/agent-af]
- **BL-033** (TestRequest, Scenario) [2026-02-17 08:31] — For each of these chess engine projects, find the EXACT format of the perft command they accept via UCI/stdin. Search for how they parse the "perft" command in their UCI loop. Pro… [T:Claude Code (subagent)/agent-a1]
- **BL-034** (FeatureRequest, Documentation, ToolingBuild) [2026-02-17 09:51] — Explore /Users/mathieuacher/SANDBOX/chess-mojo thoroughly: 1. Read the README if it exists 2. Check if there's a working UCI engine binary or script 3. List main source files and … [T:Claude Code (subagent)/agent-ab]
- **BL-035** (Documentation) [2026-02-17 09:51] — Explore /Users/mathieuacher/SANDBOX/chess-rust-cc thoroughly: 1. Read the README if it exists 2. Check if there's a working UCI engine binary 3. List main source files and identif… [T:Claude Code (subagent)/agent-a1]
- **BL-036** (Documentation) [2026-02-17 09:51] — Explore /Users/mathieuacher/SANDBOX/chess-rust-codex thoroughly: 1. Read the README if it exists 2. Check if there's a working UCI engine binary 3. List main source files and iden… [T:Claude Code (subagent)/agent-a0]
- **BL-037** (Documentation) [2026-02-17 09:52] — Explore /Users/mathieuacher/SANDBOX/chess-latex-codex-replication thoroughly: 1. Read the README if it exists 2. Check if there's a working UCI engine (binary or script) 3. List m… [T:Claude Code (subagent)/agent-a1]
- **BL-038** (FeatureRequest, TestRequest, ToolingBuild, Scenario) [2026-02-17 09:54] — Verify the following 4 new chess engine projects exist and check their binary/command details: 1. chess-mojo: Check if `build/mojo_engine` exists in `/Users/mathieuacher/SANDBOX/c… [T:Claude Code (subagent)/agent-ab]
- **BL-039** (Documentation, Scenario) [2026-02-17 15:51] — Search across all chess engine project directories in /Users/mathieuacher/SANDBOX/ for internal Elo assessments. Look for: 1. In chess-latex-codex-replication: any Elo reports, ga… [T:Claude Code (subagent)/agent-af]
- **BL-040** (Documentation) [2026-02-17 15:54] — Read the following files and report their full contents: 1. /Users/mathieuacher/SANDBOX/latex-chess-engine/elo-games.pgn - just the first 20 lines and count total games with `grep… [T:Claude Code (subagent)/agent-a5]
- _+24 more items truncated in this view — see appendix._

## Evidence pointers

- [R:chess-polyglot-eval] — repo at `/Users/mathieuacher/SANDBOX/chess-polyglot-eval`
- [T:chess-polyglot-eval/claude] — Claude sessions at `~/.claude/projects/chess-polyglot-eval...`
- [T:chess-polyglot-eval/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-polyglot-eval

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.