SELECT 
    station_id,
    name AS station_name,
    lat AS latitude,
    lon as longitude,
    address,
    capacity
FROM {{ source('toulouse_bikes', 'station_infos') }}