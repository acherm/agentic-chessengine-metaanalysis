# chess-conway

_Evidence-based dossier. Generated 2026-04-22 14:52 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-conway` [R:chess-conway]
- **Primary language:** JavaScript
- **Coding agent(s):** —
- **Period:** —
- **LOC by language:** JavaScript (878 LOC, 5 files), HTML (488 LOC, 1 files)
- **Totals:** 6 files, 1366 LOC [S:scan]
- **Git:** 1 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:chess-conway/claude]
- Claude models seen: —
- Codex sessions: 0 [T:chess-conway/codex]
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
| Check/Checkmate | 5 | `ai.js` |
| Promotion | 3 | `game.js` |
| Material counting | 2 | `ai.js` |
| Castling | 1 | `index.html` |
| Minimax/Negamax | 1 | `ai.js` |
| Alpha-beta | 1 | `ai.js` |

## Interaction profile

- Total user prompts (both agents): **0**
- Avg prompt length: 0 chars

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `2c3ceb2` | 2026-03-02T21:36:13+01:00 | Mathieu Acher | Initial commit: Chess x Conway's Game of Life hybrid game |

## User-driven feature backlog (best-effort, derived from prompts)

_No user prompts recovered; backlog cannot be reconstructed from sessions._

## Evidence pointers

- [R:chess-conway] — repo at `/Users/mathieuacher/SANDBOX/chess-conway`
- [T:chess-conway/claude] — Claude sessions at `~/.claude/projects/chess-conway...`
- [T:chess-conway/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-conway

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.