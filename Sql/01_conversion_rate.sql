-- Query: Conversion Rate per Campaign
-- Business question: Which campaigns are generating the most customer engagement?
-- Key metric: conversion_rate_pct
-- Insight: High conversion rate does not guarantee high revenue (see C014)



SELECT
    c.campaign_id,
    c.campaign_type,
    COUNT(cr.customer_id) AS total_targeted,
    SUM(cr.conversion) AS total_conversions,
    ROUND(CAST(SUM(cr.conversion) AS FLOAT) 
          / COUNT(cr.customer_id) * 100, 2) AS conversion_rate_pct
FROM campaigns c
LEFT JOIN campaign_responses cr ON c.campaign_id = cr.campaign_id
GROUP BY c.campaign_id, c.campaign_type
ORDER BY conversion_rate_pct DESC;
