"""Full ETL pipeline"""

from os import environ

import csv
import pandas as pd
import extract
import transform
import load


def convert_transactions(transaction_file: csv) -> list[tuple]:
    """Turns csv data into a list of tuples."""
    # data = pd.read_csv(transaction_file)
    # transaction_list = data.to_records().tolist()

    data = pd.read_csv(transaction_file, header=None)
    transaction_list = [tuple(row) for row in data.values]
    return transaction_list[1:]


if __name__ == "__main__":
    # EXTRACT
    s3 = extract.get_s3_client()
    extract.download_latest_batch_data_files(
        s3, environ["BUCKET"], "latest_batch_data")

    # TRANSFORM
    transform.format_truck_data_files("latest_batch_data")
    transactions = convert_transactions(
        "./latest_batch_data/combined_latest_batch_data.csv")

    # LOAD
    load.upload_transaction_data(transactions)
    # load.upload_transaction_data(transactions[:50]) # upload a sample of the data
