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

Venue and Tape stamps: pending in this file until they land.
