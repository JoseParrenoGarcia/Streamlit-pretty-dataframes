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

# ---------------------------------------------------------------------
# Generate data to plot
# ---------------------------------------------------------------------
df = create_synthetic_data()

# Raw styler
raw_styler = raw_styler_object(df)

# With thousands commas + perctange format
styler_with_thousands_commas = styler_with_thousands_commas_object(df)

# +ve and -ve gradients
styler_with_colour_gradients = styler_with_colour_gradients_object(df)

# $ sign
styler_with_dollar_sign = (styler_with_dollar_sign_object(df))

# With medal emoji
styler_with_medal_emoji = (styler_with_medal_emoji_object(df))

# ---------------------------------------------------------------------
# MAIN PANEL
# ---------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.html('<h5>Step 1: Raw dataframe object</h5>')
        st.write('You can see thst streamlit automatically adds commas as thousands separators. OK, but not amazing.')
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
        st.write('Adding a dollar sign (or other characters) is also quite easy')

        with st.expander('See code sample', expanded=False):
            st.code('''
                    def _format_with_dollar_sign(val, prec=0):
                        return f'${val:,.{prec}f}'

                    styler_with_dollar_sign = (df.copy().style
                               .format(_format_with_dollar_sign, subset=['Period_1', 'Period_2', 'Difference'])
                               )
                    ''')

        st.dataframe(styler_with_dollar_sign)

with col2:
    with st.container(border=True):
        st.html('<h5>Step 2: Raw styler object</h5>')
        st.write('The styler messes the UI display. No commas and 6 decimal points')
        st.dataframe(raw_styler)

    with st.container(border=True):
        st.html('<h5>Step 4: +ve & -ve coloured gradients</h5>')
        st.write('We want a green gradient for positive values and a negative '
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
                                            .map(lambda x: _format_positive_negative_background_colour(x, min_value_abs_diff, max_value_abs_diff),
                                                 subset=['Difference'])
                                            .map(lambda x: _format_positive_negative_background_colour(x, min_value_perct_diff, max_value_perct_diff),
                                                 subset=['Percentage Change'])
                                            )
            ''')

        st.dataframe(styler_with_colour_gradients)

    with st.container(border=True):
        st.html('<h5>Step 6: Add column with emojis</h5>')
        st.write('Emojis can also be added! I created a function to add gold, silver, bronze medals given a rank')
        with st.expander('See code sample', expanded=False):
            st.code('''
                    def _add_medal_emoji(val):
                        if val == 1:
                            return f"{val} 🥇"
                        elif val == 2:
                            return f"{val} 🥈"
                        elif val == 3:
                            return f"{val} 🥉"
                        else:
                            return val

                    styler_with_medal_emoji = (df.copy().style
                                               .format(_add_medal_emoji, subset=['Percentage Change rank'])
                                               )
                    ''')

        st.dataframe(styler_with_medal_emoji)
