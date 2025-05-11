WITH institution AS (
    SELECT DISTINCT INSTITUTIONAL_CHARACTERISTICS_LEVEL
    FROM {{ ref('stg_school_data') }}
),
institute_level AS (
    SELECT INSTITUTIONAL_CHARACTERISTICS_LEVEL,
        CASE 
            WHEN INSTITUTIONAL_CHARACTERISTICS_LEVEL = 1 THEN '4-year'
            WHEN INSTITUTIONAL_CHARACTERISTICS_LEVEL = 2 THEN '2-year'
            ELSE 'Less than 2-year'
        END AS level_name
    FROM institution
)

SELECT INSTITUTIONAL_CHARACTERISTICS_LEVEL, level_name
FROM institute_level
