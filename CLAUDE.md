# Claude Code instructions — Trading Rookie

You are working in `ozzielove/trading-rookie`. Paper-first adaptive trader. $50 bankroll. 1% risk. Never enable live trading unless the user explicitly asks after a passing walk-forward.

## Non-negotiables

- `Config.mode` stays `paper` unless the user says otherwise in this session.
- Position notional ≤ `risk_pct * equity`. No exceptions for "high confidence."
- Sleeves never get deleted. Reweight and retune. Spawning is allowed. Death is not.
- Do not invent backtest PnL. If data is missing, fail. If a 6–12 month walk-forward has not been run, say so.
- No secrets in git. Use `.env`.
- Do not help evade venue geo/KYC restrictions.

## Architecture (keep this)

- `config.py` — bankroll, risk, mode, learning rates
- `sleeves.py` — individual hypotheses. Each can `propose()`, `update()`, `morph()`
- `ensemble.py` — Dirichlet / Bayesian weights, floor so nothing dies
- `regime.py` — online regime features (vol, liquidity, event density)
- `learner.py` — the loop: observe → update → morph → maybe spawn → size
- `backtest.py` — walk-forward only. Expanding window. Costs required.
- `simulate.py` — CLI entry for paper / replay

If you add a venue (Polymarket CLOB, Kalshi, etc.), it is an adapter under `src/trading_rookie/venues/`. The learner must not import venue SDKs at module top-level.

## When filling research docs

`docs/*.md` are the research log. Replace "research pending" with sourced notes (URL, date). Do not overwrite the adaptive design to make a static strategy "simpler."

## Tests to keep green

- 1% cap holds after a winning trade (equity up) and a losing trade (equity down)
- Weight vector always sums to 1 and every sleeve ≥ `min_weight`
- `morph()` changes parameters without removing the sleeve
- Backtest runner raises if fee/spread are omitted or history < 180 days
