import altair as alt
import pandas as pd
import streamlit as st


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
            tooltip=["period", "value"],
        )
        .properties(width="container")
    )

    st.altair_chart(line_chart, width="stretch")

    # Keeping the raw table below the chart is useful while developing
    # because it lets us verify the exact rows behind the visual.
    st.dataframe(chart_data)
