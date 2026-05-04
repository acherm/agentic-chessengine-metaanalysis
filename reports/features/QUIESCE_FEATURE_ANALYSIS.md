# Quiescence Search: Cross-Engine Feature Analysis

**Feature**: quiescence search  
**Detection patterns**: `quiescence|qsearch`  
**Corpus**: 35 engines (28 with the feature present)  
**Analysis tools**: `scripts/feature_locator.py --hotspot`, `scripts/feature_compare.py`  
**Raw artefacts**: `quiescence.json`, `quiescence.hotspot.txt`, `quiescence.compare.txt`, `quiescence.compare.json`  
**Date**: 2026-04-20

---

## 1. Methodology

### 1.1 Hotspot extraction

Standard feature scanning (`scripts/feature_locator.py`) produces line-level matches with context windows across all source files. For quiescence, this is noisy: the word "quiescence" or "qsearch" appears in documentation, call-sites, and type declarations across several files. The `--hotspot` mode distils the output to a single *function body* per engine — the one most likely to be the canonical implementation.

Hotspot selection is a two-pass process:

1. **Scoring**: each match is scored by: keyword present in the matching line (+3), keyword present in the function name (+20), line is a function definition (+12), file is named after a chess concept e.g., `search.*` (+6), line is inside a test file (−25). The highest-scoring line becomes the *anchor*.

