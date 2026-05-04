# Software-engineering capabilities exhibited across the corpus

_Generated 2026-04-22 14:52 UTC._

This report characterises the software-engineering activities observable in the agent sessions, beyond "the agent produced code". Across 34 engines (main corpus + special-role), each session is segmented into steps; each step is tagged against a 10-capability taxonomy derived from the paper's research questions. A step can carry multiple tags.

## Capability taxonomy

| ID | Label | Description |
|---|---|---|
| `design` | Design \& specification | Up-front design activity: reading or authoring SPECIFICATION, ARCHITECTURE, PLAN, ROADMAP, REQUIREMENTS, DESIGN, or README documents; the first pass of a build-system manifest; or a multi-file layout step (new files across $\geq$2 directories). Captures both 'interpret the user's goal into a plan' and 'decide the top-level module structure'. |
| `implementation` | Implementation | Writing or editing source files in a canonical programming language --- the core code-authoring activity. Fires on new source files and on edits to existing source files; explicitly subsumes wire-format parser work (UCI, FEN, PGN, SAN) and edit-only iterations (refactoring, small rewrites), which in earlier drafts of this frame were separate categories but could not be reliably disentangled from ordinary implementation in the trajectory data. |
| `testing` | Testing | Correctness-oriented verification: running perft, invoking the engine under UCI to check it boots and plays legal moves, running a test harness (pytest, cargo test, dune test, cutechess), editing test-path files (\texttt{tests/}, \texttt{test\_*}, \texttt{*\_test.*}). Distinct from benchmarking, which measures strength rather than correctness. |
| `debugging` | Debugging | Fix-oriented iteration: the user reports a bug (BugFixRequest intent), the prompt contains debugging vocabulary (``bug'', ``fix'', ``illegal'', ``segfault''), the step class is \texttt{debug}, or the step edits existing files with a build/test cycle and no new authoring. Evidence of self-correction rather than first-pass generation. |
| `build-tooling` | Build \& tooling | Build-system edits (Makefile, Cargo.toml, CMakeLists.txt, pyproject.toml, Gemfile, lakefile, dune-project, package.json) after the initial manifest, package installs, and compile invocations. The first-authoring of a manifest counts as \emph{design}; subsequent build-config work counts here. |
| `version-control` | Version control | git add/commit/log/branch/diff operations. |
| `benchmarking-eval` | Benchmarking \& evaluation | Strength-measurement activity: running cutechess-cli or Stockfish as an opponent, authoring bespoke Elo-estimation scripts or tournament drivers, touching files with \texttt{elo}/\texttt{tournament}/\texttt{gauntlet} in the name. Distinct from testing (which is correctness). |
| `code-comprehension` | Code comprehension | Read / Grep / Glob / WebSearch tool uses and \texttt{cat}/\texttt{head}/\texttt{grep}-style inspection bash. Evidence of the agent exploring existing code or external references before editing. |
| `performance-eng` | Performance engineering | \texttt{--release} / \texttt{-O2} / \texttt{-O3} flags, profiling invocations, or performance vocabulary in the user prompt (``optimise'', ``faster'', ``bottleneck'', ``nodes/sec''). Evidence that the agent treats runtime performance as a first-class concern. |
| `documentation` | Documentation | Writing or editing Markdown files that are not the design/spec/plan docs (those belong to \emph{design}). Evidence of narrative writing as part of the delivery. |

## Corpus coverage: how many engines exhibit each capability

| Capability | # engines (of 34) | Share | Total events |
|---|---:|---:|---:|
| Code comprehension | 34 | 100\% | 304 |
| Debugging | 32 | 94\% | 291 |
| Benchmarking \& evaluation | 29 | 85\% | 190 |
| Implementation | 28 | 82\% | 215 |
| Testing | 27 | 79\% | 187 |
| Version control | 25 | 74\% | 114 |
| Design \& specification | 24 | 71\% | 145 |
| Build \& tooling | 24 | 71\% | 125 |
| Performance engineering | 13 | 38\% | 45 |
| Documentation | 6 | 18\% | 34 |

## Per-engine intensity profile (Likert)

