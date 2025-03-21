import streamlit as st
import geopandas
import numpy as np


@st.cache_data(show_spinner=False)
def create_color_dict(_gdf: geopandas.GeoDataFrame) -> dict:
    color_dict = {}

    for brand in _gdf["brand"]:
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


def get_color_scale_bins(curve_type: str, n_bins: int, max_value: int):
    match curve_type:
        case "Linear":
            return np.linspace(start=0, stop=max_value, num=n_bins, endpoint=True)
        case "Logarithmic":
            return np.concatenate(
                [
                    [0],
                    np.geomspace(
                        start=1,
                        stop=max_value,
                        num=n_bins,
                        endpoint=True,
                        dtype=np.int32,
                    ),
                ]
            )
