WITH open_policy AS (
    SELECT DISTINCT open_admissions_policy
    FROM 
        {{ ref('stg_school_data') }}
),
name_policy AS (
    SELECT open_admissions_policy as open_admissions_policy_id,
        CASE 
            WHEN open_admissions_policy = 1 THEN 'Yes'
            WHEN open_admissions_policy = 2 THEN 'No'
            WHEN open_admissions_policy = 3 THEN 'Does not enroll first-time students'
            ELSE 'Not Specified'
        END AS policy_name
    FROM open_policy
)

SELECT open_admissions_policy_id, policy_name
FROM name_policy
