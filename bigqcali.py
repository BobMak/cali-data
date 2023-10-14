import os.path
import streamlit as st

import pandas as pd
from google.cloud.bigquery import Client
from google.oauth2.service_account import Credentials

KEY_PATH = os.path.join(os.path.dirname(__file__), "cali-data-f58cbdd11671.json")

@st.cache_data
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

@st.cache_data
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

@st.cache_data
def get_range_columns(df):
    """
    parses columns df to get the ordinal or discrete column groups, such as age, income, etc.
    If the variable is ordinal, sorts the columns by the sum of all numbers in the column name
    :param df: columns data frame
    :return: {str: variable_name : list: [str: column_name_0, ...] }
    """
    unique_names = set()
    ranges = {}
    for i, row in df.iterrows():
        column_name = row['column_name'].split("_")
        if column_name[0] not in unique_names:
            unique_names.add(column_name[0])
            # consider the variable to be ordinal if it contains numbers
            ordinal = any([c.isnumeric() for c in column_name[1:]])
            ranges[column_name[0]] = (ordinal, [row['column_name']])
        else:
            ranges[column_name[0]][1].append(row['column_name'])
    out_vars = {}
    for k, v in ranges.items():
        if len(v[1]) == 1:
            # not a range variable
            continue
        if v[0]:
            # parse all numbers
            v[1].sort(key=lambda x: sum([int(c) for c in x.split("_")[1:] if c.isnumeric()]))
        out_vars[k] = v[1]
    return out_vars


if __name__ == "__main__":
    df = query_columns(2015)
    print(get_range_columns(df))
