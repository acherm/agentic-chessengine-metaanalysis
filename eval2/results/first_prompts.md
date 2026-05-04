# First user prompt per engine session

Classified category from `eval2/scripts/first_prompts.py`:

- **C1** Canonical: `I want to build a chess engine in X programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels`
- **C2** Translation/port (e.g., Java→Rust)
- **C3** Plan-driven (user-supplied implementation plan)
- **C4** Inspired-by / external-source / replication
- **C5** Analysis / refactor / audit of an existing engine
- **C6** Other

## Category counts (core-engine sessions)

- C1: **17**
- C2: **3**
- C3: **2**
- C4: **1**
- C6: **3**

## Per-engine first prompts (core engines only)

### `chess-apl-codex54` — Codex (2026-03-05, 1 sessions, **C1**)

> I want to build a chess engine in APL programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

### `chess-assembly-codex` — Codex (2026-02-24, 1 sessions, **C1**)

> I want to build a chess engine in assembly language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

### `chess-brainfuck` — Codex (2026-02-20, 2 sessions, **C1**)

> I want to build a chess engine in Brainfuck programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

### `chess-brainfuck-cc` — CC (2026-02-28, 3 sessions, **C3**)

> Implement the following plan:
> 
> # Plan: Integrate Proper Chess Piece Values
> 
> ## Context
> 
> BFChess's `_score_move()` uses MVV capture values that don't reflect standard chess piece values:
> - Current: P=10, N=30, **B=30**, R=50, Q=90
> - **Bug**: Knight and Bishop have identical values (both 30), so the e

### `chess-cobol-cc` — CC (2026-03-12, 1 sessions, **C1**)

> I want to build a chess engine in COBOL (using GNU Cobol)… at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of “similar” levels.

### `chess-css-codex` — Codex (2026-02-28, 1 sessions, **C1**)

> I want to build a chess engine in pure CSS programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

### `chess-css-codex-guided` — Codex (2026-03-01, 1 sessions, **C4**)

> taking technical inspirations from https://lyra.horse/x86css/ incredible success, build a chess engine in pure CSS programming language...

### `chess-icon-codex` — Codex (2026-02-23, 1 sessions, **C1**)

> I want to build a chess engine in Icon programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

### `chess-java` — Codex (2026-02-17, 1 sessions, **C1**)

> I want to build a chess engine in Java programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

### `chess-java-cc` — CC (2026-03-10, 1 sessions, **C2**)

> could you specify a specification of the current chess engine (including supported features and design choices) in such a way I can share it to a coding agent that could try to implement the same software system, independently of the language?

### `chess-latex-codex-replication` — Codex (2026-02-16, 1 sessions, **C1**)

> I want to build a chess engine in LaTeX programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

### `chess-mojo` — Codex (2026-02-16, 1 sessions, **C1**)

> I want to build a chess engine in Mojo programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

### `chess-newlang-codex` — Codex (2026-02-27, 1 sessions, **C6**)

> Below is a **self-contained language + toolchain specification** for **GAMBIT v0.1** (a chess-engine-centric language). 
> 
> This spec is **performance-oriented** and deliberately scoped: v0.1 is “enough to build a real UCI chess engine” with movegen + alpha-beta + TT + evaluation, while leaving room f

### `chess-purec-codex` — Codex (2026-02-19, 1 sessions, **C1**)

> I want to build a chess engine in C programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

### `chess-py` — Codex (2026-02-11, 1 sessions, **C1**)

> I want to build a chess engine in Python programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

### `chess-revisit-java-toCOBOL-codex` — Codex (2026-02-19, 1 sessions, **C2**)

> The goal is to write a chess engine in COBOL programming language (using GNU Cobol) through the translation of an existing chess engine written in Java, and available here: /Users/mathieuacher/SANDBOX/chess-java-cc/
> 
> Please stick as much as possible to the original Java implementation, keeping the s

### `chess-revisit-java-toRust-codex` — Codex (2026-02-19, 2 sessions, **C2**)

> The goal is to write a chess engine in Rust through the translation of an existing chess engine written in Java, and available here: /Users/mathieuacher/SANDBOX/chess-java-cc/
> 
> Please stick as much as possible to the original Java implementation, keeping the same set of features, data structure, alg

### `chess-Rocq` — CC (2026-04-09, 1 sessions, **C6**)

> I would like to find traces of historical session in this repo... especially "prompts" I have used. I couldn't find them.
>   Perhaps in ~/.claude ? or is it codex?

### `chess-ruby-cc` — CC (2026-03-12, 1 sessions, **C3**)

> Implement the following plan:
> 
> # Ruby Chess Engine — Implementation Plan
> 
> ## Context
> 
> Build a chess engine from scratch in Ruby that can play legal chess, communicate via UCI protocol, and be tested for Elo rating against other engines using cutechess-cli.
> 
> ## Architecture Decisions
> 
> - **Board repre

### `chess-ruby-codex` — Codex (2026-03-12, 1 sessions, **C1**)

> I want to build a chess engine in Ruby… at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of “similar” levels.

### `chess-rust-cc-redo` — CC (2026-04-19, 1 sessions, **C6**)

> <local-command-caveat>Caveat: The messages below were generated by the user while running local commands. DO NOT respond to these messages or otherwise consider them in your response unless the user explicitly asks you to.</local-command-caveat>

### `chess-rust-codex` — Codex (2026-02-16, 1 sessions, **C1**)

> I want to build a chess engine in Rust programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

### `chess-why3` — Codex (2026-02-17, 1 sessions, **C1**)

> I want to build a chess engine in WhyML programming language (from Why3)... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

### `COBOL-chess` — Codex (2026-02-09, 2 sessions, **C1**)

> I want to build a chess engine in COBOL (GNUCobol)... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

### `cplusplus-chess` — Codex (2026-02-10, 1 sessions, **C1**)

> I want to build a chess engine in C++ programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

### `lean-chess` — Codex (2026-02-09, 1 sessions, **C1**)

> I want to build a chess engine in Lean programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels

## Engines with no build session in local cache

The following engines have only postmortem analysis sessions in
the local transcript cache; the original build session was either
not recorded (e.g., the engine pre-existed and the agent was only
asked to inspect it) or not retained. Their earliest postmortem
prompt is shown below for reference but is **not** a build
instruction and is excluded from the category counts above.

### `latex-chess-engine` — Codex (2026-02-19, 1 sessions, *postmortem-only*)

> I'd like to understand this code base... perform an in-depth analysis of implementation details, features of the chess engine, of the general approach and architecture. Pinpoint very important code snippets coming from the implementation

