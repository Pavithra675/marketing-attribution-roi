
import pandas as pd

touchpoints = pd.read_csv(
    "anomaly_data/touchpoints_after_conversion.csv"
)
orders = pd.read_csv("orders.csv")
ground_truth = pd.read_csv("anomaly_data/ground_truth.csv")

label = ground_truth[
    ground_truth["anomaly_id"] == "ANOM-002"
].iloc[0]

order_id = label["entity_id"]

order = orders[orders["order_id"] == order_id].iloc[0]

# Find touchpoints for this order's contact
matched = touchpoints[
    touchpoints["contact_id"] == order["contact_id"]
].copy()

matched["touchpoint_date"] = pd.to_datetime(
    matched["touchpoint_date"]
)
order_date = pd.to_datetime(order["order_date"])

# Find the injected touchpoint occurring after this order
invalid = matched[
    (matched["touchpoint_date"] > order_date)
    & (matched["touchpoint_id"] == "TOUCH-005001")
]

print("Checking injected touchpoint anomaly...\n")

if not invalid.empty:
    print("ANOMALY DETECTED!")
    for _, row in invalid.iterrows():
        print("Order:", order_id)
        print("Touchpoint:", row["touchpoint_id"])
        print("Order date:", order_date.date())
        print("Touchpoint date:", row["touchpoint_date"].date())
        print("Decision: FLAG")
else:
    print("No anomaly detected.")
