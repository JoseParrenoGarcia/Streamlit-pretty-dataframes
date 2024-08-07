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

st.title('Creating beautiful streamlit tables.')

st.write('')
st.html("<b>What</b>")
st.write('This app will show you a few methods of styling dataframes in your streamlit app. We will cover:')
st.markdown("- standard Styler objects \n"
            "- the AdGrid package \n"
            "- some other Streamlit default options \n"
            )

st.write('')
st.html("<b>Considerations</b>")
st.write('Of course, things might have changed depending on when you are reading/checking this app. For example,'
         'as of August 2024, I wrote the app based on the following package versions.')

st.markdown("- streamlit==1.35.0 \n"
            "- pandas==2.2.2 \n"
            "- matplotlib==3.9.0 \n"
            "- st-pages==0.4.5 \n"
            )

st.write('')
st.html("<b>Details</b>")
st.write("If you wish to check the exact code which generated this app, feel free to check the GitHub repo"
         "associated with the app.")
st.link_button("GitHub repo", "https://github.com/JoseParrenoGarcia/Streamlit-pretty-dataframes")
