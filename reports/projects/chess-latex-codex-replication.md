# chess-latex-codex-replication

_Evidence-based dossier. Generated 2026-04-22 14:53 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-latex-codex-replication` [R:chess-latex-codex-replication]
- **Primary language:** LaTeX
- **Coding agent(s):** Codex
- **Period:** 2026-02-16 21:02 → 2026-02-17 20:06
- **LOC by language:** LaTeX (2119 LOC, 5 files), JSON (1722 LOC, 32 files), Python (1126 LOC, 3 files), Markdown (194 LOC, 2 files), Shell (60 LOC, 3 files), Text (1 LOC, 1 files)
- **Totals:** 46 files, 5222 LOC [S:scan]
- **Git:** 11 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:chess-latex-codex-replication/claude]
- Claude models seen: —
- Codex sessions: 1 [T:chess-latex-codex-replication/codex]
- Codex models seen: gpt-5.3-codex

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 1 | 15 | 84679828 | 351723 | 82916096 | — | $119.73 |
| **Total** |  |  |  |  |  |  | **$119.73** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| PGN | 62 | `README.md` |
| Time management | 52 | `README.md` |
| UCI protocol | 43 | `README.md` |
| Castling | 28 | `README.md` |
| FEN parsing | 8 | `README.md` |
| En passant | 2 | `README.md` |
| Promotion | 2 | `README.md` |
| Material counting | 2 | `README.md` |
| Perft | 1 | `scripts/verify_check_legality.py` |
| Check/Checkmate | 1 | `scripts/verify_check_legality.py` |
| Minimax/Negamax | 1 | `README.md` |
| King safety | 1 | `README.md` |
| Opening book | 1 | `engine/latex_move_picker.tex` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | exec_command | 580 |
| Codex | write_stdin | 94 |

## Interaction profile

- Total user prompts (both agents): **15**
- Avg prompt length: 1493.0 chars
- Intent distribution:
  - Scenario: 5
  - Other: 5
  - FeatureRequest: 3
  - TestRequest: 2
  - ToolingBuild: 1
  - Question: 1
  - Constraint: 1
  - Documentation: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-02-16 21:02 — session `rollout-`_

```
I want to build a chess engine in LaTeX programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-16 21:23 | Codex | FeatureRequest | create a repo and git commit... |
| 3 | 2026-02-16 21:25 | Codex | Scenario | You have basically "cheated" in the sense you have used Lua, a rich, general-purpose programming language. I want a pure implementation in … |
| 4 | 2026-02-16 22:18 | Codex | Question,Scenario | how to use the LaTeX chess engine in overleaf says? I want to play chess against the LaTeX AI... using LaTeX commands... how to? |
| 5 | 2026-02-16 22:21 | Codex | Other | let's go yes |
| 6 | 2026-02-17 08:08 | Codex | Other | sounds great! any chance to have a single file to edit? |
| 7 | 2026-02-17 08:17 | Codex | Constraint | couldn't it possible to use a kind of \include to avoid appendix manually the AI move? |
| 8 | 2026-02-17 08:51 | Codex | TestRequest,Documentation | working like a charm... would it be possible to list all moves (mine, and those played by AI) in the PDF? furthermore overleaf compilation … |
| 9 | 2026-02-17 09:04 | Codex | Other | great! would it be possible to have some randomness? |
| 10 | 2026-02-17 09:43 | Codex | FeatureRequest | ok nice! now let's move to a proper Elo evaluation of the LaTeX engine. Please write scripts to launch experiments typically against Stockf… |
| 11 | 2026-02-17 10:51 | Codex | Scenario | mathieuacher@Mathieus-MacBook-Pro overleaf % cd /Users/mathieuacher/SANDBOX/chess-latex-codex-replication ./scripts/run_elo_quick.sh ./scri… |
| 12 | 2026-02-17 10:59 | Codex | Other | let's improve the chess engine now and reach the best performance possible |
| 13 | 2026-02-17 12:07 | Codex | Scenario | I have played a game and when there is a check, and it's the chess engine to play, it seems there are issues... can you check it's not the … |
| 14 | 2026-02-17 14:24 | Codex | Other | checked indeed... how to run bench and assess Elo? |
| 15 | 2026-02-17 19:43 | Codex | Scenario | Match-by-match estimates: - sf1200 (1200): 0-24-0 score=0.000 Elo=523.9 +/- 486.4 - sf1350 (1350): 0-24-0 score=0.000 Elo=673.9 +/- 486.4 -… |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `0c1a4c4` | 2026-02-17T13:15:47+01:00 | Mathieu Acher | Add check-response legality verifier against Stockfish |
| `dc0ff6c` | 2026-02-17T13:06:14+01:00 | Mathieu Acher | Tune LaTeX engine with opening book and stronger opening heuristics |
| `94598a3` | 2026-02-17T11:53:43+01:00 | Mathieu Acher | Fix proper Elo launcher with nounset-safe optional openings args |
| `afeab46` | 2026-02-17T10:53:17+01:00 | Mathieu Acher | Upgrade Elo experiment tooling with cutechess Stockfish runner |
| `4a1a36b` | 2026-02-17T10:42:32+01:00 | Mathieu Acher | Add configurable randomness to LaTeX engine and Overleaf workflow |
| `b42a689` | 2026-02-17T09:56:50+01:00 | Mathieu Acher | Optimize Overleaf single-file flow and add move history table |
| `cf6e4e3` | 2026-02-17T09:39:05+01:00 | Mathieu Acher | Auto-include AI moves in single-file Overleaf workflow |
| `a6e1890` | 2026-02-17T09:12:17+01:00 | Mathieu Acher | Add single-file Overleaf play workflow |
| `fe38f26` | 2026-02-16T23:36:16+01:00 | Mathieu Acher | Add Overleaf play template with board rendering |
| `bba167a` | 2026-02-16T23:15:54+01:00 | Mathieu Acher | Implement pure expl3 chess engine and remove Lua backend |
| `b928671` | 2026-02-16T22:24:26+01:00 | Mathieu Acher | Initial commit: LaTeX chess engine and Elo evaluation |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **10** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, ToolingBuild) [2026-02-16 21:02] — I want to build a chess engine in LaTeX programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess en… [T:Codex/rollout-]
- **BL-002** (FeatureRequest) [2026-02-16 21:23] — create a repo and git commit... [T:Codex/rollout-]
- **BL-003** (Scenario) [2026-02-16 21:25] — You have basically "cheated" in the sense you have used Lua, a rich, general-purpose programming language. I want a pure implementation in LaTeX with macros for the chess engine p… [T:Codex/rollout-]
- **BL-004** (Question, Scenario) [2026-02-16 22:18] — how to use the LaTeX chess engine in overleaf says? I want to play chess against the LaTeX AI... using LaTeX commands... how to? [T:Codex/rollout-]
- **BL-005** (Constraint) [2026-02-17 08:17] — couldn't it possible to use a kind of \include to avoid appendix manually the AI move? [T:Codex/rollout-]
- **BL-006** (TestRequest, Documentation) [2026-02-17 08:51] — working like a charm... would it be possible to list all moves (mine, and those played by AI) in the PDF? furthermore overleaf compilation is timing out, which is a bit strange si… [T:Codex/rollout-]
- **BL-007** (FeatureRequest) [2026-02-17 09:43] — ok nice! now let's move to a proper Elo evaluation of the LaTeX engine. Please write scripts to launch experiments typically against Stockfish and using cutechess-cli [T:Codex/rollout-]
- **BL-008** (Scenario) [2026-02-17 10:51] — mathieuacher@Mathieus-MacBook-Pro overleaf % cd /Users/mathieuacher/SANDBOX/chess-latex-codex-replication ./scripts/run_elo_quick.sh ./scripts/run_elo_proper.sh [RUN] sf1200 (1200… [T:Codex/rollout-]
- **BL-009** (Scenario) [2026-02-17 12:07] — I have played a game and when there is a check, and it's the chess engine to play, it seems there are issues... can you check it's not the case and that the chess engine is correc… [T:Codex/rollout-]
- **BL-010** (Scenario) [2026-02-17 19:43] — Match-by-match estimates: - sf1200 (1200): 0-24-0 score=0.000 Elo=523.9 +/- 486.4 - sf1350 (1350): 0-24-0 score=0.000 Elo=673.9 +/- 486.4 - sf1500 (1500): 0-24-0 score=0.000 Elo=8… [T:Codex/rollout-]

## Evidence pointers

- [R:chess-latex-codex-replication] — repo at `/Users/mathieuacher/SANDBOX/chess-latex-codex-replication`
- [T:chess-latex-codex-replication/claude] — Claude sessions at `~/.claude/projects/chess-latex-codex-replication...`
- [T:chess-latex-codex-replication/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-latex-codex-replication

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.