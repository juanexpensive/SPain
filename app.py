import streamlit as st
from src.data.loader import load_housing_data
from src.ui.components import render_header
from src.ui.page import render_body

# Configure the Streamlit page before rendering anything on screen.
st.set_page_config(page_title="SPain", layout="wide")

# Load the dataset once at the entry point and pass it down explicitly.
# This keeps the data flow simple and avoids hidden globals in the UI files.
try: 
    housing_data = load_housing_data()
except Exception as e:
    st.error(f"Failed to load housing data: {e}")
    st.stop()  

render_header()
render_body(housing_data)
