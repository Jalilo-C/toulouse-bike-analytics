SELECT *
FROM {{ ref('agg_hourly_availability') }}
WHERE
    hour NOT BETWEEN 0 AND 23 OR 
    hour IS NULL OR
    avg_bikes_available < 0 OR
    pct_empty_snapshots NOT BETWEEN 0 AND 100 