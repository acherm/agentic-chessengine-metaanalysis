# chess-mojo

_Evidence-based dossier. Generated 2026-04-22 14:53 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-mojo` [R:chess-mojo]
- **Primary language:** Mojo
- **Coding agent(s):** Codex
- **Period:** 2026-02-16 21:01 → 2026-02-16 22:27
- **LOC by language:** Mojo (1907 LOC, 1 files), Python (864 LOC, 7 files), JSON (475 LOC, 9 files), Markdown (153 LOC, 2 files), Text (73 LOC, 9 files)
- **Totals:** 28 files, 3472 LOC [S:scan]
- **Git:** not a git repo

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:chess-mojo/claude]
- Claude models seen: —
- Codex sessions: 1 [T:chess-mojo/codex]
- Codex models seen: gpt-5.3-codex

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 1 | 7 | 16639061 | 125057 | 16081152 | — | $24.06 |
| **Total** |  |  |  |  |  |  | **$24.06** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| Time management | 15 | `docs/ROADMAP.md` |
| Castling | 9 | `results/20260216_225023/games_vs_sf_1320.pgn` |
| UCI protocol | 6 | `README.md` |
| Perft | 4 | `README.md` |
| Material counting | 4 | `docs/ROADMAP.md` |
| FEN parsing | 3 | `docs/ROADMAP.md` |
| PGN | 2 | `README.md` |
| Alpha-beta | 2 | `README.md` |
| Quiescence | 2 | `docs/ROADMAP.md` |
| Promotion | 1 | `src/mojo_engine/main.mojo` |
| Check/Checkmate | 1 | `src/mojo_engine/main.mojo` |
| Board: bitboard | 1 | `docs/ROADMAP.md` |
| Minimax/Negamax | 1 | `src/mojo_engine/main.mojo` |
| Iterative deepening | 1 | `docs/ROADMAP.md` |
| Transposition table | 1 | `docs/ROADMAP.md` |
| Mobility | 1 | `docs/ROADMAP.md` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | exec_command | 225 |
| Codex | write_stdin | 31 |

## Interaction profile

- Total user prompts (both agents): **7**
- Avg prompt length: 216.6 chars
- Intent distribution:
  - Other: 4
  - FeatureRequest: 2
  - TestRequest: 2
  - ToolingBuild: 2
  - BugFixRequest: 1
  - Scenario: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-02-16 21:01 — session `rollout-`_

```
I want to build a chess engine in Mojo programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-16 21:16 | Codex | FeatureRequest,ToolingBuild | mathieuacher@Mathieus-MacBook-Pro chess-mojo % uv venv && source .venv/bin/activate Using CPython 3.12.11 Creating virtual environment at: … |
| 3 | 2026-02-16 21:31 | Codex | BugFixRequest,TestRequest | please fix legal move generation and other stuff for a meaninful Elo estimate... what about perft? |
| 4 | 2026-02-16 22:00 | Codex | Other | the engine is very weak... let's try a pure Mojo engine |
| 5 | 2026-02-16 22:06 | Codex | Other | you can't try to take a tour of every possible syntaxes of Mojo... it would take too much time |
| 6 | 2026-02-16 22:06 | Codex | Other | you can't try to take a tour of every possible syntaxes of Mojo... it would take too much time |
| 7 | 2026-02-16 22:10 | Codex | Other | you can't try to take a tour of every possible syntaxes of Mojo... it would take too much time |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **3** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, ToolingBuild) [2026-02-16 21:01] — I want to build a chess engine in Mojo programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess eng… [T:Codex/rollout-]
- **BL-002** (FeatureRequest, ToolingBuild) [2026-02-16 21:16] — mathieuacher@Mathieus-MacBook-Pro chess-mojo % uv venv && source .venv/bin/activate Using CPython 3.12.11 Creating virtual environment at: .venv Activate with: source .venv/bin/ac… [T:Codex/rollout-]
- **BL-003** (BugFixRequest, TestRequest, Scenario) [2026-02-16 21:31] — please fix legal move generation and other stuff for a meaninful Elo estimate... what about perft? [T:Codex/rollout-]

## Evidence pointers

- [R:chess-mojo] — repo at `/Users/mathieuacher/SANDBOX/chess-mojo`
- [T:chess-mojo/claude] — Claude sessions at `~/.claude/projects/chess-mojo...`
- [T:chess-mojo/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-mojo

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.