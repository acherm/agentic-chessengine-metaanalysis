"""UCI handshake check: does the engine respond `uciok` and `readyok`?

Pass criteria:
  - `uciok` within 60 s of sending `uci`
  - `readyok` within 10 s of sending `isready`
  - process exits within 5 s of `quit` (otherwise SIGKILL)

Writes results/per_engine/<name>.preflight.uci.json.
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

RES = Path(__file__).resolve().parent.parent / "results" / "per_engine"
RES.mkdir(parents=True, exist_ok=True)


def run(engine_name: str, mode: str = "docker") -> dict:
    engines, _ = manifest.load()
    eng = manifest.by_name(engines).get(engine_name)
    if eng is None:
        return {"engine": engine_name, "ok": False, "error": "not in manifest"}

    if mode == "host":
        if not eng.host_cmd:
            return {"engine": engine_name, "ok": False,
                    "error": "no host_cmd in manifest"}
        cmd = host_engine.for_engine(eng.host_cmd, eng.host_cwd)
    else:
        cmd = docker_engine.for_engine(eng.image, f"preflight-uci-{engine_name}", tier=eng.tier)
    start = time.time()
    proc = subprocess.Popen(
        shlex.split(cmd),
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, bufsize=1,
    )
    res = {"engine": engine_name, "image": eng.image if mode == "docker" else "host-native",
           "mode": mode, "stages": {}}
    try:
        # uci → uciok
        t0 = time.time()
        proc.stdin.write("uci\n"); proc.stdin.flush()
        uciok = _wait_for(proc, "uciok", timeout=60)
        res["stages"]["uciok"] = {"ok": uciok, "elapsed_s": round(time.time() - t0, 2)}

        # isready → readyok
        t0 = time.time()
        proc.stdin.write("isready\n"); proc.stdin.flush()
        readyok = _wait_for(proc, "readyok", timeout=10)
        res["stages"]["readyok"] = {"ok": readyok, "elapsed_s": round(time.time() - t0, 2)}

        # quit → exit cleanly
        t0 = time.time()
        proc.stdin.write("quit\n"); proc.stdin.flush()
        try:
            proc.wait(timeout=5)
            res["stages"]["quit"] = {"ok": True, "elapsed_s": round(time.time() - t0, 2)}
        except subprocess.TimeoutExpired:
            proc.kill()
            res["stages"]["quit"] = {"ok": False, "elapsed_s": 5.0, "killed": True}

    except Exception as e:
        proc.kill()
        res["error"] = repr(e)
    finally:
        res["total_s"] = round(time.time() - start, 2)

    res["ok"] = all(s.get("ok") for s in res["stages"].values())
    return res


def _wait_for(proc: subprocess.Popen, token: str, timeout: float) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        line = proc.stdout.readline()
        if not line:
            time.sleep(0.05)
            continue
        if token in line:
            return True
    return False


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("engine", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--host", action="store_true",
                    help="use manifest.host_cmd (native macOS) instead of docker image")
    args = ap.parse_args()

    targets: list[str]
    if args.all:
        engines, _ = manifest.load()
        targets = [e.name for e in engines]
    elif args.engine:
        targets = [args.engine]
    else:
        ap.error("pass an engine name or --all")
        return

    mode = "host" if args.host else "docker"
    for name in targets:
        out = run(name, mode=mode)
        suffix = ".preflight.uci.host.json" if args.host else ".preflight.uci.json"
        path = RES / f"{name}{suffix}"
        path.write_text(json.dumps(out, indent=2))
        flag = "PASS" if out.get("ok") else "FAIL"
        print(f"{flag:4} {name} ({mode})  -> {path.name}")


if __name__ == "__main__":
    main()
