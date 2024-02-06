# pylint: disable=invalid-name
"""Transforms data into a single, cleaned csv file."""

import os
import pandas as pd

TRUCK_DATA_COLUMNS = ['truck_id', 'time_stamp', 'payment_type_id', 'total']
METADATA_COLUMNS = ['ID', 'NAME', 'DESCRIPTION',
                    'HAS_CARD_READER', 'FSA_RATING_22']
INVALID_TOTALS = [0, 0.0, '0', '0.00', '', 'nan',
                  'none', 'null', 'void', 'blank', 'err']
VALID_TYPES = ['card', 'cash', 'crypto']
TYPE_IDS = {type_id: i+1 for i, type_id in enumerate(VALID_TYPES)}
VALID_PURCHASE_RANGE = (0, 200)


def format_truck_data_files(folder_name: str):
    """Loads and combines relevant files from the data/ folder.
    Produces a single combined file in the data/ folder."""

    all_files = [file for file in os.listdir(folder_name) if ".csv" in file]
    combined_data = pd.DataFrame()

    # use pandas to read csv files and add to a combined dataframe
    for file in all_files:
        csv_data = pd.read_csv(f"{folder_name}/{file}")

        # insert truck_id
        truck_id = file.split("T3_T")[
            1].split("_")[0]
        csv_data.insert(0, 'truck_id', truck_id)

        combined_data = pd.concat([combined_data, csv_data])
        cleaned_data = clean_truck_data(combined_data)
        os.remove(f"{folder_name}/{file}")

    # use pandas to turn dataframe into a csv
    csv_truck_data = cleaned_data.to_csv(
        f"{folder_name}/combined_{folder_name}.csv",  index=False)  # header=False
    print("Batch truck data files successfully cleaned, formatted and combined.\n")
    return csv_truck_data


def clean_truck_data(df: pd.DataFrame) -> pd.DataFrame:
    """Cleaning data in dataframe."""

    # Validate rows
    df = df[df['type'].isin(VALID_TYPES)]
    df['type'] = df['type'].map(TYPE_IDS)
    df = df[~df['total'].astype(str).str.lower().isin(INVALID_TOTALS)]

    # Converting columns to the most appropriate data type or format
    df['time_stamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize(None)
    df.rename(columns={'type': 'payment_type_id'}, inplace=True)
    df['total'] = pd.to_numeric(df['total'])  # gives NaN if not possible

    # Discarding invalid rows
    df = df.dropna()
    # Removing any columns that are no longer needed
    df = df[TRUCK_DATA_COLUMNS]

    # Discarding rows with unexpected/invalid totals
    df = df[df['total'].between(*VALID_PURCHASE_RANGE)]

    return df


if __name__ == "__main__":

    format_truck_data_files("latest_batch_data")
    # format_metadata_files("data")
    # test_df = pd.read_csv("historical_truck_data/combined_historical_truck_data.csv")
