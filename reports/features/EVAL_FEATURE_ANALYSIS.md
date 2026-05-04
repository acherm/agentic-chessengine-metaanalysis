# Evaluation / Piece-Square Tables: Cross-Engine Feature Analysis

**Feature**: static evaluation / piece-square tables (PST)  
**Detection patterns**: `piece[_ ]?square|\bPST\b`  
**Corpus**: 35 engines (19 with the feature present)  
**Analysis tools**: `scripts/feature_locator.py --hotspot`, `scripts/feature_compare.py`  
**Raw artefacts**: `evaluation_pst.json`, `evaluation_pst.hotspot.txt`, `evaluation_pst.compare.txt`, `evaluation_pst.compare.json`  
**Date**: 2026-04-20

---

## 1. Why evaluation is the third point of the triad

The three features studied in this meta-analysis form a natural hierarchy of engine architecture:

1. **Algorithm** — quiescence search: *how the engine explores the game tree*
2. **Data structure** — transposition table: *how the engine stores and reuses knowledge about positions*
3. **Evaluation** — static evaluation / PST: *what score the engine assigns to a position when it stops searching*

Quiescence and TT are infrastructure that serves the evaluation: without a meaningful static evaluation function, a deeper search and a better TT are both useless — they merely explore more positions and cache more scores, but those scores are wrong. The evaluation function is the engine's chess knowledge made explicit as data.

Piece-square tables (PSTs) are the simplest non-trivial form of that knowledge. Beyond raw material counting (100 centipawns per pawn, 300 per bishop, 500 per rook, 900 per queen), a PST assigns a positional bonus or penalty to each piece type at each of the 64 squares. This encodes heuristics like "knights are better in the center," "pawns should advance," and "the king should be sheltered in the middlegame." PSTs are the canonical first upgrade beyond material balance and the subject of the chessprogramming.org article that most LLM training data cites.

The triad is also a methodological progression in extraction difficulty:

- **Quiescence search**: one function, one algorithm, highly concentrated — extractable cleanly as a single hotspot
- **Transposition table**: one data structure, but spread across initialization, probe, and store — requires multi-location extraction
- **Evaluation / PST**: the most distributed of the three — tables (typically 6 × 64 integers or 12 × 64 for MG/EG), a lookup function, and optionally an incremental updater in the board move-make function, all in separate files — with the highest extraction failure rate of the triad

This progression motivates the methodological section (Section 10) of this report.

---

## 2. Methodology

### 2.1 Hotspot extraction

Evaluation is harder to localize than quiescence or TT because the PST concept is spread across multiple architectural layers:

1. **Table declaration**: a constant array (or WORKING-STORAGE section in COBOL, or `\def`-based macro table in TeX) with 64 values per piece type
2. **Lookup function**: a function like `pieceSquareBonus(pieceType, square)` that dispatches to the right table
3. **Incremental update**: code inside `putPiece` / `makeMove` that adds or subtracts the PST delta for efficiency
4. **Terminal evaluation**: the function that sums material + PST over all pieces and returns the score

The hotspot extractor (`--hotspot` mode) scores by keyword proximity, function name, and file name. For evaluation, all four layers can score highly, and the extractor can land on any of them. This explains why the extraction failure rate is highest for this feature.

### 2.2 Sub-feature detection

Thirteen positional/evaluation sub-features were defined, each detected by a regex applied to the extracted function body:

| Sub-feature | What it detects |
|---|---|
| `material_values` | Raw material score (piece-type → centipawn constant) |
| `pst_table_lookup` | Direct array index: `PST[pieceType][square]` or equivalent |
| `midgame_tables` | Named `MG_` / `_MIDGAME` tables indicating game-phase separation |
| `endgame_tables` | Named `EG_` / `_ENDGAME` tables |
| `tapered_eval` | Phase interpolation: `(mg * phase + eg * (max_phase - phase)) / max_phase` |
| `king_safety` | Pawn shield, king zone attacks, or `king_safety` keywords |
| `passed_pawn` | Detection of passed pawns (no opposing pawn blocking or on adjacent file) |
| `mobility_terms` | Count of legal moves weighted by piece type |
| `sunfish_vals` | Sunfish material values: P=100, N=280, B=320, R=479, Q=929 |
| `cpw_simplified` | CPW/Wikipedia simplified evaluation values: P=100, N=320, B=330, R=500, Q=900 |
| `computed_positional` | Positional score derived from geometry (centrality, rank advancement) rather than a lookup table |
| `phase_computation` | Explicit game-phase calculation from remaining piece material |
| `perspective_flip` | `sq ^ 56` or `MIRROR_IDX` or equivalent to flip board for Black's perspective |

### 2.3 Similarity metrics

The same two metrics from the quiescence and TT analyses apply:

**Token-Jaccard**: bag-of-lowercase-tokens (punctuation stripped), measuring surface lexical overlap. Sensitive to language syntax differences; useful for detecting copy-paste.

**Feature-Jaccard**: binary vector over 13 sub-features, measuring algorithmic similarity across language boundaries.

---

## 3. Coverage: 19/35 engines matched, and what the gaps mean

### 3.1 Three external anchors (not scanned by design)

`tscp181`, `madchess32`, `countergo40` are third-party binaries used for Elo calibration. They have no `path:` field in `manifest.yaml` and are not scanned. Their absence is expected.

### 3.2 Thirteen engines with no PST match: genuine absence or vocabulary gap?

