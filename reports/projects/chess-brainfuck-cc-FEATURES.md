# chess-brainfuck-cc — feature-introduction trajectory

_Generated 2026-04-20 05:53 UTC_

Source: 87 Write/Edit/apply_patch events scanned against the 38-pattern chess-feature catalog (see `scripts/common.py::CHESS_PATTERNS`).

- **Distinct features detected**: 20 / 39
- **Total session steps**: 198
- **Feature introduction density**: 20 features in 198 steps ≈ 0.10 features/step

## Feature appearance order (earliest first)

| # | Step | Feature | Group | File | Kind |
|---:|---:|---|---|---|---|
| 1 | 148 | Castling | Rules & protocol | `…/MEMORY.md` | Edit |
| 2 | 148 | Check/Checkmate | Rules & protocol | `…/MEMORY.md` | Edit |
| 3 | 148 | PGN | Rules & protocol | `…/MEMORY.md` | Edit |
| 4 | 148 | Promotion | Rules & protocol | `…/MEMORY.md` | Edit |
| 5 | 148 | UCI protocol | Rules & protocol | `…/MEMORY.md` | Edit |
| 6 | 157 | FEN parsing | Rules & protocol | `…/play_random.py` | Write |
| 7 | 164 | Minimax/Negamax | Search core | `…/bf_movegen.py` | Edit |
| 8 | 167 | Alpha-beta | Search core | `…/README.md` | Write |
| 9 | 167 | En passant | Rules & protocol | `…/README.md` | Write |
| 10 | 167 | Endgame tables | Strong-engine features | `…/README.md` | Write |
| 11 | 167 | Iterative deepening | Search core | `…/README.md` | Write |
| 12 | 167 | King safety | Evaluation | `…/README.md` | Write |
| 13 | 167 | Material counting | Evaluation | `…/README.md` | Write |
| 14 | 167 | Move ordering (MVV-LVA) | Search extensions | `…/README.md` | Write |
| 15 | 167 | Opening book | Strong-engine features | `…/README.md` | Write |
| 16 | 167 | Pawn structure | Evaluation | `…/README.md` | Write |
| 17 | 167 | Perft | Search core | `…/README.md` | Write |
| 18 | 167 | Time management | Strong-engine features | `…/README.md` | Write |
| 19 | 180 | Quiescence | Search core | `…/2026-03-23-BFChessChessEngineBrainfuck.md` | Write |
| 20 | 198 | Tapered evaluation | Evaluation | `…/make_bishop_art.py` | Write |

## Per-group introduction timeline

### Rules & protocol

| Feature | Step | File |
|---|---:|---|
| UCI protocol | 148 | `…/MEMORY.md` |
| PGN | 148 | `…/MEMORY.md` |
| Castling | 148 | `…/MEMORY.md` |
| Promotion | 148 | `…/MEMORY.md` |
| Check/Checkmate | 148 | `…/MEMORY.md` |
| FEN parsing | 157 | `…/play_random.py` |
| En passant | 167 | `…/README.md` |

### Search core

| Feature | Step | File |
|---|---:|---|
| Minimax/Negamax | 164 | `…/bf_movegen.py` |
| Alpha-beta | 167 | `…/README.md` |
| Iterative deepening | 167 | `…/README.md` |
| Perft | 167 | `…/README.md` |
| Quiescence | 180 | `…/2026-03-23-BFChessChessEngineBrainfuck.md` |

### Search extensions

| Feature | Step | File |
|---|---:|---|
| Move ordering (MVV-LVA) | 167 | `…/README.md` |

### Evaluation

| Feature | Step | File |
|---|---:|---|
| Material counting | 167 | `…/README.md` |
| King safety | 167 | `…/README.md` |
| Pawn structure | 167 | `…/README.md` |
| Tapered evaluation | 198 | `…/make_bishop_art.py` |

### Strong-engine features

| Feature | Step | File |
|---|---:|---|
| Opening book | 167 | `…/README.md` |
| Endgame tables | 167 | `…/README.md` |
| Time management | 167 | `…/README.md` |

## Cumulative feature count per step

Each row: after step $k$, the agent had touched a cumulative total of $n(k)$ distinct features in newly-written content.

