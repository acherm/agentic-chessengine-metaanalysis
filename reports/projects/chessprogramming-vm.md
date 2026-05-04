# chessprogramming-vm

_Evidence-based dossier. Generated 2026-04-22 14:55 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chessprogramming-vm` [R:chessprogramming-vm]
- **Primary language:** Python
- **Coding agent(s):** Claude Code, Codex
- **Period:** 2026-03-01 07:47 → 2026-04-15 16:59
- **LOC by language:** JSON (1297598 LOC, 11985 files), Python (43642 LOC, 125 files), Markdown (24776 LOC, 164 files), C (15932 LOC, 30 files), XML (1030 LOC, 8 files), LaTeX (575 LOC, 15 files), Text (442 LOC, 36 files), HTML (387 LOC, 2 files)
- **Totals:** 12367 files, 1384448 LOC [S:scan]
- **Git:** 15 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 1 main + 0 subagent transcripts [T:chessprogramming-vm/claude]
- Claude models seen: claude-opus-4-6
- Codex sessions: 5 [T:chessprogramming-vm/codex]
- Codex models seen: gpt-5.3-codex, gpt-5.4

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 1 | 12 | 333 | 258130 | 19363488 | 224743 | $52.62 |
| Codex | 5 | 290 | 426011016 | 2164172 | 392447616 | — | $603.21 |
| **Total** |  |  |  |  |  |  | **$655.83** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| UCI protocol | 11481 | `README.md` |
| Minimax/Negamax | 11479 | `README.md` |
| En passant | 10986 | `README.md` |
| FEN parsing | 10884 | `paper/data/feature_guard_loc.csv` |
| Transposition table | 10298 | `FEATURE_MODEL.md` |
| Alpha-beta | 10169 | `README.md` |
| Pawn structure | 7947 | `README.md` |
| Zobrist hashing | 6727 | `README.md` |
| Quiescence | 6597 | `README.md` |
| Tapered evaluation | 5953 | `README.md` |
| Time management | 4995 | `FEATURE_MODEL.md` |
| Iterative deepening | 4295 | `README.md` |
| Principal-variation (PV) | 4275 | `README.md` |
| Opening book | 4125 | `FEATURE_MODEL.md` |
| Board: bitboard | 4113 | `README.md` |
| Mobility | 4065 | `README.md` |
| Null-move pruning | 4060 | `README.md` |
| Killer moves | 4000 | `README.md` |
| Razoring | 3933 | `README.md` |
| Futility pruning | 3863 | `README.md` |
| Aspiration windows | 3730 | `README.md` |
| Late-move reduction (LMR) | 3613 | `README.md` |
| History heuristic | 3597 | `README.md` |
| Board: mailbox 10x12 | 3282 | `README.md` |
| Board: mailbox 8x8 | 3089 | `README.md` |
| Board: 0x88 | 2903 | `README.md` |
| Material counting | 2094 | `paper/main.tex` |
| Perft | 1771 | `README.md` |
| Check/Checkmate | 1567 | `paper/data/feature_span_metrics.json` |
| Board: magic bitboards | 1527 | `README.md` |
| Castling | 1454 | `README.md` |
| Evaluation/PST | 619 | `paper/data/feature_guard_loc.csv` |
| Endgame tables | 526 | `replication-repo/data/chessprogramming_cache/manifest.json` |
| NNUE/neural eval | 501 | `paper/main.bbl` |
| King safety | 308 | `paper/data/feature_guard_loc.csv` |
| Promotion | 262 | `paper/data/feature_span_metrics.json` |
| PGN | 226 | `replication-repo/sessions/engineering_thread.md` |
| Move ordering (MVV-LVA) | 94 | `replication-repo/data/chessprogramming_cache/manifest.json` |
| Late-move pruning (LMP) | 49 | `replication-repo/src/cpw_variability/taxonomy_seed.py` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | exec_command | 3442 |
| Codex | write_stdin | 511 |
| Claude | Bash | 55 |
| Codex | update_plan | 30 |
| Codex | view_image | 28 |
| Claude | Edit | 23 |
| Claude | Read | 16 |
| Claude | Write | 5 |
| Codex | request_user_input | 4 |
| Claude | Grep | 1 |
| Codex | read_thread_terminal | 1 |

## Interaction profile

- Total user prompts (both agents): **302**
- Avg prompt length: 255.1 chars
- Intent distribution:
  - Other: 152
  - Constraint: 47
  - FeatureRequest: 46
  - Scenario: 44
  - TestRequest: 40
  - Documentation: 28
  - Question: 25
  - ToolingBuild: 21
  - BugFixRequest: 15
  - RefactorRequest: 8

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-03-01 07:47 — session `rollout-`_

```
I'd like to build a feature model (as in software product line) of the variability of chess engine implementation... For this, I'd like to rely on chessprogramming.org which is a unique resource describing many techniques, actual chess engines, etc. 

