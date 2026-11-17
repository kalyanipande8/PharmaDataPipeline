"""Real ETL pipeline: extracts the raw records, applies a light
transform (derived QC-pass-rate feature), and loads into a real
SQLite database -- the actual integration-platform step this
project's QC dashboard would query."""
from __future__ import annotations

import sqlite3

import pandas as pd


def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["in_spec_yield"] = df["yield_pct"].between(0, 110)
    return df


def load(df: pd.DataFrame, db_path: str):
    conn = sqlite3.connect(db_path)
    df.to_sql("pharma_records", conn, if_exists="replace", index=False)
    conn.close()


def run_etl(df: pd.DataFrame, db_path: str) -> pd.DataFrame:
    transformed = transform(df)
    load(transformed, db_path)
    return transformed
