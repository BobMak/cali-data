import os
import requests
import geopandas as gpd


def get_us_county_data(year, download=True):
    geojson_name = f"cali{year}.geojson"
    if os.path.exists(f"{geojson_name}"):
        return
    filename = f"tl_{year}_us_county.zip"
    url = f"https://www2.census.gov/geo/tiger/TIGER{year}/COUNTY/{filename}"
    if not os.path.exists(f"{filename}") and download:
        response = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(response.content)
        # unzip
        os.system(f"unzip {filename} -d tmp")
    # transform into geojson
    gdf = gpd.read_file(f"tmp/tl_{year}_us_county.shp")
    # Filter california
    gdf_filtered = gdf[gdf['GEOID'].str.startswith('06')]
    # Save as GeoJSON for folium to use
    gdf_filtered.to_file(geojson_name, driver="GeoJSON")
    # remove the zip
    os.system(f"rm -rf {filename}")


if __name__ == "__main__":
    get_us_county_data(2015)