# chess-excel

_Evidence-based dossier. Generated 2026-04-22 14:52 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-excel` [R:chess-excel]
- **Primary language:** Python
- **Coding agent(s):** Codex
- **Period:** 2026-02-18 08:19 → 2026-02-18 22:57
- **LOC by language:** Python (2234 LOC, 6 files), Markdown (588 LOC, 8 files), Shell (113 LOC, 1 files)
- **Totals:** 15 files, 2935 LOC [S:scan]
- **Git:** not a git repo

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:chess-excel/claude]
- Claude models seen: —
- Codex sessions: 2 [T:chess-excel/codex]
- Codex models seen: gpt-5.3-codex

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 2 | 16 | 33827204 | 173988 | 32990592 | — | $48.15 |
| **Total** |  |  |  |  |  |  | **$48.15** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| UCI protocol | 16 | `README.md` |
| FEN parsing | 11 | `google_sheets/template_tabs/Input.csv` |
| Castling | 8 | `google_sheets/template_tabs/Input.csv` |
| PGN | 4 | `README.md` |
| Material counting | 4 | `google_sheets/named_functions.csv` |
| Promotion | 3 | `docs/play_in_excel.md` |
| Time management | 2 | `results/sf1320_vs_sf1500_smoke.pgn` |
| Perft | 1 | `docs/excel_formula_engine.md` |
| Minimax/Negamax | 1 | `docs/excel_formula_engine.md` |
| King safety | 1 | `docs/excel_formula_engine.md` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | exec_command | 191 |
| Codex | write_stdin | 190 |

## Interaction profile

- Total user prompts (both agents): **16**
- Avg prompt length: 74.0 chars
- Intent distribution:
  - FeatureRequest: 6
  - Other: 6
  - ToolingBuild: 3
  - Question: 3
  - TestRequest: 2
  - Scenario: 2
  - Constraint: 1
  - Documentation: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-02-18 08:19 — session `rollout-`_

```
I want to build a chess engine in Excel, without VBA or macros, but only using the Excel formula... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels 

```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-18 09:00 | Codex | FeatureRequest | implement now the workbook yes |
| 3 | 2026-02-18 09:10 | Codex | Documentation,Scenario | document how to play in Excel... |
| 4 | 2026-02-18 09:18 | Codex | Question | what's the format of the move? |
| 5 | 2026-02-18 09:24 | Codex | Other | I put e2e4 in Input!B12 but nothing happens... |
| 6 | 2026-02-18 09:27 | Codex | Other | Confirm Input!B13 now shows a new FEN. => no |
| 7 | 2026-02-18 09:31 | Codex | Other | still nothing... would it work with Google sheet? |
| 8 | 2026-02-18 09:33 | Codex | Scenario | I'm opening the file with Numbers... |
| 9 | 2026-02-18 09:34 | Codex | FeatureRequest,ToolingBuild | build a Google Sheets native port |
| 10 | 2026-02-18 10:29 | Codex | Question | how to upload on Google sheets? |
| 11 | 2026-02-18 10:34 | Codex | Other | any simple solution? |
| 12 | 2026-02-18 12:51 | Codex | FeatureRequest,Question | Can you implement a solution in ODS format? |
| 13 | 2026-02-18 14:30 | Codex | Other | can't open the xlsx in Excel online |
| 14 | 2026-02-18 21:28 | Codex | FeatureRequest,TestRequest | I want to build a chess engine in C programming language... at the end, I want to test this chess engine and assess its Elo rating, typical… |
| 15 | 2026-02-18 21:41 | Codex | FeatureRequest | use Stockfish (already installed) to assess Elo... write a small report on Elo estimation; then git create/commit |
| 16 | 2026-02-18 21:56 | Codex | Other | the benchmark and Elo assessment might be unfair for your engine, maybe not enough time... please check this. In general please improve sig… |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **7** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, ToolingBuild, Constraint) [2026-02-18 08:19] — I want to build a chess engine in Excel, without VBA or macros, but only using the Excel formula... at the end, I want to test this chess engine and assess its Elo rating, typical… [T:Codex/rollout-]
- **BL-002** (FeatureRequest) [2026-02-18 09:00] — implement now the workbook yes [T:Codex/rollout-]
- **BL-003** (Documentation, Scenario) [2026-02-18 09:10] — document how to play in Excel... [T:Codex/rollout-]
- **BL-004** (Scenario) [2026-02-18 09:33] — I'm opening the file with Numbers... [T:Codex/rollout-]
- **BL-005** (FeatureRequest, ToolingBuild) [2026-02-18 09:34] — build a Google Sheets native port [T:Codex/rollout-]
- **BL-006** (FeatureRequest, TestRequest, ToolingBuild) [2026-02-18 21:28] — I want to build a chess engine in C programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engine… [T:Codex/rollout-]
- **BL-007** (FeatureRequest) [2026-02-18 21:41] — use Stockfish (already installed) to assess Elo... write a small report on Elo estimation; then git create/commit [T:Codex/rollout-]

## Evidence pointers

- [R:chess-excel] — repo at `/Users/mathieuacher/SANDBOX/chess-excel`
- [T:chess-excel/claude] — Claude sessions at `~/.claude/projects/chess-excel...`
- [T:chess-excel/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-excel

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.