One row per engine; each column carries a 4-level ordinal intensity for that capability: `—` absent (0 steps), `●` light (1 step or ≤5% of the session), `●●` moderate (5--20%), `●●●` heavy (>20%). `Dist` is the number of capabilities exercised at any level (absent excluded).

| Engine | Steps | Read | Debug | Bench | Impl | Test | VCS | Design | Build | Perf | Docs | Dist |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `chess-brainfuck` | 38 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● | ●● | ●● | 10 |
| `chess-brainfuck-cc` | 192 | ●●● | ●●● | ● | ● | ● | ●● | ● | ● | ● | ●● | 10 |
| `chess-rust-cc-redo` | 49 | ●●● | ●● | ●●● | ●●● | ●●● | ● | ●● | ●●● | ●● | ●● | 10 |
| `COBOL-chess` | 34 | ●●● | ●●● | ●●● | ●●● | ●●● | ●● | ●●● | ●●● | ●●● | — | 9 |
| `chess-apl-codex54` | 34 | ●●● | ●●● | ●●● | ●●● | ●●● | ●● | ●●● | ●● | ●●● | — | 9 |
| `chess-cobol-cc` | 23 | ●●● | ●●● | ●●● | ●●● | ●●● | ● | — | ● | ●●● | ●● | 9 |
| `chess-latex-codex-replication` | 15 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● | ● | ● | — | 9 |
| `chess-newlang-codex` | 21 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● | ●● | ● | — | 9 |
| `chess-purec-codex` | 4 | ●●● | ●●● | ●●● | ●●● | ●●● | ● | ●●● | ●●● | ● | — | 9 |
| `chess-revisit-java-toCOBOL-codex` | 28 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● | — | ●●● | 9 |
| `cplusplus-chess` | 16 | ●● | ●●● | ●●● | ●●● | ●●● | ● | ●●● | ●●● | — | ●● | 9 |
| `lean-chess` | 21 | ●● | ●●● | ●●● | ●●● | ●● | ●● | ●●● | ●●● | ● | — | 9 |
| `chess-assembly-codex` | 12 | ●●● | ●●● | ●●● | ●●● | ● | ●● | ●●● | ●●● | — | — | 8 |
| `chess-icon-codex` | 6 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● | ● | — | — | 8 |
| `chess-java` | 7 | ●●● | ●●● | ●●● | ●●● | ●●● | ● | ● | ● | — | — | 8 |
| `chess-mojo` | 6 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● | — | — | 8 |
| `chess-revisit-java-toRust-codex` | 5 | ●●● | ● | ●●● | ● | ●●● | ●●● | — | ●●● | ● | — | 8 |
| `chess-rust-codex` | 3 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● | — | — | 8 |
| `chess-why3` | 9 | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● | ●●● | — | — | 8 |
| `chess-css-codex` | 17 | ●●● | ●● | ●● | ●●● | ●● | ●●● | ●●● | — | — | — | 7 |
| `chess-ruby-cc` | 10 | ●●● | ●●● | ●●● | ●●● | ●●● | — | ● | ●● | — | — | 7 |
| `chess-css-codex-guided` | 9 | ●●● | ● | — | ●●● | ●●● | ● | ●●● | — | — | — | 6 |
| `chess-py` | 10 | ● | ● | ●●● | ●●● | ●●● | — | ●●● | — | — | — | 6 |
| `chess-ruby-codex` | 7 | ● | — | ●●● | ●●● | ●●● | ●●● | ●●● | — | — | — | 6 |
| `chess-rust-cc` | 8 | ●●● | ●●● | ● | ● | — | — | — | ●●● | ●●● | — | 6 |
| `latex-chess-engine` | 37 | ●●● | ●● | ●● | — | ●● | ●● | — | — | ●● | — | 6 |
| `chess-cplusplus-claude` | 18 | ●●● | ●●● | ● | ● | — | — | — | ● | — | — | 5 |
| `chess-purec` | 5 | ●●● | ● | — | ● | ● | — | — | ● | — | — | 5 |
| `chess-Rocq` | 11 | ●●● | ●●● | — | — | — | ●●● | ●● | — | — | — | 4 |
| `chess-java-cc` | 6 | ●●● | ● | — | ● | — | — | ●●● | — | — | — | 4 |
| `chess-sql` | 3 | ● | ● | ● | — | ● | — | — | — | — | — | 4 |
| `test-superset` | 53 | ●●● | ●●● | ● | — | — | ● | — | — | — | — | 4 |
| `chess-py-cc` | 1 | ● | — | ● | — | — | — | — | ● | — | — | 3 |
| `chess-why3-cc` | 6 | ●●● | ●●● | — | — | — | — | — | — | — | — | 2 |

