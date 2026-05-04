# Maturity ladder per engine

Cumulative levels (each engine satisfies all checked + sometimes more):

- L1: Builds (binary/image exists)
- L2: UCI handshake (preflight uciok+readyok)
- L3: Move-gen correct (perft pass OR clean game play with no disconnect)
- L4: Plays at least one full game (anchor PGN with ≥1 completed game)
- L5: Long-game robust (≥8 games completed per pair without disconnect)
- L6: Measurable Elo (≥1 anchor where engine scored >0%)
- L7: Reaches ~1700+ (best anchor/RR Elo ≥1700)
- L8: Reaches ~2000+ (best anchor/RR Elo ≥2000; CCRL-comparable)

| Engine | Tier | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | Best Elo |
|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---:|
| chess-java-cc | B | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 2096 |
| chess-rust-cc-redo | A | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | 1989 |
| chess-revisit-java-toRust-codex | A | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | 1922 |
| chess-rust-cc | A | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | 1887 |
| chess-ruby-cc | B | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | 1839 |
| chess-cplusplus-claude | A | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | 1821 |
| chess-rust-codex | A | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | 1803 |
| chess-py | B | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | 1777 |
| chess-why3-cc | B | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | 1736 |
| chess-py-cc | B | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | 1720 |
| cplusplus-chess | A | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | 1709 |
| chess-java | B | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | — | 1664 |
| chess-purec | A | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | — | 1633 |
| chess-assembly-codex | A | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | — | 1625 |
| chess-purec-codex | A | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | — | 1578 |
| chess-ruby-codex | B | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | — | 1530 |
| lean-chess | B | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | — | 1514 |
| COBOL-chess | B | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | — | 1514 |
| chess-Rocq | B | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | — | 1499 |
| chess-cobol-cc | B | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | — | 1497 |
| chess-brainfuck | C | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | — | — |
| chess-revisit-java-toCOBOL-codex | B | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | — | — |
| chess-why3 | B | ✓ | ✓ | ✓ | ✓ | ✓ | — | — | — | 1471 |
| chess-icon-codex | B | ✓ | ✓ | ✓ | ✓ | ✓ | — | — | — | 1416 |
| chess-apl-codex54 | B | ✓ | ✓ | ✓ | ✓ | ✓ | — | — | — | 1282 |
| chess-latex-codex-replication | C | ✓ | ✓ | ✓ | ✓ | ✓ | — | — | — | 1207 |
| latex-chess-engine | C | ✓ | ✓ | ✓ | ✓ | ✓ | — | — | — | — |
| chess-sql | C | ✓ | ✓ | ✓ | ✓ | ✓ | — | — | — | — |
| chess-css-codex | B | ✓ | ✓ | — | — | — | — | — | — | — |
| chess-newlang-codex | A | ✓ | ✓ | — | — | — | — | — | — | — |
| chess-css-codex-guided | B | ✓ | — | — | — | — | — | — | — | — |
| chess-brainfuck-cc | C | ✓ | — | — | — | — | — | — | — | — |
| chess-css-cc | B | — | — | — | — | — | — | — | — | — |
