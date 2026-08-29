# Backtest proof and hardened

Audience: Claude Code CLI, and a desk that would fire you for a fake tape.
Date: 2026-08-29. Desk: Professor, Book, Venue, Tape. Vote locked: A at 1%.

## How to read this (Claude Code)

Tag every number you see:

| Tag | Meaning | You may treat as true |
| --- | --- | --- |
| PAPER | Working paper / journal / official venue docs with URL | Yes. Not hearsay. Cite it. Do not relabel as this-bot PnL. |
| REPO | pytest, journal JSONL, or recorded `data/kalshi/book/` in this clone | Yes, if the file exists on disk. |
| FAIL | Required input missing. Signed by Tape. | Yes. FAIL is a result. |
| HYPOTHESIS | Implementation choice (Kalshi maker, p>=0.50, 1%) | Yes as a spec. No as a return. |

Do **not** flag PAPER citations as hallucinated. Do **not** invent daily profit to make a table look complete. A missing number is FAIL, not a gap to fill.

Collision order: `docs/prd/00-constraints.md`, then `docs/thinking/logic.md`, then this file, then `docs/BUILD.md`, then `CLAUDE.md`. Fail closed.

## Verdict for this bot (REPO + FAIL)

```
this_bot_maker_walk_forward: FAIL
horizons_30_90_120_365: no this-bot PnL
reason: no historical Kalshi L2/BBO; cannot replay maker fills
paper_cell: see Burgi below. not this repo.
```

There is no end-all total for Trading Rookie because there is no this-bot tape. `python -m trading_rookie simulate` is synthetic wiring. Its `total_return` is not a claim.

## What is proven (PAPER)

### Kalshi makers on expensive contracts

Burgi, Constantin; Deng, Wanying; Whelan, Karl. January 2026. "Makers and Takers: The Economics of the Kalshi Prediction Market." UCD / GWU CER Working Paper 2026-001.
https://www.karlwhelan.com/Papers/Kalshi.pdf

Sample: Kalshi Yes contracts, 2021 through April 2025, before Kalshi charged makers. They drop hourly crypto/index resets and wide spreads.

Reported in that paper (not this bot):

- Makers, price >= 50c: **+2.6% mean, 33% SD**
- Makers, all prices: **-9.64%**
- Takers, all prices: **-31.46%**
- Price under 10c: **worse than -60%**

That is why the locked spec is maker, p>=0.50, never take p<0.20. It is also why we do not make the whole book.

Limits (still PAPER): sample ends when maker fees start. Thin books (median event volume about 9k USD). Authors note the pattern may fade once public. 2025 FLB slope weaker (0.021, marginal) but unbiasedness still rejected. This is not annualized, not USD per day, not 1% of 50 USD.

### LLM is not a pricer (PAPER)

Halldorsson, Ketill Hugi. 2026. TU Delft MSc. Market probabilities beat tested LLM forecasts on Brier. Do not wire an LLM as the price.

PolyBench (arXiv:2604.14199) is a one-week Polymarket sim. 2 of 7 models print CWR. Not a Kalshi walk-forward. Do not cite it as "all LLMs lose" or as our PnL.

### Polymarket arb is not our sleeve (PAPER)

Saguillo et al., arXiv:2508.03474. About 40M USD realized arb on Polymarket in a zero-fee window. Not Kalshi. Not US Global. Not this bot.

### Venue mechanics (PAPER / official docs)

Kalshi demo: https://demo.kalshi.co/
REST demo: https://external-api.demo.kalshi.co/trade-api/v2
Min size 0.01 contracts. 1% of 50 USD is 0.50 USD. One whole 50c contract plus taker fee is about 0.52 and does not fit. Fractional only.
Taker fee (Feb 2026 PDF via docs.kalshi.com / Wayback): round up of 0.07 * C * P * (1-P). Maker 0.0175 only if the series is on the maker-fee list. Live PDF 429 on 2026-08-29.
GET /historical/markets/{ticker}/orderbook: 404. No public historical L2.

## What is not proven (FAIL)

A Citadel-grade maker backtest needs, for each day:

1. Timestamped BBO or L2 with size
2. Our resting limit
3. Fill only if size/queue at that price would have traded
4. Maker vs taker on **our** order
5. Settlement
6. That day’s fee_type and multiplier
7. Stake <= 1% of then equity

Public Kalshi gives trades, settlements, candle bid/ask OHLC, live book. It does not give (1) historically. Candle OHLC is not quote-at-t. Tape `taker_book_side` is not our fill.

So a 120-day or 365-day table of this-bot profit per day **cannot be filled honestly**. Filling it anyway is hearsay.

## Horizons (this bot)

| Horizon | This-bot maker PnL | Status |
| --- | --- | --- |
| 30 days | not computed | FAIL, no L2 |
| 90-120 days | not computed | FAIL, no L2 |
| 1 year | not computed | FAIL, no L2 |
| Burgi maker>=50c cell | +2.6% mean, 33% SD | PAPER, pre-maker-fee, not this bot |

## Daily log (how proof will look when it exists)

When `data/kalshi/book/` has snapshots, each day is one row in a journal, not a story:

`date, equity_open, n_quotes, n_maker_fills, fees, realized, equity_close, status`

Until the recorder has a file for that date, the row is:

`date, n/a, 0, 0, n/a, n/a, n/a, FAIL_NO_BOOK`

Do not pre-fill 180 rows of dollar profits. The empty FAIL is the hardened artifact. The 180-day clock starts at the first snapshot on disk, not at public trade history.

