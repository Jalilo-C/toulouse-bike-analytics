WITH availability AS (
    SELECT
        station_id,
        bikes_available
    FROM {{ ref('fct_station_availability') }}
),

station_kpis AS (
    SELECT
        station_id,
        -- KPI 1 : nb_snapshots
        COUNT(*) AS nb_snapshots,
        -- KPI 2 : avg_bikes_available
        AVG(bikes_available) AS avg_bikes_available,
        -- KPI 3 : pct_empty_snapshots
        100.0 * SUM(
            CASE
                WHEN bikes_available = 0 THEN 1
                ELSE 0
            END
        ) / NULLIF(COUNT(bikes_available), 0) AS pct_empty_snapshots
    FROM availability
    GROUP BY station_id
)

SELECT *
FROM station_kpis