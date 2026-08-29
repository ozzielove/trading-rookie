from trading_rookie.config import Config
from trading_rookie.learner import Learner


def test_stake_is_one_percent():
    cfg = Config(bankroll=50, risk_pct=0.01)
    assert cfg.stake(50) == 0.5
    assert cfg.stake(80) == 0.8


def test_weights_never_die():
    cfg = Config(min_weight=0.05)
    learner = Learner(cfg)
    n = len(learner.ensemble.sleeves)
    for i in range(40):
        learner.step(
            {"edge": 0.2, "momentum": 0.1, "liquidity": 0.8},
            realized=1.0 if i % 3 else -1.0,
        )
    w = learner.ensemble.weights()
    assert len(w) >= n
    assert abs(sum(w) - 1.0) < 1e-6
    assert min(w) >= learner.ensemble.live_floor() - 1e-9
    assert min(w) > 0.0


def test_morph_keeps_sleeve_identity():
    learner = Learner(Config())
    names_before = [s.name for s in learner.ensemble.sleeves]
    snap0 = learner.ensemble.sleeves[0].snapshot()
    learner.step({"edge": 0.4, "momentum": -0.2, "liquidity": 0.5}, realized=-0.3)
    names_after = [s.name for s in learner.ensemble.sleeves]
    for name in names_before:
        assert name in names_after
    snap1 = learner.ensemble.sleeves[0].snapshot()
    assert snap1["n_updates"] > snap0["n_updates"]
