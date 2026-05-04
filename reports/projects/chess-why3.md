# chess-why3

_Evidence-based dossier. Generated 2026-04-22 14:53 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-why3` [R:chess-why3]
- **Primary language:** OCaml
- **Coding agent(s):** Codex
- **Period:** 2026-02-17 12:48 → 2026-02-18 19:57
- **LOC by language:** OCaml (2265 LOC, 5 files), JSON (775 LOC, 17 files), Python (564 LOC, 3 files), Markdown (531 LOC, 19 files), Why3 (371 LOC, 1 files), Shell (24 LOC, 1 files)
- **Totals:** 46 files, 4530 LOC [S:scan]
- **Git:** 1 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:chess-why3/claude]
- Claude models seen: —
- Codex sessions: 1 [T:chess-why3/codex]
- Codex models seen: gpt-5.3-codex

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 1 | 9 | 16839308 | 87065 | 15992704 | — | $23.92 |
| **Total** |  |  |  |  |  |  | **$23.92** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| UCI protocol | 58 | `Makefile` |
| Time management | 48 | `docs/ROADMAP.md` |
| Castling | 31 | `README.md` |
| PGN | 21 | `README.md` |
| Material counting | 7 | `README.md` |
| Minimax/Negamax | 6 | `README.md` |
| Null-move pruning | 5 | `_build/default/src/uci_ocaml/main.ml` |
| Quiescence | 4 | `README.md` |
| FEN parsing | 3 | `docs/ROADMAP.md` |
| Check/Checkmate | 3 | `README.md` |
| Alpha-beta | 3 | `README.md` |
| Perft | 2 | `README.md` |
| Iterative deepening | 2 | `README.md` |
| Transposition table | 2 | `README.md` |
| Promotion | 1 | `README.md` |
| Aspiration windows | 1 | `README.md` |
| Evaluation/PST | 1 | `docs/ROADMAP.md` |
| Tapered evaluation | 1 | `docs/ROADMAP.md` |
| Mobility | 1 | `docs/ROADMAP.md` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | exec_command | 176 |
| Codex | write_stdin | 21 |
| Codex | update_plan | 2 |

## Interaction profile

- Total user prompts (both agents): **9**
- Avg prompt length: 144.6 chars
- Intent distribution:
  - Other: 6
  - FeatureRequest: 3
  - TestRequest: 1
  - ToolingBuild: 1
  - BugFixRequest: 1
  - Constraint: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-02-17 12:48 — session `rollout-`_

```
I want to build a chess engine in WhyML programming language (from Why3)... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-17 14:00 | Codex | FeatureRequest,BugFixRequest | why3 installed mathieuacher@Mathieus-MacBook-Pro chess-why3 % make why3-check Running Why3 smoke checks Warning, file "src/whyml/engine.mlw… |
| 3 | 2026-02-17 15:14 | Codex | Other | ok nice... now I want to bench/assess the chess engine, and estimate its Elo |
| 4 | 2026-02-17 18:06 | Codex | Other | please run it |
| 5 | 2026-02-17 18:13 | Codex | Other | the bench seems very fast (a couple of seconds)... |
| 6 | 2026-02-18 17:30 | Codex | Other | yes go ahead, maybe just 20 games |
| 7 | 2026-02-18 17:41 | Codex | Other | seems very weak... could it be due to time-control, that is not enough since Why3 may be not that fast? |
| 8 | 2026-02-18 17:48 | Codex | Other | ok then try to significantly improve the chess engine |
| 9 | 2026-02-18 19:53 | Codex | FeatureRequest | create git and commit |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `53702fc` | 2026-02-18T20:57:30+01:00 | Mathieu Acher | Initial WhyML chess engine + UCI + Elo benchmark tooling |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **3** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, ToolingBuild) [2026-02-17 12:48] — I want to build a chess engine in WhyML programming language (from Why3)... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games agai… [T:Codex/rollout-]
- **BL-002** (FeatureRequest, BugFixRequest, Constraint) [2026-02-17 14:00] — why3 installed mathieuacher@Mathieus-MacBook-Pro chess-why3 % make why3-check Running Why3 smoke checks Warning, file "src/whyml/engine.mlw", line 3, characters 2-20: the keyword … [T:Codex/rollout-]
- **BL-003** (FeatureRequest) [2026-02-18 19:53] — create git and commit [T:Codex/rollout-]

## Evidence pointers

- [R:chess-why3] — repo at `/Users/mathieuacher/SANDBOX/chess-why3`
- [T:chess-why3/claude] — Claude sessions at `~/.claude/projects/chess-why3...`
- [T:chess-why3/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-why3

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.