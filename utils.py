import streamlit as st
import geojson


@st.cache_data(show_spinner=False)
def create_color_dict(geojson: geojson.GeoJSON) -> dict:
    print("Creating color dict...")
    color_dict = {}

    for feature in geojson["features"]:
        brand = feature["properties"]["brand"]
        if brand not in color_dict:
            color_dict[brand] = get_color(brand)

    return color_dict


@st.cache_data
def get_color(brand: str) -> str:
    if brand in ["7-ELEVEN", "セブン-イレブン"]:
        return "#EE2526"

    if brand in ["ファミリーマート", "FamilyMart"]:
        return "#0091D4"

    if "ローソン" in brand or "lawson" in brand.lower():
        return "#1475c5"

    if "MINISTOP" in brand or "ミニストップ" in brand:
        return "#003595"

    if "デイリーヤマザキ" in brand:
        return "#f5e829"

    if "NewDays" in brand:
        return "#C7D51F"

    return "#808080"
