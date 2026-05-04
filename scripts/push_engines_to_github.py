#!/usr/bin/env python3
"""Push the 34 agentic chess engines to github.com/acherm.

For each engine:
  1. Add a per-language .gitignore (skip build artefacts: target/, .venv/, ...)
  2. Add MIT LICENSE if missing
  3. Add a README.md (Mathieu Acher + coding-agent attribution)
  4. git init if not already, commit if there are changes
  5. gh repo create acherm/<repo> --public if it doesn't exist; push current branch

Usage:
  python3 scripts/push_engines_to_github.py [--dry-run] [--only <engine>]
"""

from __future__ import annotations
import argparse
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

SANDBOX = Path('/Users/mathieuacher/SANDBOX')
GH_OWNER = 'acherm'
PAPER_ANCHOR = 'Mathieu Acher (mathieu.acher@irisa.fr)'

# (local_folder, github_repo_name, primary_agent_label, lang_label, role, notes)
ENGINES = [
    ('chess-apl-codex54',                 'agentic-chessengine-apl-codex',                'Codex (GPT-5.4 / GPT-5-codex)', 'APL',           'main',      None),
    ('chess-assembly-codex',              'agentic-chessengine-assembly-codex',           'Codex (GPT-5-codex)',           'x86-64 Assembly','main',      None),
    ('chess-brainfuck',                   'agentic-chessengine-brainfuck-codexfailure',   'Codex (GPT-5-codex)',           'Brainfuck',     'main',      'lower-strength variant; the stronger one is the CC version (agentic-chessengine-brainfuck)'),
    ('chess-brainfuck-cc',                'agentic-chessengine-brainfuck',                'Claude Code (Opus 4.6/4.7)',    'Brainfuck',     'main',      None),
    ('chess-cobol-cc',                    'agentic-chessengine-cobol-cc',                 'Claude Code (Opus 4.6/4.7)',    'COBOL',         'main',      None),
    ('COBOL-chess',                       'agentic-chessengine-cobol-codex',              'Codex (GPT-5-codex)',           'COBOL',         'main',      None),
    ('chess-cplusplus-claude',            'agentic-chessengine-cpp-cc',                   'Claude Code (Opus 4.6/4.7)',    'C++',           'main',      None),
    ('cplusplus-chess',                   'agentic-chessengine-cpp-codex',                'Codex (GPT-5-codex)',           'C++',           'main',      None),
    ('chess-css-codex',                   'agentic-chessengine-css-codex',                'Codex (GPT-5-codex)',           'CSS/HTML',      'main',      'evasion case --- engine-core uses python-chess despite the CSS framing'),
    ('chess-css-codex-guided',            'agentic-chessengine-css-codex-guided',         'Codex (GPT-5-codex)',           'CSS/HTML',      'main',      'strict-CSS variant after the user redirected the agent away from python-chess'),
    ('chess-icon-codex',                  'agentic-chessengine-icon-codex',               'Codex (GPT-5-codex)',           'Icon',          'main',      None),
    ('chess-java',                        'agentic-chessengine-java-codex',               'Codex (GPT-5-codex)',           'Java',          'main',      None),
    ('chess-java-cc',                     'agentic-chessengine-java-cc',                  'Claude Code (Opus 4.6/4.7)',    'Java',          'main',      None),
    ('chess-latex-codex-replication',     'agentic-chessengine-latex-codex-replication',  'Codex (GPT-5-codex)',           'LaTeX (expl3)', 'main',      'replication study of the canonical TeXCCChess engine'),
    ('latex-chess-engine',                'agentic-chessengine-latex-TeXCCChess',         'Codex (GPT-5-codex)',           'TeX',           'main',      'TeXCCChess --- self-claims first-of-kind in pure TeX'),
    ('lean-chess',                        'agentic-chessengine-lean-codex',               'Codex (GPT-5-codex)',           'Lean 4',        'main',      None),
    ('chess-mojo',                        'agentic-chessengine-mojo-codexfailure',        'Codex (GPT-5-codex)',           'Mojo',          'failure',   'unconverged: the engine plateaued at ~Elo 900 against calibrated Stockfish'),
    ('chess-newlang-codex',               'agentic-chessengine-dsl-newlang-codex',        'Codex (GPT-5-codex)',           'C++ (host) / GAMBIT DSL', 'DSL', 'agent-designed DSL (GAMBIT) plus its C++17 transpiler runtime'),
    ('chess-purec',                       'agentic-chessengine-c-cc',                     'Claude Code (Opus 4.6/4.7)',    'C',             'main',      'main session transcripts compacted before capture'),
    ('chess-purec-codex',                 'agentic-chessengine-c-codex',                  'Codex (GPT-5-codex)',           'C',             'main',      None),
    ('chess-py',                          'agentic-chessengine-python-codex',             'Codex (GPT-5-codex)',           'Python',        'main',      None),
    ('chess-py-cc',                       'agentic-chessengine-python-cc',                'Claude Code (Opus 4.6/4.7)',    'Python',        'main',      'main session transcripts compacted before capture'),
    ('chess-revisit-java-toRust-codex',   'agentic-chessengine-rust-from-java-codex',     'Codex (GPT-5-codex)',           'Rust',          'port',      'translation of chess-java-cc to Rust, preserving module structure'),
    ('chess-Rocq',                        'agentic-chessengine-rocq-cc',                  'Claude Code (Opus 4.6/4.7)',    'Rocq -> OCaml', 'main',      None),
    ('chess-ruby-cc',                     'agentic-chessengine-ruby-cc',                  'Claude Code (Opus 4.6/4.7)',    'Ruby',          'main',      None),
    ('chess-ruby-codex',                  'agentic-chessengine-ruby-codex',               'Codex (GPT-5-codex)',           'Ruby',          'main',      None),
    ('chess-rust-cc',                     'agentic-chessengine-rust-cc',                  'Claude Code (Opus 4.6/4.7)',    'Rust',          'main',      'main session transcripts compacted before capture'),
    ('chess-rust-cc-redo',                'agentic-chessengine-rust-cc-redo',             'Claude Code (Opus 4.6/4.7)',    'Rust',          'main',      'second-try Rust, intact authoring log; explicit "no chess crate" constraint'),
    ('chess-rust-codex',                  'agentic-chessengine-rust-codex',               'Codex (GPT-5-codex)',           'Rust',          'main',      'library-assisted: imports the Rust `chess` crate for board+move-gen'),
    ('chess-sql',                         'agentic-chessengine-sql-cc',                   'Claude Code (Opus 4.6/4.7)',    'SQL',           'main',      'main session transcripts compacted before capture'),
    ('chess-why3',                        'agentic-chessengine-why3-codex',               'Codex (GPT-5-codex)',           'Why3 -> OCaml', 'main',      None),
    ('chess-why3-cc',                     'agentic-chessengine-why3-cc',                  'Claude Code (Opus 4.6/4.7)',    'Why3 -> C',     'main',      'main session transcripts compacted before capture'),
    ('test-superset',                     'agentic-chessengine-css-ChessCSS',             'Claude Code (Opus 4.6/4.7)',    'CSS + minimal JS', 'co-design', 'ChessCSS --- 31-commit JS->CSS migration under sustained expert steering'),
]

