-- Query: Top 3 Campaigns by ROI
-- Business question: Which campaigns should receive increased budget allocation?
-- Key metric: roi_pct
-- Insight: All 3 top ROI campaigns are Email type — business should prioritize 
--          Email campaigns and reduce Telemarketing spend


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
        RANK() OVER (ORDER BY roi_pct DESC) AS roi_rank
    FROM campaign_metrics
)
SELECT
    campaign_id,
    campaign_type,
    budget,
    conversion_rate_pct,
    total_revenue,
    roi_pct,
    roi_rank
FROM ranked
WHERE roi_rank <= 3
ORDER BY roi_rank;