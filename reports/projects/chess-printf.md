# chess-printf

_Evidence-based dossier. Generated 2026-04-22 14:53 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-printf` [R:chess-printf]
- **Primary language:** C
- **Coding agent(s):** Claude Code subagents
- **Period:** —
- **LOC by language:** C (792 LOC, 2 files), Markdown (228 LOC, 1 files)
- **Totals:** 3 files, 1020 LOC [S:scan]
- **Git:** 6 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 12 subagent transcripts [T:chess-printf/claude]
- Claude models seen: —
- Codex sessions: 0 [T:chess-printf/codex]
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
| Check/Checkmate | 3 | `README.md` |
| Promotion | 2 | `README.md` |
| Material counting | 2 | `README.md` |
| En passant | 1 | `README.md` |

## Interaction profile

- Total user prompts (both agents): **14**
- Avg prompt length: 2221.5 chars
- Intent distribution:
  - Constraint: 7
  - FeatureRequest: 6
  - TestRequest: 5
  - Scenario: 5
  - Other: 4
  - Documentation: 3
  - BugFixRequest: 2
  - ToolingBuild: 2

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Claude Code (subagent) — 2026-03-03 07:48 — session `agent-a5`_

```
Research how Nicholas Carlini's printf-tac-toe works. I need to understand the specific printf tricks used to make printf Turing-complete, especially:

1. How %hhn writes the character count (mod 256) to a byte in memory
2. How %*d / %*N$d sets the character count to a dynamic value 
3. How the ZERO macro resets char count to 0 mod 256
4. How %s conditional gates work (strlen 0 vs 1)
5. How equality testing works (comparing a byte against an expected value)

Search the web for Nicholas Carlini printf-tac-toe explanation, source code, and any writeups about the technique. Also look for the actual GitHub repo.

