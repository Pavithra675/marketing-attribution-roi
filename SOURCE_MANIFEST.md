# Source Manifest

## 1. Project Information

**Project:** Marketing Attribution and ROI Analysis  
**Language:** Python 3.11  
**Data Format:** CSV  
**Random Seed:** 20261022

## 2. Core Python Scripts

| File | Purpose |
|---|---|
| `generator.py` | Generates synthetic marketing datasets. |
| `attribution.py` | Calculates First-Touch, Last-Touch, and Linear attribution. |
| `roi.py` | Calculates campaign ROI and ROAS. |
| `validate.py` | Validates dataset quality and relationships. |
| `test_data.py` | Contains automated data validation tests. |
| `database.py` | Database configuration code. |
| `models.py` | Defines database models. |

## 3. Anomaly Injection and Detection Scripts

| Injection Script | Detection Script | Scenario |
|---|---|---|
| `inject_anomalies.py` | `detect_anomalies.py` | Revenue double counting |
| `inject_anomaly2.py` | `detect_anomaly2.py` | Touchpoint after conversion |
| `inject_anomaly3.py` | `detect_anomaly3.py` | Spend currency mismatch |
| `inject_anomaly4.py` | `detect_anomaly4.py` | Campaign cost omitted |
| `inject_anomaly5.py` | `detect_anomaly5.py` | Anonymous session linked without evidence |

## 4. Original Generated Datasets

| File | Description |
|---|---|
| `campaigns.csv` | Campaign information. |
| `contacts.csv` | Contact records. |
| `touchpoints.csv` | Marketing interaction records. |
| `leads.csv` | Lead records. |
| `opportunities.csv` | Sales opportunity records. |
| `orders.csv` | Order and revenue records. |
| `cost_records.csv` | Campaign expenditure records. |
| `attribution_results.csv` | Calculated attribution results. |
| `campaign_roi_report.csv` | Campaign ROI and ROAS results. |
| `web_sessions.csv` | Synthetic web session and identity-linking records. |

## 5. Anomaly Test Data

Location: `anomaly_data/`

| File | Description |
|---|---|
| `attribution_with_double_count.csv` | Contains a duplicated attribution record. |
| `touchpoints_after_conversion.csv` | Contains an injected post-conversion touchpoint. |
| `costs_currency_mismatch.csv` | Contains a campaign cost with an incorrect currency. |
| `costs_omitted.csv` | Contains campaign costs with one record removed. |
| `web_sessions_anonymous_link.csv` | Contains an anonymous session linked without evidence. |
| `ground_truth.csv` | Stores expected anomaly labels and explanations. |

## 6. Documentation and Configuration

| File | Purpose |
|---|---|
| `README.md` | Project overview, workflow, and execution instructions. |
| `VALIDATION_REPORT.md` | Records validation, test, and anomaly detection results. |
| `SOURCE_MANIFEST.md` | Describes project source files and datasets. |
| `requirements.txt` | Lists Python dependencies. |
| `.gitignore` | Excludes files and folders from Git tracking. |

## 7. Data Characteristics

All datasets are synthetic demonstration data generated locally. The generator uses a fixed random seed to support reproducibility.

## 8. Known Limitations

- Current dataset size is smaller than the target scale.
- Anomaly detection scripts demonstrate the five injected test scenarios.
- The current analysis workflow primarily uses CSV files.