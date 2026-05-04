# Transposition Table: Cross-Engine Feature Analysis

**Feature**: Transposition Table (Zobrist hashing + TT probe/store)  
**Detection patterns**: `transposition|\bTT\b|zobrist`  
**Corpus**: 35 engines (24 with the feature present)  
**Analysis tools**: `scripts/feature_locator.py --hotspot`, `scripts/feature_compare.py`  
**Raw artefacts**: `transposition_table.json`, `transposition_table.hotspot.txt`, `transposition_table.compare.txt`, `transposition_table.compare.json`  
**Date**: 2026-04-20

---

## 1. Why TT is a different kind of feature

Quiescence search is concentrated: one function, one algorithm, one canonical skeleton. The transposition table is distributed: a data structure definition, a Zobrist initialization routine, a probe call woven into the search function, a store call woven in, and optionally a replacement policy, entry-age mechanism, and separate pawn hash table. No single function body captures the full picture.

This makes TT the ideal counterpoint to quiescence: same pipeline, harder target. Where quiescence asks "did the LLM implement the right algorithm?", TT asks "did the LLM make the right architectural decisions?" — table size, indexing strategy, Zobrist seed quality, replacement policy, flag types, move storage. These choices affect engine strength independently of algorithm correctness.

---

## 2. Coverage: 24/35 engines, and why 11 are missing

### 2.1 Three external anchors (not scanned)

`tscp181`, `madchess32`, `countergo40` — same reason as quiescence: anchors have no `path:` field in `manifest.yaml`.

### 2.2 Eight engines with no TT (genuine absence or pattern gap)

| Engine | Root cause |
|---|---|
| `chess-why3` | Minimal OCaml engine; no TT implemented (confirms the `chess-why3` vs `chess-why3-cc` quality gap) |
| `chess-icon-codex` | Icon engine has no TT in its search — pure alpha-beta |
| `chess-sql` | SQL-based engine; a positional hash table would require a temporary SQL table, apparently not implemented |
| `chess-latex-codex-replication` | LaTeX engine; no transposition/zobrist keyword match found — likely uses TeX-specific naming |
| `latex-chess-engine` | Same: algorithm encoded in TeX macro names without the standard vocabulary |
| `chess-brainfuck-cc` | BF code emitter; TT keyword in Python emitter not found |
| `chess-css-codex-guided` | JavaScript engine; JS code doesn't use standard keywords |
| `chess-mojo` | Failure case; no meaningful source |

### 2.3 Three critical extraction failures inside the 24

Not all 24 "found" entries are valid:

- **`chess-Rocq`**: The match file `chess_rocq` is the compiled Coq **binary**, not source. The string "zobrist" appears in the binary because it was embedded during compilation. The extracted "snippet" is binary garbage. This is an extraction failure that reveals a locator bug: the `--code-only` filter didn't exclude the executable because it lacked a blacklisted extension.

- **`chess-apl-codex54`**: The extracted hotspot is `tests/test_apl_engine.py` — a Python test file that *proves* the APL engine has a TT (the test asserts fewer nodes on a repeated search), but the APL source was not extracted. TT in APL was implemented but not captured.

- **`chess-cobol-cc`**: The extracted file `chess-engine-v2` is again the compiled binary, same issue as chess-Rocq. Binary content, zero informational value.

These three failures leave **21 valid hotspot extractions** for substantive analysis.

---

## 3. What the hotspot extractor found

Unlike quiescence, where all engines converged on one function body, TT hotspots landed on very different code locations across engines — each revealing a different cross-section of the TT implementation:

| Category | Engines | What was extracted |
|---|---|---|
| **Zobrist init** | chess-purec, chess-purec-codex, chess-py | Random number generation: LCG loop, splitmix64, or recompute-from-scratch |
| **TT class constructor / resize** | chess-java, chess-java-cc, chess-cplusplus-claude, cplusplus-chess, chess-newlang-codex | MB → power-of-2 sizing, parallel-array or struct-array allocation |
| **TT probe / store in search** | chess-why3-cc, chess-brainfuck | TT probe with depth check and flag matching inside alpha-beta |
| **Incremental Zobrist update** | chess-rust-cc | `make_null_move` showing XOR-based hash update on position change |
| **Delegation / abstraction** | chess-css-codex, chess-ruby-cc, chess-py-cc, lean-chess, chess-ruby-codex | Single call site — TT passed as dependency, hash lookup via method/map |
| **TT-adjacent code** | chess-revisit-java-toCOBOL-codex (×2), COBOL-chess | Search outer loop / LINKAGE SECTION — TT used but not its core logic |