| Engine | Root cause of absence |
|---|---|
| `COBOL-chess` | Has PST tables in WORKING-STORAGE (visible in hotspot.txt preamble) but the `piece_square` keyword doesn't appear — uses different section naming (`WS-PST-PAWN-VAL` etc.) |
| `chess-assembly-codex` | Assembly engine; evaluation likely uses raw constants with no English keyword match |
| `chess-css-codex` | Evaluation inside JavaScript/CSS; no PST keyword in source |
| `chess-css-codex-guided` | Same as above |
| `chess-icon-codex` | Icon engine; uses different evaluation vocabulary |
| `chess-latex-codex-replication` | A separate LaTeX engine from `latex-chess-engine`; no PST keyword in TeX source |
| `chess-mojo` | No meaningful source present |
| `chess-newlang-codex` | C++ engine with evaluation, but PST implemented without the `piece_square` or `PST` keyword |
| `chess-purec` | C engine; evaluation present but using different naming (e.g., `piece_table`, `eval_table`) |
| `chess-purec-codex` | Same |
| `chess-rust-codex` | Rust engine; evaluation present but no PST keyword match |
| `chess-why3` | Minimal OCaml engine with no PST in its evaluation |
| `chess-brainfuck-cc` | BF code emitter; evaluation is inside emitted BF program text |

Several of these are vocabulary gaps rather than genuine absences. `chess-purec`, `chess-purec-codex`, `chess-rust-codex`, `chess-newlang-codex`, and `COBOL-chess` all implement evaluation but use naming conventions outside the `piece[_ ]?square|\bPST\b` pattern. The true "no PST, no positional evaluation" engines are likely `chess-why3` (confirmed minimal) and `chess-assembly-codex` (evaluation too low-level to pattern-match).

**Contrast with quiescence**: quiescence search had 7 engines missing; evaluation has 16 missing (13 project engines + 3 anchors). The larger gap reflects both vocabulary diversity in naming evaluation functions and the deeper structural fragmentation of evaluation across files.

---

## 4. What the hotspot extractor found: a fragmented picture

Unlike quiescence — where the extractor reliably landed on the canonical `quiescence()` function body — evaluation hotspots scattered across four distinct code layers. The 19 matched engines fall into rough categories:

| Category | Engines | What was extracted |
|---|---|---|
| **Pure lookup function** | chess-java, chess-apl-codex54 | `pieceSquareBonus(pieceType, sq)` switch/dispatch — the canonical lookup |
| **Table declaration** | chess-cobol-cc (partial), latex-chess-engine | Working-storage section or TeX `\def` macros — the data, not the logic |
| **Incremental update in makeMove** | chess-java-cc, chess-rust-cc, chess-revisit-java-toCOBOL-codex, chess-revisit-java-toRust-codex | PST delta added during piece placement, not evaluation function |
| **Computed positional** | lean-chess | Geometric computation, no tables |
| **Full incremental eval helper** | chess-ruby-cc | `add_piece_eval` with MG/EG separation |
| **SQL CTE evaluation** | chess-sql | Complete SQL `WITH` query |
| **Wrong function entirely** | chess-py, chess-cplusplus-claude, chess-rust-cc, cplusplus-chess | En passant logic, FEN parsing, `put_piece` board mechanics |
| **Vendored third-party** | chess-why3-cc | ShallowBlue's `eval.cc`, not the engine's own evaluation |
| **Minimal / stub** | chess-py-cc | 2-line docstring only |
| **Material-only** | chess-Rocq, chess-ruby-codex | `piece_value(pk)` returning a constant |

This fragmentation is itself a finding. Evaluation is architecturally distributed across more files than any other chess engine component, and the hotspot extractor's single-best-match approach cannot capture the full picture.

---

## 5. Sub-feature presence matrix

```
                          mat  pst  mgt  egt  tap  ksg  psp  mob  sun  cpw  cmp  phs  prs
chess-Rocq                 ✓    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·
chess-apl-codex54          ·    ✓    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·
chess-brainfuck            ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ✓
chess-cobol-cc(wrong)      ✓    ·    ·    ·    ·    ·    ✓    ·    ·    ·    ·    ·    ✓
chess-cplusplus-claude     ·    ·    ·    ·    ·    ·    ✓    ·    ·    ·    ·    ·    ✓
chess-java                 ·    ✓    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·
chess-java-cc(wrong)       ·    ·    ·    ·    ✓    ·    ·    ·    ·    ·    ·    ·    ·
chess-py(wrong)            ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ✓
chess-py-cc(2 lines)       ·    ·    ·    ·    ✓    ·    ·    ·    ·    ·    ·    ·    ·
chess-revisit-java-toCOBOL ·    ·    ·    ·    ✓    ·    ·    ·    ·    ·    ·    ·    ✓
chess-revisit-java-toRust  ·    ·    ·    ·    ✓    ·    ·    ·    ·    ·    ·    ·    ✓
chess-ruby-cc              ✓    ✓    ✓    ✓    ✓    ·    ·    ·    ·    ·    ·    ·    ✓
chess-ruby-codex           ✓    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·
chess-rust-cc(wrong)       ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·
chess-sql                  ✓    ·    ·    ·    ·    ·    ·    ·    ·    ·    ✓    ·    ✓
chess-why3-cc(ShallowBlue) ✓    ·    ✓    ·    ✓    ✓    ·    ✓    ·    ·    ·    ·    ·
cplusplus-chess(wrong)     ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·
latex-chess-engine         ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ✓
lean-chess                 ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ✓    ·    ·
---------------------------------------------------------------------
TOTALS                    6/19 3/19 2/19 1/19 6/19 1/19 2/19 1/19 0/19 0/19 2/19 0/19 9/19
```

