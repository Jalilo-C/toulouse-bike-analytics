SELECT
    station_id,
    collected_at,
    mechanical_bikes_available,
    electric_bikes_available,
    total_bikes_available AS bikes_available,
    bikes_disabled,
    docks_available,
    docks_disabled,
    is_renting,
    is_returning,
    source_last_updated AS source_updated_at,
    last_reported
FROM {{ source('toulouse_bikes', 'station_status') }}