import streamlit as st


def render_header() -> None:
    # This top section explains the product quickly before the user interacts with it.
    st.title("SPain")
    st.subheader("Evolution of housing prices by province in Spain")
    st.write("First version under construction")


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


def render_kpis(latest_value, variation, percentage_variation, highest_variation, lowest_variation) -> None:
    # This row mixes province-specific KPIs with market-wide highlights
    # so the user can compare one province against the broader ranking.
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Latest value", latest_value)
    col2.metric("Variation", variation)
    col3.metric("% of variation", f"{percentage_variation:.2f}%")
    col4.metric("Province with highest variation", f"{highest_variation.name}")
    col5.metric("Province with lowest variation", f"{lowest_variation.name}")
