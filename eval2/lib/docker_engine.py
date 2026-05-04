"""Compose `docker run` commands that cutechess-cli can call as UCI engines.

Cutechess-cli launches an engine as a single command line. We wrap each
engine in `docker run --rm -i ...` so:

  - the engine's binaries and runtime are isolated (reproducibility);
  - resource caps are enforced (--cpus, --memory);
  - SIGTERM kills the whole container (no leaked grandchildren);
  - we can audit which exact image SHA produced each result.

The container image's ENTRYPOINT must speak UCI on stdin/stdout.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DockerSpec:
    image: str
    cpus: float = 1.0
    memory: str = "512m"
    name_prefix: str = "eval2"
    extra_args: tuple[str, ...] = ()
    pids_limit: int = 256

    def cmd(self, run_label: str) -> str:
        # `--init` reaps zombies; -i keeps stdin open for UCI; --rm cleans up.
        # --network=none keeps engines from phoning home or downloading
        # opening books at runtime.
        # Container name embeds the run label so concurrent runs don't collide.
        safe = run_label.replace("/", "_").replace(" ", "_")[:60]
        parts = [
            "docker", "run", "--rm", "-i", "--init",
            "--network=none",
            f"--cpus={self.cpus}",
            f"--memory={self.memory}",
            f"--pids-limit={self.pids_limit}",
            f"--name={self.name_prefix}-{safe}",
        ]
        parts.extend(self.extra_args)
        parts.append(self.image)
        return " ".join(parts)


def for_engine(image: str, label: str, *, cpus: float = 1.0, memory: str = "512m",
               tier: str = "B") -> str:
    """Return the cutechess `cmd=` string for a manifest engine."""
    # Tier C engines need more memory (LaTeX/Brainfuck interpreters bloat).
    if tier == "C":
        memory = "1024m"
    return DockerSpec(image=image, cpus=cpus, memory=memory).cmd(label)


def for_stockfish(image: str, uci_elo: int, label: str) -> str:
    return DockerSpec(image=image, cpus=1.0, memory="512m").cmd(f"sf{uci_elo}-{label}")


def for_anchor(image: str, label: str) -> str:
    return DockerSpec(image=image, cpus=1.0, memory="512m").cmd(label)
