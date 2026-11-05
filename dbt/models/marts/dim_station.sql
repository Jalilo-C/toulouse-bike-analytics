WITH stations AS (
    SELECT
        station_id,
        station_name,
        latitude,
        longitude,
        address,
        capacity
    FROM {{ ref('stg_station_infos') }}
)

SELECT *
FROM stations