### Per-engine raw event counts (for reference)

Same row ordering; each cell is the raw step count for the capability. Included so reviewers can recompute any intensity level without re-running the tagger.

| Engine | Steps | Read | Debug | Bench | Impl | Test | VCS | Design | Build | Perf | Docs | Dist |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `chess-brainfuck` | 38 | 16 | 9 | 15 | 18 | 17 | 17 | 16 | 8 | 4 | 2 | 10 |
| `chess-brainfuck-cc` | 192 | 60 | 115 | 6 | 7 | 4 | 11 | 5 | 5 | 2 | 14 | 10 |
| `chess-rust-cc-redo` | 49 | 11 | 5 | 11 | 12 | 12 | 2 | 4 | 10 | 8 | 3 | 10 |
| `COBOL-chess` | 34 | 8 | 17 | 13 | 18 | 18 | 4 | 8 | 19 | 8 |  | 9 |
| `chess-apl-codex54` | 34 | 11 | 11 | 18 | 14 | 17 | 6 | 15 | 2 | 7 |  | 9 |
| `chess-cobol-cc` | 23 | 14 | 16 | 13 | 13 | 13 | 1 |  | 1 | 7 | 3 | 9 |
| `chess-latex-codex-replication` | 15 | 7 | 4 | 11 | 11 | 10 | 13 | 11 | 1 | 1 |  | 9 |
| `chess-newlang-codex` | 21 | 9 | 10 | 5 | 11 | 10 | 8 | 7 | 3 | 1 |  | 9 |
| `chess-purec-codex` | 4 | 3 | 3 | 4 | 3 | 3 | 1 | 3 | 4 | 1 |  | 9 |
| `chess-revisit-java-toCOBOL-codex` | 28 | 17 | 15 | 11 | 19 | 21 | 9 | 11 | 20 |  | 10 | 9 |
| `cplusplus-chess` | 16 | 2 | 6 | 7 | 10 | 6 | 1 | 7 | 10 |  | 2 | 9 |
| `lean-chess` | 21 | 4 | 8 | 15 | 13 | 4 | 2 | 7 | 13 | 1 |  | 9 |
| `chess-assembly-codex` | 12 | 3 | 6 | 11 | 8 | 1 | 2 | 8 | 8 |  |  | 8 |
| `chess-icon-codex` | 6 | 3 | 3 | 4 | 5 | 5 | 2 | 2 | 1 |  |  | 8 |
| `chess-java` | 7 | 2 | 3 | 3 | 3 | 6 | 1 | 1 | 1 |  |  | 8 |
| `chess-mojo` | 6 | 5 | 3 | 4 | 4 | 4 | 2 | 3 | 2 |  |  | 8 |
| `chess-revisit-java-toRust-codex` | 5 | 3 | 1 | 3 | 1 | 3 | 2 |  | 2 | 1 |  | 8 |
| `chess-rust-codex` | 3 | 2 | 2 | 3 | 3 | 3 | 3 | 2 | 3 |  |  | 8 |
| `chess-why3` | 9 | 4 | 4 | 3 | 4 | 3 | 2 | 3 | 5 |  |  | 8 |
| `chess-css-codex` | 17 | 10 | 3 | 2 | 8 | 2 | 12 | 12 |  |  |  | 7 |
| `chess-ruby-cc` | 10 | 5 | 5 | 7 | 5 | 5 |  | 1 | 2 |  |  | 7 |
| `chess-css-codex-guided` | 9 | 6 | 1 |  | 6 | 5 | 1 | 5 |  |  |  | 6 |
| `chess-py` | 10 | 1 | 1 | 8 | 9 | 6 |  | 5 |  |  |  | 6 |
| `chess-ruby-codex` | 7 | 1 |  | 6 | 6 | 5 | 2 | 4 |  |  |  | 6 |
| `chess-rust-cc` | 8 | 6 | 3 | 1 | 1 |  |  |  | 2 | 2 |  | 6 |
| `latex-chess-engine` | 37 | 18 | 6 | 2 |  | 2 | 5 |  |  | 2 |  | 6 |
| `chess-cplusplus-claude` | 18 | 12 | 10 | 1 | 1 |  |  |  | 1 |  |  | 5 |
| `chess-purec` | 5 | 5 | 1 |  | 1 | 1 |  |  | 1 |  |  | 5 |
| `chess-Rocq` | 11 | 4 | 4 |  |  |  | 3 | 2 |  |  |  | 4 |
| `chess-java-cc` | 6 | 3 | 1 |  | 1 |  |  | 3 |  |  |  | 4 |
| `chess-sql` | 3 | 1 | 1 | 1 |  | 1 |  |  |  |  |  | 4 |
| `test-superset` | 53 | 43 | 12 | 1 |  |  | 2 |  |  |  |  | 4 |
| `chess-py-cc` | 1 | 1 |  | 1 |  |  |  |  | 1 |  |  | 3 |
| `chess-why3-cc` | 6 | 4 | 2 |  |  |  |  |  |  |  |  | 2 |

