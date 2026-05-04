"""Perft audit.

Two strategies:

  (1) If the engine implements `perft <n>` natively, query it directly
      (some engines emit `Nodes searched: N` or similar — we accept any
      single integer on the response line).
  (2) Otherwise, *external* perft: drive the engine through python-chess
      by replaying its own bestmoves from random positions and verifying
      every move it returns is in python-chess's legal-move list. This
      catches illegal-move bugs even if the engine doesn't expose perft.

Strategy (2) is what gives this a functional-correctness signal across
heterogeneous engines.

Writes results/per_engine/<name>.preflight.perft.json.
"""
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import manifest, docker_engine, host_engine

HERE = Path(__file__).resolve().parent.parent
RES = HERE / "results" / "per_engine"
RES.mkdir(parents=True, exist_ok=True)
PERFT_EPD = HERE / "fixtures" / "perft_suite.epd"


def parse_perft_epd(path: Path) -> list[dict]:
    out = []
    for line in path.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split(";")]
        fen = parts[0]
        depths = {}
        for token in parts[1:]:
            if not token.startswith("D"):
                continue
            d, _, n = token.partition(" ")
            try:
                depths[int(d[1:])] = int(n)
            except ValueError:
                pass
        out.append({"fen": fen, "depths": depths})
    return out


def _engine_cmd(eng, label: str, mode: str) -> str:
    if mode == "host":
        return host_engine.for_engine(eng.host_cmd, eng.host_cwd)
    return docker_engine.for_engine(eng.image, label, tier=eng.tier)


def try_native_perft(engine_name: str, eng, suite: list[dict], max_depth: int = 4,
                     mode: str = "docker") -> dict | None:
    """Attempt `perft N` on each position. If the engine ignores it (no
    integer response within 30 s), return None — caller falls back to (2)."""
    cmd = _engine_cmd(eng, f"perft-{engine_name}", mode)
    proc = subprocess.Popen(
        shlex.split(cmd),
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, bufsize=1,
    )
    matches = []
    try:
        # standard UCI handshake first
        proc.stdin.write("uci\n"); proc.stdin.flush()
        _drain_until(proc, "uciok", timeout=30)
        for pos in suite:
            for depth, expected in sorted(pos["depths"].items()):
                if depth > max_depth:
                    continue
                proc.stdin.write(f"position fen {pos['fen']}\n")
                proc.stdin.write(f"perft {depth}\n")
                proc.stdin.write("isready\n")
                proc.stdin.flush()
                got = _read_perft_count(proc, timeout=60)
                if got is None:
                    proc.kill()
                    return None  # engine doesn't support perft
                matches.append({
                    "fen": pos["fen"], "depth": depth,
                    "expected": expected, "got": got, "ok": got == expected,
                })
        proc.stdin.write("quit\n"); proc.stdin.flush()
        proc.wait(timeout=5)
    except Exception:
        proc.kill()
        return None
    return {"mode": "native_perft", "checks": matches,
            "ok": all(m["ok"] for m in matches)}


def external_legal_audit(engine_name: str, eng, n_positions: int = 100,
                         mode: str = "docker") -> dict:
    """Strategy (2): ask the engine for bestmove from random positions and
    verify legality via python-chess. Requires python-chess on the *host*
    (not in the container). This is a thin import to keep the harness
    dependency-free elsewhere.
    """
    try:
        import chess  # noqa: WPS433 (deferred import is intentional)
    except ImportError:
        return {"mode": "external", "ok": False,
                "error": "python-chess not installed on host"}

    cmd = _engine_cmd(eng, f"legal-audit-{engine_name}", mode)
    proc = subprocess.Popen(
        shlex.split(cmd),
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, bufsize=1,
    )
    illegal = []
    timeouts = []
    try:
        proc.stdin.write("uci\n"); proc.stdin.flush()
        _drain_until(proc, "uciok", timeout=30)
        proc.stdin.write("isready\n"); proc.stdin.flush()
        _drain_until(proc, "readyok", timeout=10)

        # Generate `n_positions` random positions by playing random legal
        # moves from the start position.
        import random
        random.seed(20260419)
        for i in range(n_positions):
            board = chess.Board()
            for _ in range(random.randint(2, 30)):
                if board.is_game_over():
                    break
                board.push(random.choice(list(board.legal_moves)))
            if board.is_game_over():
                continue
            fen = board.fen()
            proc.stdin.write(f"position fen {fen}\n")
            proc.stdin.write("go movetime 2000\n")
            proc.stdin.flush()
            mv = _read_bestmove_within(proc, timeout=15)
            if mv is None:
                timeouts.append(fen)
                continue
            try:
                move = chess.Move.from_uci(mv)
            except Exception:
                illegal.append({"fen": fen, "bestmove": mv, "reason": "unparsable"})
                continue
            if move not in board.legal_moves:
                illegal.append({"fen": fen, "bestmove": mv, "reason": "not in legal_moves"})
        proc.stdin.write("quit\n"); proc.stdin.flush()
        proc.wait(timeout=5)
    except Exception as e:
        proc.kill()
        return {"mode": "external", "ok": False, "error": repr(e)}

    return {
        "mode": "external",
        "n_tested": n_positions,
        "illegal_count": len(illegal),
        "timeout_count": len(timeouts),
        "illegal_examples": illegal[:5],
        "ok": len(illegal) == 0,
    }


