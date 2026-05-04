# Qualitative triangulation (pilot)

_Generated 2026-04-20 09:36 UTC._

This file is a pilot run of Path~A in the paper's qualitative-methods plan: a structured coding of author-authored and expert-sourced secondary documents against a small, RQ-tied coding frame. The purpose is to corroborate the paper's quantitative findings with *sourced* qualitative evidence --- moving specific claims out of "anecdote" territory and into "systematically coded" territory --- without attempting a full grounded-theory pass over 28 session transcripts.

## Scope of this pilot

| Source | Engine | Category | Excerpts coded |
|---|---|---|---:|
| [TeXCCChess: How Coding Agents Wrote a Chess Engine in Pure TeX](https://blog.mathieuacher.com/TeXCCChessEngine/) (2026-02-24) | `latex-chess-engine (TeXCCChess)` | domain-specific markup | 15 |
| [BFChess: A Chess Engine in Brainfuck, Built by a Coding Agent](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/) (2026-03-23) | `chess-brainfuck-cc (BFChess)` | esoteric | 18 |
| **Total** | | | **33** |

## Coding frame

Nine codes tied to paper research questions:

| Code | Label | RQs | Description |
|---|---|---|---|
| `language-constraint` | Language constraint observed | RQ2, RQ4 | An observation that a language-specific limitation (absent primitives, unusual semantics, scale limits) directly shaped the engineering choices. Strongest form: 'because the language does not have X, the engine had to do Y'. |
| `novelty-absence` | No prior engine in this language | RQ3 | Explicit claim that no open-source chess engine exists for this language (CTAN / GitHub / public search), therefore the engine is first-of-kind and cannot have been copied. |
| `synthesis-not-copy` | Genuinely synthesised, not memorised | RQ3 | Argument that the engine is not a line-by-line translation of an existing canonical engine. Usually paired with a specific observation about language-native idiom or the impossibility of mechanical translation. |
| `agent-self-correction` | Agent self-correction (debug loop) | RQ5 | The agent notices a specific failure (perft mismatch, illegal move, gauntlet regression), diagnoses it, and fixes it within the session. Often visible as a count of bugs or a specific named defect. |
| `oracle-exploitation` | Oracle exploitation (perft / Elo / gauntlets) | RQ4, RQ5 | The agent (or the developer-agent pair) sets up or uses an external oracle --- perft tests, Stockfish gauntlets, random-move baselines --- to drive iteration. Corroborates the paper's 'oracle-first is a population property' finding. |
| `human-steering` | Human steering / intervention | RQ5 | The developer intervenes to change the agent's course: rejects an approach, reports a bug, redirects scope, or confirms a design choice. Characterises the interaction abstraction (capability-level vs code-level). |
| `feature-adaptation` | Language-native feature adaptation | RQ2, RQ3 | A chess feature is encoded in a language-native idiom rather than copied from a canonical reference (e.g., `\count` registers as RAM, `\csname` tables as hash maps, BF cell ranges as a memory layout, 64-way switch as array indexing). |
| `feedback-loop-cost` | Feedback-loop cost dominates | RQ5 | Writing the code is not the bottleneck; evaluating it is. A single iteration (regenerate, test, measure) takes hours or days, limiting the number of hypotheses that can be tested. Corroborates the paper's cost-scales-with-oracle-rigor finding. |
| `evasion-risk` | Evasion risk (drift to a more expressive language) | RQ3, Method | Under pressure to produce working code, the agent drifts toward a more expressive language (Python inside a CSS engine, Python inside a Brainfuck engine). The constraint must be enforced structurally or by active human verification. |

## Code x source frequency matrix

| Code | tex-blog | bf-blog | total |
|---|---:|---:|---:|
| `language-constraint` | 5 | 4 | **9** |
| `novelty-absence` | 2 | 1 | **3** |
| `synthesis-not-copy` | 2 | 1 | **3** |
| `agent-self-correction` | 5 | 2 | **7** |
| `oracle-exploitation` | 3 | 3 | **6** |
| `human-steering` | 1 | 5 | **6** |
| `feature-adaptation` | 3 | 4 | **7** |
| `feedback-loop-cost` | 1 | 4 | **5** |
| `evasion-risk` |  | 3 | **3** |

Every code appears in at least one source; **8 / 9** codes appear in both sources (a low-bar form of saturation for a two-document pilot). Codes appearing in only one source are worth flagging: `evasion-risk`.

## Findings per code

### `language-constraint` --- Language constraint observed

_Supports: RQ2, RQ4. Total excerpts: 9._

> TeX has no arrays, no functions with return values, no convenient local variables or stack frames, no integers bigger than 2^31-1, no bitwise operations.
_Source: [latex-chess-engine (TeXCCChess)](https://blog.mathieuacher.com/TeXCCChessEngine/), line~17._ Explicit enumeration of the primitive gaps that will force language-native idioms throughout.

> TeX's \numexpr division rounds instead of truncating: 63/8 gives 8 (rounding 7.875 up), not 7. This was the source of one of the first nasty bugs.
_Source: [latex-chess-engine (TeXCCChess)](https://blog.mathieuacher.com/TeXCCChessEngine/), line~97._ A concrete language surprise that broke coordinate extraction; the agent fixed it by precomputing truncating-divide lookups.

> The ordering is critical and was a source of subtle bugs: \pushstate must be called after \makemove ... Getting this wrong produces moves that look almost right but occasionally corrupt castling rights (the kind of bug that shows up once every 50 games).
_Source: [latex-chess-engine (TeXCCChess)](https://blog.mathieuacher.com/TeXCCChessEngine/), line~173._ A long-tail bug only visible under gauntlet testing: the agent could not have caught it without oracle feedback.

> LaTeX's \newcount allocator had already reached register 360+, so the state stack at \count300-317 overlapped with LaTeX-internal registers. ... The agent traced it to a corrupted board value ... and moved the entire state stack to \count10000+.
_Source: [latex-chess-engine (TeXCCChess)](https://blog.mathieuacher.com/TeXCCChessEngine/), line~334._ Register collision is the TeX-native form of a memory-safety bug. The agent diagnosed and fixed it autonomously.

> \numexpr division rounds, it does not truncate. Digits in a normal control sequence name are not part of the name. The @ character in macro names requires \makeatletter. \newif inside macros fails on the second call. Register collision is the TeX equivalent of variable shadowing bugs.
_Source: [latex-chess-engine (TeXCCChess)](https://blog.mathieuacher.com/TeXCCChessEngine/), line~266._ A catalogued list of TeX-specific traps the agent had to discover and work around. These are the 'ceiling' visible from the developer's perspective.

> Brainfuck has no variables, no functions, no arithmetic beyond increment/decrement, and no random memory access. Its only data structure is a linear tape of byte-sized cells.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~14._ Canonical statement of the Brainfuck ceiling. Much more severe than TeX: no scope, no abstraction, no indirection.

> Brainfuck has no board[index] where index is a runtime value. To read a square whose index is computed at runtime, the engine must execute a 64-way switch: compare the index against 0, 1, 2, ..., 63 and copy from the matching fixed cell. ... Every board read or write is ~20 KB of BF code.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~68._ The paradigm single constraint: random-access cost. Drives the 5.6 MB size. No Brainfuck idiom eliminates it; the language-native encoding IS the 64-way switch.

> The generated chess.bf is 5.6 MB of raw Brainfuck. An RLE-optimized interpreter (bfi.c) compresses it at load time from ~3.8M characters to ~520K instructions (7x compression), with a precomputed jump table for O(1) bracket matching.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~49._ The engine required co-designing a custom interpreter to be practically runnable. The language ceiling forced both agent-side optimization and runtime-side optimization.

> The hardest bugs were cell collisions: multiple code paths accidentally writing to the same memory cell. ... Claude Code found and fixed at least 9 such bugs across the development, including one where the print_char function was using cell 30 (= BOARD_START) as scratch space, corrupting the board every time any text was printed.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~177._ Quantified self-correction: 9 cell-collision fixes. A class of bug a human could not track at this scale; the agent could.


### `novelty-absence` --- No prior engine in this language

_Supports: RQ3. Total excerpts: 3._

> I could not find any prior chess engine in TeX (I searched CTAN, GitHub, and TeX Stack Exchange). ... TeXCCChess appears to be the first.
_Source: [latex-chess-engine (TeXCCChess)](https://blog.mathieuacher.com/TeXCCChessEngine/), line~18._ First-of-kind claim with explicit search venues; supports the RQ3 no-copy argument where novelty is trivial.

> If this is indeed the first full TeX chess engine, it is very unlikely the model memorized one verbatim.
_Source: [latex-chess-engine (TeXCCChess)](https://blog.mathieuacher.com/TeXCCChessEngine/), line~20._ Direct synthesis-not-copy argument, anchored on the novelty claim.

> A fully functioning, openly available chess engine written in Brainfuck does not appear to exist in durable public form as of February 2026. ... BFChess appears to be the first complete, publicly available implementation.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~20._ Careful novelty claim: 2019 TalkChess thread + dead repo reviewed and excluded; chess-adjacent BF utilities acknowledged; differentiates a rendering from a playing engine.


### `synthesis-not-copy` --- Genuinely synthesised, not memorised

_Supports: RQ3. Total excerpts: 3._

> If this is indeed the first full TeX chess engine, it is very unlikely the model memorized one verbatim.
_Source: [latex-chess-engine (TeXCCChess)](https://blog.mathieuacher.com/TeXCCChessEngine/), line~20._ Direct synthesis-not-copy argument, anchored on the novelty claim.

> It is neither a translation nor a copy of an existing chess engine. ... The creativity lies in finding TeX-native ways to encode them: register-based state stacks, csname lookup tables, explicit loop unrolling for search depth.
_Source: [latex-chess-engine (TeXCCChess)](https://blog.mathieuacher.com/TeXCCChessEngine/), line~388._ Frames synthesis as algorithm-level transfer + language-native encoding, not source-level translation.

> Coding agents can operate in Brainfuck at a scale never achieved before for a chess engine, not through raw translation but by designing intermediate abstractions (a pointer-tracking emitter, a memory layout manager, runtime loop patterns) that make the task tractable.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~12._ Explicit claim that synthesis required *designing new abstractions* (the Python compiler), not translating. RQ3 corroboration at its strongest.


### `agent-self-correction` --- Agent self-correction (debug loop)

_Supports: RQ5. Total excerpts: 7._

> TeX's \numexpr division rounds instead of truncating: 63/8 gives 8 (rounding 7.875 up), not 7. This was the source of one of the first nasty bugs.
_Source: [latex-chess-engine (TeXCCChess)](https://blog.mathieuacher.com/TeXCCChessEngine/), line~97._ A concrete language surprise that broke coordinate extraction; the agent fixed it by precomputing truncating-divide lookups.

> The ordering is critical and was a source of subtle bugs: \pushstate must be called after \makemove ... Getting this wrong produces moves that look almost right but occasionally corrupt castling rights (the kind of bug that shows up once every 50 games).
_Source: [latex-chess-engine (TeXCCChess)](https://blog.mathieuacher.com/TeXCCChessEngine/), line~173._ A long-tail bug only visible under gauntlet testing: the agent could not have caught it without oracle feedback.

> The first compilation of the test suite: 3 PASS, 6 FAIL. The culprit: sqfile(64) returned 0 instead of 8. ... After the fix: all 23 tests pass.
_Source: [latex-chess-engine (TeXCCChess)](https://blog.mathieuacher.com/TeXCCChessEngine/), line~318._ Perft-style test suite catches a regression; the agent fixes within the session. Paradigm case for oracle-driven debug loop.

> LaTeX's \newcount allocator had already reached register 360+, so the state stack at \count300-317 overlapped with LaTeX-internal registers. ... The agent traced it to a corrupted board value ... and moved the entire state stack to \count10000+.
_Source: [latex-chess-engine (TeXCCChess)](https://blog.mathieuacher.com/TeXCCChessEngine/), line~334._ Register collision is the TeX-native form of a memory-safety bug. The agent diagnosed and fixed it autonomously.

> The agent spent over 30 turns debugging (fixing alpha-beta cutoffs ... then pragmatically capping depth-C at 12 moves).
_Source: [latex-chess-engine (TeXCCChess)](https://blog.mathieuacher.com/TeXCCChessEngine/), line~353._ A single debugging episode consumes dozens of turns. Illustrates that self-correction is real but costly in this language.

> The naive approach (unrolling every board access at compile time) produced a 119 MB BF program. Four optimization strategies brought it down to 5.6 MB.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~86._ Cost-driven refactoring inside the session: the agent optimised size by 20x because 119 MB was impractical. Oracle was the interpreter's load time, not Elo.

> The hardest bugs were cell collisions: multiple code paths accidentally writing to the same memory cell. ... Claude Code found and fixed at least 9 such bugs across the development, including one where the print_char function was using cell 30 (= BOARD_START) as scratch space, corrupting the board every time any text was printed.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~177._ Quantified self-correction: 9 cell-collision fixes. A class of bug a human could not track at this scale; the agent could.


### `oracle-exploitation` --- Oracle exploitation (perft / Elo / gauntlets)

_Supports: RQ4, RQ5. Total excerpts: 6._

> The first compilation of the test suite: 3 PASS, 6 FAIL. The culprit: sqfile(64) returned 0 instead of 8. ... After the fix: all 23 tests pass.
_Source: [latex-chess-engine (TeXCCChess)](https://blog.mathieuacher.com/TeXCCChessEngine/), line~318._ Perft-style test suite catches a regression; the agent fixes within the session. Paradigm case for oracle-driven debug loop.

> All matches used Stockfish with UCI_LimitStrength=true at the 120+1s time control, which is the time control Stockfish's UCI_Elo scale was calibrated against (anchored to CCRL 40/4).
_Source: [latex-chess-engine (TeXCCChess)](https://blog.mathieuacher.com/TeXCCChessEngine/), line~292._ Agent-adjacent evaluation protocol. Correlates with the paper's canonical re-eval design; the author knew the calibration issue.

> Milestone | Elo | Lines of TeX: Random move picker 300 / Depth-2 minimax + material eval 550 / Depth-3 + alpha-beta + quiescence + PSTs 1280.
_Source: [latex-chess-engine (TeXCCChess)](https://blog.mathieuacher.com/TeXCCChessEngine/), line~370._ Feature introduction drives Elo: explicit +1000 Elo curve tied to search and evaluation additions.

> Perft validation: 11/11 positions correct (including castling and EP edge cases).
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~83._ Perft as the primary correctness oracle. Matches the population finding 'first perft at step 2' in RQ5.

> 'Run perft and compare to python-chess': verification-driven development. Perft caught several move generation bugs early.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~173._ Human-steered oracle invocation, agent-executed. Typical 'capability-level prompt drives oracle-rigorous work' pattern.

> 'Play 10 games against Stockfish and show me the PGN': assessment loops.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~175._ Assessment-loop as the dominant interaction. Every iteration is a gauntlet request.


### `human-steering` --- Human steering / intervention

_Supports: RQ5. Total excerpts: 6._

> The challenge I gave Claude Code was deliberately vague: I want to build a chess engine in LaTeX... I did not specify the architecture, the search algorithm, or the data structures.
_Source: [latex-chess-engine (TeXCCChess)](https://blog.mathieuacher.com/TeXCCChessEngine/), line~24._ Confirms the corpus-canonical minimal-prompt style that the paper describes in RQ5.

> The approach was deliberately iterative. I did not hand Claude Code a specification.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~171._ Confirms minimal-prompt style. Paper's RQ5 interaction-abstraction claim: capability-level prompts dominate.

> The division of labor was roughly: the agent writes and debugs code, the human steers priorities and evaluates results.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~196._ A crisp role split. Answers 'at what abstraction do users prompt?' for the Brainfuck case: roadmap-level.

> 'Run perft and compare to python-chess': verification-driven development. Perft caught several move generation bugs early.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~173._ Human-steered oracle invocation, agent-executed. Typical 'capability-level prompt drives oracle-rigorous work' pattern.

> 'Play 10 games against Stockfish and show me the PGN': assessment loops.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~175._ Assessment-loop as the dominant interaction. Every iteration is a gauntlet request.

> When working with coding agents on constrained tasks, the human must actively verify that the constraints are respected, because the agent may 'solve' the problem by relaxing them.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~198._ Turns the evasion observation into a methodological prescription. Supports the paper's qualitative-supervision protocol (§4.4).


### `feature-adaptation` --- Language-native feature adaptation

_Supports: RQ2, RQ3. Total excerpts: 7._

> It is neither a translation nor a copy of an existing chess engine. ... The creativity lies in finding TeX-native ways to encode them: register-based state stacks, csname lookup tables, explicit loop unrolling for search depth.
_Source: [latex-chess-engine (TeXCCChess)](https://blog.mathieuacher.com/TeXCCChessEngine/), line~388._ Frames synthesis as algorithm-level transfer + language-native encoding, not source-level translation.

> The \count registers serve as RAM ... the \csname lookup tables act as a read-only ROM for precomputed data (file/rank mappings, piece-square tables, material values). Token lists serve as dynamically allocated buffers. Macros ... are the instruction set.
_Source: [latex-chess-engine (TeXCCChess)](https://blog.mathieuacher.com/TeXCCChessEngine/), line~37._ Explicit 'TeX as a virtual machine' framing: every chess-engine primitive is mapped to a TeX primitive. Paradigm case for feature-adaptation.

> This pattern (precompute into \csname tables at load time, look up by name expansion at runtime) is used throughout the engine. It is the TeX equivalent of a hash map.
_Source: [latex-chess-engine (TeXCCChess)](https://blog.mathieuacher.com/TeXCCChessEngine/), line~113._ Named language idiom: hash map = \csname lookup. Reinforces 'language-native idiom', not 'copied from a template'.

> Brainfuck has no board[index] where index is a runtime value. To read a square whose index is computed at runtime, the engine must execute a 64-way switch: compare the index against 0, 1, 2, ..., 63 and copy from the matching fixed cell. ... Every board read or write is ~20 KB of BF code.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~68._ The paradigm single constraint: random-access cost. Drives the 5.6 MB size. No Brainfuck idiom eliminates it; the language-native encoding IS the 64-way switch.

> Coding agents can operate in Brainfuck at a scale never achieved before for a chess engine, not through raw translation but by designing intermediate abstractions (a pointer-tracking emitter, a memory layout manager, runtime loop patterns) that make the task tractable.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~12._ Explicit claim that synthesis required *designing new abstractions* (the Python compiler), not translating. RQ3 corroboration at its strongest.

> The generated chess.bf is 5.6 MB of raw Brainfuck. An RLE-optimized interpreter (bfi.c) compresses it at load time from ~3.8M characters to ~520K instructions (7x compression), with a precomputed jump table for O(1) bracket matching.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~49._ The engine required co-designing a custom interpreter to be practically runnable. The language ceiling forced both agent-side optimization and runtime-side optimization.

> The engine uses 672 cells on the BF tape, each with a carefully assigned role: Cells 0-15 Temporaries, Cells 30-93 Chess board (64 squares), Cells 160-183 Depth-2/3 search control, Cells 400-471 Depth-2 state backup.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~53._ A hand-rolled memory layout with explicit address ranges is the Brainfuck-native analogue of a C struct or a Python class. This is pure language-native encoding.


### `feedback-loop-cost` --- Feedback-loop cost dominates

_Supports: RQ5. Total excerpts: 5._

> The agent spent over 30 turns debugging (fixing alpha-beta cutoffs ... then pragmatically capping depth-C at 12 moves).
_Source: [latex-chess-engine (TeXCCChess)](https://blog.mathieuacher.com/TeXCCChessEngine/), line~353._ A single debugging episode consumes dozens of turns. Illustrates that self-correction is real but costly in this language.

> The naive approach (unrolling every board access at compile time) produced a 119 MB BF program. Four optimization strategies brought it down to 5.6 MB.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~86._ Cost-driven refactoring inside the session: the agent optimised size by 20x because 119 MB was impractical. Oracle was the interpreter's load time, not Elo.

> The division of labor was roughly: the agent writes and debugs code, the human steers priorities and evaluates results.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~196._ A crisp role split. Answers 'at what abstraction do users prompt?' for the Brainfuck case: roadmap-level.

> The real bottleneck was not writing the code, but evaluating it. Each iteration of 'change something, regenerate chess.bf, play games, see if it improved' takes hours.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~180._ A direct quote of the paper's cost-scales-with-oracle-rigor claim. The Brainfuck cost structure is an upper bound.

> Generating chess.bf: ~1-2 minutes. One move from the engine: 45 seconds (opening) to 600+ seconds (complex middlegame). A 10-game tournament: 3-8 hours. A complete test-fix-retest cycle: half a day.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~187._ Concrete cost numbers for each step of the feedback loop. 'Half a day per test-fix cycle' operationalises why Elo optimisation plateaus.


### `evasion-risk` --- Evasion risk (drift to a more expressive language)

_Supports: RQ3, Method. Total excerpts: 3._

> A parallel attempt was made with Codex (GPT-5.3) to build the same kind of engine. ... The Brainfuck components are kept for backward compatibility but are not the active engine core. In other words, the agent quietly migrated critical logic back into Python.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~198._ A fully documented case of agent-driven constraint relaxation. Mirrors the chess-css-codex evasion the paper discusses in RQ3.

> When working with coding agents on constrained tasks, the human must actively verify that the constraints are respected, because the agent may 'solve' the problem by relaxing them.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~198._ Turns the evasion observation into a methodological prescription. Supports the paper's qualitative-supervision protocol (§4.4).

> In the BFChess project with Claude Code, the constraint held because the architecture (Python compiler emitting BF, with the engine running solely through ./bfi chess.bf) made it structurally impossible to smuggle Python logic into the runtime.
_Source: [chess-brainfuck-cc (BFChess)](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), line~198._ Structural-enforcement strategy for the language constraint: the *architecture* (compile-to-BF then run a fixed interpreter) prevents the evasion. Complements the human-verification prescription.


## Per-source digests

### latex-chess-engine (TeXCCChess)
_Source: [TeXCCChess: How Coding Agents Wrote a Chess Engine in Pure TeX](https://blog.mathieuacher.com/TeXCCChessEngine/), 2026-02-24._

- **`language-constraint`** (5): l.~17; l.~97; l.~173; l.~334; l.~266
- **`novelty-absence`** (2): l.~18; l.~20
- **`synthesis-not-copy`** (2): l.~20; l.~388
- **`agent-self-correction`** (5): l.~97; l.~173; l.~318; l.~334; l.~353
- **`oracle-exploitation`** (3): l.~318; l.~292; l.~370
- **`human-steering`** (1): l.~24
- **`feature-adaptation`** (3): l.~388; l.~37; l.~113
- **`feedback-loop-cost`** (1): l.~353

### chess-brainfuck-cc (BFChess)
_Source: [BFChess: A Chess Engine in Brainfuck, Built by a Coding Agent](https://blog.mathieuacher.com/BFChessChessEngineBrainfuck/), 2026-03-23._

- **`language-constraint`** (4): l.~14; l.~68; l.~49; l.~177
- **`novelty-absence`** (1): l.~20
- **`synthesis-not-copy`** (1): l.~12
- **`agent-self-correction`** (2): l.~86; l.~177
- **`oracle-exploitation`** (3): l.~83; l.~173; l.~175
- **`human-steering`** (5): l.~171; l.~196; l.~173; l.~175; l.~198
- **`feature-adaptation`** (4): l.~68; l.~12; l.~49; l.~53
- **`feedback-loop-cost`** (4): l.~86; l.~196; l.~180; l.~187
- **`evasion-risk`** (3): l.~198; l.~198; l.~198

## Synthesis: how the coded evidence corroborates each RQ

### Method

_Codes supporting this RQ: `evasion-risk` (3 excerpts across both sources)._

The `evasion-risk` code contributes evidence that the paper's qualitative-supervision protocol is not hypothetical. The Brainfuck post documents a concrete Codex-vs-Claude-Code contrast on the same constraint: under Codex, critical logic was silently migrated to Python; under Claude Code, the architecture (Python compiler emits BF, then `./bfi chess.bf` runs it) made the drift structurally impossible. The methodological prescription --- structural enforcement where possible, active human verification where not --- is the same prescription the paper's §4.4 adopts.

### RQ2

_Codes supporting this RQ: `language-constraint`, `feature-adaptation` (16 excerpts across both sources)._

The `language-constraint` and `feature-adaptation` codes together describe *why* the feature set is language-shaped. The TeX source narrates `\count`-registers-as-RAM and `\csname`-tables-as-hash-maps as first-class idioms; the Brainfuck source narrates the 64-way switch as the irreducible cost of random access and the 672-cell layout as a struct-equivalent. Neither case is 'agent translated a reference engine into the target language' --- both cases are 'agent designed the smallest language-native encoding that supports a given chess feature'. This corroborates the within-language variance finding: feature choice is mediated by which language idioms the agent picks, not by the language alone.

### RQ3

_Codes supporting this RQ: `novelty-absence`, `synthesis-not-copy`, `feature-adaptation`, `evasion-risk` (16 excerpts across both sources)._

The `novelty-absence` and `synthesis-not-copy` codes converge: both posts explicitly assert no prior open-source chess engine exists in the target language (with search venues enumerated for TeX, and the 2019 TalkChess attempt reviewed and excluded for Brainfuck), and both argue that the existing engine cannot be a line-by-line memorisation. The TeX post goes further: the creativity sits at the algorithm-to-idiom translation layer, not at the line-by-line translation layer. The `evasion-risk` code flags the failure mode --- agent drifting to Python inside a Brainfuck engine --- and its two remedies (structural enforcement of the constraint; active human verification) match the paper's §4.4 qualitative-supervision protocol and the §7.4 chess-css-codex evasion case.

### RQ4

_Codes supporting this RQ: `language-constraint`, `oracle-exploitation` (15 excerpts across both sources)._

The `oracle-exploitation` code corroborates the paper's 'oracle-first is a population property' finding: perft as primary correctness oracle in both posts; cutechess gauntlets at CCRL 120$+$1 in the TeX post; random-move baselines when Stockfish is too strong in the Brainfuck post. The `language-constraint` code provides qualitative evidence for the Elo ceiling: TeX's macro-expansion depth caps search at 3 plies + quiescence (~\elo{1280}); Brainfuck's 64-way array access makes 3-ply search cost 45--600s per move (~\elo{100-200}). The ceiling is not about what the LLM knows about chess; it is about what the language's execution model admits under realistic time budgets.

### RQ5

_Codes supporting this RQ: `agent-self-correction`, `oracle-exploitation`, `human-steering`, `feedback-loop-cost` (24 excerpts across both sources)._

All three cost/interaction codes fire here. `human-steering` confirms the capability-level prompt style (both sources explicitly state the deliberately-vague PL-ROOT). `agent-self-correction` is quantified for Brainfuck (9 cell-collision bugs found and fixed autonomously) and for TeX (the 30-turn debug loop chasing the depth-3 timeout). `feedback-loop-cost` is the sharpest qualitative match to the paper's cost-scales-with-oracle-rigor finding: 'the real bottleneck was not writing the code, but evaluating it', with a concrete 'half a day per test-fix cycle' in Brainfuck. These are not ornamental quotes; each one is the developer-side view of a behaviour the paper describes quantitatively at the population level.

## How to extend this pilot

To turn this pilot into a section of the paper, add entries to `data/qualitative/codes.json` for any of:

1. Further blog posts by the first author (`2026-03-03-PrintfOrientedProgrammingCodingAgents.md`, `2026-03-17-CodingAgentsMnMLang.md`, `2026-02-23-FromScratchChessEnginesPolyglot.md`, \ldots)
2. Repository-level `ARCHITECTURE.md`, `SPECIFICATION.md`, and `README.md` files authored by the agent for each engine (e.g., `chess-java-cc/SPECIFICATION.md`, `COBOL-chess/ARCHITECTURE.md`).
3. Expert-interview notes (Brainfuck, Rocq, Why3 informants) once anonymised.

Re-run `python3 scripts/qualitative_coding.py` to regenerate this file. Inter-rater reliability, if the paper claims it, should be established by a second coder on at least 30\% of the excerpts --- record their codings in a second JSON file and report Cohen's kappa per code.
