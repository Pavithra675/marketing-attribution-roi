
import pandas as pd

# Load anomalous attribution data and original orders
attribution = pd.read_csv(
    "anomaly_data/attribution_with_double_count.csv"
)
orders = pd.read_csv("orders.csv")

print("Checking for revenue double counting...\n")

# Check 1: Find duplicate attribution rows
duplicates = attribution[
    attribution.duplicated(
        subset=["order_id", "campaign_id", "model"],
        keep=False
    )
]

print("Duplicate attribution records:")
print(duplicates)

# Check 2: Compare attributed revenue with actual order revenue
actual_revenue = orders.set_index("order_id")["revenue"]

attributed_revenue = attribution.groupby(
    ["order_id", "model"]
)["attributed_revenue"].sum()

for (order_id, model), amount in attributed_revenue.items():
    expected = actual_revenue.get(order_id)

    if expected is not None and amount > expected + 0.01:
        print("\nANOMALY DETECTED!")
        print("Order:", order_id)
        print("Model:", model)
        print("Actual revenue:", expected)
        print("Attributed revenue:", amount)
        print("Excess revenue:", amount - expected)
        print("Decision: FLAG")
