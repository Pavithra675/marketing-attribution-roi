
import pandas as pd
from pathlib import Path

# Create output folder
Path("anomaly_data").mkdir(exist_ok=True)

# Load original data
touchpoints = pd.read_csv("touchpoints.csv")
orders = pd.read_csv("orders.csv")

# Select the first order
order = orders.iloc[0]

# Copy an existing touchpoint as a template
new_touchpoint = touchpoints.iloc[0].copy()

# Give it a new unique ID
last_id = touchpoints["touchpoint_id"].str.extract(r"(\d+)$")[0].astype(int).max()
new_touchpoint["touchpoint_id"] = f"TOUCH-{last_id + 1:06d}"

# Make it belong to the order's contact
new_touchpoint["contact_id"] = order["contact_id"]

# Set its date to one day after the order
order_date = pd.to_datetime(order["order_date"])
new_touchpoint["touchpoint_date"] = (
    order_date + pd.Timedelta(days=1)
).strftime("%Y-%m-%d")

# Add the invalid touchpoint
anomalous_touchpoints = pd.concat(
    [touchpoints, pd.DataFrame([new_touchpoint])],
    ignore_index=True
)

# Save separate anomaly dataset
anomalous_touchpoints.to_csv(
    "anomaly_data/touchpoints_after_conversion.csv",
    index=False
)

# Append ground-truth label without deleting Anomaly 1
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
    updated_labels = pd.concat(
        [existing_labels, new_label],
        ignore_index=True
    )
else:
    updated_labels = new_label

updated_labels.to_csv(ground_truth_path, index=False)

print("Touchpoint-after-conversion anomaly created!")
print("Affected order:", order["order_id"])
print("Contact:", order["contact_id"])
print("Order date:", order_date.date())
print("Invalid touchpoint date:", new_touchpoint["touchpoint_date"])
print("Ground-truth label saved.")
