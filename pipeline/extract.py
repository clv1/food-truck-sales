"""Extract script:"""

import os
import shutil
from datetime import datetime
from os import environ, path
from boto3 import client
from dotenv import load_dotenv


BATCH_HOUR_SPLIT = 3


def get_s3_client() -> client:
    """Connects to the s3 by authenticating a boto3 client."""
    load_dotenv()

    s3_client = client("s3",
                       aws_access_key_id=environ["AWS_ACCESS_KEY_ID"],
                       aws_secret_access_key=environ["AWS_SECRET_ACCESS_KEY"])

    return s3_client


def get_bucket_names(s3_client: client) -> list[str]:
    """Returns a list of bucket names in the account."""
    buckets = s3_client.list_buckets()["Buckets"]
    return [b["Name"] for b in buckets]


def get_bucket_keys(s3_client: client, bucket: str) -> list[str]:
    """Returns the contents of a specific bucket as its keys."""
    contents = s3_client.list_objects(Bucket=bucket)["Contents"]
    return [s3_object["Key"] for s3_object in contents]


def download_all_files(s3_client: client, bucket: str, folder_name: str):
    """Downloads all files from S3 to a data/ folder."""
    keys = get_bucket_keys(s3_client, bucket)

    if path.exists(folder_name):
        shutil.rmtree(folder_name)

    os.mkdir(folder_name)

    for key in keys:
        key_name = os.path.basename(key)
        s3_client.download_file(bucket, key, f"{folder_name}/{key_name}")

    print("Files successfully downloaded:")
    print(f"{get_bucket_keys(s3_client, bucket)}" + "\n")


def download_all_batch_data_files(s3_client: client, bucket: str, folder_name: str):
    """Downloads relevant files from S3 to a data/ folder."""
    keys = get_bucket_keys(s3_client, bucket)

    if path.exists(folder_name):
        shutil.rmtree(folder_name)

    os.mkdir(folder_name)

    truck_downloads = []
    other_downloads = []

    for key in keys:
        key_name = os.path.basename(key)
        local_filepath = f"{folder_name}/{key_name}"

        if "trucks/" in key and ".csv" in key:
            s3_client.download_file(bucket, key, local_filepath)
            truck_downloads.append(local_filepath)

        elif "metadata/" in key:
            s3_client.download_file(bucket, key, local_filepath)
            other_downloads.append(local_filepath)

        else:
            continue

    print("Batch data files successfully downloaded:")
    print(truck_downloads)
    print("Other files downloaded:")
    print(other_downloads)


def extract_batch_key_datetime(file: str) -> datetime:
    """
    Extracts date information from S3 object file.
    Returns it as a datetime object.
    """
    date_part = file.split('trucks/')[1].split(f'/{os.path.basename(file)}')[0]
    return datetime.strptime(date_part, '%Y-%m/%d/%H')


def download_latest_batch_data_files(s3_client: client, bucket: str, folder_name: str):
    """Downloads files from latest batch on S3 to a batch_data folder."""
    keys = get_bucket_keys(s3_client, bucket)

    if path.exists(folder_name):
        shutil.rmtree(folder_name)

    os.mkdir(folder_name)

    truck_downloads = []

    for key in keys:
        key_name = os.path.basename(key)
        local_filepath = f"{folder_name}/{key_name}"

        if "trucks/" in key:
            key_datetime = extract_batch_key_datetime(key)

            if key_datetime.hour >= datetime.now().hour - BATCH_HOUR_SPLIT:
                s3_client.download_file(bucket, key, local_filepath)
                truck_downloads.append(local_filepath)

    print(
        f"Latest {BATCH_HOUR_SPLIT}-hour batch of truck data successfully downloaded:")
    print(truck_downloads, '\n')


if __name__ == "__main__":
    s3 = get_s3_client()

    # --- Explore the S3 contents:
    # print(get_bucket_names(s3))
    # print(get_bucket_keys(s3, environ['BUCKET']))

    # --- Download preferred files:
    # download_all_files(s3, environ['BUCKET'], 'data')
    # download_all_batch_data_files(s3, environ['BUCKET'], 'batch_data')
    download_latest_batch_data_files(
        s3, environ['BUCKET'], 'latest_batch_data')
