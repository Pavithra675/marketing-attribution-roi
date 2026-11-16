# Marketing Attribution and ROI Analysis

## 1. Project Overview

This project is a Python-based Marketing Attribution and ROI Analysis system. It connects marketing campaigns, customer interactions, leads, opportunities, orders, and campaign costs to measure marketing performance.

The system calculates attributed revenue using three attribution models and generates campaign-level ROI and ROAS reports. It also includes data validation and five injected anomaly scenarios with detection scripts and ground-truth labels.

## 2. Technologies Used

- Python 3.11
- Pandas
- NumPy
- Pytest
- CSV for data storage and exchange
- Git and GitHub for version control

## 3. Project Workflow

1. Generate reproducible synthetic marketing data.
2. Connect campaign touchpoints with contacts.
3. Connect leads with opportunities and orders.
4. Calculate attributed revenue using three attribution models.
5. Generate campaign-level ROI and ROAS reports.
6. Validate data quality and relationships.
7. Inject five labeled anomaly scenarios.
8. Run anomaly detection scripts.
9. Execute automated tests.

## 4. Attribution Models

The system supports three attribution models:

- **First-Touch:** Credits the first eligible touchpoint with the order's revenue.
- **Last-Touch:** Credits the last eligible touchpoint with the order's revenue.
- **Linear:** Distributes the order's revenue equally across eligible touchpoints.

The current implementation uses a 30-day lookback window. Touchpoints occurring after an order are excluded from attribution.

## 5. ROI and ROAS

**ROI:**
`ROI (%) = ((Attributed Revenue - Campaign Cost) / Campaign Cost) * 100`

**ROAS:**

`ROAS = Attributed Revenue / Campaign Cost`

Missing campaign costs must not be treated as zero. ROI and ROAS should not be calculated when the required cost record is missing.

## 6. Generated Data Files

- `campaigns.csv`
- `contacts.csv`
- `touchpoints.csv`
- `leads.csv`
- `opportunities.csv`
- `orders.csv`
- `cost_records.csv`
- `attribution_results.csv`
- `campaign_roi_report.csv`

## 7. Anomaly Detection Scenarios

Five separate anomaly scenarios are injected into test datasets. Their expected decisions are recorded in `anomaly_data/ground_truth.csv`.

| ID | Anomaly | Expected decision |
|---|---|---|
| ANOM-001 | Revenue double counting | FLAG |
| ANOM-002 | Touchpoint after conversion | FLAG |
| ANOM-003 | Campaign spend currency mismatch | FLAG |
| ANOM-004 | Campaign cost omitted | FLAG |
| ANOM-005 | Anonymous session linked without identity evidence | FLAG |

Each scenario has an injection script and a corresponding detection script.

### Anomaly scripts

- `inject_anomalies.py` and `detect_anomalies.py`
- `inject_anomaly2.py` and `detect_anomaly2.py`
- `inject_anomaly3.py` and `detect_anomaly3.py`
- `inject_anomaly4.py` and `detect_anomaly4.py`
- `inject_anomaly5.py` and `detect_anomaly5.py`

The fifth scenario also creates `web_sessions.csv` and a separate anomalous session dataset.

**Important:** The current anomaly detectors demonstrate detection of the five injected test cases. They are not yet general-purpose detectors for every possible anomaly.

## 8. Data Validation

The validation script checks:

- Missing and duplicate primary keys.
- Invalid foreign key references.
- Lead and opportunity contact consistency.
- Orders linked to Won opportunities.
- Attribution revenue reconciliation.
- Positive campaign costs.

Run validation with:

```bash
python validate.py
```

## 9. Automated Testing

Automated tests are implemented using Pytest.

Latest test result:

**7 passed**

Run tests using:

```bash
python -m pytest -q
```

## 10. Current Dataset Size

| Entity | Records |
|---|---:|
| Campaigns | 100 |
| Contacts | 1,000 |
| Touchpoints | 5,000 |
| Leads | 500 |
| Opportunities | 200 |
| Orders | 52 |
| Cost records | 100 |
| Attribution rows | 47 |

The dataset contains synthetic demonstration records.

## 11. How to Run

Install dependencies:

```bash
python -m pip install pandas numpy pytest
```

Generate data:

```bash
python generator.py
```

Run attribution:

```bash
python attribution.py
```

Calculate ROI:

```bash
python roi.py
```

Validate data:

```bash
python validate.py
```

Run automated tests:

```bash
python -m pytest -q
```

Run all five anomaly detectors:

```bash
python detect_anomalies.py
python detect_anomaly2.py
python detect_anomaly3.py
python detect_anomaly4.py
python detect_anomaly5.py
```

## 12. Reproducibility

The data generator uses a fixed random seed (`20261022`) to support repeatable synthetic data generation.

## 13. Current Scope and Limitations

This is a working prototype demonstrating marketing attribution, ROI calculation, data validation, and five labeled anomaly scenarios.

The current dataset is smaller than the full target scale of 500 campaigns, 50,000 contacts, 200,000 touchpoints, and 10,000 opportunities.

The current workflow is primarily CSV-based. The anomaly scenarios use separate test datasets to avoid modifying the original generated data.

The project can be extended with larger datasets, integrated database workflows, broader anomaly detection, and additional reporting capabilities.

## 14. Repository

GitHub: https://github.com/Pavithra675/marketing-attribution-roi