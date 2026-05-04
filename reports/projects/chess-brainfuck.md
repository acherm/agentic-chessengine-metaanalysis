# chess-brainfuck

_Evidence-based dossier. Generated 2026-04-22 14:52 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-brainfuck` [R:chess-brainfuck]
- **Primary language:** Python
- **Coding agent(s):** Codex
- **Period:** 2026-02-20 19:16 → 2026-03-23 18:18
- **LOC by language:** Python (5881 LOC, 22 files), JSON (728 LOC, 18 files), Markdown (299 LOC, 4 files), Brainfuck (11 LOC, 11 files), Text (1 LOC, 1 files)
- **Totals:** 56 files, 6920 LOC [S:scan]
- **Git:** 6 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:chess-brainfuck/claude]
- Claude models seen: —
- Codex sessions: 2 [T:chess-brainfuck/codex]
- Codex models seen: gpt-5.3-codex, gpt-5.4

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 2 | 38 | 121271591 | 449365 | 117598464 | — | $170.78 |
| **Total** |  |  |  |  |  |  | **$170.78** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| Castling | 30 | `README.md` |
| Time management | 22 | `README.md` |
| PGN | 20 | `README.md` |
| Promotion | 9 | `README.md` |
| UCI protocol | 8 | `README.md` |
| Check/Checkmate | 7 | `README.md` |
| Material counting | 6 | `README.md` |
| Perft | 5 | `README.md` |
| En passant | 5 | `ROADMAP.md` |
| Alpha-beta | 5 | `README.md` |
| FEN parsing | 4 | `tests/test_bf_board.py` |
| Evaluation/PST | 4 | `README.md` |
| Minimax/Negamax | 3 | `README.md` |
| Iterative deepening | 2 | `README.md` |
| Transposition table | 2 | `ROADMAP.md` |
| Quiescence | 1 | `src/search.py` |
| Principal-variation (PV) | 1 | `src/search.py` |
| Late-move reduction (LMR) | 1 | `src/search.py` |
| King safety | 1 | `README.md` |
| Opening book | 1 | `src/bf_uci_engine.py` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | exec_command | 573 |
| Codex | write_stdin | 566 |
| Codex | update_plan | 2 |

## Interaction profile

- Total user prompts (both agents): **38**
- Avg prompt length: 181.8 chars
- Intent distribution:
  - Other: 25
  - FeatureRequest: 6
  - ToolingBuild: 3
  - Documentation: 3
  - Question: 3
  - BugFixRequest: 2
  - TestRequest: 1
  - Scenario: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-02-20 19:16 — session `rollout-`_

```
I want to build a chess engine in Brainfuck programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-20 19:24 | Codex | Other | brainfuck_selector.bf is one-line, we're far from having a chess engine in brainfuck... what's your plan? |
| 3 | 2026-02-20 19:26 | Codex | Other | yes, go ahead |
| 4 | 2026-02-20 19:36 | Codex | Other | please go ahead |
| 5 | 2026-02-20 20:40 | Codex | Other | go ahead |
| 6 | 2026-02-20 20:47 | Codex | Other | please go ahead |
| 7 | 2026-02-20 21:57 | Codex | Other | please go ahead |
| 8 | 2026-02-20 22:14 | Codex | Other | let's go! |
| 9 | 2026-02-20 22:42 | Codex | Other | go ahead, complete Phase B |
| 10 | 2026-02-20 22:52 | Codex | Other | let's try Phase C, go |
| 11 | 2026-02-20 23:23 | Codex | Other | go to Phase D |
| 12 | 2026-02-21 12:44 | Codex | Other | continue |
| 13 | 2026-02-21 13:02 | Codex | FeatureRequest | create a git and commit |
| 14 | 2026-02-21 13:07 | Codex | Documentation | please now run a first Elo gauntlet with the new search path and produce a baseline JSON/PGN... I would be interested to document how compi… |
| 15 | 2026-02-21 13:29 | Codex | Documentation | please commit these new gauntlet/doc changes in a follow-up commit, including games in PGN then run a larger baseline next (more Elo levels… |
| 16 | 2026-02-21 13:51 | Codex | BugFixRequest | some games lead to draw, but it's strange why... I suspect there is a kind of issue with UCI, perhaps an illegal move of brainfuck chess? p… |
| 17 | 2026-02-21 15:13 | Codex | Other | I see, thanks... now the challenge would be to improve the chess engine, and it seems the performance... any idea? please follow your origi… |
| 18 | 2026-02-23 08:35 | Codex | FeatureRequest,ToolingBuild | tell me how torun that larger Elo gauntlet on this optimized build and produce fresh JSON/PGN baselines, I will execute on my side |
| 19 | 2026-02-23 08:39 | Codex | ToolingBuild | mathieuacher@Mathieus-MacBook-Pro chess-brainfuck % >.... --engine-cmd "/Users/mathieuacher/SANDBOX/chess-brainfuck/.venv/bin/python /Users… |
| 20 | 2026-02-23 21:15 | Codex | Other | please improve the strenght/Elo of the brainfuck chess engine... the goal is to win/draw some games against 1320 Elo SF |
| 21 | 2026-02-23 22:15 | Codex | Question | how to max_plies=300, games-per-level=12, --opponent-elos 1320 ? |
| 22 | 2026-02-26 04:55 | Codex | BugFixRequest,Scenario | there is an issue with the bench, with some draws being not real draws, but I think an issue with the UCI protocol, perhaps invalid move fr… |
| 23 | 2026-02-26 09:20 | Codex | Question | which command to run? |
| 24 | 2026-02-26 21:34 | Codex | Other | please significantly improve the chess engine |
| 25 | 2026-02-27 05:43 | Codex | Other | yes please run some games to assess Elo |
| 26 | 2026-02-27 06:11 | Codex | Other | please commit at this step |
| 27 | 2026-02-27 06:18 | Codex | Other | the draws seem legit, but a bit by luck (incidental repetition)... anyway, the level of the chess engine is very weak... please improve |
| 28 | 2026-02-27 07:07 | Codex | Other | yes please go |
| 29 | 2026-03-05 23:31 | Codex | Other | go for a large eval |
| 30 | 2026-03-06 00:14 | Codex | Other | please commit, including an Elo assessment |
| 31 | 2026-03-06 00:17 | Codex | Other | I'd like to review this repo and understand the basic architecture of the Brainfuck chess engine, the way it is implemented, the features o… |
| 32 | 2026-03-06 00:26 | Codex | Other | any chance to remove "search.py" and have a pure Brainfuck implementation and thus assessment? |
| 33 | 2026-03-23 18:01 | Codex | FeatureRequest,Documentation | can you write down this, upfront, in the README.md? |
| 34 | 2026-03-23 18:02 | Codex | FeatureRequest | add Mathieu Acher and Codex (GPT 5.3) as developers... add also a warning stating it's kind of failure since it's not a pure Brainfuck solu… |
| 35 | 2026-03-23 18:05 | Codex | Other | great! please commit and push to agentic-chessengine-brainfuck-codexfailure in Github |
| 36 | 2026-03-23 18:12 | Codex | Other | please retry |
| 37 | 2026-03-23 18:16 | Codex | Other | give me an HTTPS remote instead, and I can repoint origin and try that path. => lets' try this |
| 38 | 2026-03-23 18:17 | Codex | FeatureRequest | the Github repo is not existing... you have to create it |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `deac6ea` | 2026-03-23T19:05:55+01:00 | Mathieu Acher | Clarify hybrid status in README |
| `ddf5b46` | 2026-03-06T01:15:20+01:00 | Mathieu Acher | Add large gauntlet Elo assessment (2026-03-06) |
| `9a8c240` | 2026-02-27T08:49:45+01:00 | Mathieu Acher | Speed up core search path and strengthen tactical play |
| `967491f` | 2026-02-27T07:12:13+01:00 | Mathieu Acher | Improve engine strength and fix gauntlet protocol accounting |
| `964e11c` | 2026-02-21T14:31:40+01:00 | Mathieu Acher | chore: add gauntlet baseline artifacts and runtime docs |
| `bca7fdf` | 2026-02-21T14:06:10+01:00 | Mathieu Acher | feat: implement Brainfuck kernel engine through Phase D |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **10** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, ToolingBuild) [2026-02-20 19:16] — I want to build a chess engine in Brainfuck programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against ches… [T:Codex/rollout-]
- **BL-002** (FeatureRequest) [2026-02-21 13:02] — create a git and commit [T:Codex/rollout-]
- **BL-003** (Documentation) [2026-02-21 13:07] — please now run a first Elo gauntlet with the new search path and produce a baseline JSON/PGN... I would be interested to document how compiled kernels (in bf format) are executed,… [T:Codex/rollout-]
- **BL-004** (Documentation) [2026-02-21 13:29] — please commit these new gauntlet/doc changes in a follow-up commit, including games in PGN then run a larger baseline next (more Elo levels and games) [T:Codex/rollout-]
- **BL-005** (BugFixRequest) [2026-02-21 13:51] — some games lead to draw, but it's strange why... I suspect there is a kind of issue with UCI, perhaps an illegal move of brainfuck chess? please investigate [T:Codex/rollout-]
- **BL-006** (FeatureRequest, ToolingBuild) [2026-02-23 08:35] — tell me how torun that larger Elo gauntlet on this optimized build and produce fresh JSON/PGN baselines, I will execute on my side [T:Codex/rollout-]
- **BL-007** (ToolingBuild) [2026-02-23 08:39] — mathieuacher@Mathieus-MacBook-Pro chess-brainfuck % >.... --engine-cmd "/Users/mathieuacher/SANDBOX/chess-brainfuck/.venv/bin/python /Users/mathieuacher/SANDBOX/chess-brainfuck/sr… [T:Codex/rollout-]
- **BL-008** (BugFixRequest, Scenario) [2026-02-26 04:55] — there is an issue with the bench, with some draws being not real draws, but I think an issue with the UCI protocol, perhaps invalid move from the engine, or not enough time to pla… [T:Codex/rollout-]
- **BL-009** (FeatureRequest) [2026-03-23 18:02] — add Mathieu Acher and Codex (GPT 5.3) as developers... add also a warning stating it's kind of failure since it's not a pure Brainfuck solution (beware of coding agents!) [T:Codex/rollout-]
- **BL-010** (FeatureRequest) [2026-03-23 18:17] — the Github repo is not existing... you have to create it [T:Codex/rollout-]

## Evidence pointers

- [R:chess-brainfuck] — repo at `/Users/mathieuacher/SANDBOX/chess-brainfuck`
- [T:chess-brainfuck/claude] — Claude sessions at `~/.claude/projects/chess-brainfuck...`
- [T:chess-brainfuck/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-brainfuck

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.