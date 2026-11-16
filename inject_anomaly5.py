
import pandas as pd
from pathlib import Path

Path("anomaly_data").mkdir(exist_ok=True)

# Load original datasets
sessions = pd.read_csv("web_sessions.csv")
contacts = pd.read_csv("contacts.csv")

# Find an anonymous session without evidence or consent
eligible = sessions[
    sessions["contact_id"].isna()
    & (sessions["identity_link_evidence"] == "NONE")
    & (sessions["consent_status"] == "NO")
]

if eligible.empty:
    raise ValueError("No eligible anonymous session found.")

target = eligible.iloc[0]
session_id = target["session_id"]

# Select an existing contact
contact_id = contacts.iloc[0]["contact_id"]

# Create a separate anomalous dataset
anomalous = sessions.copy()
anomalous.loc[
    anomalous["session_id"] == session_id,
    "contact_id"
] = contact_id

anomalous.to_csv(
    "anomaly_data/web_sessions_anonymous_link.csv",
    index=False
)

# Update ground truth without duplicating ANOM-005
ground_truth_path = Path("anomaly_data/ground_truth.csv")

new_label = pd.DataFrame([{
    "anomaly_id": "ANOM-005",
    "anomaly_type": "ANONYMOUS_SESSION_LINKED_WITHOUT_EVIDENCE",
    "entity_id": session_id,
    "expected_result": "FLAG",
    "reason": "Anonymous session linked to a contact without identity evidence or consent"
}])

if ground_truth_path.exists():
    existing = pd.read_csv(ground_truth_path)
    existing = existing[
        existing["anomaly_id"] != "ANOM-005"
    ]
    updated = pd.concat([existing, new_label], ignore_index=True)
else:
    updated = new_label

updated.to_csv(ground_truth_path, index=False)

print("ANOM-005 created successfully!")
print("Affected session:", session_id)
print("Linked contact:", contact_id)
print("Identity evidence:", target["identity_link_evidence"])
print("Consent:", target["consent_status"])
print("Original web_sessions.csv preserved.")
print("Expected decision: FLAG")
