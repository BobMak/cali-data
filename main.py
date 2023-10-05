"""
A public us census data set exploration dashboard
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Title
st.title("US Census Data Exploration")

# Subtitle
st.markdown("This application is a Streamlit dashboard that can be used "
            "to explore the US Census Data")

# Sidebar
st.sidebar.title("User Input Features")
st.sidebar.markdown("Select the features you want to explore")

# Read in the data
@st.cache(persist=True)
def load_data():
    data = pd.read_csv("census.csv")
    data["date"] = pd.to_datetime(data["date"])
    return data

data = load_data()

# Sidebar - Year
year = st.sidebar.slider("Year", 2010, 2015, 2011)
data = data[data["date"].dt.year == year]

# Sidebar - Month
month = st.sidebar.slider("Month", 1, 12, 1)
data = data[data["date"].dt.month == month]

# Sidebar - Region
region = st.sidebar.selectbox("Region", ["Northeast", "Midwest", "South", "West"])
data = data[data["region"] == region]

# Sidebar - Age
age = st.sidebar.slider("Age", 0, 100, 20)
data = data[data["age"] == age]