## Breakdown by language category

Engines are grouped by the paper's RQ1 language taxonomy (mainstream general-purpose, specialized/academic, domain-specific/markup, legacy, esoteric). Each cell is the share of engines in that category that exhibited the capability at least once. Bottom rows: number of engines and median steps per engine in the category.

| Capability | Mainstream general-purpose<br/>(n=15) | Specialized / academic<br/>(n=7) | Domain-specific / markup<br/>(n=6) | Legacy<br/>(n=4) | Esoteric<br/>(n=2) |
|---|---:|---:|---:|---:|---:|
| Code comprehension | 15/15 (100\%) | 7/7 (100\%) | 6/6 (100\%) | 4/4 (100\%) | 2/2 (100\%) |
| Debugging | 13/15 (87\%) | 7/7 (100\%) | 6/6 (100\%) | 4/4 (100\%) | 2/2 (100\%) |
| Benchmarking \& evaluation | 13/15 (87\%) | 5/7 (71\%) | 5/6 (83\%) | 4/4 (100\%) | 2/2 (100\%) |
| Implementation | 14/15 (93\%) | 5/7 (71\%) | 3/6 (50\%) | 4/4 (100\%) | 2/2 (100\%) |
| Testing | 11/15 (73\%) | 5/7 (71\%) | 5/6 (83\%) | 4/4 (100\%) | 2/2 (100\%) |
| Version control | 8/15 (53\%) | 6/7 (86\%) | 5/6 (83\%) | 4/4 (100\%) | 2/2 (100\%) |
| Design \& specification | 10/15 (67\%) | 6/7 (86\%) | 3/6 (50\%) | 3/4 (75\%) | 2/2 (100\%) |
| Build \& tooling | 12/15 (80\%) | 5/7 (71\%) | 1/6 (17\%) | 4/4 (100\%) | 2/2 (100\%) |
| Performance engineering | 4/15 (27\%) | 3/7 (43\%) | 2/6 (33\%) | 2/4 (50\%) | 2/2 (100\%) |
| Documentation | 2/15 (13\%) | 0/7 (0\%) | 0/6 (0\%) | 2/4 (50\%) | 2/2 (100\%) |
| **Median steps/engine** | 7 | 11 | 17 | 28 | 192 |
| **Mean distinct capabilities/engine** | 6.8 | 7.0 | 6.0 | 8.8 | 10.0 |

### Category-sensitive vs category-invariant capabilities

Capabilities ranked by across-category spread (max share minus min share):

