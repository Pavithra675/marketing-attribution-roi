# Validation Report

## 1. Overview

This report summarizes the validation and testing performed on the Marketing Attribution and ROI Analysis prototype.

## 2. Dataset Validation

The original dataset validation was executed using `validate.py`.

| Entity | Record Count |
|---|---:|
| Campaigns | 100 |
| Contacts | 1,000 |
| Touchpoints | 5,000 |
| Leads | 500 |
| Opportunities | 200 |
| Orders | 52 |
| Cost Records | 100 |
| Attribution Results | 47 |

**Result:** ALL VALIDATION CHECKS PASSED.

## 3. Automated Testing

Test command:

`python -m pytest -q`

Result:

**7 passed**

## 4. Anomaly Detection Results

Five injected anomaly scenarios were tested using separate datasets.

| Anomaly ID | Scenario | Expected Decision | Observed Decision |
|---|---|---|---|
| ANOM-001 | Revenue double count | FLAG | FLAG |
| ANOM-002 | Touchpoint after conversion | FLAG | FLAG |
| ANOM-003 | Spend currency mismatch | FLAG | FLAG |
| ANOM-004 | Campaign cost omitted | FLAG | FLAG |
| ANOM-005 | Anonymous session linked without evidence | FLAG | FLAG |

**Result:** All five injected anomalies were detected.

## 5. Reproducibility

The synthetic data generator uses a fixed random seed: `20261022`.

## 6. Limitations

- The current dataset is smaller than the requested target scale.
- Anomaly detectors currently demonstrate the five injected scenarios.
- The workflow is primarily CSV-based.
- The anomaly datasets are separate from the original datasets.

## 7. Conclusion

The prototype successfully demonstrates synthetic data generation, marketing attribution, ROI and ROAS calculations, data validation, automated testing, and detection of five injected anomaly scenarios.