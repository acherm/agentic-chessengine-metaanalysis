# chess-icon-codex

_Evidence-based dossier. Generated 2026-04-22 14:52 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-icon-codex` [R:chess-icon-codex]
- **Primary language:** Icon
- **Coding agent(s):** Codex
- **Period:** 2026-02-23 20:12 → 2026-02-24 16:51
- **LOC by language:** Icon (1660 LOC, 1 files), Python (1082 LOC, 5 files), JSON (272 LOC, 6 files), Markdown (131 LOC, 1 files), Shell (53 LOC, 3 files), Text (19 LOC, 6 files)
- **Totals:** 22 files, 3217 LOC [S:scan]
- **Git:** not a git repo

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:chess-icon-codex/claude]
- Claude models seen: —
- Codex sessions: 1 [T:chess-icon-codex/codex]
- Codex models seen: gpt-5.3-codex

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 1 | 6 | 13603046 | 88489 | 12961664 | — | $19.51 |
| **Total** |  |  |  |  |  |  | **$19.51** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| Time management | 15 | `README.md` |
| Castling | 10 | `README.md` |
| UCI protocol | 6 | `README.md` |
| Material counting | 4 | `README.md` |
| Perft | 3 | `README.md` |
| PGN | 3 | `README.md` |
| FEN parsing | 2 | `scripts/perft_check.py` |
| Promotion | 2 | `README.md` |
| Quiescence | 2 | `README.md` |
| En passant | 1 | `README.md` |
| Check/Checkmate | 1 | `src/icon_chess.icn` |
| Board: 0x88 | 1 | `README.md` |
| Alpha-beta | 1 | `README.md` |
| Iterative deepening | 1 | `README.md` |
| Transposition table | 1 | `README.md` |
| Move ordering (MVV-LVA) | 1 | `README.md` |
| Killer moves | 1 | `README.md` |
| Null-move pruning | 1 | `README.md` |
| Late-move reduction (LMR) | 1 | `README.md` |
| Aspiration windows | 1 | `README.md` |
| Pawn structure | 1 | `src/icon_chess.icn` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | exec_command | 129 |
| Codex | write_stdin | 7 |

## Interaction profile

- Total user prompts (both agents): **6**
- Avg prompt length: 83.5 chars
- Intent distribution:
  - Other: 3
  - FeatureRequest: 2
  - TestRequest: 2
  - ToolingBuild: 1
  - Scenario: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-02-23 20:12 — session `rollout-`_

```
I want to build a chess engine in Icon programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-23 21:13 | Codex | Other | continue |
| 3 | 2026-02-23 21:21 | Codex | TestRequest,Scenario | please go ahead with perft checker |
| 4 | 2026-02-23 21:31 | Codex | Other | icon is installed (icon -P 'procedure main(); writes("Hello, World!"); end') |
| 5 | 2026-02-23 21:42 | Codex | FeatureRequest | ok, it's time to quickly assess the Elo (n=20 games) against different Stockfish skills... please write a script |
| 6 | 2026-02-24 16:43 | Codex | Other | please improve significantly the strenght of the chess engine |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **3** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, ToolingBuild) [2026-02-23 20:12] — I want to build a chess engine in Icon programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess eng… [T:Codex/rollout-]
- **BL-002** (TestRequest, Scenario) [2026-02-23 21:21] — please go ahead with perft checker [T:Codex/rollout-]
- **BL-003** (FeatureRequest) [2026-02-23 21:42] — ok, it's time to quickly assess the Elo (n=20 games) against different Stockfish skills... please write a script [T:Codex/rollout-]

## Evidence pointers

- [R:chess-icon-codex] — repo at `/Users/mathieuacher/SANDBOX/chess-icon-codex`
- [T:chess-icon-codex/claude] — Claude sessions at `~/.claude/projects/chess-icon-codex...`
- [T:chess-icon-codex/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-icon-codex

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.