from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RegimeState:
    """Online regime tracker. Adaptation target, not a static label."""

    vol_ewma: float = 0.0
    liq_ewma: float = 0.0
    event_ewma: float = 0.0
    alpha: float = 0.15
    history: list[str] = field(default_factory=list)

    def update(self, features: dict[str, float]) -> str:
        vol = abs(float(features.get("momentum", 0.0)))
        liq = float(features.get("liquidity", 0.0))
        ev = abs(float(features.get("event", features.get("regime", 0.0))))
        a = self.alpha
        self.vol_ewma = (1 - a) * self.vol_ewma + a * vol
        self.liq_ewma = (1 - a) * self.liq_ewma + a * liq
        self.event_ewma = (1 - a) * self.event_ewma + a * ev
        label = self.label()
        self.history.append(label)
        return label

    def label(self) -> str:
        if self.event_ewma > 0.6:
            return "event"
        if self.vol_ewma > 0.5:
            return "stress"
        if self.liq_ewma < 0.2:
            return "thin"
        return "quiet"

    def as_feature(self) -> float:
        return {
            "quiet": 0.0,
            "thin": 0.33,
            "stress": 0.66,
            "event": 1.0,
        }[self.label()]
