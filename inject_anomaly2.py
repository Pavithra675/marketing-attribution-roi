
import pandas as pd
from pathlib import Path

Path("anomaly_data").mkdir(exist_ok=True)

# Load clean datasets
touchpoints = pd.read_csv("touchpoints.csv")
orders = pd.read_csv("orders.csv")
attributions = pd.read_csv("attribution_results.csv")

# Select an order
order = orders.iloc[0]
contact_id = order["contact_id"]

# Create a valid unique touchpoint ID for this contact
contact_touchpoints = touchpoints[
    touchpoints["contact_id"] == contact_id
]

if len(contact_touchpoints) > 0:
    sequences = pd.to_numeric(
        contact_touchpoints["touchpoint_id"].str.extract(r"-(\d+)$")[0],
        errors="coerce"
    ).dropna()
    next_sequence = int(sequences.max()) + 1 if len(sequences) else 1
else:
    next_sequence = 1

new_touchpoint = touchpoints.iloc[0].copy()
new_touchpoint["touchpoint_id"] = (
    f"TOUCH-{contact_id}-{next_sequence:06d}"
)
new_touchpoint["contact_id"] = contact_id

# Make the touchpoint occur AFTER the order
order_date = pd.to_datetime(order["order_date"])
invalid_date = order_date + pd.Timedelta(days=1)
new_touchpoint["touchpoint_date"] = invalid_date.strftime("%Y-%m-%d")

# Save anomalous touchpoint dataset
anomalous_touchpoints = pd.concat(
    [touchpoints, pd.DataFrame([new_touchpoint])],
    ignore_index=True
)

anomalous_touchpoints.to_csv(
    "anomaly_data/touchpoints_after_conversion.csv",
    index=False
)

# Create an attribution record for the invalid touchpoint
new_attribution = attributions.iloc[0].copy()
new_attribution["order_id"] = order["order_id"]
new_attribution["campaign_id"] = new_touchpoint["campaign_id"]
new_attribution["touchpoint_id"] = new_touchpoint["touchpoint_id"]
new_attribution["touchpoint_date"] = invalid_date.strftime("%Y-%m-%d")
new_attribution["model"] = "Last Touch"
new_attribution["attributed_revenue"] = order["revenue"]

anomalous_attributions = pd.concat(
    [attributions, pd.DataFrame([new_attribution])],
    ignore_index=True
)

anomalous_attributions.to_csv(
    "anomaly_data/attribution_after_conversion.csv",
    index=False
)

# Update ANOM-002 without duplicating its label
ground_truth_path = Path("anomaly_data/ground_truth.csv")

new_label = pd.DataFrame([{
    "anomaly_id": "ANOM-002",
    "anomaly_type": "TOUCHPOINT_AFTER_CONVERSION",
    "entity_id": order["order_id"],
    "expected_result": "FLAG",
    "reason": "Touchpoint occurred after the order date and must not receive attribution credit"
}])

if ground_truth_path.exists():
    existing_labels = pd.read_csv(ground_truth_path)
    existing_labels = existing_labels[
        existing_labels["anomaly_id"] != "ANOM-002"
    ]
    updated_labels = pd.concat(
        [existing_labels, new_label],
        ignore_index=True
    )
else:
    updated_labels = new_label

updated_labels.to_csv(ground_truth_path, index=False)

print("ANOM-002 created successfully!")
print("Affected order:", order["order_id"])
print("Contact:", contact_id)
print("Invalid touchpoint ID:", new_touchpoint["touchpoint_id"])
print("Order date:", order_date.date())
print("Invalid touchpoint date:", invalid_date.date())
print("Anomalous attribution added: YES")
print("Both anomaly CSV files saved.")
print("Ground-truth label saved.")
