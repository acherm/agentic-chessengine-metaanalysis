# chess-kasparov-claim

_Evidence-based dossier. Generated 2026-04-22 14:52 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-kasparov-claim` [R:chess-kasparov-claim]
- **Primary language:** Python
- **Coding agent(s):** Claude Code subagents
- **Period:** —
- **LOC by language:** Python (4147 LOC, 17 files), Text (854 LOC, 22 files), Markdown (463 LOC, 2 files), HTML (454 LOC, 1 files), LaTeX (108 LOC, 12 files)
- **Totals:** 54 files, 6026 LOC [S:scan]
- **Git:** 4 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 11 subagent transcripts [T:chess-kasparov-claim/claude]
- Claude models seen: —
- Codex sessions: 0 [T:chess-kasparov-claim/codex]
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
| Transposition table | 819 | `media/videos/scene9_weak_nuance/1080p60/partial_movie_files/WeakSolvingNuance/1479502529_705222047_3766752680.mp4` |
| Late-move reduction (LMR) | 35 | `media/videos/scene6/1080p60/partial_movie_files/ThreeLevelsSolved/3083400702_1725579044_3949135958.mp4` |
| Late-move pruning (LMP) | 16 | `media/videos/scene9_weak_nuance/1080p60/partial_movie_files/WeakSolvingNuance/1479502529_2574473371_4234923893.mp4` |
| Principal-variation (PV) | 13 | `media/videos/scene7/1080p60/partial_movie_files/TheVerdict/3083400702_706600323_2299566056.mp4` |
| FEN parsing | 5 | `scenes.md` |
| UCI protocol | 5 | `media/videos/scene6/1080p60/partial_movie_files/ThreeLevelsSolved/3083400702_509686548_428710219.mp4` |
| Evaluation/PST | 5 | `media/videos/scene0_title/1080p60/partial_movie_files/TitleCard/1479502529_1115864948_3384437374.mp4` |
| Castling | 4 | `media/videos/scene9_weak_nuance/1080p60/partial_movie_files/WeakSolvingNuance/1479502529_2132746009_2469312943.mp4` |
| PGN | 4 | `media/videos/scene3/1080p60/GameTree.mp4` |
| Endgame tables | 3 | `scenes.md` |
| Check/Checkmate | 2 | `scene9_weak_nuance.py` |
| Board: bitboard | 2 | `media/videos/scene9_weak_nuance/1080p60/partial_movie_files/WeakSolvingNuance/1479502529_992854052_2529438658.mp4` |
| Material counting | 1 | `scenes.md` |

## Interaction profile

- Total user prompts (both agents): **11**
- Avg prompt length: 3280.4 chars
- Intent distribution:
  - FeatureRequest: 8
  - Documentation: 8
  - Constraint: 7
  - TestRequest: 7
  - BugFixRequest: 6
  - Scenario: 2

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Claude Code (subagent) — 2026-02-15 07:23 — session `agent-a8`_

```
Research the following topics and provide a concise summary of each. Do NOT write any code - just research:

1. The 584-move endgame position in chess (Marc Bourzutschky's 8-piece tablebase). What is the exact position (FEN), what pieces are involved, why is it significant?

2. Kasparov's tweet about this position (from around 2025) - what exactly did he say?

3. The checkers solving by Jonathan Schaeffer and the Chinook team - key facts about how they weakly solved it, how many positions were in the proof, what was irrelevant.

4. Connect Four solving - who solved it, when, key facts.

5. Strategy-stealing proofs for Hex - how does the non-constructive proof work?

6. The Allis hierarchy of game solving (ultra-weak, weak, strong) - original paper/source.

Provide factual, concise information for each.
```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-15 07:43 | Claude Code (subagent) | FeatureRequest | Read the following files and give me a concise summary of each with key code patterns: 1. /Users/mathieuacher/SANDBOX/chess-kasparov-claim/… |
| 3 | 2026-02-15 09:52 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 4 | 2026-02-15 10:49 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 5 | 2026-02-15 14:01 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 6 | 2026-02-15 17:32 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 7 | 2026-02-15 19:17 | Claude Code (subagent) | TestRequest,Documentation | I'm working on a Manim video project at /Users/mathieuacher/SANDBOX/chess-kasparov-claim/. The project uses Manim Community Edition and has… |
| 8 | 2026-02-19 11:00 | Claude Code (subagent) | Scenario | I need to analyze all Manim scene files in /Users/mathieuacher/SANDBOX/chess-kasparov-claim/ to extract the precise timestamps where each d… |
| 9 | 2026-02-19 11:04 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 10 | 2026-02-20 06:58 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 11 | 2026-02-20 07:21 | Claude Code (subagent) | Documentation | Look at the project at /Users/mathieuacher/SANDBOX/chess-kasparov-claim. I need to understand: 1. What is the full content of scenes.md if … |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `0f4b63e` | 2026-02-20T08:18:55+01:00 | Mathieu Acher | Add title card, bonus scene, credits, and PDF/Reveal.js exports |
| `cd1618a` | 2026-02-15T20:48:43+01:00 | Mathieu Acher | Improve typography: Helvetica Neue default, Georgia for quotes |
| `8b23112` | 2026-02-15T20:17:12+01:00 | Mathieu Acher | Add TL;DR bonus scene, improve scene 6 and 7 |
| `7c459ed` | 2026-02-15T18:28:34+01:00 | Mathieu Acher | Add Manim video project: Is Kasparov Wrong About Solving Chess? |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **6** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, Constraint, Scenario) [2026-02-15 07:23] — Research the following topics and provide a concise summary of each. Do NOT write any code - just research: 1. The 584-move endgame position in chess (Marc Bourzutschky's 8-piece … [T:Claude Code (subagent)/agent-a8]
- **BL-002** (FeatureRequest) [2026-02-15 07:43] — Read the following files and give me a concise summary of each with key code patterns: 1. /Users/mathieuacher/SANDBOX/chess-kasparov-claim/.agents/skills/manimce-best-practices/ru… [T:Claude Code (subagent)/agent-a5]
- **BL-003** (FeatureRequest, BugFixRequest, TestRequest, Documentation, Constraint) [2026-02-15 09:52] — Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previous actions. This summary should be thor… [T:Claude Code (subagent)/agent-ac]
- **BL-004** (TestRequest, Documentation) [2026-02-15 19:17] — I'm working on a Manim video project at /Users/mathieuacher/SANDBOX/chess-kasparov-claim/. The project uses Manim Community Edition and has multiple scene files (scene1.py through… [T:Claude Code (subagent)/agent-a5]
- **BL-005** (Scenario) [2026-02-19 11:00] — I need to analyze all Manim scene files in /Users/mathieuacher/SANDBOX/chess-kasparov-claim/ to extract the precise timestamps where each distinct visual state is fully visible (a… [T:Claude Code (subagent)/agent-ac]
- **BL-006** (Documentation) [2026-02-20 07:21] — Look at the project at /Users/mathieuacher/SANDBOX/chess-kasparov-claim. I need to understand: 1. What is the full content of scenes.md if it exists? 2. What are the key arguments… [T:Claude Code (subagent)/agent-af]

## Evidence pointers

- [R:chess-kasparov-claim] — repo at `/Users/mathieuacher/SANDBOX/chess-kasparov-claim`
- [T:chess-kasparov-claim/claude] — Claude sessions at `~/.claude/projects/chess-kasparov-claim...`
- [T:chess-kasparov-claim/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-kasparov-claim

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.