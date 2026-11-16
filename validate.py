
import pandas as pd

print("Starting comprehensive data validation...\n")

campaigns = pd.read_csv("campaigns.csv")
contacts = pd.read_csv("contacts.csv")
touchpoints = pd.read_csv("touchpoints.csv")
leads = pd.read_csv("leads.csv")
opportunities = pd.read_csv("opportunities.csv")
orders = pd.read_csv("orders.csv")
costs = pd.read_csv("cost_records.csv")
attribution = pd.read_csv("attribution_results.csv")

touchpoints["touchpoint_date"] = pd.to_datetime(touchpoints["touchpoint_date"])
orders["order_date"] = pd.to_datetime(orders["order_date"])
attribution["touchpoint_date"] = pd.to_datetime(attribution["touchpoint_date"])

errors = []
warnings = []

# 1. Primary key checks
tables = {
    "Campaigns": (campaigns, "campaign_id"),
    "Contacts": (contacts, "contact_id"),
    "Touchpoints": (touchpoints, "touchpoint_id"),
    "Leads": (leads, "lead_id"),
    "Opportunities": (opportunities, "opportunity_id"),
    "Orders": (orders, "order_id"),
    "Costs": (costs, "cost_id"),
}

for name, (df, key) in tables.items():
    if df[key].isna().any():
        errors.append(f"{name}: missing {key}")
    if df[key].duplicated().any():
        errors.append(f"{name}: duplicate {key}")

# 2. Foreign key checks
checks = [
    (touchpoints, "campaign_id", campaigns, "campaign_id", "Touchpoints -> Campaigns"),
    (touchpoints, "contact_id", contacts, "contact_id", "Touchpoints -> Contacts"),
    (leads, "contact_id", contacts, "contact_id", "Leads -> Contacts"),
    (opportunities, "lead_id", leads, "lead_id", "Opportunities -> Leads"),
    (opportunities, "contact_id", contacts, "contact_id", "Opportunities -> Contacts"),
    (orders, "opportunity_id", opportunities, "opportunity_id", "Orders -> Opportunities"),
    (costs, "campaign_id", campaigns, "campaign_id", "Costs -> Campaigns"),
    (attribution, "campaign_id", campaigns, "campaign_id", "Attribution -> Campaigns"),
    (attribution, "order_id", orders, "order_id", "Attribution -> Orders"),
    (attribution, "touchpoint_id", touchpoints, "touchpoint_id", "Attribution -> Touchpoints"),
]

for source, source_col, target, target_col, label in checks:
    invalid = ~source[source_col].isin(target[target_col])
    if invalid.any():
        errors.append(f"{label}: {invalid.sum()} invalid references")

# 3. Opportunity contact must match its lead
lead_contacts = leads.set_index("lead_id")["contact_id"]
expected_contacts = opportunities["lead_id"].map(lead_contacts)

mismatch = opportunities["contact_id"] != expected_contacts
if mismatch.any():
    errors.append(f"Opportunities: {mismatch.sum()} lead/contact mismatches")

# 4. Orders must belong to Won opportunities
won_ids = set(
    opportunities.loc[
        opportunities["stage"] == "Won", "opportunity_id"
    ]
)

invalid_orders = ~orders["opportunity_id"].isin(won_ids)
if invalid_orders.any():
    errors.append(f"Orders: {invalid_orders.sum()} orders not linked to Won opportunities")

# 5. Allowed values
allowed_models = {"First Touch", "Last Touch", "Linear"}
allowed_stages = {"Prospecting", "Negotiation", "Won", "Lost"}
allowed_order_statuses = {"Completed"}

if not set(attribution["model"]).issubset(allowed_models):
    errors.append("Attribution: invalid attribution model")

if not set(opportunities["stage"]).issubset(allowed_stages):
    errors.append("Opportunities: invalid stage")

if not set(orders["order_status"]).issubset(allowed_order_statuses):
    errors.append("Orders: invalid order status")

# 6. Attribution must not use future touchpoints
order_dates = orders.set_index("order_id")["order_date"]
expected_order_dates = attribution["order_id"].map(order_dates)

future_touches = attribution["touchpoint_date"] > expected_order_dates

if future_touches.any():
    errors.append(
        f"Attribution: {future_touches.sum()} touchpoints occur after conversion"
    )

# 7. Duplicate attribution records
duplicate_attribution = attribution.duplicated(
    subset=["order_id", "model", "touchpoint_id"]
)

if duplicate_attribution.any():
    errors.append(
        f"Attribution: {duplicate_attribution.sum()} duplicate order/model/touchpoint records"
    )

# 8. Attribution revenue reconciliation
order_revenue = orders.set_index("order_id")["revenue"]

for model in sorted(attribution["model"].unique()):
    model_data = attribution[attribution["model"] == model]

    actual = model_data.groupby("order_id")["attributed_revenue"].sum()
    expected = order_revenue.reindex(actual.index)

    difference = (actual - expected).abs()

    if difference.isna().any() or (difference > 0.01).any():
        errors.append(
            f"{model}: attributed revenue does not reconcile with order revenue"
        )

    print(
        f"{model}: {len(actual)} orders reconciled"
    )

# 9. Positive costs and currency consistency
if (costs["cost_amount"] <= 0).any():
    errors.append("Costs: zero or negative cost amounts")

cost_currency = costs.merge(
    campaigns[["campaign_id", "currency"]],
    on="campaign_id",
    how="left",
    suffixes=("_cost", "_campaign")
)

currency_mismatch = (
    cost_currency["currency_cost"]
    != cost_currency["currency_campaign"]
)

if currency_mismatch.any():
    errors.append(
        f"Costs: {currency_mismatch.sum()} campaign/cost currency mismatches"
    )

# 10. Report orders without attribution
attributed_orders = set(attribution["order_id"])
unattributed_orders = set(orders["order_id"]) - attributed_orders

if unattributed_orders:
    warnings.append(
        f"{len(unattributed_orders)} orders have no eligible touchpoints"
    )

# 11. Summary
print("\nDATA COUNTS")
print("Campaigns:", len(campaigns))
print("Contacts:", len(contacts))
print("Touchpoints:", len(touchpoints))
print("Leads:", len(leads))
print("Opportunities:", len(opportunities))
print("Orders:", len(orders))
print("Cost records:", len(costs))
print("Attribution rows:", len(attribution))

print("\nVALIDATION RESULTS")

for warning in warnings:
    print("WARNING:", warning)

if errors:
    for error in errors:
        print("ERROR:", error)
    print("\nVALIDATION FAILED")
else:
    print("ALL VALIDATION CHECKS PASSED!")
