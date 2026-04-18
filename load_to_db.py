import pandas as pd 
import sqlite3

# create/connect database
conn = sqlite3.connect("campaign_analytics.db")

# cursor (optional for raw SQL execution)
cursor = conn.cursor()

# load CSVs
customers = pd.read_csv(r"data/customers.csv")
campaigns = pd.read_csv(r"data/campaigns.csv")
transactions = pd.read_csv(r"data/transactions.csv")
responses = pd.read_csv(r"data/campaign_responses.csv")

# push to SQLite
customers.to_sql("customers", conn, if_exists="replace", index=False)
campaigns.to_sql("campaigns", conn, if_exists="replace", index=False)
transactions.to_sql("transactions", conn, if_exists="replace", index=False)
responses.to_sql("campaign_responses", conn, if_exists="replace", index=False)

# Verify row counts
tables = ["customers", "campaigns", "transactions", "campaign_responses"]

for table in tables:
    query = f"SELECT COUNT(*) as count FROM {table}"
    count = pd.read_sql(query, conn)["count"][0]
    print(f"{table}: {count} rows")

# 6. Confirmation
print("\n✅ All tables loaded successfully into campaign_analytics.db")

# close connection
conn.close()