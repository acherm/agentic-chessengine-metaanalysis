# Deep dive — `chess-brainfuck-cc` (chess engine in Brainfuck)

_Qualitative addendum. Evidence from `~/SANDBOX/chess-brainfuck-cc/` and the Claude Code transcripts under `~/.claude/projects/-Users-mathieuacher-SANDBOX-chess-brainfuck-cc/` plus the Codex sessions that reference the same path under `~/.codex/sessions/`._

**Scope:** 58 user prompts, 19 PGN game records, $160 of list-price spend, Claude Code + Codex, Feb–Mar 2026.

## 1. Why Brainfuck is a striking language choice

Brainfuck is an esoteric Turing-complete language with a 30,000-cell tape and **eight** instructions: `>` `<` `+` `-` `.` `,` `[` `]`. No data types. No functions. No named variables. Every computation — addition, comparison, branching, board indexing — is built from pointer arithmetic and cell loops.

For a chess engine, three constraints dominate:

1. **No random access.** Reading `board[i]` where `i` is a runtime value needs a **64-way switch**: compare `i` against 0, 1, …, 63 and copy the matching cell. Inside a minimax tree this multiplies wildly.
2. **No arithmetic.** Summing material or scoring moves is a hand-rolled increment/decrement loop with scratch cells.
3. **Single 8-bit cell memory.** Cells wrap at 256; state has to be laid out by hand so search levels don't stomp on each other.

The finished program is a **~5.6 MB `chess.bf` file** that embeds an entire chess rule set and depth-3 minimax — a maximally simple language forced to encode combinatorial complexity.

## 2. PL-ROOT (first substantive prompt)

**Agent:** Claude Code (subagent) — 2026-02-21 16:55 [T:agent-a7]

> "Research the feasibility of building a chess engine in Brainfuck. I need to understand: What compilers, interpreters, constraints exist?"

**Canonical replay prompt:**

```
Build a complete UCI chess engine in Brainfuck. Requirements:
- Full move generation (all piece types, castling, en passant, promotion)
- Legal move filtering (king-safety check)
- Minimax search depth ≥ 2, MVV-LVA move ordering
- UCI protocol support (uci, isready, position, go, quit)
- Target: playable strength (~200–400 Elo) on standard hardware
```

The user explicitly instructed: **write BF directly, do not transpile from C.** Use Python as a *code generator* that emits BF at compile time.

## 3. Five illustrative user prompts (abstraction range)

| # | Time | Label | Quote (≤25 words) |
|---|---|---|---|
| A | 2026-02-21 17:08 | **capability-level** | "Write BF directly, target ~200 Elo, use Python to generate the BF code dynamically." |
| B | 2026-02-23 17:00 | **debugging / code-level** | "Engine played h5h3 (moving BLACK's rook) when it was WHITE's turn. FEN: …" |
| C | 2026-02-22 13:05 | **meta** | "Create a detailed summary of the conversation so far — context is near limits." |
| D | 2026-02-24 12:34 | **oracle-invocation** | "How would you estimate Elo vs. random legal moves and vs. Stockfish?" |
| E | 2026-02-26 16:12 | **debugging** | "Illegal-move bug when Stockfish plays underpromotion `f7f8r` (pawn to rook)." |

The arc starts *high-level* (PL-ROOT: "is this feasible?") → quickly descends to **code-level debugging** with exact FENs and move strings → punctuated by **meta** prompts where Claude Code's own context limits force summarize-and-handoff. Unlike Ruby-cc, the user had to engage with the BF-specific pathology.

## 4. Agent strategy narrative

### Phase 1 — Feasibility & architecture (2026-02-21)

The agent surveyed BF compilers/interpreters (bf-cc, awib, c2bf) and pivoted to **bottom-up Python code generation** rather than C→BF transpilation. The Python modules are split by concern:

- `bf_emitter.py` — pointer-tracking BF code generator
- `bf_memory.py` — static tape layout
- `bf_primitives.py` — control-flow macros (compare_eq, if_else, switch)
- `bf_chess.py`, `bf_movegen.py`, `bf_uci.py` — chess logic
- `generate.py` — orchestrator

**Evidence:** [R:generate.py] is the entry point assembling modules into the single `chess.bf` output.

