import streamlit as st
from pages.pages_format import pages_format
from utils.synthetic_data import create_synthetic_data
from utils.styler_functions import raw_styler_object, styler_with_thousands_commas_object, styler_with_colour_gradients_object, styler_with_dollar_sign_object, styler_with_medal_emoji_object


# ---------------------------------------------------------------------
# HOME PAGE - CONFIGURATION
# ---------------------------------------------------------------------
st.set_page_config(
    layout="wide",
)

pages_format()

st.write('hello')
