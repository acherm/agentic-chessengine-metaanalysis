# Eval / domain-knowledge inventory (Q6)

Mirror of Q4 for chess-knowledge features in evaluation code.
Each cell is ✓ if a pattern for that eval term appears in the engine's eval-related source files.
**Tuned constants** is a count of integer literals (10..32000) in eval files — a proxy for how much
weight tuning the eval has received (a serious eval has hundreds; a sketch has dozens).
Catalogue: 22 eval features.

| Engine | Tier | Eval features | Tuned constants | PSQT | tapered-eval | passed-pawn | isolated-pawn | doubled-pawn | backward-pawn | pawn-chain | king-safety | pawn-shield | king-zone | bishop-pair | rook-open-file | rook-7th-rank | knight-outpost | bad-bishop | mobility | center-control | space-eval | endgame-table | KPK | tempo | contempt |
|---|---|---:|---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| chess-rust-cc-redo | A | 16/22 | 490 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |   | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |   | ✓ |   |   |   | ✓ | ✓ |   |
| chess-rust-cc | A | 14/22 | 30 |   | ✓ | ✓ | ✓ | ✓ | ✓ |   | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |   | ✓ |   |   |   |   | ✓ |   |
| chess-purec | A | 13/22 | 554 | ✓ | ✓ | ✓ | ✓ | ✓ |   |   | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |   | ✓ |   |   |   |   |   |   |
| chess-ruby-cc | B | 12/22 | 16 |   | ✓ | ✓ | ✓ | ✓ |   |   | ✓ | ✓ |   | ✓ | ✓ | ✓ | ✓ |   | ✓ |   |   |   |   | ✓ |   |
| chess-cplusplus-claude | A | 11/22 | 481 | ✓ | ✓ | ✓ | ✓ | ✓ |   |   | ✓ | ✓ |   | ✓ | ✓ |   |   |   | ✓ |   |   |   |   | ✓ |   |
| chess-py | B | 11/22 | 193 | ✓ | ✓ | ✓ | ✓ | ✓ |   |   | ✓ | ✓ |   | ✓ | ✓ |   |   |   | ✓ |   |   |   |   | ✓ |   |
| chess-py-cc | B | 10/22 | 16 |   | ✓ | ✓ | ✓ | ✓ |   |   | ✓ | ✓ |   | ✓ | ✓ |   |   |   | ✓ |   |   |   |   | ✓ |   |
| cplusplus-chess | A | 8/22 | 219 | ✓ |   | ✓ | ✓ | ✓ |   |   | ✓ |   |   | ✓ | ✓ |   |   |   | ✓ |   |   |   |   |   |   |
| COBOL-chess | B | 8/22 | 60 |   |   | ✓ | ✓ | ✓ |   |   |   | ✓ |   | ✓ | ✓ | ✓ |   |   |   |   |   | ✓ |   |   |   |
| chess-cobol-cc | B | 7/22 | 2927 | ✓ | ✓ | ✓ | ✓ | ✓ |   |   |   |   |   | ✓ | ✓ |   |   |   |   |   |   |   |   |   |   |
| chess-why3-cc | B | 6/22 | 538 | ✓ | ✓ | ✓ | ✓ | ✓ |   |   |   |   |   | ✓ |   |   |   |   |   |   |   |   |   |   |   |
| chess-ruby-codex | B | 6/22 | 131 | ✓ |   |   | ✓ | ✓ |   |   | ✓ |   |   | ✓ | ✓ |   |   |   |   |   |   |   |   |   |   |
| chess-css-codex | B | 6/22 | 19 |   |   | ✓ | ✓ | ✓ |   |   |   |   | ✓ |   |   |   |   |   | ✓ |   |   |   |   | ✓ |   |
| chess-apl-codex54 | B | 5/22 | 219 | ✓ |   | ✓ | ✓ | ✓ |   |   | ✓ |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| chess-java-cc | B | 5/22 | 66 |   | ✓ |   |   |   |   |   | ✓ |   |   | ✓ |   |   |   |   | ✓ |   |   |   |   | ✓ |   |
| chess-rust-codex | A | 3/22 | 259 |   |   | ✓ |   |   |   |   | ✓ |   |   |   |   |   |   |   | ✓ |   |   |   |   |   |   |
| chess-Rocq | B | 3/22 | 26 | ✓ |   |   |   |   |   |   |   |   |   | ✓ |   | ✓ |   |   |   |   |   |   |   |   |   |
| chess-sql | C | 2/22 | 36 | ✓ |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | ✓ |   |   |   |   |   |
| lean-chess | B | 2/22 | 24 |   |   | ✓ |   |   |   |   | ✓ |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| latex-chess-engine | C | 1/22 | 40261 | ✓ |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| chess-brainfuck-cc | C | 1/22 | 732 |   |   |   |   |   |   |   |   |   |   |   |   | ✓ |   |   |   |   |   |   |   |   |   |
| chess-purec-codex | A | 1/22 | 227 |   |   |   |   |   |   |   | ✓ |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| chess-css-codex-guided | B | 1/22 | 29 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | ✓ |   |   |   |   |   |   |
| chess-assembly-codex | A | 0/22 | 2123 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| chess-why3 | B | 0/22 | 170 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| chess-latex-codex-replication | C | 0/22 | 141 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| chess-java | B | 0/22 | 124 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| chess-icon-codex | B | 0/22 | 119 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| chess-css-cc | B | 0/22 | 1 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| chess-brainfuck | C | 0/22 | 0 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |

## Summary

- Engines analysed: 30
- Median eval feature count: 5
- Median tuned-constant count: 141
- Eval-rich engines (≥10 features): chess-rust-cc-redo, chess-rust-cc, chess-purec, chess-ruby-cc, chess-cplusplus-claude, chess-py, chess-py-cc
- Eval-poor engines (≤3 features): chess-rust-codex, chess-Rocq, chess-sql, lean-chess, latex-chess-engine, chess-brainfuck-cc, chess-purec-codex, chess-css-codex-guided, chess-assembly-codex, chess-why3, chess-latex-codex-replication, chess-java, chess-icon-codex, chess-css-cc, chess-brainfuck
