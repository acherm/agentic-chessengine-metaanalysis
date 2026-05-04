#!/usr/bin/env python3
"""Recompute per-engine cost/prompt totals after stripping post-mortem
analysis sessions, and emit a canonical Norm. USD column.

Detection rule for post-mortem session:
  no engine-core writes (proxy: <=3 Write/Edit tool uses)
  AND <=5 user prompts in that session
  AND first-prompt looks like analysis vocabulary
    (analyze|analyse|review|README|backlog|annotate|document|assess
     ...whether...pure|post-session)

For each engine we report:
  primary_agent  - 'CC', 'Codex', or 'CC+Codex' if both contributed
                   non-trivially after stripping post-mortem
  prompts        - sum of primary-agent user prompts
  in_ktok        - sum of (input + cache_read + cache_creation) tokens / 1000
  out_ktok       - sum of output tokens / 1000
  list_usd       - sum of vendor-specific usd_estimate from primary sessions
  norm_usd       - canonical: in_MTok * 1.00 + out_MTok * 5.00
"""

import json
import re
import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / 'data' / 'projects'

ANALYSIS_RE = re.compile(
    r'(analyz[es]|analyse|please analyze|review the (repo|code|repository)'
    r'|review this repo|README|'
    r'backlog|annotate|document the architecture|assess whether|'
    r'post-session|post-mortem|introspect|strategy analyst|'
    r'reorganize the first|consider chess\.bf and reorganize)',
    re.IGNORECASE,
)

# Engines we care about for the EMSE table (matches tab_engines.tex order)
ENGINES = [
    'chess-cobol-cc', 'COBOL-chess', 'chess-brainfuck', 'chess-brainfuck-cc',
    'chess-ruby-cc', 'lean-chess', 'chess-latex-codex-replication',
    'chess-apl-codex54', 'cplusplus-chess', 'chess-rust-cc-redo',
    'chess-ruby-codex', 'chess-assembly-codex', 'chess-py', 'chess-css-codex',
    'chess-why3', 'chess-java', 'chess-icon-codex', 'chess-purec-codex',
    'chess-rust-codex', 'chess-css-codex-guided', 'chess-java-cc',
    'latex-chess-engine', 'chess-Rocq',
    # archived-transcript main rows
    'chess-cplusplus-claude', 'chess-purec', 'chess-py-cc', 'chess-rust-cc',
    'chess-sql', 'chess-why3-cc',
    # special-role
    'chess-revisit-java-toCOBOL-codex', 'chess-revisit-java-toRust-codex',
    'chess-newlang-codex', 'chess-mojo', 'test-superset',
]


def is_postmortem(sess):
    """Heuristic for post-mortem analysis sessions:
       (analysis vocab in first prompt) OR
       (no engine-core writes AND <=5 prompts AND no build vocab).
    """
    tu = sess.get('tool_uses', {}) or {}
    writes = tu.get('Write', 0) + tu.get('Edit', 0) + tu.get('apply_patch', 0)
    turns = sess.get('turns', 0)
    fp = sess.get('first_prompt_sample', '') or ''
    if ANALYSIS_RE.search(fp):
        return True
    # short, write-light, single-turn one-shots that aren't builds
    if writes <= 3 and turns <= 5:
        # Build prompts usually start with "I want to build" or
        # "build a chess engine" or imperative coding-task vocab.
        if re.search(r'(build|implement|write|create|develop)\s+(a\s+)?'
                     r'(chess|engine)', fp, re.IGNORECASE):
            return False
        if turns <= 1:
            return True
    return False


def aggregate_sessions(sessions):
    """Sum tokens, prompts, USD across the listed sessions."""
    in_t = out_t = prompts = usd = 0
    for s in sessions:
        tok = s.get('tokens', {}) or {}
        in_t += (tok.get('input', 0) + tok.get('cache_read', 0)
                 + tok.get('cache_creation', 0))
        out_t += tok.get('output', 0) + tok.get('reasoning_output', 0)
        prompts += s.get('turns', 0)
        usd += s.get('usd_estimate', 0)
    return prompts, in_t, out_t, usd


