"""Database functions"""
# pylint: disable=import-error, unused-import

import logging
from os import environ
import streamlit as st
import pandas as pd


from redshift_connector import connect
from redshift_connector.core import Connection
from dotenv import load_dotenv


def get_db_connection() -> Connection:
    """Returns a database connection."""
    try:
        connection = connect(
            host=environ["DB_HOST"],
            port=environ["DB_PORT"],
            database=environ["DB_NAME"],
            user=environ["DB_USERNAME"],
            password=environ["DB_PASSWORD"]
        )
        logging.info("Database connection successful.\n")
        return connection
    except OSError:
        logging.error("Error: Unable to connect to the database.")
        return None


def load_transaction_data(conn: Connection) -> pd.DataFrame:
    """Returns a dataframe containing the transaction data."""
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM kevin_schema.FACT_transactions;")
        return cur.fetch_dataframe()
