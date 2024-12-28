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

gdf.to_file("konbini_locations_processed.geojson", driver="GeoJSON")
