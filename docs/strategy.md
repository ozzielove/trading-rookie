# Strategy

Not sandstone. The strategy *is* the adaptive loop:

1. Multiple sleeves always alive (value, momentum, liquidity, event drift, plus spawns).
2. Posterior weights update every outcome. Floor weight so nothing dies.
3. Each sleeve morphs parameters online (polymorphic form).
4. Structured residual error spawns a new sleeve. Old ones remain.
5. Regime state (quiet / thin / stress / event) is a feature, not a hard switch that zeros anyone.
6. Size is always `0.01 * equity`, then split by weights.

Venue-specific edges (Polymarket mispricing, copy-trading, maker rebates, etc.) get attached as new sleeves once research lands and a walk-forward with real data passes. Until then, `python -m trading_rookie simulate` is a synthetic wiring test, not an edge claim.
