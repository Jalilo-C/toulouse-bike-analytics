SELECT
    station_id,
    collected_at,
    COUNT(*) AS occurrences
FROM {{ ref('fct_station_availability') }}
GROUP BY
    station_id,
    collected_at
HAVING
    COUNT(*)>1