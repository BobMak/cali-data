import os
import folium
import geopandas as gpd

from map_utils import get_us_county_data


def get_map(year, map_values, lat=37.7749, long=-122.4194):
    """
    :param year: selected census year. will re-download the map for that year if it doesn't exist
    :param map_values: geoid-value pairs to color the map
    :param lat: initial latitude
    :param long: initial longitude
    :return: displayable map
    """
    # Create a base map
    m = folium.Map(location=[lat, long], zoom_start=10) 
    # Add the GeoJSON to the map
    if not os.path.exists(f"cali{year}.geojson"):
        get_us_county_data(year)
    # Add values to the geojson
    gdb = gpd.read_file(f"cali{year}.geojson")
    for geoid, value in map_values:
        gdb.loc[gdb['GEOID'] == geoid, 'value'] = value
    # Add the choropleth
    folium.Choropleth(
        geo_data=gdb,
        name='choropleth',
        data=gdb,
        columns=['GEOID', 'value'],
        key_on='feature.properties.GEOID',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Value'
    ).add_to(m)
    # Add the geojson
    folium.GeoJson(gdb,name='geojson').add_to(m)
    return m