
import pandas as pd

# Load anomalous session dataset
sessions = pd.read_csv(
    "anomaly_data/web_sessions_anonymous_link.csv"
)

# Load ground truth
ground_truth = pd.read_csv(
    "anomaly_data/ground_truth.csv"
)

labels = ground_truth[
    ground_truth["anomaly_id"] == "ANOM-005"
]

if labels.empty:
    raise ValueError("ANOM-005 ground-truth label not found.")

session_id = labels.iloc[0]["entity_id"]

# Find affected session
record = sessions[
    sessions["session_id"] == session_id
]

if record.empty:
    raise ValueError("Affected session not found.")

session = record.iloc[0]

print("Checking anonymous session identity links...\n")

has_contact = (
    pd.notna(session["contact_id"])
    and str(session["contact_id"]).strip() != ""
)

has_evidence = (
    session["identity_link_evidence"] != "NONE"
)

has_consent = (
    session["consent_status"] == "YES"
)

if has_contact and not (has_evidence and has_consent):
    print("ANOMALY DETECTED!")
    print("Session:", session_id)
    print("Linked contact:", session["contact_id"])
    print("Identity evidence:", session["identity_link_evidence"])
    print("Consent:", session["consent_status"])
    print("Decision: FLAG")
    print("Reason: Contact linking requires valid identity evidence and consent.")
else:
    print("No anonymous identity-linking anomaly detected.")
