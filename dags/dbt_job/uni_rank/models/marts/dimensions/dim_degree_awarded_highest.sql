WITH degree AS (
    SELECT DISTINCT degrees_awarded_highest as highest_degree_id
    FROM {{ ref('stg_school_data') }}
),
highest_degree AS (
    SELECT highest_degree_id,
        CASE 
            WHEN highest_degree_id = 1 THEN 'Certificate degree'
            WHEN highest_degree_id = 2 THEN 'Associate degree'
            WHEN highest_degree_id = 3 THEN 'Bachelor`s degree'
            WHEN highest_degree_id = 4 THEN 'Graduate degree'
            ELSE 'Non-degree-granting'
        END AS type_of_degree
    FROM degree
)

SELECT highest_degree_id, type_of_degree
FROM highest_degree
