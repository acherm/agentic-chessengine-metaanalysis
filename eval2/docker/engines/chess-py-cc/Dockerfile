# chess-py-cc — Tier B, CC Python engine.
FROM python:3.11-slim
COPY src/ /opt/engine/
WORKDIR /opt/engine
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi
LABEL eval2.role="engine" eval2.engine="chess-py-cc" eval2.tier="B"
# Repo's UCI entry is a top-level main.py that imports the `engine` package;
# the manifest's `python3 -m chess_engine` was incorrect.
ENTRYPOINT ["python3", "-u", "main.py"]
