import streamlit as st
from src.data.loader import load_housing_data
from src.ui.components import render_header
from src.ui.page import render_body

# Load the dataset once at the entry point and pass it down explicitly.
# This keeps the data flow simple and avoids hidden globals in the UI files.
housing_data = load_housing_data()

# Configure the Streamlit page before rendering anything on screen.
st.set_page_config(page_title="SPain", layout="wide")
render_header()
render_body(housing_data)
