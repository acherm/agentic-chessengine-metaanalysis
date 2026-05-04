# chess-ruby-codex — Tier B.
FROM ruby:3.2-slim
COPY src/ /opt/engine/
WORKDIR /opt/engine
RUN if [ -f Gemfile ]; then bundle install --without test development || true; fi
LABEL eval2.role="engine" eval2.engine="chess-ruby-codex" eval2.tier="B"
ENTRYPOINT ["ruby", "bin/ruby_chess_engine"]
