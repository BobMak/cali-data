# ACL Data Exploration Tool

This is a streamlit webapp that allows you to visualize and explore California
map and statistics data from the [Census Bereau's American Community Survey (ACS) dataset](https://console.cloud.google.com/bigquery?p=bigquery-public-data&d=census_bureau_acs&page=dataset&project=cali-data&ws=!1m9!1m3!3m2!1sbigquery-public-data!2scensus_bureau_acs!1m4!1m3!1scali-data!2sbquxjob_276b12f2_18b2cbcb8f3!3sUS).

## Getting Started

1. Setup the conda environment: `conda env create -f env.yaml`
2. Activate the conda environment: `conda activate cali-data`
2. Run Streamlit: `streamlit run main.py`

## Features

 - Interactive Map. Select the year and variable to display on the map.
 - Correlation Matrix. You can visualize the correlation matrix between all or a subset of variables.
 - Range variable vs variable bar chart. Some variables in the dataset are grouped into ranges.
    This allows to visualize the distribution of a variable over a range of another variable.