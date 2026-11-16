
import pandas as pd

print("Validating additional marketing entities...")

channels = pd.read_csv("channels.csv")
campaigns = pd.read_csv("campaigns.csv")
creatives = pd.read_csv("creatives.csv")
audiences = pd.read_csv("audiences.csv")
campaign_creatives = pd.read_csv("campaign_creatives.csv")
campaign_audiences = pd.read_csv("campaign_audiences.csv")
sessions = pd.read_csv("web_sessions.csv")
touchpoints = pd.read_csv("touchpoints.csv")

errors = []

# 1. Unique master IDs
for df, column, name in [
    (channels, "channel_id", "Channels"),
    (creatives, "creative_id", "Creatives"),
    (audiences, "audience_id", "Audiences"),
]:
    if df[column].isna().any() or df[column].duplicated().any():
        errors.append(f"{name}: missing or duplicate IDs")

# 2. Campaign channels must exist in channel master
if not campaigns["channel"].isin(channels["channel_name"]).all():
    errors.append("Campaign: unknown channel")

# 3. Campaign-creative relationships
if not campaign_creatives["campaign_id"].isin(campaigns["campaign_id"]).all():
    errors.append("Campaign-creative: invalid campaign")

if not campaign_creatives["creative_id"].isin(creatives["creative_id"]).all():
    errors.append("Campaign-creative: invalid creative")

# 4. Campaign-audience relationships
if not campaign_audiences["campaign_id"].isin(campaigns["campaign_id"]).all():
    errors.append("Campaign-audience: invalid campaign")

if not campaign_audiences["audience_id"].isin(audiences["audience_id"]).all():
    errors.append("Campaign-audience: invalid audience")

# 5. Web session references
touchpoint_lookup = touchpoints.set_index("touchpoint_id")

linked = sessions[sessions["touchpoint_id"].notna()]
anonymous = sessions[sessions["consent_status"] == "NO"]

if not linked["touchpoint_id"].isin(touchpoints["touchpoint_id"]).all():
    errors.append("Web sessions: invalid touchpoint reference")

# 6. Identified session contact must match touchpoint contact
identified = sessions[sessions["contact_id"].notna()]

for row in identified.itertuples(index=False):
    if row.touchpoint_id not in touchpoint_lookup.index:
        errors.append("Identified session: missing touchpoint")
        break

    touch = touchpoint_lookup.loc[row.touchpoint_id]

    if row.contact_id != touch["contact_id"]:
        errors.append("Identified session: contact mismatch")
        break

# 7. Anonymous sessions must not be linked
if anonymous["contact_id"].notna().any():
    errors.append("Anonymous session has contact ID")

if anonymous["touchpoint_id"].notna().any():
    errors.append("Anonymous session has touchpoint ID")

if (anonymous["identity_link_evidence"] != "NONE").any():
    errors.append("Anonymous session has identity evidence")

if (anonymous["consent_status"] != "NO").any():
    errors.append("Anonymous session consent mismatch")

# Final result
print("\nValidation results:")

if errors:
    for error in errors:
        print("FAILED:", error)
    raise SystemExit(1)
else:
    print("ALL ADDITIONAL ENTITY CHECKS PASSED!")
