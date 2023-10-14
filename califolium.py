import os
import folium
import geopandas as gpd

from map_utils import get_us_county_data

from bigqcali import query_cali_censustract


def get_map(year, map_values=None, gdb=None, lat=37.7749, long=-122.4194):
    """
    :param year: selected census year. will re-download the map for that year if it doesn't exist
    :param map_values: df with geo_id and value columns
    :param gdb: geopandas dataframe
    :param lat: initial latitude
    :param long: initial longitude
    :return: displayable map
    """
    # Create a base map
    m = folium.Map(location=[lat, long], zoom_start=10) 
    # Add the GeoJSON to the map
    if not os.path.exists(f"cali{year}.geojson"):
        get_us_county_data(year)

    # Add the choropleth
    folium.Choropleth(
        geo_data=gdb,
        data=map_values,
        columns=['GEOID', 'value'],
        key_on='feature.properties.GEOID',
        fill_color='OrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Value'
    ).add_to(m)
    return m


if __name__ == "__main__":
    gdb = gpd.read_file(f"cali2011.geojson")
    df = query_cali_censustract(2015)
    df = df[["geo_id", 'one_car']]
    # rename the geo_id column to GEOID, and column name to value
    df = df.rename(columns={'geo_id': 'GEOID', 'one_car': 'value'})

    print(gdb.head())