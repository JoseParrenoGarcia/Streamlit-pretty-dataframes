from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

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


grid_options = {
    'autoSizeStrategy':
        {'type': 'fitCellContents',}
}


# Wrapping up function
def aggrid_cells_formatting(df):
    grid_builder = GridOptionsBuilder.from_dataframe(df)

    grid_builder.configure_grid_options(**grid_options)

    grid_builder.configure_default_column(filter=True)

    # https://streamlit-aggrid.readthedocs.io/en/docs/GridOptionsBuilder.html#st_aggrid.grid_options_builder.GridOptionsBuilder.configure_column
    # https://www.ag-grid.com/javascript-data-grid/column-properties/

    # The value formatter is only used for adding symbols or formatting stuff.
    # The data used for filter will not be from the valueFormatter.
    # It will actually be from the valueGetter.

    grid_builder.configure_column('Percentage Change',
                                  header_name='Percentage Change (%)',
                                  type=['numericColumn', 'numberColumnFilter', 'customNumericFormat'],
                                  valueGetter=percentage_getter,
                                  valueFormatter=percentage_formatter,
                                  cellRendererParams={'decimalPoints': 1}
                                  )

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
                                  cellRendererParams={'decimalPoints': 0, 'currencySymbol': '€'}
                                  )

    # Build grid options
    gridOptions = grid_builder.build()

    grid_response = AgGrid(df,
                           gridOptions=gridOptions,
                           allow_unsafe_jscode=True,
                           height=min(500, (len(df)) * 38),  # 38px per row or 500px
                           fit_columns_on_grid_load=False,
                           theme='balham')  # Theme can be changed

    # https://streamlit-aggrid.readthedocs.io/en/docs/AgGrid.html
    return grid_response
