SELECT *
FROM {{ ref('dim_time') }}
WHERE hour < 0
   OR hour > 23
   OR hour IS NULL