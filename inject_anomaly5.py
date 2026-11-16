import pandas as pd
from pathlib import Path

Path("anomaly_data").mkdir(exist_ok=True)

# Create a small web session dataset
sessions = pd.DataFrame([
    {
        "session_id": "SES-000001",
        "anonymous_id": "ANON-001",
        "contact_id": "",
        "identity_evidence": "NONE",
        "consent_status": "NO"
    },
    {
        "session_id": "SES-000002",
        "anonymous_id": "ANON-002",
        "contact_id": "CON-000001",
        "identity_evidence": "LOGIN",
        "consent_status": "YES"
    },
    {
        "session_id": "SES-000003",
        "anonymous_id": "ANON-003",
        "contact_id": "",
        "identity_evidence": "NONE",
        "consent_status": "NO"
    }
])

# Save the original session data
sessions.to_csv("web_sessions.csv", index=False)

# Inject an invalid identity link into a separate test dataset
anomalous = sessions.copy()

contact_id = pd.read_csv("contacts.csv").iloc[0]["contact_id"]

anomalous.loc[0, "contact_id"] = contact_id

anomalous.to_csv(
    "anomaly_data/web_sessions_anonymous_link.csv",
    index=False
)

# Add the anomaly to ground truth
ground_truth_path = Path("anomaly_data/ground_truth.csv")
ground_truth = pd.read_csv(ground_truth_path)

new_label = pd.DataFrame([{
    "anomaly_id": "ANOM-005",
    "anomaly_type": "ANONYMOUS_SESSION_LINKED_WITHOUT_EVIDENCE",
    "entity_id": "SES-000001",
    "expected_result": "FLAG",
    "reason": "Anonymous session linked to a contact without identity evidence or consent"
}])

ground_truth = pd.concat(
    [ground_truth, new_label],
    ignore_index=True
)

ground_truth.to_csv(ground_truth_path, index=False)

print("Anonymous session linking anomaly created!")
print("Affected session: SES-000001")
print("Linked contact:", contact_id)
print("Identity evidence: NONE")
print("Consent: NO")
print("Expected decision: FLAG")