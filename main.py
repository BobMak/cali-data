"""
A ACS public US census data set exploration dashboard
"""
import streamlit as st
import pandas as pd
import numpy as np
from califolium import get_map
from bigqcali import query_columns, query_cbsa


# Title
st.title("US Census Data Exploration")

# Subtitle
st.markdown("A CDE public dataset exploration dashboard")

# Sidebar
st.sidebar.title("User Input Features")
st.sidebar.markdown("Select the features you want to explore")
year = st.sidebar.slider("Year", 2010, 2015, 2011)
# available columns
if "columns" not in st.session_state:
    st.session_state.columns = query_columns(year, cache=True)
_columns = st.session_state.columns
if "data" not in st.session_state:
    st.session_state.data = query_cbsa(year, cache=True)
_data = st.session_state.data
columns = [c[0] for c in _columns]
column = st.sidebar.selectbox("Column", columns[1:], index=0)  # skip the geoid
map_values = [(row[0], row[column+1]) for row in _data]
# correlation between variables

# map
m = get_map(year, map_values=map_values)
st.folium_static(m)