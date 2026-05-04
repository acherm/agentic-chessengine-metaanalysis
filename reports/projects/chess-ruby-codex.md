# chess-ruby-codex

_Evidence-based dossier. Generated 2026-04-22 14:53 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-ruby-codex` [R:chess-ruby-codex]
- **Primary language:** Ruby
- **Coding agent(s):** Codex
- **Period:** 2026-03-12 19:36 → 2026-03-13 07:03
- **LOC by language:** JSON (122232 LOC, 27 files), Ruby (2125 LOC, 15 files), Markdown (86 LOC, 1 files)
- **Totals:** 43 files, 124443 LOC [S:scan]
- **Git:** not a git repo

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:chess-ruby-codex/claude]
- Claude models seen: —
- Codex sessions: 1 [T:chess-ruby-codex/codex]
- Codex models seen: gpt-5.3-codex

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 1 | 7 | 43425851 | 121863 | 42037376 | — | $60.76 |
| **Total** |  |  |  |  |  |  | **$60.76** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| Time management | 30 | `README.md` |
| UCI protocol | 9 | `README.md` |
| Null-move pruning | 8 | `README.md` |
| Opening book | 5 | `README.md` |
| Material counting | 4 | `scripts/run_matches.rb` |
| FEN parsing | 3 | `test/test_position.rb` |
| Perft | 3 | `README.md` |
| Castling | 3 | `test/test_position.rb` |
| En passant | 3 | `lib/ruby_chess_engine/position.rb` |
| Promotion | 3 | `lib/ruby_chess_engine/position.rb` |
| Check/Checkmate | 3 | `scripts/run_matches.rb` |
| Transposition table | 2 | `lib/ruby_chess_engine/position.rb` |
| Minimax/Negamax | 1 | `lib/ruby_chess_engine/search.rb` |
| Alpha-beta | 1 | `README.md` |
| Quiescence | 1 | `lib/ruby_chess_engine/search.rb` |
| Zobrist hashing | 1 | `lib/ruby_chess_engine/position.rb` |
| Killer moves | 1 | `lib/ruby_chess_engine/search.rb` |
| Late-move reduction (LMR) | 1 | `lib/ruby_chess_engine/search.rb` |
| Evaluation/PST | 1 | `lib/ruby_chess_engine/evaluator.rb` |
| King safety | 1 | `lib/ruby_chess_engine/evaluator.rb` |
| Pawn structure | 1 | `lib/ruby_chess_engine/evaluator.rb` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | write_stdin | 268 |
| Codex | exec_command | 187 |

## Interaction profile

- Total user prompts (both agents): **7**
- Avg prompt length: 39.3 chars
- Intent distribution:
  - Other: 5
  - FeatureRequest: 1
  - TestRequest: 1
  - ToolingBuild: 1
  - Question: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-03-12 19:36 — session `rollout-`_

```
I want to build a chess engine in Ruby… at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of “similar” levels.

```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-03-12 19:51 | Codex | Question | can you run and assess the Elo? |
| 3 | 2026-03-12 20:05 | Codex | Other | it's very bad... please improve |
| 4 | 2026-03-12 20:20 | Codex | Other | yes please go |
| 5 | 2026-03-12 20:59 | Codex | Other | go |
| 6 | 2026-03-12 22:19 | Codex | Other | go |
| 7 | 2026-03-13 06:50 | Codex | Other | continue |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **1** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, ToolingBuild) [2026-03-12 19:36] — I want to build a chess engine in Ruby… at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of “similar” level… [T:Codex/rollout-]

## Evidence pointers

- [R:chess-ruby-codex] — repo at `/Users/mathieuacher/SANDBOX/chess-ruby-codex`
- [T:chess-ruby-codex/claude] — Claude sessions at `~/.claude/projects/chess-ruby-codex...`
- [T:chess-ruby-codex/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-ruby-codex

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.