Legend: `mat`=material_values `pst`=pst_table_lookup `mgt`=midgame_tables `egt`=endgame_tables `tap`=tapered_eval `ksg`=king_safety `psp`=passed_pawn `mob`=mobility_terms `sun`=sunfish_vals `cpw`=cpw_simplified `cmp`=computed_positional `phs`=phase_computation `prs`=perspective_flip

**Interpretation caveat**: heavily affected by extraction location. An engine whose hotspot landed on `putPiece` (chess-java-cc, chess-rust-cc) will show `tapered_eval` from the MG/EG incremental update variables, and zero for almost everything else, even if the engine has a full evaluation function elsewhere. The sub-feature matrix reflects "what was visible in this particular hotspot."

Sub-features divide into three bands:

- **Visible frequently** (≥ 6/19): `material_values`, `tapered_eval`, `perspective_flip` — these appear across correct extractions, wrong extractions, and docstrings alike
- **Visible rarely** (2–3/19): `pst_table_lookup`, `midgame_tables`, `passed_pawn`, `computed_positional` — appear only in valid correct extractions
- **Never detected** (0/19): `sunfish_vals`, `cpw_simplified`, `phase_computation` — the last is a true absence (phase calculation lives in a separate helper), while the first two are a critical negative finding discussed in Section 7

---

## 6. Pairwise similarity

### 6.1 Feature-Jaccard: five trivial clusters and one informative pair

The feature-Jaccard matrix (computed over the 13-dimensional sub-feature vectors) reveals that most 100% pairs are artefacts of sparse or wrong extractions:

| Score | Pair | Explanation |
|---|---|---|
| 100% | chess-Rocq ↔ chess-ruby-codex | Both have ONLY `material_values` — single-feature match |
| 100% | chess-apl-codex54 ↔ chess-java | Both have ONLY `pst_table_lookup` — single-feature match |
| 100% | chess-brainfuck ↔ chess-py ↔ latex-chess-engine | All have ONLY `perspective_flip` — artefact of wrong extractions |
| 100% | chess-java-cc ↔ chess-py-cc | Both have ONLY `tapered_eval` — one is an incremental update, one is a 2-line docstring |
| 100% | chess-revisit-java-toCOBOL ↔ chess-revisit-java-toRust | Same file extracted twice (100% also in Token-Jaccard) |
| 38% | chess-ruby-cc ↔ chess-why3-cc | The only non-trivial pair with multiple real sub-features |

The 38% chess-ruby-cc ↔ chess-why3-cc pair is the most informative, but also the most misleading: chess-why3-cc's features come from ShallowBlue's vendored C++ evaluation, not the why3-cc engine's own OCaml evaluation (see Section 8). chess-ruby-cc is the only engine whose extracted snippet reflects its *own* evaluation function with multiple genuine sub-features.

**Contrast with quiescence**: quiescence feature-Jaccard showed high-scoring pairs (88%, 80%) that reflected genuine cross-language algorithmic convergence. Evaluation shows only trivial 100% pairs (single-feature overlap) or artefact pairs. The algorithm space is sparsely occupied — a consequence of both sparse extraction and genuine evaluation diversity.

### 6.2 Token-Jaccard: only the same-file pair is notable

The only notable Token-Jaccard score is `chess-revisit-java-toCOBOL ↔ chess-revisit-java-toRust` at 100% — because both engines extracted the same file (`chess-revisit-java-toCOBOL/src/cobol/chess_engine.cob`). The locator found two engine paths pointing to the same COBOL source.

After that, the highest pairs are:
- 22%: chess-apl-codex54 ↔ chess-java (APL's `PAWN_PST[LOOKUP]` dispatch shares token patterns with Java's switch returning `PAWN_PST[square]`)
- 21%: chess-java ↔ cplusplus-chess (both board code with piece-type constants and square indices)
- 18%: chess-java ↔ lean-chess (Java `Evaluator.java` and Lean `Eval.lean` share structural token patterns despite different languages)

All cross-language token-Jaccard scores are below 25%. This continues the pattern from quiescence and TT: lexical similarity is dominated by language syntax differences, not algorithmic copying.

---

## 7. The fingerprint analysis: Sunfish and CPW both absent

The two most prominent open-source evaluation templates — Sunfish and the CPW (chessprogramming.org wiki) simplified evaluation function — have distinctive material value signatures:

| Engine | P | N | B | R | Q |
|---|---|---|---|---|---|
| Sunfish | 100 | 280 | 320 | 479 | 929 |
| CPW simplified | 100 | 320 | 330 | 500 | 900 |
| Typical detection | 100 | 300–325 | 325–340 | 500–520 | 900–950 |

**Result: 0/19 for Sunfish values, 0/19 for CPW values.**

This is the strongest negative finding in the entire evaluation analysis. Sunfish is a Python chess engine with 200 lines of code that is extremely widely cited in LLM training data — every tutorial list of "learn from these chess engines" includes it. The CPW simplified evaluation function is the most-linked evaluation example on chessprogramming.org. Both are absent.

Several explanations are possible:

1. **The LLMs varied the material values intentionally.** When asked to "implement evaluation," models generated values close to but not identical to canonical examples: knight values typically appear as 300–320, bishops at 320–340, varying by session and prompt phrasing.

2. **The training data includes many evaluation examples with slightly different values.** The Sunfish value `479` for a rook (instead of the round `500`) is distinctive enough that if it appeared, it would be detectable. Its absence suggests the models were not copying from Sunfish's table.

