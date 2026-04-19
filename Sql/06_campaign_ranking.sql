-- Query: Campaign Ranking using Window Functions
-- Business question: How do campaigns rank simultaneously across ROI, 
--                    conversion rate and revenue?
-- Key metric: roi_rank
-- Insight: Rankings conflict sharply across metrics — a campaign can rank #1 
--          in conversion and #20 in revenue, proving single-metric analysis 
--          leads to wrong business decisions

WITH campaign_metrics AS (
    SELECT
        c.campaign_id,
        c.campaign_type,
        c.budget,
        ROUND(CAST(SUM(cr.conversion) AS FLOAT)
              / COUNT(cr.customer_id) * 100, 2)     AS conversion_rate_pct,
        ROUND(SUM(t.amount), 2)                     AS total_revenue,
        ROUND((SUM(t.amount) - c.budget)
              / c.budget * 100, 2)                  AS roi_pct
    FROM campaigns c
    LEFT JOIN campaign_responses cr 
        ON c.campaign_id = cr.campaign_id
    LEFT JOIN transactions t
        ON cr.customer_id = t.customer_id
        AND cr.conversion = 1
    GROUP BY c.campaign_id, c.campaign_type, c.budget
),
ranked AS (
    SELECT
        *,
        RANK() OVER (ORDER BY roi_pct DESC)              AS roi_rank,
        RANK() OVER (ORDER BY conversion_rate_pct DESC)  AS conversion_rank,
        RANK() OVER (ORDER BY total_revenue DESC)        AS revenue_rank
    FROM campaign_metrics
)
SELECT *
FROM ranked
ORDER BY roi_rank;