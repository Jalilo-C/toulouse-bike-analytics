WITH daily_data AS (
    SELECT
        t.day_of_week,
        f.bikes_available
    FROM {{ ref('fct_station_availability') }} f
    JOIN {{ ref('dim_time') }} t
        ON f.collected_at = t.collected_at
),

daily_kpis AS (
    SELECT
        day_of_week,
        AVG(bikes_available) AS avg_bikes_available,
        100.0 * SUM(
            CASE 
                WHEN bikes_available = 0 then 1
                ELSE 0
            END
        ) / NULLIF(COUNT(bikes_available), 0) AS pct_empty_snapshots
    FROM daily_data
    GROUP BY day_of_week
)

SELECT *
FROM daily_kpis
ORDER BY day_of_week