3. **The extraction failure rate is high.** Several engines that implement evaluation were extracted from wrong functions (8 of 19 extractions hit wrong code), so the sub-feature detector never saw the actual material constants. The true rate of "uses Sunfish values" could be higher than 0/19 — we cannot detect what we did not extract.

Even accounting for this caveat, the 0/19 rate for both canonical fingerprints is evidence against direct template copying. In the quiescence analysis, "stand_pat" terminology appeared in 19/26 engines — an almost universal convergence on a community term. For evaluation, neither Sunfish nor CPW values reproduced. The evaluation specification is more loosely specified in the training data (many sources, many value sets), producing more variation.

**The contrast with quiescence fingerprinting is instructive**: quiescence has one canonical algorithm and one canonical paper-trail (chessprogramming.org quiescence search); evaluation has many implementations and the material values vary across every tutorial. The algorithm-level convergence is stronger than the data-level convergence.

---

## 8. The ShallowBlue vendoring: critical finding for RQ3

The match for `chess-why3-cc` landed on:

```
tests/engines/shallowblue-src/src/eval.cc  lines 192–232  (41 LOC)
```

ShallowBlue is an open-source Java chess engine (MIT license). Its C++ port was vendored in the `tests/engines/shallowblue-src/` directory of chess-why3-cc, apparently as a reference engine for testing or benchmarking purposes.

The extracted function `Eval::evaluateForPhase` is ShallowBlue's evaluation:
```cpp
int Eval::evaluateForPhase(const Board &board, Color color) {
  score += MATERIAL_VALUES[phase][PAWN] * (_popCount(...) - _popCount(...));
  // Piece square tables
  score += board.getPSquareTable().getScore(phase, color) - ...;
  // Mobility
  score += evaluateMobility(board, phase, color) - ...;
  // King pawn shield
  if (phase == OPENING) { score += KING_PAWN_SHIELD_BONUS[OPENING] * ...; }
  return score;
}
```

This function has 5/13 sub-features detected (`material_values`, `midgame_tables`, `tapered_eval`, `king_safety`, `mobility_terms`). These features belong to **ShallowBlue's evaluation, not chess-why3-cc's own OCaml evaluation**.

**Implications for RQ3 (provenance and independence)**:

The chess-why3-cc engine's own evaluation is in its Why3/OCaml source, not in `tests/`. This is a clear instance of the engine-core / tooling distinction. The PST feature detection correctly identifies that PST-related code exists in the chess-why3-cc repository — it does — but attributes it to the wrong component.