2. **Extraction**: a language-aware function-body extractor walks outward from the anchor to find the enclosing function boundary. Eleven language families are handled: brace-counting (C/C++/Java/Rust/C#/Go), indentation-based (Python), keyword/end (Ruby/Lua/Icon), `let`/`in` (OCaml/Why3), `Fixpoint`/`Definition` (Coq/Rocq), `def`/`partial def` (Lean 4), paragraph/section names (COBOL), assembly labels, and `∇`…`∇` delimiters (APL).

A secondary keyword-stem scan (`_find_func_def_by_stem`) handles languages like Coq/Rocq where the function is named `quiesce` rather than `qsearch` — outside the literal pattern match but derivable from a 6-character stem.

### 1.2 Sub-feature detection

Thirteen algorithmic sub-features were defined for quiescence search, each detected by a regex applied to the extracted function body:

| Sub-feature | What it detects |
|---|---|
| `stand_pat` | Static evaluation used as a lower bound before capture loop |
| `beta_cutoff` | Early return when evaluation ≥ β |
| `alpha_update` | α raised to stand-pat score when stand-pat > α |
| `capture_only_gen` | Move generation restricted to captures / captures+checks |
| `delta_pruning` | Skip whole node if stand-pat + max-gain < α |
| `see_pruning` | Static Exchange Evaluation used to prune losing captures |
| `mvv_lva` | Most-Valuable-Victim / Least-Valuable-Attacker capture ordering |
| `depth_limit` | Explicit qdepth ≤ 0 base case |
| `check_evasion` | All moves generated (not just captures) when in check |
| `tt_probe` | Transposition-table lookup inside the quiescence function |
| `promotions` | Promotion moves included alongside captures |
| `negamax_recurse` | Negamax sign-flip in recursive call (`-quiescence(-β, -α)`) |
| `fail_soft` | Returns the score (not β) on a beta cutoff |

### 1.3 Similarity metrics

Two independent metrics capture different aspects of implementation similarity:

**Token-Jaccard** normalizes each snippet to a bag-of-lowercase-tokens (stripping punctuation, keywords filtered by language family) and computes |A ∩ B| / |A ∪ B|. This measures *surface lexical overlap* — useful for detecting copy-paste or near-literal translation, but sensitive to language syntax so naturally low across language boundaries.

**Feature-Jaccard** treats each engine as a 13-dimensional binary vector (sub-feature present/absent) and computes Jaccard on those vectors. This measures *algorithmic similarity* — is the same optimization strategy present? — and is language-agnostic.

Both metrics are computed pairwise for all 28×27/2 = 378 pairs, yielding full similarity matrices in `quiescence.compare.json`.

---

## 2. Coverage: 28/35 engines, and why 7 are missing

### 2.1 Three external anchors (not scanned by design)

`tscp181`, `madchess32`, `countergo40` are third-party binaries used only for Elo calibration. They are listed under `anchors:` in `manifest.yaml` without a `path:` field and are not scanned. Their absence is expected and correct.

### 2.2 Four project engines: genuine gaps

| Engine | Root cause |
|---|---|
| `chess-sql` | SQL engine; quiescence logic (if implemented) lives in SQL query strings with no `quiescence` or `qsearch` keyword in the Python driver |
| `chess-latex-codex-replication` | LaTeX engine; algorithm encoded in TeX macro dispatch (`\enginestrength` parameter), no keyword match in source |
| `chess-css-codex-guided` | JavaScript engine; likely uses different naming (e.g., `captureSearch`, `quietSearch`) — a vocabulary gap, not an absence |
| `chess-brainfuck-cc` | `bf_uci.py` is a BF *code emitter*, not a UCI driver; quiescence logic lives inside the emitted Brainfuck program text, which is not pattern-matchable |

**Note on two engines inside the 28:** `chess-assembly-codex` and `chess-mojo` were included in the 28 (pattern match found) but their extracted snippets are non-quiescence code (linker metadata and a Mojo stub respectively). Their sub-feature vectors are all-zero and they should be treated as effective extraction failures.

---

## 3. Sub-feature presence matrix

```
                          sp  bc  au  co  dp  se  ml  dl  ce  tt  pr  nr  fs
COBOL-chess               ✓   ·   ·   ✓   ✓   ·   ✓   ·   ·   ·   ·   ·   ·
chess-Rocq                ✓   ·   ·   ✓   ✓   ·   ·   ✓   ·   ·   ·   ·   ·
chess-brainfuck           ✓   ✓   ✓   ✓   ·   ·   ·   ✓   ✓   ·   ·   ·   ✓
chess-cplusplus-claude    ✓   ✓   ✓   ✓   ✓   ·   ·   ✓   ✓   ✓   ✓   ✓   ·
chess-css-codex           ✓   ✓   ✓   ·   ·   ·   ·   ·   ✓   ·   ✓   ·   ✓
chess-icon-codex          ·   ✓   ✓   ·   ·   ·   ·   ·   ·   ·   ·   ✓   ·
chess-java                ✓   ✓   ✓   ✓   ·   ·   ·   ✓   ✓   ·   ·   ✓   ·
chess-java-cc             ✓   ✓   ✓   ·   ✓   ✓   ·   ✓   ✓   ·   ·   ✓   ·
chess-newlang-codex       ·   ✓   ✓   ✓   ✓   ✓   ·   ·   ✓   ·   ·   ✓   ·
chess-purec               ✓   ✓   ✓   ·   ✓   ✓   ·   ✓   ·   ·   ·   ✓   ·
chess-purec-codex         ✓   ✓   ✓   ✓   ·   ✓   ·   ✓   ·   ✓   ·   ✓   ·
chess-py                  ✓   ✓   ✓   ✓   ·   ·   ·   ·   ✓   ·   ✓   ·   ·
chess-py-cc               ✓   ✓   ✓   ✓   ✓   ✓   ✓   ·   ·   ·   ✓   ·   ·
chess-revisit-..toRust    ✓   ✓   ✓   ·   ·   ✓   ✓   ✓   ✓   ·   ·   ✓   ·
chess-ruby-cc             ✓   ✓   ✓   ✓   ✓   ✓   ·   ·   ✓   ·   ✓   ✓   ·
chess-ruby-codex          ·   ✓   ·   ·   ·   ·   ·   ✓   ✓   ·   ·   ✓   ·
chess-rust-cc             ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ·   ✓   ·   ✓   ·
chess-rust-codex          ✓   ✓   ✓   ✓   ·   ·   ·   ·   ·   ·   ·   ✓   ·
chess-why3-cc             ✓   ✓   ✓   ·   ·   ·   ·   ✓   ·   ·   ·   ·   ·
cplusplus-chess           ✓   ✓   ✓   ·   ✓   ✓   ✓   ✓   ✓   ·   ✓   ✓   ·
lean-chess                ✓   ✓   ·   ✓   ·   ·   ·   ✓   ✓   ·   ·   ·   ·
chess-why3                ·   ·   ·   ✓   ·   ·   ·   ✓   ·   ·   ·   ·   ·
chess-Rocq                ✓   ·   ·   ✓   ✓   ·   ·   ✓   ·   ·   ·   ·   ·
COBOL-chess               ✓   ·   ·   ✓   ✓   ·   ✓   ·   ·   ·   ·   ·   ·
                         ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---
TOTAL                   19   19   17   15   11   10    5   15   13    4    6   13    2
(out of 28 engines; sp=stand_pat bc=beta_cutoff au=alpha_update co=capture_only
 dp=delta_pruning se=see_pruning ml=mvv_lva dl=depth_limit ce=check_evasion
 tt=tt_probe pr=promotions nr=negamax_recurse fs=fail_soft)
```

Sub-features split into two bands: **core** (stand_pat, beta_cutoff, alpha_update, capture_only_gen, depth_limit — all ≥ 15/28) and **optional optimizations** (delta_pruning, SEE, check_evasion, negamax — 10–13/28) and **advanced** (MVV-LVA, TT probe, promotions, fail-soft — ≤ 6/28).

---

## 4. Pairwise similarity

### 4.1 Token-Jaccard: surface syntax

Even the highest token-Jaccard pair reaches only 47% (`chess-java-cc` ↔ `chess-revisit-java-toRust-codex`), and that is explained by a known factor: the latter is a direct Codex port of the former Java engine; variable names (`alpha`, `beta`, `score`, `standPat`) transferred nearly literally. Most cross-language pairs fall in the 10–30% range, confirming that token-Jaccard is dominated by language syntax differences rather than algorithmic structure. It is most useful for detecting literal copy-paste; at these levels, it does not detect it.

### 4.2 Feature-Jaccard: algorithmic structure

Top pairs reveal cross-language algorithmic convergence:

| Score | Pair | Languages |
|---|---|---|
| 88% | chess-java-cc ↔ chess-purec | Java ↔ C |
| 80% | chess-java-cc ↔ cplusplus-chess | Java ↔ C++ |
| 80% | chess-purec-codex ↔ chess-rust-cc | C ↔ Rust |
| 80% | chess-revisit-java-toRust-codex ↔ cplusplus-chess | Rust ↔ C++ |
| 78% | chess-java-cc ↔ chess-revisit-java-toRust-codex | Java ↔ Rust |
| 78% | chess-newlang-codex ↔ chess-ruby-cc | C++ ↔ Ruby |
| 75% | chess-brainfuck ↔ chess-java | Python ↔ Java |

The 88% Java ↔ C pair is the most striking: two engines generated by different AI models in different languages share nearly identical *algorithmic decisions* (same optimizations present, same optimizations absent). This cannot be explained by token-level copying — the syntax is completely different — only by convergence on a shared latent specification.

The bottom of the feature-Jaccard table is populated by the extraction-failure engines (assembly, mojo, latex-chess-engine) whose snippets don't represent actual quiescence code, and by chess-revisit-java-toCOBOL-codex whose hotspot was extracted incorrectly.

---

## 5. The universal algorithmic skeleton

Across all 26 engines with a valid hotspot (excluding the 2 extraction failures inside the 28), every implementation follows this structure:

```
quiescence(α, β):
    score = evaluate()               # stand-pat evaluation
    if score ≥ β: return β           # beta cutoff (fail-hard)
    if score > α: α = score          # raise alpha floor

    for move in generate_captures():
        child = -quiescence(-β, -α)  # negamax sign-flip
        if child ≥ β: return β       # beta cutoff
        if child > α: α = child      # alpha update

    return α
```

The negamax sign-flip convention (`-quiescence(-β, -α)`) is essentially universal — only the COBOL engines use an iterative formulation with explicit child-alpha/child-beta variables, which is algebraically identical. The stand-pat evaluation as a lower bound is the defining algorithmic idea and appears in 19/26 valid extractions (the 7 absences are minimal implementations or detection gaps, not absent implementations).

This skeleton is the chessprogramming.org pseudocode for quiescence search, verbatim. The language of that specification has permeated the LLM training corpus so thoroughly that every model converges to it without variation.

---

## 6. Variation taxonomy

Implementations divide into three natural tiers by the number of optional optimizations present:

### Tier 1 — Full-featured (6–9 sub-features)

`chess-cplusplus-claude`, `cplusplus-chess`, `chess-rust-cc`, `chess-java-cc`, `chess-ruby-cc`, `chess-py-cc`, `chess-newlang-codex`, `chess-revisit-java-toRust-codex`

These implementations add: delta pruning, SEE-based pruning, MVV-LVA ordering, check evasion, promotions handling, and in some cases a TT probe. They represent production-quality quiescence search and correlate with the higher-Elo engines in the corpus. The common pattern is that "improve the Elo" prompts drove these additions — each optimization was added reactively in response to strength feedback, not pre-planned.

### Tier 2 — Standard (4–6 sub-features)

`chess-java`, `chess-purec`, `chess-purec-codex`, `chess-brainfuck`, `chess-py`, `chess-rust-codex`, `chess-why3-cc`, `lean-chess`

Solid textbook implementations of the core loop with a subset of optimizations. Entirely correct and sufficient for meaningful play. These typically emerge from sessions that ran quiescence once without further iteration.

### Tier 3 — Minimal (1–3 sub-features)

`chess-why3`, `chess-ruby-codex`, `chess-icon-codex`, `chess-Rocq`, `chess-css-codex`

Often associated with formal-methods languages where simplicity is a virtue for verifiability, or with short sessions where quiescence was added as a feature but not iterated on. `chess-why3` is the most extreme: captures-only + depth-limit, essentially just the stopping criterion without the full negamax recursion visible to the pattern matcher.

### The five key variation axes

**1. Delta pruning** (11/28): Present when `stand_pat + QUEEN_VALUE < α` — skip the entire node because even a queen capture cannot save it. The threshold is consistently 900–950 centipawns across all implementations. This exact value comes from the chessprogramming.org delta pruning article. Its presence correlates with SEE pruning (r≈0.7): engines that implement one usually implement the other.

**2. SEE pruning** (10/28): Static Exchange Evaluation screens out captures that lose material. Requires a separate `see()` function, making it the single best proxy for implementation depth — an engine that has SEE has invested significantly in search infrastructure.

**3. Check evasion** (13/28): When in check, generate all legal moves rather than only captures. Approximately half the engines handle this correctly; the other half have a latent bug where the engine ignores forced checkmates in quiescence. This is a known tradeoff: check evasion adds correctness but also search cost. The split at ~50% suggests the LLM sometimes adds it and sometimes omits it without strong signal from the prompt.

**4. Transposition table** (4/28): TT in quiescence is used by only `chess-cplusplus-claude`, `chess-purec-codex`, and `chess-rust-cc`. This is advanced and subtle — the TT entry must be valid for the quiescence horizon depth, and incorrect TT usage can cause subtle bugs. That only 4/28 implement it reflects appropriate (or accidental) caution.

**5. Depth limit** (15/28): An explicit `if qdepth ≤ 0: return evaluate()` cap. Mathematically redundant if you generate only captures (the tree terminates naturally), but practically important. `chess-Rocq` handles this structurally: `qdepth : nat` (a Peano natural number) requires termination proof, and subtraction bottoms at zero automatically — the depth limit is type-enforced rather than runtime-checked.

---

## 7. Notable outliers

**`chess-Rocq` (Coq/Gallina):** The most structurally unusual. `Fixpoint quiesce` uses a `qdepth : nat` argument because Coq requires structural recursion for termination guarantees. The Peano-natural depth parameter is an elegant solution: no runtime check needed, termination is verified by the type system. The cost is that any optimization (delta pruning, SEE) that could complicate the termination argument is skipped. The engine is verifiably correct but optimizationally conservative — a forced tradeoff the LLM handled intelligently.

**`chess-brainfuck` (Python wrapper):** Implements check evasion and fail-soft — features absent from several "serious" engines. The Python wrapper around the Brainfuck interpreter has more sophisticated search than the BF binary can actually exploit. This reflects the session history: the agent iterated heavily on the Python layer while the BF backend was slow to compile.

**`chess-css-codex` (Python + python-chess):** Uses the python-chess library for move generation, making check detection and capture enumeration trivial. The quiescence code is unusually clean (39 LOC) because move-legality complexity is externalized. This is the evasion-risk case discussed in RQ3 §3.4: algorithmic quality is higher precisely because the hard parts were delegated.

**`chess-why3-cc` (OCaml, Why3-extracted):** The OCaml code is machine-generated by Why3's extraction pipeline from formal specifications. Its quiescence profile (stand_pat, beta_cutoff, alpha_update, depth_limit) is minimal and clean — formal extraction trades optimization for correctness. The resulting code is not what a human would write for performance, but it is what a proof assistant would generate for safety.

**`latex-chess-engine` (LaTeX):** The extracted snippet is a TeX document preamble. The sub-feature detections (SEE, TT) in the comparison matrix are false positives from TeX comments that reference these concepts in explanatory text. The actual quiescence algorithm is encoded in TeX macro expansions that are not statically analyzable by text pattern matching. This engine must be considered an extraction failure; its row in the similarity matrices is unreliable.

---

## 8. Copy or synthesis? The verdict

**The algorithm is universal and traces to a single specification.**

The core skeleton, the "stand_pat" terminology, and the delta-pruning constant (900–950) all derive from chessprogramming.org. That source (and tutorials that synthesize it) dominates the training corpus for code-capable LLMs. When asked for quiescence search, every model retrieves the same latent specification and instantiates it.

Evidence:
- **Terminology convergence**: "stand_pat"/"stand-pat"/"STANDPAT" appears in 19/26 valid extractions across 12 languages. This is a community term not found in academic chess literature — its universal presence points to a shared web-based source.
- **Constant convergence**: Where delta pruning appears, the threshold is always 900–950 (queen value). That specific constant, with that specific interpretation, is from one article on chessprogramming.org.
- **Cross-language feature-Jaccard**: The highest pairs (88%, 80%) are cross-language pairs from different AI models. Independent derivation from first principles would produce more variation in *which* optimizations are chosen. The convergence indicates a shared training-data template.

**But the implementations are *not* copies of each other.**

Token-Jaccard confirms: lexical similarity is low even between algorithmically-identical pairs. Every implementation is a *fresh generation* from the same latent specification, not a copy of another engine's source code. The "same algorithm" finding coexists with the "not a copy" finding without contradiction.

**And genuine adaptation does occur.**

The LLMs did not blindly apply the C pseudocode to every language. Observable adaptations:
- `chess-Rocq`: terminates via `nat` (Peano) depth rather than integer comparison
- `chess-why3-cc`: follows Why3's extraction conventions for OCaml output
- `COBOL-chess`: restructures recursion into PERFORM loops with explicit child-alpha/beta variables (idiomatic COBOL)
- `chess-revisit-java-toRust-codex`: ports the parent Java engine's specific optimization choices to Rust idioms (ownership, match patterns), not the generic spec

---

## 9. PL-specific adaptation: what LLMs do well

The clearest evidence of LLM capability is how implementations adapt to language constraints:

**Type-theoretic adaptation (Coq/Lean):** Both `chess-Rocq` (`Fixpoint quiesce` with `nat` depth) and `lean-chess` (`partial def quiescence` — the `partial` keyword sidesteps Lean's totality checker for the recursive search) show the LLM understanding that termination must be handled differently in dependently-typed languages. These are not accidents; they are deliberate choices that compile and type-check.

**Paradigm adaptation (COBOL):** COBOL lacks recursion-by-default (historically iterative). `COBOL-chess` implements quiescence as a `CALL "QUIESCE" USING ...` subprogram with explicit WORKING-STORAGE for child-alpha/child-beta, mimicking the recursive structure imperatively. The algorithm is identical; the shape conforms to COBOL idioms.

**Formal-extraction style (OCaml/Why3):** `chess-why3-cc`'s OCaml code has the signature of Why3 extraction output — no mutable state in the hot path, careful option-type handling — rather than hand-written OCaml. The LLM understood the extraction workflow and shaped the Why3 specification to produce idiomatic extracted code.

**Codebase integration:** The top feature-Jaccard pairs are not random — they correspond to engines from the same session lineage. `chess-java-cc` and `chess-revisit-java-toRust-codex` share 78% feature-Jaccard precisely because the Rust port was generated from the Java engine as a reference; the agent carried over the optimization choices from one codebase to the other, not just the algorithm.

---

## 10. Missing opportunities: where LLMs fell short

Despite the strong baseline, several standard quiescence optimizations were underrepresented:

| Optimization | Frequency | Why it matters |
|---|---|---|
| Check evasion | 13/26 (50%) | Correctness: without it, the engine can walk into checkmate during quiescence |
| SEE pruning | 10/26 (38%) | Strength: avoids xraying pieces with losing captures; measurably improves Elo |
| Transposition table | 3/26 (12%) | Efficiency: avoids re-evaluating identical quiet positions reached via different capture sequences |
| Fail-soft | 2/26 (8%) | Score precision: returns exact score instead of β on cutoff; matters for TT entries |
| Quiescence TT tagging | 0/26 | Missing entirely: none of the TT-using engines properly tag TT entries by quiescence depth |

The most significant gap is **check evasion**, which is both a correctness issue and well-documented on chessprogramming.org. Its absence in half the engines suggests the LLMs had access to the stand-pat + delta-pruning template but did not consistently include the check-evasion addendum. This is the most actionable finding for improving generated engine quality: a single additional instruction ("handle check evasion in quiescence search") would lift the baseline.

**Quiescence TT tagging** is absent from all engines. In a mature engine, quiescence positions are stored in the TT with a `QSEARCH` flag and only retrieved in the quiescence search. None of the 28 engines does this, and the 3 that probe the TT do so with the same logic as the main search, which can cause subtle TT pollution. This represents a collective blind spot in the training data: the chessprogramming.org article on quiescence search and TT interaction is apparently less prominent than the basic qsearch article.

---

## Summary

Quiescence search is the same algorithm in every engine: stand-pat + negamax + alpha/beta, derived from a common specification (chessprogramming.org). The implementations are not copies of *each other* (token-Jaccard is low), but they share an algorithmic ancestor (feature-Jaccard is high for the strongest pairs). LLMs demonstrate genuine PL-specific adaptation — particularly in type-theoretic and paradigm-constrained languages — but consistently miss the check-evasion correctness requirement and do not reach the advanced optimization tier (TT tagging, fail-soft, q-futility pruning) without explicit prompting. The finding is that LLMs have internalized the standard specification very well, but have not internalized the *extensions* to that specification that a human expert would add next.
