# chess-printf-codex

_Evidence-based dossier. Generated 2026-04-22 14:53 UTC._

## Phase 0 — Discovery

- **Path:** `/Users/mathieuacher/SANDBOX/chess-printf-codex` [R:chess-printf-codex]
- **Primary language:** C
- **Coding agent(s):** Codex
- **Period:** 2026-03-03 18:34 → 2026-03-05 13:55
- **LOC by language:** C (52274 LOC, 52 files), Python (2945 LOC, 4 files), Markdown (403 LOC, 2 files), Shell (17 LOC, 1 files)
- **Totals:** 59 files, 55639 LOC [S:scan]
- **Git:** 11 commits

## Phase 0 — Session artifacts

- Claude Code sessions: 0 main + 0 subagent transcripts [T:chess-printf-codex/claude]
- Claude models seen: —
- Codex sessions: 5 [T:chess-printf-codex/codex]
- Codex models seen: gpt-5.3-codex

### Tokens & cost

| Agent | Sessions | Prompts | Input | Output | Cache read | Cache create | USD (est.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Code | 0 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| Codex | 5 | 118 | 132823623 | 1003008 | 126583680 | — | $191.88 |
| **Total** |  |  |  |  |  |  | **$191.88** |

_Cost is an estimate based on public per-model list prices; caches are charged at the discounted rate we observed._

## Chess-engine features detected

| Feature | Matches | Sample path |
|---|---:|---|
| Material counting | 2 | `README.md` |

## Agent tool usage (top 8)

| Agent | Tool | Count |
|---|---|---:|
| Codex | exec_command | 1256 |
| Codex | write_stdin | 26 |

## Interaction profile

- Total user prompts (both agents): **118**
- Avg prompt length: 818.2 chars
- Intent distribution:
  - Other: 59
  - FeatureRequest: 34
  - Constraint: 30
  - Scenario: 17
  - Question: 13
  - Documentation: 10
  - BugFixRequest: 10
  - ToolingBuild: 6
  - RefactorRequest: 5
  - TestRequest: 5

## Prompt ledger

### PL-ROOT (first substantive user prompt)

_Agent: Codex — 2026-03-03 18:34 — session `rollout-`_

```
read carefuly https://github.com/carlini/printf-tac-toe Basically git clone and analyze it. It show an implementation of tic-tac-toe using printf... 
Now implement a basic chess engine using printf exclusively, in the style of the repo

```

### Subsequent prompts (abridged)

| # | Time | Agent | Intent | Prompt (truncated) |
|---:|---|---|---|---|
| 2 | 2026-03-03 19:54 | Codex | Other | the spirit of printf-oriented programming is not respected... int main() { while(*d) printf(fmt, arg); } fmt should be a single string, and… |
| 3 | 2026-03-03 20:02 | Codex | Other | yes be closer to pure %n/format-string state mutation |
| 4 | 2026-03-03 20:20 | Codex | Other | is it possible to "unfold" the macros and so on to have a program like this int main() { while(*d) printf(fmt, arg); } |
| 5 | 2026-03-03 20:21 | Codex | Other | with fmt a char* and arg a #define |
| 6 | 2026-03-03 20:27 | Codex | Other | continue |
| 7 | 2026-03-03 20:35 | Codex | Other | would it be possible to unfold as well arg? |
| 8 | 2026-03-03 21:14 | Codex | FeatureRequest,Documentation | write a simple README.md (author Mathieu Acher and Codex) that explains the overall idea/approach, how does it work technically, whether th… |
| 9 | 2026-03-03 21:19 | Codex | FeatureRequest,Question | can you also add a section where you report on the coding session? the first attempt was a kind of failure (no respect of the spirit of pri… |
| 10 | 2026-03-03 21:23 | Codex | FeatureRequest | create a git, commit, and push on printf-chess-codex (github) |
| 11 | 2026-03-03 21:25 | Codex | Other | https://github.com/acherm/printf-chess-codex |
| 12 | 2026-03-03 21:29 | Codex | FeatureRequest | would it be possible to implement a Rust or Java variant? leveraging the same tricks with printf (or equivalent) |
| 13 | 2026-03-03 21:31 | Codex | Other | let's try Rust |
| 14 | 2026-03-03 21:44 | Codex | Other | and in Java ? |
| 15 | 2026-03-04 11:50 | Codex | FeatureRequest | still in the spirit of https://github.com/carlini/printf-tac-toe Now implement a basic snake using printf exclusively (as we have done it f… |
| 16 | 2026-03-04 12:01 | Codex | FeatureRequest,BugFixRequest | This is *very* much in the same **hybrid POP** family as the Codex chess repo: the **format string is doing a real POP-ish thing** (mutatin… |
| 17 | 2026-03-04 12:07 | Codex | Documentation | Let's get back to the chess engine in C. Printf oriented Programming is not totally respected. Let me argue What it clearly respects (more … |
| 18 | 2026-03-04 12:10 | Codex | FeatureRequest,BugFixRequest | This is a **nice step “more POP”** than the previous version, because now `fmt` is writing **two** pieces of state (`d[0]` run flag and `d[… |
| 19 | 2026-03-04 12:17 | Codex | FeatureRequest,Constraint | Role: You are implementing a program in Printf-Oriented Programming (POP). Non-negotiable goal: printf must be the execution engine; the fo… |
| 20 | 2026-03-04 12:19 | Codex | FeatureRequest,Constraint | it's still not pure POP Role: You are implementing a program in Printf-Oriented Programming (POP). Non-negotiable goal: printf must be the … |
| 21 | 2026-03-04 12:34 | Codex | Other | please commit/push |
| 22 | 2026-03-04 12:38 | Codex | Documentation,Question | can you remove from the git the Rust and Java variants? and update the README.md as well |
| 23 | 2026-03-04 12:40 | Codex | Other | yes go |
| 24 | 2026-03-04 12:43 | Codex | FeatureRequest,RefactorRequest | This is **legit POP (hybrid leaning “pretty pure”)**. You’ve nailed the two most important POP signals: * **Essential state mutation happen… |
| 25 | 2026-03-04 12:46 | Codex | FeatureRequest,RefactorRequest | Pretty strong POP attempt — **closer to “POP-pure core” than either chess variant**, with one notable “escape hatch”. ### Checklist verdict… |
| 26 | 2026-03-04 12:52 | Codex | FeatureRequest,Constraint | This is **much closer to “strict POP”**. You removed the per-tick arithmetic (PADL/PADR derived in C) and moved the *render-driving widths*… |
| 27 | 2026-03-04 12:55 | Codex | FeatureRequest,Constraint | This is **a big step closer to “Carlini-style POP”**. You’ve moved from “C selects a whole board snapshot” to **a single mutable board tape… |
| 28 | 2026-03-04 12:58 | Codex | Scenario | can we envision, following the strict POP style, a more ambitious Snake game? especially with some interactions with users |
| 29 | 2026-03-04 13:00 | Codex | Other | please commit/push first |
| 30 | 2026-03-04 13:01 | Codex | Other | let's go |
| 31 | 2026-03-04 13:01 | Codex | Other | let's go |
| 32 | 2026-03-04 13:10 | Codex | Other | let be more ambitious with chess and allows users to specify a move interactively. Please be strict POP |
| 33 | 2026-03-04 13:16 | Codex | FeatureRequest,BugFixRequest | Here’s a **refined POP Purity checklist** written as an **actionable coding-agent skill**. It’s designed to prevent “POP-shaped but not POP… |
| 34 | 2026-03-04 13:17 | Codex | Other | yes... think also about C programs "examples" likely to be compiled |
| 35 | 2026-03-04 13:18 | Codex | FeatureRequest | yes go... and then implement a compiler |
| 36 | 2026-03-04 13:21 | Codex | FeatureRequest,Constraint | Hybrid POP — **and you’re right on the edge of what my refined checklist would call “cheating (but cleanly)”**. You have a **real POP core*… |
| 37 | 2026-03-04 13:26 | Codex | FeatureRequest,BugFixRequest | Cool demo — **but per the refined POP checklist, this is “hybrid POP”**, mainly because **you mutate POP tape from C in a concurrent thread… |
| 38 | 2026-03-04 13:28 | Codex | FeatureRequest,Constraint | This is **cleaner** and “more POP-aligned” than the previous interactive version, but it’s still **hybrid POP**, not POP-pure. ### What imp… |
| 39 | 2026-03-04 13:30 | Codex | Question | can you showcase the compiler on a non-trivial program? |
| 40 | 2026-03-04 13:31 | Codex | Other | yes please go into this direction |
| 41 | 2026-03-04 13:32 | Codex | Other | go this way |
| 42 | 2026-03-04 13:33 | Codex | Other | yes second non-trivial case |
| 43 | 2026-03-04 13:41 | Codex | FeatureRequest,Question | can you write a tic-tac-toe in the C subset? |
| 44 | 2026-03-04 13:42 | Codex | Constraint | you still rely on an external thread doing read() and writing into d[KEY]. That’s reasonable (POP needs input from somewhere), but it means… |
| 45 | 2026-03-04 13:43 | Codex | Other | go this way, keep the POP spirit |
| 46 | 2026-03-04 13:44 | Codex | FeatureRequest,Constraint | This is **cleaner** and “more POP-aligned” than the previous interactive version, but it’s still **hybrid POP**, not POP-pure. ### What imp… |
| 47 | 2026-03-04 13:45 | Codex | Other | yes please extend the subset/compiler with tape input |
| 48 | 2026-03-04 13:52 | Codex | FeatureRequest,RefactorRequest | This is **much closer to “strict POP”** than your earlier interactive versions — nice move: you’ve pushed the *meaning* of the command onto… |
| 49 | 2026-03-04 13:56 | Codex | Other | yes |
| 50 | 2026-03-04 14:02 | Codex | Constraint,Scenario | I don't know how to play |
| 51 | 2026-03-04 14:09 | Codex | Other | yes |
| 52 | 2026-03-04 14:18 | Codex | Documentation,Constraint | can you update the README.md and reflect on the story: lots of back and forth to meet POP purity; very hard to reach with some anti-pattern… |
| 53 | 2026-03-04 14:22 | Codex | Constraint | great! frame the original questioning: can coding agents master Printf Oriented Programming? at the beginning... first rough impression is … |
| 54 | 2026-03-04 14:27 | Codex | FeatureRequest,BugFixRequest | the compiler looks good BUT should be improved It *sounds* like you’re aiming for POP, but **this excerpt is not “strict POP-pure” under th… |
| 55 | 2026-03-04 14:37 | Codex | Scenario | is it possible to play tic-tac-toe in POP-pure? |
| 56 | 2026-03-04 14:38 | Codex | Other | yes let's try... but before, please commit/push |
| 57 | 2026-03-04 14:58 | Codex | FeatureRequest,BugFixRequest | This version is **better structured** (the loop is clean; input handling is separated), but **it’s still not “strict POP-pure” under the re… |
| 58 | 2026-03-04 15:12 | Codex | BugFixRequest | any idea on how to fix the situation? |
| 59 | 2026-03-04 15:23 | Codex | Constraint | I want to avoid doing input semantics and branching in C (just with bit-twiddling instead of ?: is not a real solution) |
| 60 | 2026-03-04 15:33 | Codex | FeatureRequest,Constraint | yes please add a --vm-pure mode that rejects all C-evaluated expressions (not only input-derived ones). |
| … | | | | _+58 more prompts_ |

## Git timeline

| Hash | Date | Author | Subject |
|---|---|---|---|
| `1d77768` | 2026-03-05T00:52:36+01:00 | Mathieu Acher | Add basic snake subset example with POP artifact and tape encoder |
| `0bce8dc` | 2026-03-05T00:44:18+01:00 | Mathieu Acher | Document readable output filter for POP padded runs |
| `e3dd2f5` | 2026-03-05T00:30:34+01:00 | Mathieu Acher | Document expanded POP output size vs macro-compressed style |
| `79f957f` | 2026-03-04T23:28:49+01:00 | Mathieu Acher | Add generated POP artifacts and refresh compiler status docs |
| `da1c4c3` | 2026-03-04T23:24:12+01:00 | Mathieu Acher | Fix vm-pure scoring and host-snapshot audit |
| `1fe61e2` | 2026-03-04T16:01:36+01:00 | Mathieu Acher | Tighten VM-purity audit and reclassify strict-mode tic-tac-toe |
| `f72de87` | 2026-03-04T15:39:23+01:00 | Mathieu Acher | Add c2pop compiler MVP with purity modes, tape input, and examples |
| `cae4aed` | 2026-03-04T14:01:12+01:00 | Mathieu Acher | Refine POP chess core with script tape and board %hhn writes |
| `2c1b58f` | 2026-03-04T13:40:35+01:00 | Mathieu Acher | Remove Rust and Java variant docs |
| `d31d349` | 2026-03-04T13:34:38+01:00 | Mathieu Acher | Add strict POP snake driven by printf format semantics |
| `79c9e33` | 2026-03-03T22:23:34+01:00 | Mathieu Acher | Initial printf-oriented chess engine |

## User-driven feature backlog (best-effort, derived from prompts)

Extracted **48** candidate backlog items. Each maps 1-1 to a user prompt and may consolidate with implementation commits.

- **BL-001** (FeatureRequest) [2026-03-03 18:34] — read carefuly https://github.com/carlini/printf-tac-toe Basically git clone and analyze it. It show an implementation of tic-tac-toe using printf... Now implement a basic chess en… [T:Codex/rollout-]
- **BL-002** (FeatureRequest, Documentation) [2026-03-03 21:14] — write a simple README.md (author Mathieu Acher and Codex) that explains the overall idea/approach, how does it work technically, whether the spirit is preserved, and chess related… [T:Codex/rollout-]
- **BL-003** (FeatureRequest, Question) [2026-03-03 21:19] — can you also add a section where you report on the coding session? the first attempt was a kind of failure (no respect of the spirit of printf oriented programming)... otherwise l… [T:Codex/rollout-]
- **BL-004** (FeatureRequest) [2026-03-03 21:23] — create a git, commit, and push on printf-chess-codex (github) [T:Codex/rollout-]
- **BL-005** (FeatureRequest) [2026-03-03 21:29] — would it be possible to implement a Rust or Java variant? leveraging the same tricks with printf (or equivalent) [T:Codex/rollout-]
- **BL-006** (FeatureRequest) [2026-03-04 11:50] — still in the spirit of https://github.com/carlini/printf-tac-toe Now implement a basic snake using printf exclusively (as we have done it for a chess engine in this repo) [T:Codex/rollout-]
- **BL-007** (FeatureRequest, BugFixRequest, Constraint, Scenario) [2026-03-04 12:01] — This is *very* much in the same **hybrid POP** family as the Codex chess repo: the **format string is doing a real POP-ish thing** (mutating `d[0]` via `%hhn`), but the **actual g… [T:Codex/rollout-]
- **BL-008** (Documentation) [2026-03-04 12:07] — Let's get back to the chess engine in C. Printf oriented Programming is not totally respected. Let me argue What it clearly respects (more “core POP”) Still the canonical loop in … [T:Codex/rollout-]
- **BL-009** (FeatureRequest, BugFixRequest, RefactorRequest, Constraint, Scenario) [2026-03-04 12:10] — This is a **nice step “more POP”** than the previous version, because now `fmt` is writing **two** pieces of state (`d[0]` run flag and `d[1]` direction byte) via `%hhn`, and your… [T:Codex/rollout-]
- **BL-010** (FeatureRequest, Constraint, Scenario) [2026-03-04 12:17] — Role: You are implementing a program in Printf-Oriented Programming (POP). Non-negotiable goal: printf must be the execution engine; the format string must perform meaningful stat… [T:Codex/rollout-]
- **BL-011** (FeatureRequest, Constraint, Scenario) [2026-03-04 12:19] — it's still not pure POP Role: You are implementing a program in Printf-Oriented Programming (POP). Non-negotiable goal: printf must be the execution engine; the format string must… [T:Codex/rollout-]
- **BL-012** (FeatureRequest, RefactorRequest, ToolingBuild, Constraint, Scenario) [2026-03-04 12:43] — This is **legit POP (hybrid leaning “pretty pure”)**. You’ve nailed the two most important POP signals: * **Essential state mutation happens via `%hhn` in the format string** (d[0… [T:Codex/rollout-]
- **BL-013** (FeatureRequest, RefactorRequest, ToolingBuild, Constraint, Scenario) [2026-03-04 12:46] — Pretty strong POP attempt — **closer to “POP-pure core” than either chess variant**, with one notable “escape hatch”. ### Checklist verdict (actionable rubric) **1) Canonical loop… [T:Codex/rollout-]
- **BL-014** (FeatureRequest, Constraint, Scenario) [2026-03-04 12:52] — This is **much closer to “strict POP”**. You removed the per-tick arithmetic (PADL/PADR derived in C) and moved the *render-driving widths* onto the tape, and you update them thro… [T:Codex/rollout-]
- **BL-015** (FeatureRequest, Constraint, Scenario) [2026-03-04 12:55] — This is **a big step closer to “Carlini-style POP”**. You’ve moved from “C selects a whole board snapshot” to **a single mutable board tape** that `printf` modifies via `%hhn`, wh… [T:Codex/rollout-]
- **BL-016** (Scenario) [2026-03-04 12:58] — can we envision, following the strict POP style, a more ambitious Snake game? especially with some interactions with users [T:Codex/rollout-]
- **BL-017** (FeatureRequest, BugFixRequest, Constraint) [2026-03-04 13:16] — Here’s a **refined POP Purity checklist** written as an **actionable coding-agent skill**. It’s designed to prevent “POP-shaped but not POP” solutions and to push the agent toward… [T:Codex/rollout-]
- **BL-018** (FeatureRequest) [2026-03-04 13:18] — yes go... and then implement a compiler [T:Codex/rollout-]
- **BL-019** (FeatureRequest, Constraint) [2026-03-04 13:21] — Hybrid POP — **and you’re right on the edge of what my refined checklist would call “cheating (but cleanly)”**. You have a **real POP core** (the board writes + run flag are done … [T:Codex/rollout-]
- **BL-020** (FeatureRequest, BugFixRequest, Constraint, Scenario) [2026-03-04 13:26] — Cool demo — **but per the refined POP checklist, this is “hybrid POP”**, mainly because **you mutate POP tape from C in a concurrent thread** and because the loop arguments are do… [T:Codex/rollout-]
- **BL-021** (FeatureRequest, Constraint) [2026-03-04 13:28] — This is **cleaner** and “more POP-aligned” than the previous interactive version, but it’s still **hybrid POP**, not POP-pure. ### What improved (good POP moves) * You moved a bun… [T:Codex/rollout-]
- **BL-022** (Constraint) [2026-03-04 13:42] — you still rely on an external thread doing read() and writing into d[KEY]. That’s reasonable (POP needs input from somewhere), but it means not everything is inside printf. Import… [T:Codex/rollout-]
- **BL-023** (FeatureRequest, RefactorRequest, Constraint, Scenario) [2026-03-04 13:52] — This is **much closer to “strict POP”** than your earlier interactive versions — nice move: you’ve pushed the *meaning* of the command onto the **user** (raw indices + piece byte … [T:Codex/rollout-]
- **BL-024** (Constraint, Scenario) [2026-03-04 14:02] — I don't know how to play [T:Codex/rollout-]
- **BL-025** (Documentation, Constraint, Question, Scenario) [2026-03-04 14:18] — can you update the README.md and reflect on the story: lots of back and forth to meet POP purity; very hard to reach with some anti-patterns like implementing the logic directly i… [T:Codex/rollout-]
- **BL-026** (Constraint) [2026-03-04 14:22] — great! frame the original questioning: can coding agents master Printf Oriented Programming? at the beginning... first rough impression is that it was the case (with a working che… [T:Codex/rollout-]
- **BL-027** (FeatureRequest, BugFixRequest, TestRequest, Constraint) [2026-03-04 14:27] — the compiler looks good BUT should be improved It *sounds* like you’re aiming for POP, but **this excerpt is not “strict POP-pure” under the checklist** as written. It’s closer to… [T:Codex/rollout-]
- **BL-028** (Scenario) [2026-03-04 14:37] — is it possible to play tic-tac-toe in POP-pure? [T:Codex/rollout-]
- **BL-029** (FeatureRequest, BugFixRequest, RefactorRequest, TestRequest, Constraint) [2026-03-04 14:58] — This version is **better structured** (the loop is clean; input handling is separated), but **it’s still not “strict POP-pure” under the refined checklist**, because you’re still … [T:Codex/rollout-]
- **BL-030** (BugFixRequest) [2026-03-04 15:12] — any idea on how to fix the situation? [T:Codex/rollout-]
- **BL-031** (Constraint) [2026-03-04 15:23] — I want to avoid doing input semantics and branching in C (just with bit-twiddling instead of ?: is not a real solution) [T:Codex/rollout-]
- **BL-032** (FeatureRequest, Constraint) [2026-03-04 15:33] — yes please add a --vm-pure mode that rejects all C-evaluated expressions (not only input-derived ones). [T:Codex/rollout-]
- **BL-033** (FeatureRequest, BugFixRequest, Constraint) [2026-03-04 15:47] — This is **still not POP-pure**, and in fact it’s drifting *further away* from the “printf is the VM” philosophy. ### POP purity checklist verdict for this pattern **Gate A — Canon… [T:Codex/rollout-]
- **BL-034** (FeatureRequest, TestRequest, Documentation, Constraint, Scenario) [2026-03-04 15:52] — here are some explanations: Tic-Tac-Toe The game itself is represented as a board of 18 bits, 9 bits per player, along with a turn counter that alternates between player 1 and pla… [T:Codex/rollout-]
- **BL-035** (FeatureRequest, BugFixRequest, Constraint, Scenario) [2026-03-04 16:00] — You’re **very close to something that can be defended as “VM-pure tape protocol”**, *but only under a specific POP definition*. Under the stricter “printf is the VM and owns the s… [T:Codex/rollout-]
- **BL-036** (Constraint) [2026-03-04 16:17] — so it's not acceptable at all... frankly, I don't like the direction [T:Codex/rollout-]
- **BL-037** (FeatureRequest, BugFixRequest, Constraint) [2026-03-04 16:43] — Verdict for **this pattern** (reading bytes into tape, then passing *differences* as `printf` widths): ## POP purity checklist verdict **Not POP-pure (Hybrid / “C-precompute” anti… [T:Codex/rollout-]
- **BL-038** (FeatureRequest) [2026-03-04 16:45] — yes add this hard mode [T:Codex/rollout-]
- **BL-039** (Constraint) [2026-03-04 17:31] — "The strict playable subset cannot pass --vm-pure until expression evaluation is moved out of C entirely (new VM-level lowering for boolean/arithmetic ops)." That's a direction to… [T:Codex/rollout-]
- **BL-040** (Documentation) [2026-03-04 22:25] — please commit/push generated/*.pop.c and update README.md on last status of the compiler stuff [T:Codex/rollout-]
- _+8 more items truncated in this view — see appendix._

## Evidence pointers

- [R:chess-printf-codex] — repo at `/Users/mathieuacher/SANDBOX/chess-printf-codex`
- [T:chess-printf-codex/claude] — Claude sessions at `~/.claude/projects/chess-printf-codex...`
- [T:chess-printf-codex/codex] — Codex sessions filtered from `~/.codex/sessions/**.jsonl`
- [S:scan] — `scripts/common.py::compute_loc` executed on /Users/mathieuacher/SANDBOX/chess-printf-codex

## Limitations

- Cost estimates assume list prices and ignore Anthropic/OpenAI account discounts.
- Chess feature detection uses regex; languages with unusual syntax (Brainfuck, APL, assembler) can be under-detected.
- User backlog is derived from user-authored prompts; constraints and acceptance criteria are often implicit.