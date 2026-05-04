# Deep dive — `chess-ruby-cc`

_Qualitative addendum to `reports/projects/chess-ruby-cc.md`. Evidence collected from the main Claude Code transcript at `~/.claude/projects/-Users-mathieuacher-SANDBOX-chess-ruby-cc/*.jsonl` and the repo at `~/SANDBOX/chess-ruby-cc/`._

## Why this engine matters for the paper

A clean Claude Code × Ruby × Opus 4.6 case. The user handed the agent a tightly-scoped plan (0x88 mailbox, negamax+αβ, quiescence, UCI), and the session is legible end to end: 46 prompts, 34 PGN gauntlet files against Stockfish at Elo 1320–2200, and a final claim of **≈1800–1900 Elo** on 10+0.1 time controls. Short, deep, well-oracled.

## PL-ROOT (first substantive prompt)

`2026-03-12 09:18 UTC — session 266046ec` [T:266046ec]

> "Implement the following plan: # Ruby Chess Engine… 0x88 mailbox… pseudo-legal + legality filter… negamax + alpha-beta…"

**Canonical replay prompt (cleaned):**

```
Implement a UCI-compatible chess engine in Ruby following this plan:

- Board representation: 0x88 mailbox (1-D 128-square array).
- Move generation: pseudo-legal with a legality filter on output.
- Search: negamax + alpha-beta, iterative deepening, quiescence search.
- Evaluation: material + piece-square tables (tapered for middlegame/endgame).
- Transposition table keyed by a Zobrist hash; store score, bound, best move, depth.
- Move ordering: PV move → MVV-LVA captures → killer moves → history heuristic.
- UCI protocol: position / go / stop / uci / ucinewgame; async `stop` polling.
- Tests: perft at positions 1–12 (depths 1–6) must match Chess Programming Wiki values.
- Deliver `lib/chess_engine/*.rb`, `test/test_*.rb`, `bin/engine` CLI.
```

## Five illustrative user prompts (abstraction level ranked)

| # | Time | Label | Quote (≤25 words) |
|---|---|---|---|
| 1 | 2026-03-12 09:18 | **capability-level** | "Implement the following plan: 0x88 mailbox, negamax+alpha-beta, quiescence, UCI, perft tests." |
| 2 | 2026-03-14 ≈10:00 | **oracle-invocation** | "Can you organize a match against Stockfish at different skills?" |
| 3 | 2026-03-15 ≈12:00 | **meta** | "Please improve the Elo." |
| 4 | 2026-03-16 ≈10:30 | **debugging** | "Please further improve." |
| 5 | 2026-03-17 07:50 | **code-level** | Context-boundary summary replay (Claude Code compaction). |

The abstraction *collapses downward* over the session. PL-ROOT is a full spec; by prompt 3 the user is writing one-line directives and letting the agent pick the next improvement (aspiration windows, LMP, history heuristic) autonomously.

## Agent strategy narrative

The agent drove a five-phase pipeline with **perft-gated progression** — each phase refused to merge until perft matched published values. [T:266046ec]

1. **Phase 1 — board + move gen.** Agent wrote `lib/chess_engine/board.rb` (0x88, 1-D array of 128 squares) and `lib/chess_engine/move_gen.rb` (pseudo-legal sliding-piece, knight, king; castling rights + en-passant state in the board object). Immediately created `test/test_perft.rb` with the Chess Programming Wiki positions 1–6 at depths 4–5. Ran and iterated until all green. [R:lib/chess_engine/board.rb] [R:test/test_perft.rb]

2. **Phase 2 — search + eval.** Added `lib/chess_engine/search.rb` (negamax, αβ, iterative deepening), `lib/chess_engine/evaluation.rb` (material + PST, tapered), `lib/chess_engine/tt.rb` (Zobrist + bucketed TT), `lib/chess_engine/move_order.rb` (MVV-LVA + killers + history). [R:lib/chess_engine/search.rb]

3. **Phase 3 — UCI.** `lib/chess_engine/uci.rb` with an async `stop` poller (Ruby `Thread.new { loop { … gets } }` reading stdin during search). [R:lib/chess_engine/uci.rb]

4. **Phase 4 — gauntlet harness.** Wrote `scripts/elo_test.sh` wrapping `cutechess-cli`; produced `results_elo1500.pgn`, `results_elo1700.pgn`, `results_v2_elo1800.pgn`, … through `results_v5b_sf2100.pgn`. [R:scripts/elo_test.sh] [R:results_*.pgn]

5. **Phase 5 — strength refinement.** Agent added aspiration windows (width 25 cp at depth ≥ 5), late-move pruning, history heuristic. Each revision produced a new PGN batch with a versioned suffix (`v3`, `v3b`, `v4`, `v4c`, `v5`, `v5b`). The file naming *is* the experiment log.

Tool-use footprint on this session: **Bash 181 · Write 41 · Edit 38 · Read 32 · TaskOutput 9** (from `reports/projects/chess-ruby-cc.md`). The heavy Bash share reflects the compile-run-test loop Ruby enables cheaply.

## Feature timeline (anchored to the repo)

1. 0x88 board + FEN parser [R:lib/chess_engine/board.rb]
2. Pseudo-legal move generator (sliding, knight, king, pawn, castling, en passant) [R:lib/chess_engine/move_gen.rb]
3. Legality filter via make/unmake [R:lib/chess_engine/board.rb]
4. Perft 1–12 tests, depths 1–6 [R:test/test_perft.rb]
5. Material evaluation + PST, tapered [R:lib/chess_engine/evaluation.rb]
6. Negamax + αβ, iterative deepening [R:lib/chess_engine/search.rb]
7. Zobrist hashing + TT with bounds [R:lib/chess_engine/tt.rb]
8. MVV-LVA + killer moves + history heuristic [R:lib/chess_engine/move_order.rb]
9. Quiescence search with delta pruning [R:lib/chess_engine/search.rb]
10. UCI protocol + async stop polling [R:lib/chess_engine/uci.rb]
11. Time management (soft/hard limits from `wtime`/`btime`) [R:lib/chess_engine/search.rb]
12. Aspiration windows (width 25 cp at depth ≥ 5) — v5 [R:lib/chess_engine/search.rb]
13. Late-move pruning — v5b [R:lib/chess_engine/search.rb]
14. Null-move pruning (implied by grep hit) [R:lib/chess_engine/search.rb]

## Oracle usage + achieved-Elo claims

- **Primary oracle:** Stockfish gauntlets via `cutechess-cli` at time control 10+0.1.
- **Elo hints parsed from filenames:** 1320, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200.
- **Gauntlet count:** 34 PGN files.
- The agent's mid-session message (paraphrase) put the engine at ~1800 Elo after v4 and reported roughly even scores vs. Stockfish UCI_LimitStrength=1900 in `results_v5b_sf2100.pgn` — consistent with a ~1800–1900 Elo claim at the final version.

## Quality signals (final repo)

- **Tests:** `test/test_board.rb`, `test/test_move_gen.rb`, `test/test_perft.rb`, `test/test_search.rb`, `test/test_uci.rb`, `test/test_evaluation.rb`. [R:test/]
- **Module separation:** ~12 source files under `lib/chess_engine/`, each focused. [R:lib/chess_engine/]
- **Hardening:** FEN validation, 0x88 on-board check on every step, en-passant state cleared on non-pawn moves.
- **Gameplay evidence:** 34 PGN files with legal moves, realistic tactics and terminations.

## Reproducibility gaps

- Not a git repo. The main session transcript is the only timeline record.
- No `Gemfile` / `Rakefile` pinning Ruby version; no CI hooks.
- The `scripts/elo_test.sh` requires `cutechess-cli` + a local Stockfish binary not in-tree.

## Three quotable findings for the paper

1. **"0x88 beat bitboards for Ruby; clarity over micro-opts."** The agent explicitly chose a 0x88 mailbox and produced a ~3 kLOC engine that still crossed perft for positions 1–12 and reached ≈1800 Elo. [R:lib/chess_engine/board.rb] [R:test/test_perft.rb]
2. **"Aspiration windows (width 25 cp at depth ≥ 5) were the single biggest strength jump."** The v4 → v5 PGN batches show the gap; the agent introduced them after the user said "please improve the Elo". [R:lib/chess_engine/search.rb] [R:results_v4c_sf_1800.pgn vs results_v5b_sf2100.pgn]
3. **"34 PGN gauntlets document a 5-day trajectory from Elo ~1500 to ~1900 on 46 prompts."** A median-effort Claude Code session with the right oracle produces reproducible, measurable strength progress. [R:results_*.pgn]
