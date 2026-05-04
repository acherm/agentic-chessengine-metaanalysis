# NPS / search throughput bench (Q5)

Each engine is given `go movetime 5000` from startpos. We capture the
last `info nodes N nps M` line emitted, plus the depth reached.

Reference points:
- Stockfish 18: 866,603 nps
- Rustic Alpha 3.0.4 (CCRL 1820): 10,461,492 nps
- COBOL-chess: (no data)

| Engine | Depth reached | Nodes | NPS | vs Rustic | vs SF18 |
|---|---:|---:|---:|---:|---:|
| rustic (1820) | 9 | 9,101,498 | 10,461,492 | 1.00× | 1207.2% |
| chess-purec | 14 | 14,153,649 | 4,191,190 | 0.40× | 483.6% |
| chess-rust-cc | 21 | 1,501,873 | 3,257,859 | 0.31× | 375.9% |
| asymptote (2150) | 18 | 16,174,336 | 3,240,700 | 0.31× | 374.0% |
| chess-cplusplus-claude | 23 | 3,205,859 | 2,333,230 | 0.22× | 269.2% |
| cplusplus-chess | 13 | 5,635,783 | 1,802,297 | 0.17× | 208.0% |
| chess-java-cc | 14 | 3,507,493 | 1,310,232 | 0.13× | 151.2% |
| Stockfish 18 | 27 | 4,333,015 | 866,603 | 0.08× | 100.0% |
| chess-py | 9 | 173,361 | 42,057 | 0.00× | 4.9% |
| chess-ruby-cc | 11 | 62,238 | 20,425 | 0.00× | 2.4% |
| chess-rust-cc-redo | — | — | — | — | — |
| chess-rust-codex | 0 | 0 | 0 | 0.00× | 0.0% |
| COBOL-chess | — | — | — | — | — |
