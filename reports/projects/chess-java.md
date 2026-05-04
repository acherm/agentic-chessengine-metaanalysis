# chess-java

_Evidence-based dossier. Generated 2026-04-22 14:52 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-java` [R:chess-java]
- **Primary language:** Java
- **Coding agent(s):** Codex
- **Period:** 2026-02-17 12:52 → 2026-02-18 17:01
- **LOC by language:** Java (2148 LOC, 13 files), Shell (362 LOC, 6 files), Python (152 LOC, 1 files), Markdown (146 LOC, 1 files), XML (27 LOC, 1 files)
- **Totals:** 22 files, 2835 LOC [S:scan]
- **Git:** not a git repo

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:chess-java/claude]
- Claude models seen: —
- Codex sessions: 1 [T:chess-java/codex]
- Codex models seen: gpt-5.3-codex

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 1 | 7 | 15259562 | 95624 | 14588928 | — | $21.85 |
| **Total** |  |  |  |  |  |  | **$21.85** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| UCI protocol | 7 | `README.md` |
| Promotion | 6 | `README.md` |
| FEN parsing | 5 | `README.md` |
| En passant | 5 | `README.md` |
| PGN | 5 | `README.md` |
| Transposition table | 5 | `README.md` |
| Perft | 4 | `README.md` |
| Material counting | 4 | `README.md` |
| Time management | 4 | `README.md` |
| Castling | 3 | `README.md` |
| Zobrist hashing | 3 | `README.md` |
| Check/Checkmate | 2 | `src/main/java/com/example/chess/engine/Board.java` |
| Minimax/Negamax | 2 | `README.md` |
| Quiescence | 2 | `README.md` |
| Alpha-beta | 1 | `README.md` |
| Iterative deepening | 1 | `README.md` |
| Evaluation/PST | 1 | `src/main/java/com/example/chess/engine/Evaluator.java` |
| Tapered evaluation | 1 | `README.md` |
| King safety | 1 | `README.md` |
| Mobility | 1 | `README.md` |
| Opening book | 1 | `README.md` |
| Endgame tables | 1 | `README.md` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | exec_command | 135 |
| Codex | write_stdin | 61 |
| Codex | update_plan | 3 |

## Interaction profile

- Total user prompts (both agents): **7**
- Avg prompt length: 432.1 chars
- Intent distribution:
  - FeatureRequest: 3
  - TestRequest: 3
  - ToolingBuild: 2
  - Other: 2
  - Scenario: 2

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-02-17 12:52 — session `rollout-`_

```
I want to build a chess engine in Java programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-17 18:06 | Codex | Other | /Users/mathieuacher/SANDBOX/chess-java/scripts/run_engine.sh takes forever... |
| 3 | 2026-02-18 09:23 | Codex | Other | the anity check is working... still running /Users/mathieuacher/SANDBOX/chess-java/scripts/run_engine.sh seems to take a lot of time, with … |
| 4 | 2026-02-18 09:26 | Codex | TestRequest | mathieuacher@Mathieus-MacBook-Pro chess-java % /Users/mathieuacher/SANDBOX/chess-java/scripts/run_engine.sh [chess-java] UCI engine started… |
| 5 | 2026-02-18 09:30 | Codex | TestRequest,Scenario | mathieuacher@Mathieus-MacBook-Pro chess-java % /Users/mathieuacher/SANDBOX/chess-java/scripts/run_engine.sh [chess-java] UCI engine started… |
| 6 | 2026-02-18 09:33 | Codex | FeatureRequest | I want to make run_engine work (and the assessment Elo basically) |
| 7 | 2026-02-18 16:45 | Codex | FeatureRequest,ToolingBuild | mathieuacher@Mathieus-MacBook-Pro chess-java % /Users/mathieuacher/SANDBOX/chess-java/scripts/assess_elo.sh "$(command -v stockfish)" 40 "4… |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **4** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, ToolingBuild) [2026-02-17 12:52] — I want to build a chess engine in Java programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess eng… [T:Codex/rollout-]
- **BL-002** (TestRequest) [2026-02-18 09:26] — mathieuacher@Mathieus-MacBook-Pro chess-java % /Users/mathieuacher/SANDBOX/chess-java/scripts/run_engine.sh [chess-java] UCI engine started. [chess-java] Waiting for UCI commands … [T:Codex/rollout-]
- **BL-003** (FeatureRequest) [2026-02-18 09:33] — I want to make run_engine work (and the assessment Elo basically) [T:Codex/rollout-]
- **BL-004** (FeatureRequest, ToolingBuild, Scenario) [2026-02-18 16:45] — mathieuacher@Mathieus-MacBook-Pro chess-java % /Users/mathieuacher/SANDBOX/chess-java/scripts/assess_elo.sh "$(command -v stockfish)" 40 "40/5+0.05" "1320,1520,1720,1920" Level Ga… [T:Codex/rollout-]

## Evidence pointers

- [R:chess-java] — repo at `/Users/mathieuacher/SANDBOX/chess-java`
- [T:chess-java/claude] — Claude sessions at `~/.claude/projects/chess-java...`
- [T:chess-java/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-java

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.