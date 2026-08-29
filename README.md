# Trading Rookie

Paper-first, fully adaptive trading system. Starting bankroll $50. Risk per trade is 1% of equity.

This is not a frozen strategy. It is an ensemble of sleeves that keep living. They reweight, retune, and change shape as evidence comes in. Losers do not get deleted. They shrink and keep learning.

Live trading is off by default. Do not turn it on until a walk-forward backtest of at least 6 months (12 preferred) survives fees, spread, and the 1% cap.

## What it is not

- A "$6k/day AI bot" clone
- A genetic kill-or-clone farm (winners copy, losers die)
- A sandstone backtest you deploy once and pray

## Adaptive loop

Every resolved market / bar:

1. **Observe** — fills, marks, fees, regime features
2. **Update beliefs** — Bayesian sleeve weights, never zeroed out
3. **Retune** — constrained parameter drift per sleeve (polymorphic form)
4. **Spawn** — if residual error is structured, add a new sleeve. Old sleeves stay.
5. **Size** — 1% of current equity, split by posterior weights
6. **Record** — everything needed to audit why it changed

Walk-forward is the test: train on expanding history, trade the next window, repeat. A sleeve that worked in 2024 and failed in 2025 should lose weight, not vanish, and should be allowed to recover.

## Status

Research is in progress (literature, GitHub landscape, Polymarket microstructure, claim-checking). Strategy notes get filled as that lands. The learner itself is in `src/trading_rookie/` and is designed to run before we pick a venue-specific edge.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
pytest
python -m trading_rookie simulate
```

Claude Code: read `CLAUDE.md` before editing.

## Risk

US persons may not be able to use every venue. Do not evade geo-blocks. Paper until legal access and a passing walk-forward are both true.
