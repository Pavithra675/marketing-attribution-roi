
import pandas as pd

print("Exporting orders without eligible attribution...")

# Load source orders and calculated attribution results
orders = pd.read_csv("orders.csv")
attribution = pd.read_csv("attribution_results.csv")

# Find orders that do not appear in any attribution model
attributed_order_ids = set(attribution["order_id"].dropna())

unattributed = orders[
    ~orders["order_id"].isin(attributed_order_ids)
].copy()

# Clearly identify why these orders are not attributed
unattributed["attribution_status"] = "UNATTRIBUTED"
unattributed["reason"] = "NO_ELIGIBLE_TOUCHPOINT_WITHIN_180_DAYS"

# Export separately without changing source data
unattributed.to_csv("unattributed_orders.csv", index=False)

print("\nUNATTRIBUTED ORDER SUMMARY")
print("Total source orders:", len(orders))
print("Attributed orders:", len(attributed_order_ids))
print("Unattributed orders:", len(unattributed))
print("Unattributed revenue:", unattributed["revenue"].sum())

print("\nSaved: unattributed_orders.csv")
