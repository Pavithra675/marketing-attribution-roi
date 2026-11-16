
import pandas as pd
from pathlib import Path


def test_all_csv_files_exist():
    files = [
        "campaigns.csv",
        "contacts.csv",
        "touchpoints.csv",
        "leads.csv",
        "opportunities.csv",
        "orders.csv",
        "cost_records.csv",
        "attribution_results.csv",
    ]

    for file in files:
        assert Path(file).exists(), f"{file} is missing"


def test_campaign_ids_are_unique():
    df = pd.read_csv("campaigns.csv")
    assert df["campaign_id"].is_unique


def test_contact_ids_are_unique():
    df = pd.read_csv("contacts.csv")
    assert df["contact_id"].is_unique


def test_touchpoints_reference_valid_campaigns():
    touchpoints = pd.read_csv("touchpoints.csv")
    campaigns = pd.read_csv("campaigns.csv")

    assert touchpoints["campaign_id"].isin(
        campaigns["campaign_id"]
    ).all()


def test_orders_are_linked_to_won_opportunities():
    orders = pd.read_csv("orders.csv")
    opportunities = pd.read_csv("opportunities.csv")

    won_ids = set(
        opportunities.loc[
            opportunities["stage"] == "Won",
            "opportunity_id"
        ]
    )

    assert orders["opportunity_id"].isin(won_ids).all()


def test_costs_are_positive():
    costs = pd.read_csv("cost_records.csv")
    assert (costs["cost_amount"] > 0).all()


def test_attribution_revenue_is_not_negative():
    attribution = pd.read_csv("attribution_results.csv")
    assert (attribution["attributed_revenue"] >= 0).all()