### Phase 2 — Memory layout (2026-02-22)

The agent fixed a tape layout that is the engine's contract:

| Cells | Purpose |
|---|---|
| 0–15 | scratch temporaries |
| 16–22 | game state |
| 30–93 | 64-square board |
| 100–227 | stdin buffer |
| 160–183 | depth-2 and depth-3 search state |
| 400–671 | board backups for unmake |

A misaligned cell write silently corrupts the whole engine.

### Phase 3 — Move generation + legality (2026-02-23)

Three-pass: (1) pseudo-legal generation, (2) make, (3) is-king-attacked check, then unmake. The color-boundary bug surfaced here — castling state was not reset between search levels.

### Phase 4 — Search + evaluation (2026-02-24 →)

Depth-3 minimax with αβ; move scoring = MVV-LVA + positional bonuses (center, advancement, rook-on-7th, check detection). Stockfish (UCI_Elo=1320) became the oracle; random-move player was the baseline.

## 5. Engine architecture map

```
User (UCI protocol)
        ↓
    bf_uci.py (Python)    [Dispatch: uci, isready, position, go]
        ↓
    chess.bf (Brainfuck)  [Move generation, search, evaluation]
        ↓
    bfi (C interpreter)   [RLE + jump tables]
```

Python is a **host driver**, not a chess-logic cheat: `bf_uci.py` parses UCI commands, writes the `position` line to `chess.bf`'s stdin, reads the `bestmove …` line back from stdout.

Key file sizes:

| File | LOC | Role |
|---|---:|---|
| `bf_movegen.py` | ~3,900 | pseudo-legal gen, legality, search |
| `bf_chess.py` | ~400 | board init, FEN, move application |
| `bf_primitives.py` | ~150 | compare_eq, if_else, switch macros |
| `chess.bf` | 5.6 MB | final compiled BF program |
| `bfi.c` | ~180 | interpreter with RLE + jump tables |

## 6. Oracle usage + claimed Elo

**Oracle A — Stockfish @ UCI_Elo 1320, 120+1s time control (CCRL calibration).** 10 games, 0 wins, 10 losses (all by checkmate). Engine time/move: 45–600s. Interpretation: depth-3 search is insufficient; Stockfish punishes every positional slip with tactics BF cannot see.

**Oracle B — random legal moves.** 10 games, 4 wins, 6 draws (stalemate), 0 losses. 70% score.

**Stated strength [R:ASSESSMENT.md]:**

> "vs. Stockfish 1320: 0% (0/10)"  
> "vs. Random: 70% (4W/6D/0L)"  
> "Strength summary: ~100–200 Elo"

**Perft:** the README claims 11/11 positions passing — the engine is rule-compliant at the head of the tree.

## 7. Three quotable findings

1. **Random-access cost drives branching factor.** Every board[i] access inlines as a 64-way switch; the 3,900-line `bf_movegen.py` emits ~5.6 MB of BF for what C does in 50–100 kB. Engine takes 45–600 s/move against Stockfish's <1 s, making timed play infeasible without depth cuts. [R:chess.bf size, bf_movegen.py]
2. **Stalemate detection works only within the search horizon.** 6 of 10 games against random end in stalemate after BFChess wins material: the depth-3 eye can't see the 5-move sequence that locks the opponent's king. [R:ASSESSMENT.md]
3. **Color-boundary bug reveals global-memory fragility.** A missed cell reset in unmake caused the engine to play Black's rook on White's turn. In a language with no scope and no type safety, one misaligned write corrupts the whole search tree. [Prompt B]

## 8. Reproducibility notes

Claude Code main sessions + subagent transcripts survive at `~/.claude/projects/-Users-mathieuacher-SANDBOX-chess-brainfuck-cc/`, and at least one Codex rollout references the repo path. Python source + PGN files + `chess.bf` + `bfi.c` survive on disk; rebuilding is `make clean && make` (runs `python3 generate.py`). Stockfish binary is required but not vendored.

**Gap:** at least one main-transcript UUID is referenced by `sessions-index.json` but absent from disk (Claude Code compaction); subagent transcripts cover the gap for strategy narration, but token counts under-report the total interaction.