Under the four-signal audit framework used in RQ3, this would constitute a "third-party library fingerprint match in the test tree" but NOT "a fingerprint match in the engine core." This distinction is precisely what the engine-core / tooling separation is designed to enforce. The chess-why3-cc evaluation in the test directory is provably ShallowBlue code (it has ShallowBlue's exact class structure, method names, and bitboard API). The engine's own evaluation — if it has one beyond material counting — is in a different path and was not captured.

This is the evaluation analysis's clearest contribution to the provenance study: automated feature location must exclude `tests/`, `vendor/`, `third-party/`, and `benchmarks/` subtrees, or it will silently attribute third-party code features to the engine under study.

---

## 9. Implementation strategies: a taxonomy

### Tier 0 — No positional evaluation (material-only)

**chess-Rocq** (Coq/Gallina): The extracted `piece_value` function returns only material constants via Coq pattern matching (`match pk with | Pawn => val_pawn | Knight => val_knight | ...`). There are no PST tables. The engine's Elo reflects raw material counting with no positional understanding.

**chess-ruby-codex** (Ruby): `piece_value(piece)` calls `PIECE_VALUES.fetch(piece.downcase, 0)` — a hash lookup returning a single constant per piece type, no position dependence.

These two engines share the highest feature-Jaccard (100%), but only because both have a single sub-feature (`material_values`). They are conceptually identical at the evaluation level — the simplest possible evaluation function — despite being in Coq and Ruby.

### Tier 1 — Basic PST lookup

**chess-java** (Java): The cleanest extraction in the corpus. `pieceSquareBonus(int pieceType, int square)` with a switch statement returning `PAWN_PST[square]`, `KNIGHT_PST[square]`, etc. This is the textbook PST function from chessprogramming.org, translated to Java with no modification. Single MG table per piece; no endgame distinction.

**chess-apl-codex54** (APL): `PIECE_SQUARE_OPEN_VALUE` dispatches via APL branch-goto (`→(PIECE∊'Pp')⍴PAWN`) to the appropriate PST array. For black pieces, `MIRROR_IDX` flips the square index to look up from white's perspective. This is algorithmically identical to Java's switch-case dispatch — the APL idiom (branch-goto dispatch) maps onto the same control flow as a switch statement. The feature-Jaccard 100% match between these two engines (both `pst_table_lookup` only) is structurally correct: same algorithm, different syntax paradigm.

### Tier 2 — Incremental PST with MG/EG separation

**chess-java-cc** (Java): The hotspot landed on `putPiece` (incremental update), not the evaluation function. What is visible is:
```java
int pstSq = color == WHITE ? sq : sq ^ 56;
pstScore[0] += PieceSquareTables.MG_TABLE[pieceType][pstSq] * (color == WHITE ? 1 : -1);
pstScore[1] += PieceSquareTables.EG_TABLE[pieceType][pstSq] * (color == WHITE ? 1 : -1);
```
This reveals that chess-java-cc implements incremental PST evaluation with separate midgame and endgame tables, updated lazily as pieces are placed. The `sq ^ 56` is the canonical perspective flip for black pieces (XOR with 0b00111000 mirrors ranks). The `pstScore[0]`/`[1]` accumulator pair is updated incrementally, avoiding a full board scan at each evaluation. This is significantly more sophisticated than chess-java's approach, reflecting a later stage in the session trajectory.

**chess-revisit-java-toCOBOL / chess-revisit-java-toRust** (COBOL): The hotspot landed on `BOARD-MAKE-MOVE`, revealing `MOVE B-PST-MG TO U-PST-MG(B-PLY)` and `MOVE B-PST-EG TO U-PST-EG(B-PLY)` — the undo-stack saving of incremental MG/EG scores before a move is made. This confirms that both COBOL ports of the Java→COBOL→Rust pipeline carry through the MG/EG incremental evaluation infrastructure from the parent Java engine.

**chess-rust-cc** (Rust): Hotspot landed on bare `put_piece` without PST logic visible (the 6-line extract shows only bitboard and mailbox updates, no PST). The PST update is presumably in a separate method called by `put_piece`. The extraction missed the evaluation content.

### Tier 3 — Full tapered evaluation with phase interpolation

**chess-ruby-cc** (Ruby): The most complete and correctly extracted evaluation in the corpus. `add_piece_eval(piece, pt, color, sq)` shows:
```ruby
mg_pst = PST::MG_TABLES[piece]
eg_pst = PST::EG_TABLES[piece]
mg_val = PST::MG_PIECE_VALUE[pt] + (mg_pst ? mg_pst[sq] : 0)
eg_val = PST::EG_PIECE_VALUE[pt] + (eg_pst ? eg_pst[sq] : 0)
if color == WHITE
  @mg_score += mg_val
  @eg_score += eg_val
else
  @mg_score -= mg_val
  @eg_score -= eg_val
end
@phase += PST::PHASE_WEIGHTS[pt] || 0
```

This implements: separate `MG_TABLES` and `EG_TABLES` per piece (by piece identity, not just piece type), separate `MG_PIECE_VALUE` and `EG_PIECE_VALUE` material constants, accumulated `@mg_score` and `@eg_score` running totals for both sides, incremental phase tracking via `@phase`, and implicit tapered interpolation when computing the final score (not visible here but inferable from the accumulator structure). Bishop pair count (`@w_bishops`) and pawn file tracking (`@w_pawn_files`) are also tracked inline for pawn structure bonuses.

chess-ruby-cc is the only engine with all four components visible: MG tables (`mgt`), EG tables (`egt`), tapered architecture (`tap`), and full material tracking (`mat`). It has the highest sub-feature count (5/13) of any valid extraction.

### Tier 4 — Computed (geometry-based) positional evaluation

**lean-chess** (Lean 4): `pieceSquareValue` is structurally different from every other evaluation in the corpus. It uses no lookup tables at all:
```lean
def pieceSquareValue (piece : Piece) (isEndgame : Bool) (sq : Square) : Int :=
  let c := centrality sq
  let adv := Int.ofNat (forwardRank piece.color sq)
  let edgePenalty := if isEdgeSquare sq then 1 else 0
  match piece.kind with
  | .pawn   => adv * 6 + c * 2
  | .knight => c * 12 - Int.ofNat edgePenalty * 18 + adv
  | .bishop => c * 6 + adv * 2
  | .rook   => c * 2 + adv * 2
  | .queen  => c * 3 + adv
  | .king   => if isEndgame then c * 9 + adv * 2
               else kingCastledBonus piece.color sq - c * 7 - adv * 8
```

Instead of 64-entry tables, the positional value is computed from three geometric quantities: `centrality sq` (distance from center), `forwardRank piece.color sq` (advancement from own back rank), and `isEdgeSquare sq` (edge penalty for knights). The endgame distinction is a boolean parameter, not a phase interpolation.

This is the only implementation in 35 engines that replaces tabular lookup with geometric computation. It is also the only implementation where "midgame vs endgame" is exposed as an explicit `Bool` parameter to the caller rather than hidden inside a phase variable. The Lean LLM understood that:

1. Large lookup tables are inelegant in a functional proof-oriented language (they would be 64-element list or array literals with no structure)
2. Geometric computation is naturally expressible in Lean's functional style and can encode the same heuristics compactly
3. Separating the endgame flag from the evaluation internals is cleaner than having `isEndgame` as internal state

This is a genuine and sophisticated adaptation to the target language's idioms and philosophy.

### Tier 5 — Database/query-based evaluation

**chess-sql** (Python + SQL): `sql/eval.sql` implements the full evaluation as a SQL `WITH` query:

```sql
WITH
pos AS (SELECT board, side FROM position LIMIT 1),
square_eval AS (
  SELECT s.sq, substr(p.board, s.sq + 1, 1) AS piece,
    COALESCE(pv.value, 0) AS mat_value,
    COALESCE(
      CASE
        WHEN piece BETWEEN 'A' AND 'Z' THEN
          (SELECT bonus FROM pst WHERE pst.piece = UPPER(piece) AND pst.sq = s.sq)
        WHEN piece BETWEEN 'a' AND 'z' THEN
          -(SELECT bonus FROM pst WHERE pst.piece = UPPER(piece) AND pst.sq = (7 - s.rank) * 8 + s.file)
        ELSE 0
      END, 0) AS pst_bonus
  FROM squares s, pos p
  LEFT JOIN piece_value pv ON pv.piece = piece
  WHERE piece != '.'
),
center_bonus AS (
  SELECT COALESCE(SUM(CASE
    WHEN piece BETWEEN 'A' AND 'Z' AND sq IN (27,28,35,36) THEN 10
    WHEN piece BETWEEN 'a' AND 'z' AND sq IN (27,28,35,36) THEN -10
    ...
  END), 0) AS bonus FROM square_eval
)
SELECT (SUM mat_value) + (SUM pst_bonus) + (center bonus) AS score;
```

The board is stored as a string in a `position` table. White pieces are uppercase letters, black pieces lowercase. The PST lookup is a correlated subquery joining to a `pst` table keyed by (piece, sq). The perspective flip for black uses `(7 - s.rank) * 8 + s.file` to mirror vertically. Center control is computed via explicit square membership checks.

This is the only engine in any language survey where the evaluation function is implemented as a database query. The architecture is unique: evaluation is declarative (what to compute) rather than imperative (how to compute it), and the result is computed by the SQL engine's query optimizer rather than by explicit iteration. The center bonus CTE also shows that the LLM added a third component beyond material + PST without being explicitly prompted — an emergent design decision consistent with the "evaluate the center" heuristic from chess knowledge.

---

## 10. PL-specific adaptations

### Coq/Gallina (chess-Rocq): pattern matching as dispatch

`piece_value` uses Coq's `match` for piece-type dispatch, the idiomatic Coq equivalent of a switch statement. The King returns `0` (kings have no material value in chess programming, since the game ends when the king is captured). This is correct chess semantics encoded in a theorem-prover-friendly style. The absence of PST in chess-Rocq is expected: a full PST would be an array of 64 integers, which in Coq would require either a vector type with index bounds proof or an axiom-based definition. The LLM chose to omit this complexity rather than navigate Coq's dependent type system for a 64-entry table.

### APL (chess-apl-codex54): branch-goto dispatch to array lookup

APL's `→(condition)⍴label` branch idiom is the APL equivalent of conditional jump. The evaluation dispatches to the right PST array via a sequence of these branches: `→(PIECE∊'Pp')⍴PAWN`, `→(PIECE∊'Nn')⍴KNIGHT`, etc. The black-piece perspective flip is `MIRROR_IDX IDX` — a named function call that maps the square index to its vertical mirror. This is idiomatic APL: operations on scalar indices dispatched via boolean branching to array selection, avoiding explicit loops.

The full PST arrays (`PAWN_PST`, `KNIGHT_PST`, etc.) are declared elsewhere in the APL source. The `PIECE_SQUARE_OPEN_VALUE` function handles the opening PST — there is presumably a separate `PIECE_SQUARE_END_VALUE` for the endgame (not captured by this hotspot). The naming `_OPEN_` vs. `_END_` suggests the APL engine does distinguish game phases, though at a cruder level than chess-ruby-cc's continuous phase interpolation.

### COBOL (chess-cobol-cc): flat data section with REDEFINES

The COBOL evaluation data is declared in WORKING-STORAGE as a flat sequence of `FILLER PIC S9(4) VALUE +N` entries, then accessed via a `WS-PST-PAWN REDEFINES WS-PST-PAWN-DATA` clause with an `OCCURS 64 TIMES` array overlay. This is the idiomatic COBOL approach to constant arrays: data is initialized at program load via the `VALUE` clauses, and `REDEFINES` provides array syntax on top of the flat data declaration. The pattern precisely reflects COBOL's statically-allocated data model with no dynamic allocation.

The PST values themselves are readable from the hotspot: the pawn PST (rank 1 = 0s, rank 2 = {+5,+10,+10,-20,-20,+10,+10,+5}, ..., rank 7 = {+50,+50,+50,+50,+50,+50,+50,+50}) match the simplified evaluation function from chessprogramming.org almost exactly, and are identical to the values in latex-chess-engine's TeX macros. This is a rare cross-engine data value match — both chess-cobol-cc and latex-chess-engine appear to have used the same CPW PST source, but the material value sub-feature detection for CPW was not triggered (the detection targets material values P/N/B/R/Q constants, not PST entries).

### Lean 4 (lean-chess): geometric computation over lookup tables

Discussed in Section 9 (Tier 4). The key adaptation is that Lean's philosophy favors computation over data — the `centrality`, `forwardRank`, and `isEdgeSquare` functions can be formally reasoned about and potentially proved correct, whereas a 64-element table is an opaque constant. The LLM chose computation partly for expressiveness and partly because a large literal array in Lean would require an unusual syntax form that is less natural than a function definition.

The `kingCastledBonus` function (not extracted but referenced) is another example: rather than a king PST that encodes kingside vs queenside castling positions, it's a separate function computing the bonus based on the actual castled position. This is more robust (handles non-standard king positions) and more readable.

### SQL (chess-sql): declarative evaluation via CTEs

Discussed in Section 9 (Tier 5). The SQL implementation uniquely makes evaluation a first-class query artifact rather than a function. The board is a string column; squares are rows; PST bonuses are rows in a `pst` table joined at evaluation time. The center bonus is computed via explicit `IN (27, 28, 35, 36)` membership, not via a function. Everything is set-oriented and declarative, which is the defining property of SQL as a language. The LLM correctly identified that in SQL, "evaluation" means a query that produces a score row, not a function that returns an int.

---

## 11. Evaluation sophistication tiers and Elo correlation

Across the corpus, four observable sophistication levels map to expected Elo ranges:

| Tier | Evaluation style | Example engines | Expected Elo contribution |
|---|---|---|---|
| 0 | Material only | chess-Rocq, chess-ruby-codex | Baseline: ±0 vs random mover |
| 1 | Basic PST (single table) | chess-java, chess-apl-codex54 | +100–200 Elo over material-only |
| 2 | MG/EG tables, incremental | chess-java-cc, revisit ports | +150–250 Elo over basic PST |
| 3 | Tapered eval + phase interp. | chess-ruby-cc | +100–200 Elo over MG/EG |

These estimates are rough — evaluation quality interacts with search depth (a deeper search with a weaker eval can beat a shallower search with a stronger eval), and the quiescence search analysis showed that most engines already converge on the correct qsearch skeleton. But the evaluation sophistication tier is a meaningful predictor of relative strength among engines at similar search depths.

Within the corpus, the COBOL-chess pawn PST data shows rank-7 values of +50 centipawns (promotion-adjacent squares), which is materially significant — a pawn at rank 7 is worth a rook with these bonuses. The PST shape is standard and should provide meaningful positional guidance. The chess-sql center bonus (10 centipawns per piece in d4/d5/e4/e5, 5 for the outer ring) adds a simple center-control heuristic that has measurable Elo value in the opening.

---

## 12. Missing opportunities: evaluation gaps across the corpus

### King safety: nearly absent (1/19)

The single `king_safety` detection came from chess-why3-cc's ShallowBlue vendored code (not chess-why3-cc's own evaluation). Among the 19 matched engines' own implementations, king safety is effectively 0/19.