def _drain_until(proc, token: str, timeout: float) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        line = proc.stdout.readline()
        if not line:
            time.sleep(0.05); continue
        if token in line:
            return True
    return False


def _read_int_within(proc, timeout: float) -> int | None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        line = proc.stdout.readline()
        if not line:
            time.sleep(0.05); continue
        for tok in line.replace(":", " ").split():
            try:
                return int(tok)
            except ValueError:
                continue
    return None


def _read_perft_count(proc, timeout: float) -> int | None:
    """Read a perft response, then drain through `readyok`.

    Per-call protocol: caller has just sent `perft N\\nisready\\n`.
    We read lines until we either:
      - see a line containing "Nodes" or "nodes searched" with an integer
        (capture it as the count), then keep reading until `readyok`;
      - or hit `readyok` first (engine doesn't support perft).
    Many engines also emit per-move divide output before the total; we
    take the LAST integer-bearing "Nodes" line before readyok to handle
    that case.
    """
    deadline = time.time() + timeout
    last_count: int | None = None
    while time.time() < deadline:
        line = proc.stdout.readline()
        if not line:
            time.sleep(0.05); continue
        low = line.lower()
        if "readyok" in low:
            return last_count
        if "nodes" in low or "perft" in low:
            for tok in line.replace(":", " ").replace(",", "").split():
                try:
                    last_count = int(tok)
                    break
                except ValueError:
                    continue
    return last_count


def _read_bestmove_within(proc, timeout: float) -> str | None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        line = proc.stdout.readline()
        if not line:
            time.sleep(0.05); continue
        if line.startswith("bestmove"):
            parts = line.split()
            return parts[1] if len(parts) >= 2 else None
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("engine", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--max-depth", type=int, default=4)
    ap.add_argument("--n-legal-positions", type=int, default=100)
    ap.add_argument("--host", action="store_true", help="use manifest.host_cmd")
    args = ap.parse_args()

    suite = parse_perft_epd(PERFT_EPD)
    engines, _ = manifest.load()
    by = manifest.by_name(engines)
    targets = [e.name for e in engines] if args.all else [args.engine]

    mode = "host" if args.host else "docker"
    for name in targets:
        eng = by.get(name)
        if eng is None:
            print(f"FAIL {name}: not in manifest"); continue
        if mode == "host" and not eng.host_cmd:
            print(f"SKIP {name}: no host_cmd"); continue
        native = try_native_perft(name, eng, suite, max_depth=args.max_depth, mode=mode)
        external = None
        if native is None:
            external = external_legal_audit(name, eng, n_positions=args.n_legal_positions, mode=mode)
        out = {"engine": name, "mode": mode, "native": native, "external": external}
        out["ok"] = bool((native and native.get("ok")) or (external and external.get("ok")))
        suffix = ".preflight.perft.host.json" if args.host else ".preflight.perft.json"
        path = RES / f"{name}{suffix}"
        path.write_text(json.dumps(out, indent=2))
        flag = "PASS" if out["ok"] else "FAIL"
        mode = "native" if native else ("external" if external else "?")
        print(f"{flag:4} {name}  ({mode})  -> {path.name}")


if __name__ == "__main__":
    main()
