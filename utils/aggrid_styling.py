from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
import pandas as pd

# Define JsCode for percentage formatting
percentage_formatter = JsCode("""
function(params) {
    if (params.value == null) {
        return '';
    }
    var decimalPoints = params.column.colDef.cellRendererParams.decimalPoints || 2;
    return (params.value * 100).toFixed(decimalPoints) + '%';
}
""")

percentage_getter = JsCode("""
function(params) {
    return params.data[params.colDef.field];
}
""")

# Define JsCode for currency formatting
currency_formatter = JsCode("""
function(params) {
    if (params.value == null || params.value === undefined) {
        return '';
    }
    var decimalPoints = params.column.colDef.cellRendererParams.decimalPoints || 0;
    var currencySymbol = params.column.colDef.cellRendererParams.currencySymbol || '€';
    var value = params.value;

    // Format the number with thousand separators and decimal points
    var formattedNumber = value.toLocaleString('en-US', {
        minimumFractionDigits: decimalPoints,
        maximumFractionDigits: decimalPoints
    });

    return currencySymbol + formattedNumber;
}
""")

currency_getter = JsCode("""
function(params) {
    return params.data[params.colDef.field];
}
""")

# Define JsCode for colouring formatting
cellStyle = JsCode("""
function(params) {
    if (params.value == null || params.value === undefined) {
        return null;
    }

    var val = params.value;
    var minValue = params.column.colDef.cellRendererParams.minValue;
    var maxValue = params.column.colDef.cellRendererParams.maxValue;

    function interpolateColor(color1, color2, factor) {
        var result = color1.slice();
        for (var i = 0; i < 3; i++) {
            result[i] = Math.round(result[i] + factor * (color2[i] - color1[i]));
        }
        return result;
    }

    function getColorForValue(val, minVal, maxVal) {
        if (val > 0) {
            var normalizedVal = val / maxVal;
            var color = interpolateColor([255, 255, 255], [0, 128, 0], Math.pow(normalizedVal, 0.5));
        } else if (val < 0) {
            var normalizedVal = val / minVal;
            var color = interpolateColor([255, 255, 255], [255, 80, 80], Math.pow(normalizedVal, 0.5));
        } else {
            return [255, 255, 255];  // White for zero values
        }
        return color;
    }

    var bgColor = getColorForValue(val, minValue, maxValue);
    var brightness = (bgColor[0] * 299 + bgColor[1] * 587 + bgColor[2] * 114) / 1000;
    var textColor = brightness > 128 ? 'black' : 'white';

    return {
        backgroundColor: 'rgb(' + bgColor.join(',') + ')',
        color: textColor
    };
}
""")

# Define JsCode for emoji formatting
medalFormatter = JsCode("""
function(params) {
    if (params.value == null || params.value === undefined) {
        return '';
    }
    var val = params.value;
    if (val === 1) {
        return val + ' 🥇';
    } else if (val === 2) {
        return val + ' 🥈';
    } else if (val === 3) {
        return val + ' 🥉';
    } else {
        return val;
    }
}
""")


# Wrapping up function
def aggrid_cells_formatting(df):
    grid_builder = GridOptionsBuilder.from_dataframe(df)

    grid_builder.configure_side_bar()
    grid_builder.configure_default_column(filter=True)

    # https://streamlit-aggrid.readthedocs.io/en/docs/GridOptionsBuilder.html#st_aggrid.grid_options_builder.GridOptionsBuilder.configure_column
    # https://www.ag-grid.com/javascript-data-grid/column-properties/

    # The value formatter is only used for adding symbols or formatting stuff.
    # The data used for filter will not be from the valueFormatter.
    # It will actually be from the valueGetter.

    grid_builder.configure_column('Period_1',
                                  header_name='Period 1',
                                  type=['numericColumn', 'numberColumnFilter', 'customNumericFormat'],
                                  valueGetter=currency_getter,
                                  valueFormatter=currency_formatter,
                                  cellRendererParams={'decimalPoints': 0, 'currencySymbol': '€'}
                                  )

    grid_builder.configure_column('Period_2',
                                  header_name='Period 2',
                                  type=['numericColumn', 'numberColumnFilter', 'customNumericFormat'],
                                  valueGetter=currency_getter,
                                  valueFormatter=currency_formatter,
                                  cellRendererParams={'decimalPoints': 0, 'currencySymbol': '€'}
                                  )

    grid_builder.configure_column('Difference',
                                  header_name='Difference',
                                  type=['numericColumn', 'numberColumnFilter', 'customNumericFormat'],
                                  valueGetter=currency_getter,
                                  valueFormatter=currency_formatter,
                                  cellRendererParams={'decimalPoints': 0,
                                                      'currencySymbol': '€',
                                                      },
                                  )

    grid_builder.configure_column('Percentage Change',
                                  header_name='Percentage Change (%)',
                                  type=['numericColumn', 'numberColumnFilter', 'customNumericFormat'],
                                  valueGetter=percentage_getter,
                                  valueFormatter=percentage_formatter,
                                  cellRendererParams={'decimalPoints': 1,
                                                      'minValue': df['Percentage Change'].min(),
                                                      'maxValue': df['Percentage Change'].max()
                                                      },
                                  cellStyle=cellStyle,
                                  )

    grid_builder.configure_column('Percentage Change rank',
                                  header_name='Percentage Change rank',
                                  type=['numericColumn', 'numberColumnFilter', 'customNumericFormat'],
                                  valueFormatter=medalFormatter,
                                  )

    # Build grid options
    gridOptions = grid_builder.build()

    grid_response = AgGrid(df,
                           gridOptions=gridOptions,
                           allow_unsafe_jscode=True,
                           height=min(2000, (len(df)) * 60),  # 38px per row or 500px
                           fit_columns_on_grid_load=False,
                           theme='balham',
                           data_return_mode='FILTERED_AND_SORTED',
                           update_mode='MODEL_CHANGED'
                           )

    # https://streamlit-aggrid.readthedocs.io/en/docs/AgGrid.html
    # Create filtered dataframe
    filtered_df = pd.DataFrame(grid_response['data'])

    return grid_response, filtered_df