```
step   1:  0  
step   2:  0  
step   3:  0  
step   4:  0  
step   5:  0  
step   6:  0  
step   7:  0  
step   8:  0  
step   9:  0  
step  10:  0  
step  11:  0  
step  12:  0  
step  13:  0  
step  14:  0  
step  15:  0  
step  16:  0  
step  17:  0  
step  18:  0  
step  19:  0  
step  20:  0  
step  21:  0  
step  22:  0  
step  23:  0  
step  24:  0  
step  25:  0  
step  26:  0  
step  27:  0  
step  28:  0  
step  29:  0  
step  30:  0  
step  31:  0  
step  32:  0  
step  33:  0  
step  34:  0  
step  35:  0  
step  36:  0  
step  37:  0  
step  38:  0  
step  39:  0  
step  40:  0  
step  41:  0  
step  42:  0  
step  43:  0  
step  44:  0  
step  45:  0  
step  46:  0  
step  47:  0  
step  48:  0  
step  49:  0  
step  50:  0  
step  51:  0  
step  52:  0  
step  53:  0  
step  54:  0  
step  55:  0  
step  56:  0  
step  57:  0  
step  58:  0  
step  59:  0  
step  60:  0  
step  61:  0  
step  62:  0  
step  63:  0  
step  64:  0  
step  65:  0  
step  66:  0  
step  67:  0  
step  68:  0  
step  69:  0  
step  70:  0  
step  71:  0  
step  72:  0  
step  73:  0  
step  74:  0  
step  75:  0  
step  76:  0  
step  77:  0  
step  78:  0  
step  79:  0  
step  80:  0  
step  81:  0  
step  82:  0  
step  83:  0  
step  84:  0  
step  85:  0  
step  86:  0  
step  87:  0  
step  88:  0  
step  89:  0  
step  90:  0  
step  91:  0  
step  92:  0  
step  93:  0  
step  94:  0  
step  95:  0  
step  96:  0  
step  97:  0  
step  98:  0  
step  99:  0  
step 100:  0  
step 101:  0  
step 102:  0  
step 103:  0  
step 104:  0  
step 105:  0  
step 106:  0  
step 107:  0  
step 108:  0  
step 109:  0  
step 110:  0  
step 111:  0  
step 112:  0  
step 113:  0  
step 114:  0  
step 115:  0  
step 116:  0  
step 117:  0  
step 118:  0  
step 119:  0  
step 120:  0  
step 121:  0  
step 122:  0  
step 123:  0  
step 124:  0  
step 125:  0  
step 126:  0  
step 127:  0  
step 128:  0  
step 129:  0  
step 130:  0  
step 131:  0  
step 132:  0  
step 133:  0  
step 134:  0  
step 135:  0  
step 136:  0  
step 137:  0  
step 138:  0  
step 139:  0  
step 140:  0  
step 141:  0  
step 142:  0  
step 143:  0  
step 144:  0  
step 145:  0  
step 146:  0  
step 147:  0  
step 148:  5  █████
step 149:  5  █████
step 150:  5  █████
step 151:  5  █████
step 152:  5  █████
step 153:  5  █████
step 154:  5  █████
step 155:  5  █████
step 156:  5  █████
step 157:  6  ██████
step 158:  6  ██████
step 159:  6  ██████
step 160:  6  ██████
step 161:  6  ██████
step 162:  6  ██████
step 163:  6  ██████
step 164:  7  ███████
step 165:  7  ███████
step 166:  7  ███████
step 167: 18  ██████████████████
step 168: 18  ██████████████████
step 169: 18  ██████████████████
step 170: 18  ██████████████████
step 171: 18  ██████████████████
step 172: 18  ██████████████████
step 173: 18  ██████████████████
step 174: 18  ██████████████████
step 175: 18  ██████████████████
step 176: 18  ██████████████████
step 177: 18  ██████████████████
step 178: 18  ██████████████████
step 179: 18  ██████████████████
step 180: 19  ███████████████████
step 181: 19  ███████████████████
step 182: 19  ███████████████████
step 183: 19  ███████████████████
step 184: 19  ███████████████████
step 185: 19  ███████████████████
step 186: 19  ███████████████████
step 187: 19  ███████████████████
step 188: 19  ███████████████████
step 189: 19  ███████████████████
step 190: 19  ███████████████████
step 191: 19  ███████████████████
step 192: 19  ███████████████████
step 193: 19  ███████████████████
step 194: 19  ███████████████████
step 195: 19  ███████████████████
step 196: 19  ███████████████████
step 197: 19  ███████████████████
step 198: 20  ████████████████████
```
