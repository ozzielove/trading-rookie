# Backtest proof and hardened gates

Owner: Tape. Operator: Claude Code CLI.
Locked 2026-08-29 ET: strategy **A**, Kalshi maker fade-longshot, **1% of current equity**, $50 paper-first.

Ozirus asked for **day-by-day profit for 120–365 days**. This file is the proof that those numbers **do not exist** for a maker strategy on free public Kalshi data. It is not an equity curve. Zeros would be fake PnL. Missing days are **FAIL**, not `$0.00`.

Canonical gate: [`docs/prd/03-backtest-gate.md`](prd/03-backtest-gate.md). Recorder path: `data/kalshi/book/` (gitignored).

---

## Status line

```
date: 2026-08-29
maker_walk_forward: FAIL
daily_pnl_120d: FAIL
daily_pnl_180d: FAIL
daily_pnl_365d: FAIL
reason: no historical L2/BBO; no files in data/kalshi/book/
public: trades + settlements + candle bid/ask OHLC + live book (now only)
candle_as_maker: forbidden
invented_fills: forbidden
invented_daily_pnl: forbidden
licensed_books: forbidden unless spend > $50 bankroll
paper_validate: allowed on Kalshi demo off live book
book_recorder: required; 180-day maker-WF clock starts at first snapshot on disk
risk: 1% of current equity
strategy: A Kalshi maker fade-longshot
equity_curve: none
```

---

## What public data can prove (retrieved 2026-08-29, unauthenticated)

Base: `https://external-api.kalshi.com/trade-api/v2`. Live vs historical cutoff:

```
GET /historical/cutoff  HTTP 200
market_positions_last_updated_ts = 2026-06-30T00:00:00Z
market_settled_ts                = 2026-06-30T00:00:00Z
orders_updated_ts                = 2026-06-30T00:00:00Z
trades_created_ts                = 2026-06-30T00:00:00Z
```

That is a ~60-day live window on this date (docs target 3 months). Older settled markets and older trades are on `/historical/*` only.

### Trades (prints exist; this is not maker PnL)

| Fact | Value | How |
| --- | --- | --- |
| Oldest historical print retrieved | `2021-06-30T20:09:14Z` ticker `HOME-21JUN-T750` | `GET /historical/trades` with `max_ts` near 2021-07-01, HTTP 200 |
| Print at historical cutoff | `2026-06-29T23:59:59.93426Z` (several tickers on that page) | `GET /historical/trades` unfiltered, HTTP 200 |
| Print at 180-day boundary | `2026-03-01T23:59:59Z` | `GET /historical/trades?max_ts=` ~2026-03-02, HTTP 200 |
| Newest live print retrieved | `2026-08-29T09:48:32Z` | `GET /markets/trades`, HTTP 200 |
| Calendar span of **tape** | 2021-06-30 → 2026-08-29 (>180 and >365 days) | min/max `created_time` above |
| `taker_book_side` present | `bid` / `ask` on those payloads | classifies the **tape’s** resting side, not our quote |

A 365-day **trade** calendar exists. A 365-day **maker fill** calendar does not.

Third-party card, **not** Kalshi official (label it if cited): HuggingFace `TrevorJS/kalshi-trades` claimed 154,505,005 trades, June 2021–January 2026, CC-BY-4.0. Trades + market metadata. No order-book history. Stops January 2026, so it does not cover Mar–Aug 2026. Do not use it as this desk’s count or as BBO.

### Settlements

Retrieved: `GET /historical/markets/KXHIGHLAX-26MAR02-T73` HTTP 200  
`status=finalized`, `result=no`, `settlement_ts=2026-03-03T12:31:56.749229Z`, `settlement_value_dollars=0.0000`, `volume_fp=63528.00`, `open_time=2026-03-01T15:00:00Z`.

Settlements exist for historical markets. They prove outcomes. They do not prove we were filled as maker.

### Candle bid/ask OHLC (not BBO)

`GET /historical/markets/{ticker}/candlesticks` HTTP 200. Keys observed: `end_period_ts`, `yes_bid` OHLC, `yes_ask` OHLC, trade `price` OHLC, volume, open interest. Periods: 1 / 60 / 1440 minutes.

Example 1-minute bars: `KXHIGHNY-26JUN28-B81.5`, **n=421**, `2026-06-27T14:01:00Z` → `2026-06-28T00:00:00Z`. First bar: `yes_bid` open 0.01 / close 0.03, `yes_ask` open 1.00 / close 0.45. That spread is **bar range**, not quote-at-`t`.

### Live book (now only)

`GET /markets/{ticker}/orderbook` HTTP 200: `orderbook_fp.yes_dollars` / `no_dollars` as `[price, size]` ladders. Asks implied (`1 −` opposite bid).

`GET /historical/markets/{ticker}/orderbook` → **HTTP 404** `404 page not found`. No public historical L2/BBO series.

### Fees (for a future journal; not applied to fake fills)

