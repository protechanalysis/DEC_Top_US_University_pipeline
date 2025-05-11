WITH all_data as (
    SELECT * 
    FROM 
        {{ source('uni_ranking', 'school_data') }}
),
data_select as (
    SELECT
        RANK, ID, SCHOOL_NAME, ADDRESS,
        CITY, STATE_CODE, STATE_FIPS, REGION_ID,
        SCHOOL_LOCALE, SCHOOL_URL, SCHOOL_OWNERSHIP,
        SCHOOL_ACCREDITOR, PRICE_CALCULATOR_URL,
        ONLINE_ONLY, MAIN_CAMPUS,
        INSTITUTIONAL_CHARACTERISTICS_LEVEL, 
        OPEN_ADMISSIONS_POLICY, DEGREES_AWARDED_PREDOMINANT, degrees_awarded_highest,
        BOOKSUPPLY_COST, TEST_REQUIREMENTS, SAT_SCORES_OVERALL_AVERAGE,
        CARNEGIE_BASIC, ACT_SCORES_50TH_PERCENTILE,
        COST_OF_ATTENDANCE, AVG_NET_PRICE_OVERALL,
        TUITION_IN_STATE, TUITION_OUT_OF_STATE,
        ROOMBOARD_OFFCAMPUS, ROOMBOARD_ONCAMPUS,
        OTHEREXPENSE_ONCAMPUS, OTHEREXPENSE_OFFCAMPUS,
        STUDENT_SIZE, GRAD_ENROLLMENT_12_MONTH,
        UNDERGRAD_ENROLLMENT_12_MONTH,
        {{ percent_conversion('pell_grant_rate') }} AS pell_grant_rate,
        {{ percent_conversion('admission_rate_overall') }} AS admission_rate_overall,
        {{ percent_conversion('completion_rate_suppressed') }} AS completion_rate_suppressed,
        {{ percent_conversion('retention_rate_full_time') }} AS retention_rate_full_time,
        {{ percent_conversion('federal_loan_rate') }} AS federal_loan_rate,
        {{ percent_conversion('student_demographics_men') }} AS student_demographics_men,
        {{ percent_conversion('student_demographics_women') }} AS student_demographics_women,
        {{ percent_conversion('faculty_demographics_men') }} AS faculty_demographics_men,
        {{ percent_conversion('faculty_demographics_women') }} AS faculty_demographics_women
    FROM
        all_data
)

SELECT *
FROM data_select