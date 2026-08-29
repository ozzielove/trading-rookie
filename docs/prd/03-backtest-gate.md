# 03 — Backtest gate

Owner: Tape. Operator: Claude Code CLI. Repo: `github.com/ozzielove/trading-rookie`.
Locked 2026-08-29 ET: strategy **A**, Kalshi maker fade-longshot, **1% of current equity**, $50 paper-first.

This file is a gate, not a hope. If a required input is missing, the gate is **FAIL**. Do not invent PnL, fills, queue, or BBO.

---

## 1. What this gate decides

Claude Code may not claim an edge, size up, or go live until this document’s **PASS** conditions are met.

Two separate questions:

| Question | Current status (2026-08-29) |
| --- | --- |
| Can we run a **maker walk-forward** on free public Kalshi history? | **HARD FAIL** |
| Can we **paper-validate** on Kalshi demo using the **live** book, and start recording book deltas for a future WF? | **Allowed**, with the rules below |

A passing paper session is not a passing walk-forward. Do not mix the two.

---

## 2. Locked strategy (do not reopen here)

- Venue: Kalshi first (US, CFTC). Not polymarket.com Global. No VPN.
- Edge intent: maker-side fade-longshot. Post bids on compressed favorites. `p >= 0.55`. Never take `p < 0.20`.
- Risk: **1% of current equity**. Ticket is `$0.50` at `$50`. No exceptions for confidence. Do not drop the 1% cap.
- Ensemble: adaptive sleeves. Sleeves do not die (`min_weight` floor). This edge is sleeve DNA after a real maker WF **passes**, not a frozen rule.
- LLM: risk filter at most, not a pricer.

Literature (`docs/literature.md`) is **not** this desk’s PnL. Burgi/Deng/Whelan “makers on high-p ~+2.6%” is pre-April 2025 maker fees and ~33% SD. Do not paste it into a results file.

---

## 3. HARD FAIL: maker walk-forward

A maker walk-forward requires replaying **whether a resting quote would have been filled**: timestamped BBO or L2 (price + size at levels), queue, and later settlement.

Probed 2026-08-29 against the free public API (`https://external-api.kalshi.com/trade-api/v2`, also `https://api.elections.kalshi.com/trade-api/v2`):

| Input | Public? | Maker WF? |
| --- | --- | --- |
| Historical trades (`GET /historical/trades`, live `GET /markets/trades`) | Yes. Prints from at least 2021-06-30 through live. Includes `taker_book_side`. | Tape classification only. Does **not** say we were the resting order. |
| Settlements (`result`, `settlement_ts`, `settlement_value_dollars` on historical markets) | Yes | Needed, not sufficient |
| Candlesticks 1 / 60 / 1440 min (`yes_bid` / `yes_ask` OHLC + trade OHLC) | Yes, historical and live | Interval OHLC of bid and of ask. **Not** a contemporaneous BBO snapshot. **Not** depth. |
| Current order book (`GET /markets/{ticker}/orderbook`) | Yes, **now** only | Live paper only |
| Historical L2 / BBO snapshots (`GET /historical/markets/{ticker}/orderbook`) | **HTTP 404**. No such public series | **Missing** |
| Licensed book history (Predexon, DepthFeed, LO:TECH, etc.) | Not free | **Out of budget** unless Ozirus spends **above** the $50 bankroll |

Live vs historical cutoff observed 2026-08-29: `GET /historical/cutoff` → `2026-06-30T00:00:00Z` (~60-day live window; docs target 3 months). Settled-before-cutoff markets are on `/historical/*` only.

**Verdict: maker walk-forward is HARD FAIL** until we have 180+ calendar days of **recorded** book snapshots or `orderbook_delta`s (or Ozirus pays for licensed history out of extra money, not the $50).

Engine already enforces: `Config.min_history_days >= 180`; `walk_forward` requires costs (`fee_bps` and `spread_bps` may not be `None`). That gate is necessary and **not sufficient** for a maker claim. The current `simulate` CLI is **synthetic wiring**, not an edge claim (`README.md`).

---

## 4. Forbidden (Claude Code must refuse)

1. **Do not candle-as-maker.** Do not join 1-minute (or hourly/daily) `yes_bid`/`yes_ask` OHLC to trades and call that a maker fill sim. Candle bid/ask is bar OHLC, not quote-at-`t`.
2. **Do not invent fills.** No assumed queue position, no “we were the whole size,” no mid-price maker, no last-trade-as-BBO.
3. **Do not invent PnL.** No placeholder equity curves. No copying literature numbers into `data/` results. If the run cannot execute, write `FAIL` and the missing input.
4. **Do not buy licensed books from the $50 bankroll.** Extra spend only if Ozirus explicitly authorizes money **above** $50.
5. **Do not drop 1%.** No “size up for more $/day” until a maker WF **PASS** exists (it does not).
6. **Do not use 2022 “makers free”** as the 2026 fee model.

If asked to produce maker WF numbers without L2 history, the only correct output is **FAIL** plus the blocker in §3.

