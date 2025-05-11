WITH ownership_status AS (
    SELECT DISTINCT SCHOOL_OWNERSHIP
    FROM {{ ref('stg_school_data') }}
),
status_name AS (
    SELECT SCHOOL_OWNERSHIP,
        CASE 
            WHEN SCHOOL_OWNERSHIP = 1 THEN 'Public'
            WHEN SCHOOL_OWNERSHIP = 2 THEN 'Private Nonprofit'
            ELSE 'Private For-Profit'
        END AS ownership_purpose
    FROM ownership_status
)

SELECT SCHOOL_OWNERSHIP, ownership_purpose
FROM status_name
