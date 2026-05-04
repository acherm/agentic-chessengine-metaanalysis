# Folder triage (internal review)

_Generated 2026-04-22 14:52 UTC_

Every chess-related folder under `~/SANDBOX` is listed here with its in-/out-of-scope classification and a one-line rationale. The paper's corpus is the **engine** + **engine-variant** buckets.

## Counts by bucket

| Bucket | Folders |
|---|---:|
| `engine` | 29 |
| `engine-codesign` | 1 |
| `engine-dsl` | 1 |
| `engine-failure` | 1 |
| `engine-port` | 2 |
| `oos-challenge-arena` | 1 |
| `oos-css-variant` | 1 |
| `oos-experiment` | 2 |
| `oos-exploration` | 5 |
| `oos-external-corpus` | 1 |
| `oos-minichess-variant` | 2 |
| `oos-prior-work` | 1 |
| `oos-prototype` | 1 |
| `oos-study` | 4 |
| `oos-tool` | 2 |
| `oos-tournament-harness` | 1 |
| `oos-training-research` | 1 |
| `oos-variant-game` | 1 |
| **Total discovered** | **57** |

## Per-folder triage

| Folder | Bucket | Primary lang. | LOC | Sessions | Note |
|---|---|---|---:|---:|---|
| `COBOL-chess` | `engine` | COBOL | 8,890 | 3 | Second COBOL engine (CC), cobochess. Full UCI + perft + cutechess harness. (The vendored cutechess-cli source tree is now excluded from LOC counts.) |
| `Chess1MChallenge` | `oos-challenge-arena` | Python | 233,944 | 2 | Hugging Face arena (Gradio) for a course-style LLM chess challenge; not an agent-built engine. |
| `chess-Rocq` | `engine` | OCaml | 6,335 | 1 | Rocq/Coq specification extracted to OCaml (CC). |
| `chess-apl-codex54` | `engine` | APL | 3,652 | 2 | APL engine (CC+Codex). Perft + gauntlet evidence. |
| `chess-assembly-codex` | `engine` | Assembly | 12,310 | 1 | x86 Assembly engine (Codex). ~12k LOC hand-written asm. |
| `chess-brainfuck` | `engine` | Python | 6,920 | 2 | BF engine via Python code-gen (Codex). |
| `chess-brainfuck-cc` | `engine` | Python | 7,879 | 4 | BF engine via Python code-gen (CC+Codex). ~100–200 Elo. |
| `chess-brainfuck-gpt54-instant` | `oos-prototype` | — | 3 | 0 | Trivial 3-LOC one-shot experiment; not a working engine. |
| `chess-cobol-cc` | `engine` | C | 11,578 | 1 | COBOL engine (CC). ~$518 spend, ~1600 Elo claim. |
| `chess-conway` | `oos-exploration` | JavaScript | 1,366 | 0 | Chess/Conway exploration; not an engine. |
| `chess-cplusplus-claude` | `engine` | C++ | 4,248 | 0 | C++ engine (CC). |
| `chess-css-codex` | `engine` | HTML | 38,684 | 1 | CSS engine (Codex). Evasion-risk case: initial sessions used python-chess under the hood; after qualitative review the first author redirected the agent to produce a strict-CSS variant under strict-css/. Documented as an RQ3 case. |
| `chess-css-codex-guided` | `engine` | JavaScript | 2,077 | 1 | Small pure-HTML+CSS+JS experiment (Codex, 4 files) with legal move generation and perft 1--3. Separate repository from chess-css-codex; used as a second Codex try on the same premise. |
| `chess-css-x86` | `oos-css-variant` | HTML | 60,470 | 1 | CSS/HTML variant superseded by chess-css-codex --- user removed from engine corpus. |
| `chess-excel` | `oos-exploration` | Python | 2,935 | 2 | Excel-based board, no search pipeline. |
| `chess-fem` | `oos-study` | Python | 235,408 | 0 | Feature-engineering study of FIDE/LLM play; not an engine. |
| `chess-icon-codex` | `engine` | Icon | 3,217 | 1 | Icon-language engine (Codex). |
| `chess-in-conway` | `oos-study` | Python | 13,956 | 0 | Chess-inside-Conway's-Life simulation; not an engine. |
| `chess-java` | `engine` | Java | 2,835 | 1 | Java engine (Codex). |
| `chess-java-cc` | `engine` | Java | 4,884 | 1 | Java engine (CC). Surprising 2600-range Elo in PGN; flagged for re-eval. |
| `chess-kasparov-claim` | `oos-study` | Python | 6,026 | 0 | Study of Kasparov-claim narrative; analytical not constructive. |
| `chess-kasparov-claim-bis` | `oos-study` | Python | 3,405 | 0 | Follow-up study of Kasparov-claim. |
| `chess-latex-codex-replication` | `engine` | LaTeX | 5,222 | 1 | LaTeX replication attempt (Codex). ~800 Elo MLE. |
| `chess-lean-vibe` | `oos-exploration` | — | 0 | 0 | Empty Lean prototype. |
| `chess-llmtraining` | `oos-training-research` | Python | 10,313 | 2 | LLM fine-tuning research, not an engine built by the agent. |
| `chess-mojo` | `engine-failure` | Mojo | 3,472 | 1 | Failure case (engine-failure): Codex produced a Mojo UCI scaffold + perft + alpha-beta search but the engine plateaued at $\approx$900 Elo and did not converge to a competitive pipeline. Included for transparency, excluded from main analysis tables. |
| `chess-newlang-codex` | `engine-dsl` | C++ | 4,658 | 1 | DSL experiment (engine-dsl): Codex designs the GAMBIT DSL (.gmb) and its C++17 transpiler; engine runs via generated C++. Reported separately in paper. |
| `chess-polyglot-eval` | `oos-tournament-harness` | Python | 15,322 | 1 | Tournament harness that runs multiple engines; tool, not engine. |
| `chess-printf` | `oos-experiment` | C | 1,020 | 0 | Printf-only experiment (CC). User removed from scope. |
| `chess-printf-codex` | `oos-experiment` | C | 55,639 | 5 | Printf-only experiment (Codex). User removed from scope. |
| `chess-purec` | `engine` | C | 3,158 | 0 | Plain-C engine (CC). ~2100 Elo. |
| `chess-purec-codex` | `engine` | C | 3,095 | 1 | Plain-C engine (Codex). ~1800 Elo. |
| `chess-py` | `engine` | Python | 3,890 | 1 | Python engine (Codex). |
| `chess-py-cc` | `engine` | Python | 2,995 | 0 | Python engine (CC); main transcript archived, subagent logs only. |
| `chess-revisit-java-toCOBOL-codex` | `engine-port` | COBOL | 6,770 | 1 | Port experiment (engine-port): Codex translates chess-java-cc to GNU COBOL. Different protocol from scratch builds; reported separately in paper. |
| `chess-revisit-java-toRust-codex` | `engine-port` | COBOL | 11,141 | 2 | Port experiment (engine-port): Codex translates chess-java-cc to Rust. Different protocol from scratch builds; reported separately in paper. |
| `chess-ruby-cc` | `engine` | Ruby | 2,964 | 1 | Ruby engine (CC). ~1840 Elo on 420 rated games. |
| `chess-ruby-codex` | `engine` | Ruby | 124,443 | 1 | Ruby engine (Codex). Less rigorous gauntlets. |
| `chess-rust-cc` | `engine` | Rust | 5,872 | 0 | Rust engine (CC). ~2100 Elo; transcript largely archived. |
| `chess-rust-cc-redo` | `engine` | Rust | 3,329 | 1 |  |
| `chess-rust-codex` | `engine` | Rust | 1,819 | 1 | Rust engine (Codex). ~1750 Elo. |
| `chess-sql` | `engine` | Python | 2,016 | 0 | SQL engine (CC). |
| `chess-why3` | `engine` | OCaml | 4,530 | 1 | Why3 engine extracted to OCaml (Codex). |
| `chess-why3-cc` | `engine` | C | 91,558 | 0 | Why3 engine with C extraction (CC). ~2000 Elo. |
| `chessball` | `oos-variant-game` | Rust | 40,014 | 3 | Chess×football variant; out of scope for chess engines. |
| `chessfoo` | `oos-exploration` | JavaScript | 1,007 | 7 | Sandbox exploration (JavaScript). |
| `chessfoo-claude` | `oos-exploration` | TypeScript | 8,392 | 0 | TypeScript port of chessfoo; exploration. |
| `chessprogramming-vm` | `oos-external-corpus` | Python | 1,384,448 | 6 | Cloned third-party corpus of classical engines, not agent-built. |
| `chesspuzzle-tex-codex` | `oos-tool` | LaTeX | 58,242 | 1 | PGN → TeX puzzle renderer; not an engine. |
| `cplusplus-chess` | `engine` | C++ | 4,420 | 1 | C++ engine with CMake + perft (CC). |
| `gptchess` | `oos-prior-work` | Python | 74,114 | 0 | Prior-published GPT-chess study by M. Acher; not an agent-built engine. |
| `latex-chess-engine` | `engine` | LaTeX | 41,185 | 1 | TeXCCChess --- canonical pure-TeX engine (CC). Claims ``first chess engine in pure TeX'' at ~1300 Elo. |
| `lean-chess` | `engine` | Lean | 2,333 | 1 | Lean 4 engine with perft harness (CC). |
| `minichess-5x5-repro` | `oos-minichess-variant` | Rust | 22,558 | 5 | Gardner 5x5 minichess weak-solver (Rust). Variant game, not standard 8x8 chess --- user removed from engine corpus. |
| `minichess-5x5-repro-cc` | `oos-minichess-variant` | Rust | 5,814 | 1 | Gardner 5x5 minichess (CC). Same --- removed. |
| `puzzles-chess` | `oos-tool` | Python | 714 | 0 | Puzzle/SVG renderer; not an engine. |
| `test-superset` | `engine-codesign` | HTML | 224,772 | 0 | Co-design experiment (engine-codesign): ChessCSS --- a 55k-rule, ~17MB pure-CSS chess engine built in 31 commits over 5 days (2026-02-27 to 2026-03-03). The agent (Claude Code) progressively replaced JavaScript logic with CSS rules (:has() selectors, CSS if(), z-index argmax + elementFromPoint for move selection). The engine's README explicitly notes the author had to 'drive the agent with technical expertise ... and encourage the agents to not giving up with CSS' --- that is, the session protocol differs from the corpus's minimal-instruction default. Reported separately from the main corpus for that reason; treated as a cousin to the ports/DSL/failure special-role bucket. |

## Scope rules

- **engine** — a chess-playing system built by a frontier agent; plays standard 8×8 chess.
- **engine-variant** — engine for a non-standard variant (Gardner 5×5 minichess in our corpus).
- **oos-…** — out of scope. Subtypes: `tool` (renderers, harnesses), `study` (observational papers), `exploration` (unfinished prototypes), `prior-work` (predates the agent era or is the user's own published research), `training-research` (LLM fine-tuning), `variant-game` (not chess), `external-corpus` (cloned third-party engines).