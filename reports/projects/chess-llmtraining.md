# chess-llmtraining

_Evidence-based dossier. Generated 2026-04-22 14:53 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-llmtraining` [R:chess-llmtraining]
- **Primary language:** Python
- **Coding agent(s):** Codex
- **Period:** 2026-02-24 16:36 → 2026-03-05 23:16
- **LOC by language:** Python (7716 LOC, 35 files), JSON (2000 LOC, 86 files), Markdown (547 LOC, 6 files), Text (50 LOC, 35 files)
- **Totals:** 162 files, 10313 LOC [S:scan]
- **Git:** 285 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:chess-llmtraining/claude]
- Claude models seen: —
- Codex sessions: 2 [T:chess-llmtraining/codex]
- Codex models seen: gpt-5.3-codex

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 2 | 27 | 207947220 | 444054 | 200480000 | — | $289.43 |
| **Total** |  |  |  |  |  |  | **$289.43** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| FEN parsing | 82 | `chess_utils.py` |
| Transposition table | 40 | `linear_probes/tf_lens_fen_lichess_8layers_ckpt_no_optimizer_50k_5k_chess_fen_piece_probe_layer_5_pgn_vs_fen_50k5k_full_safe.pth` |
| PGN | 11 | `chess_utils.py` |
| Late-move pruning (LMP) | 8 | `linear_probes/tf_lens_fen_lichess_8layers_ckpt_no_optimizer_50k_5k_chess_fen_piece_probe_layer_5_pgn_vs_fen_50k5k_full_safe.pth` |
| Evaluation/PST | 8 | `board_state_interventions.py` |
| Late-move reduction (LMR) | 6 | `linear_probes/tf_lens_fen_lichess_8layers_ckpt_no_optimizer_50k_5k_chess_fen_piece_probe_layer_5_pgn_vs_fen_50k5k_full_safe.pth` |
| Castling | 5 | `chess_utils.py` |
| Principal-variation (PV) | 4 | `linear_probes/tf_lens_lichess_8layers_ckpt_no_optimizer_chess_piece_probe_layer_2_pgn_vs_fen_50k5k_full.pth` |
| Check/Checkmate | 3 | `third_party/nanoGPT/README.md` |
| Material counting | 2 | `chess_utils.py` |
| Opening book | 2 | `utils/unique_checks.ipynb` |
| En passant | 1 | `chess_utils.py` |
| Board: bitboard | 1 | `linear_probes/tf_lens_fen_lichess_8layers_ckpt_no_optimizer_50k_5k_chess_fen_piece_probe_layer_2_pgn_vs_fen_50k5k_full_safe.pth` |
| Board: mailbox 8x8 | 1 | `chess_utils.py` |
| Tapered evaluation | 1 | `third_party/nanoGPT/scaling_laws.ipynb` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | write_stdin | 980 |
| Codex | exec_command | 874 |

## Interaction profile

- Total user prompts (both agents): **27**
- Avg prompt length: 85.7 chars
- Intent distribution:
  - Other: 18
  - BugFixRequest: 4
  - Question: 3
  - ToolingBuild: 2

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-02-24 16:36 — session `rollout-`_

```
I'd like to reproduce this paper https://arxiv.org/abs/2403.15498 (source code here: https://github.com/adamkarvonen/chess_llm_interpretability) which is a follow-up of blog posts: https://adamkarvonen.github.io/machine_learning/2024/01/03/chess-world-models.html https://adamkarvonen.github.io/machine_learning/2024/03/20/chess-gpt-interventions.html 

I'd like also to replicate it by considering the FEN format (instead of PGN) and  PGN/FEN datasets for the same positions, (ii) holds objective/masking constant, and (iii) applies Karvonen-style mechanistic probes/interventions to FEN-trained models 



