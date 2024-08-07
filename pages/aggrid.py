import streamlit as st
from pages.pages_format import pages_format
from utils.synthetic_data import create_synthetic_data
from st_aggrid import AgGrid, GridOptionsBuilder

# ---------------------------------------------------------------------
# HOME PAGE - CONFIGURATION
# ---------------------------------------------------------------------
st.set_page_config(
    layout="wide",
)

pages_format()

# ---------------------------------------------------------------------
# Generate data to plot
# ---------------------------------------------------------------------
df = create_synthetic_data()

# ---------------------------------------------------------------------
# MAIN PANEL
# ---------------------------------------------------------------------
with st.container(border=True):
    st.html('<h5>Standard st.dataframe() view vs Standard AgGrid view</h5>')
    st.markdown("- *st.dataframe()* better styled by default with comma separators \n"
                "- AgGrid can drag columns to a different position \n"
                "- AgGrid leaves a lot of empty space below \n"
                "- AgGrid is denser in display (check row height) \n"
                "- But AgGrid has more white space between columns \n"
                )

    with st.container(border=True):
        st.write('**st.dataframe()**')
        st.dataframe(df)

    with st.container(border=True):
        st.write('**AgGrid()**')
        standard_AgGrid = AgGrid(df, gridOptions=GridOptionsBuilder.from_dataframe(df).build())