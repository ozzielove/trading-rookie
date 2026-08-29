from __future__ import annotations

import math
from dataclasses import dataclass, field

from .config import Config
from .sleeves import LinearSleeve, Sleeve, default_sleeves


@dataclass
class Ensemble:
    """Bayesian mixture. Weights have a floor. Nothing is killed."""

    config: Config
    sleeves: list[Sleeve] = field(default_factory=list)
    log_weights: list[float] = field(default_factory=list)
    steps_since_spawn: int = 0

    def __post_init__(self) -> None:
        if not self.sleeves:
            self.sleeves = list(default_sleeves())
        if not self.log_weights:
            n = len(self.sleeves)
            self.log_weights = [0.0] * n

    def live_floor(self) -> float:
        n = max(len(self.sleeves), 1)
        # Half the mass is reserved so renormalization cannot zero anyone.
        return min(self.config.min_weight, 0.5 / n)

    def weights(self) -> list[float]:
        raw = [math.exp(x) for x in self.log_weights]
        s = sum(raw) or 1.0
        w = [x / s for x in raw]
        floor = self.live_floor()
        w = [max(floor, x) for x in w]
        s = sum(w)
        return [x / s for x in w]

    def propose(self, features: dict[str, float]) -> float:
        ws = self.weights()
        return float(sum(w * sl.propose(features) for w, sl in zip(ws, self.sleeves)))

    def update(self, features: dict[str, float], realized: float, pnl: float) -> None:
        lr = self.config.learning_rate
        self.steps_since_spawn += 1
        for i, sl in enumerate(self.sleeves):
            pred = sl.propose(features)
            score = -((pred - realized) ** 2)
            self.log_weights[i] += lr * score
            sl.update(features, realized, pnl)
            sl.morph(self.config.morph_rate)
        self._renorm_logs()

    def spawn(self, name: str | None = None) -> LinearSleeve:
        """Add a sleeve. Existing sleeves stay."""
        n = len(self.sleeves)
        sleeve = LinearSleeve(name or f"spawn_{n}")
        self.sleeves.append(sleeve)
        self.log_weights.append(min(self.log_weights) if self.log_weights else 0.0)
        self.steps_since_spawn = 0
        self._renorm_logs()
        return sleeve

    def maybe_spawn(self, avg_abs_error: float) -> LinearSleeve | None:
        if self.steps_since_spawn < 25:
            return None
        if len(self.sleeves) >= 16:
            return None
        if avg_abs_error >= self.config.spawn_error_threshold:
            return self.spawn()
        return None

    def _renorm_logs(self) -> None:
        m = max(self.log_weights)
        self.log_weights = [x - m for x in self.log_weights]

    def snapshot(self) -> dict:
        return {
            "weights": self.weights(),
            "sleeves": [sl.snapshot() for sl in self.sleeves],
        }
