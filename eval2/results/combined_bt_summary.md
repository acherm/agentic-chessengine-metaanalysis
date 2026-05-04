# Unified Bradley-Terry Elo: Phase B + round-robin pooled

BT MLE over **3,256 games** across **531 unique pairs**, anchored simultaneously to Rustic (1820), Asymptote (2150), and Stockfish Skill 0/5/10/15 (Phase A calibration). All games at TC=120+1.

Per-engine CIs from a paired-game bootstrap (n=200 resamples).

| Engine | **BT Elo** | ±95% CI | Phase B | RR | Δ(BT − Phase B) | Δ(BT − RR) |
|---|---:|---:|---:|---:|---:|---:|
| `sf_skill11` | **2262** | ±189 | — | — | — | — |
| `sf_skill8` | **2127** | ±2012 | — | — | — | — |
| `chess-java-cc` | **2094** | ±56 | 2096 ± 132 | 2050 | -2 | +44 |
| `sf_skill9` | **2016** | ±111 | — | — | — | — |
| `chess-rust-cc-redo` | **1990** | ±57 | 1989 ± 105 | 1989 | +1 | +1 |
| `chess-revisit-java-toRust-codex` | **1989** | ±54 | 1922 ± 106 | 2037 | +67 | -48 |
| `chess-rust-cc` | **1825** | ±58 | 1841 ± 99 | 1882 | -16 | -57 |
| `sf_skill7` | **1816** | ±97 | — | — | — | — |
| `chess-purec-retry` | **1798** | ±82 | — | — | — | — |
| `chess-ruby-cc` | **1753** | ±55 | — | 1816 | — | -63 |
| `chess-rust-codex` | **1707** | ±63 | 1723 ± 103 | 1801 | -16 | -94 |
| `sf_skill6` | **1683** | ±75 | — | — | — | — |
| `chess-cplusplus-claude` | **1682** | ±58 | 1680 ± 103 | 1816 | +2 | -134 |
| `cplusplus-chess` | **1627** | ±69 | 1709 ± 111 | 1686 | -82 | -59 |
| `chess-newlang-codex` | **1622** | ±68 | 1758 ± 143 | 1678 | -136 | -56 |
| `chess-py` | **1616** | ±55 | — | 1771 | — | -155 |
| `chess-why3-cc` | **1567** | ±56 | 1618 ± 163 | 1714 | -51 | -147 |
| `sf_skill4` | **1545** | ±69 | — | — | — | — |
| `chess-py-cc` | **1499** | ±55 | — | 1714 | — | -215 |
| `chess-java` | **1483** | ±72 | 1509 ± 131 | 1665 | -26 | -182 |
| `chess-assembly-codex` | **1468** | ±72 | 1403 ± 196 | 1631 | +65 | -163 |
| `chess-purec` | **1415** | ±65 | 1440 ± 193 | 1645 | -25 | -230 |
| `chess-revisit-java-toCOBOL-codex` | **1404** | ±69 | — | 1590 | — | -186 |
| `chess-purec-codex` | **1402** | ±73 | — | 1555 | — | -153 |
| `sf_skill3` | **1396** | ±68 | — | — | — | — |
| `COBOL-chess` | **1365** | ±80 | — | 1519 | — | -154 |
| `chess-ruby-codex` | **1346** | ±72 | — | 1511 | — | -165 |
| `chess-Rocq` | **1315** | ±83 | 1499 ± 171 | 1481 | -184 | -166 |
| `chess-brainfuck` | **1299** | ±94 | 1392 ± 136 | — | -93 | — |
| `chess-cobol-cc` | **1274** | ±85 | — | 1511 | — | -237 |
| `lean-chess` | **1271** | ±75 | — | 1511 | — | -240 |
| `sf_skill2` | **1242** | ±93 | — | — | — | — |
| `chess-why3` | **1210** | ±74 | — | 1474 | — | -264 |
| `chess-icon-codex` | **1168** | ±88 | 1008 ± 248 | 1442 | +160 | -274 |
| `sf_skill1` | **1133** | ±184 | — | — | — | — |
| `chess-apl-codex54` | **686** | ±205 | 709 ± 248 | 1285 | -23 | -599 |
| `chess-sql` | **523** | ±297 | 518 ± 248 | — | +5 | — |
| `chess-latex-codex-replication` | **-3235** | ±76 | — | 1207 | — | -4442 |
| `latex-chess-engine` | **-3480** | ±236 | — | — | — | — |
