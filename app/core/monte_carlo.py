import numpy as np
from typing import List
from app.models import Estimate

def triangular_sample(est: Estimate, n: int) -> np.ndarray:
    return np.random.triangular(est.optimistic, est.likely,
                                est.pessimistic, n)

def simulate(estimates: List[Estimate], velocity_mean: float,
             velocity_std: float, n_simulations: int) -> dict:
    if not estimates:
        return {"p50_days": 0, "p85_days": 0, "p95_days": 0,
                "mean_days": 0, "histogram": {}}

    total_story_points = np.zeros(n_simulations)
    for est in estimates:
        total_story_points += triangular_sample(est, n_simulations)

    velocities = np.random.normal(velocity_mean, velocity_std, n_simulations)
    velocities = np.clip(velocities, 1.0, None)

    days = total_story_points / velocities * 30  # месяцы в дни

    p50 = float(np.percentile(days, 50))
    p85 = float(np.percentile(days, 85))
    p95 = float(np.percentile(days, 95))
    mean = float(days.mean())

    hist, edges = np.histogram(days, bins=30)
    histogram = {"bins": edges.tolist(), "counts": hist.tolist()}

    return {"p50_days": p50, "p85_days": p85, "p95_days": p95,
            "mean_days": mean, "histogram": histogram}
