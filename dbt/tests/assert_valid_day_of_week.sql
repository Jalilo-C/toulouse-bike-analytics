SELECT *
FROM {{ ref('dim_time') }}
WHERE day_of_week < 1
   OR day_of_week > 7
   OR day_of_week IS NULL