# Special: Java->COBOL port lives as a subdirectory of chess-revisit-java-toRust-codex.
COBOL_PORT_SUBDIR = 'chess-revisit-java-toCOBOL'
COBOL_PORT_PARENT = 'chess-revisit-java-toRust-codex'
COBOL_PORT_TARGET_DIR = 'chess-revisit-java-toCOBOL-codex'  # to materialise under SANDBOX
COBOL_PORT_REPO = 'agentic-chessengine-cobol-from-java-codex'

GITIGNORE_BY_LANG = {
    'Python': '__pycache__/\n*.pyc\n.venv/\nvenv/\nenv/\n.pytest_cache/\n*.egg-info/\nbuild/\ndist/\n',
    'Rust': 'target/\nCargo.lock\n*.rlib\n',
    'Java': 'target/\nbuild/\n*.class\n*.jar\n.gradle/\n',
    'C': 'build/\n*.o\n*.a\n*.so\n*.dylib\n*.exe\n',
    'C++': 'build/\n*.o\n*.a\n*.so\n*.dylib\n*.exe\n',
    'Lean 4': '.lake/\nbuild/\nlakefile.olean\n*.olean\n',
    'Rocq -> OCaml': '_build/\n*.vo\n*.vok\n*.vos\n*.glob\n*.aux\n.coq-native/\n*.cmi\n*.cmo\n*.cmx\n',
    'Why3 -> OCaml': '_build/\n*.cmi\n*.cmo\n*.cmx\n*.cmxa\n',
    'Why3 -> C': '_build/\n*.cmi\n*.cmo\n*.cmx\n*.o\n*.a\n',
    'Ruby': '.bundle/\nvendor/\n',
    'Mojo': '.venv/\nvenv/\n*.modular/\nbuild/\n',
    'COBOL': 'build/\n*.o\n*.so\n*.dylib\n*.exe\n',
    'LaTeX (expl3)': '*.aux\n*.log\n*.out\n*.pdf\n*.fdb_latexmk\n*.fls\n*.synctex.gz\n*.toc\n',
    'TeX': '*.aux\n*.log\n*.out\n*.fdb_latexmk\n*.fls\n*.synctex.gz\n*.toc\n',
    'CSS/HTML': 'node_modules/\n.parcel-cache/\ndist/\nbuild/\n',
    'CSS + minimal JS': 'node_modules/\n.parcel-cache/\ndist/\nbuild/\n',
    'C++ (host) / GAMBIT DSL': 'build/\n*.o\n*.a\n*.so\n*.dylib\n*.exe\n',
    'APL': '\n',  # nothing language-specific
    'x86-64 Assembly': '*.o\n*.exe\n',
    'Icon': '*.u1\n*.u2\nuni\n',
    'SQL': '*.db\n*.sqlite\n*.sqlite3\n',
}

