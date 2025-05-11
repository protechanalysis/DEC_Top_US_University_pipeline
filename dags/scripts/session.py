import boto3

from scripts.config import access_key, secret_key


def aws_session():
    """
    setting up aws boto3 session credentials
    """
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="us-east-1",
    )
    return session
