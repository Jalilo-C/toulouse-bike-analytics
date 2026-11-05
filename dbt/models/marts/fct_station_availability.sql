WITH availability AS (
    SELECT
        station_id,
        collected_at,
        mechanical_bikes_available,
        electric_bikes_available,
        bikes_available,
        bikes_disabled,
        docks_available,
        docks_disabled,
        is_renting,
        is_returning
    FROM {{ ref('stg_station_status') }}
)

SELECT *
FROM availability