MIT_LICENSE = '''MIT License

Copyright (c) 2025--2026 Mathieu Acher

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''


def make_readme(repo, agent, lang, role, notes, original_folder):
    lines = [
        f'# {repo}',
        '',
        f'An **agentic chess engine** in **{lang}**, created and supervised by '
        f'{PAPER_ANCHOR} with the **{agent}** coding agent.',
        '',
    ]
    if role == 'port':
        lines += [
            f'_Role:_ Java→{lang} port of the `chess-java-cc` reference engine.',
            '',
        ]
    elif role == 'DSL':
        lines += [
            '_Role:_ DSL-design experiment — the agent designs a new chess-engine DSL '
            'and its C++17 transpiler.',
            '',
        ]
    elif role == 'failure':
        lines += [
            '_Role:_ unconverged failure case — the engine reached a working but weak '
            'baseline and stopped at a user-judged plateau.',
            '',
        ]
    elif role == 'co-design':
        lines += [
            '_Role:_ agent-heavy co-design — engine built under sustained expert '
            'steering rather than minimal-instruction prompting.',
            '',
        ]
    if notes:
        lines += [f'_Notes:_ {notes}.', '']
    lines += [
        '## Build / play',
        '',
        'Each repository contains the engine source, build files, and any '
        'gameplay artefacts (PGN records, perft logs) preserved from the '
        'authoring sessions. Open the per-folder build instructions in the '
        'root files (`Cargo.toml`, `Makefile`, `pom.xml`, `*.cabal`, '
        '`lakefile.lean`, etc.) for build commands.',
        '',
        '## Provenance',
        '',
        f'- Original local folder: `{original_folder}`',
        f'- Primary developer agent: {agent}',
        f'- Programming language: {lang}',
        '',
        '## License',
        '',
        'Released under the MIT License (see `LICENSE`).',
        '',
    ]
    return '\n'.join(lines)


def run(cmd, cwd=None, check=True, capture=False):
    if isinstance(cmd, str):
        argv = shlex.split(cmd)
    else:
        argv = list(cmd)
    if capture:
        r = subprocess.run(argv, cwd=cwd, check=check, capture_output=True, text=True)
        return r.stdout.strip()
    else:
        subprocess.run(argv, cwd=cwd, check=check)
        return None


def gh_repo_exists(name):
    try:
        run(f'gh repo view {GH_OWNER}/{name}', capture=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def ensure_files(local, lang, repo, agent, role, notes):
    """Write README, LICENSE, .gitignore if missing or stale."""
    readme = local / 'README.md'
    if not readme.exists():
        readme.write_text(make_readme(repo, agent, lang, role, notes, local.name))
    licf = local / 'LICENSE'
    if not licf.exists():
        licf.write_text(MIT_LICENSE)
    gitig = local / '.gitignore'
    pattern = GITIGNORE_BY_LANG.get(lang, '')
    if pattern.strip():
        # Append our patterns if not already there
        existing = gitig.read_text() if gitig.exists() else ''
        marker = '# --- agentic-chessengine ignore (auto-added) ---\n'
        if marker not in existing:
            with gitig.open('a') as f:
                f.write('\n' + marker + pattern)


def current_branch(local):
    try:
        b = run('git rev-parse --abbrev-ref HEAD', cwd=local, capture=True,
                check=False)
        return b if b and b != 'HEAD' else None
    except subprocess.CalledProcessError:
        return None


def has_commits(local):
    try:
        run('git rev-parse --verify HEAD', cwd=local, capture=True,
            check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def init_and_commit(local):
    if not (local / '.git').exists():
        run('git init -b main', cwd=local)
    # Stage and commit if there are changes
    status = run('git status --porcelain', cwd=local, capture=True,
                 check=False) or ''
    if status:
        run('git add -A', cwd=local)
        try:
            run(['git', 'commit', '-m',
                 'Add agentic chess-engine README, LICENSE, .gitignore'],
                cwd=local)
        except subprocess.CalledProcessError:
            pass
    # After first commit branch will exist; rename if master
    if has_commits(local):
        b = current_branch(local)
        if b == 'master':
            try:
                run('git branch -m master main', cwd=local)
            except subprocess.CalledProcessError:
                pass


def push_to_github(local, repo):
    """Create remote if missing and push."""
    has_origin = True
    try:
        run('git remote get-url origin', cwd=local, capture=True)
    except subprocess.CalledProcessError:
        has_origin = False

    if not has_origin:
        if gh_repo_exists(repo):
            run(['git', 'remote', 'add', 'origin',
                 f'https://github.com/{GH_OWNER}/{repo}.git'], cwd=local)
        else:
            run(['gh', 'repo', 'create', f'{GH_OWNER}/{repo}',
                 '--public', '--source=.', '--remote=origin', '--push'],
                cwd=local)
            return  # already pushed via --push
    # Push current branch to origin (force-with-lease only on rename, not used here)
    branch = run('git rev-parse --abbrev-ref HEAD', cwd=local, capture=True)
    run(['git', 'push', '-u', 'origin', branch], cwd=local)


def materialise_cobol_port():
    """Move chess-revisit-java-toRust-codex/chess-revisit-java-toCOBOL into its
       own SANDBOX folder so we can push it as a separate repo."""
    src = SANDBOX / COBOL_PORT_PARENT / COBOL_PORT_SUBDIR
    dst = SANDBOX / COBOL_PORT_TARGET_DIR
    if not src.is_dir():
        print(f'  cobol-port subfolder {src} not found, skipping')
        return False
    if dst.exists():
        # Already materialised once, leave it
        return True
    print(f'  copying {src} -> {dst}')
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns('.git', 'target'))
    return True


def process_one(local_folder, repo, agent, lang, role, notes, dry_run=False):
    local = SANDBOX / local_folder
    if not local.exists():
        print(f'  SKIP: {local} does not exist')
        return False

    print(f'\n=== {local_folder} -> {repo} ({agent}, {lang}) ===')

    if dry_run:
        print('  (dry-run; no changes)')
        return True

    ensure_files(local, lang, repo, agent, role, notes)
    init_and_commit(local)
    try:
        push_to_github(local, repo)
        return True
    except subprocess.CalledProcessError as e:
        print(f'  push failed: {e}')
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--only', help='process only this repo name')
    args = ap.parse_args()

    results = []  # (status, local, repo, lang, agent)
    for (local, repo, agent, lang, role, notes) in ENGINES:
        if args.only and args.only not in (local, repo):
            continue
        ok = process_one(local, repo, agent, lang, role, notes, args.dry_run)
        results.append(('OK' if ok else 'FAIL', local, repo, lang, agent))

    # Java -> COBOL port (extract from parent folder)
    if not args.only or args.only in (COBOL_PORT_TARGET_DIR, COBOL_PORT_REPO):
        if not args.dry_run:
            ok_extract = materialise_cobol_port()
        else:
            ok_extract = True
        if ok_extract:
            ok = process_one(
                COBOL_PORT_TARGET_DIR, COBOL_PORT_REPO,
                'Codex (GPT-5-codex)', 'COBOL', 'port',
                'translation of chess-java-cc to COBOL, preserving module '
                'structure; this folder was originally a subdirectory of '
                'chess-revisit-java-toRust-codex',
                args.dry_run,
            )
            results.append(('OK' if ok else 'FAIL', COBOL_PORT_TARGET_DIR,
                            COBOL_PORT_REPO, 'COBOL', 'Codex'))

    # Print compilation table
    print('\n\n=== Compilation table ===\n')
    print(f"{'status':<6}  {'engine':<35}  {'github':<55}  {'lang':<25}  {'agent':<35}")
    print('-' * 165)
    for s, local, repo, lang, agent in results:
        print(f'{s:<6}  {local:<35}  github.com/{GH_OWNER}/{repo}  '
              f'{lang:<25}  {agent}')


if __name__ == '__main__':
    main()
