# minichess-5x5-repro

_Evidence-based dossier. Generated 2026-04-22 14:56 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/minichess-5x5-repro` [R:minichess-5x5-repro]
- **Primary language:** Rust
- **Coding agent(s):** Codex
- **Period:** 2026-02-25 07:33 → 2026-03-08 19:59
- **LOC by language:** Rust (11953 LOC, 8 files), Python (4920 LOC, 11 files), JavaScript (1716 LOC, 1 files), Shell (1569 LOC, 8 files), Markdown (1412 LOC, 19 files), Text (466 LOC, 7 files), CSS (439 LOC, 1 files), HTML (77 LOC, 1 files)
- **Totals:** 57 files, 22558 LOC [S:scan]
- **Git:** 1 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:minichess-5x5-repro/claude]
- Claude models seen: —
- Codex sessions: 5 [T:minichess-5x5-repro/codex]
- Codex models seen: gpt-5.3-codex, gpt-5.4

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 5 | 120 | 215514187 | 1104450 | 202948096 | — | $305.81 |
| **Total** |  |  |  |  |  |  | **$305.81** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| UCI protocol | 131 | `README.md` |
| FEN parsing | 56 | `README.md` |
| PGN | 29 | `README.md` |
| Check/Checkmate | 15 | `README.md` |
| Promotion | 8 | `README.md` |
| Board: bitboard | 7 | `scripts/az_formats.py` |
| Material counting | 5 | `artifacts/reference/prost2013_repro_seed_lines.txt` |
| NNUE/neural eval | 5 | `docs/reports/2026-03-07_fairy_stockfish_comparison_report.md` |
| Board: mailbox 8x8 | 4 | `scripts/extract_gardneranalysis_tree_positions.py` |
| Perft | 3 | `README.md` |
| Transposition table | 3 | `README.md` |
| Principal-variation (PV) | 3 | `README.md` |
| Pawn structure | 3 | `artifacts/runs/c4_bxc4_go_depth32_20260306.log` |
| Mobility | 3 | `artifacts/runs/c4_bxc4_go_depth32_20260306.log` |
| Minimax/Negamax | 2 | `README.md` |
| Futility pruning | 2 | `README.md` |
| Castling | 1 | `README.md` |
| Alpha-beta | 1 | `README.md` |
| Iterative deepening | 1 | `README.md` |
| Killer moves | 1 | `src/search.rs` |
| History heuristic | 1 | `src/search.rs` |
| Late-move reduction (LMR) | 1 | `README.md` |
| Aspiration windows | 1 | `README.md` |
| Opening book | 1 | `tools/pgn_viewer/app.js` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | exec_command | 1484 |
| Codex | write_stdin | 603 |
| Codex | update_plan | 20 |

## Interaction profile

- Total user prompts (both agents): **120**
- Avg prompt length: 608.0 chars
- Intent distribution:
  - Other: 67
  - Scenario: 18
  - Question: 16
  - FeatureRequest: 13
  - Constraint: 11
  - TestRequest: 4
  - ToolingBuild: 4
  - Documentation: 2
  - BugFixRequest: 2

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-02-25 07:33 — session `rollout-`_

```
Along with Mehdi Mhalla, Frédéric Prost weakly solved Gardner's 5x5 Minichess as published in 2013. They modified Stockfish in order to make it play Gardner Chess. 
Abstract: A 5×5 board is the smallest board on which one can set up all types of chess pieces as a start position. We consider Gardner’s minichess variant in which all pieces are set as in a standard chessboard (from Rook to King). This game has roughly 9×10^18 legal positions and is comparable in this respect with checkers. We weakly solve this game: we prove its game-theoretic value and give a strategy to draw against best play for White and Black sides. Our approach requires surprisingly little computing power. We give a human readable proof. The way the result is obtained is generic and could be generalized to bigger chess settings or to other games. 

Please replicate this weak solving, from scratch, using Rust.

