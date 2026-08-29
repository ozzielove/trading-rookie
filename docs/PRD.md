# Trading Rookie PRD

## 1. Problem

Ozirus wants a Claude Code CLI-built, fully adaptive paper-first trader. Bankroll 50 USD. Risk 1 percent of equity. Must be able to run 24/7 in the cloud later (Hostinger VPS + OpenClaw supervisor) without burning Claude tokens on every tick.

## 2. Users

- Builder: Claude Code CLI cloning this public repo
- Operator: Ozirus, US, America/New_York
- Runtime: Python process on a VPS, not Claude Code itself

## 3. Locked decisions

See docs/prd/01-strategy.md. Unanimous desk vote 2026-08-29: Kalshi maker fade-longshot, 1 percent, fractional size, paper first.

## 4. Goals

- G1: Claude Code can clone, venv, test, and paper-simulate with no paid SaaS
- G2: Adaptive ensemble never deletes sleeves
- G3: Orders, if any, are maker bids on Kalshi p>=0.50, never taking p<0.20
- G4: 24/7 loop is Python. OpenClaw is chat/kill-switch only
- G5: Fail closed when data or fees are missing. Never invent PnL

## 5. Non-goals

- 6000 USD/day income
- polymarket.com Global trading from the US
- LLM as a probability engine
- Genetic kill-or-clone
- Paid market-data or licensed L2 books unless Ozirus explicitly spends extra
- Dropping the 1 percent cap to chase daily dollars

## 6. Constraints

- Money: 50 USD trading bankroll. Hosting (Hostinger) is a separate bill if/when he buys it
- Legal: no VPN, no Global Polymarket. Kalshi KYC for live
- Size: 1 percent of 50 USD is 0.50 USD. One whole 50c Kalshi contract plus taker fee does not fit. Use 0.01 contract granularity
- Data: no historical Kalshi L2. Maker walk-forward is a hard fail until live books are recorded going forward
- Tokens: Claude Code is for build. Do not call a chat model per tick

## 7. Architecture

```
Claude Code CLI (build)
    -> this repo
Python learner (24/7)
    -> Kalshi demo then live API
    -> maker bids / cancels
    -> adaptive ensemble
OpenClaw on Hostinger (optional supervisor)
    -> status, halt, never order router
```

Code map:
- src/trading_rookie/config.py
- sleeves.py, ensemble.py, regime.py, learner.py
- backtest.py (walk-forward, costs required)
- venues/ (Kalshi adapter only, lazy import)
- docs/prd/* and docs/BUILD.md

## 8. Functional requirements

- FR1 Paper mode default. Live is opt-in env flag
- FR2 Stake = 0.01 * equity, never more
- FR3 Weights sum to 1, every sleeve strictly positive
- FR4 morph() changes params, keeps identity
- FR5 Kalshi adapter: auth demo, read markets, post/cancel limit bids, classify maker
- FR6 Record live BBO/trades to data/ (gitignored) for future walk-forward
- FR7 Kill switch file or env HALT=1
- FR8 OpenClaw may set HALT, not place orders

## 9. Acceptance

- pytest green
- python -m trading_rookie simulate prints a wiring test labeled not an edge
- Paper bot on Kalshi demo can post and cancel a fractional maker bid under the 1 percent cap
- Docs state maker WF is FAIL without L2 history
- No secrets in git

## 10. 24/7

See docs/prd/04-runtime-24-7.md. Python systemd/docker on Hostinger. OpenClaw is not the trader.
