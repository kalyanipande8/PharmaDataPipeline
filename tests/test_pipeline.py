import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.simulate_records import simulate
from src.etl_pipeline import run_etl
from src.validation_framework import run_validation, first_pass_compliance, RULES


def test_at_least_800_records():
    df, _ = simulate()
    assert len(df) >= 800


def test_18_checks_defined():
    assert len(RULES) == 18


def test_etl_loads_into_sqlite(tmp_path):
    df, _ = simulate()
    db_path = str(tmp_path / "test.db")
    transformed = run_etl(df, db_path)
    assert os.path.exists(db_path)
    assert "in_spec_yield" in transformed.columns


def test_first_pass_compliance_is_high():
    df, _ = simulate()
    flags = run_validation(df)
    compliance = first_pass_compliance(df, flags)
    assert compliance["first_pass_compliance_pct"] >= 85.0


def test_validation_recalls_most_true_violations():
    df, true_violations = simulate()
    flags = run_validation(df)
    any_flagged_idx = set.union(*flags.values())
    flagged_ids = set(df.loc[list(any_flagged_idx), "record_id"])
    tp = len(flagged_ids & true_violations)
    recall = tp / len(true_violations)
    assert recall >= 0.9
