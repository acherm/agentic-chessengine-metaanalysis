# Game-review folder

PGNs from the eval2 gauntlets, organized for easy review.

## Layout

```
review/
├── README.md                                 (this file)
├── curated/
│   └── strong_engines_first_game.pgn        7-game showcase, 1 per top engine vs an anchor
└── by_engine/
    ├── chess-java-cc/      *.pgn            all matches for this engine
    ├── chess-rust-cc/      *.pgn
    ├── …
```

Each `by_engine/<name>/` contains every PGN we have for that engine (Phase B + spot checks + depth diagnostic). Filenames encode the opponent, e.g. `chess-java-cc_vs_sf_skill10.pgn`.

## How to view

### Easiest: Lichess paste
1. Open https://lichess.org/paste
2. Paste a PGN's contents into the textarea
3. Click "Import game" — gives you a fully-featured analysis board with Stockfish review

Lichess accepts up to ~50 games per import, so the whole `strong_engines_first_game.pgn` works in one go.

### Native macOS chess apps
- **HIARCS Chess Explorer** (paid) — drag-and-drop PGN, very clean UI
- **Chess for Mac** (free, App Store) — basic but fine for browsing
- **SCID vs PC** (free, cross-platform) — best for batch analysis, depth annotations

### Command-line scan
```bash
# show first move + final result of every game in a PGN
awk '/^\[White|^\[Black|^\[Result|^1\./ {print}' review/by_engine/chess-rust-cc/*.pgn | head -40
```

### Depth annotations
PGNs from `pgn/depth_diag/` (and the curated file pulled from there) include per-move
`{eval/depth time}` annotations. Look for entries like `Nc3 {+0.79/15 0.18s}` — that's
"eval +0.79 cp, depth 15 ply, 0.18 s spent".

PGNs from `pgn/anchor/` (Phase B) and `pgn/spotcheck/` use cutechess `min` format and have
no annotations — Lichess analysis still works fine, you just don't see the engine's own depth.

## What's worth looking at

| Question | File |
|---|---|
| How does the strongest engine (chess-java-cc, ~1749) actually play? | `by_engine/chess-java-cc/*.pgn` |
| Why does chess-purec (claimed 2147, measured 1441) lose? | `by_engine/chess-purec/*.pgn` (look for blunders / time losses) |
| chess-rust-cc bounded < 1700: see if it lost on time or by tactics | `by_engine/chess-rust-cc/chess-rust-cc_vs_asymptote.pgn` |
| Does chess-cplusplus-claude (3 anchors converge to 1680) play coherently? | `by_engine/chess-cplusplus-claude/*.pgn` |