def process_engine(name):
    path = DATA_DIR / f'{name}.json'
    if not path.exists():
        return None
    d = json.loads(path.read_text())
    cc, cx = d.get('claude', {}) or {}, d.get('codex', {}) or {}

    # Per-vendor: split into primary vs post-mortem sessions
    cc_primary = [s for s in cc.get('sessions', []) if not is_postmortem(s)]
    cc_postmortem = [s for s in cc.get('sessions', []) if is_postmortem(s)]
    cx_primary = [s for s in cx.get('sessions', []) if not is_postmortem(s)]
    cx_postmortem = [s for s in cx.get('sessions', []) if is_postmortem(s)]

    # Aggregate primary-only from per-session
    cc_p_prompts, cc_in, cc_out, _ = aggregate_sessions(cc_primary)
    cc_pm_prompts, cc_pm_in, cc_pm_out, _ = aggregate_sessions(cc_postmortem)
    cx_p_prompts, cx_in, cx_out, _ = aggregate_sessions(cx_primary)
    cx_pm_prompts, cx_pm_in, cx_pm_out, _ = aggregate_sessions(cx_postmortem)

    def vendor_usd(vendor, primary_in, primary_out, total_in, total_out):
        """Use vendor's reported usd_estimate; if some sessions are
           post-mortem, scale by token share contributed by primary."""
        v_usd = vendor.get('cost', {}).get('usd_estimate', 0)
        total = total_in + total_out
        primary = primary_in + primary_out
        if total == 0 or primary == 0:
            return 0.0
        return v_usd * primary / total

    cc_total_in = cc_in + cc_pm_in
    cc_total_out = cc_out + cc_pm_out
    cx_total_in = cx_in + cx_pm_in
    cx_total_out = cx_out + cx_pm_out

    # Prefer vendor-level cost block when no post-mortem sessions
    if not cc_postmortem and cc.get('cost'):
        cc_tok = cc['cost'].get('tokens_total', {}) or {}
        cc_in = cc_tok.get('input', 0) + cc_tok.get('cache_read', 0) \
                + cc_tok.get('cache_creation', 0)
        cc_out = cc_tok.get('output', 0)
    if not cx_postmortem and cx.get('cost'):
        cx_tok = cx['cost'].get('tokens_total', {}) or {}
        cx_in = cx_tok.get('input', 0) + cx_tok.get('cache_read', 0) \
                + cx_tok.get('cache_creation', 0)
        cx_out = cx_tok.get('output', 0) + cx_tok.get('reasoning_output', 0)

    cc_usd = vendor_usd(cc, cc_in, cc_out, cc_total_in, cc_total_out)
    cx_usd = vendor_usd(cx, cx_in, cx_out, cx_total_in, cx_total_out)

    if not cc_postmortem:
        cc_p_prompts = cc.get('n_user_prompts', 0)
    if not cx_postmortem:
        cx_p_prompts = cx.get('n_user_prompts', 0)

    cc_p_prompts_thresh = cc_p_prompts >= 3
    cx_p_prompts_thresh = cx_p_prompts >= 3

    # Determine primary agent
    if cc_p_prompts_thresh and cx_p_prompts_thresh:
        primary = 'CC+Codex'
    elif cc_p_prompts_thresh:
        primary = 'CC'
    elif cx_p_prompts_thresh:
        primary = 'Codex'
    elif cc_p_prompts > 0:
        primary = 'CC'
    elif cx_p_prompts > 0:
        primary = 'Codex'
    else:
        primary = 'n/a'

    has_postmortem = bool(cc_postmortem or cx_postmortem)

    total_prompts = cc_p_prompts + cx_p_prompts
    total_in_ktok = (cc_in + cx_in) / 1000
    total_out_ktok = (cc_out + cx_out) / 1000
    total_list_usd = cc_usd + cx_usd
    norm_usd = (total_in_ktok / 1000) * 1.00 + (total_out_ktok / 1000) * 5.00

    return dict(
        name=name,
        primary=primary,
        flat='♭' if has_postmortem else '',
        prompts=total_prompts,
        in_ktok=round(total_in_ktok),
        out_ktok=round(total_out_ktok),
        list_usd=round(total_list_usd, 2),
        norm_usd=round(norm_usd, 2),
        cc_postmortem=len(cc_postmortem),
        cx_postmortem=len(cx_postmortem),
        cc_postmortem_prompts=sum(s.get('turns', 0) for s in cc_postmortem),
        cx_postmortem_prompts=sum(s.get('turns', 0) for s in cx_postmortem),
    )


def main():
    rows = []
    for name in ENGINES:
        r = process_engine(name)
        if r:
            rows.append(r)

    print(
        f"{'engine':<35}  {'primary':<10}  {'flat':<2}  "
        f"{'prompts':>7}  {'in_kTok':>9}  {'out_kTok':>8}  "
        f"{'list_USD':>9}  {'norm_USD':>9}  {'pm_cc/cx':<10}"
    )
    print('-' * 120)
    for r in rows:
        pm = f"{r['cc_postmortem_prompts']}/{r['cx_postmortem_prompts']}" \
             if r['flat'] else ''
        print(
            f"{r['name']:<35}  {r['primary']:<10}  {r['flat']:<2}  "
            f"{r['prompts']:>7d}  {r['in_ktok']:>9d}  {r['out_ktok']:>8d}  "
            f"${r['list_usd']:>8.2f}  ${r['norm_usd']:>8.2f}  {pm:<10}"
        )

    # Totals
    total_norm = sum(r['norm_usd'] for r in rows)
    total_list = sum(r['list_usd'] for r in rows)
    total_prompts = sum(r['prompts'] for r in rows)
    print('-' * 120)
    print(
        f"{'TOTAL':<35}  {'':<10}  {'':<2}  "
        f"{total_prompts:>7d}  {'':>9}  {'':>8}  "
        f"${total_list:>8.2f}  ${total_norm:>8.2f}"
    )


if __name__ == '__main__':
    main()