| Capability | Spread | Highest category | Lowest category |
|---|---:|---|---|
| Documentation | 100 pp | Esoteric (100\%) | Specialized / academic (0\%) |
| Build \& tooling | 83 pp | Legacy (100\%) | Domain-specific / markup (17\%) |
| Performance engineering | 73 pp | Esoteric (100\%) | Mainstream general-purpose (27\%) |
| Implementation | 50 pp | Legacy (100\%) | Domain-specific / markup (50\%) |
| Design \& specification | 50 pp | Esoteric (100\%) | Domain-specific / markup (50\%) |
| Version control | 47 pp | Legacy (100\%) | Mainstream general-purpose (53\%) |
| Benchmarking \& evaluation | 29 pp | Legacy (100\%) | Specialized / academic (71\%) |
| Testing | 29 pp | Legacy (100\%) | Specialized / academic (71\%) |
| Debugging | 13 pp | Specialized / academic (100\%) | Mainstream general-purpose (87\%) |
| Code comprehension | 0 pp | Mainstream general-purpose (100\%) | Mainstream general-purpose (100\%) |

### Representative engine per category (largest distinct-capability set)

- **Mainstream general-purpose** (15 engines): `chess-rust-cc-redo` exercises 10 of 10 capabilities across 49 steps.
- **Specialized / academic** (7 engines): `chess-apl-codex54` exercises 9 of 10 capabilities across 34 steps.
- **Domain-specific / markup** (6 engines): `chess-latex-codex-replication` exercises 9 of 10 capabilities across 15 steps.
- **Legacy** (4 engines): `COBOL-chess` exercises 9 of 10 capabilities across 34 steps.
- **Esoteric** (2 engines): `chess-brainfuck-cc` exercises 10 of 10 capabilities across 192 steps.

## Paradigm cases: the engine most exemplifying each capability

- **Code comprehension** `code-comprehension`: `chess-brainfuck-cc` (60 tagged steps; steps 1--190 (60 hits)).
- **Debugging** `debugging`: `chess-brainfuck-cc` (115 tagged steps; steps 8--184 (115 hits)).
- **Benchmarking \& evaluation** `benchmarking-eval`: `chess-apl-codex54` (18 tagged steps; steps 1--31 (18 hits)).
- **Implementation** `implementation`: `chess-revisit-java-toCOBOL-codex` (19 tagged steps; steps 1--24 (19 hits)).
- **Testing** `testing`: `chess-revisit-java-toCOBOL-codex` (21 tagged steps; steps 1--26 (21 hits)).
- **Version control** `version-control`: `chess-brainfuck` (17 tagged steps; steps 1--38 (17 hits)).
- **Design \& specification** `design`: `chess-brainfuck` (16 tagged steps; steps 1--34 (16 hits)).
- **Build \& tooling** `build-tooling`: `chess-revisit-java-toCOBOL-codex` (20 tagged steps; steps 1--24 (20 hits)).
- **Performance engineering** `performance-eng`: `COBOL-chess` (8 tagged steps; steps 14--24 (8 hits)).
- **Documentation** `documentation`: `chess-brainfuck-cc` (14 tagged steps; steps 140--190 (14 hits)).

## Saturation summary

- **Universal (\geq 80\% of engines):** `code-comprehension`, `debugging`, `benchmarking-eval`, `implementation`, `testing`.
- **Majority (50--80\% of engines):** `version-control`, `design`, `build-tooling`.
- **Selective (< 50\% of engines):** `performance-eng`, `documentation`.

## Notes and caveats

- Tagging rules are heuristic, file-path + bash-command + prompt-vocabulary based. A step can be mis-tagged; the coarse coverage pattern (which capabilities are universal vs.\ rare) is robust, individual rows should be spot-checked against the per-engine trajectory reports.
- Engines with archived main transcripts (`chess-java-cc`, the second TeX engine, two `-cc` projects whose main JSONL is gone) show reduced capability counts because tool-use events cannot be recovered; see the provenance notes in the corresponding per-engine dossiers.
- The `implementation` count is deliberately a count of *steps that wrote at least one new source file*, not a count of LOC. A Ruby engine built in one big step carries `implementation`=1 despite writing thousands of lines; the debug / testing / benchmarking counts are typically higher. Read the profile table as ``was this activity exercised?'' not ``how much code did this activity produce?''
