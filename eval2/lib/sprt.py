"""Sequential Probability Ratio Test (SPRT) for early-stopping a match.

Given two engines whose true Elo difference d is unknown, we want to
test  H0: d = elo0  against  H1: d = elo1.  After each game we update
the log-likelihood ratio (LLR); we stop when it crosses an acceptance
or rejection threshold.

Bayes-elo (Kahan) form is overkill here; we use the standard
Wald boundaries:

    A = log( (1 - beta) / alpha )       # accept H1 (engine A stronger)
    B = log( beta / (1 - alpha) )       # accept H0 (no improvement)

For each game outcome (W/D/L) we compute the win/draw/loss
probabilities under both hypotheses (Elo logistic) and accumulate
log p1 - log p0.

This is the same form fishtest uses; it's the standard early-stop for
SF-vs-SF match testing.
"""
from __future__ import annotations

import math
from dataclasses import dataclass


def _logistic_probs(elo: float, draw_elo: float = 100.0) -> tuple[float, float, float]:
    """Return (P_win, P_draw, P_loss) under BayesElo with given draw_elo."""
    s = 1.0 / (1.0 + 10 ** (-elo / 400.0))
    # Reduce to W/D/L using a draw-elo nuisance parameter (BayesElo).
    pw = s * (1.0 - 1.0 / (1.0 + 10 ** (-draw_elo / 400.0)))
    pl = (1.0 - s) * (1.0 - 1.0 / (1.0 + 10 ** (-draw_elo / 400.0)))
    pd = max(1.0 - pw - pl, 1e-9)
    return max(pw, 1e-9), pd, max(pl, 1e-9)


@dataclass
class SPRTState:
    elo0: float
    elo1: float
    alpha: float = 0.05
    beta: float = 0.05
    draw_elo: float = 100.0
    llr: float = 0.0
    wins: int = 0
    draws: int = 0
    losses: int = 0

    @property
    def upper(self) -> float:
        return math.log((1.0 - self.beta) / self.alpha)

    @property
    def lower(self) -> float:
        return math.log(self.beta / (1.0 - self.alpha))

    def update(self, result: str) -> None:
        """result is one of 'W', 'D', 'L' from the perspective of engine A."""
        pw0, pd0, pl0 = _logistic_probs(self.elo0, self.draw_elo)
        pw1, pd1, pl1 = _logistic_probs(self.elo1, self.draw_elo)
        if result == "W":
            self.wins += 1
            self.llr += math.log(pw1 / pw0)
        elif result == "D":
            self.draws += 1
            self.llr += math.log(pd1 / pd0)
        elif result == "L":
            self.losses += 1
            self.llr += math.log(pl1 / pl0)
        else:
            raise ValueError(f"unknown result {result!r}")

    def decision(self) -> str | None:
        if self.llr >= self.upper:
            return "H1"   # engine A is at least elo1 stronger
        if self.llr <= self.lower:
            return "H0"   # engine A is no better than elo0
        return None

    def games(self) -> int:
        return self.wins + self.draws + self.losses
