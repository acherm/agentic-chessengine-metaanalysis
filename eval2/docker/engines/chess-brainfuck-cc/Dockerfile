# chess-brainfuck-cc — Tier C.
FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY src/ /opt/engine/
WORKDIR /opt/engine
RUN make || true
LABEL eval2.role="engine" eval2.engine="chess-brainfuck-cc" eval2.tier="C"
ENTRYPOINT ["python3", "-u", "bf_uci.py"]
