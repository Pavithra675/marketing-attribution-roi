
import pandas as pd
from pathlib import Path

# Load original clean data
orders = pd.read_csv("orders.csv")
attribution = pd.read_csv("attribution_results.csv")

# Create separate copies for anomaly testing
anomalous_attribution = attribution.copy()

# Select one order that already has attribution records
target_order = anomalous_attribution.iloc[0]["order_id"]

# Select one existing attribution row for that order
original_row = anomalous_attribution[
    anomalous_attribution["order_id"] == target_order
].iloc[0].copy()

# Duplicate the same revenue attribution incorrectly
duplicate_row = original_row.copy()
anomalous_attribution = pd.concat(
    [anomalous_attribution, pd.DataFrame([duplicate_row])],
    ignore_index=True
)

# Save corrupted test data separately
Path("anomaly_data").mkdir(exist_ok=True)

anomalous_attribution.to_csv(
    "anomaly_data/attribution_with_double_count.csv",
    index=False
)

# Create ground-truth label
ground_truth = pd.DataFrame([{
    "anomaly_id": "ANOM-001",
    "anomaly_type": "REVENUE_DOUBLE_COUNT",
    "entity_id": target_order,
    "expected_result": "FLAG",
    "reason": "Duplicate attribution row causes revenue to be counted twice"
}])

ground_truth.to_csv(
    "anomaly_data/ground_truth.csv",
    index=False
)

print("Revenue double-counting anomaly created!")
print("Affected order:", target_order)
print("Original attribution rows:", len(attribution))
print("Anomalous attribution rows:", len(anomalous_attribution))
print("Ground-truth label saved.")
