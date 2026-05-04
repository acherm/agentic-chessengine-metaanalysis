"""Tactical EPD runner.

Plays through an EPD file (WAC, mate-in-N, etc.). For each position we
send `position fen ...` followed by `go movetime <ms>` and read the
bestmove. If the bestmove matches `bm`, we count it solved.

Reports % solved and average time per position.

Writes results/per_engine/<name>.preflight.tactics.json.
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


def parse_epd(path: Path) -> list[dict]:
    out = []
    for line in path.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        # Split on `;` to separate FEN+ops from id/etc.
        head, *ops_raw = [s.strip() for s in line.split(";")]
        # head is "FEN... bm <move>"
        if " bm " not in head:
            continue
        fen, _, bm = head.rpartition(" bm ")
        ident = next((s.split('"')[1] for s in ops_raw if s.startswith("id ")), "")
        out.append({"fen": fen.strip(), "bm": bm.strip(), "id": ident})
    return out


def run(engine_name: str, epd: Path, movetime_ms: int, limit: int | None,
        mode: str = "docker") -> dict:
    engines, _ = manifest.load()
    eng = manifest.by_name(engines).get(engine_name)
    if eng is None:
        return {"engine": engine_name, "ok": False, "error": "not in manifest"}

    positions = parse_epd(epd)
    if limit:
        positions = positions[:limit]

    if mode == "host":
        if not eng.host_cmd:
            return {"engine": engine_name, "ok": False, "error": "no host_cmd"}
        cmd = host_engine.for_engine(eng.host_cmd, eng.host_cwd)
    else:
        cmd = docker_engine.for_engine(eng.image, f"tactics-{engine_name}", tier=eng.tier)
    proc = subprocess.Popen(
        shlex.split(cmd),
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, bufsize=1,
    )

    try:
        import chess  # for SAN→UCI normalisation when comparing
    except ImportError:
        chess = None  # we'll fall back to literal compare; less accurate

    results = []
    try:
        proc.stdin.write("uci\n"); proc.stdin.flush()
        _drain_until(proc, "uciok", timeout=30)
        proc.stdin.write("isready\n"); proc.stdin.flush()
        _drain_until(proc, "readyok", timeout=10)

        for pos in positions:
            t0 = time.time()
            proc.stdin.write(f"position fen {pos['fen']}\n")
            proc.stdin.write(f"go movetime {movetime_ms}\n")
            proc.stdin.flush()
            mv = _read_bestmove_within(proc, timeout=movetime_ms / 1000.0 + 10)
            elapsed = time.time() - t0
            ok = _matches(pos["fen"], pos["bm"], mv, chess)
            results.append({"id": pos["id"], "fen": pos["fen"],
                            "bm": pos["bm"], "got": mv, "ok": ok,
                            "elapsed_s": round(elapsed, 2)})
        proc.stdin.write("quit\n"); proc.stdin.flush()
        proc.wait(timeout=5)
    except Exception as e:
        proc.kill()
        return {"engine": engine_name, "error": repr(e), "results": results}

    n = len(results)
    solved = sum(1 for r in results if r["ok"])
    return {
        "engine": engine_name, "epd": str(epd.name),
        "movetime_ms": movetime_ms,
        "n": n, "solved": solved,
        "pct_solved": round(100 * solved / n, 1) if n else 0.0,
        "results": results,
    }


def _matches(fen: str, bm: str, got: str | None, chess_mod) -> bool:
    if got is None:
        return False
    if bm == got:
        return True
    if chess_mod is None:
        return False
    try:
        board = chess_mod.Board(fen)
        bm_move = board.parse_san(bm)
        return bm_move.uci() == got
    except Exception:
        return False


def _drain_until(proc, token: str, timeout: float) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        line = proc.stdout.readline()
        if not line:
            time.sleep(0.05); continue
        if token in line:
            return True
    return False


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
    ap.add_argument("--epd", default=str(HERE / "fixtures" / "wac100.epd"))
    ap.add_argument("--movetime-ms", type=int, default=5000)
    ap.add_argument("--limit", type=int, default=None,
                    help="cap N positions (default: all in file)")
    ap.add_argument("--host", action="store_true")
    args = ap.parse_args()

    engines, _ = manifest.load()
    targets = [e.name for e in engines] if args.all else [args.engine]
    mode = "host" if args.host else "docker"
    for name in targets:
        out = run(name, Path(args.epd), args.movetime_ms, args.limit, mode=mode)
        out["mode"] = mode
        suffix = ".preflight.tactics.host.json" if args.host else ".preflight.tactics.json"
        path = RES / f"{name}{suffix}"
        path.write_text(json.dumps(out, indent=2))
        pct = out.get("pct_solved", "?")
        print(f"  {name}  {pct}% solved -> {path.name}")


if __name__ == "__main__":
    main()
