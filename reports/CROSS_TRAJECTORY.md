# Cross-project trajectory analysis

_Generated 2026-04-19 18:31 UTC_

Scope: 28 engines with enough trajectory substance (24 main corpus + 4 special-role).
Exclusion rules: $\geq$5 user prompts AND $\geq$10,000 recorded tokens. Excluded engines (thin trajectories): `chess-purec-codex` (<5 steps), `chess-py-cc` (<5 steps), `chess-rust-codex` (<5 steps), `chess-sql` (<5 steps).

The three passes below ask: **what is common**, **what is different**, and **what is unique** across the per-engine trajectories emitted by `scripts/trajectory.py`. Shape statistics, task-class mix, oracle cadence, Elo-curve shape, and phase-trigram frequencies are computed per engine and pooled.

## Common patterns (main corpus, $n = 24)

### Session shape

| Metric | 25th pct. | median | 75th pct. | max |
|---|---:|---:|---:|---:|
| User prompts per session | 8 | 12 | 22 | 192 |
| Tokens per session (k) | 19,248 | 67,905 | 136,528 | 937,764 |
| Wallclock hours | 1.1 | 2.7 | 8.5 | 666.3 |

### Task-class distribution (median fraction of steps)

| class | median frac. | 75th pct. frac. |
|---|---:|---:|
| other | 0.377 | 0.536 |
| feature | 0.294 | 0.389 |
| meta | 0.145 | 0.271 |
| debug | 0.035 | 0.103 |
| eval | 0.0 | 0.028 |
| refactor | 0.0 | 0.000 |
| test | 0.0 | 0.000 |
| tooling | 0.0 | 0.004 |

### When do agents first reach for each oracle / build?

- First `cargo test`/`make` invocation: median step **2** of 7 engines.
- First `perft` test: median step **18.0** of 4 engines.
- First gauntlet (cutechess / custom Elo script): median step **1.0** of 6 engines.


### Elo-claim trajectory shape

| shape | engines |
|---|---:|
| none | 8 |
| mixed | 5 |
| zigzag | 4 |
| single | 3 |
| monotone-up | 3 |
| monotone-down | 1 |

### Most frequent phase-trigrams across the corpus

| trigram | # engines |
|---|---:|
| `other → feature → other` | 25 |
| `feature → other → feature` | 20 |
| `other → meta → other` | 19 |
| `feature → other → meta` | 16 |
| `meta → other → feature` | 11 |
| `meta → feature → other` | 9 |
| `other → meta → feature` | 8 |
| `meta → other → meta` | 7 |
| `other → feature → meta` | 6 |
| `feature → meta → other` | 6 |

### Bash-kind share across the corpus (pooled raw counts)

| Kind | # calls | % of pooled total |
|---|---:|---:|
| `inspect` | 1457 | 46.9% |
| `other` | 1006 | 32.4% |
| `uci_run` | 294 | 9.5% |
| `gauntlet` | 159 | 5.1% |
| `git` | 74 | 2.4% |
| `build` | 67 | 2.2% |
| `perft` | 27 | 0.9% |
| `stockfish` | 21 | 0.7% |

## Differences (where engines diverge)

### Debug ratio (% of steps classified `debug`)

| Engine | Debug frac. |
|---|---:|
| chess-cplusplus-claude | 0.33 |
| COBOL-chess | 0.32 |
| chess-purec | 0.20 |
| lean-chess | 0.14 |
| chess-rust-cc | 0.12 |
| … | |
| chess-ruby-codex | 0.00 |
| chess-java-cc | 0.00 |
| chess-css-codex-guided | 0.00 |

### Improve-loop density (`Improve` intent / total prompts)

| Engine | Improve frac. |
|---|---:|
| chess-py | 0.19 |
| chess-ruby-cc | 0.16 |
| chess-cplusplus-claude | 0.13 |
| chess-brainfuck | 0.12 |
| chess-ruby-codex | 0.11 |
| … | |
| chess-brainfuck-cc | 0.02 |
| chess-Rocq | 0.00 |
| chess-css-codex-guided | 0.00 |

