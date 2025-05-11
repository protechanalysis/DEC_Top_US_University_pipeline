SELECT 
    RANK, ID, SCHOOL_OWNERSHIP,
    ONLINE_ONLY, MAIN_CAMPUS,
    INSTITUTIONAL_CHARACTERISTICS_LEVEL, 
    OPEN_ADMISSIONS_POLICY,degrees_awarded_highest, 
    DEGREES_AWARDED_PREDOMINANT, SAT_SCORES_OVERALL_AVERAGE,
    BOOKSUPPLY_COST, TEST_REQUIREMENTS,
    CARNEGIE_BASIC, ACT_SCORES_50TH_PERCENTILE,
    COST_OF_ATTENDANCE, AVG_NET_PRICE_OVERALL,
    TUITION_IN_STATE, TUITION_OUT_OF_STATE,
    ROOMBOARD_OFFCAMPUS, ROOMBOARD_ONCAMPUS,
    OTHEREXPENSE_ONCAMPUS, OTHEREXPENSE_OFFCAMPUS,
    STUDENT_SIZE, GRAD_ENROLLMENT_12_MONTH,
    UNDERGRAD_ENROLLMENT_12_MONTH, pell_grant_rate,
    admission_rate_overall, completion_rate_suppressed,
    retention_rate_full_time, federal_loan_rate,
    student_demographics_men, student_demographics_women,
    faculty_demographics_men, faculty_demographics_women
from {{ ref('stg_school_data') }}