import json
import os

from src.simulate_records import simulate
from src.etl_pipeline import run_etl
from src.validation_framework import run_validation, first_pass_compliance


def main():
    df, true_violations = simulate()
    os.makedirs("results", exist_ok=True)
    transformed = run_etl(df, "results/pharma.db")

    flags = run_validation(transformed)
    compliance = first_pass_compliance(transformed, flags)

    any_flagged_idx = set.union(*flags.values()) if flags else set()
    flagged_ids = set(transformed.loc[list(any_flagged_idx), "record_id"]) if any_flagged_idx else set()
    tp = len(flagged_ids & true_violations)
    recall = round(100 * tp / len(true_violations), 2) if true_violations else 100.0

    summary = {"n_records": len(df), "compliance": compliance, "true_violation_recall_pct": recall}

    with open("results/summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
