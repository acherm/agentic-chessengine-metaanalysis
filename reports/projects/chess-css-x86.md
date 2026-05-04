# chess-css-x86

_Evidence-based dossier. Generated 2026-04-22 14:52 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-css-x86` [R:chess-css-x86]
- **Primary language:** HTML
- **Coding agent(s):** Codex
- **Period:** 2026-03-01 22:48 → 2026-03-02 19:59
- **LOC by language:** HTML (53875 LOC, 3 files), JSON (4146 LOC, 1 files), Assembly (1045 LOC, 1 files), Python (687 LOC, 4 files), Text (306 LOC, 1 files), C (242 LOC, 2 files), Markdown (169 LOC, 1 files)
- **Totals:** 13 files, 60470 LOC [S:scan]
- **Git:** 8 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:chess-css-x86/claude]
- Claude models seen: —
- Codex sessions: 1 [T:chess-css-x86/codex]
- Codex models seen: gpt-5.3-codex

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 1 | 13 | 11135032 | 86833 | 10353280 | — | $16.08 |
| **Total** |  |  |  |  |  |  | **$16.08** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| Transposition table | 2 | `static/Lekton-bold.woff2` |
| Material counting | 1 | `LICENSE` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | exec_command | 111 |

## Interaction profile

- Total user prompts (both agents): **13**
- Avg prompt length: 2301.1 chars
- Intent distribution:
  - Other: 10
  - TestRequest: 1
  - ToolingBuild: 1
  - Question: 1
  - Scenario: 1
  - BugFixRequest: 1

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-03-01 22:48 — session `rollout-`_

```
Considering https://lyra.horse/x86css/ 
x86CSS demonstrates a working x86(8086) CPU/emulator implemented in CSS, explicitly stating “No JavaScript required” (with an optional JS clock for stability), and relying on newer CSS features such as if() and style queries/custom functions. This establishes that general-purpose computation can be forced into CSS under specific assumptions (modern Chromium features, enormous generated stylesheets, careful encoding)

Explore an x86CSS-based chess proof-of-concept: compile a tiny engine (even random-move legal generator) to 8086 and render moves via x86CSS’s output mechanism, to test whether “chess in CSS” is practically demonstrable under the emulator approach

```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-03-01 23:00 | Codex | Question,Scenario | how to show we can play? |
| 3 | 2026-03-01 23:02 | Codex | Other | yes go |
| 4 | 2026-03-01 23:09 | Codex | Other | I'm waiting for "Your move>." but nothing... |
| 5 | 2026-03-02 08:07 | Codex | Other | program exited, code 1337 |
| 6 | 2026-03-02 13:02 | Codex | Other | the interface is appaearing... with a kind of keyboard. But clicking on buttons/letters seems not doing anything |
| 7 | 2026-03-02 15:47 | Codex | Other | after 2 seconds, nothing happens... |
| 8 | 2026-03-02 15:50 | Codex | Other | Forced reflow while executing JavaScript took 189ms [Violation] Forced reflow while executing JavaScript took 177ms [Violation] Forced refl… |
| 9 | 2026-03-02 15:52 | Codex | Other | [Violation] Forced reflow while executing JavaScript took <N>ms x86css.html:28284 [Violation] 'requestAnimationFrame' handler took 50ms x86… |
| 10 | 2026-03-02 15:55 | Codex | Other | [Violation] 'requestAnimationFrame' handler took <N>ms [Violation] 'requestAnimationFrame' handler took <N>ms [Violation] 'requestAnimation… |
| 11 | 2026-03-02 16:08 | Codex | Other | [Violation] 'setTimeout' handler took <N>ms [Violation] 'setTimeout' handler took <N>ms [Violation] 'setTimeout' handler took <N>ms [Violat… |
| 12 | 2026-03-02 19:40 | Codex | Other | [Violation] 'setTimeout' handler took <N>ms [Violation] 'setTimeout' handler took <N>ms [Violation] 'setTimeout' handler took <N>ms [Violat… |
| 13 | 2026-03-02 19:53 | Codex | BugFixRequest | no error this time :) but nothing happens after a few minutes (instructions seem executed but very low certainly) |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `2c7ab3c` | 2026-02-26T02:24:10+02:00 | Lyra Rebane | License under GPLv3 |
| `fa82b48` | 2026-02-24T18:09:22+02:00 | Lyra Rebane | More stuff in FAQ |
| `b2d7428` | 2026-02-24T17:47:11+02:00 | Lyra Rebane | rename to match docs |
| `f0095b8` | 2026-02-24T04:35:19+02:00 | Lyra Rebane | add link to c program |
| `4b0bd97` | 2026-02-24T04:25:28+02:00 | Lyra Rebane | add socials |
| `5961c2a` | 2026-02-24T04:14:26+02:00 | Lyra Rebane | here we go :3c |
| `e37dc51` | 2026-02-24T04:00:22+02:00 | Lyra Rebane | Update README |
| `3eaf61c` | 2026-02-24T03:45:58+02:00 | Lyra Rebane | Initial commit |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **2** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (TestRequest, ToolingBuild) [2026-03-01 22:48] — Considering https://lyra.horse/x86css/ x86CSS demonstrates a working x86(8086) CPU/emulator implemented in CSS, explicitly stating “No JavaScript required” (with an optional JS cl… [T:Codex/rollout-]
- **BL-002** (BugFixRequest) [2026-03-02 19:53] — no error this time :) but nothing happens after a few minutes (instructions seem executed but very low certainly) [T:Codex/rollout-]

## Evidence pointers

- [R:chess-css-x86] — repo at `/Users/mathieuacher/SANDBOX/chess-css-x86`
- [T:chess-css-x86/claude] — Claude sessions at `~/.claude/projects/chess-css-x86...`
- [T:chess-css-x86/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-css-x86

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.