import copy
import json
from urllib.request import urlopen
from typing import Any, cast

import altair as alt
import pandas as pd
import pydeck as pdk
import streamlit as st

SPAIN_PROVINCES_GEOJSON_URL = (
    "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/spain-provinces.geojson"
)
GEOJSON_TO_DATA_PROVINCE = {
    "Alacant/Alicante": "Alicante/Alacant",
    "Bizkaia/Vizcaya": "Bizkaia",
    "Castelló/Castellón": "Castellón/Castelló",
    "Gipuzkoa/Guipúzcoa": "Gipuzkoa",
    "Santa Cruz De Tenerife": "Santa Cruz de Tenerife",
    "València/Valencia": "Valencia/València",
}


@st.cache_data(show_spinner=False)
def load_spain_provinces_geojson() -> dict:
    with urlopen(SPAIN_PROVINCES_GEOJSON_URL, timeout=30) as response:
        return json.load(response)


def render_chart(
    chart_data: pd.DataFrame,
    selected_province: str,
    first_period,
    last_period,
) -> None:
    # Give the chart a short sentence so the user always knows
    # which province and period range is being plotted.
    st.write(
        f"Appraised free-market housing value in {selected_province} between {first_period} and {last_period}"
    )

    # Altair gives us explicit control over the axes and tooltip,
    # which is safer than relying on Streamlit to infer the chart shape.
    line_chart = (
        alt.Chart(chart_data)
        .mark_line(point=True)
        .encode(
            x=alt.X("period:O", title="Period"),
            y=alt.Y("value:Q", title="Appraised value (EUR/m2)"),
            tooltip=[
                alt.Tooltip("period:O", title="Period"),
                alt.Tooltip("value:Q", title="Appraised value (EUR/m2)", format=".2f"),
            ],
        )
        .properties(width="container")
    )

    st.altair_chart(line_chart, width="stretch")


def build_fill_color(metric_value: float, min_value: float, max_value: float, metric_key: str) -> list[int]:
    if max_value == min_value:
        return [160, 160, 160, 180]

    if metric_key == "variation":
        max_abs = max(abs(min_value), abs(max_value))

        if max_abs == 0:
            return [160, 160, 160, 180]

        intensity = abs(metric_value) / max_abs
        red_strength = int(120 + (110 * intensity))

        if metric_value > 0:
            return [red_strength, 55, 55, 190]
        if metric_value < 0:
            return [255, 215, 215, 190]

        return [160, 160, 160, 180]

    intensity = (metric_value - min_value) / (max_value - min_value)
    return [
        255,
        int(235 - 120 * intensity),
        int(235 - 120 * intensity),
        190,
    ]


def render_map_legend(metric_key: str, min_value: float, max_value: float) -> None:
    if metric_key == "last_value":
        st.caption("Legend: lighter red means lower appraised value, darker red means higher appraised value.")
        st.markdown(
            (
                "<div style='display:flex;align-items:center;gap:10px;margin:6px 0 14px 0;'>"
                "<span style='display:inline-block;width:22px;height:14px;background:#ffe9e9;border:1px solid #d0d0d0;'></span>"
                f"<span>Lower: {min_value:.2f} EUR/m2</span>"
                "<span style='display:inline-block;width:22px;height:14px;background:#ef8f8f;border:1px solid #d0d0d0;margin-left:12px;'></span>"
                "<span>Mid range</span>"
                "<span style='display:inline-block;width:22px;height:14px;background:#ff7373;border:1px solid #d0d0d0;margin-left:12px;'></span>"
                f"<span>Higher: {max_value:.2f} EUR/m2</span>"
                "</div>"
            ),
            unsafe_allow_html=True,
        )
        return

    st.caption("Legend: darker red means stronger positive variation, pale pink means negative variation.")
    st.markdown(
        (
            "<div style='display:flex;align-items:center;gap:10px;margin:6px 0 14px 0;'>"
            "<span style='display:inline-block;width:22px;height:14px;background:#ffd7d7;border:1px solid #d0d0d0;'></span>"
            f"<span>Negative: {min_value:.2f} EUR/m2</span>"
            "<span style='display:inline-block;width:22px;height:14px;background:#a0a0a0;border:1px solid #d0d0d0;margin-left:12px;'></span>"
            "<span>Near zero</span>"
            "<span style='display:inline-block;width:22px;height:14px;background:#d14b4b;border:1px solid #d0d0d0;margin-left:12px;'></span>"
            f"<span>Positive: {max_value:.2f} EUR/m2</span>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def render_province_map(
    map_data: pd.DataFrame,
    selected_province: str,
    metric_key: str,
) -> None:
    metric_label = {
        "last_value": "Latest appraised value (EUR/m2)",
        "variation": "Absolute variation (EUR/m2)",
    }[metric_key]

    geojson = copy.deepcopy(load_spain_provinces_geojson())
    metric_lookup = map_data.set_index("province").to_dict("index")
    metric_values = map_data[metric_key].tolist()
    min_value = min(metric_values)
    max_value = max(metric_values)

    for feature in geojson["features"]:
        original_name = feature["properties"]["name"]
        province_name = GEOJSON_TO_DATA_PROVINCE.get(original_name, original_name)
        province_metrics = metric_lookup.get(province_name)

        if province_metrics is None:
            feature["properties"]["fill_color"] = [220, 220, 220, 120]
            feature["properties"]["line_color"] = [110, 110, 110, 160]
            feature["properties"]["line_width"] = 1
            feature["properties"]["province"] = province_name
            feature["properties"]["metric_label"] = metric_label
            feature["properties"]["metric_value"] = "No data"
            feature["properties"]["latest_value"] = "No data"
            feature["properties"]["variation"] = "No data"
            continue

        metric_value = province_metrics[metric_key]
        feature["properties"]["province"] = province_name
        feature["properties"]["metric_label"] = metric_label
        feature["properties"]["metric_value"] = f"{metric_value:.2f}"
        feature["properties"]["latest_value"] = f"{province_metrics['last_value']:.2f}"
        feature["properties"]["variation"] = f"{province_metrics['variation']:.2f}"
        feature["properties"]["fill_color"] = build_fill_color(
            metric_value,
            min_value,
            max_value,
            metric_key,
        )

        if province_name == selected_province:
            feature["properties"]["line_color"] = [255, 196, 61, 255]
            feature["properties"]["line_width"] = 4
        else:
            feature["properties"]["line_color"] = [80, 80, 80, 160]
            feature["properties"]["line_width"] = 1

    st.subheader("Spain provincial map")
    st.caption(f"Colored by {metric_label.lower()}. The selected province is highlighted.")
    render_map_legend(metric_key, min_value, max_value)

    layer = pdk.Layer(
        "GeoJsonLayer",
        geojson,
        pickable=True,
        stroked=True,
        filled=True,
        get_fill_color="properties.fill_color",
        get_line_color="properties.line_color",
        get_line_width="properties.line_width",
        line_width_min_pixels=1,
        auto_highlight=True,
    )

    view_state = pdk.ViewState(latitude=40.3, longitude=-3.7, zoom=4.6)
    tooltip = {
        "html": (
            "<b>{province}</b><br/>"
            "{metric_label}: {metric_value}<br/>"
            "Latest value (EUR/m2): {latest_value}<br/>"
            "Variation (EUR/m2): {variation}"
        ),
        "style": {"backgroundColor": "rgba(20, 20, 20, 0.85)", "color": "white"},
    }
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="",
    )
    deck_any = cast(Any, deck)
    deck_any.tooltip = tooltip

    st.pydeck_chart(
        deck,
        width="stretch",
    )
