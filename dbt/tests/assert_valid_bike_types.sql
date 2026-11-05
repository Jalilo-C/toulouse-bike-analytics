SELECT *
FROM {{ ref('agg_bike_types') }}
WHERE
    avg_electric_bikes_available < 0 OR
    pct_electric_bikes NOT BETWEEN 0 AND 100