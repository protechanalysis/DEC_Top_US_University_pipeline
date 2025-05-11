import json
import logging

import awswrangler as wr
import pandas as pd

from scripts.config import output_score_card, output_unirank
from scripts.session import aws_session

logging.basicConfig(format="%(asctime)s %(message)s")


def raw_scorecard_to_s3():
    """
    Fetches scorecard data from a local JSON file, processes it into a
    DataFrame, and writes the data to an S3 bucket in JSON format.

    The data is saved in overwrite mode under the path
    "s3://top-university-bucket/raw/". The function uses a boto3 session
    established through `aws_session()`.

    Raises:
        ValueError: If the loaded DataFrame is empty or None.
        Exception: If any error occurs during reading or writing operations.
    """
    try:
        with open(output_score_card, "r", encoding='utf-8') as f:
            score_card_data = pd.DataFrame(json.load(f))
        if score_card_data is None or score_card_data.empty:
            raise ValueError("No data available to write to S3.")
        wr.s3.to_json(
            df=score_card_data,
            path="s3://top-university-bucket/raw/scorecard/",
            boto3_session=aws_session(),
            mode="overwrite",
            dataset=True,
            orient="records",
            index=False,
            )
        logging.info("Data successfully written to S3 in Parquet format.")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")


def unirank_to_s3():
    """
    Fetches university ranking data from a local CSV file, processes it into a
    DataFrame, and writes the data to an S3 bucket in Parquet format.

    The data is saved in overwrite mode under the path
    "s3://top-university-bucket/raw/". The function uses a boto3 session
    established through `aws_session()`.

    Raises:
        ValueError: If the loaded DataFrame is empty or None.
        Exception: If any error occurs during reading or writing operations.
    """
    try:
        with open(output_unirank, "r") as f:
            uni_rank_data = pd.read_csv(f)
        if uni_rank_data is None or uni_rank_data.empty:
            raise ValueError("No data available to write to S3.")
        wr.s3.to_parquet(
            df=uni_rank_data,
            path="s3://top-university-bucket/raw/unirank/",
            boto3_session=aws_session(),
            mode="overwrite",
            dataset=True,
        )
        logging.info("Data successfully written to S3 in Parquet format.")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")


# def transform_to_s3():
#     """
#     Fetches transformed university ranking data from a tmp CSV file,
#     processes it into a DataFrame, and writes the data to an S3 bucket in
#     Parquet format.

#     The data is saved in overwrite mode under the path
#     "s3://top-university-bucket/transform/cleaned/". The function uses a boto3
#     session established through `aws_session()`.

#     Raises:
#         ValueError: If the loaded DataFrame is empty or None.
#         Exception: If any error occurs during reading or writing operations.
#     """
#     try:
#         with open(output_transform, "r") as f:
#             cleaned_uni = pd.read_csv(f)
#         if cleaned_uni is None or cleaned_uni.empty:
#             raise ValueError("No data available to write to S3.")
#         wr.s3.to_parquet(
#             df=cleaned_uni,
#             path="s3://top-university-bucket/transform/cleaned/",
#             boto3_session=aws_session(),
#             mode="overwrite",
#             dataset=True,
#         )
#         logging.info("Data successfully written to S3 in Parquet format.")
#     except Exception as e:
#         raise Exception(f"An error occurred: {e}")
