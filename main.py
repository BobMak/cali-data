"""
A ACS public US census data set exploration dashboard
"""
import streamlit as st
import pandas as pd
import numpy as np
from califolium import get_map


# Title
st.title("US Census Data Exploration")

# Subtitle
st.markdown("A CDE public dataset exploration dashboard")

# Sidebar
st.sidebar.title("User Input Features")
st.sidebar.markdown("Select the features you want to explore")

# Sidebar - Year
year = st.sidebar.slider("Year", 2010, 2015, 2011)

# map
m = get_map()
folium_static(m)