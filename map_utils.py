import os
import requests
import geopandas as gpd


def get_us_county_data(year, state='06', download=True):
    geojson_name = f"cali{year}.geojson"
    if os.path.exists(f"{geojson_name}"):
        return
    filename = f"tl_{year}_{state}_tract"
    if not os.path.exists(f"tmp/{filename}.shp") and download:
        url = f"https://www2.census.gov/geo/tiger/TIGER{year}/TRACT/{filename}.zip"
        response = requests.get(url, allow_redirects=True)
        open(f"{filename}.zip", 'wb').write(response.content)
        # unzip
        os.system(f"unzip {filename}.zip -d tmp")
    # transform into geojson
    gdf = gpd.read_file(f"tmp/{filename}.shp")
    # Save as GeoJSON for folium to use
    gdf.to_file(geojson_name, driver="GeoJSON")
    # remove the zip
    os.system(f"rm -rf {filename}")


if __name__ == "__main__":
    get_us_county_data(2015)