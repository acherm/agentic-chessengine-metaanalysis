# Deep dive — `chess-cobol-cc`

_Qualitative addendum to `reports/projects/chess-cobol-cc.md`. Evidence from the main Claude Code transcript at `~/.claude/projects/-Users-mathieuacher-SANDBOX-chess-cobol-cc/9d9bb74e-18ea-4bb9-844c-b4e175998988.jsonl` (≈28 MB, ≈3,700 events), the 7 subagent transcripts alongside it, and the repo at `~/SANDBOX/chess-cobol-cc/`._

## Why this engine matters for the paper

The **most expensive engine in the corpus** at ~$518 of list-price spend — and a good test of the "language matters" claim. COBOL forces verbose block structure (`PERFORM`, `DISPLAY`, 01-level records), compiles through GnuCOBOL into C, and is not the kind of language LLMs see every day. Yet the agent produced a running UCI engine that plays gauntlets against Stockfish and claims ~1600 Elo mid-session. Small session footprint (46 user prompts) but enormous tool activity.

## PL-ROOT (first substantive prompt)

`2026-03-12 19:37 UTC — session 9d9bb74e` [T:9d9bb74e]

> "I want to build a chess engine in COBOL (using GNU Cobol)… assess its Elo rating."

**Canonical replay prompt:**

```
Build a UCI-compatible chess engine in COBOL, targeting GnuCOBOL 3.x on macOS,
and assess its Elo rating against Stockfish under skill-limited play. Work in
phases and ask for my go-ahead before advancing:

  Phase 1. Board representation + move generation (no search).
  Phase 2. FEN parsing, UCI I/O loop, smoke games vs. Stockfish.
  Phase 3. Alpha-beta + iterative deepening + quiescence.
  Phase 4. Move ordering (MVV-LVA), time management, evaluation tuning.
  Phase 5. Elo measurement via cutechess-cli gauntlets.

Use GnuCOBOL's compile-to-C pipeline. Version final binaries v1, v2, ….
```

## Five illustrative user prompts

| # | Time | Label | Quote (≤25 words) |
|---|---|---|---|
| 1 | 2026-03-12 19:37 | **capability-level** | "Build a chess engine in COBOL (GNU Cobol)… assess its Elo rating." |
| 2 | 2026-03-12 late | **meta** | "Let's go for Phase 1." |
| 3 | 2026-03-13 | **meta** | "Go to Phase 2." |
| 4 | 2026-03-14 | **meta** | "Go." |
| 5 | 2026-03-16 onwards | **oracle-invocation** | "Please go ahead and try to improve the Elo." |

The user's **abstraction level stays above the code** almost entirely. The 46 prompts are dominated by `go`, `continue`, `yes`, and "improve Elo" — the agent drives virtually every technical choice. The session stress-tests a hypothesis: can a single high-level spec plus minimal steering produce a working COBOL chess engine?

## Agent strategy narrative

A strict **phased build with minimal user steering**:

- **Phase 1 (board + movegen).** COBOL `01 BOARD-TABLE OCCURS 64 TIMES PIC X` for the 8×8 squares, `88`-level condition names for piece codes, `PERFORM VARYING … UNTIL` loops for generation. The agent wrote ~3,460 LOC of COBOL in `chess-engine.cob`, compiled to C via `cobc -C`, then to native via `cobc -x`. The one-pass compile produced `chess-engine.c` of ~8,100 LOC (auto-generated; accounts for why `reports/projects/chess-cobol-cc.md` classifies "C" as primary LOC). [R:chess-engine.cob] [R:chess-engine.c]
- **Phase 2 (FEN + UCI).** Added FEN parsing using COBOL `INSPECT`/`UNSTRING`, a UCI loop with `ACCEPT FROM CONSOLE`, and first smoke games vs. Stockfish. [R:chess-engine.cob §FEN-PARSE] [R:chess-engine.cob §UCI-LOOP]
- **Phase 3 (search).** Alpha-beta, iterative deepening, quiescence — each implemented as its own COBOL paragraph, recursion simulated via an explicit stack table (COBOL has no recursion by default). [R:chess-engine.cob §NEGAMAX]
- **Phase 4 (ordering + time).** MVV-LVA ordering via a small sort paragraph; time budget derived from UCI `wtime`/`btime`. [R:chess-engine.cob §MOVE-ORDER]
- **Phase 5 (Elo).** Generated `chess-engine-v1` → `chess-engine-v4b`, plus optimization variants `chess-engine-fast`, `-o1`, `-o3`, `-noopt`, `-dbg`. Each binary played gauntlets; PGN files were produced per skill level. [R:chess-engine-v* binaries] [R:elo_vs1400.pgn] [R:elo_vs1700.pgn]

