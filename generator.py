import random
import pandas as pd

print("Marketing Attribution Generator started!")

random.seed(20261022)


def random_date():
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"2026-{month:02d}-{day:02d}"


# 1. CAMPAIGNS: 500
campaigns = []

for i in range(1, 501):
    campaigns.append({
        "campaign_id": f"CMP-2026-{i:06d}",
        "campaign_name": f"Campaign {i}",
        "channel": random.choice([
            "Email", "Social Media", "Search", "Display"
        ]),
        "budget": random.randint(1000, 10000),
        "currency": "INR"
    })

campaigns_df = pd.DataFrame(campaigns)
campaigns_df.to_csv("campaigns.csv", index=False)

print("Campaigns generated:", len(campaigns_df))


# 2. CONTACTS: 50,000
contacts = []

for i in range(1, 50001):
    contacts.append({
        "contact_id": f"CON-{i:06d}",
        "contact_name": f"Contact {i}",
        "email": f"contact{i}@example.com",
        "created_date": random_date()
    })

contacts_df = pd.DataFrame(contacts)
contacts_df.to_csv("contacts.csv", index=False)

print("Contacts generated:", len(contacts_df))


# 3. TOUCHPOINTS: 200,000
# Required format:
# TOUCH-<contact-id>-<sequence>
touchpoints = []

channels = ["Email", "Social Media", "Search", "Display"]
interactions = [
    "Impression", "Click", "Website Visit", "Form Submission"
]

touchpoint_sequence = {}

for i in range(1, 200001):
    contact_num = random.randint(1, 50000)
    contact_id = f"CON-{contact_num:06d}"

    # Maintain a separate sequence for each contact
    touchpoint_sequence[contact_id] = (
        touchpoint_sequence.get(contact_id, 0) + 1
    )

    sequence = touchpoint_sequence[contact_id]

    touchpoints.append({
        "touchpoint_id": f"TOUCH-{contact_id}-{sequence:06d}",
        "contact_id": contact_id,
        "campaign_id": f"CMP-2026-{random.randint(1, 500):06d}",
        "channel": random.choice(channels),
        "interaction_type": random.choice(interactions),
        "touchpoint_date": random_date()
    })

touchpoints_df = pd.DataFrame(touchpoints)
touchpoints_df.to_csv("touchpoints.csv", index=False)

print("Touchpoints generated:", len(touchpoints_df))


# 4. LEADS: 25,000
# Required format:
# LEAD-2026-000001
leads = []

for i in range(1, 25001):
    contact_num = random.randint(1, 50000)

    leads.append({
        "lead_id": f"LEAD-2026-{i:06d}",
        "contact_id": f"CON-{contact_num:06d}",
        "lead_source": random.choice([
            "Website", "Email", "Social Media", "Search"
        ]),
        "lead_status": random.choice([
            "New", "Qualified", "Unqualified"
        ]),
        "created_date": random_date()
    })

leads_df = pd.DataFrame(leads)
leads_df.to_csv("leads.csv", index=False)

print("Leads generated:", len(leads_df))


# 5. OPPORTUNITIES: 10,000
# Required format:
# OPP-2026-000001
opportunities = []

for i in range(1, 10001):
    lead = random.choice(leads)

    opportunities.append({
        "opportunity_id": f"OPP-2026-{i:06d}",
        "lead_id": lead["lead_id"],
        "contact_id": lead["contact_id"],
        "opportunity_name": f"Opportunity {i}",
        "stage": random.choice([
            "Prospecting", "Negotiation", "Won", "Lost"
        ]),
        "amount": random.randint(5000, 100000),
        "currency": "INR",
        "created_date": random_date()
    })

opportunities_df = pd.DataFrame(opportunities)
opportunities_df.to_csv("opportunities.csv", index=False)

print("Opportunities generated:", len(opportunities_df))


# 6. ORDERS: only Won opportunities
orders = []

for opportunity in opportunities:
    if opportunity["stage"] == "Won":
        orders.append({
            "order_id": f"ORD-{len(orders) + 1:06d}",
            "opportunity_id": opportunity["opportunity_id"],
            "contact_id": opportunity["contact_id"],
            "revenue": opportunity["amount"],
            "currency": opportunity["currency"],
            "order_status": "Completed",
            "order_date": opportunity["created_date"]
        })

orders_df = pd.DataFrame(orders)
orders_df.to_csv("orders.csv", index=False)

print("Orders generated:", len(orders_df))
print(
    "Total revenue:",
    orders_df["revenue"].sum() if not orders_df.empty else 0
)


# 6A. GUARANTEE ELIGIBLE TOUCHPOINTS FOR BASELINE ORDERS

print("\nEnsuring every order has an eligible touchpoint...")

if len(orders_df) > len(touchpoints_df):
    raise ValueError("Not enough touchpoint rows for all orders")

# Reserve one existing touchpoint row for each order.
start_index = len(touchpoints_df) - len(orders_df)

for i, order in enumerate(orders_df.itertuples(index=False)):
    row_index = start_index + i

    # Link the touchpoint to the order's contact.
    touchpoints_df.at[row_index, "contact_id"] = order.contact_id

    # Place the touchpoint between 0 and 180 days before conversion.
    order_date = pd.to_datetime(order.order_date)
    touchpoint_date = order_date - pd.Timedelta(
        days=random.randint(0, 180)
    )

    touchpoints_df.at[row_index, "touchpoint_date"] = (
        touchpoint_date.strftime("%Y-%m-%d")
    )

# Rebuild unique touchpoint IDs after changing contact assignments.
sequence = touchpoints_df.groupby("contact_id").cumcount() + 1

touchpoints_df["touchpoint_id"] = (
    "TOUCH-"
    + touchpoints_df["contact_id"]
    + "-"
    + sequence.astype(str).str.zfill(6)
)

# Save the corrected baseline touchpoints.
touchpoints_df.to_csv("touchpoints.csv", index=False)

print("Orders with guaranteed eligible touchpoints:", len(orders_df))
print("Touchpoints generated:", len(touchpoints_df))


# 7. COST RECORDS: 500
cost_records = []

for i, campaign in enumerate(campaigns, start=1):
    cost_records.append({
        "cost_id": f"COST-{i:06d}",
        "campaign_id": campaign["campaign_id"],
        "cost_amount": random.randint(1000, 20000),
        "currency": "INR",
        "cost_date": random_date()
    })

costs_df = pd.DataFrame(cost_records)
costs_df.to_csv("cost_records.csv", index=False)

print("Cost records generated:", len(costs_df))
print("Total marketing spend:", costs_df["cost_amount"].sum())

print("\nAll datasets generated successfully!")