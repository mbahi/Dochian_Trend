# Deriv Bot strategies

## digit-matches-guarded.xml

Digit Matches on Volatility 10 (R_10), 1 tick, flat stake, with hard stops.
Load it in Deriv Bot: **Bot builder → Load (folder icon) → Local → Select an XML file**.

Settings live in the *Run once at start* section:

| Variable     | Default | Meaning                                              |
|--------------|---------|------------------------------------------------------|
| Stake        | 0.35    | Stake per trade (Deriv's usual digit minimum)        |
| Prediction   | 3       | Digit to match (0–9)                                 |
| Take Profit  | 1.00    | Stop once session profit ≥ this                      |
| Stop Loss    | 0.70    | Stop once session loss ≥ this                        |
| Max Trades   | 20      | Stop after this many trades regardless               |

No martingale: the stake never increases after a loss.

**This bot has no edge.** Digits on synthetic indices come from an audited RNG, so
every digit is a 1-in-10 draw and Matches pays less than 10×. Expect to lose about
7–8% of everything staked over time. The stops limit how much one session can
cost; they cannot make it profitable. Run it on the demo account first.

## digit_sim.py

Monte Carlo check of common digit "signals" (hot/cold digit, repeat last digit…)
and bankroll outcomes from $1.17. Run with `python3 digit_sim.py`.
