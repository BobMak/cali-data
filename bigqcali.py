import os.path
import pickle

import pandas as pd
from google.cloud.bigquery import Client
from google.oauth2.service_account import Credentials

KEY_PATH = os.path.join(os.path.dirname(__file__), "cali-data-f58cbdd11671.json")


def query_cbsa(year, cache=True):
    # fname = f"results{year}.pkl"
    # if os.path.exists(fname) and cache:
    #     with open(fname, "rb") as f:
    #         res = pickle.load(f)
    #     return res
    creds = Credentials.from_service_account_file(KEY_PATH)
    client = Client(credentials=creds, project=creds.project_id)
    query_job = client.query(f"""
        --require_cache
        SELECT *
        FROM `bigquery-public-data.census_bureau_acs.censustract_2015_5yr`
        LIMIT 10
    """)
    results = query_job.result()  # Waits for job to complete.
    _results = []
    for row in results:
        _results.append(row)
        print(row)
    # if cache:
    #     with open(fname, "wb") as f:
    #         pickle.dump(_results, f)
    return _results


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
    query_columns(2015)
    # query_cbsa(2015)
