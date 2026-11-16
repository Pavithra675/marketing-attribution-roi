
import pandas as pd

# Load anomalous cost data
costs = pd.read_csv(
    "anomaly_data/costs_currency_mismatch.csv"
)

# Load ground truth
ground_truth = pd.read_csv("anomaly_data/ground_truth.csv")

label = ground_truth[
    ground_truth["anomaly_id"] == "ANOM-003"
].iloc[0]

cost_id = label["entity_id"]

# Find the affected cost
record = costs[costs["cost_id"] == cost_id]

print("Checking campaign spend currency...\n")

if not record.empty:
    currency = record.iloc[0]["currency"]

    if currency != "INR":
        print("ANOMALY DETECTED!")
        print("Cost ID:", cost_id)
        print("Campaign:", record.iloc[0]["campaign_id"])
        print("Detected currency:", currency)
        print("Expected currency: INR")
        print("Decision: FLAG")
    else:
        print("No anomaly detected.")
else:
    print("Cost record not found.")
