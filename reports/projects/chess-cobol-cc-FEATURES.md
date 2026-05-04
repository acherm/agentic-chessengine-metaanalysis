# chess-cobol-cc — feature-introduction trajectory

_Generated 2026-04-20 05:53 UTC_

Source: 331 Write/Edit/apply_patch events scanned against the 38-pattern chess-feature catalog (see `scripts/common.py::CHESS_PATTERNS`).

- **Distinct features detected**: 24 / 39
- **Total session steps**: 37
- **Feature introduction density**: 24 features in 37 steps ≈ 0.65 features/step

## Feature appearance order (earliest first)

| # | Step | Feature | Group | File | Kind |
|---:|---:|---|---|---|---|
| 1 | 4 | Castling | Rules & protocol | `…/chess-engine.cob` | Write |
| 2 | 4 | Check/Checkmate | Rules & protocol | `…/chess-engine.cob` | Write |
| 3 | 4 | En passant | Rules & protocol | `…/chess-engine.cob` | Write |
| 4 | 4 | FEN parsing | Rules & protocol | `…/chess-engine.cob` | Write |
| 5 | 4 | Promotion | Rules & protocol | `…/chess-engine.cob` | Write |
| 6 | 4 | UCI protocol | Rules & protocol | `…/chess-engine.cob` | Write |
| 7 | 6 | Evaluation/PST | Evaluation | `…/chess-engine.cob` | Edit |
| 8 | 6 | Material counting | Evaluation | `…/chess-engine.cob` | Edit |
| 9 | 8 | Alpha-beta | Search core | `…/chess-engine.cob` | Edit |
| 10 | 8 | Minimax/Negamax | Search core | `…/chess-engine.cob` | Edit |
| 11 | 17 | Iterative deepening | Search core | `…/chess-engine.cob` | Edit |
| 12 | 17 | Move ordering (MVV-LVA) | Search extensions | `…/chess-engine.cob` | Edit |
| 13 | 17 | Time management | Strong-engine features | `…/chess-engine.cob` | Edit |
| 14 | 21 | Killer moves | Search extensions | `…/chess-engine.cob` | Edit |
| 15 | 21 | Quiescence | Search core | `…/chess-engine.cob` | Edit |
| 16 | 26 | Aspiration windows | Search extensions | `…/chess-engine.cob` | Edit |
| 17 | 26 | Futility pruning | Search extensions | `…/chess-engine.cob` | Edit |
| 18 | 26 | History heuristic | Search extensions | `…/chess-engine.cob` | Edit |
| 19 | 26 | Null-move pruning | Search extensions | `…/chess-engine.cob` | Edit |
| 20 | 32 | Late-move reduction (LMR) | Search extensions | `…/chess-engine.cob` | Edit |
| 21 | 32 | Pawn structure | Evaluation | `…/chess-engine.cob` | Edit |
| 22 | 33 | Tapered evaluation | Evaluation | `…/chess-engine.cob` | Edit |
| 23 | 36 | King safety | Evaluation | `…/project_elo_progress.md` | Write |
| 24 | 36 | Principal-variation (PV) | Search extensions | `…/chess-engine.cob` | Edit |

## Per-group introduction timeline

### Rules & protocol

| Feature | Step | File |
|---|---:|---|
| FEN parsing | 4 | `…/chess-engine.cob` |
| UCI protocol | 4 | `…/chess-engine.cob` |
| Castling | 4 | `…/chess-engine.cob` |
| En passant | 4 | `…/chess-engine.cob` |
| Promotion | 4 | `…/chess-engine.cob` |
| Check/Checkmate | 4 | `…/chess-engine.cob` |

### Search core

| Feature | Step | File |
|---|---:|---|
| Minimax/Negamax | 8 | `…/chess-engine.cob` |
| Alpha-beta | 8 | `…/chess-engine.cob` |
| Iterative deepening | 17 | `…/chess-engine.cob` |
| Quiescence | 21 | `…/chess-engine.cob` |

### Search extensions

| Feature | Step | File |
|---|---:|---|
| Move ordering (MVV-LVA) | 17 | `…/chess-engine.cob` |
| Killer moves | 21 | `…/chess-engine.cob` |
| History heuristic | 26 | `…/chess-engine.cob` |
| Null-move pruning | 26 | `…/chess-engine.cob` |
| Aspiration windows | 26 | `…/chess-engine.cob` |
| Futility pruning | 26 | `…/chess-engine.cob` |
| Late-move reduction (LMR) | 32 | `…/chess-engine.cob` |
| Principal-variation (PV) | 36 | `…/chess-engine.cob` |

### Evaluation

| Feature | Step | File |
|---|---:|---|
| Material counting | 6 | `…/chess-engine.cob` |
| Evaluation/PST | 6 | `…/chess-engine.cob` |
| Pawn structure | 32 | `…/chess-engine.cob` |
| Tapered evaluation | 33 | `…/chess-engine.cob` |
| King safety | 36 | `…/project_elo_progress.md` |

### Strong-engine features

| Feature | Step | File |
|---|---:|---|
| Time management | 17 | `…/chess-engine.cob` |

## Cumulative feature count per step

Each row: after step $k$, the agent had touched a cumulative total of $n(k)$ distinct features in newly-written content.

```
step   1:  0  
step   2:  0  
step   3:  0  
step   4:  6  ██████
step   5:  6  ██████
step   6:  8  ████████
step   7:  8  ████████
step   8: 10  ██████████
step   9: 10  ██████████
step  10: 10  ██████████
step  11: 10  ██████████
step  12: 10  ██████████
step  13: 10  ██████████
step  14: 10  ██████████
step  15: 10  ██████████
step  16: 10  ██████████
step  17: 13  █████████████
step  18: 13  █████████████
step  19: 13  █████████████
step  20: 13  █████████████
step  21: 15  ███████████████
step  22: 15  ███████████████
step  23: 15  ███████████████
step  24: 15  ███████████████
step  25: 15  ███████████████
step  26: 19  ███████████████████
step  27: 19  ███████████████████
step  28: 19  ███████████████████
step  29: 19  ███████████████████
step  30: 19  ███████████████████
step  31: 19  ███████████████████
step  32: 21  █████████████████████
step  33: 22  ██████████████████████
step  34: 22  ██████████████████████
step  35: 22  ██████████████████████
step  36: 24  ████████████████████████
step  37: 24  ████████████████████████
```
