WITH bike_data AS (
    SELECT
        station_id,
        electric_bikes_available,
        bikes_available
    FROM {{ ref('fct_station_availability') }}
),

bike_kpis AS (
    SELECT
        station_id,
        AVG(electric_bikes_available) AS avg_electric_bikes_available,
        100.0 *
        SUM(electric_bikes_available)
            FILTER (WHERE bikes_available IS NOT NULL)
        /
        NULLIF(
            SUM(bikes_available)
                FILTER (WHERE electric_bikes_available IS NOT NULL),
            0
        ) AS pct_electric_bikes
    FROM bike_data
    GROUP BY station_id
)

SELECT *
FROM bike_kpis