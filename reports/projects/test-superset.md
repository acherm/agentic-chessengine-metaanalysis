# test-superset

_Evidence-based dossier. Generated 2026-04-22 14:56 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/test-superset` [R:test-superset]
- **Primary language:** HTML
- **Coding agent(s):** Claude Code subagents
- **Period:** —
- **LOC by language:** HTML (113887 LOC, 2 files), CSS (104590 LOC, 18 files), JavaScript (3711 LOC, 22 files), JSON (2181 LOC, 2 files), Markdown (284 LOC, 1 files), Shell (119 LOC, 1 files)
- **Totals:** 46 files, 224772 LOC [S:scan]
- **Git:** 1 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 52 subagent transcripts [T:test-superset/claude]
- Claude models seen: —
- Codex sessions: 0 [T:test-superset/codex]
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
| FEN parsing | 17 | `play.html` |
| Castling | 15 | `play.html` |
| Promotion | 13 | `play.html` |
| Check/Checkmate | 13 | `play.html` |
| UCI protocol | 11 | `README.md` |
| En passant | 7 | `play.html` |
| Move ordering (MVV-LVA) | 5 | `README.md` |
| Material counting | 5 | `README.md` |
| Time management | 5 | `scripts/tournament.js` |
| PGN | 4 | `scripts/elo-test.sh` |
| King safety | 3 | `scss/legality/_king-safety-non-sliding.scss` |
| Opening book | 2 | `README.md` |
| Board: mailbox 8x8 | 1 | `src/board-renderer.js` |
| Evaluation/PST | 1 | `scripts/generate-css.js` |

## Interaction profile

- Total user prompts (both agents): **53**
- Avg prompt length: 1913.5 chars
- Intent distribution:
  - TestRequest: 29
  - Scenario: 28
  - FeatureRequest: 23
  - Constraint: 18
  - Documentation: 11
  - BugFixRequest: 8
  - Other: 6
  - ToolingBuild: 5
  - RefactorRequest: 2

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Claude Code (subagent) — 2026-02-27 19:37 — session `agent-a1`_

```
Design a complete architecture for a CSS chess engine — a chess engine where the chess evaluation intelligence is written in pure CSS, with a thin Node.js driver for mechanical parts (move generation, search, UCI protocol).

## Context
The user wants to build a chess engine with maximum CSS usage. The evaluation function (material counting, piece-square tables, move scoring) must be 100% pure CSS. A minimal driver in JavaScript handles:
- Legal move generation (using chess.js library)
- Alpha-beta search tree traversal
- UCI protocol for testing Elo with cutechess-cli
- Rendering positions as HTML for CSS evaluation

## Key Technical Challenges

1. **CSS Counter Aggregation**: CSS counters can accumulate values across sibling elements via `counter-increment`. This is how we sum material + piece-square table values across all 64 squares. The counter is read via `::after { content: counter(eval); }` pseudo-element.

2. **Move Scoring**: Each candidate move is an HTML element with data attributes. CSS custom properties assign scores based on capture value, destination quality, etc. The driver reads computed `--score` from each move element.

3. **CSS Execution Speed**: Using Puppeteer (headless Chrome) to actually execute CSS. This limits search depth to 1-2 ply (~30-900 evaluations per move). At ~5-10ms per DOM update + style recalc, depth 2 takes ~5-10 seconds.

