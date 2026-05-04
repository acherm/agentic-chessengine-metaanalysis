# chess-brainfuck — Tier C. Brainfuck engine driven by Python wrapper.
FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY src/ /opt/engine/
WORKDIR /opt/engine
RUN make || true   # not all versions of this engine ship a Makefile
LABEL eval2.role="engine" eval2.engine="chess-brainfuck" eval2.tier="C"
ENTRYPOINT ["python3", "-u", "src/bf_uci_engine.py"]