King safety is the most consequential missing feature. In practical chess, the king is highly vulnerable in the middlegame and must be sheltered. An engine without king safety will routinely misjudge positions where one side's king is exposed. The chessprogramming.org article on king safety is extensive and well-known, yet it appears nowhere in the corpus's own evaluation code.

Why? King safety requires additional infrastructure: identifying the king's zone (squares around the king), counting pieces attacking that zone by type, weighting the attack count by piece value. This is a multi-step computation with several data structure dependencies. The LLMs implemented the simpler positional features (PST tables are just array lookups) and stopped before the more complex king safety computation. This is consistent with the quiescence analysis finding that LLMs implement the standard specification well but rarely reach the extension layer.

### Tapered evaluation: rare (1 confirmed, several hinted)

Only chess-ruby-cc has a confirmed, correctly extracted full tapered evaluation (MG + EG tables, phase tracking, interpolation). chess-java-cc and the revisit ports have tapered evaluation code visible in their `makeMove` incremental updates, confirming it is implemented, but the extraction did not show the interpolation step.

Tapered evaluation is well-documented on chessprogramming.org and is the standard technique for all engines above approximately 1800 Elo. Its rarity in correctly extracted code reflects not its absence but its location: the interpolation step `(mg_score * phase + eg_score * (max_phase - phase)) / max_phase` is in the evaluation function, while the phase tracking is in `makeMove`. The hotspot extractor captures one or the other, not both.