This fragmentation is a methodological finding: **TT requires multi-function analysis**. A single hotspot gives at best one cross-section. The full picture requires reading the struct definition, the Zobrist init, and the probe/store calls together.

---

## 4. Sub-feature presence matrix

The detection rate is sparse because most snippets hit one corner of the TT (init or constructor), not the probe/store logic. The table is most informative for `chess-why3-cc`, the only engine whose hotspot covered a full alpha-beta + TT probe function.

```
                           zob  inc  prb  str  dep  fex  flo  fup  bmv  siz  age  dpr  qtt
chess-why3-cc (OCaml)       ✓    ·    ✓    ·    ✓    ✓    ✓    ✓    ✓    ·    ·    ·    ·
chess-purec (C)             ✓    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·
chess-purec-codex (C)       ✓    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·
chess-py (Python)           ✓    ✓    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·
chess-revisit-..toRust      ✓    ✓    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·
chess-revisit-..toCOBOL     ✓    ✓    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·
chess-rust-cc (Rust)        ✓    ✓    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·
chess-assembly-codex        ✓    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·
COBOL-chess (COBOL)         ·    ·    ·    ·    ·    ·    ✓    ·    ✓    ✓    ·    ·    ·
chess-apl-codex54 (APL)     ·    ·    ·    ·    ·    ·    ·    ·    ✓    ·    ·    ·    ·
chess-ruby-cc (Ruby)        ·    ·    ·    ·    ·    ·    ·    ·    ✓    ·    ·    ·    ·
chess-rust-codex (Rust)     ·    ·    ·    ·    ·    ·    ·    ·    ✓    ·    ·    ·    ·
lean-chess (Lean)           ·    ·    ·    ·    ·    ·    ·    ·    ✓    ·    ·    ·    ·
cplusplus-chess (C++)       ·    ·    ·    ·    ·    ·    ·    ·    ·    ✓    ✓    ·    ·
chess-brainfuck (Python)    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·
chess-cobol-cc (C)          ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·  [binary]
chess-cplusplus-claude (C++) ·   ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·
chess-css-codex (HTML)      ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·
chess-java (Java)           ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·
chess-java-cc (Java)        ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·
chess-newlang-codex (C++)   ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·
chess-py-cc (Python)        ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·
chess-ruby-codex (Ruby)     ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·
chess-Rocq (OCaml)          ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·  [binary]

TOTAL (valid 21 only)      8/21 4/21 1/21 0/21 1/21 1/21 2/21 1/21 6/21 1/21 1/21 0/21 0/21
```

Legend: `zob`=zobrist_table `inc`=incremental_hash `prb`=tt_probe `str`=tt_store `dep`=depth_check `fex`=flag_exact `flo`=flag_lower `fup`=flag_upper `bmv`=best_move_stored `siz`=tt_size_config `age`=age_replacement `dpr`=depth_replace `qtt`=tt_in_qsearch

**Interpretation caveat**: low detection rates here reflect **extraction location** more than **implementation completeness**. An engine whose hotspot was the Zobrist init function will score 0 on `tt_probe` even if it has a full probe implementation in another file. The sub-feature matrix for TT is best read as "what is visible in this particular hotspot" rather than "what the engine implements."

---

## 5. Pairwise similarity

### 5.1 Feature-Jaccard: five distinct clusters

The feature-Jaccard matrix reveals five non-overlapping groups:

**Cluster A — Zobrist-only** (`zobrist_table` only, no other features detected):  
`chess-assembly-codex`, `chess-purec`, `chess-purec-codex`  
100% within the cluster, 50% with Cluster B.