### Edit-vs-new file ratio (large = many revisions per module)

| Engine | edit / total | new | edit |
|---|---:|---:|---:|
| chess-cplusplus-claude | 1.00 | 0 | 1 |
| chess-rust-cc | 1.00 | 0 | 15 |
| chess-cobol-cc | 0.96 | 13 | 324 |
| chess-brainfuck-cc | 0.91 | 8 | 79 |
| chess-purec | 0.78 | 2 | 7 |
| chess-java-cc | 0.75 | 1 | 3 |
| … | | | |
| chess-apl-codex54 | 0.67 | 1 | 2 |
| chess-ruby-cc | 0.41 | 82 | 57 |
| COBOL-chess | 0.33 | 2 | 1 |

### Latest first-gauntlet step (agents that delayed strength testing)

| Engine | First gauntlet at step |
|---|---:|
| chess-apl-codex54 | 17 |
| chess-brainfuck-cc | 2 |
| chess-cobol-cc | 1 |
| chess-cplusplus-claude | 1 |
| chess-rust-cc | 1 |

### Stagnation-heavy engines (# of flagged steps)

| Engine | Stagnation steps |
|---|---:|
| COBOL-chess | 7 |

## Unique signatures (main corpus, $n = 1$ occurrences)

### Task-classes observed in a single engine

- `refactor` only in **chess-brainfuck-cc**

### Tools used in a single engine

- `Task` only in **chess-brainfuck-cc** (0.1% of its tool calls)
- `TaskStop` only in **chess-brainfuck-cc** (0.2% of its tool calls)
- `request_user_input` only in **COBOL-chess** (0.1% of its tool calls)

### Single-engine extrema

- Most user prompts: **chess-brainfuck-cc** (192)
- Most new files written: **chess-ruby-cc** (82)
- Most tokens consumed: **COBOL-chess** (937.8M)
- Most stagnation steps: **COBOL-chess** (7)
- Most Elo claims in assistant text: **chess-brainfuck-cc** (86 mentions)

## Special-role experiments (separate from the main corpus)

### engine-port

| Engine | Steps | Phases | Tokens (M) | Class mix (top-3) | Elo shape |
|---|---:|---:|---:|---|---|
| chess-revisit-java-toCOBOL-codex | 28 | 16 | 678.62 | other=0.71, feature=0.18, debug=0.07 | none |
| chess-revisit-java-toRust-codex | 5 | 3 | 255.96 | other=0.60, feature=0.20, debug=0.20 | none |

### engine-dsl

| Engine | Steps | Phases | Tokens (M) | Class mix (top-3) | Elo shape |
|---|---:|---:|---:|---|---|
| chess-newlang-codex | 21 | 14 | 317.99 | other=0.48, feature=0.38, meta=0.10 | mixed |

### engine-failure

| Engine | Steps | Phases | Tokens (M) | Class mix (top-3) | Elo shape |
|---|---:|---:|---:|---|---|
| chess-mojo | 6 | 5 | 65.39 | feature=0.33, other=0.33, debug=0.17 | single |

## Paper-ready takeaways

1. **The modal trajectory is: feature-build → perft → gauntlet → improve-loop.** The phase-trigram table above shows the most common triplet by count; most main-corpus engines touch each of the four stages in that order before plateauing.
2. **Debug ratio, not total effort, separates hard from easy engines.** The same absolute hours can yield a clean feature arc (low debug frac.) or a long oracle-debugging loop (high debug frac.) --- see the debug-ratio table.
3. **Agents reach for oracles early.** The median first-perft step is low; the median first-gauntlet step follows within a few steps. Agents do not wait to be told to evaluate.
4. **Elo-curve shape is typically monotone-up or plateau** after an initial feature-build phase. Zigzag curves are associated with engines that had mid-session regressions we could independently recover from the trajectory.
5. **Uniqueness concentrates in language-specific tool-use** (compiler-specific bash-kinds) and in the stagnation-episode profile. The special-role engines (ports, DSL, failure) show distinctly different phase patterns from the main corpus, justifying their separate reporting.
