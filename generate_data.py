import os
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# -----------------------
# GLOBAL SEED (reproducibility)
# -----------------------
np.random.seed(42)
random.seed(42)


# -----------------------
# STEP 2 — CUSTOMERS
# -----------------------
def generate_customers(n=2000):
    customer_id = np.arange(1, n + 1)

    age = np.random.randint(22, 66, size=n)

    # lognormal (right-skewed)
    income = np.random.lognormal(mean=11, sigma=0.5, size=n)

    cities = [
        "Mumbai", "Delhi", "Bangalore", "Hyderabad",
        "Chennai", "Pune", "Kolkata", "Ahmedabad"
    ]
    city = np.random.choice(cities, size=n)

    # inject missing income (5%)
    mask = np.random.choice([True, False], size=n, p=[0.05, 0.95])
    income[mask] = np.nan

    def assign_segment(inc):
        if pd.isna(inc):
            return "Unknown"
        elif inc < 30000:
            return "Youth"
        elif inc < 100000:
            return "Mass"
        elif inc < 120000:
            return "Affluent"
        else:
            return "Premium"

    segment = [assign_segment(i) for i in income]

    return pd.DataFrame({
        "customer_id": customer_id,
        "age": age,
        "income": income,
        "city": city,
        "segment": segment
    })


# -----------------------
# STEP 3 — CAMPAIGNS
# -----------------------
def generate_campaigns(n=20):
    campaign_ids = [f"C{str(i).zfill(3)}" for i in range(1, n + 1)]

    campaign_types = ['Email', 'SMS', 'Push', 'Telemarketing']

    budget_map = {
        'Email': (5000, 20000),
        'SMS': (10000, 30000),
        'Push': (8000, 25000),
        'Telemarketing': (30000, 100000)
    }

    start_base = datetime(2023, 1, 1)

    rows = []

    for cid in campaign_ids:
        ctype = random.choice(campaign_types)

        start_date = start_base + timedelta(days=random.randint(0, 364))
        duration = random.randint(15, 60)
        end_date = start_date + timedelta(days=duration)

        budget = random.randint(*budget_map[ctype])

        rows.append([
            cid, ctype,
            start_date.date(),
            end_date.date(),
            budget
        ])

    return pd.DataFrame(rows, columns=[
        "campaign_id", "campaign_type",
        "start_date", "end_date", "budget"
    ])


# -----------------------
# STEP 4 — TRANSACTIONS
# -----------------------
def generate_transactions(customers_df, n=5000):
    transaction_ids = [f"T{str(i).zfill(5)}" for i in range(1, n + 1)]

    sampled_customers = np.random.choice(
        customers_df["customer_id"], size=n, replace=True
    )

    df = pd.DataFrame({
        "transaction_id": transaction_ids,
        "customer_id": sampled_customers
    })

    # JOIN → get segment
    df = df.merge(
        customers_df[["customer_id", "segment"]],
        on="customer_id",
        how="left"
    )

    amount_map = {
        "Youth": (100, 3000),
        "Mass": (1000, 15000),
        "Affluent": (10000, 100000),
        "Premium": (50000, 300000),   
        "Unknown": (500, 8000)
    }

    def assign_amount(seg):
        low, high  = amount_map[seg]
        return random.randint(low, high)

    df["amount"] = df["segment"].apply(assign_amount)

    start_date = datetime(2023, 1, 1)

    df["transaction_date"] = [
        (start_date + timedelta(days=random.randint(0, 364))).date()
        for _ in range(n)
    ]

    return df[[
        "transaction_id",
        "customer_id",
        "amount",
        "transaction_date"
    ]]


# -----------------------
# STEP 5 — CAMPAIGN RESPONSES
# -----------------------
def generate_campaign_responses(customers_df, campaigns_df, n=3000):
    customer_ids = np.random.choice(customers_df["customer_id"], size=n, replace=True)
    campaign_ids = np.random.choice(campaigns_df["campaign_id"], size=n, replace=True)

    df = pd.DataFrame({
        "customer_id": customer_ids,
        "campaign_id": campaign_ids
    })

    # JOIN → get segment
    df = df.merge(
        customers_df[["customer_id", "segment"]],
        on="customer_id",
        how="left"
    )

    conversion_map = {
        "Youth": 0.08,
        "Mass": 0.12,
        "Affluent": 0.22,
        "Premium": 0.30,
        "Unknown": 0.05
    }

    df["p"] = df["segment"].map(conversion_map)
    df["conversion"] = np.random.binomial(1, df["p"])

    def assign_response(conv):
        if conv == 1:
            return np.random.choice(["Clicked", "Clicked", "Clicked", "Ignored"])
        else:
            return np.random.choice(["Ignored", "Ignored", "Ignored", "Unsubscribed"])

    df["response"] = df["conversion"].apply(assign_response)

    df = df.drop_duplicates(subset=["customer_id", "campaign_id"])

    return df[[
        "customer_id",
        "campaign_id",
        "response",
        "conversion"
    ]]


# -----------------------
# MAIN PIPELINE
# -----------------------
def main():
    os.makedirs("data", exist_ok=True)

    customers_df = generate_customers(2000)
    campaigns_df = generate_campaigns(20)
    transactions_df = generate_transactions(customers_df, 5000)
    responses_df = generate_campaign_responses(customers_df, campaigns_df, 3000)

    # validation
    assert len(customers_df) == 2000
    assert len(campaigns_df) == 20
    assert len(transactions_df) == 5000
    assert len(responses_df) > 2500

    print("\n--- Customers ---")
    print(customers_df['segment'].value_counts())
    print(customers_df['income'].describe().apply(lambda x: f"{x:,.0f}"))

    print("\n--- Transactions ---")
    print(f"Amount range: {transactions_df['amount'].min():,} – {transactions_df['amount'].max():,}")
    print(f"Avg amount: {transactions_df['amount'].mean():,.0f}")

    print("\n--- Responses ---")
    print(f"Total responses: {len(responses_df)}")
    print(f"Overall conversion rate: {responses_df['conversion'].mean():.1%}")
    print(responses_df.merge(customers_df[['customer_id','segment']], on='customer_id')
        .groupby('segment')['conversion'].mean().apply(lambda x: f"{x:.1%}"))

    # save
    customers_df.to_csv("data/customers.csv", index=False)
    campaigns_df.to_csv("data/campaigns.csv", index=False)
    transactions_df.to_csv("data/transactions.csv", index=False)
    responses_df.to_csv("data/campaign_responses.csv", index=False)

    print("✅ All datasets generated successfully in /data folder")


if __name__ == "__main__":
    main()