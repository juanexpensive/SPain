import streamlit as st


def render_header() -> None:
    # This top section explains the product quickly before the user interacts with it.
    st.title("SPain")
    st.subheader("Evolution of appraised free-market housing value by province in Spain")
    st.write("Based on official MIVAU provincial data in euros per square meter")


def render_ranking(ranking_data):
    # This table shows the ranking of all provinces sorted by variation.
    # It gives the user a broader context to compare the selected province against.
    st.subheader("Ranking of provinces by value variation")
    ranking_table = (
        ranking_data[["variation"]]
        .sort_values("variation", ascending=False)
        .reset_index()
        .rename(
            columns={
                "province": "Province",
                "variation": "Absolute variation (EUR/m2)",
            }
        )
    )
    ranking_table["Absolute variation (EUR/m2)"] = ranking_table[
        "Absolute variation (EUR/m2)"
    ].map(lambda value: f"{value:.2f}")
    st.dataframe(ranking_table, hide_index=True)


def render_select_periods(periods):
    # We split the period controls into two columns to make the range
    # easier to scan as a start/end pair.
    col1, col2 = st.columns(2)

    first_period = col1.selectbox("select first period", options=periods, index=0)
    last_period = col2.selectbox(
        "select last period",
        options=periods,
        index=len(periods) - 1,
    )

    return first_period, last_period

def render_highest_lowest(highest_variation, lowest_variation):
    # This section highlights the provinces with the highest and lowest variation
    # in the selected period range, so the user can quickly identify them.
    st.subheader("Provinces with highest and lowest variation")
    col1, col2 = st.columns(2)
    col1.metric("Highest variation", f"{highest_variation.name} ({highest_variation.variation:.2f} EUR/m2)")
    col2.metric("Lowest variation", f"{lowest_variation.name} ({lowest_variation.variation:.2f} EUR/m2)")

def render_kpis(latest_value, variation, percentage_variation) -> None:
    # This row mixes province-specific KPIs with market-wide highlights
    # so the user can compare one province against the broader ranking.
    col1, col2, col3 = st.columns(3)
    col1.metric("Latest appraised value (EUR/m2)", f"{latest_value:.2f} €/m2")
    col2.metric("Absolute variation (EUR/m2)", f"{variation:.2f} €/m2")

    if variation > 0:
        arrow = "↑"
    elif variation < 0:
        arrow = "↓"
    else:
        arrow = "="

    col3.metric("Percentage variation", f"{arrow}{percentage_variation:.2f}%")
