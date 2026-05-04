# Deep dive — `chess-latex-codex-replication` (chess engine in LaTeX)

_Qualitative addendum. Evidence from `~/SANDBOX/chess-latex-codex-replication/` and the Codex session at `~/.codex/sessions/2026/02/16/rollout-2026-02-16T22-02-21-…jsonl` (plus 7 follow-up sessions Feb 17–18)._

**Scope:** 15 user prompts, 44 PGN game records, $119 of list-price spend, Codex (gpt-5), Feb 2026.

## 1. Why LaTeX is a striking language choice

LaTeX is a document-preparation language whose underlying TeX engine is Turing-complete but exposes computation only through **macro expansion**: tokenizable `\def`-style substitutions operating in the "mouth" phase of TeX's mouth-stomach lifecycle.

For a chess engine this imposes three unusual constraints:

1. **Expansion-only computation.** No mutable variables, no loops in the imperative sense. Iteration is recursive macro redefinition or `\loop…\repeat`.
2. **No native arithmetic at scale.** `\advance` increments counters; everything else is hand-rolled macro math where one addition can expand to 50+ intermediate invocations.
3. **Mouth vs. stomach.** The engine must compute entirely in the mouth (expansion) and emit a single `bestmove.txt` — no intermediate PDF output.

The engine is nonetheless ~1,000 lines of `expl3` macros (`latex_move_picker.tex`) implementing FEN parse, pseudo-legal + legal move generation, depth-1/2 minimax, and static evaluation — driven by a Python UCI wrapper that spawns `pdflatex` once per move.

## 2. PL-ROOT (first substantive prompt)

**Agent:** Codex (gpt-5) — 2026-02-16 21:02 [T:rollout-2026-02-16T22-02-21]

> "I want to build a chess engine in LaTeX programming language."

Expanded to:

> "…I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of 'similar' levels."

**The pivot prompt (Prompt 3 in session):**

> "You have basically 'cheated' in the sense you have used Lua, a rich, general-purpose language. I want a pure implementation in LaTeX with macros…"

**Canonical replay prompt:**

```
Build a chess engine entirely in LaTeX expl3 macros (no Lua, no Python in the
chess-logic path). Requirements:
- FEN parsing and setup; pseudo-legal move generation for all piece types
- Legal move filter with king-in-check detection (castling through check,
  en passant, promotion handled)
- Static evaluation: material + positional bonuses
- Minimax search depth 1 or 2 (selectable)
- UCI wrapper: Python spawns pdflatex per move, reads bestmove.txt
- Elo calibration vs. Stockfish UCI_LimitStrength at Elo 1200, 1350, 1500, 1650
```

## 3. Five illustrative user prompts

| # | Time | Label | Quote (≤25 words) |
|---|---|---|---|
| A | 2026-02-16 21:02 | **capability-level** | "Build a chess engine in LaTeX and assess its Elo rating." |
| B | 2026-02-16 21:25 | **constraint / refactor** | "You have 'cheated' with Lua. I want pure LaTeX macros — legality, search, eval, play." |
| C | 2026-02-16 21:23 | **tooling** | "Create a repo and git commit." |
| D | 2026-02-16 22:18 | **feature / documentation** | "How to use the LaTeX engine in Overleaf — play by editing LaTeX?" |
| E | 2026-02-17 onward | **oracle-invocation** | "Test vs. Stockfish at similar levels; report Elo with confidence intervals." |

Prompt B is the **defining one**: a constraint that reshapes the architecture (no Lua fallback) and forces the agent to implement chess logic purely in macros.

## 4. Agent strategy narrative

### Phase 1 — Feasibility & pure-macro pivot (2026-02-16)

Codex initially offered a Lua-assisted design; the user rejected it (Prompt B). The agent then generated the core `latex_move_picker.tex` in a single pass (~1,000 lines of `expl3`). Data structures:

```latex
\prop_new:N \l__chess_board_prop        % 64 squares: prop[sq_idx] = piece
\seq_new:N \l__chess_pseudo_moves_seq   % pseudo-legal moves
\seq_new:N \l__chess_legal_moves_seq    % post-filter
\tl_new:N  \l__chess_side_tl            % "w" or "b"
\int_new:N \l__chess_best_score_int
\int_new:N \l__chess_search_depth_int
```

Moves are encoded as strings (`e2e4`, `e1g1`, `e5d4`, `e7e8=Q`).

### Phase 2 — UCI wrapper & Overleaf (2026-02-16 →)

`latex_uci_engine.py` parses UCI commands, writes TeX macro definitions, spawns `pdflatex chess.tex` with a 30-second timeout, reads `bestmove.txt`, and answers back to the caller. In parallel, `overleaf/single_file.tex` lets a human play by editing `\MyMovesCSV` and re-compiling.

### Phase 3 — Elo calibration (2026-02-17 →)

`scripts/estimate_elo.py` runs automated matches via `cutechess-cli` at Elo anchors 1200 / 1350 / 1500 / 1650, parses PGN output, and computes per-opponent Elo plus a 95% CI, aggregated with both inverse-variance weighting and a logistic MLE. Convenience launchers: `run_elo_quick.sh`, `run_elo_proper.sh`, `run_elo_best.sh`.

