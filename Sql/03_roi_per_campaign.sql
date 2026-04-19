-- Query: ROI per Campaign
-- Business question: Which campaigns deliver the best return on investment?
-- Key metric: roi_pct
-- Insight: ROI is the only metric that combines both cost and revenue —
--          Telemarketing campaigns occupy bottom 4 ROI positions due to 
--          high operational cost eroding returns despite decent conversions


SELECT
    c.campaign_id,
    c.campaign_type,
    c.budget,
    ROUND(SUM(t.amount), 2) AS total_revenue,
    ROUND(SUM(t.amount) - c.budget, 2)AS net_profit,
    ROUND((SUM(t.amount) - c.budget) 
          / c.budget * 100, 2) AS roi_pct
FROM campaigns c
LEFT JOIN campaign_responses cr 
    ON c.campaign_id = cr.campaign_id
LEFT JOIN transactions t 
    ON cr.customer_id = t.customer_id
    AND cr.conversion = 1
GROUP BY c.campaign_id, c.campaign_type, c.budget
ORDER BY roi_pct DESC;