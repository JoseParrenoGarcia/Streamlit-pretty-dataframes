import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------
# HOME PAGE - CONFIGURATION
# ---------------------------------------------------------------------
st.set_page_config(
    layout="wide",
)


# ---------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------
def _format_with_thousands_commas(val):
    return f'{val:,.0f}'


def _format_as_percentage(val, prec=0):
    return f'{val:.{prec}%}'


# ---------------------------------------------------------------------
# Generate data to plot
# ---------------------------------------------------------------------
mock_data = {
    "Country": ["US", "IN", "BR", "ES", "AR", "IT"],
    "Period_1": [50_000, 30_000, 17_000, 14_000, 22_000, 16_000],
    "Period_2": [52_000, 37_000, 16_000, 12_000, 21_000, 19_000],
}

df = pd.DataFrame(mock_data)
df['Difference'] = df['Period_2'] - df['Period_1']
df['Percentage Change'] = np.round(((df['Period_2'] - df['Period_1']) / df['Period_1']), 2)

# Raw styler
raw_styler = df.style

# With thousands commas + perctange format
thousands_cols = ['Period_1', 'Period_2', 'Difference']
perct_cols = ['Percentage Change']
styler_with_thousands_commas = (raw_styler
                                .format(_format_with_thousands_commas, subset=thousands_cols)
                                .format(lambda x: _format_as_percentage(x, 2), subset=perct_cols)
                                )

# ---------------------------------------------------------------------
# MAIN PANEL
# ---------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.html('<h5>Step 1: Raw dataframe object</h5>')
        st.write('You can see thst streamlit automatically adds commas as thousands separators. It seems pretty enough, but not amazing.')
        st.dataframe(df)

    with st.container(border=True):
        st.html('<h5>Step 3: Adding thousands separator and % format</h5>')
        st.write('We can mimic the initial st.dataframe() view using defined styler functions')

        with st.expander('See code sample', expanded=False):
            st.code('''
            def _format_with_thousands_commas(val):
                return f'{val:,.0f}'
            
            def _format_as_percentage(val, prec=0):
                return f'{val:.{prec}%}'
            
            thousands_cols = ['Period_1', 'Period_2', 'Difference']
            perct_cols = ['Percentage Change']
            
            styler_with_thousands_commas = (raw_styler
                                .format(_format_with_thousands_commas, subset=thousands_cols)
                                .format(lambda x: _format_as_percentage(x, 2), subset=perct_cols)
                                )
            ''')

        st.dataframe(styler_with_thousands_commas)

with col2:
    with st.container(border=True):
        st.html('<h5>Step 2: Raw styler object</h5>')
        st.write('The styler messes the UI display. No commas and 6 decimal points')
        st.dataframe(raw_styler)

