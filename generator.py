
print("Marketing Attribution Generator started!")

import random
import pandas as pd

random.seed(20261022)

campaigns = []

for i in range(1, 101):
    campaigns.append({
        "campaign_id": f"CMP-2026-{i:06d}",
        "campaign_name": f"Campaign {i}",
        "channel": random.choice(["Email", "Social Media", "Search", "Display"]),
        "budget": random.randint(1000, 10000),
        "currency": "INR"
    })

df = pd.DataFrame(campaigns)
df.to_csv("campaigns.csv", index=False)

print("Campaigns generated:", len(df))
print("Saved campaigns.csv successfully!")


contacts = []

for i in range(1, 1001):
    contacts.append({
        "contact_id": f"CON-{i:06d}",
        "contact_name": f"Contact {i}",
        "email": f"contact{i}@example.com",
        "created_date": f"2026-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    })

contacts_df = pd.DataFrame(contacts)
contacts_df.to_csv("contacts.csv", index=False)

print("Contacts generated:", len(contacts_df))
print("Saved contacts.csv successfully!")


touchpoints = []

for i in range(1, 5001):
    campaign_num = random.randint(1, 100)
    contact_num = random.randint(1, 1000)

    touchpoints.append({
        "touchpoint_id": f"TOUCH-{i:06d}",
        "contact_id": f"CON-{contact_num:06d}",
        "campaign_id": f"CMP-2026-{campaign_num:06d}",
        "channel": random.choice([
            "Email", "Social Media", "Search", "Display"
        ]),
        "interaction_type": random.choice([
            "Impression", "Click", "Website Visit", "Form Submission"
        ]),
        "touchpoint_date": f"2026-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    })

touchpoints_df = pd.DataFrame(touchpoints)
touchpoints_df.to_csv("touchpoints.csv", index=False)

print("Touchpoints generated:", len(touchpoints_df))
print("Saved touchpoints.csv successfully!")


leads = []

for i in range(1, 501):
    contact_num = random.randint(1, 1000)

    leads.append({
        "lead_id": f"LEAD-{i:06d}",
        "contact_id": f"CON-{contact_num:06d}",
        "lead_source": random.choice([
            "Website", "Email", "Social Media", "Search"
        ]),
        "lead_status": random.choice([
            "New", "Qualified", "Unqualified"
        ]),
        "created_date": f"2026-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    })

leads_df = pd.DataFrame(leads)
leads_df.to_csv("leads.csv", index=False)

print("Leads generated:", len(leads_df))
print("Saved leads.csv successfully!")


opportunities = []

for i in range(1, 201):
    lead = random.choice(leads)

    opportunities.append({
        "opportunity_id": f"OPP-{i:06d}",
        "lead_id": lead["lead_id"],
        "contact_id": lead["contact_id"],
        "opportunity_name": f"Opportunity {i}",
        "stage": random.choice([
            "Prospecting", "Negotiation", "Won", "Lost"
        ]),
        "amount": random.randint(5000, 100000),
        "currency": "INR",
        "created_date": f"2026-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    })

opportunities_df = pd.DataFrame(opportunities)
opportunities_df.to_csv("opportunities.csv", index=False)

print("Opportunities generated:", len(opportunities_df))
print("Saved opportunities.csv successfully!")


orders = []
order_count = 0

for opportunity in opportunities:
    if opportunity["stage"] == "Won":
        order_count += 1

        orders.append({
            "order_id": f"ORD-{order_count:06d}",
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
print("Total revenue:", orders_df["revenue"].sum() if not orders_df.empty else 0)
print("Saved orders.csv successfully!")


cost_records = []

for i, campaign in enumerate(campaigns, start=1):
    cost_records.append({
        "cost_id": f"COST-{i:06d}",
        "campaign_id": campaign["campaign_id"],
        "cost_amount": random.randint(1000, 20000),
        "currency": "INR",
        "cost_date": f"2026-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    })

costs_df = pd.DataFrame(cost_records)
costs_df.to_csv("cost_records.csv", index=False)

print("Cost records generated:", len(costs_df))
print("Total marketing spend:", costs_df["cost_amount"].sum())
print("Saved cost_records.csv successfully!")
