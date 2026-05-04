# chess-ruby-cc — Tier B. Needs Ruby >= 3.0.
FROM ruby:3.2-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY src/ /opt/engine/
WORKDIR /opt/engine
RUN if [ -f Gemfile ]; then bundle install --without test development || true; fi
LABEL eval2.role="engine" eval2.engine="chess-ruby-cc" eval2.tier="B"
ENTRYPOINT ["ruby", "bin/ruby-chess"]
