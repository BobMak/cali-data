"""
A ACS public US census data set exploration dashboard
"""
import geopandas as gpd
import streamlit as st
from matplotlib import pyplot as plt
from streamlit_folium import folium_static

from califolium import get_map
from bigqcali import query_columns, query_cali_censustract, get_range_columns
import seaborn as sns


# Title
st.title("US Census Data Exploration")

# Subtitle
st.markdown("A CDE public dataset exploration dashboard")

# Sidebar
st.sidebar.title("Map")
st.sidebar.markdown("Will query five years of data prior to the selected year")
year = st.sidebar.slider("Year", 2010, 2020, 2011)
# available columns
if "columns" not in st.session_state:
    st.session_state.columns = query_columns(year, cache=True)
if "data" not in st.session_state:
    st.session_state.data = query_cali_censustract(year, cache=True)
if "gdb" not in st.session_state:
    st.session_state.gdb = gpd.read_file(f"cali{year}.geojson")

@st.cache_resource
def generate_map(year, column):
    # map
    map_values = st.session_state.data[["geo_id", column]]
    # rename the geo_id column to GEOID, and column name to value
    map_values = map_values.rename(columns={'geo_id': 'GEOID', column: 'value'})
    # type consistency
    map_values['GEOID'] = map_values['GEOID'].astype(object)
    map = get_map(year, map_values=map_values, gdb=st.session_state.gdb)
    return map

@st.cache_data
def get_columns():
    return [c for c in st.session_state.columns['column_name']]
columns = get_columns()
column = st.sidebar.selectbox("Column", columns[1:], index=4, )  # skip the geoid

m = generate_map(year, column)
folium_static(m)

# correlation between variables
# list of variables to show correlation
if "selected" not in st.session_state:
    st.session_state.selected = columns[1:3]
st.sidebar.title("Correlation")
st.session_state.selected = st.sidebar.multiselect("Variables", columns[1:], default=st.session_state.selected)
# quick select all or minimum set of variables
if 'select_all' not in st.session_state:
    st.session_state.select_all = True

selection_label = "select all" if st.session_state.select_all else "select none"
if st.sidebar.button(selection_label):
    selected = columns[1:] if st.session_state.select_all else columns[1:3]
    st.session_state.select_all = not st.session_state.select_all

corr = st.session_state.data[st.session_state.selected].corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, annot=False, cmap='coolwarm', vmin=-1, vmax=1, ax=ax)
st.title("Correlation Matrix Heatmap")
st.pyplot(fig)

# range variables
if "ranges" not in st.session_state:
    st.session_state.ranges = get_range_columns(st.session_state.columns)
st.sidebar.title("Range Variables")
st.session_state.range_selected = st.sidebar.selectbox("Range Var", list(st.session_state.ranges.keys()), index=1)
st.session_state.y_selected     = st.sidebar.selectbox("Y Variable", columns, index=4)

# range plot
fig, ax = plt.subplots(figsize=(10, 8))
range_cols = st.session_state.ranges[st.session_state.range_selected]
mean_y_data = st.session_state.data.groupby(st.session_state.y_selected)[range_cols].mean().mean()
range_plt = sns.barplot(
    x=range_cols,
    y=mean_y_data

)
range_plt.set(ylabel=st.session_state.y_selected)
for item in range_plt.get_xticklabels():
    item.set_rotation(45)
st.title("Range Plot")
st.pyplot(fig)
