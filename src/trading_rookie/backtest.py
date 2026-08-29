from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .config import Config
from .learner import Learner


class BacktestError(ValueError):
    pass


@dataclass
class WalkForwardResult:
    equity_curve: pd.Series
    journal: list[dict]
    n_sleeves_start: int
    n_sleeves_end: int
    final_equity: float

    @property
    def total_return(self) -> float:
        start = float(self.equity_curve.iloc[0])
        if start == 0:
            return 0.0
        return float(self.equity_curve.iloc[-1] / start - 1.0)


def walk_forward(
    df: pd.DataFrame,
    config: Config | None = None,
    fee_bps: float = 10.0,
    spread_bps: float = 20.0,
) -> WalkForwardResult:
    """Expanding-window replay. Costs are required. No fabricated PnL."""
    if config is None:
        config = Config()
    if fee_bps is None or spread_bps is None:
        raise BacktestError("fee_bps and spread_bps are required")
    if df is None or df.empty:
        raise BacktestError("history is missing")

    if "ts" in df.columns:
        span_days = (pd.to_datetime(df["ts"]).max() - pd.to_datetime(df["ts"]).min()).days
    else:
        span_days = len(df)
    if span_days < config.min_history_days:
        raise BacktestError(
            f"need at least {config.min_history_days} days of history, got ~{span_days}"
        )

    required = {"realized"}
    missing = required - set(df.columns)
    if missing:
        raise BacktestError(f"missing columns: {sorted(missing)}")

    learner = Learner(config)
    n0 = len(learner.ensemble.sleeves)
    cost = (fee_bps + spread_bps) / 1e4
    equities = []

    for row in df.itertuples(index=False):
        features = {
            "edge": float(getattr(row, "edge", 0.0)),
            "momentum": float(getattr(row, "momentum", 0.0)),
            "liquidity": float(getattr(row, "liquidity", 0.5)),
            "event": float(getattr(row, "event", 0.0)),
        }
        realized = float(row.realized)
        rec = learner.step(features, realized=realized)
        # apply costs on notional
        learner.equity -= abs(rec["stake"]) * cost
        learner.equity = max(0.0, learner.equity)
        equities.append(learner.equity)

    curve = pd.Series(equities, name="equity")
    return WalkForwardResult(
        equity_curve=curve,
        journal=learner.journal,
        n_sleeves_start=n0,
        n_sleeves_end=len(learner.ensemble.sleeves),
        final_equity=float(learner.equity),
    )
