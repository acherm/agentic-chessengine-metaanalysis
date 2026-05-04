# chess-css-codex — Tier B. Evasion-risk: uses python-chess inside
# src/chess_css/engine.py. The strict-css/ subdirectory is the user-
# requested compliant variant; if present, prefer it.
#
# We install python-chess to keep the engine runnable. The novelty
# audit (in reports/CONSISTENCY.md) is what flags it as evasion.
FROM python:3.11-slim
RUN pip install --no-cache-dir chess==1.10.0
COPY src/ /opt/engine/
WORKDIR /opt/engine
LABEL eval2.role="engine" eval2.engine="chess-css-codex" eval2.tier="B" \
      eval2.flag="evasion-risk-uses-python-chess"
ENTRYPOINT ["python3", "-u", "src/chess_css/uci.py"]
