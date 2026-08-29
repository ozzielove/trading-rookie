# 02 Kalshi

Locked jury (do not reopen unless Ozirus changes the motion): **A at 1%**. Kalshi maker fade-longshot, paper on demo first, fractional size only. Polymarket US sports is plan B after iOS KYC. Do not trade polymarket.com Global from the US. Do not use a VPN. No paid data. No unofficial trading bots. No invented PnL.

This file is the Claude Code CLI venue page. The 24/7 process is **Python posting and canceling orders**. A chat model is not the trader.

## Constraints

- US person, New York. Kalshi is the legal CFTC venue for this bot.
- Bankroll **$50**. Risk **1% = $0.50** per idea.
- Paper on **demo** until a walk-forward of free Kalshi history (fees plus spread, 180+ days) passes and live KYC is done.
- Live keys never mix with demo keys.
- Perps / margin products are out of scope.

## Paper path (do this in order)

1. Open **https://demo.kalshi.co/** (`.co`, not `.com`). `demo.kalshi.com` is not the documented demo UI.
2. Sign up with mock PII (fake name, address, SSN). Use an email you can access.
3. Funds are **not** preloaded. Load mock cash with the documented test Visa `4000 0566 5566 5556` (any future expiry, any 3-digit CVV). Size the bot as if the balance were **$50** even if mock cash is larger. Demo deposit cap: UNKNOWN.
4. Account & security → API Keys → Create Key. Save the **private PEM** (Kalshi does not store it) and the **API Key ID**.
5. Auth is **RSA-PSS**, not email. Every signed request needs:
   - `KALSHI-ACCESS-KEY` = Key ID
   - `KALSHI-ACCESS-TIMESTAMP` = Unix ms
   - `KALSHI-ACCESS-SIGNATURE` = base64 RSA-PSS-SHA256 of `timestamp + METHOD + path` with **no query string**
6. Point the CLI at demo, not prod:

```text
KALSHI_BASE_URL=https://external-api.demo.kalshi.co/trade-api/v2
KALSHI_WS_URL=wss://external-api-ws.demo.kalshi.co/trade-api/ws/v2
KALSHI_API_KEY_ID=<demo key id>
KALSHI_PRIVATE_KEY_PATH=<path to demo PEM>
```

Official docs do **not** name those env vars. They are local. Prod REST (later): `https://external-api.kalshi.com/trade-api/v2`. Do not reuse demo keys there.

7. First signed call: `GET /portfolio/balance`. Confirm schema (`balance` cents vs `*_dollars`); the API is mid-migration.
8. First paper order: V2 `POST /portfolio/events/orders`. Use `post_only` for maker. `count` is a string (`"0.01"` …). `self_trade_prevention_type` is required. Legacy `POST /portfolio/orders` is deprecated.
9. Cancel with the documented cancel endpoint. Overnight: **Python** posts and cancels. Do not leave a chat session as the live loop.

## Size (why 1% is fractional-only)

Min order size is **0.01 contracts**. Payout is **$1** per contract (`notional_value_dollars` `"1.0000"` on sampled binaries). Tick is **per market**: read `price_ranges[].step` (NFL sample was 1 cent `linear_cent`).

Buy YES at price P: max loss ≈ `C × P + fees`.

| Limit | Cost of **1.00** contract (official 1-lot taker table) | Fits $0.50? |
| --- | --- | --- |
| 10c | $0.11 | Yes |
| 50c | **$0.52** | **No. $0.02 over the cap.** |
| 90c | $0.91 | No |

Locked sleeve is maker fade, p>=0.55. One whole contract at 55c is already $0.55 **before** fees, so it also fails 1%. Use `count` `"0.01"` to about `"0.90"`, or skip. Do not drop the 1% cap to make 1-lots fit.

## Fees (budget these, do not invent edge)

Authoritative PDF: https://kalshi.com/docs/kalshi-fee-schedule.pdf (effective 2026-07-07).

- **Taker** (immediately matched): `fees = round up(M × 0.07 × C × P × (1 − P))`
- **Maker** (resting, only if the series is in Maker Fees): `fees = round up(M × 0.0175 × C × P × (1 − P))` with **M default 0** unless otherwise indicated
- Always read `fee_type` and `fee_multiplier` on `GET /series/{series_ticker}`. NFL `KXNFLGAME` on 2026-08-29 was `quadratic_with_maker_fees` (maker not free).
- Binary settlement fee: **none**
- Demo vs prod fee identity: UNKNOWN. Assume the same formula until a demo fill shows `average_fee_paid`.

Official 1-lot taker table: 10c → $0.01, 50c → $0.02, 90c → $0.01. All-in YES debit $0.11 / $0.52 / $0.91. A 1 cent spread is 2% of the $0.50 risk budget. Fees plus spread belong in the walk-forward. No PnL claim until Tape says that pass exists.

## Free history (backtest input)

Public REST, no key (live 200s on 2026-08-29), no paid feed, no bulk CSV.

- `GET /historical/cutoff` then split live vs archive
- Markets: `GET /markets`, `GET /historical/markets`
- Candles (period 1 / 60 / 1440 min): live `GET /series/{series}/markets/{ticker}/candlesticks`; archive `GET /historical/markets/{ticker}/candlesticks`
- Tape: `GET /markets/trades`, `GET /historical/trades` (limit max 1000, cursor)
- Live book: `GET /markets/{ticker}/orderbook` (yes bids and no bids only)

**There is no historical orderbook snapshot endpoint.** Do not fake depth. Reconstruct going forward from WS `orderbook_delta`, or approximate from candle bid/ask plus the public tape. How far `/historical` goes back is UNKNOWN; page until empty. Cutoff observed 2026-08-29: `2026-06-30T00:00:00Z`. Tape needs 180+ days from this path.

WS requires RSA even for public channels. Both REST and WS are free. Basic authenticated rate: 200 read / 100 write tokens/s (~20 GET/s).

## Hours / sports

Exchange is ~24/7 ET except Thursday **03:00–05:00 ET** pause. Trade only if the market is `active` and `GET /exchange/status` has `trading_active=true`. Sports exist on Kalshi (`KXNFLGAME`). Paper them on demo. NY prod sports: check in-app later. Do not VPN around anything.

## Live gate

Paper on demo until **all** of these are true:

1. Walk-forward on this free history, fees plus spread, 180+ days, 1% of $50, **passes** (Tape).
2. Real Kalshi KYC on production (not mock SSN).
3. Live flag stays off in the CLI until then.

Overnight after that: Python posts/cancels on the signed API. OpenClaw/Hostinger may supervise. A chat model does not place orders.

## UNKNOWN (do not fill with guesses)

Demo key URL path, demo fund cap, demo vs prod fees, unauth rate limits, max order size, historical retention floor, Developer Agreement body, balance cents vs `*_dollars`, NY sports geo-block, exact 1-lot maker round-up.

Sources: docs.kalshi.com (environments, demo, API keys, historical data, fee rounding), kalshi.com/docs/kalshi-fee-schedule.pdf, help.kalshi.com demo-account article, live GETs 2026-08-29. Venue notes: `docs/microstructure.md`.