```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-25 07:51 | Codex | Question | what's missing for a full publication-grade weak proof closure of Gardner? |
| 3 | 2026-02-25 07:52 | Codex | Other | yes go to next setps |
| 4 | 2026-02-25 08:06 | Codex | FeatureRequest | please add iterative closure runs (resume/merge certificates) to progressively reduce unknown frontier. |
| 5 | 2026-02-25 08:23 | Codex | FeatureRequest | yes please create an automated loop script... it would also be nice to be able to stop it, and resume afterwards |
| 6 | 2026-02-25 08:35 | Codex | Other | nice! would it be possible, out of current traces and proofs, to (1) have a way to visualize the different lines/games in a PGN kind format… |
| 7 | 2026-02-25 10:19 | Codex | Other | run with "1. b4 d4 2. bxc5" with the hope of solving this line... |
| 8 | 2026-02-25 13:02 | Codex | Other | let's try 1. b4 d4 2. bxc5 Bxc5 3. f4 |
| 9 | 2026-02-25 13:30 | Codex | Other | let's try with 1. b4 cxb4 2. cxb4 d4 3. e4 f4 4. Bxf4 exf4 5. Qd2 Ke5 6. Qxf4+ |
| 10 | 2026-02-25 13:43 | Codex | Other | can I "visualize" the current certificate using the facilities I've asked you before? |
| 11 | 2026-02-25 13:45 | Codex | FeatureRequest | PGN is kind of nice... But yeah I'm missing a real tool to read this very specific PGN format. Can you develop such a tool? ideally using H… |
| 12 | 2026-02-25 13:58 | Codex | Other | instead of P, R, N, P can you use real chess pieces? |
| 13 | 2026-02-25 14:03 | Codex | Scenario | for "1. b4 cxb4 2. cxb4 d4 3. e4 f4 4. Bxf4 exf4 5. Qd2 Ke5 6. Qxf4+" we might have to debug... can you depict the state board position? |
| 14 | 2026-02-25 14:09 | Codex | Question | can you try the solving over 1. b4 cxb4 2. cxb4 d4 3. e4 f4 4. Bxf4 exf4 5. Qd2 Ne5 6. Qxf4+ |
| 15 | 2026-02-25 15:06 | Codex | Other | is there the export in such a way I can visualize the proof? |
| 16 | 2026-02-25 15:11 | Codex | Documentation | for visualizing, in addition of the box list, I'd like to to be able to have a "tree" of possible possibles that have been explored (or une… |
| 17 | 2026-02-25 15:33 | Codex | Constraint,Scenario | nice! just to be sure, about the "proof", I don't get why it takes so much time for the position 1. b4 cxb4 2. cxb4 d4 3. e4 f4 4. Bxf4 exf… |
| 18 | 2026-02-25 16:02 | Codex | Other | I have impression we can leverage shallow depth first more often... |
| 19 | 2026-02-25 17:13 | Codex | Constraint | takes a while... I don't get why... if you find a "winning", you don't need to further explore, it's superior to draw |
| 20 | 2026-02-25 17:23 | Codex | Scenario | just to clarify again: when a sequence of moves and position is given, the goal is to prove the game-theoretical result at this specific ro… |
| 21 | 2026-02-25 17:27 | Codex | Question | which command should I use to try again? |
| 22 | 2026-02-25 17:28 | Codex | Question | how to generate the PGN stuff out of the proof? |
| 23 | 2026-02-25 17:33 | Codex | Other | I'd like to verify 1. c4 bxc4 |
| 24 | 2026-02-25 17:36 | Codex | Other | according to the original paper: "4.2 White moves c4 1 c4 bXc4 The pin on the b file leads to forced mate ♯27♯◦." |
| 25 | 2026-02-25 17:39 | Codex | FeatureRequest,Scenario | Along with Mehdi Mhalla, Frédéric Prost weakly solved Gardner's 5x5 Minichess as published in 2013. They modified Stockfish in order to mak… |
| 26 | 2026-02-25 17:42 | Codex | Other | root-outcome seems reasonable |
| 27 | 2026-02-25 18:12 | Codex | Other | out of the proof, PGN? |
| 28 | 2026-02-25 18:13 | Codex | Other | generate a report... especially: did you conclude similarly? did you fully reproduce or can we envision full reproduction? |
| 29 | 2026-02-25 18:14 | Codex | Scenario | for the position 1. c4 bxc4 can you run on your side and analyze the outcome/conclusion? is it coherent with the paper? |
| 30 | 2026-02-25 18:21 | Codex | Other | "Section 4.2 White moves c4 1 c4 bXc4 The pin on the b file leads to forced mate ♯27♯◦." can you check this claim? |
| 31 | 2026-02-25 20:48 | Codex | Other | continue |
| 32 | 2026-02-25 20:48 | Codex | Other | is it possible to try at depth=30 says? |
| 33 | 2026-02-25 20:55 | Codex | Other | depth=40 then |
| 34 | 2026-02-25 21:02 | Codex | FeatureRequest | can we envision a new plan: implement chess engine-related features to significantly speed up... |
| 35 | 2026-02-25 21:03 | Codex | Other | sounds a good plan, let's go for Phase 1+2 |
| 36 | 2026-02-26 04:07 | Codex | Other | yes Phase 3 |
| 37 | 2026-02-26 04:14 | Codex | Other | Phase 4 gooo |
| 38 | 2026-02-26 04:49 | Codex | Other | Phase 5 |
| 39 | 2026-02-26 05:14 | Codex | Other | yes go |
| 40 | 2026-02-26 15:32 | Codex | Other | let's try at depth=40 |
| 41 | 2026-02-26 16:10 | Codex | Other | nice! we seem closed... |
| 42 | 2026-02-26 21:30 | Codex | Other | try depth=45 |
| 43 | 2026-03-05 19:46 | Codex | Other | depth 50? |
| 44 | 2026-03-05 19:56 | Codex | Other | yes please go this way |
| 45 | 2026-03-05 20:44 | Codex | Other | status? |
| 46 | 2026-03-05 22:09 | Codex | Question | where are we? |
| 47 | 2026-03-05 22:10 | Codex | Question | how many pieces remaining? |
| 48 | 2026-03-05 22:11 | Codex | Other | We can stop... |
| 49 | 2026-03-05 22:19 | Codex | Other | let's try to reproduce as much as possible other claims of the paper |
| 50 | 2026-03-05 22:24 | Codex | Constraint | "I’ll expand the reproduction suite claim-by-claim from the paper using the existing tooling, then run it and produce a structured report o… |
| 51 | 2026-03-05 22:39 | Codex | Other | yep |
| 52 | 2026-03-05 22:56 | Codex | Question,Scenario | what about using a threshold (cp score of Stockfish) to consider a given position winning/losing? is there a specific value specified in th… |
| 53 | 2026-03-05 22:58 | Codex | Constraint | I don't get how forced mate annotations (♯x♯•, ♯x♯◦) and obvious non-win markers (+−, −+) have been obtained |
| 54 | 2026-03-05 23:01 | Codex | FeatureRequest,Scenario | Along with Mehdi Mhalla, Frédéric Prost weakly solved Gardner's 5x5 Minichess as published in 2013. They modified Stockfish in order to mak… |
| 55 | 2026-03-05 23:02 | Codex | Question | how to visualize the (partial) proof? |
| 56 | 2026-03-05 23:09 | Codex | Other | yes, please train an AlphaZero player... my hope (1) can beat the specialized Stockfish (2) offer "strong oracle" judgment we can rely on a… |
| 57 | 2026-03-05 23:14 | Codex | TestRequest,Question | can you analyze https://lig-membres.imag.fr/prost/MiniChessResolution/pgn_files/Gardneranalysis.pgn and extract some test-cases (aka positi… |
| 58 | 2026-03-05 23:29 | Codex | Scenario | wire az-eval to play directly against the historical stockfish5x5 binary from the reproduction workflow; is an interesting step to assess a… |
| 59 | 2026-03-05 23:32 | Codex | TestRequest,Scenario | this plan: Continue training from hard.bin with a longer release run. Improve az-eval so it tests diverse seeded positions instead of repla… |
| 60 | 2026-03-05 23:42 | Codex | FeatureRequest,Constraint | Longer release training from long.bin with a larger network. Add multiprocessing/self-play parallelism. Don't distill |
| … | | | | _+60 more prompts_ |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `322669d` | 2026-03-07T21:33:37+01:00 | Mathieu Acher | Add Fairy-Stockfish comparison harness and findings |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **36** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, Scenario) [2026-02-25 07:33] — Along with Mehdi Mhalla, Frédéric Prost weakly solved Gardner's 5x5 Minichess as published in 2013. They modified Stockfish in order to make it play Gardner Chess. Abstract: A 5×5… [T:Codex/rollout-]
- **BL-002** (FeatureRequest) [2026-02-25 08:06] — please add iterative closure runs (resume/merge certificates) to progressively reduce unknown frontier. [T:Codex/rollout-]
- **BL-003** (FeatureRequest) [2026-02-25 08:23] — yes please create an automated loop script... it would also be nice to be able to stop it, and resume afterwards [T:Codex/rollout-]
- **BL-004** (FeatureRequest) [2026-02-25 13:45] — PGN is kind of nice... But yeah I'm missing a real tool to read this very specific PGN format. Can you develop such a tool? ideally using HTML/CSS/SVG... [T:Codex/rollout-]
- **BL-005** (Scenario) [2026-02-25 14:03] — for "1. b4 cxb4 2. cxb4 d4 3. e4 f4 4. Bxf4 exf4 5. Qd2 Ke5 6. Qxf4+" we might have to debug... can you depict the state board position? [T:Codex/rollout-]
- **BL-006** (Documentation) [2026-02-25 15:11] — for visualizing, in addition of the box list, I'd like to to be able to have a "tree" of possible possibles that have been explored (or unexplored), and then I can click and have … [T:Codex/rollout-]
- **BL-007** (Constraint, Scenario) [2026-02-25 15:33] — nice! just to be sure, about the "proof", I don't get why it takes so much time for the position 1. b4 cxb4 2. cxb4 d4 3. e4 f4 4. Bxf4 exf4 5. Qd2 Ke5 6. Qxf4+, since it was mate… [T:Codex/rollout-]
- **BL-008** (Constraint) [2026-02-25 17:13] — takes a while... I don't get why... if you find a "winning", you don't need to further explore, it's superior to draw [T:Codex/rollout-]
- **BL-009** (Scenario) [2026-02-25 17:23] — just to clarify again: when a sequence of moves and position is given, the goal is to prove the game-theoretical result at this specific root node (last move) not to solve backwar… [T:Codex/rollout-]
- **BL-010** (Scenario) [2026-02-25 18:14] — for the position 1. c4 bxc4 can you run on your side and analyze the outcome/conclusion? is it coherent with the paper? [T:Codex/rollout-]
- **BL-011** (FeatureRequest) [2026-02-25 21:02] — can we envision a new plan: implement chess engine-related features to significantly speed up... [T:Codex/rollout-]
- **BL-012** (Constraint) [2026-03-05 22:24] — "I’ll expand the reproduction suite claim-by-claim from the paper using the existing tooling, then run it and produce a structured report of what we can confirm, what is only dire… [T:Codex/rollout-]
- **BL-013** (Question, Scenario) [2026-03-05 22:56] — what about using a threshold (cp score of Stockfish) to consider a given position winning/losing? is there a specific value specified in the paper? [T:Codex/rollout-]
- **BL-014** (Constraint) [2026-03-05 22:58] — I don't get how forced mate annotations (♯x♯•, ♯x♯◦) and obvious non-win markers (+−, −+) have been obtained [T:Codex/rollout-]
- **BL-015** (TestRequest, Question) [2026-03-05 23:14] — can you analyze https://lig-membres.imag.fr/prost/MiniChessResolution/pgn_files/Gardneranalysis.pgn and extract some test-cases (aka positions to analyze), especially those leadin… [T:Codex/rollout-]
- **BL-016** (Scenario) [2026-03-05 23:29] — wire az-eval to play directly against the historical stockfish5x5 binary from the reproduction workflow; is an interesting step to assess az-eval... but before I'd like to train h… [T:Codex/rollout-]
- **BL-017** (TestRequest, Scenario) [2026-03-05 23:32] — this plan: Continue training from hard.bin with a longer release run. Improve az-eval so it tests diverse seeded positions instead of replaying the same opening. Wire az-eval to t… [T:Codex/rollout-]
- **BL-018** (FeatureRequest, Constraint, Scenario) [2026-03-05 23:42] — Longer release training from long.bin with a larger network. Add multiprocessing/self-play parallelism. Don't distill [T:Codex/rollout-]
- **BL-019** (FeatureRequest) [2026-03-06 00:37] — diagnose why MPS is unavailable in this environment, add MLX as an Apple-native backend, [T:Codex/rollout-]
- **BL-020** (Scenario) [2026-03-06 08:11] — backend=mlx device=gpu hidden=64 shards=512 epochs=1 batch_size=2048 epoch 1 | examples 6046677 | policy 1.2245 | value 0.2893 | 45180.6 ex/s saved checkpoint to artifacts/alphaze… [T:Codex/rollout-]
- **BL-021** (Scenario) [2026-03-07 00:53] — I'd like to identify position (sequence of moves) that lead necessary to a solved verdict (being draw/win/lose)... and have ways to visualize this sequence of moves... [T:Codex/rollout-]
- **BL-022** (ToolingBuild, Constraint) [2026-03-07 00:55] — cargo run --release -- az-analyze --checkpoint artifacts/alphazero/latest.bin --simulations 256 --search-depth 8 --line-mini-text "1. b4 d4 2. bxc5" cargo run --release -- weak-so… [T:Codex/rollout-]
- **BL-023** (FeatureRequest) [2026-03-07 01:03] — yes please add a companion command [T:Codex/rollout-]
- **BL-024** (Scenario) [2026-03-07 01:09] — I'd like to visualize the position in a Web app [T:Codex/rollout-]
- **BL-025** (Constraint) [2026-03-07 01:14] — node=dxc3 Rb3 cxd2=Q Nd4 Qxe3 Qxe3 b4 Ke2 e4 Kd2 exd3 Kxd3 Bf4 | status=unknown | outcome=unknown | matching=1 | explored=1 | unexplored=22 BUT Qxe6 is winning (check mate) Hence … [T:Codex/rollout-]
- **BL-026** (BugFixRequest) [2026-03-07 01:19] — there is still the issue... [T:Codex/rollout-]
- **BL-027** (BugFixRequest, Constraint) [2026-03-07 01:28] — I have impression the issue is more profound... it's not only a "visualizaton" problem, but a (possible) discrepancy about the notion of weak solving. When there is a forced line … [T:Codex/rollout-]
- **BL-028** (Constraint) [2026-03-07 09:03] — yes, let's go this way. Don't touch AlphaZero, it's another side project [T:Codex/rollout-]
- **BL-029** (ToolingBuild) [2026-03-07 09:32] — wouldn't be interesting to git clone fairy-stockfish repo, compile, and run it [T:Codex/rollout-]
- **BL-030** (Question) [2026-03-07 18:35] — could you try running fairy-stockfish on some example positions (typically those that we want to reproduce from the original paper, see other Codex sessions), and compare to the h… [T:Codex/rollout-]
- **BL-031** (Documentation) [2026-03-07 20:27] — nice! please commit, including some docs/reports on key findings and attempts [T:Codex/rollout-]
- **BL-032** (Scenario) [2026-03-07 20:33] — can we organize a tournament of the two engines (fairy-SF vs historical-SF), starting from the starting position or from a given position? I think depth >= 20 is needed to have a … [T:Codex/rollout-]
- **BL-033** (Scenario) [2026-03-07 22:16] — I'm basically seeking some opening moves where Fairy >> historical... could be a good signal it's winning [T:Codex/rollout-]
- **BL-034** (Constraint) [2026-03-07 22:21] — I don't want to show the superiority of Fairy... I want to identify positions in which one side (certainly Fairy) wins (significantly)... it is then a good candidate for doing a p… [T:Codex/rollout-]
- **BL-035** (Constraint) [2026-03-08 09:42] — let's use fairy-stockfish at cost-effective depth... and now revisit some claims of the original paper (about checkmates, large advantage, etc.) the goal is to confirm or refute s… [T:Codex/rollout-]
- **BL-036** (FeatureRequest, ToolingBuild) [2026-03-08 13:30] — yes please build such an extractor [T:Codex/rollout-]

## Evidence pointers

- [R:minichess-5x5-repro] — repo at `/Users/mathieuacher/SANDBOX/minichess-5x5-repro`
- [T:minichess-5x5-repro/claude] — Claude sessions at `~/.claude/projects/minichess-5x5-repro...`
- [T:minichess-5x5-repro/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/minichess-5x5-repro

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.