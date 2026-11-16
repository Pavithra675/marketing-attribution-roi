
import pandas as pd

attribution = pd.read_csv("attribution_results.csv")
costs = pd.read_csv("cost_records.csv")
campaigns = pd.read_csv("campaigns.csv")

# Calculate campaign revenue for each model
revenue = (
    attribution.groupby(["model", "campaign_id"])
    ["attributed_revenue"].sum()
    .reset_index()
)

# Include every campaign, even those with zero attributed revenue
all_results = []

for model in ["First Touch", "Last Touch", "Linear"]:

    model_revenue = revenue[
        revenue["model"] == model
    ]

    report = campaigns[
        ["campaign_id", "campaign_name"]
    ].merge(
        costs[["campaign_id", "cost_amount", "currency"]],
        on="campaign_id",
        how="left"
    )

    report = report.merge(
        model_revenue[["campaign_id", "attributed_revenue"]],
        on="campaign_id",
        how="left"
    )

    report["attributed_revenue"] = (
        report["attributed_revenue"].fillna(0)
    )

    report["ROI_percent"] = (
        (report["attributed_revenue"] - report["cost_amount"])
        / report["cost_amount"] * 100
    )

    report["ROAS"] = (
        report["attributed_revenue"] / report["cost_amount"]
    )

    report["model"] = model

    all_results.append(report)

final_report = pd.concat(all_results, ignore_index=True)

final_report.to_csv("campaign_roi_report.csv", index=False)

print("ROI calculation completed!")
print("\nTop campaigns by ROI:")

print(
    final_report[
        final_report["model"] == "Linear"
    ].sort_values(
        "ROI_percent", ascending=False
    ).head(10)
)

print("\nSaved campaign_roi_report.csv")
