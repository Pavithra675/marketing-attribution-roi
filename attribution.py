
import pandas as pd

print("Starting optimized attribution...")

touchpoints = pd.read_csv("touchpoints.csv")
orders = pd.read_csv("orders.csv")

touchpoints["touchpoint_date"] = pd.to_datetime(
    touchpoints["touchpoint_date"]
)
orders["order_date"] = pd.to_datetime(orders["order_date"])

# Sort once instead of sorting separately for every order
touchpoints = touchpoints.sort_values(
    ["contact_id", "touchpoint_date", "touchpoint_id"]
)

# Group touchpoints by contact for faster lookup
touch_groups = {
    contact_id: group
    for contact_id, group in touchpoints.groupby("contact_id")
}

results = []
skipped_orders = 0

for order in orders.itertuples(index=False):

    customer_touches = touch_groups.get(order.contact_id)

    if customer_touches is None:
        skipped_orders += 1
        continue

    # Apply the 30-day lookback and chronology rules
    eligible = customer_touches[
        (customer_touches["touchpoint_date"] <= order.order_date) &
        (customer_touches["touchpoint_date"] >=
         order.order_date - pd.Timedelta(days=30))
    ]

    if eligible.empty:
        skipped_orders += 1
        continue

    first = eligible.iloc[0]
    last = eligible.iloc[-1]

    results.append({
        "order_id": order.order_id,
        "campaign_id": first["campaign_id"],
        "model": "First Touch",
        "attributed_revenue": order.revenue
    })

    results.append({
        "order_id": order.order_id,
        "campaign_id": last["campaign_id"],
        "model": "Last Touch",
        "attributed_revenue": order.revenue
    })

    # Divide revenue equally among eligible touchpoints
    share = order.revenue / len(eligible)

    for touch in eligible.itertuples(index=False):
        results.append({
            "order_id": order.order_id,
            "campaign_id": touch.campaign_id,
            "model": "Linear",
            "attributed_revenue": share
        })

result_df = pd.DataFrame(
    results,
    columns=[
        "order_id",
        "campaign_id",
        "model",
        "attributed_revenue"
    ]
)

result_df.to_csv("attribution_results.csv", index=False)

print("\nAttribution completed!")

if not result_df.empty:
    print("\nRevenue by attribution model:")
    print(
        result_df.groupby("model")["attributed_revenue"].sum()
    )

print("\nOrders without eligible touchpoints:", skipped_orders)
print("Total attribution rows:", len(result_df))
print("Saved attribution_results.csv")
