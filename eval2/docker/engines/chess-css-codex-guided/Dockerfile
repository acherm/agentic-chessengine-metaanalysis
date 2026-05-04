# chess-css-codex-guided — Tier B. Small CSS+JS experiment.
FROM node:20-slim
COPY src/ /opt/engine/
WORKDIR /opt/engine
RUN if [ -f package.json ]; then npm ci --omit=dev || npm install --omit=dev; fi
LABEL eval2.role="engine" eval2.engine="chess-css-codex-guided" eval2.tier="B"
ENTRYPOINT ["node", "engine.js"]
