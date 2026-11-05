SELECT *
FROM {{ ref('agg_station_availability') }}
WHERE nb_snapshots <= 0
   OR avg_bikes_available < 0
   OR pct_empty_snapshots < 0
   OR pct_empty_snapshots > 100