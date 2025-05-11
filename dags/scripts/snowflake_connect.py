import logging

from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook

from scripts.config import (access_key, parquet_path, s3_bucket, secret_key,
                            snowflake_table)

logging.basicConfig(format="%(asctime)s %(message)s")


def create_snowflake_table():
    """
    Executes a SQL script to create a table in Snowflake.

    This function reads an SQL file containing the create table statement
    and executes it using the SnowflakeHook to interact with Snowflake.

    Raises:
        Exception: If there is an error while reading the SQL file or
        executing the SQL command.
    """
    try:
        hook = SnowflakeHook(snowflake_conn_id="snow_flake")
        sql_file_path = "/usr/local/airflow/include/snowflake/create_table.sql"
        with open(sql_file_path, "r") as f:
            create_table_sql = f.read()

        hook.run(create_table_sql)
    except Exception as e:
        logging.info(f"error {e}")


def create_snowflake_stage():
    """
    Creates or replaces a Snowflake stage that points to an S3 bucket.

    This function constructs and executes a SQL query to create or replace a
    stage in Snowflake
    that links to a specified S3 bucket using provided AWS credentials.
    The stage will be configured to use the Parquet file format.

    Args:
        s3_bucket (str): The name of the S3 bucket.
        access_key (str): The AWS access key ID.
        secret_key (str): The AWS secret access key.

    Raises:
        Exception: If there is an error while executing the SQL query or
        setting up the stage.
    """
    hook = SnowflakeHook(snowflake_conn_id="snow_flake")
    try:

        sql_query = f"""
        CREATE OR REPLACE STAGE my_snowflake_stage
        URL = 's3://{s3_bucket}/'
        CREDENTIALS = (AWS_KEY_ID = '{access_key}',
                    AWS_SECRET_KEY = '{secret_key}')
        FILE_FORMAT = (TYPE = PARQUET);
        """
        hook.run(sql_query)
    except Exception as e:
        logging.info(f"error {e}")


def get_row_count(hook, table_name):
    """
    Helper function to get the row count from a Snowflake table.

    This function executes a SQL query to count the number of rows in a given
    Snowflake table and returns the result. If the query fails or the table
    has no rows, it returns 0.

    Args:
        hook (SnowflakeHook): The Snowflake connection hook used to execute
            the query.
        table_name (str): The name of the Snowflake table for which the row
            count is to be retrieved.

    Returns:
        int: The number of rows in the specified table. Returns 0 if no rows
            are found or an error occurs.

    Raises:
        Exception: If there is an issue with executing the query or retrieving
        the result.
    """
    sql_count = f"SELECT COUNT(*) FROM {table_name};"
    result = hook.get_first(sql_count)
    return result[0] if result else 0


def load_parquet_to_snowflake():
    """
    Loads a Parquet file from a Snowflake stage into a Snowflake table.

    This function constructs and executes a COPY INTO SQL command to load data
    from a Parquet file stored in a Snowflake stage into a specified Snowflake
    table.
    The file format is set to Parquet, and the matching of columns is
    case-insensitive.

    Args:
        parquet_path (str): The path to the Parquet file in the Snowflake
        stage.
        snowflake_table (str): The name of the Snowflake table into which the
        data will be loaded.

    Raises:
        Exception: If an error occurs during the loading process or while
        executing the SQL query.
    """
    try:
        hook = SnowflakeHook(snowflake_conn_id="snow_flake")

        initial_row_count = get_row_count(hook, snowflake_table)

        sql_copy_into = f"""
        COPY INTO {snowflake_table}
        FROM @my_snowflake_stage/{parquet_path}
        FILE_FORMAT = (TYPE = PARQUET)
        MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
        ON_ERROR = 'ABORT_STATEMENT';
        """

        hook.run(sql_copy_into)
        # Check row count after loading data
        final_row_count = get_row_count(hook, snowflake_table)

        if final_row_count > initial_row_count:
            logging.info(f"Successfully loaded {parquet_path} into \
                         {snowflake_table}. Rows added: \
                            {final_row_count - initial_row_count}")
        else:
            logging.warning(f"No new data was added to {snowflake_table}."
                            "Row count before and after loading:"
                            "{initial_row_count}.")

    except Exception as e:
        logging.error(f"Failed to load Parquet to Snowflake:{e}",
                      exc_info=True)
