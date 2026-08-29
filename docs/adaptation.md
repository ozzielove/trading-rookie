# Adaptation (not genetic death)

People describe bots that clone winners and kill losers. That is a discrete genetic algorithm. It overfits, it forgets, and it cannot recover a sleeve that was merely out of regime.

Trading Rookie is Lamarckian / Bayesian:

| Genetic farm | Trading Rookie |
| --- | --- |
| Fitness → kill | Fitness → down-weight |
| Clone winners | Morph winners *and* losers |
| Population turnover | Population only grows |
| Static DNA until death | Parameters drift every tick |
| One champion deployed | Mixture always on |

Fully able to adapt means: after a regime break, weights move, forms morph, a new sleeve can appear, and a previously cold sleeve can heat back up without being re-created from scratch. The 1% risk cap does not adapt away.