---

## 5. What public data *is* for

Allowed, and already retrieved unauthenticated:

- **Trades + settlements:** taker/last-price studies, settlement labels, universe construction. `taker_book_side` classifies the *tape’s* resting side, not our fill.
- **Candle bid/ask OHLC:** coarse spread *distribution* research, not fill replay.
- **Live order book:** paper quoting **now**, and the seed for the recording path in §6.
- **Series metadata:** `fee_type`, `fee_multiplier` (`GET /series/{series}`, `GET /series/fee_changes?show_historical=true`).

HuggingFace `TrevorJS/kalshi-trades` (CC-BY-4.0, trades Jun 2021–Jan 2026) is trades-only, stops before the Mar–Aug 2026 window, and is not a book history. Do not treat it as maker WF input. Kalshi Data Terms forbid redistributing archived datasets and training ML without written consent; pull official REST for this project.

---

## 6. Paper-validate path (Claude Code, now)

Until a maker WF can PASS, paper is the only execution path. Use **Kalshi demo** for orders (`https://demo.kalshi.co/`, API `https://external-api.demo.kalshi.co/trade-api/v2`). Demo credentials are not production. Demo prices “may not be reflective of real markets.”

### 6.1 Quote off the live book, not candles

For every intended order:

1. `GET /markets/{ticker}/orderbook` (or authenticated WS `orderbook_snapshot` / `orderbook_delta` — WS connection itself requires API keys even for public channels).
2. Read **current** yes bids / no bids. Asks are implied: yes ask ≈ `1 −` best no bid (see Kalshi orderbook docs).
3. Post a **resting** bid on a favorite (`p >= 0.55` on the intended price). Maker only. Never take `p < 0.20`.
4. Size: `stake = current_equity * 0.01`. Kalshi min size 0.01 contracts. Do not exceed 1% notional.
5. Count a fill **only** if Kalshi reports the demo order executed as maker (resting order later matched). If it takes liquidity, that fill is a **protocol violation**, not a data point for this edge.
6. Log: timestamp, ticker, side, limit, size, **live BBO at send**, order id, maker/taker flag on fill, fee charged, equity after.

No fill in the log ⇒ no PnL row. Unfilled quotes are not losses except opportunity; do not fabricate them.

### 6.2 Record deltas going forward (this is how the FAIL eventually lifts)

Start a recorder **today**. This is the only free path to a future maker WF.

Write under `data/kalshi/book/` (gitignored; do not commit market data):

- Snapshot cadence: each `orderbook_delta` or, if WS is down, poll `GET /markets/{ticker}/orderbook` with timestamps.
- Fields: `ts`, `ticker`, `yes_bids[]` and `no_bids[]` as `[price, size]`, source (`ws`|`rest`).
- Also log trades and settlements for the same tickers (`data/kalshi/trades/`, `data/kalshi/settlements/`).
- Retention: keep **180+ calendar days** before anyone may attempt a maker WF.
- Universe: start with markets you will actually quote (favorites, `p >= 0.55` candidates). Document the ticker list in `data/kalshi/universe.md`.

Clock starts when the first durable snapshot is on disk. Days of public *trade* history do not count toward this 180. Candle history does not count.

When 180 days of **book** files exist, re-run this gate. Only then may `walk_forward` consume that recording, with fees + spread from the recorded BBO, fill logic from queue/size at our price, and 1% risk. Until that date, the maker WF line stays **FAIL**.

### 6.3 Wiring tests vs claims

`make simulate` / synthetic `walk_forward` may run as a **wiring test**. Label output `mode=paper (synthetic replay — not a claim of edge)`. Never copy synthetic equity into claims, PRs, or live-go memos.

---

## 7. Fees and spread (required on every scored fill)

Costs are required. Missing costs ⇒ FAIL (already tested in `tests/test_backtest.py`).

### 7.1 Spread

- **Paper now:** spread = live `yes_ask − yes_bid` (or implied ask) **at send**, from the book in §6.1.
- **Future maker WF:** spread from recorded BBO at the quote timestamp. Not a flat `spread_bps` guess. Not candle OHLC.
- Engine default `10 bps fee + 20 bps spread` is a **generic haircut for synthetic wiring only**. It is not Kalshi.

### 7.2 Fees (2026, public pages; live PDF unread)

Live `https://kalshi.com/docs/kalshi-fee-schedule.pdf` returned **HTTP 429** on 2026-08-29. Do not pretend to have read today’s PDF.

Retrieved official sources:

- Wayback 2026-06-12 of “Fee Schedule for Feb 2026 - 2.5.26 Update” (effective Feb 5, 2026):
  - Taker (immediate match): `round up(0.07 × C × P × (1−P))`
  - Maker, only if the series is in the Maker Fees list, and only when a resting order later executes: `round up(0.0175 × C × P × (1−P))`
  - Cancel is free. Same formula at longshots and favorites (symmetric in `P(1−P)`).
