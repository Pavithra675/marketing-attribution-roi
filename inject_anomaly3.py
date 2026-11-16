
import pandas as pd
from pathlib import Path

Path("anomaly_data").mkdir(exist_ok=True)

# Load clean campaign costs
costs = pd.read_csv("cost_records.csv")

# Select one campaign cost
target = costs.iloc[0].copy()

# Change INR to USD
anomalous_costs = costs.copy()
anomalous_costs.loc[
    anomalous_costs["cost_id"] == target["cost_id"],
    "currency"
] = "USD"

anomalous_costs.to_csv(
    "anomaly_data/costs_currency_mismatch.csv",
    index=False
)

# Update ground truth without duplicating ANOM-003
ground_truth_path = Path("anomaly_data/ground_truth.csv")

new_label = pd.DataFrame([{
    "anomaly_id": "ANOM-003",
    "anomaly_type": "SPEND_CURRENCY_MISMATCH",
    "entity_id": target["cost_id"],
    "expected_result": "FLAG",
    "reason": "Campaign spend currency differs from expected reporting currency INR"
}])

if ground_truth_path.exists():
    existing = pd.read_csv(ground_truth_path)
    existing = existing[existing["anomaly_id"] != "ANOM-003"]
    updated = pd.concat([existing, new_label], ignore_index=True)
else:
    updated = new_label

updated.to_csv(ground_truth_path, index=False)

print("ANOM-003 created successfully!")
print("Cost ID:", target["cost_id"])
print("Campaign:", target["campaign_id"])
print("Original currency:", target["currency"])
print("Anomalous currency: USD")
print("Decision: FLAG")