### Phase 4 — Tuning (2026-02-17 onward)

Surfaced tuning parameters:

- `\SearchDepth` 1 or 2 (default 2)
- `\MoveJitter` 0–500 (controlled randomness)
- `\RandomSeed` (reproducibility)
- `--move-time` 8–12 s, `--latex-timeout` 30 s
- `--min-movetime-depth2-ms` 10,500 (auto-fallback to depth-1 in time pressure)

Raising move-time from 8 s to 12 s lifted the aggregate Elo estimate by ~200 points, indicating that the depth-2 budget is the binding constraint, not the static evaluation.

## 5. Engine architecture map

```
User (UCI protocol or Overleaf)
        ↓
latex_uci_engine.py (Python)
        ↓ [write TeX macros to tempdir]
pdflatex (TeX engine)
        ↓ [expand in the mouth]
latex_move_picker.tex (expl3)
        ↓ [compute bestmove, write to file]
bestmove.txt
        ↓ [read back]
UCI output / Overleaf board render
```

| File | Role |
|---|---|
| `engine/latex_move_picker.tex` | ~1,000 lines of `expl3` — the engine itself |
| `engine/latex_uci_engine.py` | ~200 lines — UCI wrapper, pdflatex spawner |
| `scripts/estimate_elo.py` | ~400 lines — Elo testing harness |
| `scripts/run_elo_*.sh` | convenience launchers |
| `overleaf/single_file.tex` | all-in-one Overleaf template |

## 6. Oracle usage + claimed Elo

**Best run — `results/best/best-20260217-205815_elo_summary.json`:**

| Opponent Elo | Games | LaTeX score | Per-opp Elo | CI95 |
|---:|---:|---|---:|---:|
| 1200 | 20 | 1W / 19L | 754.4 | ±288.5 |
| 1350 | 16 | 0W / 16L | 742.6 | ±488.8 |
| 1500 | 24 | 1W / 23L | 1022.0 | ±286.7 |

Aggregates: **inverse-variance 867.4, MLE 826.8**, i.e. an engine in the **~800–900 Elo band** (halfway between Stockfish anchors at 1200 and 1350).

Earlier tuning run (`best-20260217-161218`) with `--move-time 8 s` returned an aggregate ~674 Elo and zero wins across 72 games — the ~200-point delta is what the longer macro-expansion budget bought.

All 60+ games legal (no illegal-move penalties in PGN); castling, en passant, promotion all handled.

## 7. Three quotable findings

1. **Macro-expansion depth is a hard ceiling.** Depth-2 minimax at ~40 moves/ply approaches pdflatex's token-expansion limits; going to depth-3 is likely infeasible without changing the TeX dialect (which the user explicitly forbade). [R:engine/latex_move_picker.tex, L:results/best/best-20260217-205815_elo_summary.json]
2. **Three-pass legality works across macro boundaries.** King safety, destination safety, and check detection are encoded as nested macro token lists; 60 rated games vs. Stockfish produced **zero** illegal moves. Declarative substitution can encode complex conditional logic. [R:engine/latex_move_picker.tex]
3. **The Elo gap between depth-1 and depth-2 is modest (~150 Elo).** The engine is bottlenecked by shallow horizon, not by evaluation quality. Reaching 1400+ would need depth-3, which the language makes impractical. [L:results/best/*.json — 674 Elo @ 8 s → 867 Elo @ 12 s]

## 8. Reproducibility notes

| Artifact | Location | Status |
|---|---|---|
| Codex sessions | `~/.codex/sessions/2026/02/{16,17,18}/rollout-*.jsonl` | 8 relevant sessions preserved |
| Source | `engine/`, `scripts/`, `overleaf/` | in-tree |
| PGN runs | `results/` | 44 files, in-tree |
| Elo summaries | `results/best/*.json`, `results/*.csv` | in-tree |
| Git | `.git/` | 20+ commits |

**Replay quick-path:**

```bash
# smoke test
printf 'uci\nisready\nposition startpos\ngo\nquit\n' \
  | python3 engine/latex_uci_engine.py

# short match
cutechess-cli \
  -engine name=latex cmd=python3 arg=engine/latex_uci_engine.py \
  -engine name=sf1320 cmd=stockfish \
    option.UCI_LimitStrength=true option.UCI_Elo=1320 \
  -each proto=uci st=0.5 -games 2 -rounds 1 -repeat -concurrency 1

# full 3-hour Elo run
python3 scripts/estimate_elo.py --games-per-opponent 24 \
  --move-time 12.0 --latex-timeout 30 --out-dir results/custom_run
```

## Paper takeaway (for §"language matters")

LaTeX and Brainfuck sit at opposite ends of the constraint spectrum: LaTeX has rich declarative macros but no runtime loops; Brainfuck has a trivial imperative core but no data types. Both reach a working chess engine, and both bottom-out at **depth ≈2–3** search — the language's execution model, not the chess knowledge the LLM brings, is what caps playing strength. LaTeX's ceiling is macro-expansion depth; Brainfuck's is 64-way array-access cost. Neither ceiling is about whether the model "knows chess".
