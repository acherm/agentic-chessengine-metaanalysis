# chess-py

_Evidence-based dossier. Generated 2026-04-22 14:53 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-py` [R:chess-py]
- **Primary language:** Python
- **Coding agent(s):** Codex
- **Period:** 2026-02-11 08:12 → 2026-02-16 21:01
- **LOC by language:** Python (3769 LOC, 19 files), Markdown (84 LOC, 1 files), Text (33 LOC, 1 files), Shell (4 LOC, 1 files)
- **Totals:** 22 files, 3890 LOC [S:scan]
- **Git:** not a git repo

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:chess-py/claude]
- Claude models seen: —
- Codex sessions: 1 [T:chess-py/codex]
- Codex models seen: gpt-5.2, gpt-5.3-codex

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 1 | 10 | 19373958 | 273823 | 18671488 | — | $29.29 |
| **Total** |  |  |  |  |  |  | **$29.29** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| UCI protocol | 11 | `README.md` |
| FEN parsing | 10 | `README.md` |
| Promotion | 5 | `README.md` |
| Board: 0x88 | 5 | `README.md` |
| Time management | 5 | `README.md` |
| Castling | 4 | `README.md` |
| Perft | 3 | `README.md` |
| Check/Checkmate | 3 | `tools/match.py` |
| PGN | 3 | `README.md` |
| Transposition table | 3 | `chesspy/board.py` |
| Zobrist hashing | 3 | `chesspy/board.py` |
| Null-move pruning | 3 | `chesspy/board.py` |
| Evaluation/PST | 3 | `chesspy/board.py` |
| Material counting | 3 | `chesspy/board.py` |
| En passant | 2 | `README.md` |
| Minimax/Negamax | 2 | `README.md` |
| Alpha-beta | 2 | `README.md` |
| Iterative deepening | 2 | `README.md` |
| Quiescence | 2 | `README.md` |
| Futility pruning | 1 | `chesspy/search.py` |
| Tapered evaluation | 1 | `chesspy/eval.py` |
| Pawn structure | 1 | `chesspy/eval.py` |
| Mobility | 1 | `chesspy/eval.py` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | exec_command | 136 |
| Codex | write_stdin | 58 |
| Codex | update_plan | 24 |

## Interaction profile

- Total user prompts (both agents): **10**
- Avg prompt length: 840.8 chars
- Intent distribution:
  - Scenario: 5
  - FeatureRequest: 3
  - Other: 2
  - TestRequest: 1
  - ToolingBuild: 1
  - Question: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-02-11 08:12 — session `rollout-`_

```
I want to build a chess engine in Python programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-11 08:38 | Codex | Other | Target is ~1500 blitz please tune defaults (depth/time, eval, move ordering) and launch a quick experiment |
| 3 | 2026-02-11 09:15 | Codex | Other | Please now improve significantly the chess engine |
| 4 | 2026-02-11 09:40 | Codex | FeatureRequest,Scenario | please add an opening-suite option to match.py (randomize starts) so the Elo estimate is much more reliable. |
| 5 | 2026-02-11 10:31 | Codex | Scenario | mathieuacher@Mathieus-MacBook-Pro chess-py % python3 /Users/mathieuacher/SANDBOX/chess-py/tools/match.py \ --games 50 --movetime-ms 250 \ -… |
| 6 | 2026-02-11 10:47 | Codex | Scenario | mathieuacher@Mathieus-MacBook-Pro chess-py % python3 /Users/mathieuacher/SANDBOX/chess-py/tools/match.py \ --games 50 --movetime-ms 250 \ -… |
| 7 | 2026-02-11 13:03 | Codex | Scenario | mathieuacher@Mathieus-MacBook-Pro chess-py % python3 /Users/mathieuacher/SANDBOX/chess-py/tools/match.py \ --games 50 --movetime-ms 250 \ -… |
| 8 | 2026-02-11 16:35 | Codex | Scenario | python3 /Users/mathieuacher/SANDBOX/chess-py/tools/match.py \ --games 50 --movetime-ms 250 \ --openings /Users/mathieuacher/SANDBOX/chess-p… |
| 9 | 2026-02-16 20:56 | Codex | Question | how to re-run matchs and accurately assess Elo? |
| 10 | 2026-02-16 20:58 | Codex | FeatureRequest | yes, please write such a script |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **5** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, ToolingBuild) [2026-02-11 08:12] — I want to build a chess engine in Python programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess e… [T:Codex/rollout-]
- **BL-002** (FeatureRequest, Scenario) [2026-02-11 09:40] — please add an opening-suite option to match.py (randomize starts) so the Elo estimate is much more reliable. [T:Codex/rollout-]
- **BL-003** (Scenario) [2026-02-11 10:31] — mathieuacher@Mathieus-MacBook-Pro chess-py % python3 /Users/mathieuacher/SANDBOX/chess-py/tools/match.py \ --games 50 --movetime-ms 250 \ --openings /Users/mathieuacher/SANDBOX/ch… [T:Codex/rollout-]
- **BL-004** (Scenario) [2026-02-11 16:35] — python3 /Users/mathieuacher/SANDBOX/chess-py/tools/match.py \ --games 50 --movetime-ms 250 \ --openings /Users/mathieuacher/SANDBOX/chess-py/openings.example.txt \ --openings-seed… [T:Codex/rollout-]
- **BL-005** (FeatureRequest) [2026-02-16 20:58] — yes, please write such a script [T:Codex/rollout-]

## Evidence pointers

- [R:chess-py] — repo at `/Users/mathieuacher/SANDBOX/chess-py`
- [T:chess-py/claude] — Claude sessions at `~/.claude/projects/chess-py...`
- [T:chess-py/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-py

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.