import streamlit as st
from streamlit_folium import st_folium
import folium

from utils import create_color_dict
from geodata_functions import load_geodata, create_choropleth_gdf

st.set_page_config(
    page_title="Tokyo Konbini Choropleth Map", page_icon=":convenience_store:"
)


DATA_FILE = "data/konbini_locations_processed.geojson"
TOKYO_AREA_GEOJSON = "data/tokyo_area.geojson"

st.title("Convenience store density in Tokyo")


geodata = load_geodata(DATA_FILE)
tokyo_area_geometry = load_geodata(TOKYO_AREA_GEOJSON)["geometry"][0]

konbini_colors = create_color_dict(geodata)

# Mapping

min_lon, max_lon = 137, 141
min_lat, max_lat = (
    33,
    37,
)

with st.sidebar:
    st.title("Convenience Stores in Tokyo - Density")
    st.subheader("Choropleth Settings")
    st.slider(
        key="choropleth_square_distance",
        min_value=1.0,
        max_value=10.0,
        step=0.5,
        label="Choropleth Square Distance (km)",
        value=2.0,
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

choropleth_data = create_choropleth_gdf(
    geodata,
    st.session_state["choropleth_square_distance"],
    bounding_area=tokyo_area_geometry,
)

choropleth_data["key"] = [str(x) for x in choropleth_data.index]
folium.Choropleth(
    geo_data=choropleth_data,
    fill_opacity=0.7,
    line_weight=1,
    data=choropleth_data,
    columns=["key", "store_count"],
    key_on="feature.properties.key",
).add_to(m)
folium.LayerControl().add_to(m)

st_data = st_folium(m, width=725, returned_objects=[])
