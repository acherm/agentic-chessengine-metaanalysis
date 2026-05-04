# chess-revisit-java-toCOBOL-codex

_Evidence-based dossier. Generated 2026-04-22 14:56 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-revisit-java-toRust-codex/chess-revisit-java-toCOBOL` [R:chess-revisit-java-toCOBOL-codex]
- **Primary language:** COBOL
- **Coding agent(s):** Codex
- **Period:** 2026-02-19 12:01 → 2026-02-21 13:20
- **LOC by language:** COBOL (6133 LOC, 1 files), Python (496 LOC, 2 files), Markdown (137 LOC, 2 files), Shell (4 LOC, 1 files)
- **Totals:** 6 files, 6770 LOC [S:scan]
- **Git:** not a git repo

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:chess-revisit-java-toCOBOL-codex/claude]
- Claude models seen: —
- Codex sessions: 1 [T:chess-revisit-java-toCOBOL-codex/codex]
- Codex models seen: gpt-5.3-codex

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 1 | 28 | 171399134 | 592115 | 167891200 | — | $241.16 |
| **Total** |  |  |  |  |  |  | **$241.16** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| UCI protocol | 9 | `PORTING_NOTES.md` |
| Time management | 7 | `Makefile` |
| FEN parsing | 6 | `PORTING_NOTES.md` |
| Perft | 6 | `PORTING_NOTES.md` |
| Castling | 6 | `README.md` |
| Opening book | 6 | `PORTING_NOTES.md` |
| Board: bitboard | 5 | `PORTING_NOTES.md` |
| Quiescence | 5 | `PORTING_NOTES.md` |
| Transposition table | 5 | `PORTING_NOTES.md` |
| Zobrist hashing | 5 | `PORTING_NOTES.md` |
| Null-move pruning | 5 | `PORTING_NOTES.md` |
| Mobility | 5 | `PORTING_NOTES.md` |
| Promotion | 4 | `README.md` |
| Evaluation/PST | 4 | `PORTING_NOTES.md` |
| Material counting | 4 | `PORTING_NOTES.md` |
| Minimax/Negamax | 3 | `chess_engine_trace` |
| Move ordering (MVV-LVA) | 3 | `chess_engine_trace` |
| PGN | 2 | `README.md` |
| Board: magic bitboards | 2 | `PORTING_NOTES.md` |
| Board: mailbox 8x8 | 2 | `PORTING_NOTES.md` |
| Alpha-beta | 2 | `PORTING_NOTES.md` |
| Iterative deepening | 2 | `PORTING_NOTES.md` |
| Principal-variation (PV) | 2 | `PORTING_NOTES.md` |
| Late-move reduction (LMR) | 2 | `PORTING_NOTES.md` |
| Tapered evaluation | 2 | `PORTING_NOTES.md` |
| King safety | 2 | `PORTING_NOTES.md` |
| Pawn structure | 2 | `PORTING_NOTES.md` |
| En passant | 1 | `README.md` |
| History heuristic | 1 | `PORTING_NOTES.md` |
| Futility pruning | 1 | `PORTING_NOTES.md` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | exec_command | 920 |
| Codex | write_stdin | 398 |

## Interaction profile

- Total user prompts (both agents): **28**
- Avg prompt length: 250.3 chars
- Intent distribution:
  - Other: 16
  - FeatureRequest: 5
  - Question: 5
  - Scenario: 2
  - Constraint: 1
  - TestRequest: 1
  - BugFixRequest: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-02-19 12:01 — session `rollout-`_

```
The goal is to write a chess engine in COBOL programming language (using GNU Cobol) through the translation of an existing chess engine written in Java, and available here: /Users/mathieuacher/SANDBOX/chess-java-cc/

Please stick as much as possible to the original Java implementation, keeping the same set of features, data structure, algorithms, approach, etc. 

