# Marketing Attribution and ROI Analysis

## 1. Project Overview

A Python-based Marketing Attribution and ROI Analysis system that connects campaigns, contacts, marketing touchpoints, web sessions, leads, opportunities, orders, and campaign costs.

The system compares three attribution models, calculates campaign-level ROI and ROAS, validates data quality, and demonstrates five injected anomaly scenarios with separate ground-truth labels.

All generated records are synthetic demonstration data.

## 2. Technologies

- Python 3.11
- Pandas
- NumPy
- SQLite
- SQLAlchemy
- Pytest
- CSV and JSON
- Git and GitHub

## 3. Project Workflow

1. Generate core marketing datasets using a fixed random seed.
2. Generate channels, creatives, audiences, campaign relationships, and web sessions.
3. Calculate First-Touch, Last-Touch, and Linear attribution.
4. Calculate campaign-level ROI and ROAS.
5. Validate primary keys, foreign keys, dates, relationships, and revenue reconciliation.
6. Inject five separate anomaly scenarios.
7. Detect the injected anomalies and compare their expected decisions.
8. Export CSV datasets to JSON and SQLite.
9. Run automated tests.

## 4. Attribution Models

The attribution script uses a **180-day lookback window**.

- **First-Touch:** Credits the first eligible touchpoint with the order's revenue.
- **Last-Touch:** Credits the last eligible touchpoint with the order's revenue.
- **Linear:** Distributes the order's revenue equally across eligible touchpoints.

Touchpoints occurring after an order are excluded.

Orders without eligible touchpoints are not attributed.

## 5. ROI and ROAS

**ROI (%)**

`((Attributed Revenue - Campaign Cost) / Campaign Cost) * 100`

**ROAS**

`Attributed Revenue / Campaign Cost`

The system checks whether campaign costs exist and whether currencies match before calculating ROI and ROAS. Missing or mismatched costs must not be treated as valid zero-cost records.

## 6. Generated Dataset Scale

The current full-scale generation produces:

| Dataset | Records |
|---|---:|
| Campaigns | 500 |
| Channels | 5 |
| Contacts | 50,000 |
| Touchpoints | 200,000 |
| Web sessions | 200,000 |
| Creatives | 50 |
| Audiences | 25 |
| Campaign-creative relationships | 500 |
| Campaign-audience relationships | 500 |
| Leads | 25,000 |
| Opportunities | 10,000 |
| Orders | 2,563 |
| Cost records | 500 |
| Attribution results | 11,667 |
| Unattributed orders | 0 |
| Campaign ROI report | 1,500 |

The ROI report contains 500 campaign rows for each of the three attribution models.

## 7. Anomaly Scenarios

Five separate anomaly datasets are stored in `anomaly_data/`. The original generated datasets are preserved.

| ID | Scenario | Expected decision |
|---|---|---|
| ANOM-001 | Revenue double counting | FLAG |
| ANOM-002 | Touchpoint after conversion | FLAG |
| ANOM-003 | Campaign spend currency mismatch | FLAG |
| ANOM-004 | Campaign cost omitted | FLAG |
| ANOM-005 | Anonymous session linked without identity evidence and consent | FLAG |

Each scenario has an injection script, a detection script, and a corresponding ground-truth label.

The detectors demonstrate the five injected test cases; they are not general-purpose detectors for every possible anomaly.

## 8. Validation

Run the main validation:

```bash
python validate.py
```

Run additional entity validation:

```bash
python validate_entities.py
```

The validation scripts check identifiers, relationships, attribution chronology, revenue reconciliation, costs, campaign currency consistency, and web-session identity-linking rules.

**Latest result:** All validation checks passed.

**Attribution coverage:** All 2,563 orders have eligible touchpoints within the 180-day lookback window. No orders remain unattributed in the baseline dataset. Unattributed orders are exported separately for auditability.

## 9. Automated Tests

Run:

```bash
python -m pytest -q
```

**Latest result: 7 passed.**

##