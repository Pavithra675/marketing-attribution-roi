
import pandas as pd

attribution = pd.read_csv(
    "anomaly_data/attribution_with_double_count.csv"
)
orders = pd.read_csv("orders.csv")

print("Checking revenue double counting...\n")

duplicates = attribution[
    attribution.duplicated(
        subset=["order_id", "model", "touchpoint_id"],
        keep=False
    )
]

if not duplicates.empty:
    print("ANOMALY DETECTED: DUPLICATE ATTRIBUTION")

    for order_id in duplicates["order_id"].unique():
        print("Affected order:", order_id)

    print("Duplicate records:", len(duplicates))
    print("Decision: FLAG")

actual_revenue = orders.set_index("order_id")["revenue"]

attributed_revenue = attribution.groupby(
    ["order_id", "model"]
)["attributed_revenue"].sum()

for (order_id, model), amount in attributed_revenue.items():
    expected = actual_revenue.get(order_id)

    if expected is not None and amount > expected + 0.01:
        print("\nREVENUE RECONCILIATION FAILURE")
        print("Order:", order_id)
        print("Model:", model)
        print("Actual revenue:", expected)
        print("Attributed revenue:", amount)
        print("Excess:", amount - expected)
        print("Decision: FLAG")
