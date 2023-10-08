import folium


def get_map(lat=37.7749, long=-122.4194):
    # Create a base map
    m = folium.Map(location=[lat, long], zoom_start=10) 
    # Add the GeoJSON to the map
    folium.GeoJson('cali.geojson').add_to(m)
    return m


if __name__ == "__main__":
    m = get_map()
    m.save('cali.html')