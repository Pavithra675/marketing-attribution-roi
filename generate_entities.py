
import random
import pandas as pd

random.seed(20261022)

print("Generating additional marketing entities...")

campaigns = pd.read_csv("campaigns.csv", usecols=["campaign_id"])
contacts = pd.read_csv("contacts.csv", usecols=["contact_id"])
touchpoints = pd.read_csv(
    "touchpoints.csv",
    usecols=["touchpoint_id", "contact_id", "touchpoint_date"]
)

campaign_ids = campaigns["campaign_id"].tolist()
contact_ids = contacts["contact_id"].tolist()
touchpoint_ids = touchpoints["touchpoint_id"].tolist()
# 1. CHANNELS
channels = pd.DataFrame([
    {"channel_id": "CH-001", "channel_name": "Email"},
    {"channel_id": "CH-002", "channel_name": "Social Media"},
    {"channel_id": "CH-003", "channel_name": "Search"},
    {"channel_id": "CH-004", "channel_name": "Display"},
    {"channel_id": "CH-005", "channel_name": "Offline"}
])
channels.to_csv("channels.csv", index=False)

# 2. CREATIVES
creatives = []

for i in range(1, 51):
    creatives.append({
        "creative_id": f"CRE-{i:04d}",
        "creative_name": f"Creative {i}",
        "creative_type": random.choice(["Image", "Video", "Text", "Banner"]),
        "status": "Active"
    })

pd.DataFrame(creatives).to_csv("creatives.csv", index=False)

# 3. AUDIENCES
audiences = []

for i in range(1, 26):
    audiences.append({
        "audience_id": f"AUD-{i:04d}",
        "audience_name": f"Audience {i}",
        "segment_type": random.choice([
            "New Customers", "Returning Customers",
            "High Intent", "General"
        ])
    })

pd.DataFrame(audiences).to_csv("audiences.csv", index=False)

# 4. CAMPAIGN TO CREATIVE MAPPING
campaign_creatives = []

for campaign_id in campaign_ids:
    campaign_creatives.append({
        "campaign_id": campaign_id,
        "creative_id": f"CRE-{random.randint(1, 50):04d}"
    })

pd.DataFrame(campaign_creatives).to_csv(
    "campaign_creatives.csv", index=False
)

# 5. CAMPAIGN TO AUDIENCE MAPPING
campaign_audiences = []

for campaign_id in campaign_ids:
    campaign_audiences.append({
        "campaign_id": campaign_id,
        "audience_id": f"AUD-{random.randint(1, 25):04d}"
    })

pd.DataFrame(campaign_audiences).to_csv(
    "campaign_audiences.csv", index=False
)


# 6. WEB SESSIONS
# Sessions inherit the contact and date from their linked touchpoint.
# Anonymous sessions have no contact and no identity-link evidence.


web_sessions = []

for i, touch in enumerate(
    touchpoints.itertuples(index=False), start=1
):
    identified = random.random() < 0.70

    if identified:
        contact_id = touch.contact_id
        touchpoint_id = touch.touchpoint_id
        consent = "YES"
        evidence = "Authenticated Login"
    else:
        contact_id = None
        touchpoint_id = None
        consent = "NO"
        evidence = "NONE"

    web_sessions.append({
        "session_id": f"SES-2026-{i:06d}",
        "contact_id": contact_id,
        "touchpoint_id": touchpoint_id,
        "session_date": touch.touchpoint_date,
        "consent_status": consent,
        "identity_link_evidence": evidence
    })

sessions_df = pd.DataFrame(web_sessions)
sessions_df.to_csv("web_sessions.csv", index=False)
