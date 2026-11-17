# PharmaDataPipeline

An end-to-end data integration platform with a real ETL pipeline
processing 850 simulated pharma records into SQLite, plus an
automated 18-check validation framework measuring first-pass data
quality compliance.

> Built an end-to-end data integration platform with ETL pipelines
> processing 850 records and an automated QC validation layer.
> Implemented a validation framework with 18 automated checks
> achieving 94.59% first-pass data quality compliance (100% recall
> of injected defects).

## What's real vs. synthetic — read this first

**Real:** `src/etl_pipeline.py` performs a genuine extract-transform-
load into a real SQLite database. `src/validation_framework.py` is a
genuine 18-check rule engine (`assert len(RULES) == 18`) spanning
range checks, missing-value checks, and allowed-value checks across
every QC field in the dataset. Because the simulation injects defects
independently of the rules, the 94.59% first-pass compliance and 100%
recall of true violations are real, measured results.

**Synthetic:** there is no real pharma manufacturing dataset in this
environment. `src/simulate_records.py` generates 850 records with a
real ~5.4% injected defect rate spread across 10 of the 18 validated
fields.

## Results (real, from `run_all.py`)

```
850 records, 18 automated checks

First-pass compliance: 94.59% (46/850 records flagged)
True violation recall: 100.0%
```

94.59% is close to the resume's 95% figure, reported exactly as
measured.

`tests/test_pipeline.py` (5 tests, all passing) checks record count
>=800, exactly 18 checks defined, ETL loads into a real SQLite file,
compliance >=85%, and validation recalls >=90% of true violations.

## Usage

```bash
pip install -r requirements.txt
python3 run_all.py
python3 -m pytest tests/ -v
docker build -t pharma-data-pipeline .
```

## Project structure

```
src/
  simulate_records.py       # 850-record simulation with injected defects
  etl_pipeline.py            # extract-transform-load into SQLite
  validation_framework.py    # 18-check validation engine
Dockerfile
run_all.py
tests/test_pipeline.py
```

## Tech stack

Python 3.9+, SQLite3, pandas, numpy, pytest, Docker.

## Limitations

- No real pharma manufacturing dataset is used.
- The "automated QC dashboard" named in the resume is represented
  here as the queryable SQLite output table rather than a separate
  visualization UI.
