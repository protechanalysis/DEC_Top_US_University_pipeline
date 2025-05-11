import os
from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from cosmos import DbtTaskGroup, ExecutionConfig, ProfileConfig, ProjectConfig
from cosmos.profiles import SnowflakeUserPasswordProfileMapping
from scripts.extraction import fetch_page, scrape_universities
from scripts.snowflake_connect import (create_snowflake_stage,
                                       create_snowflake_table,
                                       load_parquet_to_snowflake)
from scripts.load_to_s3 import raw_scorecard_to_s3, unirank_to_s3
from scripts.transform import transform_data

dbt_project_path = Path("/usr/local/airflow/dags/dbt_job/uni_rank/")

profile_config = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profile_mapping=SnowflakeUserPasswordProfileMapping(
        conn_id="snow_flake",
        profile_args={
            "database": "scorecard",
            "schema": "uni_ranking"
        },
    )
)

default_args = {
    "owner": "adewunmi",
}


with DAG(
    dag_id="dbt_snowflake",
    start_date=datetime(2025, 3, 25),
    # schedule_interval="@daily",
    default_args=default_args,
) as dag:

    dbt_snowflake_dag = DbtTaskGroup(
        group_id="dbt_flake",
        project_config=ProjectConfig(dbt_project_path,),
        operator_args={"install_deps": True},
        profile_config=profile_config,
        execution_config=ExecutionConfig(
            dbt_executable_path=(
                f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt"
            ),
            commands=["dbt seed", "dbt run"],
        )
    )

    top_university = PythonOperator(
        task_id='university_ranking',
        python_callable=scrape_universities,
    )

    scorecard_extract = PythonOperator(
        task_id='scorecard_api_extraction',
        python_callable=fetch_page,
    )

    load_raw_scorecard = PythonOperator(
        task_id='raw_scorecard_data',
        python_callable=raw_scorecard_to_s3,
    )

    load_unirank = PythonOperator(
        task_id='rank_uni',
        python_callable=unirank_to_s3,
    )

    transformation = PythonOperator(
        task_id='data_transformation',
        python_callable=transform_data,
    )

    snowflake_table = PythonOperator(
        task_id='snowflake_table_creation',
        python_callable=create_snowflake_table,
    )

    create_stage = PythonOperator(
        task_id='create_stage',
        python_callable=create_snowflake_stage,
    )

    data_to_snowflake = PythonOperator(
        task_id='load_data_to_snowflake',
        python_callable=load_parquet_to_snowflake,
    )

    top_university >> load_unirank
    scorecard_extract >> load_raw_scorecard
    [load_raw_scorecard, load_unirank] >> transformation
    transformation >> [snowflake_table, create_stage]
    [snowflake_table, create_stage] >> data_to_snowflake >> dbt_snowflake_dag
