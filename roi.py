
import pandas as pd

attribution = pd.read_csv("attribution_results.csv")
costs = pd.read_csv("cost_records.csv")
campaigns = pd.read_csv("campaigns.csv")

revenue = (
    attribution.groupby(["model", "campaign_id"])["attributed_revenue"]
    .sum()
    .reset_index()
)

all_results = []

for model in ["First Touch", "Last Touch", "Linear"]:
    model_revenue = revenue[revenue["model"] == model]

    report = campaigns[
        ["campaign_id", "campaign_name", "currency"]
    ].merge(
        costs[["campaign_id", "cost_amount", "currency"]],
        on="campaign_id",
        how="left",
        suffixes=("_campaign", "_cost"),
        validate="one_to_one"
    )

    report = report.merge(
        model_revenue[["campaign_id", "attributed_revenue"]],
        on="campaign_id",
        how="left"
    )

    report["attributed_revenue"] = report["attributed_revenue"].fillna(0)

    report["cost_status"] = "AVAILABLE"
    report.loc[report["cost_amount"].isna(), "cost_status"] = "MISSING"

    report["currency_status"] = "MATCHED"
    report.loc[
        report["cost_amount"].notna()
        & (report["currency_campaign"] != report["currency_cost"]),
        "currency_status"
    ] = "MISMATCH"

    valid = (
        report["cost_amount"].notna()
        & (report["cost_amount"] > 0)
        & (report["currency_status"] == "MATCHED")
    )

    report["ROI_percent"] = float("nan")
    report["ROAS"] = float("nan")

    report.loc[valid, "ROI_percent"] = (
        (report.loc[valid, "attributed_revenue"]
         - report.loc[valid, "cost_amount"])
        / report.loc[valid, "cost_amount"] * 100
    )

    report.loc[valid, "ROAS"] = (
        report.loc[valid, "attributed_revenue"]
        / report.loc[valid, "cost_amount"]
    )

    report["roi_status"] = "CALCULATED"
    report.loc[
        report["cost_status"] == "MISSING",
        "roi_status"
    ] = "NOT CALCULATED - MISSING COST"

    report.loc[
        report["currency_status"] == "MISMATCH",
        "roi_status"
    ] = "NOT CALCULATED - CURRENCY MISMATCH"

    report["model"] = model
    all_results.append(report)

final_report = pd.concat(all_results, ignore_index=True)
final_report.to_csv("campaign_roi_report.csv", index=False)

print("ROI calculation completed!")
print("\nROI status:")
print(final_report.groupby(["model", "roi_status"]).size())

print("\nTop campaigns by Linear ROI:")
print(
    final_report[
        (final_report["model"] == "Linear")
        & (final_report["roi_status"] == "CALCULATED")
    ].sort_values("ROI_percent", ascending=False).head(10)
)

print("\nSaved campaign_roi_report.csv")
