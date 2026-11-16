
import pandas as pd

touchpoints = pd.read_csv(
    "anomaly_data/touchpoints_after_conversion.csv"
)

attribution = pd.read_csv(
    "anomaly_data/attribution_after_conversion.csv"
)

orders = pd.read_csv("orders.csv")

ground_truth = pd.read_csv("anomaly_data/ground_truth.csv")

label = ground_truth[
    ground_truth["anomaly_id"] == "ANOM-002"
].iloc[0]

order_id = label["entity_id"]

order = orders[orders["order_id"] == order_id].iloc[0]

# Find touchpoints attributed to this order
order_attribution = attribution[
    attribution["order_id"] == order_id
].copy()

# Match attributed touchpoints with source touchpoint records
matched = order_attribution.merge(
    touchpoints[["touchpoint_id", "contact_id", "touchpoint_date"]],
    on="touchpoint_id",
    suffixes=("_attribution", "_source")
)

order_date = pd.to_datetime(order["order_date"])
matched["touchpoint_date_source"] = pd.to_datetime(
    matched["touchpoint_date_source"]
)

# Find attributed touchpoints occurring after conversion
invalid = matched[
    matched["touchpoint_date_source"] > order_date
]

print("Checking touchpoint-after-conversion anomaly...\n")

if not invalid.empty:
    print("ANOMALY DETECTED!")

    for _, row in invalid.iterrows():
        print("Order:", order_id)
        print("Touchpoint:", row["touchpoint_id"])
        print("Order date:", order_date.date())
        print(
            "Touchpoint date:",
            row["touchpoint_date_source"].date()
        )
        print("Model:", row["model"])
        print("Decision: FLAG")
else:
    print("No anomaly detected.")
