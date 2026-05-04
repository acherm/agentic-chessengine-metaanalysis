# Deep-dive: chess-rust-cc-redo

_Second-try Rust engine, built from scratch with no `chess` crate
dependency. Replaces the evasion case in the original Rust cell._

## Context

The Rust cell originally held two engines: `chess-rust-codex`
(Codex, scratch-built but using the `chess` crate for board-state
types) and `chess-rust-cc` (Claude Code, scratch-built but with
archived transcripts). The crate dependency in the first Rust row
was an evasion: the agent delegated board representation, move
generation, and legal-move checking to a library and authored only
search and evaluation. This "redo" re-runs Rust from a blank slate
under the explicit constraint "no chess crate", so the whole stack
(board, move gen, search, eval, UCI) is agent-authored.

## Engine summary

| | |
|---|---|
| Language | Rust |
| Agent | Claude Code (4 conversations, compacted) |
| Prompts | 55 |
| Cost (USD, list) | $63.94 |
| Wallclock hours (longest session) | 70.3 |
| LOC (src/) | ~2,755 |
| Perft tests | 35 (CPW positions, depth 1–6) |
| Board representation | Bitboards, PEXT/PDEP slider attacks |
| Search features | Iterative deepening, PVS, two-tier TT, null-move, LMR, LMP, futility, reverse-futility, singular extensions, ProbCut, SEE pruning, IID |
| Move ordering | TT move + SEE captures + history + killers + countermoves |
| Eval | Material + PST + tapered MG/EG + pawn structure + king safety |
| Stated Elo goal | 2000 vs calibrated Stockfish |
| Reached Elo (PGN, 1,200 games) | **1,853 ±24.7** |
| Per-opponent Elo (inverse-variance) | vs SF-L5 (~1650): 1,890; SF-L8 (~1900): 1,862; SF-L10 (~2000): 1,752; SF-L13 (~2400): 1,963 |

## Observations

Three qualitative observations from this session, ordered by how
directly they constrain the paper's quantitative readings.

### 1. High effort, moderate payoff in a mainstream general-purpose language

Rust has no execution-model handicap for a chess engine; the feature
set implemented is essentially the full modern search-extension
catalogue; the agent had multi-session budget and a single
concentrated goal. Elo 2000 was out of reach anyway. The engine
converged to ~1,850 Elo, which is within the "strong" band but well
short of the stated target.

This is a counter-data-point to a naive reading of the Elo table:
Rust _can_ top the corpus (`chess-rust-cc` at ~2,110) but does not
always, under comparable scratch-build commitment. The ceiling
effect is real.

### 2. Benchmarking misallocation; the user had to intervene

The gauntlet burned 1,200 games across four Stockfish skill levels:
L5 (~1650), L8 (~1900), L10 (~2000), L13 (~2400). Read against the
final ~1,850 Elo estimate:

- **SF-L5 (300 games, 80% score)** — engine crushes this opponent;
  score is saturated; no calibration information.
- **SF-L8 (300 games, 45% score)** — ideal calibration point;
  informative.
- **SF-L10 (300 games, 19% score)** — informative but asymmetric.
- **SF-L13 (300 games, 7.5% score)** — engine gets crushed; score
  is saturated; no calibration information.

Half of the 600 games spent on L5 and L13 were largely wasted, and
it was clear to the user _before_ the gauntlet finished that L13 was
too strong and L5 too weak for this engine's band. The agent did not
adjust the gauntlet composition on its own; the user had to be
proactive and stop the mis-calibrated matches.

This is a session-level pattern the aggregate cost table and the
SE-activity matrix do not surface: evaluation time can be
mis-allocated in a way the agent does not detect, even when the
tooling to do better (shrinking the opponent ladder after a few
games at extremes) is within the agent's capability.

### 3. Chess domain knowledge surfaced at the wrong level of abstraction

Partway through the session the agent diagnosed recurring weaknesses
in the engine's opening play by replaying the gauntlet games,
identifying specific anti-patterns (piece placement errors in the
Sicilian, weak responses to 1. d4 setups), and proposing an
**opening book** as the fix.

Two things going on here.

**What's striking**: the agent reaches for game-level analysis, not
just code-level debugging. It read its own PGN output and evaluated
move sequences the way a human chess student would. The coding agent
is drawing on chess-domain knowledge that goes beyond programming.

**What's problematic**: the fix it proposed is, from a chess
expert's point of view, a short-term workaround rather than a
remedy. The engine's opening losses were symptoms of a deeper
evaluation or search issue — giving a piece away for nothing in a
quasi-tactical position — that an opening book cannot remedy. The
book masks the bug in positions it covers and leaves it intact
everywhere else.

This cuts two ways:

- **Benchmark caveat.** Chess has a domain-knowledge surface area.
  Agents that understand chess better can debug their own play in
  ways that domain-agnostic agents cannot, and this affects measured
  strength. A coding-agent benchmark built on chess tests
  programming _plus chess_, not programming in isolation.
- **Capability observation.** Domain-knowledge usage is not
  uniformly helpful. Surface-level pattern recognition ("my openings
  lose") can drive fixes that do not address the underlying
  engineering problem ("my evaluation of quiet-tactical positions is
  off"), and the agent did not distinguish the two here.

## Pointer

Paper deep-dive: `paper/appendix/A7-deepdive-rust-redo.tex`.
Source: `~/SANDBOX/chess-rust-cc-redo/`. Transcript:
`~/.claude/projects/-Users-mathieuacher-SANDBOX-chess-rust-cc-redo/bd32e433-e56a-4205-bf0a-32497952d6d4.jsonl`.
PGN gauntlets: `~/SANDBOX/chess-rust-cc-redo/elo_results{,_v2,_v3}/sf_level{5,8,10,13}.pgn`.
