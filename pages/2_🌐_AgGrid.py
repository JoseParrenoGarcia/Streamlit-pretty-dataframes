import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from utils.synthetic_data import create_synthetic_data
from utils.aggrid_styling import aggrid_cells_formatting, aggrid_aggregation


# ---------------------------------------------------------------------
# HOME PAGE - CONFIGURATION
# ---------------------------------------------------------------------
st.set_page_config(
    layout="wide",
)

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
    st.write('If you clicks on the "burger" icon in any of the columns above, or use right hand side '
             'pinned menu, you can filter by any of the fields. When you have filtered the data, '
             'we can pass it back as a new dataframe (it could be pandas or polars) so use it later in the Streamlit'
             'app.')
    st.write('   ')
    st.write('For example, below I am only displaying the result of whatever you are seeing and filtering in the dataframe '
             'above. But you can imagine using this dataframe to show a plot')

    st.dataframe(filtered_df)

with st.container(border=True):
    st.subheader('Enabling aggregation through the UI')
    st.write('Being able to aggregate directly using the UI is amazing. In order to aggregate: ')
    st.markdown("- Click on 'Columns'  tab located in the right hand side pinned menu \n"
                "- You can drag any of the columns to the 'Row Groups' section \n"
                "- Doing that 'will trigger the aggregation functions defined in the 'Values' section. \n"
                )

    grid_response_agg = aggrid_aggregation(df)



