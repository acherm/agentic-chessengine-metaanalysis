# gptchess

_Evidence-based dossier. Generated 2026-04-22 14:55 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/gptchess` [R:gptchess]
- **Primary language:** Python
- **Coding agent(s):** —
- **Period:** —
- **LOC by language:** Text (72243 LOC, 426 files), Python (1786 LOC, 12 files), Markdown (85 LOC, 1 files)
- **Totals:** 439 files, 74114 LOC [S:scan]
- **Git:** 17 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:gptchess/claude]
- Claude models seen: —
- Codex sessions: 0 [T:gptchess/codex]
- Codex models seen: —

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 0 | 0 | 0 | 0 | 0 | — | $0.00 |
| **Total** |  |  |  |  |  |  | **$0.00** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| Castling | 371 | `reasoning_llmso3o4mini.ipynb` |
| PGN | 310 | `analyze_games.py` |
| Pawn structure | 128 | `games_o3/game247c8e66-b073-4b2a-9707-a134a68c5fd6/session.txt` |
| Material counting | 102 | `games_o3/game335d5678-ad34-44d5-8ef2-d9881b5213a1/session.txt` |
| Check/Checkmate | 55 | `analysis_yosha.ipynb` |
| En passant | 45 | `games_o3/game473eb15e-f1fd-4000-be73-a7f31de6a8d3/session.txt` |
| King safety | 41 | `games_deepseek/integrated_games_2.pgn` |
| Promotion | 26 | `analysis_yosha.ipynb` |
| Transposition table | 23 | `analysis_prompt_variations.ipynb` |
| Mobility | 14 | `games_deepseek/integrated_games_0.pgn` |
| Time management | 5 | `games_db.csv` |
| UCI protocol | 1 | `gptchess/gpt-experiments.py` |
| Tapered evaluation | 1 | `analysis.ipynb` |

## Interaction profile

- Total user prompts (both agents): **0**
- Avg prompt length: 0 chars

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `d2e78f5` | 2025-05-26T18:40:34+02:00 | Mathieu Acher | o3 experiments and data |
| `553a867` | 2025-05-22T21:11:02+02:00 | Mathieu Acher | prompt variations on 1.e4 d6 2. Bb5+ with Monsieur Phi talk at Devoxx France |
| `a5c7f0b` | 2025-05-22T21:04:39+02:00 | Mathieu Acher | experiments with gpt4o a few months ago (unreleased and blog post to write); data from deepseek; prompt variations expe… |
| `8fea7d5` | 2024-05-07T18:31:32+02:00 | Mathieu Acher | further experiments |
| `56beb97` | 2024-05-07T16:19:35+02:00 | Mathieu Acher | Yosha dataset |
| `3588715` | 2024-05-07T16:18:51+02:00 | Mathieu Acher | Yosha dataset |
| `fe6875a` | 2024-05-07T16:17:42+02:00 | Mathieu Acher | Yosha experiments with 0-1 and simpler prompt |
| `0e3775a` | 2024-04-19T17:29:16+02:00 | Mathieu Acher | preliminary data and analysis |
| `8479700` | 2024-04-19T14:49:30+02:00 | Mathieu Acher | refactoring |
| `003d117` | 2024-04-19T14:27:05+02:00 | Mathieu Acher | prompt variatins |
| `99d1f51` | 2023-10-18T21:02:52+02:00 | Mathieu Acher | clarification about effect of temperature and altered prompts for Elo rating |
| `4c6d269` | 2023-10-18T12:29:38+02:00 | Mathieu Acher | clarification about effect of temperature and altered prompts for Elo rating |
| `54dfb0e` | 2023-10-18T11:56:21+02:00 | Mathieu Acher | fix altered prompt |
| `de6e39a` | 2023-10-18T11:29:22+02:00 | Mathieu Acher | fix |
| `5ef0bfc` | 2023-10-16T15:24:50+02:00 | Mathieu Acher | games |
| `96ebde9` | 2023-10-16T15:21:25+02:00 | Mathieu Acher | games |
| `d2de479` | 2023-10-16T15:16:13+02:00 | Mathieu Acher | Python scripts to execute experiments and analysis notebooks |

## User-driven feature backlog (best-effort, derived from prompts)

_No user prompts recovered; backlog cannot be reconstructed from sessions._

## Evidence pointers

- [R:gptchess] — repo at `/Users/mathieuacher/SANDBOX/gptchess`
- [T:gptchess/claude] — Claude sessions at `~/.claude/projects/gptchess...`
- [T:gptchess/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/gptchess

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.