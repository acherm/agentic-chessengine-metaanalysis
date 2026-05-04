# chess-fem

_Evidence-based dossier. Generated 2026-04-22 14:52 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-fem` [R:chess-fem]
- **Primary language:** Python
- **Coding agent(s):** —
- **Period:** —
- **LOC by language:** JSON (226920 LOC, 18 files), Python (3489 LOC, 7 files), Markdown (1492 LOC, 10 files), R (1080 LOC, 1 files), CSS (901 LOC, 2 files), JavaScript (900 LOC, 1 files), HTML (296 LOC, 1 files), YAML (233 LOC, 2 files)
- **Totals:** 44 files, 235408 LOC [S:scan]
- **Git:** 7 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:chess-fem/claude]
- Claude models seen: —
- Codex sessions: 0 [T:chess-fem/codex]
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
| Principal-variation (PV) | 3 | `generate_explorable_data.py` |
| Time management | 1 | `STUDY_DESIGN.md` |

## Interaction profile

- Total user prompts (both agents): **0**
- Avg prompt length: 0 chars

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `6e37384` | 2026-01-23T12:16:39+01:00 | Mathieu Acher | Fix R constraint deduplication to match Python exactly |
| `88441a1` | 2026-01-23T11:15:39+01:00 | Mathieu Acher | Match R multiverse specification to Python/YAML spec |
| `250458f` | 2026-01-23T10:57:36+01:00 | Mathieu Acher | Fix R multiverse analysis to work with base R only |
| `42ca998` | 2026-01-23T10:05:57+01:00 | Mathieu Acher | Add R multiverse analysis as alternative implementation |
| `160ac84` | 2026-01-23T09:35:26+01:00 | Mathieu Acher | Add stratified statistics, specification curves, and model defensibility guide |
| `321f44d` | 2026-01-22T09:12:06+01:00 | Mathieu Acher | Add multiple inference models for multiverse analysis |
| `fa9e1b5` | 2026-01-22T09:00:37+01:00 | Mathieu Acher | Initial commit: Multiverse analysis of gender representation in chess |

## User-driven feature backlog (best-effort, derived from prompts)

_No user prompts recovered; backlog cannot be reconstructed from sessions._

## Evidence pointers

- [R:chess-fem] — repo at `/Users/mathieuacher/SANDBOX/chess-fem`
- [T:chess-fem/claude] — Claude sessions at `~/.claude/projects/chess-fem...`
- [T:chess-fem/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-fem

## Limitations

- 1 Claude Code session transcripts referenced by `sessions-index.json` but missing on disk (likely archived).
- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.