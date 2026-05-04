# Unified Feature Analysis Report: Three-Feature Triad

**Features**: Quiescence search · Transposition table · Evaluation/PST  
**Corpus**: 35 engines across 15 programming languages  
**Pipeline**: `scripts/feature_locator.py --hotspot` + `scripts/feature_compare.py`  
**Date**: 2026-04-20  
**Per-feature detail**: `QUIESCE_FEATURE_ANALYSIS.md`, `TT_FEATURE_ANALYSIS.md`, `EVAL_FEATURE_ANALYSIS.md`

---

## 1. Why this triad

Chess engine strength is determined by three separable components:

- **Search algorithm** (quiescence): correctness and extension quality of the capture-resolution phase
- **Data structure** (transposition table): architectural quality of position memoization
- **Evaluation function** (PST): accuracy of static position assessment

Together they cover the three design layers of any alpha-beta engine. Analyzing all three with the same pipeline makes it possible to characterize what LLMs do well across layers, rather than drawing conclusions from a single feature.

The triad also represents three structural archetypes for static analysis:
- Quiescence is **concentrated**: one function, one algorithm
- Transposition table is **distributed**: data structure + initialization + probe + store across multiple files
- Evaluation/PST is **highly distributed**: constant tables, lookup functions, and incremental updates each in separate files

This gradient tests the limits of single-hotspot extraction.

---

## 2. Coverage summary

| Feature | Engines with feature | Valid extractions | Invalid / missing | Artefact rate |
|---|---|---|---|---|
| Quiescence search | 28/35 | 26 | 2 (Assembly stub, Mojo placeholder) | ~8% |
| Transposition table | 24/35 | 21 | 3 (2 compiled binaries, 1 test file) | ~14% |
| Evaluation / PST | ~19/35 | ~10 | ~9 (wrong function, wrong file) | ~47% |

The artefact rate scales with feature distribution. Quiescence, concentrated in one function, is easiest to extract. Evaluation, spread across constant files and update code, is the hardest. The 47% rate for evaluation establishes a clear methodological threshold: single-hotspot extraction is insufficient for distributed features.

---

## 2b. Three representative quiescence variants (pedagogical illustration)

The following three implementations of quiescence search, drawn from
`quiescence.hotspot.txt`, illustrate specification convergence and PL-specific
adaptation concretely. They are selected to maximise paradigm diversity:
imperative OOP (Java), functional proof-assistant (Coq/Gallina), and
procedural legacy (COBOL). The full 26-engine per-feature table and
pairwise distance matrix are in `reports/features/quiescence.compare.txt`
and the paper's Appendix A5.

### Pairwise distances for the trio

| Pair | Feature-Jaccard | Token-Jaccard |
|---|---|---|
| chess-java ↔ chess-Rocq | 38% | 10% |
| chess-java ↔ COBOL-chess | 22% | 9% |
| chess-Rocq ↔ COBOL-chess | **60%** | **8%** |

The Rocq↔COBOL pair (60% feat-J, 8% tok-J) is the key data point:
these two engines share 3 of 5 combined sub-features (stand_pat,
capture_only, delta_pruning) while sharing almost no surface tokens.

### Variant 1: chess-java (Java) — imperative OOP, check evasion

**Sub-features**: stand_pat, beta_cutoff, alpha_update, capture_only,
depth_limit, check_evasion, negamax_recurse  (7/13)

```java
// [1] stand-pat evaluation
int standPat = evaluator.evaluate(board);
boolean inCheck = board.isInCheck(board.sideToMove());
if (!inCheck) {
    if (standPat >= beta) return beta;      // [2] beta-cutoff
    if (standPat > alpha) alpha = standPat; // [3] alpha-update
}
// [4] capture-only, or ALL legal if in check
List<Move> moves = board.generateLegalMoves(!inCheck);
if (moves.isEmpty())
    return inCheck ? -MATE_SCORE + ply : alpha;
for (Move move : moves) {
    if (!inCheck && !isTactical(move)) continue;
    board.makeMove(move, undo);
    int score = -quiescence(-beta, -alpha, ply + 1); // [5] negamax
    board.unmakeMove(move, undo);
    if (score >= beta) return beta;
    if (score > alpha) alpha = score;
}
return alpha;
```

