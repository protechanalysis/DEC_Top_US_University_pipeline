import logging

import awswrangler as wr
import pandas as pd
from rapidfuzz import fuzz, process

from scripts.columns import columns_to_int, columns_with_nulls
from scripts.config import column_mapping
from scripts.session import aws_session

logging.basicConfig(format="%(asctime)s %(message)s")


def scorecard_from_s3():
    """
    Reads and processes JSON data from an S3 bucket using AWS Wrangler.

    This function reads a JSON dataset from the specified S3 bucket path using
    a boto3 session, normalizes the nested JSON structure, and renames the
    columns based on a predefined mapping.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the normalized and renamed
        data.

    Raises:
        Exception: If reading or processing the data fails.
    """
    try:
        df = wr.s3.read_json(
            path="s3://top-university-bucket/raw/scorecard/",
            boto3_session=aws_session(),
            dataset=True
        )

        normalized_data = pd.json_normalize(df.iloc[0])
        data = normalized_data.rename(columns=column_mapping)

        logging.info("Successfully read and processed Scorecard data from S3.")
        return data

    except Exception as e:
        raise Exception(f"Failed to read Scorecard data from S3: {e}")


def rank_from_s3():
    """
    Reads university ranking data from an S3 bucket in Parquet format using
    AWS Wrangler.

    This function retrieves a dataset stored in Parquet format from the
    specified S3 bucket path and returns it as a pandas DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the university ranking data.

    Raises:
        Exception: If reading the data from S3 fails.
    """
    try:
        df = wr.s3.read_parquet(
            path="s3://top-university-bucket/raw/unirank/",
            boto3_session=aws_session(),
            dataset=True
        )
        logging.info("Successfully read university ranking data from S3.")
        return df

    except Exception as e:
        raise Exception(f"Failed to read university ranking data from S3: {e}")


def transform_data(score_threshold=95):
    """
    Match universities from the College Scorecard API with Unirank data using
    fuzzy matching and save the transformed results to S3.

    This function performs fuzzy string matching between university names from
    the College Scorecard dataset and the Unirank top 1000 universities list.
    Universities with a similarity score above the specified threshold are
    considered matches. The matched data is enriched with additional Scorecard
    fields, cleaned, and then saved as a Parquet file to an S3 bucket for
    further use.

    Args:
        score_threshold (int, optional): Minimum similarity score (0–100)
        required to consider a university name a match. Defaults to 95.

    Saves:
        A cleaned and matched dataset is saved to:
        's3://top-university-bucket/transform/cleaned/' in Parquet format.

    Raises:
        Exception: If there is any failure in loading, matching, transforming,
        or saving the data.
    """
    try:
        # Load data
        df_score = scorecard_from_s3()
        uni = rank_from_s3()

        df_subset = df_score[['school_name', 'id']].dropna(
            subset=['school_name'])
        unirank_subset = uni[['University', 'Rank']].dropna(
            subset=['University'])

        unirank_names = unirank_subset['University'].tolist()
        matched_results = []

        for _, row in df_subset.iterrows():
            school_name = row['school_name']
            scorecard_id = row['id']

            match, score, match_index = process.extractOne(
                school_name, unirank_names, scorer=fuzz.WRatio, score_cutoff=0
            )

            if score > score_threshold:
                unirank_row = unirank_subset.iloc[match_index]
                matched_results.append([
                    school_name, match, score,
                    unirank_row['Rank'],
                    scorecard_id
                ])
            else:
                None

        # Create matched_df DataFrame
        columns = [
            'scorecard_school_name',
            'unirank_university',
            'score',
            'rank',
            'id'
        ]
        matched_df = pd.DataFrame(matched_results, columns=columns)

        matched_df = matched_df.sort_values(by='score', ascending=False)
        select_column = matched_df[['rank', 'id']]
        final = pd.merge(select_column, df_score, left_on='id',
                         right_on='id', how='inner')
        final[columns_with_nulls] = final[columns_with_nulls].fillna(0)
        final['carnegie_basic'] = final['carnegie_basic'].fillna(-3)
        final[['online_only', 'open_admissions_policy']] = final[[
            'online_only', 'open_admissions_policy']].fillna(-1)
        final[['address', 'price_calculator_url', 'school_accreditor'
               ]] = final[['address', 'price_calculator_url',
                           'school_accreditor']].fillna('Not Specified')
        final[columns_to_int] = final[columns_to_int].astype(int)
        final['main_campus'] = final['main_campus'].astype(bool)
        logging.info("University matching and transformation completed "
                     "successfully.")
        wr.s3.to_parquet(
            df=final,
            path="s3://top-university-bucket/transform/cleaned/",
            boto3_session=aws_session(),
            mode="overwrite",
            dataset=True,
        )
        logging.info("transformed loaded to s3 successfully.")
    except Exception as e:
        raise Exception(f"Matching failed: {e}")
