# MadChess 3.2 — Erik Madsen's .NET engine. MIT licensed.
# CCRL 40/4 ≈ 2200 Elo. Used as the mid anchor.
#
# Build:
#   docker build -t eval2/anchor-madchess32 docker/anchors/madchess/

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
# NOTE: MadChess git tags don't follow a "v3.2" convention; tracking master
# for now. Pin to a specific commit SHA once we know the build works.
RUN git clone --depth 1 https://github.com/ErikMadsen/MadChess.git
WORKDIR /src/MadChess
RUN dotnet publish -c Release -o /opt/madchess \
    $(find . -name 'MadChess.Engine.csproj' -o -name 'MadChess*Engine.csproj' | head -1)

FROM mcr.microsoft.com/dotnet/runtime:8.0
COPY --from=build /opt/madchess /opt/madchess
LABEL eval2.role="anchor" eval2.kind="external" eval2.engine="madchess" eval2.version="3.2" eval2.ccrl_40_4="2200"
ENTRYPOINT ["dotnet", "/opt/madchess/MadChess.Engine.dll"]
