from __future__ import annotations

import argparse

import numpy as np
import pandas as pd

from .backtest import walk_forward
from .config import Config


def synthetic_history(days: int = 365, seed: int = 7) -> pd.DataFrame:
    """Placeholder path only. Real venue data must replace this before any live talk."""
    rng = np.random.default_rng(seed)
    n = days
    momentum = rng.normal(0, 0.3, n).cumsum()
    momentum = np.tanh(momentum / 5)
    edge = 0.15 * momentum + rng.normal(0, 0.4, n)
    realized = np.tanh(edge + rng.normal(0, 0.35, n))
    return pd.DataFrame(
        {
            "ts": pd.date_range("2025-01-01", periods=n, freq="D"),
            "edge": edge,
            "momentum": momentum,
            "liquidity": rng.uniform(0.2, 1.0, n),
            "event": (rng.random(n) > 0.92).astype(float),
            "realized": realized,
        }
    )


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="trading_rookie")
    p.add_argument("cmd", nargs="?", default="simulate", choices=["simulate"])
    p.add_argument("--days", type=int, default=365)
    args = p.parse_args(argv)

    cfg = Config()
    if cfg.mode != "paper":
        raise SystemExit("refusing to run: mode is not paper")

    df = synthetic_history(days=max(args.days, cfg.min_history_days))
    result = walk_forward(df, cfg, fee_bps=1.0, spread_bps=1.0)
    print("mode=paper synthetic wiring test. costs are placeholders not Kalshi fees. not a claim of edge")
    print(f"start_equity={cfg.bankroll:.2f}")
    print(f"final_equity={result.final_equity:.2f}")
    print(f"total_return={result.total_return:.2%}")
    print(f"sleeves {result.n_sleeves_start} -> {result.n_sleeves_end}")
    print("replace synthetic_history with venue data before trusting this.")


if __name__ == "__main__":
    main()
