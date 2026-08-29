import pandas as pd
import pytest

from trading_rookie.backtest import BacktestError, walk_forward
from trading_rookie.config import Config
from trading_rookie.simulate import synthetic_history


def test_short_history_fails():
    df = synthetic_history(days=30)
    with pytest.raises(BacktestError, match="180"):
        walk_forward(df, Config(min_history_days=180), fee_bps=1.0, spread_bps=1.0)


def test_missing_costs_fail():
    df = synthetic_history(days=200)
    with pytest.raises(BacktestError):
        walk_forward(df, fee_bps=None, spread_bps=20)  # type: ignore[arg-type]


def test_walk_forward_adapts_and_keeps_sleeves():
    df = synthetic_history(days=200)
    result = walk_forward(df, Config(bankroll=50.0), fee_bps=1.0, spread_bps=1.0)
    assert result.n_sleeves_end >= result.n_sleeves_start
    assert len(result.equity_curve) == len(df)
    assert result.final_equity >= 0
    assert isinstance(result.equity_curve, pd.Series)
