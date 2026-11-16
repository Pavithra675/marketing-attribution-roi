# Marketing Attribution and ROI Analysis

## Project Overview

This project analyzes marketing campaign performance by connecting campaign interactions, contacts, leads, opportunities, orders, and campaign costs.

It calculates attributed revenue using three attribution models and generates campaign-level ROI and ROAS reports.

## Technologies Used

- Python 3.11
- Pandas
- NumPy
- Pytest

## Project Workflow

1. Generate synthetic marketing data.
2. Connect touchpoints with contacts and campaigns.
3. Connect leads with opportunities and orders.
4. Calculate attributed revenue using First-Touch, Last-Touch, and Linear attribution.
5. Calculate campaign ROI and ROAS.
6. Validate data quality and relationships.
7. Run automated tests.

## Attribution Models

- **First-Touch:** Credits the first eligible touchpoint with the order's revenue.
- **Last-Touch:** Credits the last eligible touchpoint with the order's revenue.
- **Linear:** Distributes the order's revenue equally across eligible touchpoints.

The current implementation uses a 30-day lookback window. Touchpoints after an order are excluded.

## ROI and ROAS

ROI is calculated as:

`ROI (%) = ((Attributed Revenue - Campaign Cost) / Campaign Cost) × 100`

ROAS is calculated as:

`ROAS = Attributed Revenue / Campaign Cost`

## Generated Data Files

- `campaigns.csv`
- `contacts.csv`
- `touchpoints.csv`
- `leads.csv`
- `opportunities.csv`
- `orders.csv`
- `cost_records.csv`
- `attribution_results.csv`
- `campaign_roi_report.csv`

## How to Run

### 1. Install dependencies

```bash
python -m pip install pandas numpy pytest
```

### 2. Generate data

```bash
python generator.py
```

### 3. Run attribution

```bash
python attribution.py
```

### 4. Calculate ROI

```bash
python roi.py
```

### 5. Validate data

```bash
python validate.py
```

### 6. Run automated tests

```bash
python -m pytest -q
```

## Data Validation

The validation script checks:

- Missing and duplicate primary keys.
- Invalid foreign key references.
- Lead and opportunity contact consistency.
- Orders linked to Won opportunities.
- Attribution revenue reconciliation.
- Positive campaign costs.

## Testing

Automated tests are written using Pytest.

Current result: **7 tests passed.**

## Current Dataset Size

| Entity | Records |
|---|---:|
| Campaigns | 100 |
| Contacts | 1,000 |
| Touchpoints | 5,000 |
| Leads | 500 |
| Opportunities | 200 |
| Orders | 52 |
| Cost records | 100 |

These are synthetic demonstration records.

## Current Scope and Limitations

This is an initial working prototype. It does not yet implement the full target dataset scale or all five required anomaly scenarios. The current reports should be interpreted as results from synthetic data, not real marketing performance.

## Reproducibility

The data generator uses a fixed random seed (`20261022`) to support repeatable data generation.