4. **Reading CSS Counter Values**: CSS counters can only be displayed via `content` property. The driver reads the t
```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-02-28 09:54 | Claude Code (subagent) | TestRequest,Scenario | Explore the css-chess-engine project to understand: 1. How the engine driver works (src/driver.js, src/uci.js) — how does a game session fl… |
| 3 | 2026-02-28 13:20 | Claude Code (subagent) | TestRequest | Explore the css-chess-engine directory thoroughly. I need to understand: 1. The project structure (all files and directories) 2. How CssEva… |
| 4 | 2026-02-28 14:32 | Claude Code (subagent) | TestRequest,Documentation | Very thoroughly explore the css-chess-engine directory at /Users/mathieuacher/.superset/worktrees/test-superset/mathieu-acher/test-superset… |
| 5 | 2026-02-28 14:32 | Claude Code (subagent) | FeatureRequest,Documentation | Research what modern CSS features could be used to implement chess logic. DO NOT write any code or edit any files - just research and repor… |
| 6 | 2026-02-28 14:47 | Claude Code (subagent) | FeatureRequest,TestRequest | I need to design an implementation plan for moving chess logic from JavaScript into pure CSS, as far as possible. This is for the CSS chess… |
| 7 | 2026-02-28 15:10 | Claude Code (subagent) | TestRequest | Thoroughly explore the css-chess-engine directory to understand the full codebase structure. I need: 1. All files and their purposes (list … |
| 8 | 2026-02-28 16:41 | Claude Code (subagent) | Constraint,Scenario | Analyze the current CSS chess engine codebase to identify everything that's still done in JavaScript that could potentially be moved to CSS… |
| 9 | 2026-02-28 16:43 | Claude Code (subagent) | FeatureRequest,TestRequest | I'm designing a plan to push more chess logic from JavaScript into CSS for a CSS chess engine. Based on analysis, here's the current state … |
| 10 | 2026-02-28 17:28 | Claude Code (subagent) | TestRequest,Scenario | Explore the css-chess-engine codebase thoroughly. I need to understand: 1. The full directory structure (ls -la at root and key subdirs) 2.… |
| 11 | 2026-02-28 19:42 | Claude Code (subagent) | FeatureRequest,Scenario | Read all source files in css-chess-engine/src/ and identify what chess intelligence or logic remains in JavaScript vs what is handled by CS… |
| 12 | 2026-02-28 20:22 | Claude Code (subagent) | Constraint,Scenario | I need to understand how to generate CSS rules that directly compute move legality (not just pseudo-legality). Currently, legality is check… |
| 13 | 2026-02-28 20:32 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 14 | 2026-02-28 20:34 | Claude Code (subagent) | FeatureRequest | I need to understand how the existing CSS check detection and move generation work, so I can plan a CSS legality detection system. Please e… |
| 15 | 2026-02-28 22:18 | Claude Code (subagent) | Other | Your response was cut off because it exceeded the output token limit. Please break your work into smaller pieces. Continue from where you l… |
| 16 | 2026-02-28 23:20 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 17 | 2026-03-01 06:20 | Claude Code (subagent) | TestRequest | Explore the CSS chess engine legality CSS generator and move scoring CSS. I need to understand: 1. Read `/Users/mathieuacher/.superset/work… |
| 18 | 2026-03-01 06:20 | Claude Code (subagent) | TestRequest | Explore the CSS chess engine search and driver code. Read these files fully: 1. `/Users/mathieuacher/.superset/worktrees/test-superset/math… |
| 19 | 2026-03-01 07:18 | Claude Code (subagent) | Other | I need to understand the structure of `css-chess-engine/scripts/generate-legality-css.js` in detail. This script generates ~16,160 CSS rule… |
| 20 | 2026-03-01 07:20 | Claude Code (subagent) | FeatureRequest,TestRequest | I need to convert a JavaScript CSS generator for chess move legality into pure Sass/SCSS files. The JS script (`scripts/generate-legality-c… |
| 21 | 2026-03-01 08:10 | Claude Code (subagent) | FeatureRequest,TestRequest | Explore the css-chess-engine codebase thoroughly. I need to understand: 1. How the engine works end-to-end (how CSS encodes chess knowledge… |
| 22 | 2026-03-01 08:18 | Claude Code (subagent) | FeatureRequest,ToolingBuild | I need to understand how to build a web-based UI for the CSS chess engine. Explore these files thoroughly: 1. `src/css-evaluator.js` - How … |
| 23 | 2026-03-01 09:30 | Claude Code (subagent) | Scenario | Explore the css-chess-engine directory thoroughly. I need to understand: 1. The full content of src/game-state.js 2. The full content of sr… |
| 24 | 2026-03-01 15:25 | Claude Code (subagent) | Other | Explore the CSS chess engine's move scoring system. I need to understand: 1. How `css-chess-engine/css/dynamic-move-scoring.css` works - wh… |
| 25 | 2026-03-01 16:00 | Claude Code (subagent) | Scenario | Explore the CSS chess engine's tournament infrastructure. I need to understand: 1. How `css-chess-engine/src/tournament.js` works - what do… |
| 26 | 2026-03-01 16:34 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 27 | 2026-03-01 18:48 | Claude Code (subagent) | FeatureRequest,Scenario | I need to understand how depth search currently works in the CSS chess engine's Node.js player, and how the browser-based play.html current… |
| 28 | 2026-03-01 18:49 | Claude Code (subagent) | TestRequest,Scenario | Read the following sections from `/Users/mathieuacher/.superset/worktrees/test-superset/mathieu-acher/test-superset/css-chess-engine/play.h… |
| 29 | 2026-03-01 19:52 | Claude Code (subagent) | FeatureRequest,TestRequest | I need to understand the current CSS move scoring system and move generation in this CSS chess engine to plan enrichments that approximate … |
| 30 | 2026-03-01 21:54 | Claude Code (subagent) | RefactorRequest,ToolingBuild | Explore the CSS chess engine codebase to understand what CSS features are currently used and where newer CSS features like `if()`, style qu… |
| 31 | 2026-03-01 22:23 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 32 | 2026-03-01 22:39 | Claude Code (subagent) | Other | Very thorough exploration of the CSS chess engine architecture. I need to understand: 1. How the DOM represents the board state and legal m… |
| 33 | 2026-03-01 22:39 | Claude Code (subagent) | FeatureRequest | Research CSS @function and if() capabilities for building complex computations. Specifically: 1. Read the current `scripts/generate-movesco… |
| 34 | 2026-03-01 22:40 | Claude Code (subagent) | Other | Read `css-chess-engine/src/search.js` thoroughly to understand how the current JavaScript depth-2 search works. I need to understand: 1. Th… |
| 35 | 2026-03-01 22:49 | Claude Code (subagent) | FeatureRequest,TestRequest | Design an implementation plan for adding depth-2-like tactical awareness to a CSS chess engine, entirely encoded in CSS rules. ## Current A… |
| 36 | 2026-03-02 08:11 | Claude Code (subagent) | Other | Find how the CSS chess engine selects the best move. Look for: 1. The JS code that sorts moves by score and picks the best one (the `moves.… |
| 37 | 2026-03-02 08:18 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 38 | 2026-03-02 11:49 | Claude Code (subagent) | TestRequest,Documentation | Read the file /Users/mathieuacher/.superset/worktrees/test-superset/mathieu-acher/test-superset/css-chess-engine/play.html in its entirety.… |
| 39 | 2026-03-02 12:36 | Claude Code (subagent) | TestRequest,Scenario | Search the css-chess-engine directory at /Users/mathieuacher/.superset/worktrees/test-superset/mathieu-acher/test-superset/css-chess-engine… |
| 40 | 2026-03-02 16:50 | Claude Code (subagent) | Scenario | Explore the CSS chess engine's move scoring system thoroughly. I need to understand: 1. How moves get their scores — look at `css-chess-eng… |
| 41 | 2026-03-02 22:00 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |
| 42 | 2026-03-03 00:14 | Claude Code (subagent) | FeatureRequest | I need to understand how the CSS move scoring system works in this chess engine to add "destination safety" analysis (is the destination sq… |
| 43 | 2026-03-03 00:17 | Claude Code (subagent) | FeatureRequest,BugFixRequest | I need to design an implementation plan for adding "CSS depth-2 tactical awareness" to a CSS chess engine. The key principle: ALL chess int… |
| 44 | 2026-03-03 00:34 | Claude Code (subagent) | TestRequest,Scenario | Find how tournaments are run in this chess engine project. Look at scripts/tournament.js for the available options, opponent types, and how… |
| 45 | 2026-03-03 08:14 | Claude Code (subagent) | TestRequest,Scenario | I need a comprehensive understanding of the CSS chess engine project at /Users/mathieuacher/.superset/worktrees/test-superset/mathieu-acher… |
| 46 | 2026-03-03 08:40 | Claude Code (subagent) | RefactorRequest,TestRequest | I need to find ALL occurrences of data-* HTML attributes used in this chess engine project to plan a rename for size reduction. The project… |
| 47 | 2026-03-03 09:12 | Claude Code (subagent) | Scenario | Find how tournaments are configured and run in this project. Look at: 1. scripts/tournament.js - how it works, what arguments it takes 2. s… |
| 48 | 2026-03-03 12:29 | Claude Code (subagent) | Scenario | I need to understand the current I/O model of this CSS chess engine - specifically how board state is represented in HTML, how CSS reads it… |
| 49 | 2026-03-03 12:44 | Claude Code (subagent) | Scenario | I need to deeply understand the play.html file's board interaction model to plan a radio-button-based pure CSS move selection prototype. Fo… |
| 50 | 2026-03-03 12:44 | Claude Code (subagent) | Scenario | I need to understand how the CSS rules work in this chess engine — specifically the selector patterns — to plan a radio-button-based approa… |
| 51 | 2026-03-03 12:48 | Claude Code (subagent) | FeatureRequest,Documentation | Design an implementation plan for adding CSS-only legal move highlighting to a CSS chess engine using radio buttons. ## Current Architectur… |
| 52 | 2026-03-03 16:14 | Claude Code (subagent) | TestRequest,Scenario | I need a comprehensive analysis of ALL JavaScript code in /Users/mathieuacher/.superset/worktrees/test-superset/mathieu-acher/test-superset… |
| 53 | 2026-03-03 22:19 | Claude Code (subagent) | FeatureRequest,BugFixRequest | Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previ… |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `41a9ec5` | 2026-02-27T19:15:34+01:00 | Mathieu Acher | Initial commit |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **39** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest, TestRequest, ToolingBuild, Constraint) [2026-02-27 19:37] — Design a complete architecture for a CSS chess engine — a chess engine where the chess evaluation intelligence is written in pure CSS, with a thin Node.js driver for mechanical pa… [T:Claude Code (subagent)/agent-a1]
- **BL-002** (TestRequest, Scenario) [2026-02-28 09:54] — Explore the css-chess-engine project to understand: 1. How the engine driver works (src/driver.js, src/uci.js) — how does a game session flow? 2. How the random engine works in sc… [T:Claude Code (subagent)/agent-a5]
- **BL-003** (TestRequest) [2026-02-28 13:20] — Explore the css-chess-engine directory thoroughly. I need to understand: 1. The project structure (all files and directories) 2. How CssEvaluator and Search classes work (construc… [T:Claude Code (subagent)/agent-a0]
- **BL-004** (TestRequest, Documentation) [2026-02-28 14:32] — Very thoroughly explore the css-chess-engine directory at /Users/mathieuacher/.superset/worktrees/test-superset/mathieu-acher/test-superset/css-chess-engine/ I need to understand … [T:Claude Code (subagent)/agent-ac]
- **BL-005** (FeatureRequest, Documentation, Constraint) [2026-02-28 14:32] — Research what modern CSS features could be used to implement chess logic. DO NOT write any code or edit any files - just research and report back. I'm working on a chess engine th… [T:Claude Code (subagent)/agent-a0]
- **BL-006** (FeatureRequest, TestRequest, Constraint, Scenario) [2026-02-28 14:47] — I need to design an implementation plan for moving chess logic from JavaScript into pure CSS, as far as possible. This is for the CSS chess engine at /Users/mathieuacher/.superset… [T:Claude Code (subagent)/agent-a5]
- **BL-007** (TestRequest) [2026-02-28 15:10] — Thoroughly explore the css-chess-engine directory to understand the full codebase structure. I need: 1. All files and their purposes (list every file) 2. The content of key files:… [T:Claude Code (subagent)/agent-a4]
- **BL-008** (Constraint, Scenario) [2026-02-28 16:41] — Analyze the current CSS chess engine codebase to identify everything that's still done in JavaScript that could potentially be moved to CSS. Read these files thoroughly: 1. `css-c… [T:Claude Code (subagent)/agent-a2]
- **BL-009** (FeatureRequest, TestRequest, Constraint, Scenario) [2026-02-28 16:43] — I'm designing a plan to push more chess logic from JavaScript into CSS for a CSS chess engine. Based on analysis, here's the current state and what I want to move. Please design a… [T:Claude Code (subagent)/agent-a5]
- **BL-010** (TestRequest, Scenario) [2026-02-28 17:28] — Explore the css-chess-engine codebase thoroughly. I need to understand: 1. The full directory structure (ls -la at root and key subdirs) 2. Contents of all source files in src/ 3.… [T:Claude Code (subagent)/agent-a9]
- **BL-011** (FeatureRequest, Scenario) [2026-02-28 19:42] — Read all source files in css-chess-engine/src/ and identify what chess intelligence or logic remains in JavaScript vs what is handled by CSS. I need a precise audit of: 1. What CS… [T:Claude Code (subagent)/agent-a8]
- **BL-012** (Constraint, Scenario) [2026-02-28 20:22] — I need to understand how to generate CSS rules that directly compute move legality (not just pseudo-legality). Currently, legality is checked by DOM mutation: apply move, read CSS… [T:Claude Code (subagent)/agent-ae]
- **BL-013** (FeatureRequest, BugFixRequest, TestRequest, Documentation, Constraint) [2026-02-28 20:32] — Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previous actions. This summary should be thor… [T:Claude Code (subagent)/agent-ac]
- **BL-014** (FeatureRequest) [2026-02-28 20:34] — I need to understand how the existing CSS check detection and move generation work, so I can plan a CSS legality detection system. Please examine: 1. `css-chess-engine/scripts/gen… [T:Claude Code (subagent)/agent-a6]
- **BL-015** (TestRequest) [2026-03-01 06:20] — Explore the CSS chess engine legality CSS generator and move scoring CSS. I need to understand: 1. Read `/Users/mathieuacher/.superset/worktrees/test-superset/mathieu-acher/test-s… [T:Claude Code (subagent)/agent-a4]
- **BL-016** (TestRequest) [2026-03-01 06:20] — Explore the CSS chess engine search and driver code. Read these files fully: 1. `/Users/mathieuacher/.superset/worktrees/test-superset/mathieu-acher/test-superset/css-chess-engine… [T:Claude Code (subagent)/agent-aa]
- **BL-017** (FeatureRequest, TestRequest, ToolingBuild, Constraint, Scenario) [2026-03-01 07:20] — I need to convert a JavaScript CSS generator for chess move legality into pure Sass/SCSS files. The JS script (`scripts/generate-legality-css.js`) generates ~16,160 CSS rules that… [T:Claude Code (subagent)/agent-a3]
- **BL-018** (FeatureRequest, ToolingBuild, Scenario) [2026-03-01 08:18] — I need to understand how to build a web-based UI for the CSS chess engine. Explore these files thoroughly: 1. `src/css-evaluator.js` - How does it set up the DOM? How does it load… [T:Claude Code (subagent)/agent-ab]
- **BL-019** (Scenario) [2026-03-01 16:00] — Explore the CSS chess engine's tournament infrastructure. I need to understand: 1. How `css-chess-engine/src/tournament.js` works - what does it do, how are games played, what for… [T:Claude Code (subagent)/agent-a4]
- **BL-020** (FeatureRequest, Scenario) [2026-03-01 18:48] — I need to understand how depth search currently works in the CSS chess engine's Node.js player, and how the browser-based play.html currently picks moves. Explore these files and … [T:Claude Code (subagent)/agent-aa]
- **BL-021** (TestRequest, Scenario) [2026-03-01 18:49] — Read the following sections from `/Users/mathieuacher/.superset/worktrees/test-superset/mathieu-acher/test-superset/css-chess-engine/play.html`: 1. The `<head>` section - what CSS… [T:Claude Code (subagent)/agent-a6]
- **BL-022** (FeatureRequest, TestRequest) [2026-03-01 19:52] — I need to understand the current CSS move scoring system and move generation in this CSS chess engine to plan enrichments that approximate depth-2 thinking purely in CSS. Explore … [T:Claude Code (subagent)/agent-a0]
- **BL-023** (RefactorRequest, ToolingBuild, Scenario) [2026-03-01 21:54] — Explore the CSS chess engine codebase to understand what CSS features are currently used and where newer CSS features like `if()`, style queries (`@container style()`), or custom … [T:Claude Code (subagent)/agent-a9]
- **BL-024** (FeatureRequest) [2026-03-01 22:39] — Research CSS @function and if() capabilities for building complex computations. Specifically: 1. Read the current `scripts/generate-movescoring-css.js` to understand how CSS rules… [T:Claude Code (subagent)/agent-a2]
- **BL-025** (FeatureRequest, TestRequest, Constraint, Scenario) [2026-03-01 22:49] — Design an implementation plan for adding depth-2-like tactical awareness to a CSS chess engine, entirely encoded in CSS rules. ## Current Architecture The CSS chess engine scores … [T:Claude Code (subagent)/agent-a0]
- **BL-026** (TestRequest, Documentation, Constraint, Scenario) [2026-03-02 11:49] — Read the file /Users/mathieuacher/.superset/worktrees/test-superset/mathieu-acher/test-superset/css-chess-engine/play.html in its entirety. I need you to identify and catalog ever… [T:Claude Code (subagent)/agent-a3]
- **BL-027** (TestRequest, Scenario) [2026-03-02 12:36] — Search the css-chess-engine directory at /Users/mathieuacher/.superset/worktrees/test-superset/mathieu-acher/test-superset/css-chess-engine for ALL usages of `data-king` across al… [T:Claude Code (subagent)/agent-a6]
- **BL-028** (Scenario) [2026-03-02 16:50] — Explore the CSS chess engine's move scoring system thoroughly. I need to understand: 1. How moves get their scores — look at `css-chess-engine/css/dynamic-move-scoring.css` and an… [T:Claude Code (subagent)/agent-ab]
- **BL-029** (FeatureRequest) [2026-03-03 00:14] — I need to understand how the CSS move scoring system works in this chess engine to add "destination safety" analysis (is the destination square attacked by opponent pieces?). Spec… [T:Claude Code (subagent)/agent-ac]
- **BL-030** (FeatureRequest, BugFixRequest, TestRequest, Constraint) [2026-03-03 00:17] — I need to design an implementation plan for adding "CSS depth-2 tactical awareness" to a CSS chess engine. The key principle: ALL chess intelligence stays in CSS, JS only orchestr… [T:Claude Code (subagent)/agent-a1]
- **BL-031** (TestRequest, Scenario) [2026-03-03 00:34] — Find how tournaments are run in this chess engine project. Look at scripts/tournament.js for the available options, opponent types, and how to invoke it. Also check package.json f… [T:Claude Code (subagent)/agent-ac]
- **BL-032** (TestRequest, Scenario) [2026-03-03 08:14] — I need a comprehensive understanding of the CSS chess engine project at /Users/mathieuacher/.superset/worktrees/test-superset/mathieu-acher/test-superset/. This is a chess engine … [T:Claude Code (subagent)/agent-a2]
- **BL-033** (RefactorRequest, TestRequest, Scenario) [2026-03-03 08:40] — I need to find ALL occurrences of data-* HTML attributes used in this chess engine project to plan a rename for size reduction. The project is at /Users/mathieuacher/.superset/wor… [T:Claude Code (subagent)/agent-a3]
- **BL-034** (Scenario) [2026-03-03 09:12] — Find how tournaments are configured and run in this project. Look at: 1. scripts/tournament.js - how it works, what arguments it takes 2. src/tournament.js - the tournament module… [T:Claude Code (subagent)/agent-ad]
- **BL-035** (Scenario) [2026-03-03 12:29] — I need to understand the current I/O model of this CSS chess engine - specifically how board state is represented in HTML, how CSS reads it, and how JS updates it. Look at: 1. `pl… [T:Claude Code (subagent)/agent-ae]
- **BL-036** (Scenario) [2026-03-03 12:44] — I need to deeply understand the play.html file's board interaction model to plan a radio-button-based pure CSS move selection prototype. Focus on: 1. The HTML structure: How is #g… [T:Claude Code (subagent)/agent-a2]
- **BL-037** (Scenario) [2026-03-03 12:44] — I need to understand how the CSS rules work in this chess engine — specifically the selector patterns — to plan a radio-button-based approach. Look at: 1. `css/move-generation.css… [T:Claude Code (subagent)/agent-a5]
- **BL-038** (FeatureRequest, Documentation, Constraint, Scenario) [2026-03-03 12:48] — Design an implementation plan for adding CSS-only legal move highlighting to a CSS chess engine using radio buttons. ## Current Architecture - `play.html` contains the full browse… [T:Claude Code (subagent)/agent-ad]
- **BL-039** (TestRequest, Scenario) [2026-03-03 16:14] — I need a comprehensive analysis of ALL JavaScript code in /Users/mathieuacher/.superset/worktrees/test-superset/mathieu-acher/test-superset/play.html. The file is very large, so r… [T:Claude Code (subagent)/agent-aa]

## Evidence pointers

- [R:test-superset] — repo at `/Users/mathieuacher/SANDBOX/test-superset`
- [T:test-superset/claude] — Claude sessions at `~/.claude/projects/test-superset...`
- [T:test-superset/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/test-superset

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.