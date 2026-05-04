# chess-latex-codex-replication — Tier C, LaTeX-spawning Python wrapper.
# Heaviest base image in the corpus because we need a working pdflatex.

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
      python3 python3-pip \
      texlive-latex-base texlive-latex-recommended \
      texlive-fonts-recommended texlive-pictures \
      texlive-latex-extra \
    && rm -rf /var/lib/apt/lists/*

COPY src/ /opt/engine/
WORKDIR /opt/engine

# Engine spawns pdflatex per move. No build step.
LABEL eval2.role="engine" eval2.engine="chess-latex-codex-replication" eval2.tier="C"
ENTRYPOINT ["python3", "engine/latex_uci_engine.py"]
