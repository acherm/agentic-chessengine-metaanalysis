"""Q5 — nodes-per-second (NPS) bench across engines + Rustic + COBOL + SF.

For each engine, send `position startpos`, `go movetime 5000`, parse
the engine's UCI `info` lines for `nps` and `nodes`. Take the
final/highest-depth `info` line.

Comparison set:
  - top corpus engines (chess-rust-cc, chess-cplusplus-claude, chess-java-cc, …)
  - Rustic 1820 (mid-anchor reference)
  - COBOL-chess (slow-language reference)
  - Stockfish 18 (top reference)

Output: results/nps_bench.md
"""
from __future__ import annotations

import json
import re
import shlex
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "lib"))
import manifest, docker_engine

INFO_RE = re.compile(r'\binfo\b.*?\bdepth\s+(\d+).*?\bnodes\s+(\d+).*?\bnps\s+(\d+)')


def bench_one(cmd: str, label: str, movetime_ms: int = 5000) -> dict:
    """Run `position startpos; go movetime N` and parse last info line."""
    t0 = time.time()
    proc = subprocess.Popen(shlex.split(cmd),
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, bufsize=1)
    last = None
    try:
        proc.stdin.write("uci\n"); proc.stdin.flush()
        # drain until uciok
        deadline = time.time() + 30
        while time.time() < deadline:
            line = proc.stdout.readline()
            if not line: time.sleep(0.05); continue
            if "uciok" in line: break
        proc.stdin.write("isready\n"); proc.stdin.flush()
        deadline = time.time() + 10
        while time.time() < deadline:
            line = proc.stdout.readline()
            if not line: time.sleep(0.05); continue
            if "readyok" in line: break
        proc.stdin.write("position startpos\n")
        proc.stdin.write(f"go movetime {movetime_ms}\n")
        proc.stdin.flush()
        deadline = time.time() + (movetime_ms / 1000) + 30
        while time.time() < deadline:
            line = proc.stdout.readline()
            if not line: time.sleep(0.05); continue
            line = line.strip()
            m = INFO_RE.search(line)
            if m:
                last = {"depth": int(m.group(1)),
                        "nodes": int(m.group(2)),
                        "nps": int(m.group(3))}
            if line.startswith("bestmove"):
                break
        proc.stdin.write("quit\n"); proc.stdin.flush()
        try: proc.wait(timeout=5)
        except subprocess.TimeoutExpired: proc.kill()
    except Exception as e:
        proc.kill()
        return {"label": label, "error": repr(e), "elapsed_s": round(time.time() - t0, 1)}
    return {"label": label, **(last or {}), "elapsed_s": round(time.time() - t0, 1)}


def main() -> None:
    engs, anchors = manifest.load()
    by = manifest.by_name(engs)

    # Engines to bench: top tier + slow-language + 2 anchors + SF.
    plan = [
        ("chess-rust-cc",          docker_engine.for_engine("eval2/chess-rust-cc:latest", "bench-rust-cc", tier="A")),
        ("chess-rust-cc-redo",     docker_engine.for_engine("eval2/chess-rust-cc-redo:latest", "bench-rust-cc-redo", tier="A")),
        ("chess-cplusplus-claude", docker_engine.for_engine("eval2/chess-cplusplus-claude:latest", "bench-cpp-claude", tier="A")),
        ("cplusplus-chess",        docker_engine.for_engine("eval2/cplusplus-chess:latest", "bench-cpp-codex", tier="A")),
        ("chess-purec",            docker_engine.for_engine("eval2/chess-purec:latest", "bench-purec", tier="A")),
        ("chess-java-cc",          docker_engine.for_engine("eval2/chess-java-cc:latest", "bench-java-cc", tier="B")),
        ("chess-rust-codex",       docker_engine.for_engine("eval2/chess-rust-codex:latest", "bench-rust-codex", tier="A")),
        ("chess-py",               docker_engine.for_engine("eval2/chess-py:latest", "bench-py", tier="B")),
        ("chess-ruby-cc",          docker_engine.for_engine("eval2/chess-ruby-cc:latest", "bench-ruby-cc", tier="B")),
        ("COBOL-chess",            docker_engine.for_engine("eval2/cobol-chess:latest", "bench-cobol", tier="B")),
        # references
        ("rustic (1820)",          docker_engine.for_engine("eval2/anchor-rustic:latest", "bench-rustic", tier="A")),
        ("asymptote (2150)",       docker_engine.for_engine("eval2/anchor-asymptote:latest", "bench-asymptote", tier="A")),
        ("Stockfish 18",           docker_engine.for_engine("eval2/stockfish:18", "bench-sf18", tier="A")),
    ]

    results = []
    for label, cmd in plan:
        print(f"  benching {label}...", file=sys.stderr, flush=True)
        r = bench_one(cmd, label, movetime_ms=5000)
        results.append(r)

    # Sort by nps desc
    results.sort(key=lambda r: -(r.get("nps") or 0))

    out_path = HERE / "results" / "nps_bench.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sf_nps = next((r["nps"] for r in results if "Stockfish" in r["label"] and r.get("nps")), None)
    rustic_nps = next((r["nps"] for r in results if "rustic" in r["label"] and r.get("nps")), None)
    cobol_nps = next((r["nps"] for r in results if "COBOL" in r["label"] and r.get("nps")), None)

    lines = ["# NPS / search throughput bench (Q5)", "",
             "Each engine is given `go movetime 5000` from startpos. We capture the",
             "last `info nodes N nps M` line emitted, plus the depth reached.",
             "",
             "Reference points:",
             f"- Stockfish 18: {sf_nps:,} nps" if sf_nps else "- Stockfish 18: (no data)",
             f"- Rustic Alpha 3.0.4 (CCRL 1820): {rustic_nps:,} nps" if rustic_nps else "- Rustic: (no data)",
             f"- COBOL-chess (slow language): {cobol_nps:,} nps" if cobol_nps else "- COBOL-chess: (no data)",
             "",
             "| Engine | Depth reached | Nodes | NPS | vs Rustic | vs SF18 |",
             "|---|---:|---:|---:|---:|---:|"]
    for r in results:
        if "nps" not in r:
            lines.append(f"| {r['label']} | — | — | — | — | — |")
            continue
        nps = r["nps"]
        vsr = f"{nps/rustic_nps:.2f}×" if rustic_nps else "—"
        vssf = f"{nps/sf_nps*100:.1f}%" if sf_nps else "—"
        lines.append(f"| {r['label']} | {r.get('depth','?')} | {r.get('nodes','?'):,} | {nps:,} | {vsr} | {vssf} |")
    out_path.write_text("\n".join(lines) + "\n")
    print(f"wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
