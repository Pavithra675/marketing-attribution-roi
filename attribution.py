
import pandas as pd

touchpoints = pd.read_csv("touchpoints.csv")
orders = pd.read_csv("orders.csv")

# Convert dates into proper datetime values
touchpoints["touchpoint_date"] = pd.to_datetime(
    touchpoints["touchpoint_date"]
)
orders["order_date"] = pd.to_datetime(orders["order_date"])

results = []
skipped_orders = 0

for _, order in orders.iterrows():

    # Only consider touches from the same customer
    customer_touches = touchpoints[
        touchpoints["contact_id"] == order["contact_id"]
    ].copy()

    # Only touches within 30 days before the order
    customer_touches = customer_touches[
        (customer_touches["touchpoint_date"] <= order["order_date"]) &
        (customer_touches["touchpoint_date"] >=
         order["order_date"] - pd.Timedelta(days=30))
    ]

    customer_touches = customer_touches.sort_values(
        ["touchpoint_date", "touchpoint_id"]
    )

    if customer_touches.empty:
        skipped_orders += 1
        continue

    # First touch
    first = customer_touches.iloc[0]

    results.append({
        "order_id": order["order_id"],
        "campaign_id": first["campaign_id"],
        "model": "First Touch",
        "attributed_revenue": order["revenue"]
    })

    # Last touch
    last = customer_touches.iloc[-1]

    results.append({
        "order_id": order["order_id"],
        "campaign_id": last["campaign_id"],
        "model": "Last Touch",
        "attributed_revenue": order["revenue"]
    })

    # Linear attribution
    share = order["revenue"] / len(customer_touches)

    for _, touch in customer_touches.iterrows():
        results.append({
            "order_id": order["order_id"],
            "campaign_id": touch["campaign_id"],
            "model": "Linear",
            "attributed_revenue": share
        })

result_df = pd.DataFrame(results)

result_df.to_csv("attribution_results.csv", index=False)

print("\nAttribution completed!")
print("\nRevenue by attribution model:")

if not result_df.empty:
    print(
        result_df.groupby("model")["attributed_revenue"].sum()
    )

print("\nOrders without eligible touchpoints:", skipped_orders)
print("Saved attribution_results.csv")
