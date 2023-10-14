import os.path
import pickle

import pandas as pd
from google.cloud.bigquery import Client
from google.oauth2.service_account import Credentials

KEY_PATH = os.path.join(os.path.dirname(__file__), "cali-data-f58cbdd11671.json")


def query_cali_censustract(year, cache=True, state='06', verbose=False):
    fname = f"results{year}.csv"
    if os.path.exists(fname) and cache:
        df = pd.read_csv(fname)
        return df
    creds = Credentials.from_service_account_file(KEY_PATH)
    client = Client(credentials=creds, project=creds.project_id)
    query_job = client.query(f"""
        --require_cache
        SELECT *
        FROM `bigquery-public-data.census_bureau_acs.censustract_{year}_5yr`
        WHERE geo_id LIKE '{state}%%'
    """)
    results = query_job.result()  # Waits for job to complete.
    df = results.to_dataframe()
    if verbose:
        print(df.head())
    if cache:
        df.to_csv(fname)
    return df


def query_columns(year, cache=True):
    fname = f"columns{year}.csv"
    if os.path.exists(fname) and cache:
        df = pd.read_csv(fname)
        return df
    creds = Credentials.from_service_account_file(KEY_PATH)
    client = Client(credentials=creds, project=creds.project_id)
    query_job = client.query(f"""
        --require_cache
        SELECT column_name
        FROM `bigquery-public-data.census_bureau_acs.INFORMATION_SCHEMA.COLUMNS`
        WHERE table_name = 'censustract_{year}_5yr'
    """)
    results = query_job.result()  # Waits for job to complete.
    df = results.to_dataframe()
    if cache:
        df.to_csv(fname)
    return df


if __name__ == "__main__":
    # df = query_columns(2015)
    df = query_cali_censustract(2015, verbose=True)
    print(df.head())