def aggrid_aggregation(df):
    grid_builder = GridOptionsBuilder.from_dataframe(df)

    grid_builder.configure_side_bar()
    grid_builder.configure_default_column(filter=True, groupable=True, value=True, enableRowGroup=True, aggFunc="sum")

    # https://streamlit-aggrid.readthedocs.io/en/docs/GridOptionsBuilder.html#st_aggrid.grid_options_builder.GridOptionsBuilder.configure_column
    # https://www.ag-grid.com/javascript-data-grid/column-properties/

    # The value formatter is only used for adding symbols or formatting stuff.
    # The data used for filter will not be from the valueFormatter.
    # It will actually be from the valueGetter.

    grid_builder.configure_column('Month',
                                  header_name='Month',
                                  type=['numericColumn', 'numberColumnFilter'],
                                  aggFunc=None,
                                  )

    grid_builder.configure_column('Country',
                                  header_name='Country',
                                  type=['textColumn', 'stringColumnFilter'],
                                  aggFunc=None,
                                  )

    grid_builder.configure_column('Period_1',
                                  header_name='Period 1',
                                  type=['numericColumn', 'numberColumnFilter', 'customNumericFormat'],
                                  aggFunc="sum",
                                  valueGetter=currency_getter,
                                  valueFormatter=currency_formatter,
                                  cellRendererParams={'decimalPoints': 0, 'currencySymbol': '€'}
                                  )

    grid_builder.configure_column('Period_2',
                                  header_name='Period 2',
                                  type=['numericColumn', 'numberColumnFilter', 'customNumericFormat'],
                                  aggFunc="sum",
                                  valueGetter=currency_getter,
                                  valueFormatter=currency_formatter,
                                  cellRendererParams={'decimalPoints': 0, 'currencySymbol': '€'}
                                  )

    grid_builder.configure_column('Difference',
                                  header_name='Difference',
                                  type=['numericColumn', 'numberColumnFilter', 'customNumericFormat'],
                                  aggFunc="sum",
                                  valueGetter=currency_getter,
                                  valueFormatter=currency_formatter,
                                  cellRendererParams={'decimalPoints': 0,
                                                      'currencySymbol': '€',
                                                      },
                                  )

    grid_builder.configure_column('Percentage Change',
                                  header_name='Percentage Change (%)',
                                  type=['numericColumn', 'numberColumnFilter', 'customNumericFormat'],
                                  aggFunc="avg",
                                  valueGetter=percentage_getter,
                                  valueFormatter=percentage_formatter,
                                  cellRendererParams={'decimalPoints': 1,
                                                      },
                                  )

    grid_builder.configure_column('Percentage Change rank',
                                  header_name='Percentage Change rank',
                                  type=['numericColumn', 'numberColumnFilter', 'customNumericFormat'],
                                  aggFunc="avg",
                                  valueFormatter=medalFormatter,
                                  )

    # Build grid options
    gridOptions = grid_builder.build()

    grid_response = AgGrid(df,
                           gridOptions=gridOptions,
                           allow_unsafe_jscode=True,
                           height=min(2000, (len(df)) * 60),  # 38px per row or 500px
                           fit_columns_on_grid_load=False,
                           theme='balham'
                           )

    # https://streamlit-aggrid.readthedocs.io/en/docs/AgGrid.html
    return grid_response
