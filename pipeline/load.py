"""Uploads transaction data to a Redshift database."""

import logging

from os import environ
from redshift_connector import connect
from redshift_connector.core import Connection
from dotenv import load_dotenv


def get_db_connection() -> Connection:
    """Returns a database connection."""
    load_dotenv()
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


def upload_transaction_data(transactions: list) -> None:
    """Uploads transaction data to the database."""

    query = """
    INSERT INTO kevin_schema.FACT_transactions 
        (truck_id, timestamp, payment_type_id, total)
    VALUES 
        (%s, %s, %s, %s);
    """

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.executemany(query, transactions)
        cur.execute("SELECT * FROM kevin_schema.FACT_transactions LIMIT 10;")
        uploads = cur.fetchall()
        conn.commit()

    print(f"Transactions uploaded successfully: \n {uploads}")


# if __name__ == "__main__":
#     load_dotenv()

#     sample_transactions = [
#         (2, '2023-11-21 13:45:00', 2, 20.50),
#         (3, '2023-11-22 09:15:00', 1, 10.75),
#         (1, '2023-11-22 14:30:00', 3, 25.00),
#         (4, '2023-11-23 11:00:00', 1, 18.99),
#         (5, '2023-11-23 17:45:00', 2, 12.25)
#     ]
#     upload_transaction_data(sample_transactions)