- Live `docs.kalshi.com` (HTTP 200, 2026-08-29) still points at that PDF and adds:
  - Series `FeeMultiplier` **M**
  - `fee_type`: `quadratic` (taker table) | `quadratic_with_maker_fees` (table + maker section, standard maker multiplier 0.25) | `quadratic_with_combo_maker_fees` (0.5 instead of 0.25; changelog 2026-08-21) | `flat`
  - Rounding: `fee_rounding.md` (ceil to $0.000001, then penny/direct rounding)

Implementation: read `fee_type` and `fee_multiplier` from the series endpoint **per ticker**. Apply maker formula only on `quadratic_with_maker_fees` / combo maker types when the fill is maker. On `quadratic` (example: `KXHIGHNY` observed `fee_type=quadratic`, `M=1`), resting fills are **not** in the maker-fee section of that PDF.

Gap: coefficients are **not** verified against the unread live PDF. If the live PDF becomes readable, replace this subsection and keep the Wayback citation as history. Unofficial “Jul 7, 2026 reprint” was not retrieved; do not use it.

Perps fees are a different notional/tier schedule. Out of scope for this $50 event-contract bot.

---

## 8. Success / fail gates (checklist)

Claude Code must print one of `PASS` | `FAIL` | `PAPER-ONLY` for each row. No silent skip.

### 8.1 Maker walk-forward (historical)

| Gate | Pass if | Fail if |
| --- | --- | --- |
| Span | ≥ 180 calendar days of **book recordings** (or licensed L2 Ozirus paid extra for) | Using trade span, candle span, or synthetic days |
| Book | Timestamped BBO or L2 with size at levels | Candle OHLC, last trade, mid, or invented quotes |
| Fills | Fill model uses recorded size/queue at our limit; unfilled = no row | Assumed fills, “hit every print,” full-book size |
| Maker vs taker | Each scored fill classified from **our order** (resting vs taking) | Tape `taker_book_side` used as if we were the maker |
| Settlement | Real `result` / `settlement_value_dollars` | Guessed outcomes |
| Fees | Series `fee_type` + M + 2026 formula from §7.2 | 2022 makers-free, silent 10 bps, or invented bps |
| Spread | From recorded BBO at quote time | Flat bps, candle bar, or zero |
| Risk | Each stake ≤ 1% of **then** equity | Size-up, full Kelly, >1% |
| Sleeves | Weights stay > 0 (no death) | Killing sleeves to juice PnL |
| Claim | Report computed numbers from the file | Literature +2.6%, placeholders, or empty `data/` |

**Current overall: FAIL** (book history missing). Re-evaluate only after §6.2 has 180 days.

### 8.2 Paper-validate (demo, live book)

| Gate | Pass if | Fail if |
| --- | --- | --- |
| Venue | Kalshi demo API, signed RSA keys, paper mode | Production live, Polymarket Global, random bots |
| Book | Live orderbook at send time in the log | Candles or last price as the quote |
| Side | Resting bids, `p >= 0.55`, no take `p < 0.20` | Taker hits, longshot takes |
| Size | 1% of current demo equity | Oversize |
| Fills | Only Kalshi-reported maker executions | Hypothetical fills |
| Recorder | Book deltas writing to `data/kalshi/book/` | Papering without recording (WF clock never starts) |
| Output label | `PAPER-ONLY` — not a WF PASS | Calling paper PnL a walk-forward |

Paper **PASS** means: the bot can post, log, respect 1%, and record books. It does **not** unlock live or a maker-edge claim.

### 8.3 Go-live (not this file’s PASS today)

Live production requires: paper path stable, maker WF **PASS** on recorded (or extra-paid) L2, 1% still on, US/Kalshi only. Until WF PASS, go-live is **FAIL**.

---

## 9. Claude Code CLI — required behavior

1. Read this file before any backtest or “results” task.
2. If the user (or another agent) asks for maker WF PnL without §8.1 PASS inputs, answer **FAIL** and cite §3. Do not start a proxy.
3. Implement §6.2 recorder before optimizing sleeves on synthetic data.
4. Wire Kalshi fees from series `fee_type` / `M`, not `fee_bps=10`.
5. Keep `walk_forward(..., fee_bps=..., spread_bps=...)` costs required; when real books exist, replace bps with per-fill fee + recorded spread.
6. Never commit secrets, demo keys, or `data/kalshi/**` book dumps.
7. Budget: Claude Code CLI, $50, 1%. No social-bot installs, no VPN, no licensed data unless Ozirus spends extra.

---

## 10. Status line (update in place, do not rewrite history)

```
date: 2026-08-29
maker_walk_forward: FAIL
reason: no historical L2/BBO; public API is trades + settlements + candle bid/ask OHLC + live book only
candle_as_maker: forbidden
licensed_books: forbidden unless spend > $50 bankroll
paper_validate: allowed on Kalshi demo off live book
book_recorder: required; 180-day clock starts at first snapshot on disk
risk: 1% of current equity
strategy: A Kalshi maker fade-longshot
```
