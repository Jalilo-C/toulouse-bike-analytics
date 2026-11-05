WITH timestamps AS (
    SELECT DISTINCT collected_at
    FROM {{ ref('stg_station_status') }}
),

time_attributes AS (
    SELECT
        collected_at,
        (collected_at AT TIME ZONE 'Europe/Paris')::date AS date_local,

        EXTRACT(
            HOUR FROM collected_at AT TIME ZONE 'Europe/Paris'
        ) AS hour,

        EXTRACT(
            ISODOW FROM collected_at AT TIME ZONE 'Europe/Paris'
        ) AS day_of_week

    FROM timestamps
),

final AS (
    SELECT
        collected_at,
        date_local,
        hour,
        day_of_week,

        CASE
            WHEN day_of_week IN (6, 7) THEN TRUE
            ELSE FALSE
        END AS is_weekend

    FROM time_attributes
)

SELECT *
FROM final