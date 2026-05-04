# latex-chess-engine — Tier C. TeXCCChess. Heavy texlive image.
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
      python3 \
      texlive-latex-base texlive-latex-recommended texlive-latex-extra \
      texlive-fonts-recommended texlive-pictures \
    && rm -rf /var/lib/apt/lists/*
COPY src/ /opt/engine/
WORKDIR /opt/engine
LABEL eval2.role="engine" eval2.engine="latex-chess-engine" eval2.tier="C"
ENTRYPOINT ["python3", "-u", "chess-uci.py"]
