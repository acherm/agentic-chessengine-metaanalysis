# Q2 self-reproduction summary (host-native, original methodology)

Each engine was run on host hardware against host Stockfish 18, using the *engine's own original* opponent set (UCI_Elo rungs or SF Skill levels), original TC, and original Hash size (per `runners/self_reproduction.yaml`). The `Repro` column is the Elo we measure under the engine's own methodology; the `Anchor` and `RR` columns are the rigorous measurements.

| Engine | Self-claim | **Repro** | Anchor (Phase B) | RR | Δ self vs anchor | Δ self vs repro |
|---|---|---:|---:|---:|---:|---:|
| `chess-Rocq` | 1500 | **1640 ± 101** | 1499 ± 171 | 1481 | -1 | +140 |
| `chess-cplusplus-claude` | 1897 | **1485 ± 124** | 1675 ± 103 | 1816 | -222 | -412 |
| `chess-purec` | 1997 | **2121 ± 78** | 1440 ± 193 | 1645 | -557 | +124 |
| `chess-purec-codex` | 1670–1972 | **1889 ± 78** | 1504 ± 160 | 1555 | — | — |
| `chess-ruby-cc` | 1840 | **1917 ± 124** | 1719 ± 110 | 1816 | -121 | +77 |
| `chess-rust-cc` | 2110 | **2208 ± 88** | 1841 ± 99 | 1882 | -269 | +98 |
| `chess-rust-cc-redo` | 1879 | **2355 ± 88** | 2023 ± 100 | 1989 | +144 | +476 |
| `chess-rust-codex` | 2043 | **1987 ± 88** | 1756 ± 103 | 1801 | -287 | -56 |
| `chess-why3-cc` | 1882 | **1959 ± 95** | 1598 ± 163 | 1714 | -284 | +77 |
| `cplusplus-chess` | 2087 | **1984 ± 101** | 1660 ± 111 | 1686 | -427 | -103 |

## Per-rung scores (Stockfish opponent strength is the agent's own label)

### `chess-Rocq` (repro: 1640 ± 101 from rungs)

| Opponent | Opp Elo | W | D | L | Score% |
|---|---:|---:|---:|---:|---:|
| sf_e1320 | 1320 | 18 | 0 | 2 | 90% |
| sf_e1500 | 1500 | 12 | 1 | 7 | 62% |
| sf_e1700 | 1700 | 7 | 2 | 11 | 40% |

### `chess-cplusplus-claude` (repro: 1485 ± 124 from rungs)

| Opponent | Opp Elo | W | D | L | Score% |
|---|---:|---:|---:|---:|---:|
| sf_sk10 | 2004 | 0 | 0 | 20 | 0% |
| sf_sk12 | 2150 | 0 | 0 | 20 | 0% |
| sf_sk14 | 2245 | 0 | 0 | 20 | 0% |
| sf_sk5 | 1658 | 8 | 0 | 12 | 40% |
| sf_sk7 | 1818 | 1 | 1 | 18 | 8% |

### `chess-purec` (repro: 2121 ± 78 from rungs)

| Opponent | Opp Elo | W | D | L | Score% |
|---|---:|---:|---:|---:|---:|
| sf_e1500 | 1500 | 19 | 0 | 1 | 95% |
| sf_e1800 | 1800 | 16 | 0 | 4 | 80% |
| sf_e2000 | 2000 | 7 | 0 | 13 | 35% |
| sf_e2200 | 2200 | 13 | 2 | 5 | 70% |
| sf_e2400 | 2400 | 6 | 3 | 11 | 38% |

### `chess-purec-codex` (repro: 1889 ± 78 from rungs)

| Opponent | Opp Elo | W | D | L | Score% |
|---|---:|---:|---:|---:|---:|
| sf_e1500 | 1500 | 17 | 1 | 2 | 88% |
| sf_e1700 | 1700 | 13 | 0 | 7 | 65% |
| sf_e1800 | 1800 | 15 | 0 | 5 | 75% |
| sf_e1900 | 1900 | 6 | 2 | 12 | 35% |
| sf_e2000 | 2000 | 9 | 3 | 8 | 52% |

### `chess-ruby-cc` (repro: 1917 ± 124 from rungs)

| Opponent | Opp Elo | W | D | L | Score% |
|---|---:|---:|---:|---:|---:|
| sf_e1500 | 1500 | 20 | 0 | 0 | 100% |
| sf_e1700 | 1700 | 13 | 1 | 6 | 68% |
| sf_e1900 | 1900 | 13 | 0 | 7 | 65% |

### `chess-rust-cc` (repro: 2208 ± 88 from rungs)

| Opponent | Opp Elo | W | D | L | Score% |
|---|---:|---:|---:|---:|---:|
| sf_e1500 | 1500 | 20 | 0 | 0 | 100% |
| sf_e1800 | 1800 | 18 | 0 | 2 | 90% |
| sf_e2000 | 2000 | 15 | 0 | 5 | 75% |
| sf_e2200 | 2200 | 9 | 0 | 11 | 45% |
| sf_e2400 | 2400 | 7 | 0 | 13 | 35% |

### `chess-rust-cc-redo` (repro: 2355 ± 88 from rungs)

| Opponent | Opp Elo | W | D | L | Score% |
|---|---:|---:|---:|---:|---:|
| sf_e1500 | 1500 | 20 | 0 | 0 | 100% |
| sf_e1800 | 1800 | 16 | 1 | 3 | 82% |
| sf_e2000 | 2000 | 18 | 0 | 2 | 90% |
| sf_e2200 | 2200 | 16 | 0 | 4 | 80% |
| sf_e2400 | 2400 | 13 | 1 | 6 | 68% |

### `chess-rust-codex` (repro: 1987 ± 88 from rungs)

| Opponent | Opp Elo | W | D | L | Score% |
|---|---:|---:|---:|---:|---:|
| sf_e1500 | 1500 | 17 | 1 | 2 | 88% |
| sf_e1800 | 1800 | 13 | 1 | 6 | 68% |
| sf_e2000 | 2000 | 10 | 3 | 7 | 57% |
| sf_e2200 | 2200 | 7 | 2 | 11 | 40% |

### `chess-why3-cc` (repro: 1959 ± 95 from rungs)

| Opponent | Opp Elo | W | D | L | Score% |
|---|---:|---:|---:|---:|---:|
| sf_e1500 | 1500 | 17 | 0 | 3 | 85% |
| sf_e1800 | 1800 | 10 | 2 | 8 | 55% |
| sf_e2000 | 2000 | 12 | 1 | 7 | 62% |
| sf_e2200 | 2200 | 5 | 1 | 2 | 69% |

### `cplusplus-chess` (repro: 1984 ± 101 from rungs)

| Opponent | Opp Elo | W | D | L | Score% |
|---|---:|---:|---:|---:|---:|
| sf_e1500 | 1500 | 18 | 1 | 1 | 92% |
| sf_e1800 | 1800 | 12 | 1 | 7 | 62% |
| sf_e2000 | 2000 | 13 | 1 | 6 | 68% |

