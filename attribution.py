
import pandas as pd

LOOKBACK_DAYS = 180

print("Starting attribution calculation...")
print("Conversion lookback window:", LOOKBACK_DAYS, "days")

touchpoints = pd.read_csv("touchpoints.csv")
orders = pd.read_csv("orders.csv")

touchpoints["touchpoint_date"] = pd.to_datetime(touchpoints["touchpoint_date"])
orders["order_date"] = pd.to_datetime(orders["order_date"])

touchpoints = touchpoints.sort_values(
    ["contact_id", "touchpoint_date", "touchpoint_id"]
)

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

    eligible = customer_touches[
        (customer_touches["touchpoint_date"] <= order.order_date)
        & (
            customer_touches["touchpoint_date"]
            >= order.order_date - pd.Timedelta(days=LOOKBACK_DAYS)
        )
    ]

    if eligible.empty:
        skipped_orders += 1
        continue

    first = eligible.iloc[0]
    last = eligible.iloc[-1]

    results.append({
        "order_id": order.order_id,
        "campaign_id": first["campaign_id"],
        "touchpoint_id": first["touchpoint_id"],
        "touchpoint_date": first["touchpoint_date"],
        "model": "First Touch",
        "attributed_revenue": order.revenue
    })

    results.append({
        "order_id": order.order_id,
        "campaign_id": last["campaign_id"],
        "touchpoint_id": last["touchpoint_id"],
        "touchpoint_date": last["touchpoint_date"],
        "model": "Last Touch",
        "attributed_revenue": order.revenue
    })

    share = order.revenue / len(eligible)

    for touch in eligible.itertuples(index=False):
        results.append({
            "order_id": order.order_id,
            "campaign_id": touch.campaign_id,
            "touchpoint_id": touch.touchpoint_id,
            "touchpoint_date": touch.touchpoint_date,
            "model": "Linear",
            "attributed_revenue": share
        })

columns = [
    "order_id",
    "campaign_id",
    "touchpoint_id",
    "touchpoint_date",
    "model",
    "attributed_revenue"
]

result_df = pd.DataFrame(results, columns=columns)
result_df.to_csv("attribution_results.csv", index=False)

print("\nAttribution completed!")

if not result_df.empty:
    print("\nRevenue by attribution model:")
    print(result_df.groupby("model")["attributed_revenue"].sum())

print("\nOrders without eligible touchpoints:", skipped_orders)
print("Orders with eligible touchpoints:", len(orders) - skipped_orders)
print("Total attribution rows:", len(result_df))
print("Saved attribution_results.csv")
