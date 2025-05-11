WITH carnegien as (
    SELECT CARNEGIEBASIC_ID as carnegie_basic_id,
        CARNEGIEBASIC as carnegie_basic_classification
    FROM 
        {{ source('uni_ranking', 'carnegie_basic_dict') }}
)

SELECT *
FROM 
    carnegien