```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-19 12:31 | Codex | Other | please go ahead and continue the translation/implementation |
| 3 | 2026-02-19 14:02 | Codex | Other | Next natural target is translating Java move/MoveList scoring/pick-best path and then search/SearchInfo + TT + alpha-beta on top of this ha… |
| 4 | 2026-02-19 14:16 | Codex | Other | yes let's go ahead |
| 5 | 2026-02-19 14:25 | Codex | Other | continue with the remaining features |
| 6 | 2026-02-19 14:40 | Codex | FeatureRequest,Constraint | continue but really stick to the original, Java implementation, don't try to invent new features or re-implement |
| 7 | 2026-02-19 14:54 | Codex | Other | continue with tapered evaluation + pawn/king terms. |
| 8 | 2026-02-19 15:04 | Codex | Other | let's continue with mobility terms and pawn hash |
| 9 | 2026-02-19 15:12 | Codex | FeatureRequest | let's implement MagicBitboards as in Java |
| 10 | 2026-02-19 16:51 | Codex | Other | continue the next Java-parity target |
| 11 | 2026-02-19 17:12 | Codex | Other | let's go to PolyglotBook |
| 12 | 2026-02-19 17:29 | Codex | FeatureRequest,TestRequest | please add such a test script |
| 13 | 2026-02-19 17:34 | Codex | Question | what's missing wrt original Java implementation? are you ready to assess the ported, COBOL engine? |
| 14 | 2026-02-19 17:42 | Codex | Other | structured parity: prioritize Time allocation... about stop, does it have an impact on Elo? |
| 15 | 2026-02-19 17:43 | Codex | Other | ok let's go this way |
| 16 | 2026-02-19 17:52 | Codex | Other | let's go for stop and then we're almost complete for a parity port... |
| 17 | 2026-02-19 18:14 | Codex | FeatureRequest,Question | could you write a script to assess Elo? |
| 18 | 2026-02-19 18:20 | Codex | Question | how to run the ported chess engine (COBOL) against the original Java implementation? |
| 19 | 2026-02-19 18:29 | Codex | Question | how to run the ported chess engine (COBOL) against Stockfish at different Skills to estimate Elo? |
| 20 | 2026-02-19 19:26 | Codex | Scenario | mathieuacher@Mathieus-MacBook-Pro chess-revisit-java-toCOBOL % >.... cutechess-cli \ -engine name=COBOL cmd="$COBOL" proto=uci option.Hash=… |
| 21 | 2026-02-20 14:09 | Codex | Scenario | Finished game 144 (SF-Skill-10 vs COBOL): 1-0 {White wins by adjudication} Score of COBOL vs SF-Skill-10: 0 - 144 - 0 [0.000] 144 Started g… |
| 22 | 2026-02-20 19:21 | Codex | Other | please go ahead |
| 23 | 2026-02-20 20:41 | Codex | Other | let's try first running Elo on longer TC |
| 24 | 2026-02-20 22:21 | Codex | BugFixRequest | please fix the bestmove bug |
| 25 | 2026-02-20 22:29 | Codex | Other | let's run a benchmark now to see the effect and whethere we can truly assess its Elo |
| 26 | 2026-02-20 22:43 | Codex | Question | can you benchmark by allocating more time? |
| 27 | 2026-02-20 23:12 | Codex | Other | run a similar benchmark, but try to gain more solid evidence about Elo |
| 28 | 2026-02-21 12:44 | Codex | Other | continue |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **7** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest) [2026-02-19 12:01] — The goal is to write a chess engine in COBOL programming language (using GNU Cobol) through the translation of an existing chess engine written in Java, and available here: /Users… [T:Codex/rollout-]
- **BL-002** (FeatureRequest, Constraint) [2026-02-19 14:40] — continue but really stick to the original, Java implementation, don't try to invent new features or re-implement [T:Codex/rollout-]
- **BL-003** (FeatureRequest) [2026-02-19 15:12] — let's implement MagicBitboards as in Java [T:Codex/rollout-]
- **BL-004** (FeatureRequest, TestRequest) [2026-02-19 17:29] — please add such a test script [T:Codex/rollout-]
- **BL-005** (Scenario) [2026-02-19 19:26] — mathieuacher@Mathieus-MacBook-Pro chess-revisit-java-toCOBOL % >.... cutechess-cli \ -engine name=COBOL cmd="$COBOL" proto=uci option.Hash=64 \ -engine name=SF-Skill-$S cmd="$SF" … [T:Codex/rollout-]
- **BL-006** (Scenario) [2026-02-20 14:09] — Finished game 144 (SF-Skill-10 vs COBOL): 1-0 {White wins by adjudication} Score of COBOL vs SF-Skill-10: 0 - 144 - 0 [0.000] 144 Started game 146 of 200 (SF-Skill-10 vs COBOL) Fi… [T:Codex/rollout-]
- **BL-007** (BugFixRequest) [2026-02-20 22:21] — please fix the bestmove bug [T:Codex/rollout-]

## Evidence pointers

- [R:chess-revisit-java-toCOBOL-codex] — repo at `/Users/mathieuacher/SANDBOX/chess-revisit-java-toRust-codex/chess-revisit-java-toCOBOL`
- [T:chess-revisit-java-toCOBOL-codex/claude] — Claude sessions at `~/.claude/projects/chess-revisit-java-toCOBOL...`
- [T:chess-revisit-java-toCOBOL-codex/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-revisit-java-toRust-codex/chess-revisit-java-toCOBOL

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.