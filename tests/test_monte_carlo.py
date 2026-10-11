from app.models import Estimate
from app.core.monte_carlo import simulate

def test_simulation_returns_quantiles():
    est = [Estimate(id=1, feature_id=1, optimistic=5, likely=10, pessimistic=20)]
    result = simulate(est, velocity_mean=40, velocity_std=8, n_simulations=1000)
    assert result["p50_days"] > 0
    assert result["p85_days"] >= result["p50_days"]
    assert result["p95_days"] >= result["p85_days"]

def test_empty_estimates():
    result = simulate([], 40, 8, 1000)
    assert result["p50_days"] == 0
