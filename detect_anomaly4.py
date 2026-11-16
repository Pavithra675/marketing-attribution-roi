import pandas as pd

# Load the test data
costs = pd.read_csv("anomaly_data/costs_omitted.csv")
attribution = pd.read_csv("attribution_results.csv")
ground_truth = pd.read_csv("anomaly_data/ground_truth.csv")

# Get the affected campaign from ground truth
label = ground_truth[
    ground_truth["anomaly_id"] == "ANOM-004"
].iloc[0]

campaign_id = label["entity_id"]

# Check whether the campaign generated revenue
campaign_revenue = attribution[
    attribution["campaign_id"] == campaign_id
]["attributed_revenue"].sum()

# Check whether its cost record exists
campaign_cost = costs[
    costs["campaign_id"] == campaign_id
]

print("Checking for missing campaign costs...\n")

if campaign_revenue > 0 and campaign_cost.empty:
    print("ANOMALY DETECTED!")
    print("Campaign:", campaign_id)
    print("Attributed revenue:", campaign_revenue)
    print("Cost record: MISSING")
    print("Decision: FLAG")
    print("ROI: NOT CALCULATED")
    print("Reason: Missing cost must not be treated as zero.")
else:
    print("No campaign cost omission detected.")