Tool footprint on this session: heavy Bash + Write use. The JSONL is ≈28 MB because the agent pasted entire COBOL source blocks across turns. Seven subagent transcripts under `9d9bb74e-18ea-4bb9-844c-b4e175998988/subagents/` indicate Claude Code's auto-compaction fired repeatedly — the session was context-bound.

## Feature timeline

1. COBOL skeleton + `IDENTIFICATION DIVISION`, `DATA DIVISION` board table [R:chess-engine.cob]
2. Move encoding (`01 MOVE-REC …`), move-list table
3. Pseudo-legal move gen for each piece (explicit paragraphs)
4. Make/unmake with state snapshot in a history table
5. Perft harness (CALLable from a test driver)
6. FEN parsing (INSPECT/UNSTRING)
7. UCI I/O loop (ACCEPT/DISPLAY)
8. Material + basic PST evaluation
9. Negamax + αβ with a software call stack
10. Iterative deepening + time check
11. Quiescence with delta pruning
12. MVV-LVA move ordering
13. Compilation pipeline (cobc → C → native)
14. Optimization variants (`-O1`, `-O3`, `-fast`, `-dbg`)
15. cutechess-cli gauntlets vs. Stockfish UCI_LimitStrength 1400/1600/1700

## Oracle usage + claimed Elo

- **Oracle:** Stockfish `UCI_LimitStrength` with `UCI_Elo` values 1400, 1600, 1700 (file names `elo_vs1400.pgn`, `elo_vs1600.pgn`, `elo_vs1700.pgn`).
- **PGN evidence:** 25 PGN files in the repo with legal, typical-looking games including mate sequences and piece trades.
- **Claim:** a mid-session agent message put the engine at **~1627 Elo** after Phase 4 optimization. The final v4b binary is the most recent artifact.
- **Perft:** the agent wrote perft and printed per-depth node counts during Phase 1, though the repo-level perft-literal grep finds zero matches — perft values were displayed at runtime, not committed as test fixtures.

## Quality signals

- **Source organization:** `chess-engine.cob` is a single 3,460-LOC file with ~8 named sections. COBOL doesn't reward per-file splitting; the section names (`WORKING-STORAGE`, `BOARD-OPS`, `MOVE-GEN`, `SEARCH`, `EVAL`, `UCI`) are the de-facto modules.
- **PERFORM/DO density:** ~811 `PERFORM` statements in the source — extreme control-flow verbosity compared to the same functionality in Python (`chess-py-cc`: ~3k LOC, negligible explicit loops).
- **Binaries:** 10 compiled variants (`chess-engine`, `-fast`, `-o1`, `-o3`, `-os`, `-noopt`, `-dbg`, `-v1`, `-v2`, `-v3`, `-v4`, `-v4b`). Suggests the agent benchmarked strength *and* performance.
- **Generated C:** `chess-engine.c` is preserved, i.e. the pipeline is inspectable.

## Reproducibility gaps

- Not a git repo. The 28 MB JSONL transcript is the only authoritative timeline.
- No Makefile or CI; build commands live inside the transcript and in agent memory.
- 7 subagent transcripts indicate compaction events — the main transcript has condensed summaries at context boundaries, so earlier reasoning is partly compressed.

## Three quotable findings for the paper

1. **"COBOL's verbose block structure produced ~3.5 kLOC of engine source with ≈811 `PERFORM` statements — the language's grammar drove granularity."** [R:chess-engine.cob]
2. **"The agent bridged a legacy language to modern chess via a C-intermediate: GnuCOBOL → 8.1 kLOC of auto-generated C → a 108 kB UCI binary."** [R:chess-engine.c] [R:chess-engine binary]
3. **"Minimal user steering (many 'go'/'continue' prompts) and one capability-level goal produced an Elo ≈1600 engine for ~$518 of agent spend — expensive because seven subagent compactions fired."** [T:9d9bb74e subagents/]
