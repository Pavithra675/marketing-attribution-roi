
import pandas as pd
from pathlib import Path

Path("anomaly_data").mkdir(exist_ok=True)

# Load latest clean datasets
orders = pd.read_csv("orders.csv")
attribution = pd.read_csv("attribution_results.csv")

if attribution.empty:
    raise ValueError("No attribution records found.")

# Select an order with existing attribution
target_order = attribution.iloc[0]["order_id"]

original_row = attribution[
    attribution["order_id"] == target_order
].iloc[0].copy()

# Duplicate one attribution record
anomalous_attribution = pd.concat(
    [attribution, pd.DataFrame([original_row])],
    ignore_index=True
)

anomalous_attribution.to_csv(
    "anomaly_data/attribution_with_double_count.csv",
    index=False
)

# Prepare ANOM-001 ground-truth label
new_label = pd.DataFrame([{
    "anomaly_id": "ANOM-001",
    "anomaly_type": "REVENUE_DOUBLE_COUNT",
    "entity_id": target_order,
    "expected_result": "FLAG",
    "reason": "Duplicate order, model and touchpoint attribution causes revenue overcounting"
}])

# Preserve the other four labels
ground_truth_path = Path("anomaly_data/ground_truth.csv")

if ground_truth_path.exists():
    existing = pd.read_csv(ground_truth_path)
    existing = existing[
        existing["anomaly_id"] != "ANOM-001"
    ]
    updated = pd.concat(
        [existing, new_label],
        ignore_index=True
    )
else:
    updated = new_label

updated.to_csv(ground_truth_path, index=False)

print("ANOM-001 refreshed successfully!")
print("Affected order:", target_order)
print("Original attribution rows:", len(attribution))
print("Anomalous attribution rows:", len(anomalous_attribution))
print("Ground truth labels preserved:", len(updated))
