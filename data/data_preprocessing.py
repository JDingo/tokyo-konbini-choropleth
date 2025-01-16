import geopandas
import geojson

# Load data
gdf = geopandas.read_file("./konbini_locations.geojson")

# Select columns
gdf = gdf.loc[
    :,
    [
        "id",
        "@id",
        "branch",
        "branch:en",
        "branch:ja",
        "branch:ja-Hira",
        "branch:ja-Latn",
        "branch:ja_kana",
        "brand",
        "brand:en",
        "brand:ja",
        "brand:ja-Hira",
        "brand:ja-Latn",
        "name",
        "name:en",
        "name:ja",
        "name:ja-Hira",
        "name:ja-Latn",
        "name:ja_kana",
        "name:ja_rm",
        "official_name",
        "official_name:en",
        "shop",
        "type",
        "url",
        "geometry",
    ],
]

gdf = gdf[~gdf["brand"].isnull()]
gdf["geometry_type"] = gdf["geometry"].type


def solve_coordinates_long(x):
    if x["geometry_type"] == "LineString":
        return x["geometry"].coords.xy[0][0]
    elif x["geometry_type"] == "Polygon":
        return x["geometry"].exterior.coords.xy[0][0]
    elif x["geometry_type"] == "Point":
        return x["geometry"].coords.xy[0][0]
    else:
        print("Unknown geometry type!")


def solve_coordinates_lat(x):
    if x["geometry_type"] == "LineString":
        return x["geometry"].coords.xy[1][0]
    elif x["geometry_type"] == "Polygon":
        return x["geometry"].exterior.coords.xy[1][0]
    elif x["geometry_type"] == "Point":
        return x["geometry"].coords.xy[1][0]
    else:
        print("Unknown geometry type!")


gdf["first_coordinate_longitude"] = gdf.apply(
    lambda x: solve_coordinates_long(x),
    axis=1,
)

gdf["first_coordinate_latitude"] = gdf.apply(
    lambda x: solve_coordinates_lat(x),
    axis=1,
)

gdf.to_file("konbini_locations_processed.geojson", driver="GeoJSON")
