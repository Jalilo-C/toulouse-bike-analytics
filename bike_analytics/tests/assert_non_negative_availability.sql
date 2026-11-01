SELECT *
FROM {{ ref('fct_station_availability') }}
WHERE mechanical_bikes_available < 0
   OR electric_bikes_available < 0
   OR bikes_available < 0
   OR bikes_disabled < 0
   OR docks_available < 0
   OR docks_disabled < 0