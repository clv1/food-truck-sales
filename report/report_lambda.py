# pylint: disable = invalid-name, redefined-outer-name, unnecessary-pass, unused-argument
"""
A script that retrieves the previous day's transaction data from the database 
and summarises useful information into a report for T3 stakeholders.
"""

from os import environ
from datetime import datetime, timedelta

import pandas as pd
from redshift_connector import connect
from redshift_connector.core import Connection
from dotenv import load_dotenv


PREVIOUS_DAY = datetime.now() - timedelta(days=1)
PREVIOUS_DAY_STR = PREVIOUS_DAY.strftime('%Y-%m-%d')


def get_db_connection() -> Connection:
    """Returns a database connection."""
    load_dotenv()

    connection = connect(
        host=environ["DB_HOST"],
        port=environ["DB_PORT"],
        database=environ["DB_NAME"],
        user=environ["DB_USERNAME"],
        password=environ["DB_PASSWORD"]
    )
    return connection


def extract_previous_day_data():
    """Extracts the previous day's data as a pandas dataframe."""

    query = f"""
    SELECT 
        transactions.truck_id, 
        transactions.timestamp,
        transactions.total,
        trucks.name
    FROM kevin_schema.fact_transactions AS transactions
    JOIN kevin_schema.dim_trucks AS trucks
        ON transactions.truck_id = trucks.truck_id
    WHERE DATE_TRUNC('day', transactions.timestamp) = '{PREVIOUS_DAY_STR}'
    ;
    """

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(query)
        result: pd.DataFrame = cur.fetch_dataframe()
    # print(result[:10])  # prints sample of data
    return result


def fleet_revenue(df: pd.DataFrame):
    """Returns the total revenue for the entire fleet."""
    total_revenue = df['total'].sum()
    return pd.DataFrame({'Total Fleet Revenue': [total_revenue]})


def truck_revenue(df: pd.DataFrame):
    """Returns the total revenue for each truck."""

    # Group by truck_id, name and sum the total column
    truck_revenue = df.groupby(['truck_id', 'name'], as_index=False)[
        'total'].sum()
    truck_revenue.columns = ['Truck ID', 'Truck Name', 'Total Revenue (£)']

    return truck_revenue


def truck_transaction_count(df: pd.DataFrame):
    """Returns the total revenue for each truck."""

    # Group by truck_id, name and sum the total column
    truck_revenue = df.groupby(['truck_id', 'name'], as_index=False).size()
    truck_revenue.columns = ['Truck ID',
                             'Truck Name', 'Number of Transactions']

    return truck_revenue


def truck_avg_transaction_value(df: pd.DataFrame):
    """pass"""
    pass


# --- OPTIONAL EXTRAS to add
# most revenue truck
# most popular truck
# least popular truck


def generate_summary_JSON(data: pd.DataFrame):
    """Produces summary JSON."""

    # Your script should store this data in
    # an appropriately-formatted JSON file entitled report_data_[date].json.
    pass


def make_fleet_revenue_table():
    """pass"""
    pass


def make_truck_revenue_table():
    """pass"""
    pass


def make_truck_transaction_count_table():
    """pass"""
    pass


def generate_html_string(df: pd.DataFrame):
    """pass"""

    html_string = df.to_html(index=False)
    return html_string


def generate_summary_html(df_list: list[pd.DataFrame]) -> str:
    """pass"""
    summary_html = ""

    for df in df_list:
        new_html_string = generate_html_string(df)
        summary_html += '\n\n'
        summary_html += new_html_string

    return summary_html


def write_html_to_file(html_string: str) -> None:
    """Generates a report file from a html string."""
    with open(f"report_data_{PREVIOUS_DAY_STR}", "w", encoding="utf-8") as file:
        file.write(html_string)


def handler(event=None, context=None) -> dict:
    """pass"""
    data = extract_previous_day_data()
    dataframes = [fleet_revenue(data), truck_revenue(
        data), truck_transaction_count(data)]
    summary = generate_summary_html(dataframes)
    return {'summary': f"{summary}"}


if __name__ == "__main__":
    print(handler(event=None, context=None))
