import streamlit as st
from pages.pages_format import pages_format
from st_aggrid import AgGrid, GridOptionsBuilder
from utils.synthetic_data import create_synthetic_data
from utils.aggrid_styling import aggrid_cells_formatting, aggrid_aggregation


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
    st.subheader('Standard st.dataframe() view vs Standard AgGrid view')
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

with st.container(border=True):
    st.subheader('Formatting values in cells')
    st.markdown("- Thousand comma separators \n"
                "- Decimal points \n"
                "- Column width \n"
                "- Currency symbol \n"
                "- ... and all of these filterable!! \n"
                )

    grid_response, filtered_df = aggrid_cells_formatting(df)


with st.container(border=True):
    st.subheader('Passing the filtered table above as an input to other Streamlit objects')

    st.dataframe(filtered_df)

with st.container(border=True):
    st.subheader('Enabling aggregation through the UI')

    grid_response_agg = aggrid_aggregation(df)



