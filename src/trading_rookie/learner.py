from __future__ import annotations

from dataclasses import dataclass, field

from .config import Config
from .ensemble import Ensemble
from .regime import RegimeState


@dataclass
class Learner:
    """The adaptive loop. Observe, update, morph, maybe spawn, then size."""

    config: Config
    equity: float | None = None
    ensemble: Ensemble | None = None
    regime: RegimeState = field(default_factory=RegimeState)
    errors: list[float] = field(default_factory=list)
    journal: list[dict] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.equity is None:
            self.equity = self.config.bankroll
        if self.ensemble is None:
            self.ensemble = Ensemble(self.config)

    def step(self, features: dict[str, float], realized: float | None = None) -> dict:
        feats = dict(features)
        feats["regime"] = self.regime.as_feature()
        label = self.regime.update(feats)
        edge = self.ensemble.propose(feats)
        stake = self.config.stake(self.equity)
        signed_stake = stake * edge  # in [-stake, stake]

        record: dict = {
            "regime": label,
            "edge": edge,
            "stake": signed_stake,
            "equity": self.equity,
            "mode": self.config.mode,
            "weights": self.ensemble.weights(),
        }

        if realized is not None:
            pnl = signed_stake * realized
            self.equity = max(0.0, self.equity + pnl)
            err = abs(edge - realized)
            self.errors.append(err)
            window = self.errors[-50:]
            avg_err = sum(window) / len(window)
            self.ensemble.update(feats, realized, pnl)
            spawned = self.ensemble.maybe_spawn(avg_err)
            record.update(
                {
                    "realized": realized,
                    "pnl": pnl,
                    "equity": self.equity,
                    "avg_abs_error": avg_err,
                    "spawned": spawned.name if spawned else None,
                    "weights": self.ensemble.weights(),
                    "n_sleeves": len(self.ensemble.sleeves),
                }
            )

        self.journal.append(record)
        return record
