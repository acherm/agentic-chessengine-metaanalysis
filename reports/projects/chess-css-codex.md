# chess-css-codex

_Evidence-based dossier. Generated 2026-04-22 14:52 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-css-codex` [R:chess-css-codex]
- **Primary language:** HTML
- **Coding agent(s):** Codex
- **Period:** 2026-02-28 14:24 → 2026-03-01 07:48
- **LOC by language:** HTML (34988 LOC, 3 files), CSS (2093 LOC, 5 files), Python (1388 LOC, 10 files), Markdown (177 LOC, 2 files), TOML (21 LOC, 1 files), JSON (17 LOC, 1 files)
- **Totals:** 22 files, 38684 LOC [S:scan]
- **Git:** 1 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:chess-css-codex/claude]
- Claude models seen: —
- Codex sessions: 1 [T:chess-css-codex/codex]
- Codex models seen: gpt-5.3-codex

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 1 | 17 | 18165231 | 224606 | 17469824 | — | $27.14 |
| **Total** |  |  |  |  |  |  | **$27.14** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| UCI protocol | 7 | `pyproject.toml` |
| Mobility | 5 | `README.md` |
| FEN parsing | 4 | `strict-css/index.html` |
| Time management | 3 | `tests/test_smoke.py` |
| Promotion | 2 | `README.md` |
| Check/Checkmate | 2 | `src/chess_css/engine.py` |
| Quiescence | 2 | `README.md` |
| Transposition table | 2 | `README.md` |
| Material counting | 2 | `src/chess_css/engine.py` |
| En passant | 1 | `src/chess_css/search.py` |
| Minimax/Negamax | 1 | `src/chess_css/search.py` |
| Alpha-beta | 1 | `README.md` |
| Iterative deepening | 1 | `README.md` |
| History heuristic | 1 | `README.md` |
| Principal-variation (PV) | 1 | `README.md` |
| Evaluation/PST | 1 | `README.md` |
| Pawn structure | 1 | `src/chess_css/engine.py` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | exec_command | 178 |
| Codex | write_stdin | 13 |

## Interaction profile

- Total user prompts (both agents): **17**
- Avg prompt length: 83.0 chars
- Intent distribution:
  - Other: 8
  - FeatureRequest: 4
  - Scenario: 4
  - TestRequest: 1
  - ToolingBuild: 1
  - Constraint: 1
  - BugFixRequest: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-02-28 14:24 — session `rollout-`_

```
I want to build a chess engine in pure CSS programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-28 14:40 | Codex | Other | the problem with your solution is that the main part is in Python... I want a pure CSS solution |
| 3 | 2026-02-28 14:42 | Codex | Other | Strict pure CSS |
| 4 | 2026-02-28 16:17 | Codex | FeatureRequest | create git and commit |
| 5 | 2026-02-28 16:19 | Codex | FeatureRequest,Scenario | as recognized it is a finite-state opening-book engine. It is strict CSS but not a full chess search engine. let's be more ambitious and im… |
| 6 | 2026-02-28 17:31 | Codex | Constraint | you don't get it... I don't want a Python solution at all... Only CSS. Even if it's hard |
| 7 | 2026-03-01 05:30 | Codex | Other | go |
| 8 | 2026-03-01 05:50 | Codex | FeatureRequest | try to implement a pseudo-legal moves generation |
| 9 | 2026-03-01 06:01 | Codex | Other | not general at all, not covering enough moves |
| 10 | 2026-03-01 06:12 | Codex | Other | True occupancy-dependent pseudo-legal generation (arbitrary blockers/en-passant/castling state) and full legal move checking are not genera… |
| 11 | 2026-03-01 06:18 | Codex | Other | yes go ahead |
| 12 | 2026-03-01 06:25 | Codex | Scenario | goal is to have a random chess engine in CSS... generate randomly a legal move and play |
| 13 | 2026-03-01 06:44 | Codex | Scenario | a bit hard to play... could you improve the interface and have a real chess board to play with? |
| 14 | 2026-03-01 06:52 | Codex | Other | the workflow seems very complicated |
| 15 | 2026-03-01 07:17 | Codex | Other | does not work well |
| 16 | 2026-03-01 07:31 | Codex | BugFixRequest | can't select an origin square (e2 by default, but when clicking other squares doesn't work... same for target) |
| 17 | 2026-03-01 07:41 | Codex | Scenario | once played, it seems the status/state of the game is not updated... I'd like to play a real game against a CSS engine |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `1bb2c45` | 2026-02-28T17:17:59+01:00 | Mathieu Acher | Initial commit: CSS chess engine prototypes and strict CSS variant |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **9** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, ToolingBuild) [2026-02-28 14:24] — I want to build a chess engine in pure CSS programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess… [T:Codex/rollout-]
- **BL-002** (FeatureRequest) [2026-02-28 16:17] — create git and commit [T:Codex/rollout-]
- **BL-003** (FeatureRequest, Scenario) [2026-02-28 16:19] — as recognized it is a finite-state opening-book engine. It is strict CSS but not a full chess search engine. let's be more ambitious and implement a full chess search engine [T:Codex/rollout-]
- **BL-004** (Constraint) [2026-02-28 17:31] — you don't get it... I don't want a Python solution at all... Only CSS. Even if it's hard [T:Codex/rollout-]
- **BL-005** (FeatureRequest) [2026-03-01 05:50] — try to implement a pseudo-legal moves generation [T:Codex/rollout-]
- **BL-006** (Scenario) [2026-03-01 06:25] — goal is to have a random chess engine in CSS... generate randomly a legal move and play [T:Codex/rollout-]
- **BL-007** (Scenario) [2026-03-01 06:44] — a bit hard to play... could you improve the interface and have a real chess board to play with? [T:Codex/rollout-]
- **BL-008** (BugFixRequest) [2026-03-01 07:31] — can't select an origin square (e2 by default, but when clicking other squares doesn't work... same for target) [T:Codex/rollout-]
- **BL-009** (Scenario) [2026-03-01 07:41] — once played, it seems the status/state of the game is not updated... I'd like to play a real game against a CSS engine [T:Codex/rollout-]

## Evidence pointers

- [R:chess-css-codex] — repo at `/Users/mathieuacher/SANDBOX/chess-css-codex`
- [T:chess-css-codex/claude] — Claude sessions at `~/.claude/projects/chess-css-codex...`
- [T:chess-css-codex/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-css-codex

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.