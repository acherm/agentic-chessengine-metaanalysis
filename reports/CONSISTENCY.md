# Consistency report: paper vs. blog post vs. polyglot-eval

_Comparison of the Elo numbers this paper reports against two prior evaluation runs by the first author:_
- **Blog post (2026-02)**: `blog.mathieuacher.com/FromScratchChessEnginesPolyglot/`, tier-list numbers transcribed in `scripts/consistency_report.py`.
- **polyglot-eval**: `~/SANDBOX/chess-polyglot-eval/metrics.json`, an earlier evaluation run over 9 engines.
- **This paper**: per-engine PGN-derived Elo (inverse-variance aggregate) + agent-claimed Elo band mined from session transcripts.

## Per-engine comparison

| Engine | Lang. | Polyglot-eval Elo (method, N) | Blog tier / Elo | Ours: PGN Elo (N) | Ours: agent-claimed | Discrepancy note |
|---|---|---|---|---|---|---|
| COBOL-chess | COBOL | 1598 (vs Stockfish 1600, N=200) | 2 / ~1530-1560 | — | — |  |
| chess-Rocq | OCaml | 1575 (Gauntlet vs Stockfish 1320/1500/1700, N=150) | 3 / ~1450 | 1319 (N=560) | — | **Δ=-255** vs polyglot-eval |
| chess-brainfuck | Python | — | — | 1113 (N=75) | — |  |
| chess-brainfuck-cc | Python | — | — | 578 (N=145) | — |  |
| chess-cplusplus-claude | C++ | 1835 (Gauntlet vs Stockfish (Skill 10, UCI_Elo 1800), N=120) | 2 / ~1700-1900 | 2018 (N=698) | — |  |
| chess-icon-codex | Icon | — | — | 704 (N=113) | — |  |
| chess-java | Java | — | 2 / ~1700-1900 | — | — |  |
| chess-java-cc | Java | — | 1 / ~2200 | 2603 (N=240) | — | **Δ=+403** vs blog |
| chess-latex-codex-replication | LaTeX | — | 3 / ~900 | 546 (N=292) | — | **Δ=-353** vs blog |
| chess-mojo | Mojo | — | — | 963 (N=350) | — |  |
| chess-newlang-codex | C++ | — | 1 / ~1950-2200 | — | — |  |
| chess-polyglot-eval | Python | — | — | 1750 (N=1027) | — |  |
| chess-purec | C | 2210 (Gauntlet vs Stockfish 2200 (closest to 50%), N=600) | 1 / ~1950-2200 | 2147 (N=1400) | — |  |
| chess-purec-codex | C | — | 1 / ~1950-2200 | 1836 (N=500) | — |  |
| chess-py | Python | — | 1 / ~1950-2200 | — | — |  |
| chess-py-cc | Python | — | 2 / ~1700-1900 | — | — |  |
| chess-ruby-cc | Ruby | — | — | 1840 (N=440) | — |  |
| chess-rust-cc | Rust | — | 1 / ~1950-2200 | 2110 (N=364) | — |  |
| chess-rust-cc-redo | Rust | — | — | 1853 (N=1200) | — |  |
| chess-rust-codex | Rust | — | 1 / ~1950-2200 | 1746 (N=410) | — |  |
| chess-sql | Python | 1019 (vs Stockfish 1320, N=100) | 3 / ~1120 | — | — |  |
| chess-why3 | OCaml | — | 2 / ~1530-1560 | 1008 (N=240) | — |  |
| chess-why3-cc | C | — | 2 / ~1700-1900 | 1991 (N=180) | — |  |
| chessprogramming-vm | Python | — | — | 1886 (N=7900) | — |  |
| cplusplus-chess | C++ | 2044 (vs Stockfish 2000, N=774) | — | — | — |  |
| gptchess | Python | — | — | 1485 (N=6) | — |  |
| latex-chess-engine | LaTeX | 1292 (vs Stockfish 1320, N=100) | 3 / ~1280 | 1260 (N=170) | — |  |
| lean-chess | Lean | 1484 (vs Stockfish 1320, N=50) | — | 1404 (N=390) | — |  |
| test-superset | HTML | — | — | 629 (N=8) | — |  |

## Discrepancies to investigate (|Δ| ≥ 200 Elo)

- `chess-Rocq`: polyglot-eval=1575 vs ours=1319
- `chess-java-cc`: blog~2200 vs ours=2603
- `chess-latex-codex-replication`: blog~900 vs ours=546

## Likely causes of discrepancies

1. **Different opponent ladders.** Our PGN-derived Elo aggregates only what survives in-tree; polyglot-eval used a deliberately-designed ladder (1320 / 1500 / 1700 / 1900 / 2100) at 120+1. The engine faced different mixes.
2. **Time-control mismatch.** `UCI_LimitStrength` is calibrated for 120+1 (CCRL 40/4). Many of our surviving PGNs were played at 10+0.1 or 30+0.3; the Elo-vs-opponent mapping is not identical.
3. **Inflated single-opponent wins.** When only one PGN survives (e.g.\ `chess-java-cc` with a single 2200-level gauntlet in which the Java engine scored heavily), the logistic Elo estimate extrapolates far above the opponent's Elo --- a known artifact.
4. **Evolving engines.** The blog snapshot is February 2026; several engines received further iterations between February and April. Our April numbers reflect the final state of the repository.

## What to report in the paper

- Cite the blog tier list as a prior estimate and report our own per-engine numbers alongside, flagging the method mismatch.
- Commit to a **unified re-evaluation pass** (see `eval/README.md`) using the polyglot-eval opponent ladder at 120+1 for a single directly comparable Elo per engine.
- Use the blog-quoted performance deltas (e.g.\ ``C\texttt{++} reaches depth 22--25 in 10s; COBOL depth 9; SQL depth 2'') as concrete evidence of the language-ceiling effect in §Discussion.
