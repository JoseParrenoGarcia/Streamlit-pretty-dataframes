import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


thousands_cols = ['Period_1', 'Period_2', 'Difference']
perct_cols = ['Percentage Change']


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


# Add gold, silver, bronze medal emoji
def _add_medal_emoji(val):
    if val == 1:
        return f"{val} 🥇"
    elif val == 2:
        return f"{val} 🥈"
    elif val == 3:
        return f"{val} 🥉"
    else:
        return val


def raw_styler_object(df):
    return df.copy().style


def styler_with_thousands_commas_object(df):
    return (df.copy().style
            .format(_format_with_thousands_commas, subset=thousands_cols)
            .format(lambda x: _format_as_percentage(x, 2), subset=perct_cols)
            )


def styler_with_colour_gradients_object(df):
    min_value_abs_diff = df['Difference'].min()
    max_value_abs_diff = df['Difference'].max()

    min_value_perct_diff = df['Percentage Change'].min()
    max_value_perct_diff = df['Percentage Change'].max()

    return (styler_with_thousands_commas_object(df)
            .format(_format_with_thousands_commas, subset=thousands_cols)
            .format(lambda x: _format_as_percentage(x, 2), subset=perct_cols)
            .map(lambda x: _format_positive_negative_background_colour(x, min_value_abs_diff, max_value_abs_diff),
                 subset=['Difference'])
            .map(lambda x: _format_positive_negative_background_colour(x, min_value_perct_diff, max_value_perct_diff),
                 subset=['Percentage Change'])
            )


def styler_with_dollar_sign_object(df):
    return (styler_with_colour_gradients_object(df)
            .format(_format_with_dollar_sign, subset=['Period_1', 'Period_2', 'Difference']))


def styler_with_medal_emoji_object(df):
    return (styler_with_dollar_sign_object(df)
            .format(_add_medal_emoji, subset=['Percentage Change rank'])
            )