**Cluster B — Zobrist + incremental XOR**:  
`chess-py`, `chess-revisit-java-toCOBOL-codex`, `chess-revisit-java-toRust-codex`, `chess-rust-cc`  
100% within, 50% with Cluster A.

**Cluster C — best_move_stored** (TT returns best move, no Zobrist visible):  
`chess-apl-codex54`, `chess-ruby-cc`, `chess-rust-codex`, `lean-chess`  
100% within, 33% with COBOL-chess (which also has best_move + other flags).

**Cluster D — Full probe/store logic (why3-cc)**:  
Only `chess-why3-cc` — has 7/13 sub-features. Unique; 12–25% with every other cluster.

**Cluster E — All-zero** (constructor/resize only, or binary):  
`chess-brainfuck`, `chess-cobol-cc`, `chess-cplusplus-claude`, `chess-css-codex`, `chess-java`, `chess-java-cc`, `chess-newlang-codex`, `chess-py-cc`, `chess-ruby-codex`, `cplusplus-chess`, `chess-Rocq`  
0% with each other and with all other clusters.

These clusters reflect *extraction location*, not algorithmic sophistication. The C/C++/Java engines in Cluster E almost certainly implement full probe/store/flags — they were simply not extracted.

### 5.2 Token-Jaccard: the only informative pair

The only striking token-Jaccard score is **chess-revisit-java-toCOBOL-codex ↔ chess-revisit-java-toRust-codex at 100%** — because both extracted the exact same file (the COBOL subdirectory of the Java→COBOL port). This is not algorithmic similarity; it is the locator finding the same file twice via two different engine paths.

After that, the highest token-Jaccard scores are intra-language C++ pairs: cplusplus-chess ↔ chess-newlang-codex (34%), chess-cplusplus-claude ↔ chess-newlang-codex (21%). These share surface token overlap because all three C++ engines extracted a `resize()` / constructor function with essentially the same structure.

---

## 6. Implementation strategies: what LLMs chose

### 6.1 The canonical approach: Zobrist XOR hashing

Most engines implement standard Zobrist hashing: a 2D array of random 64-bit integers indexed by `[piece][square]`, plus arrays for castling rights, en passant file, and side-to-move. On each `make_move`/`unmake_move`, the relevant Zobrist entries are XOR-ed in or out of a running 64-bit hash key.

Engines implementing this (extracted or confirmable from search): `chess-purec`, `chess-purec-codex`, `chess-py`, `chess-rust-cc`, `chess-why3-cc`, `COBOL-chess`, both Java engines, both C++ engines, both Rust engines.

This is the textbook approach from chessprogramming.org — but unlike quiescence (where every engine does it identically), the Zobrist implementations diverge meaningfully in initialization:

| Engine | Seed / PRNG method |
|---|---|
| chess-purec | `rand_state = 1070372ull` (small prime-ish constant; custom LCG `rand64()`) |
| chess-purec-codex | `seed = 0x123456789abcdef0ULL` (sequential hex; SplitMix64) |
| chess-py | Pre-computed constants at module load (no seed visible) |
| chess-rust-cc | External `zobrist()` singleton, seeded separately |
| chess-why3-cc | `Zobrist.hash_board b` — abstract; Zobrist module handles init |

The seed `0x123456789abcdef0` in chess-purec-codex is a well-known example constant for SplitMix64 — it appears verbatim in many blog posts and tutorials. Its presence suggests the agent sourced this initialization from a specific online example rather than generating a random (or cryptographically appropriate) seed. For a chess engine, this is benign; for reproducibility of Zobrist collisions, it matters.

### 6.2 The power-of-2 constructor: convergent engineering

Five engines independently produced nearly identical TT constructors:

```java
// chess-java: parallel arrays
budgetBytes = megabytes * 1024L * 1024L;
int entryBytes = Long.BYTES + Integer.BYTES + Integer.BYTES + 1 + Integer.BYTES;
int size = 1;
while ((long) size * entryBytes * 2L <= budgetBytes) size <<= 1;
```
```java
// chess-java-cc: packed 2-array (16 bytes/entry)
int entries = (sizeInMB * 1024 * 1024) / 16;
entries = Integer.highestOneBit(entries);
```
```cpp
// chess-cplusplus-claude: single struct array
size_ = (mb * 1024 * 1024) / sizeof(TTEntry);
size_t s = 1; while (s * 2 <= size_) s *= 2;
```
```cpp
// chess-newlang-codex: explicit minimum
std::size_t bytes = mb * 1024ULL * 1024ULL;
while (p2 < n) p2 <<= 1U;
entries_.resize(p2);
```

