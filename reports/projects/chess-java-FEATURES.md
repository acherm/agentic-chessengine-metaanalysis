# chess-java — feature-introduction trajectory

_Generated 2026-04-20 04:20 UTC_

Source: 25 Write/Edit/apply_patch events scanned against the 38-pattern chess-feature catalog (see `scripts/common.py::CHESS_PATTERNS`).

- **Distinct features detected**: 22 / 39
- **Total session steps**: 7
- **Feature introduction density**: 22 features in 7 steps ≈ 3.14 features/step

## Feature appearance order (earliest first)

| # | Step | Feature | Group | File | Kind |
|---:|---:|---|---|---|---|
| 1 | 1 | Alpha-beta | Search core | `README.md` | heredoc |
| 2 | 1 | Castling | Rules & protocol | `…/Undo.java` | heredoc |
| 3 | 1 | Check/Checkmate | Rules & protocol | `…/Board.java` | heredoc |
| 4 | 1 | En passant | Rules & protocol | `…/Move.java` | heredoc |
| 5 | 1 | Endgame tables | Strong-engine features | `README.md` | heredoc |
| 6 | 1 | Evaluation/PST | Evaluation | `…/Evaluator.java` | heredoc |
| 7 | 1 | FEN parsing | Rules & protocol | `…/Piece.java` | heredoc |
| 8 | 1 | Iterative deepening | Search core | `README.md` | heredoc |
| 9 | 1 | King safety | Evaluation | `README.md` | heredoc |
| 10 | 1 | Material counting | Evaluation | `…/Piece.java` | heredoc |
| 11 | 1 | Minimax/Negamax | Search core | `…/Search.java` | heredoc |
| 12 | 1 | Mobility | Evaluation | `README.md` | heredoc |
| 13 | 1 | Opening book | Strong-engine features | `README.md` | heredoc |
| 14 | 1 | PGN | Rules & protocol | `…/run_match.sh` | heredoc |
| 15 | 1 | Perft | Search core | `…/Perft.java` | heredoc |
| 16 | 1 | Promotion | Rules & protocol | `…/Piece.java` | heredoc |
| 17 | 1 | Quiescence | Search core | `…/Search.java` | heredoc |
| 18 | 1 | Tapered evaluation | Evaluation | `README.md` | heredoc |
| 19 | 1 | Time management | Strong-engine features | `…/SearchLimits.java` | heredoc |
| 20 | 1 | Transposition table | Search core | `README.md` | heredoc |
| 21 | 1 | UCI protocol | Rules & protocol | `…/UciEngine.java` | heredoc |
| 22 | 1 | Zobrist hashing | Search core | `README.md` | heredoc |

## Per-group introduction timeline

### Rules & protocol

| Feature | Step | File |
|---|---:|---|
| FEN parsing | 1 | `…/Piece.java` |
| UCI protocol | 1 | `…/UciEngine.java` |
| PGN | 1 | `…/run_match.sh` |
| Castling | 1 | `…/Undo.java` |
| En passant | 1 | `…/Move.java` |
| Promotion | 1 | `…/Piece.java` |
| Check/Checkmate | 1 | `…/Board.java` |

### Search core

| Feature | Step | File |
|---|---:|---|
| Minimax/Negamax | 1 | `…/Search.java` |
| Alpha-beta | 1 | `README.md` |
| Iterative deepening | 1 | `README.md` |
| Quiescence | 1 | `…/Search.java` |
| Transposition table | 1 | `README.md` |
| Zobrist hashing | 1 | `README.md` |
| Perft | 1 | `…/Perft.java` |

### Evaluation

| Feature | Step | File |
|---|---:|---|
| Material counting | 1 | `…/Piece.java` |
| Evaluation/PST | 1 | `…/Evaluator.java` |
| Tapered evaluation | 1 | `README.md` |
| King safety | 1 | `README.md` |
| Mobility | 1 | `README.md` |

### Strong-engine features

| Feature | Step | File |
|---|---:|---|
| Opening book | 1 | `README.md` |
| Endgame tables | 1 | `README.md` |
| Time management | 1 | `…/SearchLimits.java` |

## Cumulative feature count per step

Each row: after step $k$, the agent had touched a cumulative total of $n(k)$ distinct features in newly-written content.

```
step   1: 22  ██████████████████████
step   2: 22  ██████████████████████
step   3: 22  ██████████████████████
step   4: 22  ██████████████████████
step   5: 22  ██████████████████████
step   6: 22  ██████████████████████
step   7: 22  ██████████████████████
```
