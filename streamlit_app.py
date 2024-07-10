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
# Generate data to plot
# ---------------------------------------------------------------------
mock_data = {
    "Country": ["US", "IN", "BR", "ES", "AR", "IT"],
    "Period_1": [50_000, 30_000, 17_000, 14_000, 22_000, 16_000],
    "Period_2": [52_000, 37_000, 16_000, 12_000, 21_000, 19_000],
}

df = pd.DataFrame(mock_data)
df['Difference'] = df['Period_2'] - df['Period_1']
df['Percentage Change'] = np.round(((df['Period_2'] - df['Period_1']) / df['Period_1']) * 100, 2)

# ---------------------------------------------------------------------
# MAIN PANEL
# ---------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.html('<h5>Step 1: Raw dataframe object</h5>')
        st.write('You can see xxxxx')
        st.dataframe(df)

with col2:
    with st.container(border=True):
        st.html('<h5>Step 2: Raw styler object</h5>')
        st.write('You can see xxxx')
        raw_styler = df.style
        st.dataframe(raw_styler)

