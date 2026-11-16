
import pandas as pd

print("Starting data validation...\n")

campaigns = pd.read_csv("campaigns.csv")
contacts = pd.read_csv("contacts.csv")
touchpoints = pd.read_csv("touchpoints.csv")
leads = pd.read_csv("leads.csv")
opportunities = pd.read_csv("opportunities.csv")
orders = pd.read_csv("orders.csv")
costs = pd.read_csv("cost_records.csv")
attribution = pd.read_csv("attribution_results.csv")

errors = []

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

# 4. Orders must belong to WON opportunities
won_ids = set(
    opportunities.loc[opportunities["stage"] == "Won", "opportunity_id"]
)
invalid_orders = ~orders["opportunity_id"].isin(won_ids)

if invalid_orders.any():
    errors.append(f"Orders: {invalid_orders.sum()} orders are not linked to Won opportunities")

# 5. Attribution totals must match order revenue
order_revenue = orders.set_index("order_id")["revenue"]

for model in attribution["model"].unique():
    model_data = attribution[attribution["model"] == model]

    actual = model_data.groupby("order_id")["attributed_revenue"].sum()
    expected = order_revenue.reindex(actual.index)

    difference = (actual - expected).abs()
    if (difference > 0.01).any():
        errors.append(f"{model}: attribution totals do not match order revenue")

# 6. Cost amounts must be positive
if (costs["cost_amount"] <= 0).any():
    errors.append("Costs: zero or negative cost amounts found")

# 7. Print summary
print("DATA COUNTS")
print("Campaigns:", len(campaigns))
print("Contacts:", len(contacts))
print("Touchpoints:", len(touchpoints))
print("Leads:", len(leads))
print("Opportunities:", len(opportunities))
print("Orders:", len(orders))
print("Cost records:", len(costs))
print("Attribution rows:", len(attribution))

print("\nVALIDATION RESULTS")

if errors:
    for error in errors:
        print("ERROR:", error)
    print("\nValidation completed with errors.")
else:
    print("ALL VALIDATION CHECKS PASSED!")
