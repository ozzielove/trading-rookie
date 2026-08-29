# Trading Rookie

## Read first (clone)

Before CLAUDE.md, BUILD.md, or any Python: read the backtest notes and proof.

1. [`docs/backtest-proof-and-hardened.md`](docs/backtest-proof-and-hardened.md) — PAPER vs this-bot FAIL, Book/Venue/Tape stamps. Not hearsay.
2. [`docs/prd/03-backtest-gate.md`](docs/prd/03-backtest-gate.md) — Tape gate. Maker walk-forward is FAIL until recorded books exist.

Do not invent daily P&L. `simulate` is wiring, not an edge.

Paper-first, fully adaptive trading system. Starting bankroll **$50**. Risk per trade is **1%** of equity. Built to be driven 100% from **Claude Code CLI**.

This is not a frozen strategy. It is an ensemble of sleeves that keep living. They reweight, retune, and change shape as evidence comes in. Losers are not deleted. They shrink and keep learning.

Live trading is off by default. Do not turn it on until a walk-forward backtest of at least 6 months (12 preferred) survives fees, spread, and the 1% cap.

## Claude Code CLI (this is the product)

No other IDE, cloud agent, or paid platform is required.

```bash
git clone https://github.com/ozzielove/trading-rookie.git
cd trading-rookie
claude
```

Claude Code reads the two files above first, then CLAUDE.md, then docs/PRD.md, then executes docs/BUILD.md. You should not need to type the Python yourself.

## $50 is the only money

| Spend | Allowed |
| --- | --- |
| $50 trading bankroll | Yes (1% tickets) |
| Paid data / signals / SaaS / extra cloud | No |
| Second deposit "for gas" or "for Vercel" | No — gas, if any, comes out of the $50 |

Paper mode costs $0. Live mode, when you later opt in, is that same $50.

## What it is not

- A "$6k/day AI bot" clone
- A genetic kill-or-clone farm (winners copy, losers die)
- A sandstone backtest you deploy once and pray
- A project that needs more cash to "just start"

## Adaptive loop

Every resolved market / bar:

1. **Observe** — fills, marks, fees, regime features
2. **Update beliefs** — Bayesian sleeve weights, never zeroed out
3. **Retune** — constrained parameter drift per sleeve (polymorphic form)
4. **Spawn** — if residual error is structured, add a new sleeve. Old sleeves stay.
5. **Size** — 1% of current equity, split by posterior weights
6. **Record** — everything needed to audit why it changed

## Manual setup (only if you are not using Claude Code)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
PYTHONPATH=src pytest -q
PYTHONPATH=src python -m trading_rookie simulate
```

Or: `make setup test simulate`

## Status

Locked spec: Kalshi maker, p≥0.50, 1% of $50, fractional. Literature cell (PAPER): Burgi, Deng, Whelan (Jan 2026). This-bot maker walk-forward: **FAIL** until recorded books exist. Provenance: `docs/backtest-proof-and-hardened.md`. `simulate` is a wiring test, not an edge claim.

## Risk

US persons may not be able to use every venue. Do not evade geo-blocks. Paper until legal access and a passing walk-forward are both true.
