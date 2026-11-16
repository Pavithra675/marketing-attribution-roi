import pandas as pd

sessions = pd.read_csv(
    "anomaly_data/web_sessions_anonymous_link.csv"
)

ground_truth = pd.read_csv(
    "anomaly_data/ground_truth.csv"
)

label = ground_truth[
    ground_truth["anomaly_id"] == "ANOM-005"
].iloc[0]

session_id = label["entity_id"]

session = sessions[
    sessions["session_id"] == session_id
].iloc[0]

print("Checking anonymous session identity links...\n")

has_contact = pd.notna(session["contact_id"]) and str(
    session["contact_id"]
).strip() != ""

has_evidence = session["identity_evidence"] != "NONE"
has_consent = session["consent_status"] == "YES"

if has_contact and not (has_evidence and has_consent):
    print("ANOMALY DETECTED!")
    print("Session:", session_id)
    print("Linked contact:", session["contact_id"])
    print("Identity evidence:", session["identity_evidence"])
    print("Consent:", session["consent_status"])
    print("Decision: FLAG")
    print("Reason: Contact linking requires valid identity evidence and consent.")
else:
    print("No anonymous identity-linking anomaly detected.")