Please synthesize such a feature model with automated scripts. 
Each feature should be traced back to a resource and justified. 
Keep a cache of downloaded resources of chessprogramming (in a dedicated folder). 

In addition, I'd like to have a comparison table of chess engines, with supported/unsupported features

```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-03-01 07:53 | Codex | FeatureRequest,BugFixRequest | PLEASE IMPLEMENT THIS PLAN: # CPW Variability Mining Pipeline and SPL Feature Model ## Summary Build a Python CLI pipeline that mines `ches… |
| 3 | 2026-03-01 08:12 | Codex | FeatureRequest,Constraint | I can run on my side, but I'd like to avoid to be a scrapper, and I'm OK to not flood the website... implement a safe strategy, especially … |
| 4 | 2026-03-01 09:27 | Codex | Other | mathieuacher@Mathieus-MacBook-Pro chessprogramming-vm % PYTHONPATH=src python3 -m cpw_variability.cli fetch \ --seed main \ --mode snapshot… |
| 5 | 2026-03-01 10:19 | Codex | Other | please commit everything, including artefacts generated/cached |
| 6 | 2026-03-01 10:33 | Codex | Other | now we should significantly improve the pipeline... here is a partial review of the feature model in FeatureIDE for <and name="BoardReprese… |
| 7 | 2026-03-01 14:35 | Codex | Other | please commit |
| 8 | 2026-03-01 14:43 | Codex | ToolingBuild | it's a bit better... though far from perfect... anyway. Now I want a feature model to guide the implementation of a family of chess engines… |
| 9 | 2026-03-01 14:52 | Codex | FeatureRequest,Constraint | let's focus on the feature model: Add explicit cross-tree constraints (requires/excludes) and export them into FeatureIDE <constraints>. an… |
| 10 | 2026-03-01 16:12 | Codex | Other | great! is it possible to increase the max depth to 1? |
| 11 | 2026-03-01 16:21 | Codex | Other | oh there is a misunderstanding... depth max 3 (default) was OK... I was targetting the ability to have depth=4 |
| 12 | 2026-03-04 23:07 | Codex | FeatureRequest,ToolingBuild | leveraging the extracted feature model at depth=4 and mainly using compile-time options (corresponding to features of the feature model), p… |
| 13 | 2026-03-04 23:19 | Codex | Other | I want a real implementation of each feature |
| 14 | 2026-03-04 23:39 | Codex | FeatureRequest,Scenario | implement full tournament legality” (castling/en-passant/repetition/50-move) and then map additional CPW features on top |
| 15 | 2026-03-05 06:37 | Codex | Other | go |
| 16 | 2026-03-05 08:26 | Codex | FeatureRequest,TestRequest | can we envision to derive one variant, and to make perft pass? |
| 17 | 2026-03-05 08:31 | Codex | FeatureRequest,TestRequest | can you try 5 random configurations/variants, make the perft, and report results on a CSV-like format, where each row is a variant, and fea… |
| 18 | 2026-03-05 08:44 | Codex | Question | why are variants not passing? |
| 19 | 2026-03-05 09:59 | Codex | FeatureRequest | yes please add the constraint, which seems obvious |
| 20 | 2026-03-05 10:03 | Codex | TestRequest,Scenario | can we try perft depth=5? and re-run bench... |
| 21 | 2026-03-05 10:26 | Codex | Other | let's try with depth 6 |
| 22 | 2026-03-05 10:31 | Codex | TestRequest,Scenario | nice! what would be the best configuration/variant for speeding up perft at depth 6? |
| 23 | 2026-03-05 10:38 | Codex | Constraint,Question | can you generate n=5 random chess engines without Castling feature? |
| 24 | 2026-03-05 10:44 | Codex | BugFixRequest,TestRequest | it's reassuring they all fail for perft ;) |
| 25 | 2026-03-05 10:51 | Codex | BugFixRequest,TestRequest | why perft_random_variants_no_castling.csv then FAIL? |
| 26 | 2026-03-05 10:51 | Codex | BugFixRequest,TestRequest | why perft_random_variants_no_castling.csv then FAIL? |
| 27 | 2026-03-05 10:51 | Codex | Other | ignore the image... |
| 28 | 2026-03-05 10:55 | Codex | BugFixRequest | the Codex thread in this folder is problematic since it contains an image... { "error": { "message": "Invalid 'input[480].content[2].image_… |
| 29 | 2026-03-05 11:01 | Codex | BugFixRequest | still the issue :( |
| 30 | 2026-03-05 12:10 | Codex | BugFixRequest,TestRequest | why perft_random_variants_no_castling.csv then FAIL? |
| 31 | 2026-03-05 12:38 | Codex | Other | oh super nice! isn't it strange to have CFG_MOVE_GENERATION as optional? |
| 32 | 2026-03-05 12:41 | Codex | TestRequest,Documentation | yes, please state it's mandatory... please document somewhere the justification of some constraints added and how some features work and th… |
| 33 | 2026-03-05 12:43 | Codex | Other | please commit |
| 34 | 2026-03-05 12:50 | Codex | TestRequest,Scenario | pick n=3 random chess variants and organize a small tournament among them (check before the perft test) |
| 35 | 2026-03-05 13:06 | Codex | FeatureRequest,Question | can you add Stockfish (skill 1, lowest Elo possible) as a player? and run again? |
| 36 | 2026-03-05 13:17 | Codex | FeatureRequest | super nice! let's add two new players, with a stronger Stockfish and a much stronger Stockfish (but below 2200 Elo) |
| 37 | 2026-03-05 13:45 | Codex | FeatureRequest | please add a strong Stockfish 2500 Elo |
| 38 | 2026-03-05 15:12 | Codex | Scenario | I'd like to redo a proper tournament, with 3 variants of chess engines and 4 Stockfish... the goal is to have a good assessment of Elo of e… |
| 39 | 2026-03-05 16:26 | Codex | Other | continue |
| 40 | 2026-03-05 16:29 | Codex | Scenario | great! try to find 2 best configurations/variants, and run a new tournament with the same players (from scratch) |
| 41 | 2026-03-05 17:16 | Codex | Other | sorry for the misunderstanding, when I say 2 best variants I was thinking: what are the best combinations of features you could do to reach… |
| 42 | 2026-03-05 17:25 | Codex | Other | investigate why there are illegal moves in these variants |
| 43 | 2026-03-05 17:36 | Codex | BugFixRequest | nice, this fix will benefit to many variants I suspect |
| 44 | 2026-03-05 17:36 | Codex | Other | ok let's assess the two best chess variants |
| 45 | 2026-03-05 17:42 | Codex | Question | can you improve the strength of some features/variants? |
| 46 | 2026-03-05 19:08 | Codex | Scenario | let's go for a tournament |
| 47 | 2026-03-05 19:41 | Codex | Other | please commit and report on current assessment/experiments |
| 48 | 2026-03-05 21:29 | Codex | Other | is there a process still running? if yes, why? |
| 49 | 2026-03-05 21:32 | Codex | Other | yes please |
| 50 | 2026-04-02 08:59 | Codex | FeatureRequest | "uses a negamax alpha-beta tree search with pruning and iterative deepening" is there a configuration that would implement such a chess eng… |
| 51 | 2026-04-02 12:29 | Codex | FeatureRequest,BugFixRequest | OK... there is, I think, a big general issue. the tldr; is that most of the features are simply not fully implemented to say the least... i… |
| 52 | 2026-04-02 12:33 | Codex | Other | please go with Phase 1... but assess quickly that your modularization pays off and that features can be combined |
| 53 | 2026-04-02 14:49 | Codex | Other | let's go to Phase 2 |
| 54 | 2026-04-02 17:01 | Codex | TestRequest | a natural challenge is to handle properly feature interactions and how features combined... specifically here, after Phase 1 and Phase 2, w… |
| 55 | 2026-04-02 17:07 | Codex | Documentation | please heavily document and commit |
| 56 | 2026-04-03 05:11 | Codex | Other | let's move to all these steps |
| 57 | 2026-04-03 12:00 | Codex | FeatureRequest | please go to Extend Phase 3 with richer evaluation subfeatures and stronger evaluation-specific probes... I would day one particular use ca… |
| 58 | 2026-04-03 12:20 | Codex | Documentation | Promote some of these new evaluation subfeatures into first-class feature-model options instead of keeping them grouped under the current e… |
| 59 | 2026-04-03 12:34 | Codex | Other | please go ahead |
| 60 | 2026-04-03 13:10 | Codex | Other | yes promote into proper intermediate groups... and commit |
| … | | | | _+242 more prompts_ |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `402626d` | 2026-04-15T18:47:13+02:00 | Mathieu Acher | Fold Feature Model pointer into Implementation-Oriented Model |
| `ad9d7a5` | 2026-04-15T18:41:37+02:00 | Mathieu Acher | Rebalance README/FEATURE_MODEL.md framing |
| `2e96a19` | 2026-04-15T18:29:27+02:00 | Mathieu Acher | Add feature model visualization and UVL/FAMILIAR exports |
| `2aaf95e` | 2026-04-06T01:29:14+02:00 | Mathieu Acher | Add 20-game 2500 anchor match artifacts |
| `0a72c9b` | 2026-04-05T20:04:03+02:00 | Mathieu Acher | Optimize common search path and document anchor assessment |
| `7b1682d` | 2026-04-05T08:07:40+02:00 | Mathieu Acher | Add controlled tournament artifacts and setup comparison |
| `c5c01a2` | 2026-04-04T16:14:32+02:00 | Mathieu Acher | Add setup variability model and setup-based tournament tooling |
| `5259dc6` | 2026-04-04T13:29:42+02:00 | Mathieu Acher | Update README for executable feature status |
| `bedf3d1` | 2026-04-04T13:17:59+02:00 | Mathieu Acher | Implement real engine feature backends and runtime book/pondering |
| `748f796` | 2026-04-03T15:28:05+02:00 | Mathieu Acher | Promote evaluation leaves into hierarchical groups |
| `bbb79ca` | 2026-04-02T19:09:02+02:00 | Mathieu Acher | Modularize engine variation points and document feature interactions |
| `518d523` | 2026-03-05T20:42:24+01:00 | Mathieu Acher | Improve engine strength and add tournament assessment artifacts |
| `932eb04` | 2026-03-05T13:43:41+01:00 | Mathieu Acher | Enforce executable variant constraints and add perft benchmarking workflows |
| `2f957dd` | 2026-03-01T15:35:51+01:00 | Mathieu Acher | Improve feature mining precision with core anchors and strict noise filtering |
| `3ffe70a` | 2026-03-01T11:23:57+01:00 | Mathieu Acher | Add CPW variability mining pipeline with safe resumable crawling |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **133** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, ToolingBuild) [2026-03-01 07:47] — I'd like to build a feature model (as in software product line) of the variability of chess engine implementation... For this, I'd like to rely on chessprogramming.org which is a … [T:Codex/rollout-]
- **BL-002** (FeatureRequest, BugFixRequest, TestRequest, Documentation, ToolingBuild, Constraint, Scenario) [2026-03-01 07:53] — PLEASE IMPLEMENT THIS PLAN: # CPW Variability Mining Pipeline and SPL Feature Model ## Summary Build a Python CLI pipeline that mines `chessprogramming.org` into: 1. A 2-3 level S… [T:Codex/rollout-]
- **BL-003** (FeatureRequest, Constraint) [2026-03-01 08:12] — I can run on my side, but I'd like to avoid to be a scrapper, and I'm OK to not flood the website... implement a safe strategy, especially resumable with cache [T:Codex/rollout-]
- **BL-004** (ToolingBuild) [2026-03-01 14:43] — it's a bit better... though far from perfect... anyway. Now I want a feature model to guide the implementation of a family of chess engines... the goal is that, for each combinati… [T:Codex/rollout-]
- **BL-005** (FeatureRequest, Constraint) [2026-03-01 14:52] — let's focus on the feature model: Add explicit cross-tree constraints (requires/excludes) and export them into FeatureIDE <constraints>. and I suspect it's incomplete... can you a… [T:Codex/rollout-]
- **BL-006** (FeatureRequest, ToolingBuild) [2026-03-04 23:07] — leveraging the extracted feature model at depth=4 and mainly using compile-time options (corresponding to features of the feature model), please implement a product line of chess … [T:Codex/rollout-]
- **BL-007** (FeatureRequest, Scenario) [2026-03-04 23:39] — implement full tournament legality” (castling/en-passant/repetition/50-move) and then map additional CPW features on top [T:Codex/rollout-]
- **BL-008** (FeatureRequest, TestRequest, Scenario) [2026-03-05 08:26] — can we envision to derive one variant, and to make perft pass? [T:Codex/rollout-]
- **BL-009** (FeatureRequest, TestRequest, Question, Scenario) [2026-03-05 08:31] — can you try 5 random configurations/variants, make the perft, and report results on a CSV-like format, where each row is a variant, and features are both features of the variant/c… [T:Codex/rollout-]
- **BL-010** (FeatureRequest) [2026-03-05 09:59] — yes please add the constraint, which seems obvious [T:Codex/rollout-]
- **BL-011** (TestRequest, Scenario) [2026-03-05 10:03] — can we try perft depth=5? and re-run bench... [T:Codex/rollout-]
- **BL-012** (TestRequest, Scenario) [2026-03-05 10:31] — nice! what would be the best configuration/variant for speeding up perft at depth 6? [T:Codex/rollout-]
- **BL-013** (BugFixRequest, TestRequest, Scenario) [2026-03-05 10:44] — it's reassuring they all fail for perft ;) [T:Codex/rollout-]
- **BL-014** (BugFixRequest) [2026-03-05 10:55] — the Codex thread in this folder is problematic since it contains an image... { "error": { "message": "Invalid 'input[480].content[2].image_url'. Expected a base64-encoded data URL… [T:Codex/rollout-]
- **BL-015** (TestRequest, Documentation, Scenario) [2026-03-05 12:41] — yes, please state it's mandatory... please document somewhere the justification of some constraints added and how some features work and their possible impacts eg on perft [T:Codex/rollout-]
- **BL-016** (TestRequest, Scenario) [2026-03-05 12:50] — pick n=3 random chess variants and organize a small tournament among them (check before the perft test) [T:Codex/rollout-]
- **BL-017** (FeatureRequest) [2026-03-05 13:17] — super nice! let's add two new players, with a stronger Stockfish and a much stronger Stockfish (but below 2200 Elo) [T:Codex/rollout-]
- **BL-018** (FeatureRequest) [2026-03-05 13:45] — please add a strong Stockfish 2500 Elo [T:Codex/rollout-]
- **BL-019** (Scenario) [2026-03-05 15:12] — I'd like to redo a proper tournament, with 3 variants of chess engines and 4 Stockfish... the goal is to have a good assessment of Elo of each variant [T:Codex/rollout-]
- **BL-020** (Scenario) [2026-03-05 16:29] — great! try to find 2 best configurations/variants, and run a new tournament with the same players (from scratch) [T:Codex/rollout-]
- **BL-021** (BugFixRequest) [2026-03-05 17:36] — nice, this fix will benefit to many variants I suspect [T:Codex/rollout-]
- **BL-022** (Scenario) [2026-03-05 19:08] — let's go for a tournament [T:Codex/rollout-]
- **BL-023** (FeatureRequest) [2026-04-02 08:59] — "uses a negamax alpha-beta tree search with pruning and iterative deepening" is there a configuration that would implement such a chess engine? [T:Codex/rollout-]
- **BL-024** (FeatureRequest, BugFixRequest, Constraint) [2026-04-02 12:29] — OK... there is, I think, a big general issue. the tldr; is that most of the features are simply not fully implemented to say the least... it's just a representative example, but l… [T:Codex/rollout-]
- **BL-025** (TestRequest) [2026-04-02 17:01] — a natural challenge is to handle properly feature interactions and how features combined... specifically here, after Phase 1 and Phase 2, we can combine different board representa… [T:Codex/rollout-]
- **BL-026** (Documentation) [2026-04-02 17:07] — please heavily document and commit [T:Codex/rollout-]
- **BL-027** (FeatureRequest) [2026-04-03 12:00] — please go to Extend Phase 3 with richer evaluation subfeatures and stronger evaluation-specific probes... I would day one particular use case is to fully implement a chess engine … [T:Codex/rollout-]
- **BL-028** (Documentation) [2026-04-03 12:20] — Promote some of these new evaluation subfeatures into first-class feature-model options instead of keeping them grouped under the current evaluation flags... It sounds a great dir… [T:Codex/rollout-]
- **BL-029** (Question, Scenario) [2026-04-03 13:32] — can you organize a match (10 games say) between the best supposed variants and Stockfish at an interesting skill, says ~2200 (at 120+1 time control, CCRL 40/4 scale) using cuteche… [T:Codex/rollout-]
- **BL-030** (Constraint, Question) [2026-04-03 15:00] — what features should be implemented in priority to improve full (with or without pruning)? or what's part of the "commonality" should be improved? [T:Codex/rollout-]
- **BL-031** (FeatureRequest) [2026-04-03 15:52] — SEE sounds like an optional feature (can be turn on/off) Better move ordering seems optional as well and splitted into 3 subfeatures (at least), all optionals... Better TT seems a… [T:Codex/rollout-]
- **BL-032** (Scenario) [2026-04-03 18:38] — yes, Run the same updated pruning variant against Stockfish at the earlier ~2200 anchor to see whether the gain survives outside self-play. [T:Codex/rollout-]
- **BL-033** (FeatureRequest, RefactorRequest, Constraint) [2026-04-04 08:10] — please refactor to have Minimax as a selectable feature... I don't get why Magic Bitboards is not implemented... then implement weak/aliased features [T:Codex/rollout-]
- **BL-034** (Documentation) [2026-04-04 11:07] — let's go for the next steps you describe [T:Codex/rollout-]
- **BL-035** (Documentation) [2026-04-04 11:20] — update/commit README [T:Codex/rollout-]
- **BL-036** (Scenario) [2026-04-04 11:32] — please organize a tournament using cluechess-cli across different configurations/variants of the chess engine... let's consider N=3 variants, one is the supposedly the best, one i… [T:Codex/rollout-]
- **BL-037** (Constraint) [2026-04-04 11:53] — ok, I see... but then using depth=20 for the best variant that seems to "support" depth, and only this variant, seems fair... in general, given a variant, I'm expecting to set oth… [T:Codex/rollout-]
- **BL-038** (ToolingBuild) [2026-04-04 11:55] — please elaborate a feature model for modeling variability of "setup"... and then design a recommended setup table per variant, and ideally per feature... [T:Codex/rollout-]
- **BL-039** (FeatureRequest, Documentation, ToolingBuild, Scenario) [2026-04-04 12:33] — please add a setup section in the main README.md organize a tournament with N=3 (variant, setup), where setup is the best given a variant... and the N=3 variants cover supposedly … [T:Codex/rollout-]
- **BL-040** (Scenario) [2026-04-04 14:13] — commit and then run a controlled equal-condition tournament for the same 3 variants [T:Codex/rollout-]
- _+93 more items truncated in this view — see appendix._

## Evidence pointers

- [R:chessprogramming-vm] — repo at `/Users/mathieuacher/SANDBOX/chessprogramming-vm`
- [T:chessprogramming-vm/claude] — Claude sessions at `~/.claude/projects/chessprogramming-vm...`
- [T:chessprogramming-vm/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chessprogramming-vm

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.