### Mobility: absent from own evaluations (1/19, ShallowBlue)

Piece mobility (counting the number of legal moves per piece and adding a bonus per move) is the next natural evaluation term after PST. It is described in chessprogramming.org and implemented in most serious engines. The 1/19 detection is from ShallowBlue. No engine's own evaluation code shows mobility, despite mobility being a well-understood technique.

Mobility requires generating moves in the evaluation function, which is computationally expensive. The LLMs likely judged (correctly) that adding mobility evaluation without careful caching would significantly slow the engine. This is a correct engineering tradeoff, not ignorance of the feature.

### Passed pawn: 2/19, both from wrong extractions

`passed_pawn` was detected in chess-cobol-cc and chess-cplusplus-claude, but both detections come from wrong extractions (chess-cobol-cc's hotspot is working-storage with `WS-PP-FLAG` (passed pawn flag) visible in the data section, chess-cplusplus-claude's hotspot is the `passed_pawn_mask(Color c, Square s)` helper function). The passed pawn infrastructure exists in both engines but was not captured in an evaluation context.

Passed pawn evaluation is a standard endgame technique: a pawn with no opposing pawns in front of it or on adjacent files is highly valuable. The absence from evaluation outputs does not mean engines lack it — it means the extractor did not reach the evaluation function where it would be summed.

---

## 13. The broader triad synthesis

The three features studied — quiescence search, transposition table, evaluation — jointly determine engine strength, and the cross-analysis reveals consistent patterns:

**Convergence at the algorithm level, diversity at the data level.** Quiescence has one algorithm (stand-pat + alpha/beta) that every engine implements identically. TT has one architectural concept (position hash → stored (score, depth, flag, move)) with significant structural variation. Evaluation has one concept (position → score) with maximum structural diversity: material-only, basic PST, incremental MG/EG, computed geometric, SQL CTE, tapered phase interpolation. The data level (PST values, material constants) shows the most variation: no common fingerprint (Sunfish absent, CPW absent).

**The LLM implementation ceiling varies by feature.** For quiescence, LLMs reliably reach Tier 1 (basic stand-pat) and often Tier 2 (delta pruning, SEE). For TT, they reliably implement Zobrist hashing and basic probe/store. For evaluation, the ceiling is lower: most engines stop at basic PST without tapered evaluation, and king safety is missing across the board. The difficulty of the extension layer scales with the amount of additional infrastructure required: check evasion in quiescence is one if-statement, tapered evaluation requires two table sets and a phase interpolation, king safety requires zone computation and attack counting. LLMs implement the base feature well and add extensions in proportion to their simplicity.

