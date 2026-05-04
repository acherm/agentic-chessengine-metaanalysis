# chess-py — Tier B, Codex Python engine.
FROM python:3.11-slim
COPY src/ /opt/engine/
WORKDIR /opt/engine
# If the engine ships a requirements.txt, install it. Otherwise no deps.
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi
LABEL eval2.role="engine" eval2.engine="chess-py" eval2.tier="B"
ENTRYPOINT ["python3", "-u", "-m", "chesspy"]
