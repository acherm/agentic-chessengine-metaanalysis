# chess-sql — Tier C. SQL+Python hybrid (SQLite-backed).
FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends sqlite3 \
    && rm -rf /var/lib/apt/lists/*
COPY src/ /opt/engine/
WORKDIR /opt/engine
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi
LABEL eval2.role="engine" eval2.engine="chess-sql" eval2.tier="C"
ENTRYPOINT ["python3", "-u", "uci_wrapper.py"]