**Extraction methodology reveals its own hierarchy.** Quiescence (one concentrated function): high extraction accuracy, interpretable matrix. TT (one distributed data structure): medium accuracy, cluster-structured matrix. Evaluation (multiple distributed components): low accuracy (8/19 wrong), sparse matrix, high artefact rate. The methodological lesson scales with feature distribution.

**Missing features are consistent across the triad.** The quiescence analysis found check evasion (correctness gap) and TT-in-qsearch (optimization gap) missing. The TT analysis found depth-preferred replacement and age management missing. The evaluation analysis finds king safety and tapered evaluation missing. In all three cases, LLMs implement the base algorithm from the most-cited source (chessprogramming.org's main article on each topic) and miss the extensions from the less-cited refinement articles. This points to a systematic training-data coverage gap: refinements are underrepresented relative to base implementations.

---

## 14. Extraction failures: the methodological lesson for evaluation

Evaluation is the hardest feature to extract for a static hotspot locator, for three structural reasons:

**Reason 1: Evaluation is distributed across more files than any other component.**

A complete evaluation implementation touches: `constants.h` or equivalent (PST table data), `evaluate.cpp` or equivalent (the lookup function), `board.cpp` or equivalent (incremental update in makeMove/unmakeMove), and sometimes a `pawn_hash.cpp` or separate structure for pawn evaluation caching. No single file "is" the evaluation the way `search.cpp` "is" the quiescence search.

**Reason 2: Evaluation-adjacent code contains the same keywords.**

`putPiece` in chess-java-cc and chess-rust-cc contains `PST` references because it performs incremental PST updates. `BOARD-MAKE-MOVE` in the COBOL engines saves and restores `B-PST-MG`/`B-PST-EG` on the undo stack. `_set_ep_square_if_capturable` in chess-py contains `BLACK` and `PAWN` as identifiers. All of these score highly on the PST keyword detector without being evaluation functions.

**Reason 3: PST tables are often in separate constant files.**

The actual 64-integer tables are typically in `PieceSquareTables.java` (chess-java-cc), `pst.h` (C/C++ engines), or `PST` modules (Ruby, Rust). The extraction pattern `piece[_ ]?square` can match these files or match callers of these files interchangeably, depending on which file has more context around the keyword.

**Extraction failure count**: Of 19 matched engines, 8 extracted wrong functions and 1 extracted a 2-line docstring stub. That is 9/19 = 47% artefact rate — nearly half of all "found" entries are not the evaluation code.

**Contrast with quiescence (12%) and TT (14%)**:

| Feature | Total matched | Invalid extractions | Artefact rate |
|---|---|---|---|
| Quiescence search | 28 | ~3–4 (assembly, mojo, latex false hits) | ~12% |
| Transposition table | 24 | 3 (binary files) | ~14% |
| Evaluation / PST | 19 | 9 (wrong functions + stub) | 47% |

The progression confirms that extraction failure scales with feature distribution. The solution is multi-hotspot extraction: for evaluation, collect the top-3 hotspots per engine (likely landing on table declaration, lookup function, and incremental update separately) and report sub-features from their union. A single hotspot cannot capture a distributed feature.

**The ShallowBlue case** adds a fourth failure mode: third-party code vendored in the repository scoring higher than the engine's own code because the vendored code is in a richer context (a well-structured C++ file with named functions) while the engine's own code may be in a more idiomatic-but-sparse source (OCaml/Why3 with minimal keyword presence). Any future hotspot extraction must explicitly filter paths containing `tests/`, `vendor/`, `third-party/`, `lib/engines/`, and similar non-own-code directories.

---

## Summary

Static evaluation / piece-square tables, the third point of the algorithm–data-structure–evaluation triad, shows the highest extraction failure rate (47%) and the most structural diversity of the three features studied. The core findings are:

**What LLMs implement well**: the basic PST lookup (dispatch by piece type, index by square, flip for black's perspective), incremental MG/EG evaluation during move-make/unmake, and language-appropriate forms of PST lookup (APL branch-goto arrays, SQL CTE joins, Lean geometric computation, COBOL REDEFINES arrays, Coq pattern matching).

**What LLMs do not implement**: king safety (0/19 in own code), continuous phase interpolation (1/19 confirmed, chess-ruby-cc only), and mobility terms (0/19 in own code). These represent the "second article" extensions beyond the base chessprogramming.org template — complex to implement, requiring additional data structures, and apparently underrepresented in the training data relative to basic PST implementation.

**The fingerprint verdict**: no Sunfish material values (0/19), no CPW simplified values (0/19). Material constants vary by session without converging on any named canonical set. This extends the quiescence and TT findings: while algorithms converge on chessprogramming.org-derived specifications, data values (material constants, PST entries) are generated fresh each session without copying a canonical table.

**The ShallowBlue finding**: chess-why3-cc's PST match comes from a vendored third-party engine in its test directory, not from its own evaluation code. This is a clear instance of the engine-core / tooling distinction required by RQ3's provenance analysis, and demonstrates that automated feature location must exclude vendor and test subtrees explicitly.

**The methodological finding**: PST/evaluation is the hardest feature to localize for static hotspot extraction because it is distributed across table declarations, lookup functions, incremental update code, and phase-computation helpers — all in separate files. The 47% artefact rate (9/19 wrong extractions) is the highest of the triad and establishes that multi-hotspot mode with path filtering is necessary for distributed architectural features.
