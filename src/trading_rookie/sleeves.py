from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

import numpy as np


class Sleeve(Protocol):
    name: str

    def propose(self, features: dict[str, float]) -> float:
        """Signed edge in [-1, 1]. Positive = long / Yes."""

    def update(self, features: dict[str, float], realized: float, pnl: float) -> None:
        """Online update. Must not remove the sleeve."""

    def morph(self, rate: float) -> None:
        """Change internal form. Identity (name) stays."""

    def snapshot(self) -> dict:
        ...


def _clip(x: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return float(np.clip(x, lo, hi))


@dataclass
class LinearSleeve:
    """Adaptive linear hypothesis. Weights drift; the sleeve stays."""

    name: str
    keys: tuple[str, ...] = ("edge", "momentum", "liquidity", "regime")
    weights: dict[str, float] = field(default_factory=dict)
    bias: float = 0.0
    n_updates: int = 0

    def __post_init__(self) -> None:
        if not self.weights:
            self.weights = {k: 0.0 for k in self.keys}

    def propose(self, features: dict[str, float]) -> float:
        s = self.bias
        for k, w in self.weights.items():
            s += w * float(features.get(k, 0.0))
        return _clip(np.tanh(s))

    def update(self, features: dict[str, float], realized: float, pnl: float) -> None:
        pred = self.propose(features)
        err = realized - pred
        lr = 0.05 / (1.0 + 0.001 * self.n_updates)
        self.bias += lr * err
        for k in self.weights:
            self.weights[k] += lr * err * float(features.get(k, 0.0))
        self.n_updates += 1

    def morph(self, rate: float) -> None:
        # Polymorphic: rotate emphasis toward recently useful features.
        vals = np.array(list(self.weights.values()), dtype=float)
        if vals.std() < 1e-9:
            noise = np.random.normal(0, rate, size=vals.shape)
            vals = vals + noise
        else:
            vals = (1 - rate) * vals + rate * (vals - vals.mean())
        for k, v in zip(self.weights, vals):
            self.weights[k] = float(v)
        self.n_updates += 1

    def snapshot(self) -> dict:
        return {
            "name": self.name,
            "bias": self.bias,
            "weights": dict(self.weights),
            "n_updates": self.n_updates,
        }


def default_sleeves() -> list[LinearSleeve]:
    return [
        LinearSleeve("value"),
        LinearSleeve("momentum"),
        LinearSleeve("liquidity_maker"),
        LinearSleeve("event_drift"),
    ]
