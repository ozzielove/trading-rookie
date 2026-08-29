# Logic predicates

All must hold or do not order.

- venue == Kalshi demo until live asked. Reject Global CLOB.
- side == maker bid. v1 no takes.
- price >= 0.50. Reject p < 0.50 bids. Reject any p < 0.20 take.
- notional + fees <= 0.01 * equity. Fractional, multiple of 0.01. Hard fail over 1%. Do not allow 5%.
- maker fee known, else fail live; paper may use documented formula with warning.
- 10+20 bps is wrong. 1c tick is about 2% of the $0.50 ticket.
- WF: real books + fees + spread, 180+ days. Missing data FAIL. No candle fills.
- journal why ensemble changed. Sleeves never die.
- LLM is never the price. No model call per tick.
