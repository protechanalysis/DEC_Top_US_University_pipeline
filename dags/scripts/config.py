from airflow.models import Variable

unirank_url = "https://www.4icu.org/us/"
scorecard_url = "https://api.data.gov/ed/collegescorecard/v1/schools"

api_key = Variable.get("api_key")
access_key = Variable.get("access_key")
secret_key = Variable.get("secret_key")

output_unirank = "/tmp/uniranking_universities.csv"
output_score_card = "/tmp/schools.json"

snowflake_table = "school_data"
s3_bucket = "top-university-bucket"
parquet_path = "transform/cleaned/"

fields = ",".join([
    "id", "latest.school.name", "latest.school.address", "latest.school.city",
    "latest.school.state", "latest.school.state_fips",
    "latest.school.region_id", "latest.school.locale",
    "latest.school.school_url", "latest.school.ownership",
    "latest.school.accreditor", "latest.school.price_calculator_url",
    "latest.school.online_only", "latest.school.main_campus",
    "latest.school.institutional_characteristics.level",
    "latest.school.open_admissions_policy", "latest.aid.pell_grant_rate",
    "latest.school.degrees_awarded.highest",
    "latest.school.degrees_awarded.predominant", "latest.cost.booksupply",
    "latest.admissions.test_requirements",
    "latest.admissions.sat_scores.average.overall",
    "latest.school.carnegie_basic",
    "latest.admissions.act_scores.50th_percentile.cumulative",
    "latest.admissions.admission_rate.overall",
    "latest.completion.rate_suppressed.overall",
    "latest.student.retention_rate.overall.full_time",
    "latest.aid.federal_loan_rate", "latest.cost.attendance.academic_year",
    "latest.cost.avg_net_price.overall", "latest.cost.tuition.in_state",
    "latest.cost.tuition.out_of_state", "latest.cost.roomboard.offcampus",
    "latest.cost.roomboard.oncampus", "latest.cost.otherexpense.oncampus",
    "latest.cost.otherexpense.offcampus", "latest.student.size",
    "latest.student.demographics.men", "latest.student.demographics.women",
    "latest.student.demographics.faculty.men",
    "latest.student.demographics.faculty.women",
    "latest.student.enrollment.grad_12_month",
    "latest.student.enrollment.undergrad_12_month"
]
)

params = {
    "api_key": api_key,
    "per_page": 95,
    "page": 0,
    "fields": fields,
}

column_mapping = {
    "id": "id",
    "latest.school.name": "school_name",
    "latest.school.address": "address",
    "latest.school.city": "city",
    "latest.school.state": "state_code",
    "latest.school.state_fips": "state_fips",
    "latest.school.region_id": "region_id",
    "latest.school.locale": "school_locale",
    "latest.school.school_url": "school_url",
    "latest.school.ownership": "school_ownership",
    "latest.school.accreditor": "school_accreditor",
    "latest.school.price_calculator_url": "price_calculator_url",
    "latest.school.online_only": "online_only",
    "latest.school.main_campus": "main_campus",
    "latest.school.institutional_characteristics.level":
    "institutional_characteristics_level",
    "latest.school.open_admissions_policy": "open_admissions_policy",
    "latest.school.degrees_awarded.highest": "degrees_awarded_highest",
    "latest.school.degrees_awarded.predominant": "degrees_awarded_predominant",
    "latest.cost.booksupply": "booksupply_cost",
    "latest.admissions.test_requirements": "test_requirements",
    "latest.aid.pell_grant_rate": "pell_grant_rate",
    "latest.admissions.sat_scores.average.overall":
    "sat_scores_overall_average",
    "latest.school.carnegie_basic": "carnegie_basic",
    "latest.admissions.act_scores.50th_percentile.cumulative":
    "act_scores_50th_percentile",
    "latest.admissions.admission_rate.overall": "admission_rate_overall",
    "latest.completion.rate_suppressed.overall": "completion_rate_suppressed",
    "latest.student.retention_rate.overall.full_time":
    "retention_rate_full_time",
    "latest.aid.federal_loan_rate": "federal_loan_rate",
    "latest.cost.attendance.academic_year": "cost_of_attendance",
    "latest.cost.avg_net_price.overall": "avg_net_price_overall",
    "latest.cost.tuition.in_state": "tuition_in_state",
    "latest.cost.tuition.out_of_state": "tuition_out_of_state",
    "latest.cost.roomboard.offcampus": "roomboard_offcampus",
    "latest.cost.roomboard.oncampus": "roomboard_oncampus",
    "latest.cost.otherexpense.oncampus": "otherexpense_oncampus",
    "latest.cost.otherexpense.offcampus": "otherexpense_offcampus",
    "latest.student.size": "student_size",
    "latest.student.demographics.men": "student_demographics_men",
    "latest.student.demographics.women": "student_demographics_women",
    "latest.student.demographics.faculty.men": "faculty_demographics_men",
    "latest.student.demographics.faculty.women": "faculty_demographics_women",
    "latest.student.enrollment.grad_12_month": "grad_enrollment_12_month",
    "latest.student.enrollment.undergrad_12_month":
    "undergrad_enrollment_12_month"
}
