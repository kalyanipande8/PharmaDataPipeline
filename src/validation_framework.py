"""Real 18-check automated validation framework -- a flat rule list
interpreted by a small dispatch table, covering every pharma QC field
in the dataset, measuring real first-pass data quality compliance."""
from __future__ import annotations

import pandas as pd


def _range_violation(df, field, lo, hi):
    return ~df[field].between(lo, hi)


def _missing_violation(df, field):
    return df[field].isna()


RULES = [
    {"name": "yield_range", "check": _range_violation, "params": {"field": "yield_pct", "lo": 0, "hi": 110}},
    {"name": "temperature_range", "check": _range_violation, "params": {"field": "temperature_c", "lo": 20, "hi": 50}},
    {"name": "ph_range", "check": _range_violation, "params": {"field": "ph_level", "lo": 1, "hi": 13}},
    {"name": "pressure_range", "check": _range_violation, "params": {"field": "pressure_kpa", "lo": 50, "hi": 200}},
    {"name": "weight_range", "check": _range_violation, "params": {"field": "weight_g", "lo": 300, "hi": 700}},
    {"name": "viscosity_range", "check": _range_violation, "params": {"field": "viscosity_cp", "lo": 100, "hi": 600}},
    {"name": "moisture_range", "check": _range_violation, "params": {"field": "moisture_pct", "lo": 0, "hi": 10}},
    {"name": "particle_size_range", "check": _range_violation, "params": {"field": "particle_size_um", "lo": 0, "hi": 200}},
    {"name": "shelf_life_range", "check": _range_violation, "params": {"field": "shelf_life_days", "lo": 1, "hi": 1460}},
    {"name": "operator_id_range", "check": _range_violation, "params": {"field": "operator_id", "lo": 1, "hi": 50}},
    {"name": "missing_record_id", "check": _missing_violation, "params": {"field": "record_id"}},
    {"name": "missing_batch_id", "check": _missing_violation, "params": {"field": "batch_id"}},
    {"name": "missing_lot_number", "check": _missing_violation, "params": {"field": "lot_number"}},
    {"name": "missing_yield", "check": _missing_violation, "params": {"field": "yield_pct"}},
    {"name": "missing_temperature", "check": _missing_violation, "params": {"field": "temperature_c"}},
    {"name": "missing_ph", "check": _missing_violation, "params": {"field": "ph_level"}},
    {"name": "missing_weight", "check": _missing_violation, "params": {"field": "weight_g"}},
    {"name": "quality_flag_valid", "check": lambda df, field: ~df[field].isin([0, 1]), "params": {"field": "quality_pass"}},
]

assert len(RULES) == 18


def run_validation(df: pd.DataFrame) -> dict:
    flags = {}
    for rule in RULES:
        mask = rule["check"](df, **rule["params"])
        flags[rule["name"]] = set(df.index[mask])
    return flags


def first_pass_compliance(df: pd.DataFrame, flags: dict) -> dict:
    any_flagged = set()
    for s in flags.values():
        any_flagged |= s
    compliance_pct = round(100 * (1 - len(any_flagged) / len(df)), 2)
    return {"n_records": len(df), "n_flagged": len(any_flagged), "first_pass_compliance_pct": compliance_pct,
            "n_checks": len(RULES)}
