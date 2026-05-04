# chessball

_Evidence-based dossier. Generated 2026-04-22 14:54 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chessball` [R:chessball]
- **Primary language:** Rust
- **Coding agent(s):** Codex
- **Period:** 2026-03-05 23:46 → 2026-04-02 13:01
- **LOC by language:** Text (18588 LOC, 21 files), Rust (11272 LOC, 18 files), HTML (6089 LOC, 8 files), Python (1306 LOC, 9 files), JavaScript (1286 LOC, 1 files), Markdown (856 LOC, 5 files), CSS (611 LOC, 1 files), TOML (6 LOC, 1 files)
- **Totals:** 64 files, 40014 LOC [S:scan]
- **Git:** 38 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:chessball/claude]
- Claude models seen: —
- Codex sessions: 3 [T:chessball/codex]
- Codex models seen: gpt-5.4

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 3 | 88 | 92126109 | 711364 | 81020416 | — | $132.40 |
| **Total** |  |  |  |  |  |  | **$132.40** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| Endgame tables | 16 | `README.md` |
| Board: bitboard | 8 | `rust_chessball/src/weak_solve.rs` |
| Minimax/Negamax | 5 | `rust_chessball/src/solver.rs` |
| Mobility | 4 | `rust_chessball/src/solver.rs` |
| Check/Checkmate | 2 | `rust_chessball/src/minimax.rs` |
| Alpha-beta | 2 | `rust_chessball/src/lib.rs` |
| Material counting | 2 | `CHESSBALL_RULES_SPEC.md` |
| Transposition table | 1 | `CHESSBALL_SOLVER_STATUS.md` |
| Evaluation/PST | 1 | `python_chessball/chessball_win_positions.py` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | exec_command | 856 |
| Codex | write_stdin | 170 |
| Codex | update_plan | 16 |

## Interaction profile

- Total user prompts (both agents): **88**
- Avg prompt length: 367.4 chars
- Intent distribution:
  - Other: 42
  - Scenario: 24
  - Question: 11
  - FeatureRequest: 10
  - Constraint: 9
  - ToolingBuild: 6
  - BugFixRequest: 3
  - Documentation: 2
  - RefactorRequest: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-03-05 23:46 — session `rollout-`_

```
Please analyze the repo and the rules of ChessBall as documented and implemented. Make a more formal specification of the rules of ChessBall. Don't search on the Internet, really stick to the content of the repo to infer rules

