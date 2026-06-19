-- 02_host_performance.sql
-- Ranking de hosts por desempeño con score compuesto

WITH host_metrics AS (
    SELECT
        l.host_id,
        l.host_name,
        -- Potencial de ingresos: precio promedio por cantidad máxima de listings del host
        AVG(l.price) * MAX(l.calculated_host_listings_count) AS revenue_potential,
        -- Promedio de calificación, si existe columna rating en fact_reviews
        COALESCE(AVG(r.rating), 0) AS avg_rating,
        -- Tasa de respuesta rápida (ejemplo, si exite response_time en fact_reviews)
        COALESCE(
            SUM(CASE WHEN r.response_time < '24:00:00' THEN 1 ELSE 0 END) / NULLIF(COUNT(r.response_time), 0),
            0
        ) AS response_rate,
        -- Cantidad de listings del host
        COUNT(l.id) AS listings_count
    FROM dim_listings l
    LEFT JOIN fact_reviews r ON l.id = r.listing_id
    GROUP BY l.host_id, l.host_name
),
performance_score AS (
    SELECT
        *,
        (revenue_potential * 0.4) + (avg_rating * 0.3) + (response_rate * 0.2) + (listings_count * 0.1) AS score
    FROM host_metrics
)
SELECT
    host_id,
    host_name,
    score AS performance_score,
    RANK() OVER (ORDER BY score DESC) AS ranking,
    JSON_OBJECT(
        'revenue_potential', revenue_potential,
        'avg_rating', avg_rating,
        'response_rate', response_rate,
        'listings_count', listings_count
    ) AS key_metrics_breakdown
FROM performance_score
ORDER BY ranking;
