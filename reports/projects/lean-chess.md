# lean-chess

_Evidence-based dossier. Generated 2026-04-22 14:55 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/lean-chess` [R:lean-chess]
- **Primary language:** Lean
- **Coding agent(s):** Codex
- **Period:** 2026-02-09 19:24 → 2026-02-10 20:29
- **LOC by language:** Lean (1670 LOC, 12 files), Shell (567 LOC, 1 files), Markdown (91 LOC, 1 files), JSON (5 LOC, 1 files)
- **Totals:** 15 files, 2333 LOC [S:scan]
- **Git:** not a git repo

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:lean-chess/claude]
- Claude models seen: —
- Codex sessions: 1 [T:lean-chess/codex]
- Codex models seen: gpt-5.2, gpt-5.3-codex

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 1 | 21 | 87667411 | 301629 | 85070464 | — | $123.23 |
| **Total** |  |  |  |  |  |  | **$123.23** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| Time management | 27 | `matches/strengthwave2_sf1320_combined_g50.pgn` |
| Castling | 26 | `matches/strengthwave2_sf1320_combined_g50.pgn` |
| FEN parsing | 6 | `PerftMain.lean` |
| Material counting | 6 | `matches/strengthpass_sf1320_combined_g50_pvslmr.pgn` |
| UCI protocol | 5 | `README.md` |
| Perft | 5 | `PerftMain.lean` |
| Transposition table | 3 | `README.md` |
| En passant | 2 | `Chess/MoveGen.lean` |
| Check/Checkmate | 2 | `Chess/MoveGen.lean` |
| PGN | 2 | `README.md` |
| Alpha-beta | 2 | `README.md` |
| Quiescence | 2 | `README.md` |
| Promotion | 1 | `Chess/MoveGen.lean` |
| Minimax/Negamax | 1 | `Chess/Search.lean` |
| Iterative deepening | 1 | `README.md` |
| Null-move pruning | 1 | `Chess/Search.lean` |
| Evaluation/PST | 1 | `Chess/Eval.lean` |
| Pawn structure | 1 | `Chess/Eval.lean` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | write_stdin | 395 |
| Codex | exec_command | 337 |
| Codex | update_plan | 51 |

## Interaction profile

- Total user prompts (both agents): **21**
- Avg prompt length: 495.5 chars
- Intent distribution:
  - Other: 10
  - FeatureRequest: 7
  - ToolingBuild: 3
  - BugFixRequest: 3
  - Constraint: 2
  - Scenario: 2
  - TestRequest: 1
  - Question: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-02-09 19:24 — session `rollout-`_

```
I want to build a chess engine in Lean programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-09 19:47 | Codex | FeatureRequest,BugFixRequest | mathieuacher@Mathieus-MacBook-Pro lean-chess % lake build info: downloading https://releases.lean-lang.org/lean4/v4.27.0/lean-4.27.0-darwin… |
| 3 | 2026-02-10 07:42 | Codex | FeatureRequest | working fine! add a small script to run matches and summarize Elo from the PGNs. |
| 4 | 2026-02-10 07:53 | Codex | FeatureRequest | please add a small script to run matches and summarize Elo from the PGNs. |
| 5 | 2026-02-10 08:06 | Codex | BugFixRequest,Constraint | there is an issue with the PGN generation, with games with only 3 moves... |
| 6 | 2026-02-10 10:06 | Codex | Other | please continue |
| 7 | 2026-02-10 10:19 | Codex | Question | how to compute the Elo of the engine and get some games? |
| 8 | 2026-02-10 10:21 | Codex | FeatureRequest,ToolingBuild | mathieuacher@Mathieus-MacBook-Pro lean-chess % lake build /Users/mathieuacher/SANDBOX/lean-chess/scripts/run_match_and_elo.sh \ --games 300… |
| 9 | 2026-02-10 10:51 | Codex | Constraint | ok... the evaluation shows that the engine is very weak... I don't know if it's a misconfiguration during the evaluation (eg not enough sea… |
| 10 | 2026-02-10 11:21 | Codex | Other | yes let's go! |
| 11 | 2026-02-10 11:53 | Codex | Other | just to be sure the randomizer is part of the evaluation (as a way to reduce bias) or part of the chess engine (to have more diversity in t… |
| 12 | 2026-02-10 11:54 | Codex | Other | ok let's improve the evals with some randomization... however I have concerns regarding the strenght of the chess engine, try to dramatical… |
| 13 | 2026-02-10 13:20 | Codex | Other | not sure 300 games is necessary at this step... also, allocating enough time/searchdepth is needed |
| 14 | 2026-02-10 15:12 | Codex | BugFixRequest,Scenario | mathieuacher@Mathieus-MacBook-Pro lean-chess % /Users/mathieuacher/SANDBOX/lean-chess/scripts/run_match_and_elo.sh --games 24 --engine-dept… |
| 15 | 2026-02-10 17:30 | Codex | FeatureRequest | make a real speed pass |
| 16 | 2026-02-10 17:49 | Codex | Other | yes run a clean benchmark with estimation of Elo |
| 17 | 2026-02-10 18:16 | Codex | Other | the evolution of the chess engine seems not paying off with an estimated Elo of 1300... is it due to the way it is benchmarked? |
| 18 | 2026-02-10 18:27 | Codex | Other | yes go ahead |
| 19 | 2026-02-10 18:38 | Codex | Other | continue... |
| 20 | 2026-02-10 19:13 | Codex | Other | so now please focus on significanlty improving the engine |
| 21 | 2026-02-10 19:56 | Codex | FeatureRequest | yes implement the next strength wave and rerun the benchmark |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **9** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, ToolingBuild) [2026-02-09 19:24] — I want to build a chess engine in Lean programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess eng… [T:Codex/rollout-]
- **BL-002** (FeatureRequest, BugFixRequest, ToolingBuild) [2026-02-09 19:47] — mathieuacher@Mathieus-MacBook-Pro lean-chess % lake build info: downloading https://releases.lean-lang.org/lean4/v4.27.0/lean-4.27.0-darwin_aarch64.tar.zst Total: 469.1 MiB Speed:… [T:Codex/rollout-]
- **BL-003** (FeatureRequest) [2026-02-10 07:42] — working fine! add a small script to run matches and summarize Elo from the PGNs. [T:Codex/rollout-]
- **BL-004** (FeatureRequest) [2026-02-10 07:53] — please add a small script to run matches and summarize Elo from the PGNs. [T:Codex/rollout-]
- **BL-005** (BugFixRequest, Constraint) [2026-02-10 08:06] — there is an issue with the PGN generation, with games with only 3 moves... [T:Codex/rollout-]
- **BL-006** (Constraint) [2026-02-10 10:51] — ok... the evaluation shows that the engine is very weak... I don't know if it's a misconfiguration during the evaluation (eg not enough search depth, not enough time) or a more pr… [T:Codex/rollout-]
- **BL-007** (BugFixRequest, Scenario) [2026-02-10 15:12] — mathieuacher@Mathieus-MacBook-Pro lean-chess % /Users/mathieuacher/SANDBOX/lean-chess/scripts/run_match_and_elo.sh --games 24 --engine-depth 4 --tc 15+0.15 --seed 42 --pgn /Users/… [T:Codex/rollout-]
- **BL-008** (FeatureRequest) [2026-02-10 17:30] — make a real speed pass [T:Codex/rollout-]
- **BL-009** (FeatureRequest) [2026-02-10 19:56] — yes implement the next strength wave and rerun the benchmark [T:Codex/rollout-]

## Evidence pointers

- [R:lean-chess] — repo at `/Users/mathieuacher/SANDBOX/lean-chess`
- [T:lean-chess/claude] — Claude sessions at `~/.claude/projects/lean-chess...`
- [T:lean-chess/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/lean-chess

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.