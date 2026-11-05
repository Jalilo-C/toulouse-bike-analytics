WITH hourly_data AS (
    SELECT
        t.hour,
        f.bikes_available
    FROM {{ ref('fct_station_availability') }} f
    JOIN {{ ref('dim_time') }} t
        ON f.collected_at = t.collected_at
),

hourly_kpis AS (
    SELECT
        hour,
        AVG(bikes_available) AS avg_bikes_available,
        100.0 * SUM(
            CASE 
                WHEN bikes_available = 0 then 1
                ELSE 0
            END
        ) / NULLIF(COUNT(bikes_available), 0) AS pct_empty_snapshots
    FROM hourly_data
    GROUP BY hour
)

SELECT *
FROM hourly_kpis
ORDER BY hour