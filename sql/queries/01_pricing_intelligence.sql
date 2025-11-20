-- 01_pricing_intelligence.sql
-- Identifica listings sobrevalorados o subvalorados comparando con promedio del vecindario

WITH neighborhood_property_stats AS (
    SELECT
        neighbourhood,
        room_type,
        AVG(price) AS avg_price,
        STDDEV(price) AS stddev_price
    FROM dim_listings
    GROUP BY neighbourhood, room_type
),
listings_with_stats AS (
    SELECT
        l.id AS listing_id,
        l.price AS current_price,
        nps.avg_price,
        nps.stddev_price,
        CASE
            WHEN nps.avg_price IS NULL THEN NULL
            ELSE
                (l.price - nps.avg_price) / NULLIF(nps.avg_price, 0) * 100
        END AS price_difference_pct
    FROM dim_listings l
    LEFT JOIN neighborhood_property_stats nps
        ON l.neighbourhood = nps.neighbourhood AND l.room_type = nps.room_type
)
SELECT
    listing_id,
    current_price,
    avg_price AS market_average,
    price_difference_pct,
    CASE
        WHEN price_difference_pct IS NULL THEN 'no data'
        WHEN price_difference_pct > 20 THEN 'overpriced'
        WHEN price_difference_pct < -20 THEN 'underpriced'
        ELSE 'fair'
    END AS recommendation
FROM listings_with_stats
ORDER BY recommendation DESC, price_difference_pct DESC;