```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-03-05 23:55 | Codex | FeatureRequest,Scenario | No. I suggest you implement your own implementation in Rust. I'd like to develop very strong AI or to envision to (weakly) solve the game. |
| 3 | 2026-03-05 23:56 | Codex | FeatureRequest,Scenario | Considering CHESSBALL_RULES_SPEC.md, can you write a Web app in HTML/CSS/JS that would allow to play games against himself or a random engi… |
| 4 | 2026-03-06 00:06 | Codex | Question,Scenario | can you envision to organize a tournament between the same solver, export games in a suited format (in such a way we can replay), and compu… |
| 5 | 2026-03-06 00:07 | Codex | Question | how to run the app? |
| 6 | 2026-03-06 00:22 | Codex | Question,Scenario | how to run the tournament? |
| 7 | 2026-03-06 00:34 | Codex | Other | there is a cbr format in the repo that has been created... can you handle it and allow to replay games? |
| 8 | 2026-03-06 00:47 | Codex | Other | can we now think about a weak solving procedure? |
| 9 | 2026-03-06 00:53 | Codex | RefactorRequest,Scenario | Use: White wins if the ball reaches White’s goal row. => Yes Black wins if the ball reaches Black’s goal row. => Yes Infinite play is a dra… |
| 10 | 2026-03-06 00:58 | Codex | Other | yes go |
| 11 | 2026-03-06 01:06 | Codex | Other | let's go for symmetry reduction (horizontal symmetry canonicalization plus a more compact graph store) |
| 12 | 2026-03-06 06:23 | Codex | Other | go for next scaling steps |
| 13 | 2026-03-06 07:03 | Codex | Other | go this way |
| 14 | 2026-03-06 07:16 | Codex | Other | let's try |
| 15 | 2026-03-06 08:07 | Codex | BugFixRequest | ok let's fix the bottlenecks and a next round of improvements before trying on a large |
| 16 | 2026-03-06 08:11 | Codex | Question | what's your recommendation to run a 3-hour run? |
| 17 | 2026-03-06 08:25 | Codex | Other | is it possible to print some intermediate checkpoint, with no overhead? |
| 18 | 2026-03-06 08:26 | Codex | Other | yes please |
| 19 | 2026-03-06 08:39 | Codex | BugFixRequest | mathieuacher@Mathieus-MacBook-Pro rust_chessball % cd /Users/mathieuacher/SANDBOX/chessball/rust_chessball target/release/solve_start \ --m… |
| 20 | 2026-03-06 13:27 | Codex | Other | summary phase=pred_fill processed=14698984 phase_elapsed_s=107.3 total_elapsed_s=418.0 states=100000000 expanded_states=14698984 edges=3839… |
| 21 | 2026-03-06 13:35 | Codex | Other | I have 128GB |
| 22 | 2026-03-06 14:49 | Codex | Other | checkpoint phase=pred_fill processed=19050496 phase_elapsed_s=143.4 total_elapsed_s=4238.0 states=1000000000 expanded_states=189552252 edge… |
| 23 | 2026-03-06 16:53 | Codex | Other | --checkpoint-seconds 30 \ 2> solve_progress_1b.log exact=false elapsed_ms=5510395 states=1000000000, expanded_states=189552252, edges=50130… |
| 24 | 2026-03-06 18:27 | Codex | Constraint,Scenario | before resumable graph checkpoints I am wondering what optimizations we can envision... right now, is there a kind of caching mechanism to … |
| 25 | 2026-03-06 18:32 | Codex | Other | yes try |
| 26 | 2026-03-07 00:35 | Codex | FeatureRequest,ToolingBuild | mathieuacher@Mathieus-MacBook-Pro rust_chessball % cd /Users/mathieuacher/SANDBOX/chessball/rust_chessball cargo build --release --bin solv… |
| 27 | 2026-03-07 00:38 | Codex | Other | I have launched the script... as part of it, I guess there are part of the tree that have been solved ie given a sequence of moves, we know… |
| 28 | 2026-03-07 00:41 | Codex | FeatureRequest | I think it's a good direction to develop such a trustworthy partial tablebase... and ideally visualizing it! I also think it should be a de… |
| 29 | 2026-03-07 00:51 | Codex | Scenario | I'd like to identify position (sequence of moves) that lead necessary to a solved verdict (being draw/win/lose) |
| 30 | 2026-03-07 00:58 | Codex | Scenario | wrt visualization, I "simply" want the ability to play positions leading to a solved verdict... a kind of browser of the partial_tablebase |
| 31 | 2026-03-07 01:07 | Codex | Other | State #4370 BlackWin Depth 4 · 4 plies c2-c3 e5-e4 c3-d4@e5 e4-e5@e6 I'm not sure to follow: why BlackWin? the ball is on their side, and "… |
| 32 | 2026-03-07 01:11 | Codex | ToolingBuild,Constraint | here are the new rules definition: Below is a **formal, implementation‑ready specification** of the rules visible on the box back **plus** … |
| 33 | 2026-03-07 01:16 | Codex | FeatureRequest | yes please do so... in addition can you add a new Markdown file specifying the new, official rules (you can keep the old one)? |
| 34 | 2026-03-07 01:29 | Codex | Question,Scenario | how to run a "solver" to try solving the game? |
| 35 | 2026-03-07 01:40 | Codex | Constraint,Scenario | partial_tablebase is nice, but it tends to show "only" positions with 1 move forcing the result (ie closed to 1 move for finishing the game… |
| 36 | 2026-03-07 01:48 | Codex | Scenario | can I launch a long night experiment for solving the game? and then I can visualize some interesting positions that have been solved... or … |
| 37 | 2026-03-07 08:17 | Codex | Other | es=4772093849 resident_bytes=45088375404 disk_edge_bytes=38176750792 state_table_peak_bytes=42949672960 aux_bytes=4000000000 checkpoint pha… |
| 38 | 2026-03-07 08:24 | Codex | Question | why 56? |
| 39 | 2026-03-07 13:29 | Codex | Other | checkpoint phase=pred_fill processed=170000000 phase_elapsed_s=1260.0 total_elapsed_s=5135.4 states=1000000000 expanded_states=174634174 ed… |
| 40 | 2026-03-07 16:50 | Codex | Other | mathieuacher@Mathieus-MacBook-Pro rust_chessball % cat overnight_solve.out exact=false elapsed_ms=5193020 states=1000000000, expanded_state… |
| 41 | 2026-03-07 16:54 | Codex | FeatureRequest | please implement |
| 42 | 2026-03-07 22:09 | Codex | Other | tail -f overnight_solve.out state 16 outcome=BlackWin -- WD NB WD -- WD -- -- -- BA BA -- -- -- -- -- -- WA -- -- -- -- -- -- -- -- -- -- -… |
| 43 | 2026-03-07 22:18 | Codex | FeatureRequest,ToolingBuild | mathieuacher@Mathieus-MacBook-Pro rust_chessball % cd /Users/mathieuacher/SANDBOX/chessball/rust_chessball cargo build --release --bin solv… |
| 44 | 2026-03-08 09:14 | Codex | Scenario | checkpoint phase=retrograde processed=10000000 solved_states=10755881 phase_elapsed_s=2.4 total_elapsed_s=8312.2 states=1000000000 expanded… |
| 45 | 2026-03-08 11:41 | Codex | Scenario | exact=false elapsed_ms=7665861 states=1000000000, expanded_states=167381068, closed_states=171101864, certified_states=61956510, edges=4564… |
| 46 | 2026-03-08 11:48 | Codex | Scenario | before implementing, I need to understand what's missing... I can live with a weak solving, when under perfect play, we've got a verdict (e… |
| 47 | 2026-03-08 11:55 | Codex | Scenario | let's consider state 7 outcome=Draw -- WD -- WD BA WD -- -- -- WA -- WA -- -- -- -- -- NB -- -- -- -- -- -- -- -- -- -- -- -- BA -- -- -- -… |
| 48 | 2026-03-08 11:57 | Codex | Other | so even for state 7 and 8, there are unresolved frontier states? |
| 49 | 2026-03-08 12:01 | Codex | Other | to reduce a bit the complexity and get some proof, what about starting from "move e6-e4^e5" and try to cover unresolved frontier children? … |
| 50 | 2026-03-08 12:03 | Codex | Scenario | I would like to have cases like "given this position, it's necessary [verdict] and we have a proof of it" |
| 51 | 2026-03-08 17:16 | Codex | Other | is there an overhead with this proposal? |
| 52 | 2026-03-08 17:16 | Codex | Other | yes go ahead |
| 53 | 2026-03-08 19:51 | Codex | Question | how to run a night experiment? (I'm fearing a bit about size of generated artefacts like summary.txt or proof_positions.txt) |
| 54 | 2026-03-08 19:56 | Codex | Other | mathieuacher@Mathieus-MacBook-Pro rust_chessball % cat overnight_partial_tb.out exact=false states=250000, closed_states=20135, open_states… |
| 55 | 2026-03-08 19:59 | Codex | Other | mathieuacher@Mathieus-MacBook-Pro rust_chessball % cat overnight_partial_tb_1m.out exact=false states=1000000, closed_states=99716, open_st… |
| 56 | 2026-03-08 20:02 | Codex | Other | yes let's go this way |
| 57 | 2026-03-08 20:06 | Codex | Other | I want to run a very large, night-long experiment |
| 58 | 2026-03-10 09:17 | Codex | Other | state=71299 depth=5 proof_plies=2 outcome=WhiteWin sequence=c5-c6 e2-e1 e5-d4@c3 b1-c1 d4-c3@b2 c2-c4^c3 c3-b2@a1 state=77519 depth=5 proof… |
| 59 | 2026-03-10 09:57 | Codex | Constraint,Scenario | browser.html can be huge in size, as well as dot total 6744 drwxr-xr-x@ 30 mathieuacher staff 960B Mar 10 10:20 .. drwxr-xr-x@ 9 mathieuach… |
| 60 | 2026-03-10 12:50 | Codex | Constraint | checkpoint phase=retrograde processed=5000000 solved_states=5871759 phase_elapsed_s=0.4 total_elapsed_s=3424.4 states=1000000000 expanded_s… |
| … | | | | _+28 more prompts_ |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `a4e3659` | 2026-04-02T14:54:16+02:00 | Mathieu Acher | Document solver status and add run tooling |
| `634e4f4` | 2026-03-11T18:19:06+01:00 | Mathieu Acher | Add arena engines and sample arena games |
| `d20de0a` | 2026-02-04T15:08:04+01:00 | skunne | Use Add trait to replace method is_on_board with option return type |
| `6318837` | 2026-02-04T14:35:50+01:00 | skunne | Add trait Copy to Coord and add struct CoordDelta: remove hundreds of .clone() and more cleanly handle addition of coor… |
| `52200be` | 2026-01-24T16:43:42+01:00 | skunne | Rules of ChessBall |
| `07b8643` | 2026-01-24T16:42:57+01:00 | skunne | Add Coord struct to replace (usize, usize) throughout; Better structure for MoveInfo; Fix bug with generating PushBall … |
| `95c7c3f` | 2026-01-22T19:11:50+01:00 | skunne | First draft of report |
| `0f0d941` | 2026-01-22T19:08:52+01:00 | skunne | Attempt to fix bug in gen_ball_push_move_for |
| `2fe8e46` | 2026-01-22T18:59:08+01:00 | skunne | Refactor possible_moves into subfuctions possible_simple_move_for, possible_push_move_for, etc |
| `36b0791` | 2026-01-22T18:38:37+01:00 | skunne | cargo clippy |
| `e85efb1` | 2026-01-22T18:14:51+01:00 | skunne | tests possible moves push move |
| `3940511` | 2026-01-22T18:10:34+01:00 | skunne | First draft of report on solving ChessBall |
| `71bcfeb` | 2025-12-12T14:06:43+01:00 | skunne | Add command to make AI play for several turns. |
| `0029dfb` | 2025-11-28T11:07:52+01:00 | skunne | Improved CLI; fix small bug with disappearing Defender during tackle move |
| `f240358` | 2025-11-28T10:48:23+01:00 | skunne | Add doc and tests |
| `0c11546` | 2025-11-28T10:16:00+01:00 | skunne | better tests and place_ball |
| `16f1750` | 2025-11-27T18:14:50+01:00 | skunne | Translation from python into rust by copilot |
| `dc21cb6` | 2025-11-07T11:05:09+01:00 | skunne | Add minimax with optional alphabeta pruning, using heuristics |
| `bd0fadd` | 2025-11-07T10:49:07+01:00 | skunne | Add heuristics evaluation functions |
| `765ab2b` | 2025-11-07T09:58:43+01:00 | skunne | add unit tests for ChessBallBoard.from_str and ChessBallBoard.__repr__ |
| `318557e` | 2025-11-07T09:55:12+01:00 | skunne | add ChessBallBoard.from_str method to construct ChessBallBoard object |
| `d879b74` | 2025-11-05T17:25:22+01:00 | skunne | better printing of tests for moves with print_two_boards |
| `9b3e21d` | 2025-11-05T17:17:31+01:00 | skunne | add tests for possible_previous_moves |
| `731f443` | 2025-11-05T17:16:21+01:00 | skunne | add tests for possible_moves |
| `706d065` | 2025-11-05T17:12:59+01:00 | skunne | add Defender tackle moves |
| `df47fd0` | 2025-11-05T17:07:56+01:00 | skunne | add Attacker jump moves |
| `2c1208c` | 2025-11-05T17:06:21+01:00 | skunne | add main function to chessball_win_positions to count unblockable win positions |
| `5d0b418` | 2025-11-05T16:58:09+01:00 | skunne | blocking moves |
| `8b7e5b3` | 2025-11-05T16:51:33+01:00 | skunne | generate unavoidable win positions |
| `c260929` | 2025-11-05T16:49:53+01:00 | skunne | more efficient checking that winning position is really reachable by ball push |
| `3373ba7` | 2025-11-05T16:48:07+01:00 | skunne | is_win_avoidable_by_opponent: checks whether the opponent could always have blocked this win, or if some previous posit… |
| `4f2e016` | 2025-11-05T16:46:04+01:00 | skunne | winning moves |
| `956dfa2` | 2025-11-05T16:44:17+01:00 | skunne | is position reachable by ball push |
| `368c76f` | 2025-11-05T16:43:10+01:00 | skunne | use lazy generators instead of lists |
| `715405f` | 2025-11-05T16:41:52+01:00 | skunne | generate_white_win_positions |
| `0ca239c` | 2025-11-05T16:39:47+01:00 | skunne | forbid moves that push the ball onto the sides |
| `10a830b` | 2025-11-05T16:38:08+01:00 | skunne | ChessBallBoard class |
| `0405c3d` | 2025-11-05T16:28:12+01:00 | skunne | Initial commit |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **34** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, Documentation, Constraint) [2026-03-05 23:46] — Please analyze the repo and the rules of ChessBall as documented and implemented. Make a more formal specification of the rules of ChessBall. Don't search on the Internet, really … [T:Codex/rollout-]
- **BL-002** (FeatureRequest, Scenario) [2026-03-05 23:55] — No. I suggest you implement your own implementation in Rust. I'd like to develop very strong AI or to envision to (weakly) solve the game. [T:Codex/rollout-]
- **BL-003** (FeatureRequest, Scenario) [2026-03-05 23:56] — Considering CHESSBALL_RULES_SPEC.md, can you write a Web app in HTML/CSS/JS that would allow to play games against himself or a random engine [T:Codex/rollout-]
- **BL-004** (Question, Scenario) [2026-03-06 00:06] — can you envision to organize a tournament between the same solver, export games in a suited format (in such a way we can replay), and compute some stats on win/draw/lose [T:Codex/rollout-]
- **BL-005** (RefactorRequest, Scenario) [2026-03-06 00:53] — Use: White wins if the ball reaches White’s goal row. => Yes Black wins if the ball reaches Black’s goal row. => Yes Infinite play is a draw. => to simplify a bit 3 fold repetitio… [T:Codex/rollout-]
- **BL-006** (BugFixRequest) [2026-03-06 08:07] — ok let's fix the bottlenecks and a next round of improvements before trying on a large [T:Codex/rollout-]
- **BL-007** (BugFixRequest) [2026-03-06 08:39] — mathieuacher@Mathieus-MacBook-Pro rust_chessball % cd /Users/mathieuacher/SANDBOX/chessball/rust_chessball target/release/solve_start \ --max-states 100000000 \ --disk-edges \ --c… [T:Codex/rollout-]
- **BL-008** (Constraint, Scenario) [2026-03-06 18:27] — before resumable graph checkpoints I am wondering what optimizations we can envision... right now, is there a kind of caching mechanism to avoid analyzing the same position twice? [T:Codex/rollout-]
- **BL-009** (FeatureRequest) [2026-03-07 00:41] — I think it's a good direction to develop such a trustworthy partial tablebase... and ideally visualizing it! I also think it should be a dedicated script, since this strategy of m… [T:Codex/rollout-]
- **BL-010** (Scenario) [2026-03-07 00:51] — I'd like to identify position (sequence of moves) that lead necessary to a solved verdict (being draw/win/lose) [T:Codex/rollout-]
- **BL-011** (Scenario) [2026-03-07 00:58] — wrt visualization, I "simply" want the ability to play positions leading to a solved verdict... a kind of browser of the partial_tablebase [T:Codex/rollout-]
- **BL-012** (ToolingBuild, Constraint, Scenario) [2026-03-07 01:11] — here are the new rules definition: Below is a **formal, implementation‑ready specification** of the rules visible on the box back **plus** a few clarifications confirmed by an ext… [T:Codex/rollout-]
- **BL-013** (FeatureRequest) [2026-03-07 01:16] — yes please do so... in addition can you add a new Markdown file specifying the new, official rules (you can keep the old one)? [T:Codex/rollout-]
- **BL-014** (Constraint, Scenario) [2026-03-07 01:40] — partial_tablebase is nice, but it tends to show "only" positions with 1 move forcing the result (ie closed to 1 move for finishing the game)... I would love to have position leadi… [T:Codex/rollout-]
- **BL-015** (Scenario) [2026-03-07 01:48] — can I launch a long night experiment for solving the game? and then I can visualize some interesting positions that have been solved... or have a proof that the game is solved [T:Codex/rollout-]
- **BL-016** (Scenario) [2026-03-08 09:14] — checkpoint phase=retrograde processed=10000000 solved_states=10755881 phase_elapsed_s=2.4 total_elapsed_s=8312.2 states=1000000000 expanded_states=175379271 edges=4783566131 resid… [T:Codex/rollout-]
- **BL-017** (Scenario) [2026-03-08 11:41] — exact=false elapsed_ms=7665861 states=1000000000, expanded_states=167381068, closed_states=171101864, certified_states=61956510, edges=4564805599, max_successors_per_state=39, ter… [T:Codex/rollout-]
- **BL-018** (Scenario) [2026-03-08 11:48] — before implementing, I need to understand what's missing... I can live with a weak solving, when under perfect play, we've got a verdict (eg draw). [T:Codex/rollout-]
- **BL-019** (Scenario) [2026-03-08 11:55] — let's consider state 7 outcome=Draw -- WD -- WD BA WD -- -- -- WA -- WA -- -- -- -- -- NB -- -- -- -- -- -- -- -- -- -- -- -- BA -- -- -- -- -- BD -- BD -- BD -- move e6-e4^e5 sta… [T:Codex/rollout-]
- **BL-020** (Scenario) [2026-03-08 12:03] — I would like to have cases like "given this position, it's necessary [verdict] and we have a proof of it" [T:Codex/rollout-]
- **BL-021** (Question) [2026-03-08 19:51] — how to run a night experiment? (I'm fearing a bit about size of generated artefacts like summary.txt or proof_positions.txt) [T:Codex/rollout-]
- **BL-022** (Constraint, Scenario) [2026-03-10 09:57] — browser.html can be huge in size, as well as dot total 6744 drwxr-xr-x@ 30 mathieuacher staff 960B Mar 10 10:20 .. drwxr-xr-x@ 9 mathieuacher staff 288B Mar 10 10:20 . -rw-r--r--@… [T:Codex/rollout-]
- **BL-023** (Constraint) [2026-03-10 12:50] — checkpoint phase=retrograde processed=5000000 solved_states=5871759 phase_elapsed_s=0.4 total_elapsed_s=3424.4 states=1000000000 expanded_states=167381068 edges=4564805599 residen… [T:Codex/rollout-]
- **BL-024** (Constraint) [2026-03-10 16:54] — the process was still running, you were right mathieuacher@Mathieus-MacBook-Pro rust_chessball % cat overnight_solve_12b.out exact=false elapsed_ms=6233556 states=1200000000, expa… [T:Codex/rollout-]
- **BL-025** (FeatureRequest) [2026-03-11 10:54] — please implement... I have also doubts about repetitions or positions that have already been visited [T:Codex/rollout-]
- **BL-026** (Scenario) [2026-03-11 11:42] — ok nice! could you give an estimation of the number of possible positions? the branching factor? any metric that can help to understand the complexity of the game [T:Codex/rollout-]
- **BL-027** (FeatureRequest, Scenario) [2026-03-11 11:50] — Look at CHESSBALL_RULES_OFFICIAL_SPEC. Implement two engines: * one following AlphaZero principle (self-play) * another more "classical" [T:Codex/rollout-]
- **BL-028** (Constraint) [2026-03-11 16:20] — summary phase=retrograde processed=10904478 solved_states=10904478 phase_elapsed_s=1.2 total_elapsed_s=5238.0 states=1400000000 expanded_states=247047221 edges=6756136572 resident… [T:Codex/rollout-]
- **BL-029** (BugFixRequest, ToolingBuild) [2026-03-11 16:21] — cd /Users/mathieuacher/SANDBOX/chessball/rust_chessball cargo run --bin arena -- --white classical --black alphazero Finished `dev` profile [unoptimized + debuginfo] target(s) in … [T:Codex/rollout-]
- **BL-030** (ToolingBuild) [2026-03-11 16:28] — mathieuacher@Mathieus-MacBook-Pro rust_chessball % cargo run --bin arena -- --white classical --black alphazero Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s… [T:Codex/rollout-]
- **BL-031** (ToolingBuild) [2026-03-11 17:09] — cargo run --bin arena -- --white classical --black alphazero is it possible to save the games in a specific format that is compatible with the Web app already developed? [T:Codex/rollout-]
- **BL-032** (Scenario) [2026-03-11 19:48] — the problem I am seeing with an AlphaZero (AZ) like approach is that most of self-play will lead to draw... there are certainly "rare" patterns that would deserve to be "learned",… [T:Codex/rollout-]
- **BL-033** (Scenario) [2026-03-11 19:56] — a critical-position curriculum plus decisive-position replay would be awesome, and kind of complementary to the solving initiative [T:Codex/rollout-]
- **BL-034** (Constraint) [2026-04-02 12:56] — I don't have the rights for https://github.com/skunne/chessball/ so I may need to do a pull request [T:Codex/rollout-]

## Evidence pointers

- [R:chessball] — repo at `/Users/mathieuacher/SANDBOX/chessball`
- [T:chessball/claude] — Claude sessions at `~/.claude/projects/chessball...`
- [T:chessball/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chessball

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.