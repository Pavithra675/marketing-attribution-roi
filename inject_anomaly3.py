
import pandas as pd
from pathlib import Path

Path("anomaly_data").mkdir(exist_ok=True)

# Load original campaign costs
costs = pd.read_csv("cost_records.csv")

# Select the first cost record
target = costs.iloc[0].copy()

# Change its currency to USD to create an anomaly
target["currency"] = "USD"

# Create a separate anomalous dataset
anomalous_costs = costs.copy()
anomalous_costs.loc[0, "currency"] = "USD"

anomalous_costs.to_csv(
    "anomaly_data/costs_currency_mismatch.csv",
    index=False
)

# Add ground-truth label
ground_truth_path = Path("anomaly_data/ground_truth.csv")

new_label = pd.DataFrame([{
    "anomaly_id": "ANOM-003",
    "anomaly_type": "SPEND_CURRENCY_MISMATCH",
    "entity_id": target["cost_id"],
    "expected_result": "FLAG",
    "reason": "Campaign spend currency differs from the expected reporting currency INR"
}])

existing_labels = pd.read_csv(ground_truth_path)
updated_labels = pd.concat(
    [existing_labels, new_label],
    ignore_index=True
)
updated_labels.to_csv(ground_truth_path, index=False)

print("Currency mismatch anomaly created!")
print("Affected cost:", target["cost_id"])
print("Campaign:", target["campaign_id"])
print("Original currency: INR")
print("Anomalous currency: USD")
print("Decision: FLAG")
