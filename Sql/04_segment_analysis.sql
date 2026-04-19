-- Query: Customer Segment Analysis
-- Business question: Which customer segments drive the most revenue?
-- Key metric: total_revenue
-- Insight: Premium segment (5.6% of customers) generates 75% of total revenue —
--          Mass segment has 10x more customers but 14x less revenue



SELECT
    cu.segment,
    COUNT(DISTINCT cr.customer_id) AS unique_customers_targeted,
    SUM(cr.conversion)             AS total_conversion_events,
    ROUND(CAST(SUM(cr.conversion) AS FLOAT)
          / COUNT(cr.customer_id) * 100, 2)     AS conversion_rate_pct,
    ROUND(SUM(t.amount), 2)                     AS total_revenue,
    ROUND(AVG(t.amount), 2)                     AS avg_transaction_value
FROM customers cu
LEFT JOIN campaign_responses cr ON cu.customer_id = cr.customer_id
LEFT JOIN transactions t
    ON cr.customer_id = t.customer_id
    AND cr.conversion = 1
GROUP BY cu.segment
ORDER BY total_revenue DESC;