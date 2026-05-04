# CounterGo 4.0 — Vadim Chizhov's Go engine. MIT licensed.
# CCRL 40/4 ≈ 2400 Elo. Used as the high anchor.
#
# Build:
#   docker build -t eval2/anchor-countergo40 docker/anchors/countergo/

FROM golang:1.22-bookworm AS build
WORKDIR /src
# NOTE: CounterGo's tag "4.0.0" doesn't exist; the project versions are
# typically not git-tagged. Tracking master; pin to a specific SHA once
# the build is known to work.
RUN git clone --depth 1 https://github.com/ChizhovVadim/CounterGo.git
WORKDIR /src/CounterGo
RUN go build -o /opt/countergo/counter ./cmd/counter \
 || go build -o /opt/countergo/counter .

FROM debian:bookworm-slim
COPY --from=build /opt/countergo/counter /opt/countergo/counter
# CounterGo expects its NNUE net at /root/chess/n-30-5268.nn; ship the
# version shipped with the repo alongside the binary.
COPY --from=build /src/CounterGo/pkg/evalnn/n-30-5268.nn /root/chess/n-30-5268.nn
LABEL eval2.role="anchor" eval2.kind="external" eval2.engine="countergo" eval2.version="4.0" eval2.ccrl_40_4="2400"
ENTRYPOINT ["/opt/countergo/counter"]
