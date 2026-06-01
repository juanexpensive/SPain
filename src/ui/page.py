import pandas as pd
import streamlit as st

from src.domain.analytics import (
    build_map_data,
    calculate_kpis,
    filter_period_range,
    get_province_data,
    calculate_highest_and_lowest_variation,
    normalize_period_range,
    prepare_periods,
    calculate_ranking
)
from src.ui.charts import render_chart, render_province_map
from src.ui.components import render_highest_lowest, render_kpis, render_ranking, render_select_periods


def render_body(housing_data: pd.DataFrame) -> None:
    # Build the province selector from the available dataset values.
    provinces = housing_data["province"].unique()
    selected_province = st.selectbox("select a province", options=provinces)

    # Prepare the selected province data before calculating anything else.
    sorted_province_data = get_province_data(housing_data, selected_province)
    available_periods = prepare_periods(sorted_province_data)

    # Read the date range from the UI and normalize it if the user picked it backwards.
    first_period, last_period = render_select_periods(available_periods)
    first_period, last_period, was_swapped = normalize_period_range(
        first_period,
        last_period,
    )

    if was_swapped:
        st.info("Selected period range was reversed, so it has been swapped automatically.")

    # This filtered table represents the exact slice of data we want to analyze
    # for the selected province and period range.
    selected_range_data = filter_period_range(
        sorted_province_data,
        first_period,
        last_period,
    )

    # The chart only needs period and value, so we prepare a smaller table for it.
    chart_data = selected_range_data[["period", "value"]]

    # The ranking looks across all provinces, using the same period range chosen in the UI.
    ranking_data = calculate_ranking(housing_data, first_period, last_period)
    map_data = build_map_data(housing_data, first_period, last_period)

    # Extract the top and bottom province from the sorted ranking table
    # so we can show them as headline highlights.
    highest_variation, lowest_variation = calculate_highest_and_lowest_variation(
        ranking_data
    )

    # Calculate the KPI values for the province currently selected in the chart.
    latest_value, variation, percentage_variation = calculate_kpis(selected_range_data)

    # Render the KPI row first so the user sees the summary before the detailed chart.
    render_kpis(latest_value, variation, percentage_variation)

    # Render the detailed time-series view after the summary cards.
    render_chart(chart_data, selected_province, first_period, last_period)

    map_metric = st.radio(
        "Map colored by",
        options=["latest value", "variation"],
        horizontal=True,
    )
    map_metric_key = "last_value" if map_metric == "latest value" else "variation"
    render_province_map(map_data, selected_province, map_metric_key)

    render_highest_lowest(highest_variation, lowest_variation)

    render_ranking(ranking_data)
