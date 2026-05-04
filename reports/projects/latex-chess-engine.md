# latex-chess-engine

_Evidence-based dossier. Generated 2026-04-22 14:55 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/latex-chess-engine` [R:latex-chess-engine]
- **Primary language:** LaTeX
- **Coding agent(s):** Claude Code subagents, Codex
- **Period:** 2026-02-19 14:01 → 2026-02-19 15:19
- **LOC by language:** LaTeX (39838 LOC, 17 files), Python (920 LOC, 2 files), Shell (301 LOC, 2 files), Markdown (125 LOC, 1 files), Text (1 LOC, 1 files)
- **Totals:** 23 files, 41185 LOC [S:scan]
- **Git:** 15 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 23 subagent transcripts [T:latex-chess-engine/claude]
- Claude models seen: —
- Codex sessions: 1 [T:latex-chess-engine/codex]
- Codex models seen: gpt-5.3-codex

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 1 | 14 | 3946313 | 33397 | 3546368 | — | $5.71 |
| **Total** |  |  |  |  |  |  | **$5.71** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| Promotion | 26 | `test-greedy.log` |
| Castling | 24 | `chess-game.tex` |
| Time management | 9 | `chess-uci.py` |
| FEN parsing | 7 | `test-debug.log` |
| UCI protocol | 6 | `chess-uci.py` |
| Check/Checkmate | 6 | `chess-interactive.sh` |
| En passant | 5 | `chess-test.log` |
| Quiescence | 4 | `chess-uci.py` |
| PGN | 3 | `run-elo-test.sh` |
| Minimax/Negamax | 3 | `chess-engine.tex` |
| Alpha-beta | 2 | `chess-engine.tex` |
| Material counting | 2 | `chess-engine.tex` |
| Board: mailbox 8x8 | 1 | `chess-engine.tex` |
| Iterative deepening | 1 | `chess-uci.py` |
| Move ordering (MVV-LVA) | 1 | `README.md` |
| Evaluation/PST | 1 | `chess-engine.tex` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | exec_command | 56 |

## Interaction profile

- Total user prompts (both agents): **37**
- Avg prompt length: 1182.2 chars
- Intent distribution:
  - FeatureRequest: 13
  - TestRequest: 11
  - Documentation: 10
  - Scenario: 10
  - Other: 9
  - Constraint: 9
  - BugFixRequest: 6
  - Question: 5

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Claude Code (subagent) — 2026-02-13 20:29 — session `agent-ab`_

```
Explore the codebase at /Users/mathieuacher/SANDBOX/latex-chess-engine/ thoroughly. Look for any existing files - .tex, .sty, .cls, .lua, .py, or any other files. Also search for any LaTeX chess-related packages that might be installed on the system (like skak, chessboard, xskak, etc.). Check:
1. All files in the project directory (recursively)
2. Whether texlive or mactex is installed and what chess-related packages are available
3. Any README or documentation files
Report everything you find.
```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-13 20:29 | Claude Code (subagent) | Other | Research what's known about implementing chess engines in LaTeX/TeX. Search the web for: 1. Any existing chess engines written in LaTeX or … |
| 3 | 2026-02-13 20:37 | Claude Code (subagent) | FeatureRequest,TestRequest | I need to design a detailed implementation plan for a chess engine written entirely in pure LaTeX/pdfLaTeX (no Lua, no external programs fo… |
| 4 | 2026-02-14 18:28 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 5 | 2026-02-14 18:40 | Claude Code (subagent) | FeatureRequest | Explore the chess engine in /Users/mathieuacher/SANDBOX/latex-chess-engine/. I need to understand: 1. In `chess-engine.tex`: How does the e… |
| 6 | 2026-02-14 18:40 | Claude Code (subagent) | Constraint,Scenario | Search the web and explore what's needed to integrate with cutechess-cli: 1. What is the UCI protocol? What commands must an engine respond… |
| 7 | 2026-02-14 21:00 | Claude Code (subagent) | FeatureRequest,Scenario | Thoroughly explore the chess engine codebase at /Users/mathieuacher/SANDBOX/latex-chess-engine/. I need to understand: 1. **Move generation… |
| 8 | 2026-02-14 21:08 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Design a minimax chess engine implementation for a pure pdfLaTeX chess engine. Here's the context: ## Current Architecture (chess-engine.te… |
| 9 | 2026-02-14 21:12 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 10 | 2026-02-15 06:20 | Claude Code (subagent) | TestRequest | Read the file /Users/mathieuacher/SANDBOX/latex-chess-engine/chess-test.tex and give me a summary of how the tests work - what macros they … |
| 11 | 2026-02-15 07:07 | Claude Code (subagent) | TestRequest,Scenario | I need to understand the performance characteristics of the TeX chess engine for planning improvements. Please investigate: 1. Read /Users/… |
| 12 | 2026-02-15 07:08 | Claude Code (subagent) | FeatureRequest,Constraint | I'm improving a chess engine written in pure pdfLaTeX. It currently has: - Depth-2 minimax (no alpha-beta pruning yet, though the code has … |
| 13 | 2026-02-19 14:01 | Codex | Other | I'd like to understand this code base... perform an in-depth analysis of implementation details, features of the chess engine, of the gener… |
| 14 | 2026-02-19 14:18 | Codex | FeatureRequest | I would like to understand how it is possible to implement negamax alpha-beta + quiescence and evaluation function based on material... whe… |
| 15 | 2026-02-19 14:22 | Codex | Documentation | " like a tiny VM: integer registers (\count), token-list “arrays”, and recursive macro calls." explain this story of registers... and why a… |
| 16 | 2026-02-19 14:46 | Codex | Question | how is Quiescence search implemented? detail the pseudo algorithm |
| 17 | 2026-02-19 14:48 | Codex | Question | when is Quiescence search performed? |
| 18 | 2026-02-19 14:54 | Codex | FeatureRequest,Question | can you create a kind of call-graph style map (macro-to-macro flow) from \playmove down to leaf functions for easier onboarding? also, make… |
| 19 | 2026-02-19 15:03 | Codex | Other | for each "box", can you associate a description, and where it is in the code? for instance, how the search stack trace works? is 10000 a st… |
| 20 | 2026-02-19 15:03 | Codex | Other | search stack sorry (no search stack trace) |
| 21 | 2026-02-19 15:11 | Codex | Constraint | sounds good... I still don't get how the tiny VM abstractions are leveraged... like registers |
| 22 | 2026-02-19 15:17 | Codex | Question | how is the generation of legal moves made? |
| 23 | 2026-02-19 15:18 | Codex | Documentation | let's dig into \def\tryknightjump#1#2{% \mg@tf=\numexpr\mg@fromfile+(#1)\relax \mg@tr=\numexpr\mg@fromrank+(#2)\relax \ifnum\mg@tf>0 \ifnum… |
| 24 | 2026-02-19 15:18 | Codex | Other | in pseudo code terms? |
| 25 | 2026-02-19 15:19 | Codex | Question | what -2, -1 means? |
| 26 | 2026-02-19 15:19 | Codex | Other | addMove has a kind of side-effect no? on which variables? |
| 27 | 2026-02-23 10:54 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 28 | 2026-02-23 14:51 | Claude Code (subagent) | FeatureRequest,TestRequest | Thoroughly explore the chess engine codebase at /Users/mathieuacher/SANDBOX/latex-chess-engine. I need to understand: 1. The main TeX file(… |
| 29 | 2026-02-23 14:51 | Claude Code (subagent) | FeatureRequest,TestRequest | Very thoroughly explore the chess engine codebase at /Users/mathieuacher/SANDBOX/latex-chess-engine. I need to understand: 1. The main TeX … |
| 30 | 2026-02-23 14:52 | Claude Code (subagent) | Other | Read the file /Users/mathieuacher/.codex/sessions/2026/02/19/rollout-2026-02-19T13-01-27-019c75c6-c737-7522-b22d-99cdb231bd10.jsonl in chun… |
| 31 | 2026-02-23 16:18 | Claude Code (subagent) | Constraint | Search through the file /Users/mathieuacher/.codex/sessions/2026/02/19/rollout-2026-02-19T13-01-27-019c75c6-c737-7522-b22d-99cdb231bd10.jso… |
| 32 | 2026-02-23 16:24 | Claude Code (subagent) | Other | Search for Codex session files that might contain Mermaid diagrams related to the LaTeX/TeX chess engine. Look in: 1. /Users/mathieuacher/.… |
| 33 | 2026-02-23 16:31 | Claude Code (subagent) | Documentation,Scenario | Explore this repository at /Users/mathieuacher/SANDBOX/latex-chess-engine to gather information for writing a README. I need: 1. Read the f… |
| 34 | 2026-02-23 16:49 | Claude Code (subagent) | Other | Search thoroughly for Claude Code session data, logs, or conversation history related to the LaTeX chess engine project. Look in: 1. /Users… |
| 35 | 2026-02-23 16:51 | Claude Code (subagent) | BugFixRequest,TestRequest | I need to extract interesting insights from Claude Code session files for the LaTeX chess engine project. The sessions are at: /Users/mathi… |
| 36 | 2026-02-23 19:50 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 37 | 2026-02-24 06:55 | Claude Code (subagent) | Scenario | I need to verify that the TeX chess engine is configured to use depth-3 search (the strongest setting) when invoked via the UCI wrapper. Ch… |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `697931b` | 2026-02-26T07:26:08+01:00 | Mathieu Acher | overleaf link |
| `26a07ee` | 2026-02-26T07:00:47+01:00 | Mathieu Acher | edits before release |
| `778b75f` | 2026-02-26T06:49:15+01:00 | Mathieu Acher | Remove LaTeX build artifacts from tracking |
| `1aa4d17` | 2026-02-26T06:00:56+01:00 | Mathieu Acher | for elo in 1320 1400 1500; do GAMES=50 STOCKFISH_ELO=1500 bash run-elo-test.sh; done ~[1200, 1322] Elo |
| `fa66457` | 2026-02-25T07:58:39+01:00 | Mathieu Acher | for elo in 1320 1400 1500 1600 1700; do GAMES=10 STOCKFISH_ELO= bash run-elo-test.sh; done |
| `b034419` | 2026-02-24T18:51:02+01:00 | Mathieu Acher | fixing some timeouts UCI + results with latex-chess-engine % GAMES=100 STOCKFISH_ELO=1320 bash run-elo-test.sh Score of… |
| `2e8331e` | 2026-02-24T07:28:22+01:00 | Mathieu Acher | results with GAMES=100 STOCKFISH_ELO=1320 TIME_CONTROL="40/60+1" bash run-elo-test.sh |
| `3c51f09` | 2026-02-23T18:10:21+01:00 | Mathieu Acher | Add first-ever claim and video demos to README |
| `9476f9a` | 2026-02-23T17:38:20+01:00 | Mathieu Acher | Add README documenting the TeX chess engine |
| `d16b663` | 2026-02-23T13:51:09+01:00 | Mathieu Acher | Add engine strength configuration to chess-game.tex |
| `04c51d5` | 2026-02-16T08:54:28+01:00 | Mathieu Acher | Add PSTs, depth-3 alpha-beta search, and quiescence |
| `926869f` | 2026-02-14T21:59:23+01:00 | Mathieu Acher | Add native TeX board rendering mode to pgn2latex.py |
| `081f9de` | 2026-02-14T21:52:14+01:00 | Mathieu Acher | Fix pgn2latex.py to parse SAN notation from cutechess-cli |
| `2571f5b` | 2026-02-14T21:48:18+01:00 | Mathieu Acher | Add UCI protocol wrapper and Elo assessment infrastructure |
| `9e4b41a` | 2026-02-14T19:28:05+01:00 | Mathieu Acher | Add chess engine in pure pdfLaTeX |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **21** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (Documentation) [2026-02-13 20:29] — Explore the codebase at /Users/mathieuacher/SANDBOX/latex-chess-engine/ thoroughly. Look for any existing files - .tex, .sty, .cls, .lua, .py, or any other files. Also search for … [T:Claude Code (subagent)/agent-ab]
- **BL-002** (FeatureRequest, TestRequest, Scenario) [2026-02-13 20:37] — I need to design a detailed implementation plan for a chess engine written entirely in pure LaTeX/pdfLaTeX (no Lua, no external programs for the engine logic). The requirements ar… [T:Claude Code (subagent)/agent-a3]
- **BL-003** (FeatureRequest, BugFixRequest, TestRequest, Documentation, Constraint) [2026-02-14 18:28] — Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previous actions. This summary should be thor… [T:Claude Code (subagent)/agent-ac]
- **BL-004** (FeatureRequest) [2026-02-14 18:40] — Explore the chess engine in /Users/mathieuacher/SANDBOX/latex-chess-engine/. I need to understand: 1. In `chess-engine.tex`: How does the engine output data for interactive mode? … [T:Claude Code (subagent)/agent-a9]
- **BL-005** (Constraint, Scenario) [2026-02-14 18:40] — Search the web and explore what's needed to integrate with cutechess-cli: 1. What is the UCI protocol? What commands must an engine respond to? (uci, isready, position, go, quit) … [T:Claude Code (subagent)/agent-af]
- **BL-006** (FeatureRequest, Scenario) [2026-02-14 21:00] — Thoroughly explore the chess engine codebase at /Users/mathieuacher/SANDBOX/latex-chess-engine/. I need to understand: 1. **Move generation**: How does `\generateallmoves`, `\filt… [T:Claude Code (subagent)/agent-aa]
- **BL-007** (FeatureRequest, BugFixRequest, TestRequest, Constraint, Scenario) [2026-02-14 21:08] — Design a minimax chess engine implementation for a pure pdfLaTeX chess engine. Here's the context: ## Current Architecture (chess-engine.tex) **Board**: `\count200`-`\count263` fo… [T:Claude Code (subagent)/agent-a5]
- **BL-008** (TestRequest) [2026-02-15 06:20] — Read the file /Users/mathieuacher/SANDBOX/latex-chess-engine/chess-test.tex and give me a summary of how the tests work - what macros they use, how assertions are done, and the ge… [T:Claude Code (subagent)/agent-ab]
- **BL-009** (TestRequest, Scenario) [2026-02-15 07:07] — I need to understand the performance characteristics of the TeX chess engine for planning improvements. Please investigate: 1. Read /Users/mathieuacher/SANDBOX/latex-chess-engine/… [T:Claude Code (subagent)/agent-a6]
- **BL-010** (FeatureRequest, Constraint) [2026-02-15 07:08] — I'm improving a chess engine written in pure pdfLaTeX. It currently has: - Depth-2 minimax (no alpha-beta pruning yet, though the code has \mm@alpha that's not used for cutoffs) -… [T:Claude Code (subagent)/agent-ac]
- **BL-011** (FeatureRequest) [2026-02-19 14:18] — I would like to understand how it is possible to implement negamax alpha-beta + quiescence and evaluation function based on material... where it is in the code, and what implement… [T:Codex/rollout-]
- **BL-012** (Documentation) [2026-02-19 14:22] — " like a tiny VM: integer registers (\count), token-list “arrays”, and recursive macro calls." explain this story of registers... and why a "VM" is needed [T:Codex/rollout-]
- **BL-013** (FeatureRequest, Question) [2026-02-19 14:54] — can you create a kind of call-graph style map (macro-to-macro flow) from \playmove down to leaf functions for easier onboarding? also, make a figure about the "tiny VM" [T:Codex/rollout-]
- **BL-014** (Constraint) [2026-02-19 15:11] — sounds good... I still don't get how the tiny VM abstractions are leveraged... like registers [T:Codex/rollout-]
- **BL-015** (Documentation) [2026-02-19 15:18] — let's dig into \def\tryknightjump#1#2{% \mg@tf=\numexpr\mg@fromfile+(#1)\relax \mg@tr=\numexpr\mg@fromrank+(#2)\relax \ifnum\mg@tf>0 \ifnum\mg@tf<9 \ifnum\mg@tr>0 \ifnum\mg@tr<9 \… [T:Codex/rollout-]
- **BL-016** (FeatureRequest, TestRequest, Documentation, Scenario) [2026-02-23 14:51] — Thoroughly explore the chess engine codebase at /Users/mathieuacher/SANDBOX/latex-chess-engine. I need to understand: 1. The main TeX file(s) that implement the chess engine 2. Th… [T:Claude Code (subagent)/agent-ab]
- **BL-017** (FeatureRequest, TestRequest, Documentation, Scenario) [2026-02-23 14:51] — Very thoroughly explore the chess engine codebase at /Users/mathieuacher/SANDBOX/latex-chess-engine. I need to understand: 1. The main TeX file(s) that implement the chess engine … [T:Claude Code (subagent)/agent-a7]
- **BL-018** (Constraint) [2026-02-23 16:18] — Search through the file /Users/mathieuacher/.codex/sessions/2026/02/19/rollout-2026-02-19T13-01-27-019c75c6-c737-7522-b22d-99cdb231bd10.jsonl to find all Mermaid diagrams. The fil… [T:Claude Code (subagent)/agent-af]
- **BL-019** (Documentation, Scenario) [2026-02-23 16:31] — Explore this repository at /Users/mathieuacher/SANDBOX/latex-chess-engine to gather information for writing a README. I need: 1. Read the first ~100 lines of chess-engine.tex to u… [T:Claude Code (subagent)/agent-a1]
- **BL-020** (BugFixRequest, TestRequest, Scenario) [2026-02-23 16:51] — I need to extract interesting insights from Claude Code session files for the LaTeX chess engine project. The sessions are at: /Users/mathieuacher/.claude/projects/-Users-mathieua… [T:Claude Code (subagent)/agent-ae]
- **BL-021** (Scenario) [2026-02-24 06:55] — I need to verify that the TeX chess engine is configured to use depth-3 search (the strongest setting) when invoked via the UCI wrapper. Check these files: 1. chess-uci.tex - the … [T:Claude Code (subagent)/agent-a8]

## Evidence pointers

- [R:latex-chess-engine] — repo at `/Users/mathieuacher/SANDBOX/latex-chess-engine`
- [T:latex-chess-engine/claude] — Claude sessions at `~/.claude/projects/latex-chess-engine...`
- [T:latex-chess-engine/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/latex-chess-engine

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.