# chess-rust-codex

_Evidence-based dossier. Generated 2026-04-22 14:53 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-rust-codex` [R:chess-rust-codex]
- **Primary language:** Rust
- **Coding agent(s):** Codex
- **Period:** 2026-02-16 21:14 → 2026-02-17 07:21
- **LOC by language:** Rust (1574 LOC, 3 files), Markdown (172 LOC, 2 files), Shell (66 LOC, 2 files), TOML (7 LOC, 1 files)
- **Totals:** 8 files, 1819 LOC [S:scan]
- **Git:** 2 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:chess-rust-codex/claude]
- Claude models seen: —
- Codex sessions: 1 [T:chess-rust-codex/codex]
- Codex models seen: gpt-5.3-codex

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 1 | 3 | 10594824 | 79865 | 10192128 | — | $15.32 |
| **Total** |  |  |  |  |  |  | **$15.32** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| Time management | 18 | `README.md` |
| Castling | 13 | `matches/sf_1800.pgn` |
| UCI protocol | 5 | `README.md` |
| PGN | 4 | `README.md` |
| Perft | 2 | `README.md` |
| Board: bitboard | 2 | `src/uci.rs` |
| Minimax/Negamax | 2 | `README.md` |
| Quiescence | 2 | `README.md` |
| Transposition table | 2 | `README.md` |
| Null-move pruning | 2 | `README.md` |
| Pawn structure | 2 | `README.md` |
| Mobility | 2 | `README.md` |
| Material counting | 2 | `README.md` |
| FEN parsing | 1 | `src/uci.rs` |
| En passant | 1 | `src/engine.rs` |
| Promotion | 1 | `src/engine.rs` |
| Check/Checkmate | 1 | `src/engine.rs` |
| Alpha-beta | 1 | `README.md` |
| Iterative deepening | 1 | `README.md` |
| Killer moves | 1 | `README.md` |
| History heuristic | 1 | `README.md` |
| Principal-variation (PV) | 1 | `README.md` |
| Late-move reduction (LMR) | 1 | `README.md` |
| King safety | 1 | `src/engine.rs` |
| Opening book | 1 | `src/engine.rs` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | exec_command | 93 |
| Codex | write_stdin | 36 |

## Interaction profile

- Total user prompts (both agents): **3**
- Avg prompt length: 6416.3 chars
- Intent distribution:
  - FeatureRequest: 2
  - TestRequest: 1
  - ToolingBuild: 1
  - Scenario: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-02-16 21:14 — session `rollout-`_

```
I want to build a chess engine in Rust programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-16 22:56 | Codex | Scenario | 31 of 60 (rust-engine vs stockfish-1600) Finished game 31 (rust-engine vs stockfish-1600): 1-0 {White mates} Score of rust-engine vs stockf… |
| 3 | 2026-02-17 05:47 | Codex | FeatureRequest | commit first (including current Elo assessment report) and then add a full tapered eval + phase interpolation and TT aging/replacement tuni… |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `6ec6f2a` | 2026-02-17T08:21:07+01:00 | Mathieu Acher | feat: add tapered eval and TT aging replacement policy |
| `d562497` | 2026-02-17T08:16:19+01:00 | Mathieu Acher | feat: strengthen engine and add Elo assessment report |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **3** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, ToolingBuild) [2026-02-16 21:14] — I want to build a chess engine in Rust programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess eng… [T:Codex/rollout-]
- **BL-002** (Scenario) [2026-02-16 22:56] — 31 of 60 (rust-engine vs stockfish-1600) Finished game 31 (rust-engine vs stockfish-1600): 1-0 {White mates} Score of rust-engine vs stockfish-1600: 11 - 15 - 5 [0.435] 31 Started… [T:Codex/rollout-]
- **BL-003** (FeatureRequest) [2026-02-17 05:47] — commit first (including current Elo assessment report) and then add a full tapered eval + phase interpolation and TT aging/replacement tuning. [T:Codex/rollout-]

## Evidence pointers

- [R:chess-rust-codex] — repo at `/Users/mathieuacher/SANDBOX/chess-rust-codex`
- [T:chess-rust-codex/claude] — Claude sessions at `~/.claude/projects/chess-rust-codex...`
- [T:chess-rust-codex/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-rust-codex

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.