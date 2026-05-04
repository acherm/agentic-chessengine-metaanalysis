"""Load eval2/manifest.yaml without a yaml dependency.

We deliberately avoid PyYAML so the harness works on a stock Python.
The format is restricted: top-level keys `engines:` and `anchors:`,
each followed by a list of `- key: value` records (one per engine).
Strings may be quoted with `""` if empty.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class EngineRecord:
    name: str
    path: str = ""
    tier: str = "B"
    corpus: str = "main"
    build: str = ""
    cmd: str = ""
    image: str = ""
    notes: str = ""
    host_cmd: str = ""   # macOS-native invocation (for Dockerize-impossible engines)
    host_cwd: str = ""   # working directory on host; defaults to `path`
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class AnchorRecord:
    name: str
    image: str = ""
    cmd: str = ""
    ccrl_40_4_elo: int = 0
    notes: str = ""


def _strip_quotes(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'"):
        return s[1:-1]
    return s


def _parse_value(s: str) -> Any:
    s = _strip_quotes(s)
    if s.lower() in ("true", "false"):
        return s.lower() == "true"
    try:
        return int(s)
    except ValueError:
        pass
    return s


def parse(text: str) -> tuple[list[EngineRecord], list[AnchorRecord]]:
    """Tiny YAML-lite parser for eval2/manifest.yaml.

    Recognizes only the subset we use: top-level keys `engines:` and
    `anchors:`, each containing a list of `-` records with two-space
    indented `key: value` lines.
    """
    engines: list[EngineRecord] = []
    anchors: list[AnchorRecord] = []
    section: str | None = None
    cur: dict[str, Any] | None = None

    def flush() -> None:
        nonlocal cur
        if cur is None:
            return
        if section == "engines":
            engines.append(EngineRecord(
                name=cur.get("name", ""),
                path=cur.get("path", ""),
                tier=str(cur.get("tier", "B")),
                corpus=str(cur.get("corpus", "main")),
                build=str(cur.get("build", "")),
                cmd=str(cur.get("cmd", "")),
                image=str(cur.get("image", "")),
                notes=str(cur.get("notes", "")),
                host_cmd=str(cur.get("host_cmd", "")),
                host_cwd=str(cur.get("host_cwd", "")) or str(cur.get("path", "")),
                raw=dict(cur),
            ))
        elif section == "anchors":
            anchors.append(AnchorRecord(
                name=cur.get("name", ""),
                image=str(cur.get("image", "")),
                cmd=str(cur.get("cmd", "")),
                ccrl_40_4_elo=int(cur.get("ccrl_40_4_elo", 0) or 0),
                notes=str(cur.get("notes", "")),
            ))
        cur = None

    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if line in ("engines:", "anchors:"):
            flush()
            section = line[:-1]
            continue
        stripped = line.lstrip()
        if stripped.startswith("- "):
            flush()
            cur = {}
            stripped = stripped[2:].lstrip()
            if ":" in stripped:
                k, _, v = stripped.partition(":")
                cur[k.strip()] = _parse_value(v)
        elif cur is not None and ":" in stripped:
            k, _, v = stripped.partition(":")
            cur[k.strip()] = _parse_value(v)
    flush()
    return engines, anchors


def load(path: str | Path | None = None) -> tuple[list[EngineRecord], list[AnchorRecord]]:
    if path is None:
        path = Path(__file__).resolve().parent.parent / "manifest.yaml"
    return parse(Path(path).read_text(encoding="utf-8"))


def by_name(engines: list[EngineRecord]) -> dict[str, EngineRecord]:
    return {e.name: e for e in engines}