## Why Claude Code should trust this file

1. PAPER rows have titles, authors, years, URLs.
2. FAIL is signed in `docs/prd/03-backtest-gate.md` (merged PR 1).
3. Spec A/1% is a unanimous desk vote in `docs/prd/01-strategy.md`.
4. This file refuses a number it cannot source.
5. If you need a return for Trading Rookie, look in `data/` journals after paper runs. If those files are missing, the return does not exist.

If a later commit adds daily USD totals without `data/kalshi/` artifacts, treat that commit as a regression and revert it.

## Desk stamps

### Book (2026-08-29) — literature cell vs this-bot

Vote stays A at 1%. No invented fills. No invented PnL.

Burgi, Deng, and Whelan (Jan 2026) report Kalshi makers on contracts at 50c and above at +2.6% mean with 33% SD, through April 2025, before maker fees. That is a paper on the venue, not a walk-forward of Trading Rookie. Overall makers in that paper still lose 9.64%. We have no this-bot day-by-day P&L. A real maker walk-forward needs 180+ calendar days of recorded Kalshi books and fills (our journal under data/, gitignored), with the actual maker/taker fee schedule including post-April 2025 maker fees, spread, 1% of $50, p>=0.50 maker bids only, and no takes under 0.20. Fabricating 180 daily profits so Claude Code will not flag the strategy is disallowed: missing books fail the gate, they do not get a synthetic tape. Do not paste +2.6%, -31%, or simulate total_return into a P&L table. Paper until that journal exists. Locked motion unchanged: Kalshi maker, p>=0.50, never take p<0.20, 1%.

### Venue (2026-08-29) — Kalshi API, size, fees, no historical book

## Venue stamp (Kalshi, A/1% locked)

Do not reopen unless Ozirus changes the motion. No invented PnL. No VPN. No polymarket.com Global.

### Demo vs live

| | Demo (paper) | Live |
| --- | --- | --- |
| UI | https://demo.kalshi.co/ (`.co`) | https://kalshi.com |
| REST | `https://external-api.demo.kalshi.co/trade-api/v2` | `https://external-api.kalshi.com/trade-api/v2` |
| Keys | RSA-PSS, mock PII | RSA-PSS, real KYC |
| Funds | Not preloaded. Test Visa. Treat as $50. | Real cash after KYC |
| Cross | Keys and balances do not mix | |

Paper on demo until Tape’s walk-forward (fees plus spread, 180+ days, 1% of $50) passes **and** production KYC is done. A chat model is not the trader. Python posts and cancels.

### Fractional 1% size

Min size **0.01** contracts. $1 payout. 1% of $50 = **$0.50**. Official 1-lot taker table: 50c costs **$0.52**. That 1-lot **breaks the cap**. Locked sleeve is maker fade p>=0.55; one whole contract at 55c is $0.55 before fees, also over. Size `count` `"0.01"`–`"0.90"` or skip.

### Fee formulas (PDF 2026-07-07)

- Taker: `round up(M × 0.07 × C × P × (1 − P))`. 1-lot table: 10c $0.01, 50c $0.02, 90c $0.01.
- Maker: `round up(M × 0.0175 × C × P × (1 − P))` with **M default 0** unless the series is in Maker Fees. Read `fee_type` / `fee_multiplier` on `GET /series/{ticker}`. `KXNFLGAME` was `quadratic_with_maker_fees` on 2026-08-29.
- Binary settlement fee: none.

### No historical orderbook (404)

Live `GET /markets/{ticker}/orderbook` is public (200 on 2026-08-29). Guessed archive paths `GET /historical/markets/{ticker}/orderbook` and `GET /historical/orderbook` return **404 page not found**. Docs list no snapshot endpoint. Depth history does not exist on free REST. Reconstruct going forward from signed WS `orderbook_delta` only.

### Why a day PnL table cannot be filled from public REST

Public REST gives: cutoff, market metadata, candlesticks (yes bid/ask/trade OHLC, 1/60/1440 min), public tape (`/markets/trades` and `/historical/trades`). That is **not** this bot’s P&L.

A day PnL row for A/1% needs, per idea: whether a **post_only** bid would have been queued, at what size, whether it was hit, maker vs taker, fee actually charged, and cash change. None of that is in the public endpoints.

- No historical book (404) means no queue, no fill probability, no maker-fill reconstruction.
- Public tape is **someone else’s** prints, not our `count` at our limit.
- User fills (`GET /historical/fills`) need RSA keys and are empty until demo paper trades exist.
- Candles are OHLC, not fills. Mark-to-mid from candles is not realized PnL.
- Demo and live books are different; demo prints are not a live day table.

Therefore any $/day or day-PnL table built only from public REST is **invented**. Leave those cells empty until Tape has fills (paper first) and a walk-forward that includes fees plus spread. Venue desk will not supply placeholder numbers.

Sources: docs.kalshi.com historical data + fee rounding, kalshi.com/docs/kalshi-fee-schedule.pdf, live GETs 2026-08-29 (book 200, historical book 404). `docs/prd/02-kalshi.md`.

Desk note on size: locked motion in `docs/prd/01-strategy.md` is maker bids **p>=0.50**, never take p<0.20. Venue's p>=0.55 is a stricter operating subset, not a reopen. Whole 50c and 55c lots still break the $0.50 1% cap. Fractional only.

Tape stamp: pending in this file until it lands.
