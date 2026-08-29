# Claude Code CLI — build this, in order

Do not skip. Do not enable live. Do not install social trading bots. Do not call a chat model on every tick.

## 0. Setup

```bash
git clone https://github.com/ozzielove/trading-rookie.git
cd trading-rookie
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp -n .env.example .env
PYTHONPATH=src pytest -q
PYTHONPATH=src python -m trading_rookie simulate
```

Read docs/PRD.md, docs/prd/01-strategy.md, CLAUDE.md.

## 1. Keep the learner

Do not replace the ensemble with a static rule. Sleeves must propose, update, morph. Floor weights. Spawn allowed. Death forbidden.

Tests that must stay green: tests/test_risk.py, tests/test_backtest.py.

## 2. Kalshi paper adapter

Implement src/trading_rookie/venues/kalshi.py using official Kalshi python client or documented REST.

- Base URL from KALSHI_API_BASE (demo first)
- RSA-PSS headers, keys in .env, never committed
- List markets, read BBO, post GTC limit bid as maker, cancel
- Size = min(0.01 * equity / price, remaining book), quantity multiple of 0.01
- Reject any order if notional + expected taker fee > 0.01 * equity
- Reject p < 0.50 bids and any p < 0.20 take
- If a series has maker fees, include them in the notional check

Details: docs/prd/02-kalshi.md (Venue fills this)

## 3. Paper loop

src/trading_rookie/paper.py (or extend simulate):

Every N seconds: refresh markets -> learner.propose -> if edge long favorites, post/replace maker bid -> on fill/expire, learner.step with realized when settled -> write journal JSONL under data/ (gitignored)

HALT file or TRADING_ROOKIE_HALT=1 cancels all and exits 0.

## 4. Record the book

Because historical L2 is missing, persist live orderbook snapshots + trades locally. This is how a future 180-day maker walk-forward becomes possible. Do not invent past books. Do not treat candlestick bid/ask OHLC as fills.

See docs/prd/03-backtest-gate.md (Tape fills this)

## 5. Fees

Do not hardcode 10 bps. Load Kalshi fee_type per series. Taker quadratic 0.07*C*P*(1-P) rounded per docs. Maker 0.0175 only if the series is in the maker-fee list. If the live PDF cannot be fetched, fail the live path, paper may use the documented Feb 2026 formulas with a log warning.

## 6. 24/7 on Hostinger

Only after paper loop works locally.

- VPS: Docker or systemd running `python -m trading_rookie paper`
- Restart on failure, log rotate
- OpenClaw (optional): Telegram status + HALT. OpenClaw must not sign Kalshi orders
- Do not run Claude Code as a daemon

See docs/prd/04-runtime-24-7.md

## 7. Live (last)

User must type that they want live. Then: switch KALSHI_API_BASE to prod, real keys, KYC already done. Same 1 percent cap. Same maker-only rules.

## Done when

- pytest green
- Demo paper can post and cancel a fractional favorite bid
- Journal records why the ensemble changed
- README and CLAUDE.md still say paper default and no fake PnL