Live PDF `https://kalshi.com/docs/kalshi-fee-schedule.pdf` HTTP **429** on 2026-08-29. Coefficients from Wayback 2026-06-12 of the Feb 5, 2026 schedule, plus live `docs.kalshi.com` (HTTP 200): taker `round up(0.07×C×P×(1−P))`; maker on maker-fee series `round up(0.0175×C×P×(1−P))` when a resting order later executes; series `FeeMultiplier` M; combo maker 0.5 instead of 0.25. Do not use 2022 makers-free. Do not apply these formulas to invented fills.

---

## What public data cannot prove

| Claim | Why FAIL |
| --- | --- |
| Day-by-day **maker** profit, 120 days | No book at those timestamps |
| Same, 180 days | Same |
| Same, 365 days | Same. Trade span ≥365d is irrelevant |
| We were filled as maker at price P | Need our resting order vs recorded size/queue. Tape `taker_book_side` is someone else |
| Candle `yes_bid`/`yes_ask` as the quote we joined | Bar OHLC ≠ BBO snapshot |
| Spread paid/earned | Need BBO at send. Flat `spread_bps` is synthetic wiring only |
| `$50 → $X` equity | No scored maker fills. **No fake equity.** |
| Literature +2.6% / day scaled | Burgi/Deng/Whelan is not this desk; pre-April 2025 maker fees; ~33% SD |

---

## Requested windows (calendar, ending 2026-08-29)

| Window | Start (inclusive) | Maker daily PnL |
| --- | --- | --- |
| 120 days | 2026-05-01 | **FAIL** every day — no book |
| 180 days | 2026-03-02 | **FAIL** every day — no book |
| 365 days | 2025-08-29 | **FAIL** every day — no book |

PASS days in each window: **0**.  
FAIL days: **120 / 180 / 365**.  
Equity: **not reported** (no path).

Do not emit a CSV of `net_pnl=0.00` for those dates. That would be a fabricated flat equity curve.

---

## Future daily journal (columns)

When `data/kalshi/book/` has snapshots for a date **and** Kalshi reports maker fills for our demo/live orders that day, append one row. Until then, do not write a PnL number.

Suggested file: `data/kalshi/journal/daily.csv` (gitignored). Header:

```
date,status,n_snapshots,n_resting_quotes,n_maker_fills,n_taker_fills_violation,notional,gross_pnl,fees,spread_at_send_sum,net_pnl,equity_eod,fail_reason
```

| Column | Rule |
| --- | --- |
| `date` | America/New_York calendar date |
| `status` | `PASS` \| `FAIL` \| `PAPER-ONLY` |
| `n_snapshots` | Book files that day. If 0 → `status=FAIL`, **omit all PnL columns** (leave empty), `fail_reason=no_book` |
| `n_resting_quotes` | Limit bids we posted that stayed maker |
| `n_maker_fills` | Fills Kalshi marked as resting-then-matched. 0 fills and snapshots>0 is allowed; `net_pnl` may then be 0 **only** because we logged real quotes, not because we guessed |
| `n_taker_fills_violation` | Must be 0 for this edge. Any taker fill is a protocol fail, not a data point |
| `notional` | Sum of stakes; each stake ≤ 1% of equity **at send** |
| `gross_pnl` | Settlement vs fill price on **our** maker fills only |
| `fees` | Series `fee_type` + M + 2026 formula on those fills |
| `spread_at_send_sum` | Live/recorded `yes_ask − yes_bid` at each send, not candle OHLC |
| `net_pnl` | `gross_pnl − fees` (spread is already in fill vs mid/BBO; do not double-count). Empty if `status=FAIL` |
| `equity_eod` | Prior equity + net_pnl. Empty if any FAIL day would break the chain |
| `fail_reason` | `no_book` \| `candle_proxy_attempt` \| `invented_fill` \| `costs_missing` \| `taker_fill` \| empty |

Hardening: a generator that cannot see `data/kalshi/book/{date}*` **must** write `status=FAIL` and empty PnL. No default zero. No candle join. No mid.

### Example rows (illustrative, not results)

```
date,status,n_snapshots,n_resting_quotes,n_maker_fills,n_taker_fills_violation,notional,gross_pnl,fees,spread_at_send_sum,net_pnl,equity_eod,fail_reason
2026-03-02,FAIL,0,,,,,,no_book
2026-08-29,FAIL,0,,,,,,no_book
```

A later PASS row is allowed only after the recorder has been running and Kalshi has reported maker fills. Do not pre-fill it with sample dollars.

---

## Hardened checks for Claude Code

1. Read this file and `docs/prd/03-backtest-gate.md` before any “results” or “daily profit” task.
2. If asked for 120/180/365-day maker PnL without book files: print the status line and **FAIL**. Do not start a candle-as-maker job.
3. `walk_forward` on synthetic history remains a **wiring test**, labeled not an edge. Do not copy its equity into this file.
4. Start the book recorder (`data/kalshi/book/`) before optimizing sleeves. The 180-day clock starts at the first snapshot on disk.
5. Never commit journals, books, or secrets.

---

## Bottom line

Public Kalshi history is long enough **as a trade tape**. It is not a maker book. Day-by-day profit for 120, 180, or 365 days: **FAIL**. No equity curve. No invented fills.
