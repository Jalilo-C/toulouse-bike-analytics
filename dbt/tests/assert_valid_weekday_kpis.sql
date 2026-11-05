SELECT *
FROM {{ ref('agg_weekday_availability') }}
WHERE
    day_of_week NOT BETWEEN 1 AND 7 OR 
    day_of_week IS NULL OR
    avg_bikes_available < 0 OR
    pct_empty_snapshots NOT BETWEEN 0 AND 100 