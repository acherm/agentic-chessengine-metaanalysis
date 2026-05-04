# Prompts for the Rust × Claude Code redo

_Playbook for a fresh Claude Code session that produces a scratch-built Rust chess engine, matching the canonical low-instruction / reactive style observed across the rest of the corpus._

## Why the redo

`chess-rust-codex` uses the Rust `chess` crate in `src/uci.rs` and `src/engine.rs` for board-state types and move generation, then authors search + evaluation around it. This makes the Rust cell not directly comparable to the other scratch cells (Ruby-cc, COBOL-cc, C, Java, Ruby-codex, ...). The redo gives us a clean Rust × agent data point and a fair within-language A/B against `chess-rust-cc`. We match the prompt cadence of the COBOL-cc, C-codex, and Mojo sessions: one capability-level PL-ROOT, then minimal reactive steering ("go", "continue", "improve the Elo"), with explicit redirects only when the agent reaches for an external library.

## Suggested target

Fresh folder: `~/SANDBOX/chess-rust-cc-v2/` (empty, git-init optional). Run Claude Code from that folder.

## PL-ROOT (paste verbatim as the first message)

```
I want to build a chess engine in Rust programming language... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels
```

_This is the same PL-ROOT used for `chess-rust-codex`, `chess-cobol-cc`, `chess-mojo`, `chess-latex-codex-replication`, etc. Keep the ellipsis and the quoted ``similar'' --- it is part of the corpus-canonical phrasing._

## Typical reactive cadence

Send one prompt at a time. Wait for the agent to pause / ask a question / produce a checkpoint before sending the next. Do not queue them all upfront.

1. `Let's go for Phase 1`          _(when the agent proposes a phased roadmap)_
2. `go to Phase 2`                  _(after perft / smoke tests pass)_
3. `go`                             _(standard acknowledgement)_
4. `continue`                       _(after a context-boundary summary)_
5. `yes`                            _(for direct yes/no confirmations)_
6. `status?`                        _(when a session feels idle)_
7. `please go ahead and try to improve the Elo`   _(recurring improvement loop --- send multiple times as needed)_

## Reactive redirects --- use only if triggered

**(A) If the agent adds a chess library to `Cargo.toml`** (likely triggers: `chess`, `shakmaty`, `cozy-chess`, `pgn-reader`, or any other `<name>-chess` crate):

> I noticed `<crate>` in Cargo.toml. I'd like the engine to be implemented from scratch — no external chess library. Please implement board representation, move generation, legality, search, and evaluation yourself.

**(B) If the agent uses a chess crate in engine-core source** (`src/board.rs`, `src/movegen.rs`, `src/engine.rs`, `src/uci.rs` — anything not under `tests/` or `benches/`):

> `<file>` is engine-core, not tooling. The engine itself should be pure Rust with no chess-library dependency; external libraries are fine in the evaluation harness if you want, but not in the engine.

**(C) If the agent proposes a tournament but skips Stockfish calibration:**

> Can you organize a match against Stockfish at different skill levels (cutechess-cli with UCI_LimitStrength=true at UCI_Elo 1320, 1500, 1700, 1900, 2100)?

**(D) If perft compliance is deferred too long:**

> Please verify perft 1–6 from the Chess Programming Wiki reference positions first, then proceed.

**(E) If the agent gets stuck in a debugging loop:**

> please further improve

or a specific FEN-based report if you spot an illegal move:

> Engine played `<move>` in this position: `<FEN>`. That looks illegal. Can you investigate?

## Stop conditions

- Two successive `improve the Elo` rounds yield no measurable gain at the target Stockfish rung.
- Session hits Claude Code auto-compaction for the second time.
- Your own budget / time cap.

Match the corpus convention: no uniform budget cap; stop when strength plateaus or the engine is feature-rich enough for end-to-end gameplay.

## Post-session housekeeping (for the meta-analysis pipeline)

```bash
cd ~/SANDBOX/chess-meta-analysis

# Add the new engine to the taxonomy (edit synthesis.py CLASSIFICATION):
#    "chess-rust-cc-v2": "engine",

# Refresh data
python3 scripts/discover.py
python3 scripts/elo_and_perft.py
python3 scripts/extract_elo.py
python3 scripts/enrich_projects.py
python3 scripts/novelty_analysis.py chess-rust-cc-v2
python3 scripts/consistency_report.py
python3 scripts/engines_manifest.py

# Sanity-check:
#   - reports/ENGINES.md shows the new engine
#   - data/novelty.json classifies chess-rust-cc-v2 as "scratch"
#     (not "library-assisted" or "fingerprint-match")
#   - reports/CONSISTENCY.md has a row for it
```

## Expected outputs

After the session and the post-session refresh, the meta-analysis paper gets:

- **A clean Rust × Claude Code scratch data point**, comparable against `chess-rust-cc` (also scratch) and `chess-rust-codex` (library-assisted).
- **A "same language, same agent, with vs. without library" comparison** between `chess-rust-cc-v2` and `chess-rust-codex` --- an independent secondary finding for the paper.
- **A validation** of the novelty-audit pipeline: if the redirect (A) or (B) fires, the reactive supervision protocol (§4.4 of the paper) becomes an operational claim rather than a retrospective one.

## Things to avoid (to preserve corpus comparability)

- Don't provide an architecture plan (the Ruby-cc session had one; we treat it as an outlier, not the canonical protocol).
- Don't pre-name algorithms (``use MTD(f)'', ``use PVS with aspiration windows'').
- Don't dictate board representation (0×88 vs bitboards).
- Don't propose evaluation terms (material + PST + mobility + king safety, etc.).
- Don't intervene on technical choices unless the agent explicitly asks.
- Do help with environment issues (install `cutechess-cli`, install Stockfish, linker errors) if they block progress — these count as developer support, not engine authorship (per §4.3 of the paper).

## Recording the run

If possible, keep the `~/.claude/projects/-Users-mathieuacher-SANDBOX-chess-rust-cc-v2/` transcript intact (do not let Claude Code archive it). The paper relies on transcript retention for the novelty audit and the interaction-profile analysis.
