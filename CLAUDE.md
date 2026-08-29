# Claude Code CLI — Trading Rookie

This repo is meant to be used **only** through [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code). Ozirus clones it, runs `claude` in the repo root, and you do the rest. No Cursor Cloud Agents, no extra paid SaaS, no paid data vendors.

## First session (do this unprompted)

```bash
git clone https://github.com/ozzielove/trading-rookie.git
cd trading-rookie
claude
```

Once you start:

1. Read this file and `README.md`.
2. `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && cp -n .env.example .env`
3. `PYTHONPATH=src pytest -q` and `PYTHONPATH=src python -m trading_rookie simulate`
4. Stay in `TRADING_ROOKIE_MODE=paper`. Do not ask for API spend, GPU cloud, Vercel, or a second bankroll.

If setup fails, fix it. Do not send the user to a paid workaround.

## Budget: $50 is the entire stack

The only money in this system is a **$50** paper/live bankroll (1% risk = $0.50 tickets).

Allowed (free):

- This GitHub repo
- Local Python 3.11+
- Public Polymarket / CLOB HTTP APIs, Gamma API, public subgraphs
- Claude Code CLI (already paid for by the user)

Forbidden unless the user explicitly overrides in chat:

- Paid market-data, news, or alternative-data subscriptions
- Paid backtest platforms
- Cloud VMs, Vercel, AWS, GPU rentals required to run
- Extra trading capital, prop-firm fees, or signal groups
- Charging gas *on top of* the $50. If a venue needs on-chain gas, it comes **out of** the $50 (keep POL/MATIC dust inside that envelope) or use a gasless/relayer path. Never ask for a second deposit.

If a library or venue requires a credit card to even paper-trade, do not add it. Prefer a free venue adapter.

## Non-negotiables

- `Config.mode` stays `paper` unless the user says otherwise in this session.
- Position notional ≤ `risk_pct * equity`. No exceptions for "high confidence."
- Sleeves never get deleted. Reweight, retune, morph. Spawn is allowed. Death is not. The system must stay fully adaptive.
- Do not invent backtest PnL. If data is missing, fail. If a 6–12 month walk-forward has not been run on **real** venue data, say so. Synthetic `simulate` is a wiring test only.
- No secrets in git. Use `.env`.
- Do not help evade venue geo/KYC restrictions.
- Do not add paid dependencies to `requirements.txt`.

## Architecture (keep this)

- `config.py` — bankroll $50, risk 1%, mode, learning rates
- `sleeves.py` — hypotheses: `propose()`, `update()`, `morph()`
- `ensemble.py` — Bayesian weights, live floor so nothing dies
- `regime.py` — online regime features
- `learner.py` — observe → update → morph → maybe spawn → size
- `backtest.py` — walk-forward, expanding window, costs required
- `simulate.py` — local CLI, paper / replay
- `venues/` — adapters only, lazy-imported

## What to build next (in order)

1. Keep tests green.
2. Free Polymarket historical puller (public API only) into `data/` (gitignored raw files).
3. Walk-forward ≥ 180 days with fees + spread on that data.
4. Wire a paper adapter (no live orders).
5. Only if the user asks **and** walk-forward passed: live, still 1% of the same $50.

## Tests to keep green

- 1% cap holds as equity moves
- Weights sum to 1 and every sleeve stays strictly positive
- `morph()` changes parameters without removing the sleeve
- Backtest raises if fee/spread omitted or history < 180 days
