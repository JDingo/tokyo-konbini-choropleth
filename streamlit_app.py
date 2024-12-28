import streamlit as st
from streamlit_folium import st_folium
import geojson
import folium

from utils import create_color_dict

st.title("Convenience store density in Tokyo")


@st.cache_data
def load_geodata(fpath: str):
    print("Loaded geojson")
    with open(fpath, "r", encoding="utf-8") as datafile:
        return geojson.load(datafile)


geodata = load_geodata("data/konbini_locations_processed.geojson")

konbini_colors = create_color_dict(geodata)

# Mapping

min_lon, max_lon = 137, 141
min_lat, max_lat = (
    33,
    37,
)

m = folium.Map(
    location=(35.689722, 139.692222),
    max_bounds=True,
    min_lat=min_lat,
    max_lat=max_lat,
    min_lon=min_lon,
    max_lon=max_lon,
)

popup = folium.GeoJsonPopup(
    fields=["name", "shop"],
    aliases=["Name", "Shop"],
    localize=True,
    labels=True,
    style="background-color: yellow;",
)

folium.GeoJson(
    data=geodata,
    name="Convenience Store",
    marker=folium.Circle(
        fields=["name", "shop"],
        radius=10,
        fill=True,
        fill_opacity=0.6,
    ),
    popup=popup,
    style_function=lambda x: {"color": konbini_colors[x["properties"]["brand"]]},
).add_to(m)
folium.LayerControl().add_to(m)

st_data = st_folium(m, width=725, returned_objects=[])
