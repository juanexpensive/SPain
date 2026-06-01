import pandas as pd


def get_province_data(housing_data: pd.DataFrame, selected_province: str) -> pd.DataFrame:
    # Keep only the rows for the province selected in the UI.
    # We sort by period here so every later calculation can assume
    # the first row is the oldest value and the last row is the newest.
    province_data = housing_data[housing_data["province"] == selected_province]
    return province_data.sort_values("period")


def prepare_periods(sorted_province_data: pd.DataFrame):
    # The selectboxes only need the distinct period labels available
    # for the currently selected province.
    return sorted_province_data["period"].unique()


def normalize_period_range(first_period, last_period):
    # Users may choose the range backwards in the UI.
    # Instead of breaking the app, we swap the values and return
    # a flag so the page can explain what happened.
    if first_period <= last_period:
        return first_period, last_period, False

    return last_period, first_period, True


def filter_period_range(
    sorted_province_data: pd.DataFrame,
    first_period,
    last_period,
) -> pd.DataFrame:
    # Keep only the rows that fall inside the selected period range.
    # This filtered table is reused for the chart and KPI calculations.
    return sorted_province_data[
        (sorted_province_data["period"] >= first_period)
        & (sorted_province_data["period"] <= last_period)
    ]


def calculate_kpis(selected_range_data: pd.DataFrame):
    # Because the data is already sorted by period, the first row represents
    # the beginning of the range and the last row represents the latest value.
    latest_row = selected_range_data.iloc[-1]
    first_row = selected_range_data.iloc[0]

    # Extract the numeric values that will feed the KPI cards.
    latest_value = latest_row["value"]
    first_value = first_row["value"]
    variation = latest_value - first_value

    # Avoid division by zero when computing percentage change.
    if first_value != 0:
        percentage_variation = (variation / first_value) * 100
    else:
        percentage_variation = 0

    return latest_value, variation, percentage_variation


def calculate_ranking(housing_data, first_period, last_period):
    # For the ranking we compare every province inside the same date range,
    # not just the province currently selected in the main chart.
    filtered_housing_data: pd.DataFrame = housing_data[
        (housing_data["period"] >= first_period)
        & (housing_data["period"] <= last_period)
    ]

    sorted_housing_data = filtered_housing_data.sort_values(["province", "period"])
    grouped_data = sorted_housing_data.groupby(["province"])

    # We keep only the first and last values for every province.
    # That gives us the minimum information needed to compare growth.
    first = grouped_data.first()["value"]
    last = grouped_data.last()["value"]

    # Build a summary table with one row per province.
    # Once variation is calculated, we sort descending so the province
    # with the biggest growth appears at the top.
    grouped_data = pd.DataFrame(
        {
            "first_value": first,
            "last_value": last,
            "variation": last - first,
        }
    ).sort_values("variation", ascending=False)

    return grouped_data


def calculate_highest_and_lowest_variation(ranking_data):
    # The ranking is already sorted from highest to lowest variation.
    # That means the first row is the winner and the last row is the lowest.
    highest_variation = ranking_data.iloc[0]
    lowest_variation = ranking_data.iloc[-1]
    return highest_variation, lowest_variation
