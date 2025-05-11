WITH degrees AS (
    SELECT DISTINCT DEGREES_AWARDED_PREDOMINANT as predominant_degree_id
    FROM {{ ref('stg_school_data') }}
),
predominant_degree AS (
    SELECT predominant_degree_id,
        CASE 
            WHEN predominant_degree_id = 1 THEN 'Predominantly certificate-degree granting'
            WHEN predominant_degree_id = 2 THEN 'Predominantly associate`s-degree granting'
            WHEN predominant_degree_id = 3 THEN 'Predominantly bachelor`s-degree granting'
            WHEN predominant_degree_id = 4 THEN 'Entirely graduate-degree granting'
            ELSE 'Not classified'
        END AS predominant_degree_classification
    FROM degrees
)

SELECT predominant_degree_id, predominant_degree_classification
FROM predominant_degree