```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-24 16:38 | Codex | Other | I'd like to reproduce this paper https://arxiv.org/abs/2403.15498 (source code here: https://github.com/adamkarvonen/chess_llm_interpretabi… |
| 3 | 2026-02-24 17:52 | Codex | Other | go ahead |
| 4 | 2026-02-24 19:59 | Codex | ToolingBuild | please use "uv" to install what you need and run |
| 5 | 2026-02-25 07:39 | Codex | Other | about FEN, the idea is to obtain them from PGN, right? what's the blocker? |
| 6 | 2026-02-25 07:41 | Codex | Question | What about training a model and have our own checkpoint on FEN, using another tokenizer? |
| 7 | 2026-02-25 07:43 | Codex | Other | yes, go ahead |
| 8 | 2026-02-25 08:14 | Codex | ToolingBuild | please run a longer FEN pretrain (same setup, more iters/data) to get a stronger checkpoint before PGN-vs-FEN comparisons... can you also e… |
| 9 | 2026-02-25 13:07 | Codex | Other | now launch the full PGN-vs-FEN comparison using this new checkpoint. |
| 10 | 2026-02-25 16:04 | Codex | Question | what's the status? |
| 11 | 2026-02-25 17:10 | Codex | Other | before relaunching, is it worth correcting something? |
| 12 | 2026-02-25 17:14 | Codex | Other | ok, then relaunch with the new settings |
| 13 | 2026-02-25 18:22 | Codex | BugFixRequest | it's done but there is an error |
| 14 | 2026-02-26 04:19 | Codex | BugFixRequest | yes please fix issues with FEN |
| 15 | 2026-02-26 09:18 | Codex | Other | Run full PGN-vs-FEN again with current fixes (to update final artifacts consistently) |
| 16 | 2026-02-26 11:14 | Codex | Other | please investigate |
| 17 | 2026-02-26 15:53 | Codex | Other | re-do |
| 18 | 2026-02-27 05:37 | Codex | Question | what to do next? |
| 19 | 2026-02-27 05:39 | Codex | Other | yes |
| 20 | 2026-02-27 06:49 | Codex | Other | go |
| 21 | 2026-02-27 12:34 | Codex | Other | status? |
| 22 | 2026-02-27 12:35 | Codex | BugFixRequest | please improve and fix the situation... it's not normal |
| 23 | 2026-03-05 19:41 | Codex | BugFixRequest | please fix the FEN issue |
| 24 | 2026-03-05 20:32 | Codex | Other | is FEN: success_rate=0.0 still bad? |
| 25 | 2026-03-05 20:36 | Codex | Other | so what to do? |
| 26 | 2026-03-05 20:37 | Codex | Other | go this way |
| 27 | 2026-03-05 23:14 | Codex | Other | is PGN success_rate = 0.6503496503496503 conform to the original study? |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `0f61e66` | 2024-11-18T20:57:34Z | Adam Karvonen | Clean up |
| `793b010` | 2024-11-18T20:56:33Z | Adam Karvonen | Clean up |
| `3c8db9f` | 2024-05-24T14:38:14-05:00 | Adam Karvonen | Add documentation on adding functions |
| `2a89376` | 2024-05-20T12:22:19-05:00 | Adam Karvonen | Fix othello data gen |
| `9c78700` | 2024-05-18T07:36:10-05:00 | Adam Karvonen | Add directions |
| `f726692` | 2024-05-18T00:48:26-05:00 | Adam Karvonen | Support othellogpt probing |
| `0f0eef5` | 2024-05-17T16:13:29-05:00 | Adam Karvonen | Update to use shape name convention |
| `04deec2` | 2024-05-07T08:15:14-05:00 | Adam Karvonen | Add board_to_pin_state function, use int8 as dtype |
| `a20028a` | 2024-04-28T22:05:12-05:00 | Adam Karvonen | Formatting |
| `d6c9569` | 2024-04-28T19:33:07-05:00 | Adam Karvonen | Add documentation on data filtering pipeline |
| `5c1253d` | 2024-04-11T09:28:49-05:00 | Adam Karvonen | Track saved figures |
| `34be49f` | 2024-04-11T09:28:38-05:00 | Adam Karvonen | Clean up and format utility notebooks |
| `b13d5bc` | 2024-04-11T09:26:55-05:00 | Adam Karvonen | Intervene at all positions |
| `986b21a` | 2024-04-11T09:19:22-05:00 | Adam Karvonen | Store string instead of object in dictionary |
| `7f460e2` | 2024-04-11T09:18:30-05:00 | Adam Karvonen | Remove experimental indexing functions |
| `bb6a02c` | 2024-04-10T22:05:58-05:00 | Adam Karvonen | Adding new intervention indices functions |
| `7b1fdf2` | 2024-04-10T20:44:39-05:00 | Adam Karvonen | Help out the type checker |
| `d37d924` | 2024-04-10T20:35:00-05:00 | Adam Karvonen | Add white_pos and black_pos indices functions |
| `661c4bc` | 2024-04-10T18:54:06-05:00 | Adam Karvonen | Switch to torch.no_grad() |
| `11c4e42` | 2024-04-10T18:50:29-05:00 | Adam Karvonen | Add test_only to test artifacts' names |
| `b645fc8` | 2024-04-10T17:58:22-05:00 | Adam Karvonen | Make the type checker happy |
| `6bffc5d` | 2024-04-10T17:41:09-05:00 | Adam Karvonen | Test caa |
| `f249db0` | 2024-04-10T17:27:04-05:00 | Adam Karvonen | Switch from numpy to tensors for state stacks |
| `1bb3f78` | 2024-04-10T17:05:44-05:00 | Adam Karvonen | set to dtype torch.int |
| `9298103` | 2024-04-10T16:32:15-05:00 | Adam Karvonen | Add end to end board state interventions test |
| `0f506f2` | 2024-04-10T15:48:35-05:00 | Adam Karvonen | Add wandb argument |
| `4578b98` | 2024-04-10T15:45:41-05:00 | Adam Karvonen | Clean up formatting |
| `fc08661` | 2024-04-10T15:41:47-05:00 | Adam Karvonen | Move configs to chess_utils |
| `8ac987b` | 2024-04-10T15:17:41-05:00 | Adam Karvonen | Add additional board to state functions |
| `dd2819f` | 2024-04-10T15:12:08-05:00 | Adam Karvonen | Add extra configs and argparse |
| `309b8ed` | 2024-04-10T14:02:00-05:00 | Adam Karvonen | Remove old layers argument |
| `4aae66f` | 2024-04-07T22:33:43-05:00 | Adam Karvonen | Add better commentary to the Jupyter notebook |
| `1ed0500` | 2024-04-05T14:24:53-05:00 | Adam Karvonen | Add VRAM and time info to README |
| `890988d` | 2024-04-05T10:26:17-05:00 | Adam Karvonen | Add an attacked square probe |
| `5efa0ad` | 2024-03-30T10:27:10-05:00 | Adam Karvonen | Tighten up test epsilon |
| `b374401` | 2024-03-28T12:05:09-05:00 | Adam Karvonen | Add function for predicting next move |
| `df1e4d7` | 2024-03-28T11:36:31-05:00 | Adam Karvonen | Remove name overlap |
| `de9e263` | 2024-03-28T10:00:32-05:00 | Adam Karvonen | Improve replication directions |
| `b2a4649` | 2024-03-28T09:57:23-05:00 | Adam Karvonen | Remove extra argument |
| `66dd52c` | 2024-03-27T21:57:23-05:00 | Adam Karvonen | Properly initialize probes in tests |
| `2d2bc6b` | 2024-03-27T21:17:48-05:00 | Adam Karvonen | Move probe initialization out of training loop |
| `e02e684` | 2024-03-27T20:45:19-05:00 | Adam Karvonen | Update pytest command |
| `b2a0af4` | 2024-03-27T18:19:25-05:00 | Adam Karvonen | Add end to end tests for probe training and testing |
| `3ba1286` | 2024-03-27T17:13:20-05:00 | Adam Karvonen | Move nanogpt conversion notebook |
| `fad4696` | 2024-03-27T16:59:33-05:00 | Adam Karvonen | Train multiple probes at once |
| `e2b82c3` | 2024-03-26T13:15:17-05:00 | Adam Karvonen | Delete temporary directory |
| `92f6d4f` | 2024-03-26T11:19:38-05:00 | Adam Karvonen | Enable easy use of GPTs with different dimensions |
| `29738bb` | 2024-03-23T16:13:22-05:00 | Adam Karvonen | Add links to all other related repos. |
| `0a42da8` | 2024-03-23T15:49:53-05:00 | Adam Karvonen | Notebook to create skill intervention from skill probes |
| `d8e6ecc` | 2024-03-23T15:49:36-05:00 | Adam Karvonen | Notebook used to look through board state intervention grid sweeps |
| `46364d1` | 2024-03-23T15:47:58-05:00 | Adam Karvonen | Final graph creation notebook used for paper |
| `569a1a3` | 2024-03-23T15:47:26-05:00 | Adam Karvonen | Improve heat map plotting, make intervention accurate |
| `e8b6c86` | 2024-03-23T15:45:45-05:00 | Adam Karvonen | Delete hardcoded target value |
| `c5d561d` | 2024-03-23T15:45:10-05:00 | Adam Karvonen | Clean up board state interventions testing code |
| `7191409` | 2024-03-23T15:43:21-05:00 | Adam Karvonen | Disable caa cascades by default |
| `dbaf619` | 2024-03-23T15:42:51-05:00 | Adam Karvonen | Add for loop to train a probe on arbitrary sets of layers |
| `f44c27b` | 2024-03-23T15:42:35-05:00 | Adam Karvonen | Discuss contrastive activations and interventions in README |
| `e1ceeca` | 2024-02-29T19:49:27-06:00 | Adam Karvonen | Rename stockfish_data_filtering to chess_gpt_eval_data_filtering |
| `1c46c3a` | 2024-02-29T19:47:41-06:00 | Adam Karvonen | Add a notebook for manipulating chess_gpt_eval outputs |
| `586e4c4` | 2024-02-29T17:48:59-06:00 | Adam Karvonen | Add an optional pos_end parameter |
| `db4546f` | 2024-02-28T14:29:58-06:00 | Adam Karvonen | Add an option to create "cascading" contrastive activations |
| `5f4ff98` | 2024-02-28T13:00:20-06:00 | Adam Karvonen | Annotate tensor shapes, more clean up |
| `0c58f37` | 2024-02-28T11:00:27-06:00 | Adam Karvonen | Clean up contrastive activation code |
| `b95a3fd` | 2024-02-28T10:12:46-06:00 | Adam Karvonen | Add in progress classification function |
| `f41ce44` | 2024-02-26T18:15:40-06:00 | Adam Karvonen | Move model to torch.device when instantiating it, use DEVICE as a constant |
| `9cbe4fa` | 2024-02-26T17:38:33-06:00 | Adam Karvonen | Include an option to visualize the 16 layer model probe outputs |
| `f03de03` | 2024-02-26T17:20:39-06:00 | Adam Karvonen | Move reference notebooks to utils |
| `40270e1` | 2024-02-26T17:19:14-06:00 | Adam Karvonen | Move data exploration notebook to utils folder |
| `8f79054` | 2024-02-26T17:18:00-06:00 | Adam Karvonen | Default to using 8 layer model |
| `2dc0d87` | 2024-02-26T17:07:50-06:00 | Adam Karvonen | Add updated linear probes |
| `d0a74a1` | 2024-02-26T17:05:03-06:00 | Adam Karvonen | Delete old 16 layer activations and probes |
| `c69c772` | 2024-02-26T16:53:21-06:00 | Adam Karvonen | Graph probe predictions with chess unicode characters |
| `47627b7` | 2024-02-26T16:39:51-06:00 | Adam Karvonen | Clean up unused imports, mention softmax location, select final game idx |
| `40a71af` | 2024-02-26T16:30:05-06:00 | Adam Karvonen | Document reason for discarding unused games |
| `c89a804` | 2024-02-26T16:28:33-06:00 | Adam Karvonen | Discard unused games to lower VRAM usage |
| `c1a76bd` | 2024-02-26T14:37:03-06:00 | Adam Karvonen | Fix jaxtyping type annotation error |
| `45d152f` | 2024-02-26T14:19:42-06:00 | Adam Karvonen | Mention python 3.11 |
| `5d34069` | 2024-02-26T14:19:11-06:00 | Adam Karvonen | document tensor shapes |
| `ba28a71` | 2024-02-26T13:51:05-06:00 | Adam Karvonen | Add shape annotations |
| `e51e29e` | 2024-02-26T13:00:40-06:00 | Adam Karvonen | Set black formatter max line length to 100 |
| … | | | _+205 more commits_ |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **6** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (ToolingBuild) [2026-02-24 19:59] — please use "uv" to install what you need and run [T:Codex/rollout-]
- **BL-002** (ToolingBuild) [2026-02-25 08:14] — please run a longer FEN pretrain (same setup, more iters/data) to get a stronger checkpoint before PGN-vs-FEN comparisons... can you also estimate time needed wrt iters/data? [T:Codex/rollout-]
- **BL-003** (BugFixRequest) [2026-02-25 18:22] — it's done but there is an error [T:Codex/rollout-]
- **BL-004** (BugFixRequest) [2026-02-26 04:19] — yes please fix issues with FEN [T:Codex/rollout-]
- **BL-005** (BugFixRequest) [2026-02-27 12:35] — please improve and fix the situation... it's not normal [T:Codex/rollout-]
- **BL-006** (BugFixRequest) [2026-03-05 19:41] — please fix the FEN issue [T:Codex/rollout-]

## Evidence pointers

- [R:chess-llmtraining] — repo at `/Users/mathieuacher/SANDBOX/chess-llmtraining`
- [T:chess-llmtraining/claude] — Claude sessions at `~/.claude/projects/chess-llmtraining...`
- [T:chess-llmtraining/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-llmtraining

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.