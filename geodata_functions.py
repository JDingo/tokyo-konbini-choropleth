import geopandas
import streamlit as st
from shapely.geometry import Polygon, MultiPolygon
import numpy

# Source: University of Wisconsin-Madison
# https://www.sco.wisc.edu/2022/01/21/how-big-is-a-degree/
LATITUDE_KILOMETER_RATIO = 1 / 111.1
LONGITUDE_KILOMETER_RATIO = 1 / 96.2

MIN_LATITUDE = 35.4
MAX_LATITUDE = 35.9
MIN_LONGITUDE = 139.1
MAX_LONGITUDE = 140


def solve_latitude_longitude_difference_for_distance(
    distance: float,
) -> tuple[float, float]:
    return (LATITUDE_KILOMETER_RATIO * distance, LONGITUDE_KILOMETER_RATIO * distance)


@st.cache_data
def load_geodata(fpath: str):
    return geopandas.read_file(fpath)


def create_choropleth_gdf(
    gdf_store: geopandas.GeoDataFrame,
    distance: float,
    bounding_area: Polygon | MultiPolygon | None = None,
):
    delta_lat, delta_long = solve_latitude_longitude_difference_for_distance(distance)

    latitudes = list(numpy.arange(MIN_LATITUDE, MAX_LATITUDE, delta_lat))
    longitudes = list(numpy.arange(MIN_LONGITUDE, MAX_LONGITUDE, delta_long))

    geometries = []

    store_count = []

    for latitude in latitudes:
        for longitude in longitudes:
            stores_in_area = len(
                gdf_store[
                    (gdf_store["first_coordinate_latitude"] > latitude)
                    & (gdf_store["first_coordinate_latitude"] < latitude + delta_lat)
                    & (gdf_store["first_coordinate_longitude"] > longitude)
                    & (gdf_store["first_coordinate_longitude"] < longitude + delta_long)
                ]
            )

            store_count.append(stores_in_area)

            geometries.append(
                Polygon(
                    zip(
                        [
                            longitude,
                            longitude + delta_long,
                            longitude + delta_long,
                            longitude,
                        ],
                        [
                            latitude,
                            latitude,
                            latitude + delta_lat,
                            latitude + delta_lat,
                        ],
                    ),
                )
            )

    df_choropleth_blanked = geopandas.GeoDataFrame(
        data=store_count, crs="WGS84", geometry=geometries, columns=["store_count"]
    )

    return df_choropleth_blanked[
        df_choropleth_blanked["geometry"].intersects(bounding_area, align=False)
    ]
