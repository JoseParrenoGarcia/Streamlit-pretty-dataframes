import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

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


def _format_with_dollar_sign(val, prec=0):
    return f'${val:,.{prec}f}'


def _format_positive_negative_background_colour(val, min_value, max_value):
    if val > 0:
        # Normalize positive values to a scale of 0 to 1
        normalized_val = (val - 0) / (max_value - 0)
        # Create a gradient of green colors
        color = plt.cm.Greens(normalized_val * 0.7)
        color_hex = mcolors.to_hex(color)
    elif val < 0:
        # Normalize negative values to a scale of 0 to -1
        normalized_val = (val - min_value) / (0 - min_value)
        # Create a gradient of red colors
        color = plt.cm.Reds_r(normalized_val * 0.7)
        color_hex = mcolors.to_hex(color)
    else:
        color_hex = 'white'  # For zero values, set the background color to white

    # Determine text color based on the darkness of the background color
    r, g, b = mcolors.hex2color(color_hex)
    if (r * 299 + g * 587 + b * 114) / 1000 > 0.5:  # Use the formula for perceived brightness
        text_color = 'black'
    else:
        text_color = 'white'

    return f'background-color: {color_hex}; color: {text_color}'


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
raw_styler = df.copy().style

# With thousands commas + perctange format
thousands_cols = ['Period_1', 'Period_2', 'Difference']
perct_cols = ['Percentage Change']
styler_with_thousands_commas = (df.copy().style
                                .format(_format_with_thousands_commas, subset=thousands_cols)
                                .format(lambda x: _format_as_percentage(x, 2), subset=perct_cols)
                                )

# +ve and -ve gradients
min_value_abs_diff = df['Difference'].min()
max_value_abs_diff = df['Difference'].max()

min_value_perct_diff = df['Percentage Change'].min()
max_value_perct_diff = df['Percentage Change'].max()

styler_with_colour_gradients = (df.copy().style
                                .format(_format_with_thousands_commas, subset=thousands_cols)
                                .format(lambda x: _format_as_percentage(x, 2), subset=perct_cols)
                                .map(lambda x: _format_positive_negative_background_colour(x, min_value_abs_diff, max_value_abs_diff),
                                     subset=['Difference'])
                                .map(lambda x: _format_positive_negative_background_colour(x, min_value_perct_diff, max_value_perct_diff),
                                     subset=['Percentage Change'])
                                )

# $ sign
styler_with_dollar_sign = (df.copy().style
                           .format(_format_with_thousands_commas, subset=thousands_cols)
                           .format(lambda x: _format_as_percentage(x, 2), subset=perct_cols)
                           .map(lambda x: _format_positive_negative_background_colour(x, min_value_abs_diff, max_value_abs_diff),
                                subset=['Difference'])
                           .map(lambda x: _format_positive_negative_background_colour(x, min_value_perct_diff, max_value_perct_diff),
                                subset=['Percentage Change'])
                           .format(_format_with_dollar_sign, subset=['Period_1', 'Period_2', 'Difference'])
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

    with st.container(border=True):
        st.html('<h5>Step 5: Add dollar sign</h5>')
        st.write('xxxx')
        st.dataframe(styler_with_dollar_sign)

    with st.container(border=True):
        st.html('<h5>Step 7: Bar charts in background</h5>')
        st.write('xxxx')
        st.dataframe(df)

with col2:
    with st.container(border=True):
        st.html('<h5>Step 2: Raw styler object</h5>')
        st.write('The styler messes the UI display. No commas and 6 decimal points')
        st.dataframe(raw_styler)

    with st.container(border=True):
        st.html('<h5>Step 4: +ve & -ve coloured gradients</h5>')
        st.write('Now we are ready to colour columns. We want a green gradient for positive values and a negative '
                 'gradient for negative values.')

        with st.expander('See code sample', expanded=False):
            st.code('''
            def _format_positive_negative_background_colour(val, min_value, max_value):
                if val > 0:
                    # Normalize positive values to a scale of 0 to 1
                    normalized_val = (val - 0) / (max_value - 0)
                    # Create a gradient of green colors
                    color = plt.cm.Greens(normalized_val * 0.7)
                    color_hex = mcolors.to_hex(color)
                elif val < 0:
                    # Normalize negative values to a scale of 0 to -1
                    normalized_val = (val - min_value) / (0 - min_value)
                    # Create a gradient of red colors
                    color = plt.cm.Reds_r(normalized_val * 0.7)
                    color_hex = mcolors.to_hex(color)
                else:
                    color_hex = 'white'  # For zero values, set the background color to white
            
                # Determine text color based on the darkness of the background color
                r, g, b = mcolors.hex2color(color_hex)
                if (r * 299 + g * 587 + b * 114) / 1000 > 0.5:  # Use the formula for perceived brightness
                    text_color = 'black'
                else:
                    text_color = 'white'
            
                return f'background-color: {color_hex}; color: {text_color}'

            min_value_abs_diff = df['Difference'].min()
            max_value_abs_diff = df['Difference'].max()
            
            min_value_perct_diff = df['Percentage Change'].min()
            max_value_perct_diff = df['Percentage Change'].max()
            
            styler_with_colour_gradients = (df.copy().style
                                            .format(_format_with_thousands_commas, subset=thousands_cols)
                                            .format(lambda x: _format_as_percentage(x, 2), subset=perct_cols)
                                            .map(lambda x: _format_positive_negative_background_colour(x, min_value_abs_diff, max_value_abs_diff),
                                                 subset=['Difference'])
                                            .map(lambda x: _format_positive_negative_background_colour(x, min_value_perct_diff, max_value_perct_diff),
                                                 subset=['Percentage Change'])
                                            )
            ''')

        st.dataframe(styler_with_colour_gradients)

    with st.container(border=True):
        st.html('<h5>Step 6: Add column with emojis</h5>')
        st.write('xxxx')
        st.dataframe(df)
