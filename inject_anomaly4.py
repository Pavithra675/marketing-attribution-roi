
import pandas as pd
from pathlib import Path

Path("anomaly_data").mkdir(exist_ok=True)

# Load clean datasets
costs = pd.read_csv("cost_records.csv")
attribution = pd.read_csv("attribution_results.csv")

# Find campaigns with attributed revenue
revenue_campaigns = attribution[
    attribution["attributed_revenue"] > 0
]["campaign_id"].unique()

eligible = costs[
    costs["campaign_id"].isin(revenue_campaigns)
]

if eligible.empty:
    raise ValueError("No campaign with both revenue and cost found.")

target = eligible.iloc[0]
campaign_id = target["campaign_id"]

# Remove the campaign's cost from the anomaly dataset
anomalous_costs = costs[
    costs["campaign_id"] != campaign_id
].copy()

anomalous_costs.to_csv(
    "anomaly_data/costs_omitted.csv",
    index=False
)

# Update ground truth without duplicating ANOM-004
ground_truth_path = Path("anomaly_data/ground_truth.csv")

new_label = pd.DataFrame([{
    "anomaly_id": "ANOM-004",
    "anomaly_type": "CAMPAIGN_COST_OMITTED",
    "entity_id": campaign_id,
    "expected_result": "FLAG",
    "reason": "Campaign has attributed revenue but its cost record is missing; ROI must not be calculated"
}])

if ground_truth_path.exists():
    existing = pd.read_csv(ground_truth_path)
    existing = existing[
        existing["anomaly_id"] != "ANOM-004"
    ]
    updated = pd.concat([existing, new_label], ignore_index=True)
else:
    updated = new_label

updated.to_csv(ground_truth_path, index=False)

print("ANOM-004 created successfully!")
print("Affected campaign:", campaign_id)
print("Original cost:", target["cost_amount"], target["currency"])
print("Cost record removed from anomaly dataset.")
print("Expected decision: FLAG")
