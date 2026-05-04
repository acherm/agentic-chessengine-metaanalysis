# chess-java-cc — feature-introduction trajectory

_Generated 2026-04-20 04:42 UTC_

Source: 4 Write/Edit/apply_patch events scanned against the 38-pattern chess-feature catalog (see `scripts/common.py::CHESS_PATTERNS`).

- **Distinct features detected**: 32 / 39
- **Total session steps**: 6
- **Feature introduction density**: 32 features in 6 steps ≈ 5.33 features/step

## Feature appearance order (earliest first)

| # | Step | Feature | Group | File | Kind |
|---:|---:|---|---|---|---|
| 1 | 4 | Alpha-beta | Search core | `…/SPECIFICATION.md` | Write |
| 2 | 4 | Aspiration windows | Search extensions | `…/SPECIFICATION.md` | Write |
| 3 | 4 | Board: bitboard | Board representation | `…/SPECIFICATION.md` | Write |
| 4 | 4 | Board: magic bitboards | Board representation | `…/SPECIFICATION.md` | Write |
| 5 | 4 | Board: mailbox 8x8 | Board representation | `…/SPECIFICATION.md` | Write |
| 6 | 4 | Castling | Rules & protocol | `…/SPECIFICATION.md` | Write |
| 7 | 4 | Check/Checkmate | Rules & protocol | `…/SPECIFICATION.md` | Write |
| 8 | 4 | En passant | Rules & protocol | `…/SPECIFICATION.md` | Write |
| 9 | 4 | Evaluation/PST | Evaluation | `…/SPECIFICATION.md` | Write |
| 10 | 4 | FEN parsing | Rules & protocol | `…/SPECIFICATION.md` | Write |
| 11 | 4 | Futility pruning | Search extensions | `…/SPECIFICATION.md` | Write |
| 12 | 4 | History heuristic | Search extensions | `…/SPECIFICATION.md` | Write |
| 13 | 4 | Iterative deepening | Search core | `…/SPECIFICATION.md` | Write |
| 14 | 4 | Killer moves | Search extensions | `…/SPECIFICATION.md` | Write |
| 15 | 4 | King safety | Evaluation | `…/SPECIFICATION.md` | Write |
| 16 | 4 | Late-move reduction (LMR) | Search extensions | `…/SPECIFICATION.md` | Write |
| 17 | 4 | Material counting | Evaluation | `…/SPECIFICATION.md` | Write |
| 18 | 4 | Minimax/Negamax | Search core | `…/SPECIFICATION.md` | Write |
| 19 | 4 | Mobility | Evaluation | `…/SPECIFICATION.md` | Write |
| 20 | 4 | Move ordering (MVV-LVA) | Search extensions | `…/SPECIFICATION.md` | Write |
| 21 | 4 | Null-move pruning | Search extensions | `…/SPECIFICATION.md` | Write |
| 22 | 4 | Opening book | Strong-engine features | `…/SPECIFICATION.md` | Write |
| 23 | 4 | Pawn structure | Evaluation | `…/SPECIFICATION.md` | Write |
| 24 | 4 | Perft | Search core | `…/SPECIFICATION.md` | Write |
| 25 | 4 | Principal-variation (PV) | Search extensions | `…/SPECIFICATION.md` | Write |
| 26 | 4 | Promotion | Rules & protocol | `…/SPECIFICATION.md` | Write |
| 27 | 4 | Quiescence | Search core | `…/SPECIFICATION.md` | Write |
| 28 | 4 | Tapered evaluation | Evaluation | `…/SPECIFICATION.md` | Write |
| 29 | 4 | Time management | Strong-engine features | `…/SPECIFICATION.md` | Write |
| 30 | 4 | Transposition table | Search core | `…/SPECIFICATION.md` | Write |
| 31 | 4 | UCI protocol | Rules & protocol | `…/SPECIFICATION.md` | Write |
| 32 | 4 | Zobrist hashing | Search core | `…/SPECIFICATION.md` | Write |

## Per-group introduction timeline

### Rules & protocol

| Feature | Step | File |
|---|---:|---|
| FEN parsing | 4 | `…/SPECIFICATION.md` |
| UCI protocol | 4 | `…/SPECIFICATION.md` |
| Castling | 4 | `…/SPECIFICATION.md` |
| En passant | 4 | `…/SPECIFICATION.md` |
| Promotion | 4 | `…/SPECIFICATION.md` |
| Check/Checkmate | 4 | `…/SPECIFICATION.md` |

### Board representation

| Feature | Step | File |
|---|---:|---|
| Board: bitboard | 4 | `…/SPECIFICATION.md` |
| Board: magic bitboards | 4 | `…/SPECIFICATION.md` |
| Board: mailbox 8x8 | 4 | `…/SPECIFICATION.md` |

### Search core

| Feature | Step | File |
|---|---:|---|
| Minimax/Negamax | 4 | `…/SPECIFICATION.md` |
| Alpha-beta | 4 | `…/SPECIFICATION.md` |
| Iterative deepening | 4 | `…/SPECIFICATION.md` |
| Quiescence | 4 | `…/SPECIFICATION.md` |
| Transposition table | 4 | `…/SPECIFICATION.md` |
| Zobrist hashing | 4 | `…/SPECIFICATION.md` |
| Perft | 4 | `…/SPECIFICATION.md` |

### Search extensions

| Feature | Step | File |
|---|---:|---|
| Move ordering (MVV-LVA) | 4 | `…/SPECIFICATION.md` |
| Killer moves | 4 | `…/SPECIFICATION.md` |
| History heuristic | 4 | `…/SPECIFICATION.md` |
| Principal-variation (PV) | 4 | `…/SPECIFICATION.md` |
| Null-move pruning | 4 | `…/SPECIFICATION.md` |
| Late-move reduction (LMR) | 4 | `…/SPECIFICATION.md` |
| Aspiration windows | 4 | `…/SPECIFICATION.md` |
| Futility pruning | 4 | `…/SPECIFICATION.md` |

### Evaluation

| Feature | Step | File |
|---|---:|---|
| Material counting | 4 | `…/SPECIFICATION.md` |
| Evaluation/PST | 4 | `…/SPECIFICATION.md` |
| Tapered evaluation | 4 | `…/SPECIFICATION.md` |
| King safety | 4 | `…/SPECIFICATION.md` |
| Pawn structure | 4 | `…/SPECIFICATION.md` |
| Mobility | 4 | `…/SPECIFICATION.md` |

### Strong-engine features

| Feature | Step | File |
|---|---:|---|
| Opening book | 4 | `…/SPECIFICATION.md` |
| Time management | 4 | `…/SPECIFICATION.md` |

## Cumulative feature count per step

Each row: after step $k$, the agent had touched a cumulative total of $n(k)$ distinct features in newly-written content.

```
step   1:  0  
step   2:  0  
step   3:  0  
step   4: 32  ████████████████████████████████
step   5: 32  ████████████████████████████████
step   6: 32  ████████████████████████████████
```