Return a detailed summary of the techniques with concrete printf format string examples.
```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-03-03 08:26 | Claude Code (subagent) | Constraint,Scenario | I need to design an implementation for computing and displaying ALL legal chess moves using ONLY printf format string logic (the %hhn, %*d,… |
| 3 | 2026-03-03 16:16 | Claude Code (subagent) | Constraint | don't ask me for python3 executions |
| 4 | 2026-03-04 13:09 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 5 | 2026-03-04 14:20 | Claude Code (subagent) | FeatureRequest,Scenario | I need to understand how printf-tac-toe by Nicholas Carlini encodes game logic in the format string using %n. Fetch and analyze the source … |
| 6 | 2026-03-04 14:20 | Claude Code (subagent) | Other | Analyze /Users/mathieuacher/SANDBOX/chess-printf/printf_chess.c to understand: 1. The exact structure of the d[] array and how state is enc… |
| 7 | 2026-03-04 14:37 | Claude Code (subagent) | Other | I accept use of python3 all time in this project |
| 8 | 2026-03-04 14:44 | Claude Code (subagent) | FeatureRequest,TestRequest | Design a POP-pure (Printf-Oriented Programming) minimal chess engine that follows the exact techniques of printf-tac-toe by Nicholas Carlin… |
| 9 | 2026-03-04 16:21 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 10 | 2026-03-04 16:53 | Claude Code (subagent) | FeatureRequest,TestRequest | Explore the /Users/mathieuacher/SANDBOX/chess-printf directory. I need to understand: 1. What files exist (glob all .c, .h files) 2. Read a… |
| 11 | 2026-03-04 21:38 | Claude Code (subagent) | Other | Search for printf-tac-toe or Carlini's printf tic-tac-toe source code anywhere on this system. Look in: 1. /Users/mathieuacher/SANDBOX/ and… |
| 12 | 2026-03-04 22:06 | Claude Code (subagent) | Constraint,Scenario | Design a POP-pure (Printf-Oriented Programming) implementation of Breakthrough chess. ## Context I'm redesigning pop_breakthrough.c to matc… |
| 13 | 2026-03-05 09:44 | Claude Code (subagent) | Other | Read the file /Users/mathieuacher/.claude/projects/-Users-mathieuacher-SANDBOX-chess-printf/ba32eba5-cec0-4a1a-820d-414721f0802a.jsonl and … |
| 14 | 2026-03-05 09:44 | Claude Code (subagent) | Documentation,Constraint | Search the codebase at /Users/mathieuacher/SANDBOX/chess-printf/ for any existing Carlini-style printf implementations. Look for: 1. printf… |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `c61feaf` | 2026-03-04T15:14:46+01:00 | Mathieu Acher | Rewrite README to tell the full story of human-directed POP improvements |
| `3736145` | 2026-03-04T14:35:30+01:00 | Mathieu Acher | Improve POP purity: %hhn loop control, %.*s conditionals, remove atexit |
| `296871a` | 2026-03-03T22:12:15+01:00 | Mathieu Acher | Update README with tldr, expanded commentary, and supervision notes |
| `c038063` | 2026-03-03T22:00:11+01:00 | Mathieu Acher | Add README documenting the printf-chess approach and features |
| `34d234a` | 2026-03-03T21:56:29+01:00 | Mathieu Acher | Add eval display, legal move gen, random AI, checkmate detection, and simplify main |
| `ce7f416` | 2026-03-03T01:29:31+01:00 | Mathieu Acher | Initial printf chess: board display + move logic via while(*d) printf(fmt, arg) |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **9** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest) [2026-03-03 07:48] — Research how Nicholas Carlini's printf-tac-toe works. I need to understand the specific printf tricks used to make printf Turing-complete, especially: 1. How %hhn writes the chara… [T:Claude Code (subagent)/agent-a5]
- **BL-002** (Constraint, Scenario) [2026-03-03 08:26] — I need to design an implementation for computing and displaying ALL legal chess moves using ONLY printf format string logic (the %hhn, %*d, %s gate techniques from printf-tac-toe … [T:Claude Code (subagent)/agent-a0]
- **BL-003** (Constraint) [2026-03-03 16:16] — don't ask me for python3 executions [T:Claude Code (subagent)/agent-a0]
- **BL-004** (FeatureRequest, BugFixRequest, TestRequest, Documentation, Constraint) [2026-03-04 13:09] — Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previous actions. This summary should be thor… [T:Claude Code (subagent)/agent-ac]
- **BL-005** (FeatureRequest, Scenario) [2026-03-04 14:20] — I need to understand how printf-tac-toe by Nicholas Carlini encodes game logic in the format string using %n. Fetch and analyze the source code from https://github.com/carlini/pri… [T:Claude Code (subagent)/agent-a2]
- **BL-006** (FeatureRequest, TestRequest, ToolingBuild, Constraint, Scenario) [2026-03-04 14:44] — Design a POP-pure (Printf-Oriented Programming) minimal chess engine that follows the exact techniques of printf-tac-toe by Nicholas Carlini. ## Context We have two programs: 1. *… [T:Claude Code (subagent)/agent-a2]
- **BL-007** (FeatureRequest, TestRequest, ToolingBuild) [2026-03-04 16:53] — Explore the /Users/mathieuacher/SANDBOX/chess-printf directory. I need to understand: 1. What files exist (glob all .c, .h files) 2. Read any existing printf-tac-toe or POP-relate… [T:Claude Code (subagent)/agent-a3]
- **BL-008** (Constraint, Scenario) [2026-03-04 22:06] — Design a POP-pure (Printf-Oriented Programming) implementation of Breakthrough chess. ## Context I'm redesigning pop_breakthrough.c to match Carlini's printf-tac-toe purity level.… [T:Claude Code (subagent)/agent-a8]
- **BL-009** (Documentation, Constraint, Scenario) [2026-03-05 09:44] — Search the codebase at /Users/mathieuacher/SANDBOX/chess-printf/ for any existing Carlini-style printf implementations. Look for: 1. printf_tac_toe.c or any printf-only tic-tac-to… [T:Claude Code (subagent)/agent-a4]

## Evidence pointers

- [R:chess-printf] — repo at `/Users/mathieuacher/SANDBOX/chess-printf`
- [T:chess-printf/claude] — Claude sessions at `~/.claude/projects/chess-printf...`
- [T:chess-printf/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-printf

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.