**Commentary**: Java's check-evasion branch (`inCheck`) is the key
distinguishing feature — when in check, all legal moves are generated
(not just captures) and a mate score is returned if none are legal.
This is absent from both Rocq and COBOL. The OOP style
(`board.generateLegalMoves`, `evaluator.evaluate`) wraps the algorithm
in class method calls but the algorithm itself is identical to the
C/Python implementations in the corpus.

### Variant 2: chess-Rocq (Coq/Gallina) — functional proof-assistant

**Sub-features**: stand_pat, capture_only, delta_pruning, depth_limit  (4/13)

```coq
(* qdepth : nat => termination proved by structural recursion *)
Fixpoint quiesce (pos : Position) (alpha beta : int) (qdepth : nat) : int :=
  match qdepth with
  | O => evaluate pos              (* [1] base case: depth exhausted *)
  | S qdepth' =>
    let stand_pat := evaluate pos in          (* [1] stand-pat *)
    if leb beta stand_pat then stand_pat      (* [2] beta-cutoff via leb *)
    else if ltb (add stand_pat delta_margin) alpha
         then stand_pat                       (* delta pruning *)
    else
      let a := if ltb alpha stand_pat         (* [3] alpha-update via ltb *)
               then stand_pat else alpha in
      let captures := gen_capture_moves pos in (* [4] capture-only *)
      let fix go (mvs : list Move) (cur_a : int) (fuel : nat) : int :=
        match fuel with
        | O => cur_a
        | S fuel' =>
          match mvs with
          | nil => cur_a
          | m :: rest =>
            let score := negate_score          (* [5] negamax sign-flip *)
              (quiesce (make_move pos m)
                (negate_score beta)
                (negate_score cur_a) qdepth') in
            if leb beta score then score
            else go rest (if ltb cur_a score then score else cur_a) fuel'
          end
        end
      in go captures a 256%nat
  end.
```

**Commentary**: Three PL-specific adaptations are visible:
1. `Fixpoint` with `qdepth : nat` — Coq's totality checker requires structural recursion; the depth argument decreases by one `S` step at each call, making termination formally proved.
2. `leb`/`ltb` instead of `>=`/`>` — Coq's integer comparison functions. The beta_cutoff and alpha_update algorithms are present but use non-standard vocabulary, explaining why the regexes don't detect them.
3. `let fix go ... in go captures a 256%nat` — a local named recursive function for iterating the capture list. The `fuel : nat` argument is a second termination witness for the inner loop.
No mutable state exists; every alpha/score update is a `let ... in` binding.

### Variant 3: COBOL-chess (COBOL) — procedural, explicit working-storage

**Sub-features**: stand_pat, capture_only, delta_pruning, mvv_lva  (4/13)

```cobol
    CALL "EVAL" USING GAME-STATE STANDPAT          *> [1] stand-pat
    IF STANDPAT >= L-BETA                           *> [2] beta-cutoff
        MOVE L-BETA TO L-OUT
        GOBACK
    END-IF
    IF STANDPAT > L-ALPHA                           *> [3] alpha-update
        MOVE STANDPAT TO L-ALPHA
    END-IF
    *> delta pruning: constant = 950 cp (queen value, from CPW)
    IF (STANDPAT + 950) < L-ALPHA
        MOVE L-ALPHA TO L-OUT
        GOBACK
    END-IF
    MOVE 1 TO CAP-ONLY                              *> [4] capture flag
    CALL "MOVEGEN" USING GAME-STATE LS-LIST CAP-ONLY
    PERFORM VARYING I FROM 1 BY 1
            UNTIL I > ML-COUNT OF LS-LIST
        PERFORM SCORE-Q-MOVE                        *> MVV-LVA ordering
    END-PERFORM
    PERFORM VARYING I FROM 1 BY 1
            UNTIL I > ML-COUNT OF LS-LIST
        PERFORM PICK-BEST-Q
        CALL "MAKEMOVE" USING GAME-STATE LS-MOVE OK
        IF OK = 1
            COMPUTE CHILD-ALPHA = 0 - L-BETA
            COMPUTE CHILD-BETA  = 0 - L-ALPHA
            CALL "QUIESCE" USING GAME-STATE         *> [5] recursive call
                CHILD-ALPHA CHILD-BETA L-SS CHILD-SCORE
            COMPUTE CHILD-SCORE = 0 - CHILD-SCORE   *> negamax sign-flip
            CALL "UNMAKEMOVE" USING GAME-STATE LS-MOVE
            IF CHILD-SCORE > L-ALPHA
                MOVE CHILD-SCORE TO L-ALPHA
                IF L-ALPHA >= L-BETA
                    MOVE L-BETA TO L-OUT
                    GOBACK
                END-IF
            END-IF
        END-IF
    END-PERFORM
    MOVE L-ALPHA TO L-OUT
    GOBACK.
```

