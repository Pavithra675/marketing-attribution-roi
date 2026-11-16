# Marketing Attribution & ROI — Validation Report

## 1. Project Configuration

- Random seed: 20261022
- Attribution lookback window: 180 days
- Primary currency: INR
- Dataset format: CSV
- Additional exports: JSON and SQLite

## 2. Generated Dataset Counts

| Dataset | Records |
|---|---:|
| Campaigns | 500 |
| Channels | 5 |
| Creatives | 50 |
| Audiences | 25 |
| Contacts | 50,000 |
| Touchpoints | 200,000 |
| Web Sessions | 200,000 |
| Leads | 25,000 |
| Opportunities | 10,000 |
| Orders | 2,563 |
| Cost Records | 500 |
| Campaign-Creative Links | 500 |
| Campaign-Audience Links | 500 |
| Attribution Results | 11,667 |
| Campaign ROI Report | 1,500 |
| Unattributed Orders | 0 |

## 3. Attribution Validation

Three attribution models are implemented:

- First Touch
- Last Touch
- Linear

Latest results:

| Model | Orders Reconciled | Attributed Revenue |
|---|---:|---:|
| First Touch | 2,563 | 134,045,294 |
| Last Touch | 2,563 | 134,045,294 |
| Linear | 2,563 | 134,045,294 |

The attribution process:
- Uses a 180-day conversion lookback window.
- Excludes touchpoints after the order date.
- Reconciles attributed revenue against eligible order revenue.
- Reports orders without eligible touchpoints.

All 2,563 orders have eligible touchpoints.
Unattributed orders: 0.
Unattributed revenue: 0.

## 4. ROI Validation

- ROI calculated for 500 campaigns under each attribution model.
- Total campaign-model ROI records: 1,500.
- All baseline campaign costs are available.
- Campaign and cost currencies match (INR).

## 5. Data Quality Validation

The validation process checks:
- Missing and duplicate primary keys.
- Foreign key references.
- Opportunity and lead contact consistency.
- Order and opportunity lifecycle consistency.
- Allowed status and attribution model values.
- Touchpoint dates against conversion dates.
- Duplicate attribution records.
- Revenue reconciliation.
- Positive campaign costs.
- Campaign and cost currency consistency.

Latest core validation:

**ALL VALIDATION CHECKS PASSED**

Additional entity validation:

**ALL ADDITIONAL ENTITY CHECKS PASSED**

Automated tests:

**7 PASSED**

## 6. Anomaly Detection Scenarios

| ID | Anomaly | Expected Result |
|---|---|---|
| ANOM-001 | Revenue double-counted | FLAG |
| ANOM-002 | Touchpoint after conversion | FLAG |
| ANOM-003 | Spend currency mismatch | FLAG |
| ANOM-004 | Campaign cost omitted | FLAG |
| ANOM-005 | Anonymous session linked without evidence | FLAG |

Ground-truth labels are stored separately in `anomaly_data/ground_truth.csv`.

## 7. Export Validation

- 16 JSON dataset exports generated.
- 16 SQLite tables created.
- SQL schema exported.
- Unattributed orders exported separately.