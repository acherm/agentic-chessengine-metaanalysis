# chess-kasparov-claim-bis

_Evidence-based dossier. Generated 2026-04-22 14:53 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-kasparov-claim-bis` [R:chess-kasparov-claim-bis]
- **Primary language:** Python
- **Coding agent(s):** Claude Code subagents
- **Period:** —
- **LOC by language:** Python (1957 LOC, 11 files), Markdown (570 LOC, 1 files), Text (509 LOC, 23 files), LaTeX (369 LOC, 41 files)
- **Totals:** 76 files, 3405 LOC [S:scan]
- **Git:** not a git repo

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 4 subagent transcripts [T:chess-kasparov-claim-bis/claude]
- Claude models seen: —
- Codex sessions: 0 [T:chess-kasparov-claim-bis/codex]
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
| Transposition table | 187 | `media/videos/scene1_kasparov_tweet/480p15/Scene1KasparovTweet.mp4` |
| Evaluation/PST | 4 | `media/videos/scene9_reframe/720p30/Scene9Reframe.mp4` |
| FEN parsing | 3 | `scene9_reframe.py` |
| Castling | 3 | `media/videos/scene1_kasparov_tweet/480p15/Scene1KasparovTweet.mp4` |
| Endgame tables | 3 | `scenes.md` |
| Promotion | 2 | `scene9_reframe.py` |
| Late-move pruning (LMP) | 2 | `media/videos/scene6_checkers/480p15/Scene6Checkers.mp4` |
| Check/Checkmate | 1 | `scene7_andor_tree.py` |
| Material counting | 1 | `scenes.md` |

## Interaction profile

- Total user prompts (both agents): **4**
- Avg prompt length: 1013.5 chars
- Intent distribution:
  - Scenario: 3
  - Documentation: 2
  - Constraint: 2

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Claude Code (subagent) — 2026-02-15 10:51 — session `agent-a2`_

```
Explore the project at /Users/mathieuacher/SANDBOX/chess-kasparov-claim-bis thoroughly. I need to understand:
1. What files exist (all of them)
2. What the project is about
3. Any existing code, data, scripts, or documentation
4. The topic/claim related to Kasparov and chess

Read all relevant files to get the full picture. Give me a comprehensive summary.
```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-15 10:57 | Claude Code (subagent) | Scenario | Research "Kasparov claim" in the context of chess. I need to understand the most famous claims or controversies involving Garry Kasparov. K… |
| 3 | 2026-02-15 11:01 | Claude Code (subagent) | Constraint,Scenario | Research the following: 1. Kasparov's tweet about "584 moves with just 8 of 32 pieces" - this is about a chess endgame tablebase position t… |
| 4 | 2026-02-15 11:01 | Claude Code (subagent) | Documentation,Constraint | Research and explain the formal definitions and implications of: 1. **Weak solving** a game: Formally, a game is weakly solved if from the … |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **4** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (Documentation) [2026-02-15 10:51] — Explore the project at /Users/mathieuacher/SANDBOX/chess-kasparov-claim-bis thoroughly. I need to understand: 1. What files exist (all of them) 2. What the project is about 3. Any… [T:Claude Code (subagent)/agent-a2]
- **BL-002** (Scenario) [2026-02-15 10:57] — Research "Kasparov claim" in the context of chess. I need to understand the most famous claims or controversies involving Garry Kasparov. Key topics to look for: 1. Kasparov vs De… [T:Claude Code (subagent)/agent-ae]
- **BL-003** (Constraint, Scenario) [2026-02-15 11:01] — Research the following: 1. Kasparov's tweet about "584 moves with just 8 of 32 pieces" - this is about a chess endgame tablebase position that requires 584 moves to win. Find deta… [T:Claude Code (subagent)/agent-af]
- **BL-004** (Documentation, Constraint, Scenario) [2026-02-15 11:01] — Research and explain the formal definitions and implications of: 1. **Weak solving** a game: Formally, a game is weakly solved if from the initial position, the game-theoretic val… [T:Claude Code (subagent)/agent-a9]

## Evidence pointers

- [R:chess-kasparov-claim-bis] — repo at `/Users/mathieuacher/SANDBOX/chess-kasparov-claim-bis`
- [T:chess-kasparov-claim-bis/claude] — Claude sessions at `~/.claude/projects/chess-kasparov-claim-bis...`
- [T:chess-kasparov-claim-bis/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-kasparov-claim-bis

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.