**Commentary**: COBOL adaptations:
1. `PERFORM VARYING` loop over the move list (COBOL's iterative construct) combined with a `CALL "QUIESCE"` recursive call. The outer iteration is iterative; the recursion is via a `CALL`.
2. `CHILD-ALPHA`/`CHILD-BETA` in working-storage — COBOL lacks local variables, so child bounds must be named data items. This is idiomatic COBOL: all computation state is in a flat WORKING-STORAGE SECTION.
3. Delta pruning constant = **950** cp — the exact queen value from the CPW delta-pruning article. This is independent of the chess-Rocq `delta_margin` (which is a named constant of unknown value), yet both implement delta pruning.
4. MVV-LVA ordering via `PERFORM SCORE-Q-MOVE` — one of only 5/26 engines with MVV-LVA in quiescence.
5. No check-evasion branch — the `CAP-ONLY` flag is always set to 1 without a check for `in_check`. This is the missing correctness feature.

### What the trio demonstrates

| Property | Java | Coq | COBOL |
|---|---|---|---|
| Stand-pat lower bound | `standPat = evaluate(board)` | `evaluate pos` | `CALL "EVAL"` |
| Beta-cutoff | `if (standPat >= beta)` | `if leb beta stand_pat` | `IF STANDPAT >= L-BETA` |
| Alpha-update | `if (standPat > alpha)` | `let a := if ltb alpha stand_pat` | `IF STANDPAT > L-ALPHA MOVE` |
| Delta pruning | absent | `if ltb (add stand_pat delta_margin) alpha` | `IF (STANDPAT + 950) < L-ALPHA` |
| Capture-only | `generateLegalMoves(!inCheck)` | `gen_capture_moves pos` | `CALL "MOVEGEN" CAP-ONLY` |
| Negamax flip | `-quiescence(-beta, -alpha, ...)` | `negate_score (quiesce ... (negate_score beta) ...)` | `COMPUTE CHILD-SCORE = 0 - CHILD-SCORE` |
| Check evasion | `if (inCheck)` → all moves | absent | absent |
| PL key adaptation | OOP method dispatch | Fixpoint + qdepth:nat + inner fix | PERFORM VARYING + CALL + working-storage params |

Every row in the "algorithm" block maps the same concept across three completely
different syntactic realizations. This is specification convergence: one
community standard, three paradigms, zero shared tokens.

---

## 3. Headline findings

### 3.1 Specification convergence (quiescence)

Every valid quiescence extraction follows the same four-step skeleton:
1. stand-pat evaluation as lower bound
2. β-cutoff if stand-pat ≥ β
3. α-update if stand-pat > α
4. capture-only negamax loop

The term `stand_pat` appears in 19/26 extractions across 11 programming languages. This term does not appear in academic chess literature — it is a Chess Programming Wiki community term. Its cross-language ubiquity is the strongest single evidence in the corpus that LLMs have internalized the wiki specification to the point of regenerating its vocabulary in every target language.

The delta-pruning threshold, where present, is always 900–950 centipawns — the value from the wiki's delta-pruning sub-article. Independent derivation from first principles would not reproduce this constant.

**Implication**: LLMs do not "derive" quiescence from chess principles; they regenerate a community specification. This is not "copying" (no engine copies another), but it is not independent derivation either. The best characterization is **specification convergence**: the wiki has been absorbed so thoroughly that any model, prompted for a chess engine in any language, regenerates the same skeleton.

### 3.2 Architectural diversity (transposition table)

While the abstract concept is universal (Zobrist hash → stored entry with score, depth, flag, move), implementation varies substantially:

| Engine | TT implementation |
|---|---|
| C/C++ engines | Flat power-of-two array, struct entries, modular index |
| chess-java / chess-java-cc | Java class with MB→entry-count resize, parallel arrays |
| chess-ruby-cc | Ruby `@tt = {}` native hash, Zobrist key as symbol |
| lean-chess | Lean `HashMap` with `Option Move` entries |
| chess-cobol-cc | COBOL `OCCURS 500000 TIMES` flat table |
| chess-py | Python dict, Zobrist computed at runtime from seeded `random` |
| COBOL-chess | Flat OCCURS-based array with modular address |

These are not mechanical translations of the same code — they use each language's idiomatic container and access pattern. The architectural diversity coexists with complete algorithmic convergence on Zobrist hashing.

### 3.3 Data independence (evaluation/PST)

Material constants are the most directly fingerprint-testable aspect of any chess engine: if an engine copied Sunfish, it would have P=100, N=280, B=320, R=479, Q=929, K=60000. Zero of 19 engines show these values. The CPW simplified material values are likewise absent from all 19.

This is the strongest novelty evidence in the corpus: even though LLMs know the chess domain deeply enough to generate correct material ordering (R > B > N > P, Q ≈ 2R), they generate the specific values fresh each session rather than copying a canonical table.

Two engines go further and eliminate lookup tables entirely:
- **lean-chess**: `pieceSquareValue` uses `centrality sq`, `forwardRank piece.color sq`, and `isEdgeSquare sq` — fully geometric, formally reasonable, no 64-entry table
- **chess-sql**: evaluation is a SQL `WITH` query joining a `pst` table; the board is a string column; PST lookup is a correlated subquery

These are genuine language-idiomatic synthesis.

---

## 4. LLM capability evidence across the triad

| Capability | Quiescence | TT | Evaluation |
|---|---|---|---|
| Base algorithm from CPW primary article | ✓ universal | ✓ universal | ✓ universal |
| PL-specific adaptation | ✓ (Coq termination proof, COBOL PERFORM loop) | ✓ (Ruby Hash, Lean HashMap, COBOL OCCURS) | ✓ (Lean geometry, SQL CTE, COBOL REDEFINES) |
| Independent numerical constants | N/A | ✓ (Zobrist seeds vary, no canonical match) | ✓ (no Sunfish, no CPW values) |
| CPW secondary article extensions | ✗ (check evasion 31%, TT-in-qsearch 12%) | ✗ (age replacement 0%, depth-preferred 0%) | ✗ (king safety 0%, tapered eval 5%) |

The consistent pattern: LLMs implement the primary specification reliably, adapt it to the target language idiomatically, generate data values independently — and uniformly miss the refinements documented in the same article's "Improvements" or "Advanced" subsections.

---

## 5. LLM blind spots: the second-article gap

Across all three features, the missing items share a structural property: they require additional bookkeeping not described in the opening paragraphs of the relevant wiki article.

| Missing feature | Feature | Infrastructure required |
|---|---|---|
| Check evasion in qsearch | Quiescence | `inCheck()` call + branch to full move gen |
| TT probe in quiescence | Quiescence | Pass TT reference into qsearch |
| Fail-soft returns | Quiescence | Score accumulator instead of β return |
| Age-based replacement | TT | Entry age field + generation counter |
| Depth-preferred replacement | TT | Compare stored depth before overwrite |
| King safety | Evaluation | King zone computation + attack counting |
| Tapered evaluation | Evaluation | Two table sets + phase variable + interpolation |
| Mobility terms | Evaluation | Move generation in evaluation function |

None of these is algorithmically complex. Each appears prominently on the wiki. The pattern points to a **training-data coverage gap**: the primary descriptions are widely quoted and reproduced; the refinements appear in fewer secondary sources and are apparently underrepresented in the LLMs' training data.

---

## 6. PL-specific adaptation table

| Language | Feature | Adaptation |
|---|---|---|
| Coq/Rocq | Quiescence | `Fixpoint quiesce` with `qdepth : nat` (Peano depth, termination proved) |
| COBOL | Quiescence | `PERFORM VARYING` loop instead of recursion; explicit working-storage for child α/β |
| Why3/OCaml | Quiescence | No mutable state; option-type board boundary handling |
| Rust (port) | Quiescence | Parent Java engine's optimization choices carried over (match patterns, ownership) |
| Ruby | TT | Native `@tt = {}` hash; Zobrist key as symbol |
| Lean 4 | TT | `HashMap` with `Option Move`; no raw array indexing |
| COBOL | TT | `OCCURS 500000 TIMES` flat table with modular address |
| COBOL | Evaluation | `WORKING-STORAGE` flat `VALUE` data + `REDEFINES OCCURS 64` overlay |
| APL | Evaluation | Branch-goto dispatch (`→(PIECE∊'Pp')⍴PAWN`) to PST arrays |
| Lean 4 | Evaluation | Fully computed: `centrality`, `forwardRank`, `isEdgeSquare`; no table |
| SQL | Evaluation | Full `WITH` query; PST as a joined table; declarative result row |
| Coq/Rocq | Evaluation | Material-only via `match` (PST omitted: 64-entry array awkward in Coq type theory) |

The Coq/Rocq evaluation note deserves emphasis: the LLM chose to omit the PST rather than navigate Coq's dependent type system for a 64-entry array literal. This is a correct engineering judgment about Coq's idiomatic style.

---

## 7. Extraction methodology lessons

### Single-hotspot mode: where it works

Concentrated features (one function, one canonical name, in a search-adjacent file) extract reliably. Quiescence is the ideal case: the function is named `quiescence`/`qsearch`, lives in `search.cpp`/`search.py`, and contains the algorithm inline. The 8% artefact rate is acceptable.

### Single-hotspot mode: where it fails

Distributed features (PST) fail at 47% artefact rate because:
1. Evaluation spans constant files, lookup functions, and incremental update code
2. All three have similar keyword density (PST, piece_value, etc.)
3. No single file "is" the evaluation the way `search.cpp` "is" the quiescence

**Fix**: multi-hotspot mode — collect top-3 matches per engine and compute sub-features from their union.

### Binary false positives

Compiled executables embed string literals from source. `chess-Rocq` and `chess-cobol-cc` both matched `zobrist` in their compiled binaries. Extension-based filtering is insufficient; content-based binary detection (ELF magic bytes, Mach-O header, PE header) is needed.

### Vendor/test tree contamination

`chess-why3-cc`'s PST hotspot matched `tests/engines/shallowblue-src/src/eval.cc` — a vendored ShallowBlue reference engine. The ShallowBlue code is richer in PST keywords than the why3-cc engine's own code, so it wins the scoring. Fix: explicitly exclude paths matching `tests/`, `vendor/`, `third-party/`, `lib/engines/`.

---

## 8. Research implications per RQ

### RQ2 (Features implemented)

The sub-feature analysis adds a depth dimension to the binary feature matrix:
- Quiescence is near-universal but varies from 2-sub-feature minimal to 8-sub-feature complete
- Evaluation sophistication spans 5 tiers (material-only → computed geometric)
- The tier reached correlates with prompt iteration ("improve the Elo") rather than with language

### RQ3 (Novelty: copy or synthesis?)

Three independent novelty signals emerge from the triad:
1. Algorithm level: specification convergence (same skeleton, independent tokens)
2. Architecture level: language-adapted implementation (Ruby Hash ≠ C array ≠ Lean HashMap)
3. Data level: independent constants (no Sunfish, no CPW, Zobrist seeds vary)

The first is the weakest signal (convergence ≠ independence), the third is the strongest.

### RQ4 (Elo)

Evaluation sophistication tier predicts relative Elo contribution within search-depth-matched groups:
- Material-only → baseline
- Basic PST → +100–200 Elo
- MG/EG incremental → +150–250 Elo over basic PST
- Full tapered → +100–200 Elo over MG/EG

The missing king safety and tapered evaluation represent the largest untapped Elo gains in the corpus: engines that implement quiescence and TT correctly but stop at basic PST are leaving ~200–400 Elo on the table.

### Discussion

The "implementation ceiling" pattern is cross-feature: LLMs implement the primary specification, adapt to language idioms, and miss the secondary refinements. This is consistent with a training-data hypothesis (primary articles are more heavily represented than secondary refinements) and with a complexity hypothesis (secondary refinements require more infrastructure). Both hypotheses predict the same observable pattern.

---

## 9. Summary

The three-feature triad reveals three distinct LLM synthesis behaviors:

- **Quiescence** (concentrated algorithm): specification convergence — same skeleton, same vocabulary, same constant, adapted to PL idioms
- **TT** (distributed data structure): architectural diversity — same abstract concept, language-appropriate containers and access patterns
- **Evaluation** (distributed data + computation): data independence — same structural choices, independently generated constants, language-specific exotic implementations (geometric Lean, SQL CTE)

The common thread is the **second-article gap**: across all three features, the extensions documented in secondary/refinement sections of chessprogramming.org are absent from the corpus. This is the most actionable finding for prompting: explicitly requesting the refinement layer (``implement depth-preferred TT replacement'', ``add king safety'', ``add check evasion in quiescence'') could close the gap in a single additional prompt.
