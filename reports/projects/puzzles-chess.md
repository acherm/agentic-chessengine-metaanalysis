# puzzles-chess

_Evidence-based dossier. Generated 2026-04-22 14:56 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/puzzles-chess` [R:puzzles-chess]
- **Primary language:** Python
- **Coding agent(s):** —
- **Period:** —
- **LOC by language:** Python (714 LOC, 3 files)
- **Totals:** 3 files, 714 LOC [S:scan]
- **Git:** not a git repo

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:puzzles-chess/claude]
- Claude models seen: —
- Codex sessions: 0 [T:puzzles-chess/codex]
- Codex models seen: —

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 0 | 0 | 0 | 0 | 0 | — | $0.00 |
| **Total** |  |  |  |  |  |  | **$0.00** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| FEN parsing | 2 | `stockfish_depth_sensitivity.py` |
| Castling | 1 | `stockfish_depth_sensitivity.py` |
| Endgame tables | 1 | `stockfish_depth_sensitivity.py` |

## Interaction profile

- Total user prompts (both agents): **0**
- Avg prompt length: 0 chars

## User-driven feature backlog (best-effort, derived from prompts)

_No user prompts recovered; backlog cannot be reconstructed from sessions._

## Evidence pointers

- [R:puzzles-chess] — repo at `/Users/mathieuacher/SANDBOX/puzzles-chess`
- [T:puzzles-chess/claude] — Claude sessions at `~/.claude/projects/puzzles-chess...`
- [T:puzzles-chess/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/puzzles-chess

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.