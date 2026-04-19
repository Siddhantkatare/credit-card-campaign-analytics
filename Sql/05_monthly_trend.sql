-- Query: Monthly Revenue Trend
-- Business question: How does revenue and transaction volume trend across 2023?
-- Key metric: monthly_revenue
-- Insight: Transaction volume grows steadily through the year — October peaks 
--          at highest revenue, February is weakest month and needs campaign push

SELECT
    strftime('%Y-%m', t.transaction_date)       AS month,
    COUNT(DISTINCT t.transaction_id)            AS total_transactions,
    ROUND(SUM(t.amount), 2)                     AS monthly_revenue,
    ROUND(AVG(t.amount), 2)                     AS avg_transaction_value
FROM transactions t
GROUP BY strftime('%Y-%m', t.transaction_date)
ORDER BY month ASC;