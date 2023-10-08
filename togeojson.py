import geopandas as gpd

# Read the shapefile
gdf = gpd.read_file("tl_2015_us_county/tl_2015_us_county.shp")
# Filter california
gdf_filtered = gdf[gdf['GEOID'].str.startswith('06')]
# Save as GeoJSON
gdf_filtered.to_file("cali.geojson", driver="GeoJSON")
