# Marketing Attribution & ROI — Source Manifest

## 1. Project Overview

This project generates synthetic marketing data, calculates attribution using three models, calculates campaign ROI, validates data quality, detects injected anomalies, and exports results.

Random seed: `20261022`

Attribution lookback window: 180 days.

## 2. Python Source Files

| File | Purpose |
|---|---|
| `generator.py` | Generates core marketing datasets |
| `generate_entities.py` | Generates channels, creatives, audiences, bridge tables, and web sessions |
| `attribution.py` | Calculates First Touch, Last Touch, and Linear attribution |
| `roi.py` | Calculates campaign ROI and ROAS |
| `validate.py` | Validates core datasets and attribution results |
| `validate_entities.py` | Validates additional entities and relationships |
| `export_data.py` | Exports CSV datasets to JSON and SQLite |
| `database.py` | Defines SQLAlchemy database connection configuration |
| `models.py` | Defines SQLAlchemy entity models |
| `test_data.py` | Contains automated tests |
| `inject_anomalies.py` | Creates the revenue double-counting anomaly |
| `inject_anomaly2.py` | Creates the post-conversion touchpoint anomaly |
| `inject_anomaly3.py` | Creates the currency mismatch anomaly |
| `inject_anomaly4.py` | Creates the missing campaign cost anomaly |
| `inject_anomaly5.py` | Creates the unsupported anonymous session identity-link anomaly |
| `detect_anomalies.py` | Detects revenue double-counting |
| `detect_anomaly2.py` | Detects post-conversion touchpoints |
| `detect_anomaly3.py` | Detects currency mismatches |
| `detect_anomaly4.py` | Detects missing campaign costs |
| `detect_anomaly5.py` | Detects unsupported anonymous session identity links |

## 3. Core Generated CSV Datasets

| File | Contents |
|---|---|
| `campaigns.csv` | Campaign master data |
| `contacts.csv` | Contact master data |
| `touchpoints.csv` | Marketing interactions |
| `leads.csv` | Lead records |
| `opportunities.csv` | Sales opportunities |
| `orders.csv` | Completed order and revenue records |
| `cost_records.csv` | Campaign marketing spend |
| `attribution_results.csv` | Revenue attributed under three models |
| `campaign_roi_report.csv` | Campaign ROI and ROAS results |

## 4. Additional Generated CSV Datasets

| File | Contents |
|---|---|
| `channels.csv` | Marketing channel master data |
| `creatives.csv` | Creative master data |
| `audiences.csv` | Audience segments |
| `campaign_creatives.csv` | Campaign-to-creative relationships |
| `campaign_audiences.csv` | Campaign-to-audience relationships |
| `web_sessions.csv` | Identified and anonymous web sessions |

## 5. Anomaly Test Data

Location: `anomaly_data/`

| File | Purpose |
|---|---|
| `ground_truth.csv` | Expected anomaly labels |
| `attribution_with_double_count.csv` | Revenue double-counting test data |
| `touchpoints_after_conversion.csv` | Post-conversion touchpoint test data |
| `attribution_after_conversion.csv` | Attribution data for the post-conversion test |
| `costs_currency_mismatch.csv` | Currency mismatch test data |
| `costs_omitted.csv` | Missing campaign cost test data |
| `web_sessions_anonymous_link.csv` | Unsupported anonymous identity-link test data |

The anomaly datasets are kept separate from the valid baseline datasets.

## 6. Export Directory

Location: `exports/`

Contains:
- JSON versions of generated CSV datasets.
- `marketing_attribution.db`, the SQLite export database.
- `schema.sql`, containing exported SQL table definitions.

The SQLite export provides portable data tables. The pandas-based export does not enforce all foreign-key constraints.

## 7. Documentation and Configuration

| File | Purpose |
|---|---|
| `README.md` | Project overview, setup, and execution instructions |
| `DATA_DICTIONARY.md` | Dataset fields and relationships |
| `VALIDATION_REPORT.md` | Validation, anomaly, and test results |
| `SOURCE_MANIFEST.md` | Project file and dataset inventory |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Files and folders excluded from Git |

## 8. Dataset Scale

| Entity | Records |
|---|---:|
| Campaigns | 500 |
| Contacts | 50,000 |
| Touchpoints | 200,000 |
| Leads | 25,000 |
| Opportunities | 10,000 |
| Orders | 2,563 |
| Cost Records | 500 |
| Web Sessions | 200,000 |

## 9. Execution Order

Run commands from the project root:

1. `generator.py`
2. `generate_entities.py`
3. `attribution.py`
4. `roi.py`
5. `validate.py`
6. `validate_entities.py`
7. `export_data.py`
8. `python -m pytest -q`

Use the project's virtual environment Python executable when running commands in Windows PowerShell.

## 10. Reproducibility

The generators use the fixed seed `20261022`.

Two runs produced matching SHA-256 hashes for seven core CSV datasets: campaigns, contacts, touchpoints, leads, opportunities, orders, and cost records.