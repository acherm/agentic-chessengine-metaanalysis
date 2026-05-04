"""Host-native engine invocation (fallback for engines that can't be Dockerized).

For engines whose toolchain doesn't exist on Linux (macOS-only assembly
syntax, commercial runtimes, fragile source builds), we fall back to
running them directly on the host. The rest of the harness is unchanged:
same cutechess-cli driver, same Stockfish-in-Docker opponent, same
fixtures, same SPRT and scoring logic.

The `host_cmd` is composed as `bash -c 'cd <cwd> && <cmd>'` so cutechess
can pass it as a single `cmd=` argument — it has to be a single shell
word/command.
"""
from __future__ import annotations

import shlex
from pathlib import Path


def for_engine(host_cmd: str, host_cwd: str | Path, label: str = "") -> str:
    """Return a cutechess `cmd=` string that launches the engine on host.

    Uses `bash -lc` so login-shell env (brew path, opam switch, etc.) is
    picked up. The engine must be idempotent to multiple launches — each
    game spawns a fresh process.
    """
    cwd = str(host_cwd)
    # Quote everything; `bash -lc` gets a single string to eval.
    inner = f"cd {shlex.quote(cwd)} && exec {host_cmd}"
    return f"bash -lc {shlex.quote(inner)}"