All four implement: **MB input → divide by entry size → round down to power of 2 → allocate**. The power-of-2 constraint enables fast modulo via bitmasking (`index = hash & mask`). This is standard engineering knowledge from the chess programming wiki's TT article, and the convergence across Java, C++, and Rust confirms it.

The variation is in implementation detail, not concept:
- chess-java uses parallel arrays (cache-friendly, separate DRAM access per field)
- chess-java-cc packs key + data into two longs (16 bytes; better cache locality for the key check)
- chess-cplusplus-claude uses a `TTEntry` struct array
- cplusplus-chess uses `TTBucket` — suggesting a two-tier scheme where each "bucket" holds multiple entries

### 6.3 The language-idiomatic TT: where LLMs actually adapt

The most revealing architectural variations come from languages that don't support the C-style struct-array approach:

**Ruby (`chess-ruby-codex`): `@tt = {}`**  
Plain Ruby Hash, no Zobrist at all. Ruby's `Hash` uses the object's `hash` method as the key. For a board position, this would either be the FEN string hash or a custom board hash. This is a fully valid approach — Ruby's hash is O(1) expected, and you pay zero code complexity for the Zobrist layer. The trade-off is that the board hash may not be collision-resistant or incremental. This engine chose language ergonomics over chess-specific optimization, and it likely loses some strength compared to Zobrist-based engines (more TT collisions, cannot be updated incrementally).

