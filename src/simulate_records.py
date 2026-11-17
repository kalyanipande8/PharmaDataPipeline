"""Simulate 850 pharma manufacturing/QC records with fields spanning
18 validation dimensions, with a real ~5% injected defect rate -- the
ground truth the ETL + validation framework must catch."""
from __future__ import annotations

import numpy as np
import pandas as pd

N_RECORDS = 850
SEED = 997


def simulate(n: int = N_RECORDS, seed: int = SEED):
    rng = np.random.default_rng(seed)

    df = pd.DataFrame({
        "record_id": [f"REC-{i:05d}" for i in range(n)],
        "batch_id": [f"B-{i:05d}" for i in range(n)],
        "yield_pct": np.round(rng.normal(92, 5, n), 2),
        "temperature_c": np.round(rng.normal(37, 2, n), 2),
        "ph_level": np.round(rng.normal(7.0, 0.3, n), 2),
        "pressure_kpa": np.round(rng.normal(101, 5, n), 2),
        "weight_g": np.round(rng.normal(500, 20, n), 2),
        "viscosity_cp": np.round(rng.normal(300, 40, n), 2),
        "moisture_pct": np.round(rng.normal(3.0, 0.8, n), 2),
        "particle_size_um": np.round(rng.normal(50, 10, n), 2),
        "shelf_life_days": rng.integers(180, 730, n),
        "operator_id": rng.integers(1, 51, n),
        "lot_number": [f"LOT-{rng.integers(1, 3000)}" for _ in range(n)],
        "quality_pass": rng.choice([0, 1], n, p=[0.06, 0.94]),
    })

    true_violations = set()
    for col, bad_values, rate in [
        ("yield_pct", [-5, 150], 0.01), ("temperature_c", [-10, 80], 0.008),
        ("ph_level", [0.5, 13.5], 0.008), ("pressure_kpa", [0, 500], 0.006),
        ("weight_g", [0, 5000], 0.006), ("viscosity_cp", [-50, 2000], 0.006),
        ("moisture_pct", [-1, 50], 0.005), ("particle_size_um", [-5, 1000], 0.005),
        ("shelf_life_days", [-10, 5000], 0.004), ("operator_id", [0, 999], 0.004),
    ]:
        n_affected = int(n * rate)
        idx = rng.choice(df.index, n_affected, replace=False)
        df.loc[idx, col] = rng.choice(bad_values, n_affected)
        true_violations.update(df.loc[idx, "record_id"])

    return df, true_violations


if __name__ == "__main__":
    df, violations = simulate()
    print(df.shape, len(violations))
