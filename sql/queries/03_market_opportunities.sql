WITH neighborhood_stats AS (
    SELECT
        neighbourhood,
        COUNT(DISTINCT id) AS supply,
        COUNT(r.review_id) AS demand
    FROM dim_listings l
    LEFT JOIN fact_reviews r ON l.id = r.listing_id
    GROUP BY neighbourhood
),
scores_base AS (
    SELECT
        neighbourhood,
        demand,
        supply,
        demand * 1.0 / NULLIF(MAX(demand) OVER (), 0) AS demand_score,
        supply * 1.0 / NULLIF(MAX(supply) OVER (), 0) AS supply_score
    FROM neighborhood_stats
),
scores AS (
    SELECT
        neighbourhood,
        demand_score,
        supply_score,
        (demand_score - supply_score) AS opportunity_score
    FROM scores_base
)
SELECT
    neighbourhood AS neighborhood,
    demand_score,
    supply_score,
    opportunity_score,
    CASE
        WHEN opportunity_score > 0.2 THEN 'high opportunity'
        ELSE 'normal'
    END AS recommended_action
FROM scores
ORDER BY opportunity_score DESC;
