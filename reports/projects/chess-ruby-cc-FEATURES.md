# chess-ruby-cc — feature-introduction trajectory

_Generated 2026-04-20 05:53 UTC_

Source: 139 Write/Edit/apply_patch events scanned against the 38-pattern chess-feature catalog (see `scripts/common.py::CHESS_PATTERNS`).

- **Distinct features detected**: 32 / 39
- **Total session steps**: 16
- **Feature introduction density**: 32 features in 16 steps ≈ 2.00 features/step

## Feature appearance order (earliest first)

| # | Step | Feature | Group | File | Kind |
|---:|---:|---|---|---|---|
| 1 | 3 | Board: 0x88 | Board representation | `…/constants.rb` | Write |
| 2 | 3 | Board: mailbox 8x8 | Board representation | `…/piece_square_tables.rb` | Write |
| 3 | 3 | Castling | Rules & protocol | `…/constants.rb` | Write |
| 4 | 3 | Check/Checkmate | Rules & protocol | `…/board.rb` | Write |
| 5 | 3 | En passant | Rules & protocol | `…/constants.rb` | Write |
| 6 | 3 | Evaluation/PST | Evaluation | `…/chess_engine.rb` | Write |
| 7 | 3 | FEN parsing | Rules & protocol | `…/constants.rb` | Write |
| 8 | 3 | History heuristic | Search extensions | `…/search.rb` | Write |
| 9 | 3 | Iterative deepening | Search core | `…/search.rb` | Write |
| 10 | 3 | Killer moves | Search extensions | `…/search.rb` | Write |
| 11 | 3 | Late-move reduction (LMR) | Search extensions | `…/search.rb` | Write |
| 12 | 3 | Material counting | Evaluation | `…/constants.rb` | Write |
| 13 | 3 | Minimax/Negamax | Search core | `…/search.rb` | Write |
| 14 | 3 | Move ordering (MVV-LVA) | Search extensions | `…/constants.rb` | Write |
| 15 | 3 | Null-move pruning | Search extensions | `…/search.rb` | Write |
| 16 | 3 | PGN | Rules & protocol | `…/elo_test.sh` | Write |
| 17 | 3 | Perft | Search core | `…/test_perft.rb` | Write |
| 18 | 3 | Promotion | Rules & protocol | `…/move.rb` | Write |
| 19 | 3 | Quiescence | Search core | `…/search.rb` | Write |
| 20 | 3 | Time management | Strong-engine features | `…/time_manager.rb` | Write |
| 21 | 3 | Transposition table | Search core | `…/chess_engine.rb` | Write |
| 22 | 3 | UCI protocol | Rules & protocol | `…/chess_engine.rb` | Write |
| 23 | 3 | Zobrist hashing | Search core | `…/chess_engine.rb` | Write |
| 24 | 7 | Aspiration windows | Search extensions | `…/search.rb` | Write |
| 25 | 7 | Futility pruning | Search extensions | `…/search.rb` | Write |
| 26 | 7 | King safety | Evaluation | `…/evaluation.rb` | Write |
| 27 | 7 | Mobility | Evaluation | `…/evaluation.rb` | Write |
| 28 | 7 | Pawn structure | Evaluation | `…/evaluation.rb` | Write |
| 29 | 7 | Principal-variation (PV) | Search extensions | `…/search.rb` | Write |
| 30 | 9 | Late-move pruning (LMP) | Search extensions | `…/search.rb` | Write |
| 31 | 9 | Razoring | Search extensions | `…/search.rb` | Write |
| 32 | 9 | Tapered evaluation | Evaluation | `…/piece_square_tables.rb` | Write |

## Per-group introduction timeline

### Rules & protocol

| Feature | Step | File |
|---|---:|---|
| FEN parsing | 3 | `…/constants.rb` |
| UCI protocol | 3 | `…/chess_engine.rb` |
| PGN | 3 | `…/elo_test.sh` |
| Castling | 3 | `…/constants.rb` |
| En passant | 3 | `…/constants.rb` |
| Promotion | 3 | `…/move.rb` |
| Check/Checkmate | 3 | `…/board.rb` |

### Board representation

| Feature | Step | File |
|---|---:|---|
| Board: 0x88 | 3 | `…/constants.rb` |
| Board: mailbox 8x8 | 3 | `…/piece_square_tables.rb` |

### Search core

| Feature | Step | File |
|---|---:|---|
| Minimax/Negamax | 3 | `…/search.rb` |
| Iterative deepening | 3 | `…/search.rb` |
| Quiescence | 3 | `…/search.rb` |
| Transposition table | 3 | `…/chess_engine.rb` |
| Zobrist hashing | 3 | `…/chess_engine.rb` |
| Perft | 3 | `…/test_perft.rb` |

### Search extensions

| Feature | Step | File |
|---|---:|---|
| Move ordering (MVV-LVA) | 3 | `…/constants.rb` |
| Killer moves | 3 | `…/search.rb` |
| History heuristic | 3 | `…/search.rb` |
| Null-move pruning | 3 | `…/search.rb` |
| Late-move reduction (LMR) | 3 | `…/search.rb` |
| Principal-variation (PV) | 7 | `…/search.rb` |
| Aspiration windows | 7 | `…/search.rb` |
| Futility pruning | 7 | `…/search.rb` |
| Late-move pruning (LMP) | 9 | `…/search.rb` |
| Razoring | 9 | `…/search.rb` |

### Evaluation

| Feature | Step | File |
|---|---:|---|
| Material counting | 3 | `…/constants.rb` |
| Evaluation/PST | 3 | `…/chess_engine.rb` |
| King safety | 7 | `…/evaluation.rb` |
| Pawn structure | 7 | `…/evaluation.rb` |
| Mobility | 7 | `…/evaluation.rb` |
| Tapered evaluation | 9 | `…/piece_square_tables.rb` |

### Strong-engine features

| Feature | Step | File |
|---|---:|---|
| Time management | 3 | `…/time_manager.rb` |

## Cumulative feature count per step

Each row: after step $k$, the agent had touched a cumulative total of $n(k)$ distinct features in newly-written content.

```
step   1:  0  
step   2:  0  
step   3: 23  ███████████████████████
step   4: 23  ███████████████████████
step   5: 23  ███████████████████████
step   6: 23  ███████████████████████
step   7: 29  █████████████████████████████
step   8: 29  █████████████████████████████
step   9: 32  ████████████████████████████████
step  10: 32  ████████████████████████████████
step  11: 32  ████████████████████████████████
step  12: 32  ████████████████████████████████
step  13: 32  ████████████████████████████████
step  14: 32  ████████████████████████████████
step  15: 32  ████████████████████████████████
step  16: 32  ████████████████████████████████
```