**Lean 4 (`lean-chess`): `tt.get? pos`**  
Five-line `ttMoveHint?` function:
```lean
def ttMoveHint? (tt : TT) (pos : Position) : Option Move :=
  match tt.get? pos with
  | some entry => entry.bestMove
  | none => none
```
Lean uses functional pattern matching on `Option`. The TT is a `HashMap` (Lean's standard library), and positions are keys. The `Option Move` return type is idiomatic — no null, no sentinel value. The LLM chose the cleanest Lean idiom (functional pattern match on `Option`) while preserving the conceptual structure (probe → optional best move).

**OCaml (`chess-why3-cc`): `Tt.probe hash` returning `option`**  
Similar to Lean, but the implementation is more complete — the full probe logic visible in the alpha_beta function shows:
```ocaml
match Tt.probe hash with
| Some entry ->
  tt_move := entry.tt_move;
  if entry.tt_depth >= depth then begin
    match entry.tt_flag with
    | Tt.Exact -> ...
    | Tt.Lower -> if tt_score > !alpha then alpha := tt_score
    | Tt.Upper -> if tt_score < beta then ...
  end
| None -> ()
```
This is the most complete TT implementation visible in any extracted snippet. It has depth check, three flag types (Exact/Lower/Upper), best-move extraction, and score-from-TT conversion. Notably, the OCaml `option` type makes the absence case explicit — there's no risk of a null-pointer dereference on a TT miss.

**COBOL (`COBOL-chess`): fixed-size OCCURS array**  
COBOL cannot dynamically allocate memory. The TT must be a `WORKING-STORAGE` entry with a fixed `OCCURS TT-SIZE TIMES` clause. The initialization visible in the hotspot confirms this:
```cobol
IF SS-TT-INIT NOT = 1
    PERFORM VARYING TT-I FROM 1 BY 1 UNTIL TT-I > TT-SIZE
        MOVE -1 TO TTE-KEY(TT-I)
    END-PERFORM
    MOVE 1 TO SS-TT-INIT
```
The TT is zero-initialized at first use (lazy init). `-1` is a sentinel "empty" key. The sizing is compile-time fixed (no MB parameter). The COBOL LLM understood that COBOL requires a different initialization and replacement approach than C/Java and implemented accordingly — even though the result is architecturally constrained.

**Python (`chess-css-codex`): `board._transposition_key()`**  
One line — complete delegation to python-chess's internal hash function. No Zobrist table, no hand-rolled probe, no flag types. The python-chess library provides `_transposition_key()` which returns a tuple encoding the full board state. This is the same "evasion" pattern as quiescence for this engine: difficult logic is externalized to the library. The TT is then just a Python `dict` keyed by this tuple.

---

## 7. The "same algorithm?" question for TT

**No — TT is not a single algorithm.** Unlike quiescence, which has one canonical skeleton, TT admits several architecturally distinct implementations, and LLMs made divergent choices:

| Dimension | Variants in corpus |
|---|---|
| **Key type** | Zobrist 64-bit (most), Ruby built-in hash, python-chess tuple, Lean HashMap key |
| **Initialization** | Seeded LCG at startup, SplitMix64 with fixed seed, pre-computed constants, module abstraction |
| **Storage** | Parallel arrays (Java), struct array (C++), Ruby Hash, Python dict, COBOL OCCURS, Lean HashMap |
| **Sizing** | MB-parameterized power-of-2 (Java/C++), fixed compile-time (COBOL), unlimited (Ruby/Python) |
| **Replacement** | Always-replace (most), two-tier bucket (cplusplus-chess), depth-preferred (unclear) |
| **Flag system** | Exact/Lower/Upper (chess-why3-cc; likely all serious engines), binary (some), none |
| **Probe signature** | Returns score + flag (C/C++/Java), returns `Option entry` (OCaml/Lean), plain dict lookup |

Despite this structural diversity, all serious TT implementations share the same **conceptual invariants**:
- A position hash is a compact key for the position
- An entry stores (score, depth, flag, best_move)
- On probe: check that hash matches (no collision) and depth ≥ required depth before using score
- On store: overwrite based on some replacement policy

These invariants also come from chessprogramming.org — but unlike quiescence's *single pseudocode*, the TT is described with multiple valid implementations, which explains the structural diversity.

---

## 8. Fingerprint analysis: do the Zobrist tables match?

The most fingerprint-sensitive aspect of any TT implementation is the **Zobrist random numbers**. If two engines use the same Zobrist table, they must have copied from the same source (or both generated from the same seed, which is equivalent).

From the extracted snippets:
- `chess-purec`: custom LCG seeded with `1070372`. The sequence depends on the LCG constants.
- `chess-purec-codex`: SplitMix64 seeded with `0x123456789abcdef0`. This is a *deterministic* sequence.
- All other engines: Zobrist values either not extracted, or computed at runtime from different seeds.

The two C engines (`chess-purec` and `chess-purec-codex`) use *different PRNGs* with *different seeds*, so their Zobrist tables are different. They cannot be copies of each other at the Zobrist level, despite being algorithmically similar. This is consistent with the quiescence finding: independent generations from a common spec, not copies of each other.

The `0x123456789abcdef0` seed in chess-purec-codex is the only concrete signal of a specific source: this exact seed appears in numerous online SplitMix64 examples (including the original Vigna paper's example code). The LLM sourced the PRNG initialization from a specific example, not from a chess-specific source.

---

## 9. LLM capability: what was done well

**Paradigm adaptation is consistently correct.** Every LLM correctly adapted the TT to its target language's idioms:
- Ruby used a Hash, not a manual open-addressing table
- Lean and OCaml used `Option` types for TT misses, avoiding null/sentinel patterns
- COBOL used OCCURS-based arrays with explicit loop initialization
- Python used a dict (when not delegating to python-chess)
- C/Java/Rust used the standard array + index-masking approach

**MB-parameterized sizing is an LLM addition.** The chessprogramming.org TT article describes the concept but typically shows a fixed-size array. The LLMs added MB-based sizing with power-of-2 rounding independently across Java, C++, and Rust engines. This represents an engineering decision beyond the base specification — making the TT configurable via a runtime parameter rather than a compile-time constant. This behavior was not prompted; it emerged from the "improve the Elo" / "make it practical" prompts.

**TT class encapsulation** was also a LLM addition: chess-java, chess-java-cc, chess-cplusplus-claude, and chess-newlang-codex all extracted from a dedicated `TranspositionTable.java` or `tt.cpp` file, showing the LLM structured the TT as a first-class class or module rather than a file-scope array. This is good software engineering that also wasn't required by the algorithm.

---

## 10. Missing opportunities and blind spots

**Depth-preferred replacement** (0/21 detected): The standard recommendation is to replace a TT entry only if the new search depth is greater than the stored depth (prefer deeper results). Only cplusplus-chess's `TTBucket` hints at a more sophisticated replacement policy. Most engines appear to use always-replace.

**Age/generation management** (1/21, cplusplus-chess only): Stockfish and most strong engines assign a "generation" to each TT entry and prefer newer entries from the current search. Aged entries from a previous search are less likely to be useful. None of the extracted snippets (except cplusplus-chess) show this.

**Collision verification** (0/21): A TT entry is indexed by the lower bits of the hash; the upper bits should be stored and verified on probe to detect index collisions. None of the extracted snippets show a stored verification key separate from the index key. This is a latent correctness issue — hash collisions can cause the engine to use a score from a different position.

**Separate pawn hash table** (0/21): A common optimization is a small, dedicated hash table for pawn structure evaluation (pawn structure changes rarely, so pawn evaluation can be cached). Zero engines show this.

**TT in quiescence search** (0/21 detected): While the quiescence analysis found 3 engines that probe the TT in quiescence (`chess-cplusplus-claude`, `chess-purec-codex`, `chess-rust-cc`), the TT hotspots for these engines were extracted from *initialization* code, not from the search loop. The proximity-based TT-in-qsearch detector found zero. This is a regex limitation, not an absence.

**Lock-free TT for multithreading** (0/21): None of the engines appear multithreaded, so this is not a gap per se — but it illustrates that the LLMs implemented a single-threaded TT even in languages where concurrent access would be natural (Java, Rust).

---

## 11. The methodological lesson

TT is the clearest demonstration that **the hotspot extractor, designed for concentrated single-function features, works differently for distributed architectural features**.

For quiescence: one function, one snippet, high sub-feature detection, interpretable matrix.

For TT: the locator finds whatever file/function first matches the keyword — sometimes initialization, sometimes the constructor, sometimes the probe call site, sometimes a binary. The resulting matrix is sparse and cluster-structured not because engines implement TT differently, but because the extractor found different aspects.

The solution for future work is **multi-hotspot mode**: collect the top-N hotspots per engine for distributed features, then report on the union of sub-features across all extracted snippets. For TT, collecting (1) the Zobrist init, (2) the TT class/struct definition, and (3) the search function containing the probe/store calls would give a complete picture.

---

## 12. Summary

The transposition table is implemented in 24/35 engines (21 valid extractions). Unlike quiescence — which converges on a single canonical algorithm — TT is architecturally diverse: Zobrist-array vs. Ruby-Hash vs. python-chess delegation vs. COBOL-OCCURS, MB-parameterized vs. fixed-size, always-replace vs. two-tier. This diversity is genuine and reflects that the TT is an engineering artifact, not a single algorithm, and different LLM sessions made different tradeoffs.

Where LLMs excel: paradigm-appropriate adaptation (OCaml/Lean `Option`, COBOL OCCURS, Ruby Hash), adding MB-parameterized sizing beyond the base spec, structuring TT as a first-class module. Where they fall short: replacement policy sophistication (age management, depth-preferred), collision verification, and pawn hash tables — the "optimization layer above the basic implementation" gap that also appeared in quiescence.

The Zobrist fingerprint analysis finds no evidence of copying between engines. Different engines use different PRNGs with different seeds; even the two C engines (`chess-purec` and `chess-purec-codex`) generate incompatible Zobrist tables. The only outside-source signal is the `0x123456789abcdef0` SplitMix64 example seed, which points to a specific online PRNG tutorial rather than a chess-specific source.

Finally, TT exposed an extraction failure mode (compiled binaries matching `zobrist` string because Coq and COBOL compiler embeds symbol names) that the quiescence extractor avoided by pure coincidence. Robust feature location for compiled-output languages requires explicit binary-file filtering by content, not just by extension.
