# 00 -- Constraints (non-negotiable)

Owner: Book (claims desk). Date: 2026-08-29.
Locked motion: Kalshi maker fade-longshot, p >= 0.50, never take p < 0.20, 1% of $50. Do not reopen unless Ozirus changes the motion.
This file is law for Claude Code CLI. It is not a performance claim. There is no this-bot PnL.

## Operator
- US person. No VPN. No geo-block evasion.
- Venue: Kalshi first. Polymarket US sports is plan B after legal access. Never trade polymarket.com Global.
- Bankroll: $50. Nothing else. No second deposit, no paid data, no paid bot SaaS, no social-install packages.
- Risk: 1% of current equity per trade ($0.50 at start). Fractional Kalshi size required. Validator must not allow 5%.
- Interface: Claude Code CLI locally. Live off until a real-data walk-forward passes.
- Paper, then live. Synthetic simulate is wiring, not edge.

## What the papers actually say (do not paste as our PnL)
Burgi, Deng, and Whelan (Jan 2026), Makers and Takers -- Kalshi 2021 through April 2025, pre-maker-fee:
- Makers, price >= 50c: +2.6% mean, 33% SD. Candidate cell. Not annualized. Not this bot.
- Makers, all prices: -9.64%. Do not make the whole book.
- Takers, all prices: -31.46%. Do not take.
- Price < 10c: worse than -60%. Never take p < 0.20.
Sample ends April 2025 when Kalshi started charging makers. +2.6% is pre-maker-fee.
FLB is weakening, not dead (2025 slope 0.021, still unbiasedness rejected).
Snowberg/Wolfers (2010) too-small-to-trade is horse racing after track take, not Kalshi.
Halldorsson (2026): market p beats tested LLMs on Brier. LLM-as-pricer rejected.
Saguillo et al.: about $40M arb on Polymarket, zero-fee window. Not Kalshi. Not our sleeve.
PolyBench: one-week Polymarket sim, 2 of 7 models print CWR. Not a walk-forward.

## Build this
1. Kalshi maker only: post bids on compressed favorites, p >= 0.50.
2. Never take p < 0.20. Prefer never taking at all in v1.
3. Size = 1% of equity. Fractional contracts. Hard fail if a ticket would exceed 1%.
4. Walk-forward: real Kalshi history, fees + spread, 180+ days, 1% cap. Wire actual Kalshi fees including post-April 2025 maker fees.
5. Live stays off until that gate is green on real data. No invented PnL.

## Do not build
- LLM as pricer
- Taker longshots, p < 0.20, 15-minute crypto
- Combinatorial / rebalancing arb
- Full Kelly or any drop of the 1% cap
- Global CLOB, VPN, geo workarounds
- Social trading packages
- Burgi +2.6% or simulate total_return as this-bot performance
- Paid data, paid signals, a second bankroll

## Claims hygiene
Any PRD number must cite a paper or a walk-forward artifact in this repo. Else it is a hypothesis, not a result. Do not put coffee money in the PRD as a target.
